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
import time
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

    SINALIZADORES_SN = """$objTarefaDTO->setStrSinHistoricoResumido('S');
$objTarefaDTO->setStrSinHistoricoCompleto('S');
$objTarefaDTO->setStrSinLancarAndamentoFechado('N');
$objTarefaDTO->setStrSinPermiteProcessoFechado('N');
$objTarefaDTO->setStrSinFecharAndamentosAbertos('S');
"""
    COLUNAS = (
        "id_tarefa,nome,sin_historico_resumido,sin_historico_completo,sin_lancar_andamento_fechado,"
        "sin_permite_processo_fechado,sin_fechar_andamentos_abertos,id_tarefa_modulo"
    )

    def test_release_script_registering_tasks_is_eligible_by_content(self):
        """Script de release cadastra tarefa sem 'tarefa' no nome; o gate le o conteudo.

        RN que so consulta TarefaDTO no mesmo diretorio fica fora, para o gate nao
        bloquear arquivo que nao cadastra tarefa.
        """
        script = self.write(
            "release/sei_atualizar_versao_modulo_ts.php",
            """<?php
$numIdTarefa = BancoSEI::getInstance()->getValorSequencia('seq_tarefa');
$objTarefaDTO = new TarefaDTO();
$objTarefaDTO->setNumIdTarefa($numIdTarefa);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_RECEBIDO');
$objTarefaDTO->setStrNome('Item recebido (@UNIDADE@)');
""" + self.SINALIZADORES_SN + """$objTarefaRN->cadastrar($objTarefaDTO);

$strCampos = 'id_tarefa,nome,sin_historico_resumido,sin_historico_completo,sin_lancar_andamento_fechado,sin_permite_processo_fechado,sin_fechar_andamentos_abertos,id_tarefa_modulo';
BancoSEI::getInstance()->executarSql("INSERT INTO tarefa ($strCampos) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Item devolvido (@UNIDADE@, @MOTIVO@)','S','S','N','S','S','MD_TS_ITEM_DEVOLVIDO')");
""",
        )
        self.write(
            "release/MdTsConsultaRN.php",
            "<?php $objTarefaDTO = new TarefaDTO(); $objTarefaDTO->retNumIdTarefa(); $objTarefaRN->listar($objTarefaDTO);",
        )
        process, payload = self.run_auditor("tarefa", script.parent)
        self.assertEqual(0, process.returncode, payload)
        self.assertEqual(["sei_atualizar_versao_modulo_ts.php"], [result["file"] for result in payload["results"]])
        self.assertEqual(
            ["MD_TS_ITEM_RECEBIDO", "MD_TS_ITEM_DEVOLVIDO"],
            [tarefa["nome"] for tarefa in payload["results"][0]["tarefas"]],
        )

    def test_task_registration_requires_explicit_s_or_n_flags(self):
        script = self.write(
            "sei_atualizar_versao_modulo_ts.php",
            """<?php
$numIdTarefa = BancoSEI::getInstance()->getValorSequencia('seq_tarefa');
$objTarefaDTO = new TarefaDTO();
$objTarefaDTO->setNumIdTarefa($numIdTarefa);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_RECEBIDO');
$objTarefaDTO->setStrSinHistoricoResumido('S');
$objTarefaDTO->setStrSinHistoricoCompleto('X');
$objTarefaDTO->setStrSinLancarAndamentoFechado('N');
$objTarefaDTO->setStrSinFecharAndamentosAbertos('S');
$objTarefaBD->cadastrar($objTarefaDTO);
""",
        )
        process, payload = self.run_auditor("tarefa", script)
        self.assertEqual(2, process.returncode)
        self.assertEqual({"K009"}, self.codes(payload))
        mensagens = [issue["mensagem"] for issue in payload["results"][0]["erros"]]
        self.assertIn("sin_permite_processo_fechado", mensagens[0])
        self.assertIn("sin_historico_completo", mensagens[1])

    def test_calculated_task_id_requires_seq_tarefa_realignment(self):
        """Id calculado sem realinhar seq_tarefa colide com a proxima tarefa; o ajuste por SQL proprio fica para a revisao."""
        cadastro = """<?php
$arrMax = BancoSEI::getInstance()->consultarSql('select max(id_tarefa) as max from tarefa');
$numIdTarefa = max(1000, $arrMax[0]['max'] + 1);
REALINHAMENTO
$objTarefaDTO = new TarefaDTO();
$objTarefaDTO->setNumIdTarefa($numIdTarefa);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_RECEBIDO');
""" + self.SINALIZADORES_SN + """$objTarefaRN->cadastrar($objTarefaDTO);
"""
        sem_realinhar = self.write("sem/sei_atualizar_versao_modulo_ts.php", cadastro.replace("REALINHAMENTO", ""))
        process, payload = self.run_auditor("tarefa", sem_realinhar)
        self.assertEqual(2, process.returncode)
        self.assertEqual({"K008"}, self.codes(payload))

        realinhamentos = {
            "k8": ("BancoSEI::getInstance()->criarSequencialNativa('seq_tarefa', $numIdTarefa + 1);", 0, set()),
            "script_rn": ("$objScriptRN = new ScriptRN();\n$objScriptRN->atualizarSequencias();", 0, set()),
            "sql_proprio": ("BancoSEI::getInstance()->executarSql('INSERT INTO seq_tarefa (id) VALUES (' . $numIdTarefa . ')');", 1, {"K008"}),
        }
        for nome, (realinhamento, retorno, avisos) in realinhamentos.items():
            with self.subTest(nome):
                path = self.write(f"{nome}/sei_atualizar_versao_modulo_ts.php", cadastro.replace("REALINHAMENTO", realinhamento))
                process, payload = self.run_auditor("tarefa", path)
                self.assertEqual(retorno, process.returncode, payload)
                self.assertEqual(set(), self.codes(payload))
                self.assertEqual(avisos, self.codes(payload, "avisos"))

    def test_registration_blocks_task_65_and_unresolved_insert_and_reads_literal_insert(self):
        """A 65 e tarefa do core: o modulo lanca andamento com ela, nunca a cadastra."""
        id65 = self.write(
            "id65/sei_atualizar_versao_modulo_ts.php",
            """<?php
$objTarefaDTO = new TarefaDTO();
$objTarefaDTO->setNumIdTarefa(65);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ANDAMENTO_LIVRE');
""" + self.SINALIZADORES_SN + """$objTarefaRN->cadastrar($objTarefaDTO);
""",
        )
        process, payload = self.run_auditor("tarefa", id65)
        self.assertEqual(2, process.returncode)
        self.assertEqual({"K001"}, self.codes(payload))

        sem_colunas = self.write(
            "sem_colunas/sei_atualizar_versao_modulo_ts.php",
            "<?php BancoSEI::getInstance()->executarSql(\"INSERT INTO tarefa ($strCampos) VALUES (1001,'Item','S','S','N','S','S','MD_TS_ITEM')\");",
        )
        process, payload = self.run_auditor("tarefa", sem_colunas)
        self.assertEqual(2, process.returncode)
        self.assertEqual({"K000"}, self.codes(payload))

        insert_literal = (
            "<?php BancoSEI::getInstance()->executarSql('insert into tarefa (id_tarefa,nome,sin_historico_resumido,"
            "sin_historico_completo,sin_lancar_andamento_fechado,sin_permite_processo_fechado,sin_fechar_andamentos_abertos,"
            "id_tarefa_modulo) values (1001,\\'Item arquivado\\',\\'S\\',\\'S\\',\\'N\\',\\'S\\',\\'S\\',\\'MD_TS_ITEM_ARQUIVADO\\')');"
        )
        sem_realinhar = self.write("literal/sei_atualizar_versao_modulo_ts.php", insert_literal)
        process, payload = self.run_auditor("tarefa", sem_realinhar)
        self.assertEqual(2, process.returncode)
        self.assertEqual({"K008"}, self.codes(payload))

        realinhado = self.write(
            "literal_realinhado/sei_atualizar_versao_modulo_ts.php",
            insert_literal + "\nBancoSEI::getInstance()->executarSql('alter table seq_tarefa AUTO_INCREMENT = 1001');",
        )
        process, payload = self.run_auditor("tarefa", realinhado)
        self.assertEqual(1, process.returncode, payload)
        self.assertEqual(set(), self.codes(payload))
        self.assertEqual({"K008"}, self.codes(payload, "avisos"))
        self.assertEqual(1001, payload["results"][0]["tarefas"][0]["id"])

    def test_registration_parser_does_not_hide_invalid_records(self):
        """Cada forma abaixo ja escondeu cadastro invalido e recebeu PASS."""
        valido = """$objTarefaDTO->setNumIdTarefa(BancoSEI::getInstance()->getValorSequencia('seq_tarefa'));
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_RECEBIDO');
""" + self.SINALIZADORES_SN + "$objTarefaRN->cadastrar($objTarefaDTO);\n"
        casos = {
            "construtor sem parenteses": ("$objTarefaDTO = new TarefaDTO;\n" + valido.replace(
                "BancoSEI::getInstance()->getValorSequencia('seq_tarefa')", "65"), "K001"),
            "unSetTodos limpa os sinalizadores": ("$objTarefaDTO = new TarefaDTO();\n" + valido + """$objTarefaDTO->unSetTodos();
$objTarefaDTO->setNumIdTarefa(BancoSEI::getInstance()->getValorSequencia('seq_tarefa'));
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_DEVOLVIDO');
$objTarefaRN->cadastrar($objTarefaDTO);
""", "K009"),
            "segunda tupla do INSERT": ("""BancoSEI::getInstance()->executarSql("INSERT INTO tarefa (id_tarefa,nome,sin_historico_resumido,sin_historico_completo,sin_lancar_andamento_fechado,sin_permite_processo_fechado,sin_fechar_andamentos_abertos,id_tarefa_modulo) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Item','S','S','N','S','S','MD_TS_ITEM'),(65,'Livre','S','S','N','S','S','MD_TS_LIVRE')");
""", "K001"),
            "variavel reatribuida depois da sequencia": ("""$numIdTarefa = BancoSEI::getInstance()->getValorSequencia('seq_tarefa');
$numIdTarefa = 1001;
$objTarefaDTO = new TarefaDTO();
""" + valido.replace("BancoSEI::getInstance()->getValorSequencia('seq_tarefa')", "$numIdTarefa"), "K008"),
            "conta sobre a sequencia": ("$objTarefaDTO = new TarefaDTO();\n" + valido.replace(
                "getValorSequencia('seq_tarefa')", "getValorSequencia('seq_tarefa') * 0 + 65"), "K008"),
            "identificador concatenado": ("$objTarefaDTO = new TarefaDTO();\n" + valido.replace(
                "'MD_TS_ITEM_RECEBIDO'", "'MD_TS_ITEM' . $strSufixo"), "K003"),
            "id negativo": ("$objTarefaDTO = new TarefaDTO();\n" + valido.replace(
                "BancoSEI::getInstance()->getValorSequencia('seq_tarefa')", "-1"), "K001"),
            "retorno de cadastrar reatribuido": ("$objTarefaDTO = new TarefaDTO();\n" + valido.replace(
                "BancoSEI::getInstance()->getValorSequencia('seq_tarefa')", "65").replace(
                "$objTarefaRN->cadastrar(", "$objTarefaDTO = $objTarefaRN->cadastrar("), "K001"),
            "segunda tupla concatenada": ("""BancoSEI::getInstance()->executarSql("INSERT INTO tarefa (""" + self.COLUNAS + """) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Item','S','S','N','S','S','MD_TS_ITEM'),"
    . "(65,'Livre','S','S','N','S','S','MD_TS_LIVRE')");
""", "K001"),
            "lista de colunas reatribuida sem literal": ("$strCampos = '" + self.COLUNAS + """';
$strCampos = str_replace('sin_historico_completo', 'sin_consulta_processual', $strCampos);
BancoSEI::getInstance()->executarSql("INSERT INTO tarefa ($strCampos) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Item','S','S','N','S','S','MD_TS_ITEM')");
""", "K000"),
            "realinha outra sequencia": ("$objTarefaDTO = new TarefaDTO();\n" + valido.replace(
                "BancoSEI::getInstance()->getValorSequencia('seq_tarefa')", "1001")
                + "BancoSEI::getInstance()->executarSql('INSERT INTO seq_tarefa_sessao (id) VALUES (1001)');\n", "K008"),
            "DTO reaproveitado apos cadastrar": ("$objTarefaDTO = new TarefaDTO();\n" + valido.replace(
                "$objTarefaRN->cadastrar(", "$objTarefaDTO = $objTarefaRN->cadastrar(") + "$objTarefaDTO->unSetTodos();\n"
                + valido.replace("BancoSEI::getInstance()->getValorSequencia('seq_tarefa')", "65"), "K001"),
            "segunda tupla em aspas simples": ("""BancoSEI::getInstance()->executarSql("INSERT INTO tarefa (""" + self.COLUNAS + """) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Item','S','S','N','S','S','MD_TS_ITEM')"
    . ',(65,\\'Livre\\',\\'S\\',\\'S\\',\\'N\\',\\'S\\',\\'S\\',\\'MD_TS_LIVRE\\')');
""", "K001"),
            "colunas com interpolacao": ('$strCampos = "' + self.COLUNAS.replace(",id_tarefa_modulo", "") + """,$strExtra";
BancoSEI::getInstance()->executarSql("INSERT INTO tarefa ($strCampos) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Item','S','S','N','S','S','MD_TS_ITEM')");
""", "K000"),
        }
        for indice, (nome, (corpo, codigo)) in enumerate(casos.items()):
            with self.subTest(caso=nome):
                path = self.write(f"caso{indice}/sei_atualizar_versao_modulo_ts.php", "<?php\n" + corpo)
                process, payload = self.run_auditor("tarefa", path)
                self.assertEqual(2, process.returncode, payload)
                self.assertIn(codigo, self.codes(payload))

    def test_insert_reads_appended_columns_and_quoted_values(self):
        """Falsos positivos ja vistos: coluna acrescentada por .=, virgula entre aspas duplas e apostrofo escapado."""
        script = self.write(
            "sei_atualizar_versao_modulo_ts.php",
            """<?php
$strCampos = 'id_tarefa,nome,sin_historico_resumido,sin_historico_completo,sin_lancar_andamento_fechado,sin_permite_processo_fechado,id_tarefa_modulo';
$strCampos .= ',sin_fechar_andamentos_abertos';
BancoSEI::getInstance()->executarSql('INSERT INTO tarefa (' . $strCampos . ') VALUES (' . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ',"Reuniao, inicio",\\'S\\',\\'S\\',\\'N\\',\\'S\\',\\'MD_TS_REUNIAO\\',\\'S\\')');
BancoSEI::getInstance()->executarSql("INSERT INTO tarefa (""" + self.COLUNAS + """) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Registro d\\'agua, atualizado','S','S','N','S','S','MD_TS_AGUA')");
BancoSEI::getInstance()->executarSql("INSERT INTO tarefa (""" + self.COLUNAS + """) VALUES (" . BancoSEI::getInstance()->getValorSequencia('seq_tarefa') . ",'Registro d\\\\'oleo, atualizado','S','S','N','S','S','MD_TS_OLEO')");
""",
        )
        process, payload = self.run_auditor("tarefa", script)
        self.assertEqual(0, process.returncode, payload)
        self.assertEqual(
            ["MD_TS_REUNIAO", "MD_TS_AGUA", "MD_TS_OLEO"],
            [tarefa["nome"] for tarefa in payload["results"][0]["tarefas"]],
        )

    def test_registration_blocks_id_below_1000_from_variable_even_with_realignment(self):
        """Id abaixo de 1000 por variavel e K1 mesmo quando o arquivo realinha seq_tarefa; id >= 1000 segue no K8."""
        cadastro = """<?php
$numIdTarefa = NUMERO;
$objTarefaDTO = new TarefaDTO();
$objTarefaDTO->setNumIdTarefa($numIdTarefa);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_RECEBIDO');
""" + self.SINALIZADORES_SN + """$objTarefaRN->cadastrar($objTarefaDTO);
REALINHAMENTO
"""
        insert = """<?php
$numIdTarefa = NUMERO;
BancoSEI::getInstance()->executarSql("INSERT INTO tarefa (""" + self.COLUNAS + """) VALUES (" . $numIdTarefa . ",'Item','S','S','N','S','S','MD_TS_ITEM')");
REALINHAMENTO
"""
        script_rn = "$objScriptRN = new ScriptRN();\n$objScriptRN->atualizarSequencias();"
        casos = {
            "TarefaDTO com atualizarSequencias": (cadastro, "500", script_rn, 2, {"K001"}),
            "TarefaDTO com seq_tarefa realinhada": (cadastro, "999", "BancoSEI::getInstance()->executarSql('INSERT INTO seq_tarefa (id) VALUES (999)');", 2, {"K001"}),
            "tarefa 65 por variavel": (cadastro, "65", script_rn, 2, {"K001"}),
            "INSERT com atualizarSequencias": (insert, "500", script_rn, 2, {"K001"}),
            "id 1500 por variavel com realinhamento": (cadastro, "1500", script_rn, 0, set()),
            "id 1500 por variavel sem realinhamento": (cadastro, "1500", "", 2, {"K008"}),
        }
        for indice, (nome, (modelo, numero, realinhamento, retorno, codigos)) in enumerate(casos.items()):
            with self.subTest(caso=nome):
                path = self.write(
                    f"variavel{indice}/sei_atualizar_versao_modulo_ts.php",
                    modelo.replace("NUMERO", numero).replace("REALINHAMENTO", realinhamento),
                )
                process, payload = self.run_auditor("tarefa", path)
                self.assertEqual(retorno, process.returncode, payload)
                self.assertEqual(codigos, self.codes(payload))

    def test_registration_parser_time_is_linear(self):
        """8.000 TarefaDTO sem cadastrar levavam segundos por leitura do arquivo; o limite e 1 s na execucao inteira."""
        script = self.write(
            "sei_atualizar_versao_modulo_ts.php",
            """<?php
$numIdTarefa = BancoSEI::getInstance()->getValorSequencia('seq_tarefa');
$objTarefaDTO = new TarefaDTO();
$objTarefaDTO->setNumIdTarefa($numIdTarefa);
$objTarefaDTO->setStrIdTarefaModulo('MD_TS_ITEM_RECEBIDO');
""" + self.SINALIZADORES_SN + "$objTarefaRN->cadastrar($objTarefaDTO);\n"
            + "".join(f"$objTarefa{indice}DTO = new TarefaDTO();\n" for indice in range(8000)),
        )

        inicio = time.perf_counter()
        process, payload = self.run_auditor("tarefa", script)
        duracao = time.perf_counter() - inicio

        self.assertEqual(0, process.returncode, payload)
        self.assertEqual(["MD_TS_ITEM_RECEBIDO"], [tarefa["nome"] for tarefa in payload["results"][0]["tarefas"]])
        self.assertLess(duracao, 1.0)


if __name__ == "__main__":
    unittest.main()
