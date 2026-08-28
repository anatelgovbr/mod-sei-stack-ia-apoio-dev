"""Testes do auditor da skill sei-verificacao-rn.

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
    "rn": SKILLS / "sei-verificacao-rn" / "audit.py",
}


class RnAuditTest(unittest.TestCase):
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
    def rn_base(methods=""):
        return f"""<?php
class MdTsItemRN extends InfraRN
{{
    protected function inicializarObjInfraIBanco(): InfraIBanco
    {{
        return BancoSEI::getInstance();
    }}

    protected function consultarConectado($objDTO)
    {{
        try {{
            SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_listar', __METHOD__, $objDTO);
            $objBD = new MdTsItemBD($this->getObjInfraIBanco());
            return $objBD->consultar($objDTO);
        }} catch (Exception $e) {{
            throw new InfraException('Erro consultando.', $e);
        }}
    }}

{methods}
}}
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
                process, payload = self.run_auditor("rn", target)
                self.assertEqual(2, process.returncode)
                self.assertEqual("BLOCK", payload["verdict"])

    def test_auditor_blocks_when_eligible_parser_extracts_nothing(self):
        """Arquivo elegivel do qual nada foi extraido tambem bloqueia."""
        target = self.write('MdTsVaziaRN.php', '<?php class MdTsVazia {}')
        process, payload = self.run_auditor("rn", target)
        self.assertEqual(2, process.returncode)
        self.assertEqual("BLOCK", payload["verdict"])

    def test_rn_accepts_external_effect_after_controlled_return(self):
        methods = """
    public function salvarComNotificacao($objDTO)
    {
        $retorno = $this->cadastrar($objDTO);
        $client->request('POST', '/evento');
        return $retorno;
    }

    protected function cadastrarControlado($objDTO)
    {
        try {
            SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);
            $objBD = new MdTsItemBD($this->getObjInfraIBanco());
            return $objBD->cadastrar($objDTO);
        } catch (Exception $e) {
            throw new InfraException('Erro cadastrando.', $e);
        }
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(methods))
        process, payload = self.run_auditor("rn", path)
        self.assertNotEqual(2, process.returncode)
        self.assertNotIn("T006", self.codes(payload))

        wrong_order = self.rn_base(methods.replace(
            "$retorno = $this->cadastrar($objDTO);\n        $client->request('POST', '/evento');",
            "$client->request('POST', '/evento');\n        $retorno = $this->cadastrar($objDTO);",
        ))
        path = self.write("MdTsWrongOrderRN.php", wrong_order.replace("MdTsItemRN", "MdTsWrongOrderRN").replace("MdTsItemBD", "MdTsWrongOrderBD"))
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("T006", self.codes(payload))

    def test_rn_blocks_direct_controlado_call_before_external_effect(self):
        methods = """
    public function salvarComNotificacao($objDTO)
    {
        $retorno = $this->cadastrarControlado($objDTO);
        $objEmail->notificar($retorno);
        return $retorno;
    }

    protected function cadastrarControlado($objDTO)
    {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);
        $objBD = new MdTsItemBD($this->getObjInfraIBanco());
        return $objBD->cadastrar($objDTO);
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(methods))
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("T006", self.codes(payload))

    def test_rn_blocks_external_effect_inside_controlado(self):
        methods = """
    protected function cadastrarControlado($objDTO)
    {
        try {
            SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);
            $objBD = new MdTsItemBD($this->getObjInfraIBanco());
            $retorno = $objBD->cadastrar($objDTO);
            $objEmail->notificar($retorno);
            return $retorno;
        } catch (Exception $e) {
            throw new InfraException('Erro cadastrando.', $e);
        }
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(methods))
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("T006", self.codes(payload))

    def test_rn_does_not_treat_integracao_identifiers_as_external_effects(self):
        methods = """
    protected function cadastrarControlado($objDTO)
    {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);
        $objDTO->setStrIntegracao('interna');
        $objDTO->validarDadosIntegracao();
        $objIntegracao = $objDTO->getStrIntegracao();
        return (new MdTsItemBD($this->getObjInfraIBanco()))->cadastrar($objDTO);
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(methods))
        process, payload = self.run_auditor("rn", path)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("A001", self.codes(payload))
        self.assertNotIn("T006", self.codes(payload))

        external = methods.replace(
            "$objDTO->setStrIntegracao('interna');\n        $objDTO->validarDadosIntegracao();\n        $objIntegracao = $objDTO->getStrIntegracao();",
            "MdExternaIntegracao::sincronizar($objDTO);",
        )
        path = self.write("MdTsExternalRN.php", self.rn_base(external).replace("MdTsItemRN", "MdTsExternalRN").replace("MdTsItemBD", "MdTsExternalBD"))
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("T006", self.codes(payload))

    def test_rn_ignores_commented_audit_and_blocks_mail_and_http_in_controlado(self):
        commented = """
    protected function cadastrarControlado($objDTO)
    {
        // SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);
        return (new MdTsItemBD($this->getObjInfraIBanco()))->cadastrar($objDTO);
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(commented))
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("A001", self.codes(payload))

        effects = {
            "mail": "mail('destino@example.test', 'Assunto', 'Mensagem');",
            "http_post": "$http->post('/evento', $objDTO);",
            "http_get": "$objHttp->get('/evento');",
            "http_request": "$httpClient->request('POST', '/evento');",
            "http_send": "$http->send($objRequest);",
            "generic_client_request": "$client->request('POST', '/evento');",
            "guzzle_client": "$transport = new GuzzleHttp\\Client();\n        $transport->post('/evento', $objDTO);",
            "curl": "curl_exec($handle);",
        }
        for name, effect in effects.items():
            with self.subTest(effect=name):
                methods = commented.replace(
                    "// SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);",
                    "SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);\n        " + effect,
                )
                path = self.write(f"MdTs{name.title().replace('_', '')}RN.php", self.rn_base(methods).replace("MdTsItemRN", f"MdTs{name.title().replace('_', '')}RN").replace("MdTsItemBD", f"MdTs{name.title().replace('_', '')}BD"))
                process, payload = self.run_auditor("rn", path)
                self.assertEqual(2, process.returncode)
                self.assertIn("T006", self.codes(payload))

    def test_rn_ignores_commented_read_audit(self):
        content = self.rn_base().replace(
            "SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_listar', __METHOD__, $objDTO);",
            "// SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_listar', __METHOD__, $objDTO);",
        )
        path = self.write("MdTsItemRN.php", content)
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("A003", self.codes(payload))

    def test_rn_internal_helper_does_not_require_user_session(self):
        helper = """
    protected function sincronizarInterno($objDTO)
    {
        return $objDTO;
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(helper))
        process, payload = self.run_auditor("rn", path)
        self.assertNotEqual(2, process.returncode)
        self.assertNotIn("A001", self.codes(payload))
        self.assertNotIn("A003", self.codes(payload))

    def test_rn_requires_all_persistence_before_first_external_effect(self):
        methods = """
    public function salvarComNotificacao($objDTO)
    {
        $this->cadastrar($objDTO);
        $objEmail->notificar($objDTO);
        $objBD = new MdTsItemBD($this->getObjInfraIBanco());
        return $objBD->alterar($objDTO);
    }

    protected function cadastrarControlado($objDTO)
    {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_cadastrar', __METHOD__, $objDTO);
        return (new MdTsItemBD($this->getObjInfraIBanco()))->cadastrar($objDTO);
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(methods))
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("T006", self.codes(payload))

    def test_rn_requires_listar_for_public_reads(self):
        content = self.rn_base().replace("md_ts_item_listar", "md_ts_item_consultar")
        path = self.write("MdTsItemRN.php", content)
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("A003", self.codes(payload))

    def test_rn_requires_md_prefix_and_operation_suffix_without_class_equality(self):
        wrong_write = """
    protected function cadastrarControlado($objDTO)
    {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_ts_item_listar', __METHOD__, $objDTO);
        $objBD = new MdTsItemBD($this->getObjInfraIBanco());
        return $objBD->cadastrar($objDTO);
    }
