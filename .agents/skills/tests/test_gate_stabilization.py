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
    "pagina": SKILLS / "sei-verificacao-pagina" / "audit.py",
    "rn": SKILLS / "sei-verificacao-rn" / "audit.py",
    "controladores": SKILLS / "sei-verificacao-controladores" / "audit.py",
    "tarefa": SKILLS / "sei-verificacao-tarefa" / "audit.py",
    "banco": SKILLS / "sei-verificacao-banco-dados" / "audit.py",
}


class GateStabilizationTest(unittest.TestCase):
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

    def test_all_auditors_fail_closed_for_missing_incompatible_and_empty_input(self):
        incompatible = self.write("arquivo.txt", "sem artefato")
        empty = self.work / "vazio"
        empty.mkdir()
        missing = self.work / "inexistente"
        for name in AUDITORS:
            for target in (missing, incompatible, empty):
                with self.subTest(auditor=name, target=target.name):
                    process, payload = self.run_auditor(name, target)
                    self.assertEqual(2, process.returncode)
                    self.assertEqual("BLOCK", payload["verdict"])

    def test_all_auditors_block_when_eligible_parser_extracts_nothing(self):
        cases = {
            "pagina": self.write("md_ts_vazia_lista.php", "<?php"),
            "rn": self.write("MdTsVaziaRN.php", "<?php class MdTsVazia {}"),
            "controladores": self.write("MdTsIntegracao.php", "<?php class MdTsIntegracao extends SeiIntegracao {}"),
            "tarefa": self.write("md_ts_tarefa.php", "<?php return [];"),
            "banco": self.write("modelo.sql", "SELECT 1;"),
        }
        for name, target in cases.items():
            with self.subTest(auditor=name):
                process, payload = self.run_auditor(name, target)
                self.assertEqual(2, process.returncode)
                self.assertEqual("BLOCK", payload["verdict"])

    def test_page_p5_p6_p8_and_p10_are_blocking(self):
        cases = {
            "p5": ("$valor = $_REQUEST['valor'];", "P005"),
            "p6": ("$valor = $_POST['valor'];", "P006"),
            "p8": ("echo $strNome;", "P008"),
            "p10": ('<a href="controlador.php?acao=md_ts_item_excluir">Excluir</a>', "P010"),
        }
        for name, (extra, code) in cases.items():
            with self.subTest(rule=name):
                path = self.write(f"md_ts_item_{name}_lista.php", self.page_base(extra))
                process, payload = self.run_auditor("pagina", path)
                self.assertEqual(2, process.returncode)
                self.assertIn(code, self.codes(payload))

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
        self.assertEqual(2, process.returncode)
        self.assertIn("P008", self.codes(payload))

        indirect = self.write(
            "md_ts_indirect_lista.php",
            self.page_base("$strNome = montarNome();\necho $strNome;"),
        )
        process, payload = self.run_auditor("pagina", indirect)
        self.assertEqual(1, process.returncode)
        self.assertIn("P008", self.codes(payload, "avisos"))

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

    def test_database_documentation_uses_db_ids_for_modeling_rules(self):
        reference = (SKILLS / "sei-verificacao-banco-dados" / "references" / "padroes-manual-md.md").read_text(encoding="utf-8")
        self.assertNotRegex(reference, r"(?:###|\|)\s*R(?:1[0-5]|[1-9])\b")
        self.assertNotIn("R1-R15", reference)

        dto_checklist = (ROOT / ".agents" / "checklists" / "checklist-dto-infraphp-sei.md").read_text(encoding="utf-8")
        self.assertIn("DB01-DB15", dto_checklist)
        self.assertIsNone(re.search(r"`R(?:1[0-5]|[1-9])`", dto_checklist))

    def test_crud_generator_uses_listar_in_generated_rn(self):
        contract = {
            "entidade": {
                "tabela": "md_ts_item",
                "singular": "item",
                "plural": "itens",
                "artigo": "o",
                "campoPrincipal": "str_nome",
                "comentario": "Item de teste",
            },
            "colunas": [
                {"nome": "id_md_ts_item", "tipoBanco": "integer", "chavePrimaria": True, "obrigatorio": True, "comentario": "Identificador"},
                {"nome": "str_nome", "tipoBanco": "varchar", "tamanho": 50, "chavePrimaria": False, "obrigatorio": True, "comentario": "Nome"},
            ],
            "relacionamentos": [],
            "relacionamentosNn": [],
            "regrasGeracao": {"campoSinAtivo": None},
            "ui": {"campos": {"str_nome": {"rotulo": "Nome", "teclaAtalho": "N"}}, "ordemFormulario": ["str_nome"]},
        }
        contract_path = self.write("contrato.json", json.dumps(contract))
        output = self.work / "gerado"
        process = subprocess.run(
            [sys.executable, str(SKILLS / "sei-gerador-crud" / "generate_from_contrato.py"), str(contract_path), str(output)],
            cwd=ROOT,
            text=True,
            capture_output=True,
            check=False,
        )
        self.assertEqual(0, process.returncode, process.stderr)
        rn = output / "rn" / "MdTsItemRN.php"
        content = rn.read_text(encoding="latin-1")
        self.assertNotIn("validarAuditarPermissao('md_ts_item_consultar'", content)
        self.assertGreaterEqual(content.count("validarAuditarPermissao('md_ts_item_listar'"), 3)
        audit, payload = self.run_auditor("rn", rn)
        self.assertNotEqual(2, audit.returncode, payload)


if __name__ == "__main__":
    unittest.main()
