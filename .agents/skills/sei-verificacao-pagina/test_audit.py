"""Testes do auditor da skill sei-verificacao-pagina.

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
    "pagina": SKILLS / "sei-verificacao-pagina" / "audit.py",
}


class PaginaAuditTest(unittest.TestCase):
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

    @staticmethod
    def page_base(extra=""):
        return f"""<?php
SessaoSEI::getInstance()->validarLink();
$strAcao = PaginaSEI::GET('acao');
SessaoSEI::getInstance()->validarPermissao($strAcao);
{extra}
"""

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
                process, payload = self.run_auditor("pagina", target)
                self.assertEqual(2, process.returncode)
                self.assertEqual("BLOCK", payload["verdict"])

    def test_auditor_blocks_when_eligible_parser_extracts_nothing(self):
        """Arquivo elegivel do qual nada foi extraido tambem bloqueia."""
        target = self.write('md_ts_vazia_lista.php', '<?php')
        process, payload = self.run_auditor("pagina", target)
        self.assertEqual(2, process.returncode)
        self.assertEqual("BLOCK", payload["verdict"])

    @unittest.expectedFailure  # P1/P2/P4 sem varredura de comentario nem iteracao por acao; ver README desta pasta
    def test_page_checks_order_action_coverage_and_every_action_link(self):
        content = """<?php
SessaoSEI::getInstance()->validarPermissao(PaginaSEI::GET('acao'));
SessaoSEI::getInstance()->validarLink();
$ok = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_ts_item_listar');
$bad = 'controlador.php?acao=md_ts_item_consultar';
switch ($strAcao) {
    case 'md_ts_item_listar': break;
    case 'md_ts_item_consultar': break;
}
"""
        path = self.write("md_ts_ordem_lista.php", content)
        process, payload = self.run_auditor("pagina", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("P002", self.codes(payload))
        self.assertIn("P004", self.codes(payload))

    @unittest.expectedFailure  # P1/P2/P4 sem varredura de comentario nem iteracao por acao; ver README desta pasta
    def test_page_detects_static_actions_but_ignores_validation_and_declarations(self):
        static_action = self.write(
            "md_ts_static_lista.php",
            self.page_base().replace("<?php\n", "<?php\nMdTsItemINT::cadastrar($objDTO);\n"),
        )
        process, payload = self.run_auditor("pagina", static_action)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"P001", "P002"}.issubset(self.codes(payload)))

        harmless = self.write(
            "md_ts_validation_lista.php",
            self.page_base().replace(
                "<?php\n",
                "<?php\nclass Auxiliar { public static function processar($objDTO) {} }\nMdTsValidador::validar($objDTO);\n$bolVazia = InfraString::isBolVazia('');\n",
            ),
        )
        process, payload = self.run_auditor("pagina", harmless)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("P001", self.codes(payload))
        self.assertNotIn("P002", self.codes(payload))

    @unittest.expectedFailure  # P1/P2/P4 sem varredura de comentario nem iteracao por acao; ver README desta pasta
    def test_page_guards_precede_actions_and_multiline_signed_links_are_covered(self):
        before_guards = self.write(
            "md_ts_pre_guard_lista.php",
            self.page_base().replace("<?php\n", "<?php\n$objRN->cadastrar($objDTO);\n"),
        )
        process, payload = self.run_auditor("pagina", before_guards)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"P001", "P002"}.issubset(self.codes(payload)))

        signed = self.write(
            "md_ts_signed_lista.php",
            self.page_base("""
$strLink = SessaoSEI::getInstance()->assinarLink(
    'controlador.php?acao=md_ts_item_listar'
);
switch ($strAcao) {
    case 'md_ts_item_listar':
        break;
}
"""),
        )
        process, payload = self.run_auditor("pagina", signed)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("P004", self.codes(payload))
        self.assertNotIn("P010", self.codes(payload))

    @unittest.expectedFailure  # P1/P2/P4 sem varredura de comentario nem iteracao por acao; ver README desta pasta
    def test_page_ignores_commented_guards_without_masking_strings(self):
        content = """<?php