"""
        path = self.write("MdTsItemRN.php", self.rn_base(wrong_write))
        process, payload = self.run_auditor("rn", path)
        self.assertEqual(2, process.returncode)
        self.assertIn("A001", self.codes(payload))

        wrong_write_module = self.write(
            "MdTsWriteModuleRN.php",
            self.rn_base(wrong_write.replace("md_ts_item_listar", "md_zz_item_cadastrar")).replace("MdTsItemRN", "MdTsWriteModuleRN").replace("MdTsItemBD", "MdTsWriteModuleBD"),
        )
        process, payload = self.run_auditor("rn", wrong_write_module)
        self.assertEqual(2, process.returncode)
        self.assertIn("A001", self.codes(payload))

        wrong_read = self.write(
            "MdTsOutroRN.php",
            self.rn_base().replace("MdTsItemRN", "MdTsOutroRN").replace("MdTsItemBD", "MdTsOutroBD").replace("md_ts_item_listar", "md_ts_outra_listar"),
        )
        process, payload = self.run_auditor("rn", wrong_read)
        self.assertNotEqual(2, process.returncode, payload)
        self.assertNotIn("A003", self.codes(payload))

        invalid_prefix = self.write(
            "MdTsPrefixRN.php",
            self.rn_base().replace("MdTsItemRN", "MdTsPrefixRN").replace("MdTsItemBD", "MdTsPrefixBD").replace("md_ts_item_listar", "ts_item_listar"),
        )
        process, payload = self.run_auditor("rn", invalid_prefix)
        self.assertEqual(2, process.returncode)
        self.assertIn("A003", self.codes(payload))

        wrong_module = self.write(
            "MdTsWrongModuleRN.php",
            self.rn_base().replace("MdTsItemRN", "MdTsWrongModuleRN").replace("MdTsItemBD", "MdTsWrongModuleBD").replace("md_ts_item_listar", "md_zz_item_listar"),
        )
        process, payload = self.run_auditor("rn", wrong_module)
        self.assertEqual(2, process.returncode)
        self.assertIn("A003", self.codes(payload))

        for sigla, class_prefix in (("ia", "MdIa"), ("apt", "MdApt")):
            with self.subTest(sigla=sigla):
                write = f"""
    protected function cadastrarControlado($objDTO)
    {{
        SessaoSEI::getInstance()->validarAuditarPermissao('md_{sigla}_outra_entidade_cadastrar', __METHOD__, $objDTO);
        return (new {class_prefix}ItemBD($this->getObjInfraIBanco()))->cadastrar($objDTO);
    }}
"""
                content = self.rn_base(write).replace("MdTsItemRN", f"{class_prefix}ItemRN").replace("MdTsItemBD", f"{class_prefix}ItemBD").replace("md_ts_item_listar", f"md_{sigla}_outra_entidade_listar")
                path = self.write(f"{class_prefix}ItemRN.php", content)
                process, payload = self.run_auditor("rn", path)
                self.assertNotEqual(2, process.returncode, payload)
                self.assertNotIn("A001", self.codes(payload))
                self.assertNotIn("A003", self.codes(payload))


if __name__ == "__main__":
    unittest.main()
