"""Testes do auditor da skill sei-verificacao-controladores.

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
    "controladores": SKILLS / "sei-verificacao-controladores" / "audit.py",
}


class ControladoresAuditTest(unittest.TestCase):
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
                process, payload = self.run_auditor("controladores", target)
                self.assertEqual(2, process.returncode)
                self.assertEqual("BLOCK", payload["verdict"])

    def test_auditor_blocks_when_eligible_parser_extracts_nothing(self):
        """Arquivo elegivel do qual nada foi extraido tambem bloqueia."""
        target = self.write('MdTsIntegracao.php', '<?php class MdTsIntegracao extends SeiIntegracao {}')
        process, payload = self.run_auditor("controladores", target)
        self.assertEqual(2, process.returncode)
        self.assertEqual("BLOCK", payload["verdict"])

    def test_controller_ci1_requires_restrictive_pattern_in_method_body(self):
        template = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function tratarLinkSemAssinatura($strLink) {
        %s
    }
}
"""
        for name, statement in (
            ("permissive", "return preg_match('/.*/', $strLink) === 1;"),
            ("ungrouped_alternation", "return preg_match('/^md_ts_|qualquer$/', $strLink) === 1;"),
            ("commented", "// preg_match('/^md_ts_[a-z_]+$/', $strLink);\n        return true;"),
        ):
            with self.subTest(case=name):
                path = self.write(f"MdTs{name.title()}Integracao.php", template % statement)
                process, payload = self.run_auditor("controladores", path)
                self.assertEqual(2, process.returncode)
                self.assertIn("CI001", self.codes(payload))

        path = self.write("MdTsRestritivaIntegracao.php", template % "return preg_match('/^md_ts_[a-z_]+$/', $strLink) === 1;")
        process, payload = self.run_auditor("controladores", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("CI001", self.codes(payload))

        path = self.write("MdTsGroupedIntegracao.php", template % "return preg_match('/^(md_ts_a|md_ts_b)$/', $strLink) === 1;")
        process, payload = self.run_auditor("controladores", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("CI001", self.codes(payload))

    def test_controller_ci4_accepts_specific_relationships_and_rejects_unrelated_resource(self):
        template = """<?php
class MdRiIntegracao extends SeiIntegracao {
    public function processarControladorAjax() {
        switch ($strAcao) {
            case '%s':
                SessaoSEI::getInstance()->validarPermissao('%s');
                return $this->executar();
        }
    }
}
"""
        valid_cases = (
            ("md_ri_consultar_cpf", "md_ri_consultar"),
            ("md_ri_item_listar", "md_ri_item_consultar"),
            ("md_ri_item_excluir", "md_ri_item_remover"),
        )
        for index, (action, resource) in enumerate(valid_cases):
            with self.subTest(action=action, resource=resource):
                path = self.write(f"MdRiSpecific{index}Integracao.php", template % (action, resource))
                process, payload = self.run_auditor("controladores", path)
                self.assertNotEqual(2, process.returncode, payload)
                self.assertNotIn("CI004", self.codes(payload))

        path = self.write(
            "MdTsUnrelatedIntegracao.php",
            template.replace("MdRiIntegracao", "MdTsUnrelatedIntegracao") % ("md_ts_item_excluir", "md_ts_relatorio_listar"),
        )
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("CI004", self.codes(payload))

    def test_controller_ci4_blocks_missing_case_authorization(self):
        content = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function processarControladorAjax() {
        switch ($strAcao) {
            case 'md_ts_item_listar':
                return $this->listar();
        }
    }
}
"""
        path = self.write("MdTsIntegracao.php", content)
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("CI004", self.codes(payload))

        different_resource = content.replace(
            "return $this->listar();",
            "SessaoSEI::getInstance()->validarPermissao('md_ts_outra_acao');\n                return $this->listar();",
        )
        path = self.write("MdTsOutraIntegracao.php", different_resource.replace("MdTsIntegracao", "MdTsOutraIntegracao"))
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("CI004", self.codes(payload))

        implausible_resource = content.replace(
            "return $this->listar();",
            "SessaoSEI::getInstance()->validarPermissao('md_zz_outra_acao');\n                return $this->listar();",
        )
        path = self.write("MdTsImplausivelIntegracao.php", implausible_resource.replace("MdTsIntegracao", "MdTsImplausivelIntegracao"))
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("CI004", self.codes(payload))

    def test_controller_ci4_ignores_prior_switch_and_reports_case_line(self):
        valid = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function processarControladorAjax() {
        switch ($strFormato) { case 'json': break; }
        switch ($strAcao) {
            case 'md_ts_item_listar':
                SessaoSEI::getInstance()->validarPermissao('md_ts_item_consultar');
                return $this->listar();
        }
    }
}
"""
        path = self.write("MdTsSwitchIntegracao.php", valid)
        process, payload = self.run_auditor("controladores", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("CI004", self.codes(payload))

        missing = valid.replace(
            "SessaoSEI::getInstance()->validarPermissao('md_ts_item_consultar');",
            "// sem autorizacao",
        )
        path = self.write("MdTsCaseLineIntegracao.php", missing.replace("MdTsIntegracao", "MdTsCaseLineIntegracao"))
        process, payload = self.run_auditor("controladores", path)
        issue = next(error for error in payload["results"][0]["erros"] if error["codigo"] == "CI004")
        self.assertEqual(6, issue["linha"])

    def test_controller_ci4_requires_authorization_before_first_sink(self):
        template = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function processarControladorAjax() {
        switch ($strAcao) {
            case 'md_ts_item_listar':
                %s
                return $this->listar();
        }
    }
}
"""
        cases = {
            "commented": "// SessaoSEI::getInstance()->validarPermissao('md_ts_item_listar');",
            "later": "$this->registrar();\n                SessaoSEI::getInstance()->validarPermissao('md_ts_item_listar');",
        }
        for name, authorization in cases.items():
            with self.subTest(case=name):
                path = self.write(f"MdTs{name.title()}Integracao.php", template % authorization)
                process, payload = self.run_auditor("controladores", path)
                self.assertEqual(2, process.returncode)
                self.assertIn("CI004", self.codes(payload))

    def test_controller_ci4_uses_actual_dispatch_variable_and_grouped_cases(self):
        wrong_variable = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function processarControladorAjax() {
        switch ($strAcao) {
            case 'md_ts_item_listar':
                SessaoSEI::getInstance()->validarPermissao($strServico);
                return $this->listar();
        }
    }
}
"""
        path = self.write("MdTsWrongIntegracao.php", wrong_variable)
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("CI004", self.codes(payload))

        grouped = wrong_variable.replace(
            "case 'md_ts_item_listar':",
            "case 'md_ts_item_listar':\n            case 'md_ts_item_consultar':",
        ).replace("$strServico", "$strAcao")
        path = self.write("MdTsGroupedIntegracao.php", grouped.replace("MdTsIntegracao", "MdTsGroupedIntegracao"))
        process, payload = self.run_auditor("controladores", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("CI004", self.codes(payload))

    def test_controller_ci5_warns_about_sensitive_payload(self):
        content = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function processarControladorAjax() {
        switch ($strAcao) {
            case 'md_ts_item_listar':
                SessaoSEI::getInstance()->validarPermissao('md_ts_item_listar');
                return ['token' => $strToken];
        }
    }
}
"""
        path = self.write("MdTsIntegracao.php", content)
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(1, process.returncode)
        self.assertIn("CI005", self.codes(payload, "avisos"))

    def test_controller_dispatch_cases_belong_to_expected_switch(self):
        content = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function processarControladorAjax() {
        switch ($strAcao) {}
        switch ($strFormato) { case 'md_ts_item_listar': return $this->listar(); }
    }
    public function processarControladorWebServices() {
        switch ($strServico) {}
        switch ($strFormato) { case 'md_ts_item_ws': return $this->executar(); }
    }
}
"""
        path = self.write("MdTsIntegracao.php", content)
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"CI002", "CI003"}.issubset(self.codes(payload)))

    def test_controller_rules_do_not_accept_tokens_from_other_methods(self):
        content = """<?php
class MdTsIntegracao extends SeiIntegracao {
    public function auxiliar() {
        preg_match('/x/', 'x');
        switch ($strAcao) { case 'x': break; }
        switch ($strServico) { case 'x': break; }
    }
    public function tratarLinkSemAssinatura() {}
    public function processarControladorWebServices() {}
    public function processarControladorAjax() {}
}
"""
        path = self.write("MdTsIntegracao.php", content)
        process, payload = self.run_auditor("controladores", path)
        self.assertEqual(2, process.returncode)
        self.assertTrue({"CI001", "CI002", "CI003"}.issubset(self.codes(payload)))


if __name__ == "__main__":
    unittest.main()
