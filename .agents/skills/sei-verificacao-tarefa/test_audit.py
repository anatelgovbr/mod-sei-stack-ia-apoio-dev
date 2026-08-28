"""Testes do auditor da skill sei-verificacao-tarefa.

Independente de proposito: nao importa helper de outra skill nem de pasta
compartilhada. A duplicacao de andaime e o preco de a skill ser portavel.

    python3 -m unittest test_audit
"""

import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / ".agents" / "skills"
AUDITORS = {
    "tarefa": SKILLS / "sei-verificacao-tarefa" / "audit.py",
}


class TarefaAuditTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def write(self, name, content):
        path = self.work / name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")
        return path

    def run_auditor(self, name, target, *extra):
        process = subprocess.run(
            [sys.executable, str(AUDITORS[name]), "--input", str(target), "--format", "json", "--exit-code", *extra],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertTrue(process.stdout, process.stderr)
        return process, json.loads(process.stdout)

    @staticmethod
    def codes(payload, field="erros"):
        return {
            issue["codigo"]
            for result in payload.get("results", [])
            for issue in result.get(field, [])
        }

    def test_auditor_fails_closed_for_missing_incompatible_and_empty_input(self):
        """Entrada que o auditor nao consegue ler tem de bloquear, nunca passar.

        Detector falha verde: se ele nao reconhece o arquivo, devolve PASS e
        parece que esta tudo bem. Este teste existe em todas as skills de
        verificacao, com a mesma forma, de proposito.
        """
        incompatible = self.write("arquivo.txt", "sem artefato")
        empty = self.work / "vazio"
        empty.mkdir()
        missing = self.work / "inexistente"
        for target in (missing, incompatible, empty):
            with self.subTest(target=target.name):
                process, payload = self.run_auditor("tarefa", target)
                self.assertEqual(2, process.returncode)
                self.assertEqual("BLOCK", payload["verdict"])

    def test_auditor_blocks_when_eligible_parser_extracts_nothing(self):
        """Arquivo elegivel do qual nada foi extraido tambem bloqueia."""
        target = self.write('md_ts_tarefa.php', '<?php return [];')
        process, payload = self.run_auditor("tarefa", target)
        self.assertEqual(2, process.returncode)
        self.assertEqual("BLOCK", payload["verdict"])

    def test_task_example_arrays_and_setters_are_accepted(self):
        example = SKILLS / "sei-verificacao-tarefa" / "examples" / "scripts" / "md_ri_tarefa.php.example"
        process, payload = self.run_auditor("tarefa", example)
        self.assertEqual(0, process.returncode, payload)

        content = """<?php
$tarefas = array(1001 => 'MD_TS_ITEM_CADASTRAR');
$tarefasNovas = [1002 => 'MD_TS_ITEM_ALTERAR'];
$objTarefaDTO->setNumIdTarefa(1003);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_EXCLUIR');
"""
        path = self.write("md_ts_tarefa.php", content)
        process, payload = self.run_auditor("tarefa", path)
        self.assertEqual(0, process.returncode, payload)

    def test_task_ignores_comments_and_blocks_incomplete_records(self):
        commented = self.write(
            "md_ts_comentada_tarefa.php",
            """<?php
// ['id_tarefa' => 1001, 'id_tarefa_modulo' => 'MD_TS_COMENTADA']
/* ['id_tarefa' => 1002, 'id_tarefa_modulo' => 'MD_TS_BLOCO'] */
""",
        )
        process, payload = self.run_auditor("tarefa", commented)
        self.assertEqual(2, process.returncode)
        self.assertEqual("K000", payload["results"][0]["erros"][0]["codigo"])

        incomplete = self.write(
            "md_ts_incompleta_tarefa.php",
            """<?php
return [
    ['id_tarefa' => 1001],
    ['id_tarefa_modulo' => 'MD_TS_SEM_NUMERO'],
    ['id_tarefa' => $id, 'id_tarefa_modulo' => 'MD_TS_VARIAVEL']
];
""",
        )
        process, payload = self.run_auditor("tarefa", incomplete)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"K001", "K003"}.issubset(self.codes(payload)))
        for issue in payload["results"][0]["erros"]:
            self.assertIsInstance(issue.get("linha"), int)

    def test_task_pairs_records_checks_cross_file_duplicates_and_reports_lines(self):
        first = self.write(
            "tarefas/md_ts_a_tarefa.php",
            """<?php
return [
    ['id_tarefa' => 1001, 'id_tarefa_modulo' => 'MD_TS_ITEM_LISTAR'],
    ['id_tarefa' => 1002, 'id_tarefa_modulo' => 'MD_TS_ITEM_ALTERAR']
];
""",
        )
        self.write(
            "tarefas/md_ts_b_tarefa.php",
            """<?php
$objTarefaDTO->setNumIdTarefa(1003);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_LISTAR');
""",
        )
        process, payload = self.run_auditor("tarefa", first.parent)
        self.assertEqual(2, process.returncode)
        self.assertEqual(3, sum(len(result["tarefas"]) for result in payload["results"]))
        duplicate = next(
            issue
            for result in payload["results"]
            for issue in result["erros"]
            if issue["codigo"] == "K006"
        )
        self.assertIsInstance(duplicate["linha"], int)
        self.assertEqual("md_ts_b_tarefa.php", duplicate["file"])

        markdown = subprocess.run(
            [sys.executable, str(AUDITORS["tarefa"]), "--input", str(first.parent), "--format", "markdown", "--exit-code"],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(2, markdown.returncode)
        self.assertRegex(markdown.stdout, r"K006.*\(linha 3\)")

        empty_description = self.write(
            "md_ts_empty_65_tarefa.php",
            "<?php return [['id_tarefa' => 65, 'id_tarefa_modulo' => 'MD_TS_LIVRE', 'DESCRICAO' => '  ']];",
        )
        process, payload = self.run_auditor("tarefa", empty_description)
        self.assertEqual(2, process.returncode)
        self.assertIn("K007", self.codes(payload))

        valid_description = self.write(
            "md_ts_valid_65_tarefa.php",
            "<?php return [['id_tarefa' => 65, 'id_tarefa_modulo' => 'MD_TS_LIVRE', 'DESCRICAO' => 'Texto livre']];",
        )
        process, payload = self.run_auditor("tarefa", valid_description)
        self.assertEqual(0, process.returncode, payload)

        lowercase = self.write(
            "md_ts_65_lower_tarefa.php",
            "<?php return [['id_tarefa' => 65, 'id_tarefa_modulo' => 'MD_TS_LIVRE', 'descricao' => 'texto']];",
        )
        process, payload = self.run_auditor("tarefa", lowercase)
        self.assertEqual(2, process.returncode)
        self.assertIn("K007", self.codes(payload))

    def test_task_separates_identifiers_checks_duplicates_and_id65(self):
        invalid = """<?php
return [
    ['id_tarefa' => 999, 'id_tarefa_modulo' => 'invalido'],
    ['id_tarefa' => 1001, 'id_tarefa_modulo' => 'MD_TS_ITEM'],
    ['id_tarefa' => 1001, 'id_tarefa_modulo' => 'MD_TS_ITEM']
];
"""
        path = self.write("md_ts_tarefa.php", invalid)
        process, payload = self.run_auditor("tarefa", path)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"K001", "K003", "K006"}.issubset(self.codes(payload)))

        id65 = self.write(
            "md_ts_65_tarefa.php",
            "<?php return [['id_tarefa' => 65, 'id_tarefa_modulo' => 'MD_TS_LIVRE']];",
        )
        process, payload = self.run_auditor("tarefa", id65)
        self.assertEqual(2, process.returncode)
        self.assertIn("K007", self.codes(payload))


if __name__ == "__main__":
    unittest.main()
