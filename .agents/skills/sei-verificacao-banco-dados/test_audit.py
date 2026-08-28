"""Testes do auditor da skill sei-verificacao-banco-dados.

Independente de proposito: nao importa helper de outra skill nem de pasta
compartilhada. A duplicacao de andaime e o preco de a skill ser portavel.

    python3 -m unittest test_audit
"""

import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / ".agents" / "skills"
AUDITORS = {
    "banco": SKILLS / "sei-verificacao-banco-dados" / "audit.py",
}


class BancoDadosAuditTest(unittest.TestCase):
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
                process, payload = self.run_auditor("banco", target)
                self.assertEqual(2, process.returncode)
                self.assertEqual("BLOCK", payload["verdict"])

    def test_auditor_blocks_when_eligible_parser_extracts_nothing(self):
        """Arquivo elegivel do qual nada foi extraido tambem bloqueia."""
        target = self.write('modelo.sql', 'SELECT 1;')
        process, payload = self.run_auditor("banco", target)
        self.assertEqual(2, process.returncode)
        self.assertEqual("BLOCK", payload["verdict"])

    def test_database_associates_constraints_and_checks_all_name_limits(self):
        ddl = """
CREATE TABLE md_ts_parent (
    id_md_ts_parent INTEGER,
    CONSTRAINT pk_md_ts_parent PRIMARY KEY (id_md_ts_parent)
);
CREATE TABLE md_ts_child (
    id_md_ts_child INTEGER,
    id_md_ts_parent INTEGER,
    coluna_com_nome_muito_maior_que_limite VARCHAR(10),
    CONSTRAINT pk_md_ts_child PRIMARY KEY (id_md_ts_child),
    CONSTRAINT fk_md_ts_child_md_ts_parent_nome_longo FOREIGN KEY (id_md_ts_parent) REFERENCES md_ts_parent (id_md_ts_parent),
    CONSTRAINT ak_md_ts_child_nome_alternativo_longo UNIQUE (id_md_ts_parent)
);
CREATE INDEX indice_md_ts_child_com_nome_muito_longo ON md_ts_child (id_md_ts_parent);
CREATE SEQUENCE seq_md_ts_child_com_nome_muito_longo;
CREATE TABLE md_ts_entidade_com_nome_muito_longo (
    id_md_ts_entidade_com_nome_muito_longo INTEGER
);
CREATE TABLE md_ts_pk (
    id_md_ts_pk INTEGER,
    CONSTRAINT pk_md_ts_pk_com_nome_de_constraint_longo PRIMARY KEY (id_md_ts_pk)
);
"""
        path = self.write("limites.sql", ddl)
        process, payload = self.run_auditor("banco", path)
        self.assertEqual(2, process.returncode)
        parent = next(result for result in payload["results"] if result["entidade"] == "md_ts_parent")
        child = next(result for result in payload["results"] if result["entidade"] == "md_ts_child")
        self.assertNotIn("DB03", {error["regra"] for error in parent["erros"]})
        messages = "\n".join(error["mensagem"] for error in child["erros"] if error["regra"] == "DB03")
        for kind in ("coluna", "indice", "constraint FK", "constraint AK"):
            self.assertIn(kind, messages)
        all_messages = "\n".join(
            error["mensagem"]
            for result in payload["results"]
            for error in result["erros"]
            if error["regra"] == "DB03"
        )
        for kind in ("Tabela", "constraint PK", "sequence"):
            self.assertIn(kind, all_messages)

    def test_database_composite_pk_exact_pk_related_column_and_evidence(self):
        invalid = """<?php
class MdTsItemDTO extends InfraDTO {
    public function getStrNomeTabela() { return 'md_ts_item'; }
    public function montar() {
        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdA', 'id_md_ts_a');
        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdB', 'id_md_ts_b');
        $this->configurarPK('IdA', InfraDTO::$TIPO_PK_INFORMADO);
        $this->configurarPK('IdB', InfraDTO::$TIPO_PK_INFORMADO);
        $this->configurarFK('IdA', 'md_ts_a', 'id_md_ts_a');
        $this->configurarFK('IdB', 'md_ts_b', 'id_md_ts_b');
        $this->adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, 'NomeA', 'a.NomeInvalido', 'md_ts_a a');
    }
}
"""
        path = self.write("MdTsItemDTO.php", invalid)
        process, payload = self.run_auditor("banco", path)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"DB02", "DB08"}.issubset({error["regra"] for error in payload["results"][0]["erros"]}))
        for issue in payload["results"][0]["erros"] + payload["results"][0]["avisos"]:
            self.assertTrue(issue["arquivo"])
            self.assertIsInstance(issue["linha"], int)

        relation = self.write(
            "MdTsRelItemDTO.php",
            invalid.replace("MdTsItemDTO", "MdTsRelItemDTO")
            .replace("md_ts_item", "md_ts_rel_a_b")
            .replace("a.NomeInvalido", "a.nome"),
        )
        process, payload = self.run_auditor("banco", relation)
        rules = {error["regra"] for error in payload["results"][0]["erros"]}
        self.assertNotIn("DB02", rules)
        self.assertNotIn("DB04", rules)
        self.assertNotIn("DB08", rules)

        wrong_pk = self.write(
            "MdTsWrongPkDTO.php",
            """<?php
class MdTsWrongPkDTO extends InfraDTO {
    public function getStrNomeTabela() { return 'md_ts_item'; }
    public function montar() {
        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdItem', 'id_md_ts_outro');
        $this->configurarPK('IdItem', InfraDTO::$TIPO_PK_NATIVA);
    }
}
""",
        )
        process, payload = self.run_auditor("banco", wrong_pk)
        self.assertEqual(2, process.returncode)
        self.assertIn("DB04", {error["regra"] for error in payload["results"][0]["erros"]})

    def test_database_db04_requires_generation_evidence_for_simple_pk(self):
        informed = """CREATE TABLE md_ts_item (
    codigo INTEGER,
    CONSTRAINT pk_md_ts_item PRIMARY KEY (codigo)
);"""
        path = self.write("informed.sql", informed)
        process, payload = self.run_auditor("banco", path)
        self.assertNotIn("DB04", {error["regra"] for error in payload["results"][0]["erros"]})

        generated = self.write("generated.sql", informed + "\nCREATE SEQUENCE seq_md_ts_item;")
        process, payload = self.run_auditor("banco", generated)
        self.assertEqual(2, process.returncode)
        self.assertIn("DB04", {error["regra"] for error in payload["results"][0]["erros"]})

        composite = self.write(
            "composite.sql",
            """CREATE TABLE md_ts_rel_a_b (
    id_md_ts_a INTEGER,
    id_md_ts_b INTEGER,
    CONSTRAINT pk_md_ts_rel_a_b PRIMARY KEY (id_md_ts_a, id_md_ts_b)
);
CREATE SEQUENCE seq_md_ts_rel_a_b;""",
        )
        process, payload = self.run_auditor("banco", composite)
        self.assertNotIn("DB04", {error["regra"] for error in payload["results"][0]["erros"]})

    def test_database_db05_checks_owner_reference_and_each_constraint_line(self):
        ddl = """CREATE TABLE md_ts_item (
    id_md_ts_item INTEGER,
    id_usuario INTEGER,
    id_grupo INTEGER,
    CONSTRAINT pk_md_ts_item PRIMARY KEY (id_md_ts_item),
    CONSTRAINT fk_md_ts_outra_coisa FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario),
    CONSTRAINT FK_MD_TS_ITEM_GRUPO FOREIGN KEY (id_grupo) REFERENCES grupo (id_grupo),
    CONSTRAINT fk_md_ts_item_usuario FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);"""
        path = self.write("constraints.sql", ddl)
        process, payload = self.run_auditor("banco", path)
        self.assertEqual(2, process.returncode)
        issues = {
            next(name for name in ("fk_md_ts_outra_coisa", "FK_MD_TS_ITEM_GRUPO") if name in error["mensagem"]): error
            for error in payload["results"][0]["erros"]
            if error["regra"] == "DB05"
        }
        self.assertEqual(6, issues["fk_md_ts_outra_coisa"]["linha"])
        self.assertEqual(7, issues["FK_MD_TS_ITEM_GRUPO"]["linha"])
        self.assertNotIn("fk_md_ts_item_usuario", "\n".join(error["mensagem"] for error in issues.values()))

    def test_database_db05_validates_each_constraint_against_its_own_reference(self):
        ddl = """CREATE TABLE md_ts_item (
    id_md_ts_item INTEGER,
    id_usuario INTEGER,
    id_grupo INTEGER,
    CONSTRAINT pk_md_ts_item PRIMARY KEY (id_md_ts_item),
    CONSTRAINT fk_md_ts_item_usuario FOREIGN KEY (id_grupo) REFERENCES grupo (id_grupo),
    CONSTRAINT fk_md_ts_item_grupo FOREIGN KEY (id_usuario) REFERENCES usuario (id_usuario)
);"""
        path = self.write("swapped_constraints.sql", ddl)
        process, payload = self.run_auditor("banco", path)
        self.assertEqual(2, process.returncode)
        messages = "\n".join(error["mensagem"] for error in payload["results"][0]["erros"] if error["regra"] == "DB05")
        self.assertIn("fk_md_ts_item_usuario", messages)
        self.assertIn("fk_md_ts_item_grupo", messages)

    def test_database_db08_blocks_actual_text_type(self):
        ddl = """CREATE TABLE md_ts_item (
    id_md_ts_item INTEGER,
    str_conteudo TEXT,
    CONSTRAINT pk_md_ts_item PRIMARY KEY (id_md_ts_item)
);"""
        path = self.write("text.sql", ddl)
        process, payload = self.run_auditor("banco", path)
        self.assertEqual(2, process.returncode)
        issue = next(error for error in payload["results"][0]["erros"] if error["regra"] == "DB08")
        self.assertIn("text", issue["mensagem"])
        self.assertEqual(3, issue["linha"])

        literal = self.write(
            "text_literal.sql",
            """CREATE TABLE md_ts_item (
    id_md_ts_item INTEGER,
    str_conteudo VARCHAR(20) DEFAULT 'text',
    CONSTRAINT pk_md_ts_item PRIMARY KEY (id_md_ts_item)
);""",
        )
        process, payload = self.run_auditor("banco", literal)
        self.assertNotIn("DB08", {error["regra"] for error in payload["results"][0]["erros"]})

    def test_database_documentation_uses_db_ids_for_modeling_rules(self):
        reference = (SKILLS / "sei-verificacao-banco-dados" / "references" / "padroes-manual-md.md").read_text(encoding="utf-8")
        self.assertNotRegex(reference, r"(?:###|\|)\s*R(?:1[0-5]|[1-9])\b")
        self.assertNotIn("R1-R15", reference)

        dto_checklist = (ROOT / ".agents" / "checklists" / "checklist-dto-infraphp-sei.md").read_text(encoding="utf-8")
        self.assertIn("DB01-DB15", dto_checklist)
        self.assertIsNone(re.search(r"`R(?:1[0-5]|[1-9])`", dto_checklist))

    def test_database_generated_identity_triggers_db04_and_db08(self):
        ddl = """CREATE TABLE md_ts_item (
    codigo INTEGER GENERATED ALWAYS AS IDENTITY,
    CONSTRAINT pk_md_ts_item PRIMARY KEY (codigo)
);"""
        path = self.write("identity.sql", ddl)
        process, payload = self.run_auditor("banco", path)
        self.assertEqual(2, process.returncode)
        rules = {error["regra"] for error in payload["results"][0]["erros"]}
        self.assertTrue({"DB04", "DB08"}.issubset(rules))
        self.assertTrue(any("identity" in error["mensagem"] for error in payload["results"][0]["erros"] if error["regra"] == "DB08"))

    def test_database_ignores_declared_temporary_table_and_accepts_isolated_bd(self):
        ddl = """
CREATE TEMPORARY TABLE md_ts_temporaria (coluna_invalida_com_nome_muito_longo INTEGER);
CREATE TABLE md_ts_item (
    id_md_ts_item INTEGER,
    CONSTRAINT pk_md_ts_item PRIMARY KEY (id_md_ts_item)
);
"""
        path = self.write("temporaria.sql", ddl)
        process, payload = self.run_auditor("banco", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertEqual(["md_ts_item"], [result["entidade"] for result in payload["results"]])

        bd = self.write("MdTsItemBD.php", "<?php class MdTsItemBD extends InfraBD {}")
        process, payload = self.run_auditor("banco", bd)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertEqual("md_ts_item", payload["results"][0]["entidade"])

    def test_database_merges_dto_bd_and_reports_constraint_source(self):
        module = self.work / "modulo"
        dto = self.write(
            "modulo/dto/MdTsItemDTO.php",
            """<?php
class MdTsItemDTO extends InfraDTO {
    public function getStrNomeTabela() { return 'md_ts_item'; }
    public function montar() {
        $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdItem', 'id_md_ts_item');
        $this->configurarPK('IdItem', InfraDTO::$TIPO_PK_NATIVA);
    }
}
""",
        )
        bd = self.write(
            "modulo/bd/MdTsItemBD.php",
            """<?php
class MdTsItemBD extends InfraBD {
    private const FK = 'FK_MD_TS_ITEM_PARENT';
}
""",
        )
        process, payload = self.run_auditor("banco", module)
        self.assertEqual(2, process.returncode)
        self.assertEqual(1, len(payload["results"]))
        result = payload["results"][0]
        self.assertEqual({str(dto), str(bd)}, set(result["arquivos"]))
        issue = next(error for error in result["erros"] if error["regra"] == "DB05")
        self.assertEqual(str(bd), issue["arquivo"])
        self.assertEqual(3, issue["linha"])

    def test_database_parses_incremental_helpers_with_both_array_syntaxes(self):
        content = """<?php
$objInfraMetaBD->adicionarColuna('md_ts_item', 'str_nome', $objInfraMetaBD->tipoTextoVariavel(50), 'NULL');
$objInfraMetaBD->adicionarChavePrimaria('md_ts_item', 'pk_md_ts_item', array('id_md_ts_item'));
$objInfraMetaBD->criarIndice('md_ts_item', 'i01_md_ts_item', ['str_nome']);
"""
        path = self.write("sei_atualizar_versao_modulo_ts.php", content)
        process, payload = self.run_auditor("banco", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertEqual("md_ts_item", payload["results"][0]["entidade"])

        incremental = self.write(
            "incremental.sql",
            "ALTER TABLE md_ts_item ADD str_codigo VARCHAR(20);\nCREATE INDEX i01_md_ts_item ON md_ts_item (str_codigo);",
        )
        process, payload = self.run_auditor("banco", incremental)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertEqual("md_ts_item", payload["results"][0]["entidade"])

    def test_database_parses_simple_multiple_and_sequence_only_ddl(self):
        ddl = """
CREATE TABLE md_ts_item (
    id_md_ts_item INTEGER,
    str_nome VARCHAR(20),
    CONSTRAINT pk_md_ts_item PRIMARY KEY (id_md_ts_item)
);
CREATE TABLE md_ts_grupo (
    id_md_ts_grupo INTEGER,
    CONSTRAINT pk_md_ts_grupo PRIMARY KEY (id_md_ts_grupo)
);
"""
        path = self.write("modelo.sql", ddl)
        process, payload = self.run_auditor("banco", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertEqual(2, len(payload["results"]))

        sequence = self.write("sequence.sql", "CREATE SEQUENCE seq_md_ts_item;")
        process, payload = self.run_auditor("banco", sequence)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertEqual(1, len(payload["results"]))


if __name__ == "__main__":
    unittest.main()