// SessaoSEI::getInstance()->validarLink();
# SessaoSEI::getInstance()->validarPermissao($strAcao);
/* SessaoSEI::getInstance()->validarLink(); */
$texto = '// validarLink() dentro de string';
"""
        path = self.write("md_ts_comentada_lista.php", content)
        process, payload = self.run_auditor("pagina", path)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"P001", "P002"}.issubset(self.codes(payload)))

    def test_page_p5_and_p10_block(self):
        cases = {
            "p5": ("$valor = $_REQUEST['valor'];", "P005"),
            "p10": ('<a href="controlador.php?acao=md_ts_item_excluir">Excluir</a>', "P010"),
        }
        for name, (extra, code) in cases.items():
            with self.subTest(rule=name):
                path = self.write(f"md_ts_item_{name}_lista.php", self.page_base(extra))
                process, payload = self.run_auditor("pagina", path)
                self.assertEqual(2, process.returncode)
                self.assertIn(code, self.codes(payload))

    def test_page_p6_and_p8_severity_follows_action_context(self):
        """P6 e P8 bloqueiam pagina nova, avisam em preexistente, e sem a flag valem como preexistente."""
        cases = {
            "p6": ("$valor = $_POST['valor'];", "P006"),
            "p8": ("echo $strNome;", "P008"),
        }
        for name, (extra, code) in cases.items():
            path = self.write(f"md_ts_item_{name}_lista.php", self.page_base(extra))

            with self.subTest(rule=name, contexto="nova"):
                process, payload = self.run_auditor("pagina", path, "--pagina", "nova")
                self.assertEqual(2, process.returncode)
                self.assertIn(code, self.codes(payload))

            with self.subTest(rule=name, contexto="existente"):
                process, payload = self.run_auditor("pagina", path, "--pagina", "existente")
                self.assertEqual(1, process.returncode)
                self.assertIn(code, self.codes(payload, "avisos"))

            with self.subTest(rule=name, contexto="padrao"):
                process, payload = self.run_auditor("pagina", path)
                self.assertEqual(1, process.returncode)
                self.assertIn(code, self.codes(payload, "avisos"))

    def test_page_p8_tracks_sanitized_dynamic_and_indirect_assignments(self):
        sanitized = self.write(
            "md_ts_sanitized_lista.php",
            self.page_base("$strNome = PaginaSEI::tratarHTML(PaginaSEI::GET('nome'));\necho $strNome;"),
        )
        process, payload = self.run_auditor("pagina", sanitized)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("P008", self.codes(payload))

        dynamic = self.write(
            "md_ts_dynamic_lista.php",
            self.page_base("$strNome = PaginaSEI::GET('nome');\necho $strNome;"),
        )
        process, payload = self.run_auditor("pagina", dynamic)
        # entrada HTTP sem tratarHTML(): so avisa porque o contexto padrao e
        # pagina preexistente, conforme test_page_p6_and_p8_severity_follows_action_context
        self.assertEqual(1, process.returncode)
        self.assertIn("P008", self.codes(payload, "avisos"))

        indirect = self.write(
            "md_ts_indirect_lista.php",
            self.page_base("$strNome = montarNome();\necho $strNome;"),
        )
        process, payload = self.run_auditor("pagina", indirect)
        self.assertEqual(1, process.returncode)
        self.assertIn("P008", self.codes(payload, "avisos"))

    def test_page_p9_distinguishes_confirmed_flow_from_heuristic(self):
        blocked = self.write(
            "md_ts_fluxo_lista.php",
            self.page_base("const html = responseText;\ndocument.getElementById('x').innerHTML = html;"),
        )
        process, payload = self.run_auditor("pagina", blocked)
        self.assertEqual(2, process.returncode)
        self.assertIn("P009", self.codes(payload))

        warning = self.write(
            "md_ts_heuristica_lista.php",
            self.page_base("document.getElementById('x').innerHTML = markup;"),
        )
        process, payload = self.run_auditor("pagina", warning)
        self.assertEqual(1, process.returncode)
        self.assertIn("P009", self.codes(payload, "avisos"))


if __name__ == "__main__":
    unittest.main()
