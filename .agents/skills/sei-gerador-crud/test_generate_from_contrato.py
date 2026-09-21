"""Testes do gerador de CRUD da skill sei-gerador-crud.

Fecha o ciclo da stack: o que o gerador produz precisa passar nos auditores de
sei-verificacao-rn, sei-verificacao-pagina e sei-verificacao-banco-dados, alem
de php -l. Por isso este arquivo invoca os tres audit.py.

    python3 -m unittest test_generate_from_contrato
"""

import copy
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[3]
SKILLS = ROOT / ".agents" / "skills"
GENERATOR = SKILLS / "sei-gerador-crud" / "generate_from_contrato.py"
EXAMPLES = SKILLS / "sei-gerador-crud" / "examples"
AUDITORS = {
    "rn": SKILLS / "sei-verificacao-rn" / "audit.py",
    "pagina": SKILLS / "sei-verificacao-pagina" / "audit.py",
    "banco": SKILLS / "sei-verificacao-banco-dados" / "audit.py",
}
PHP = shutil.which("php")


def coluna(nome, tipo, comentario, tamanho=None, obrigatorio=True, pk=False, fk=False):
    col = {"nome": nome, "tipoBanco": tipo, "obrigatorio": obrigatorio, "comentario": comentario}
    if tamanho is not None:
        col["tamanho"] = tamanho
    if pk:
        col["chavePrimaria"] = True
    if fk:
        col["chaveEstrangeira"] = True
    return col


def relacao(col, tabela, campo, tipo="obrigatoria"):
    return {"coluna": col, "tabelaReferencia": tabela, "campoExibicao": campo, "tipoFk": tipo, "filtroFk": "on"}


def ui(ordem, campos):
    return {
        "ordemFormulario": ordem,
        "campos": {nome: {"rotulo": rotulo, "teclaAtalho": tecla, "artigo": artigo} for nome, (rotulo, tecla, artigo) in campos.items()},
    }


def contrato_projeto():
    """Standalone com sin_ativo (gabarito TRF4 md_abc_projeto)."""
    return {
        "entidade": {"tabela": "md_abc_projeto", "singular": "Projeto", "plural": "Projetos", "artigo": "o", "campoPrincipal": "identificacao", "comentario": "Cadastro de projetos."},
        "colunas": [
            coluna("id_md_abc_projeto", "int", "Identificador sequencial do projeto.", obrigatorio=False, pk=True),
            coluna("identificacao", "varchar", "Identificação do projeto.", 50),
            coluna("descricao", "varchar", "Descrição do projeto.", 255, obrigatorio=False),
            coluna("dta_cadastramento", "date", "Data de cadastramento do projeto."),
            coluna("sin_ativo", "char", "Indica se o projeto está ativo.", 1),
        ],
        "relacionamentos": [],
        "regrasGeracao": {"campoSinAtivo": "sin_ativo"},
        "ui": ui(["identificacao", "descricao", "dta_cadastramento"], {"identificacao": ("Identificação", "I", "a"), "descricao": ("Descrição", "D", "a"), "dta_cadastramento": ("Data de Cadastramento", "M", "a")}),
    }


def contrato_aquisicao():
    """1:N com FK obrigatoria e valor monetario, sem sin_ativo (gabarito TRF4 md_abc_aquisicao)."""
    return {
        "entidade": {"tabela": "md_abc_aquisicao", "singular": "Aquisição", "plural": "Aquisições", "artigo": "a", "campoPrincipal": "descricao", "comentario": "Aquisições vinculadas a um projeto."},
        "colunas": [
            coluna("id_md_abc_aquisicao", "int", "Identificador sequencial da aquisição.", obrigatorio=False, pk=True),
            coluna("id_md_abc_projeto", "int", "Projeto da aquisição.", fk=True),
            coluna("descricao", "varchar", "Descrição da aquisição.", 50),
            coluna("din_custo", "numeric", "Custo da aquisição.", ),
        ],
        "relacionamentos": [relacao("id_md_abc_projeto", "md_abc_projeto", "identificacao")],
        "regrasGeracao": {"campoSinAtivo": None},
        "ui": ui(["id_md_abc_projeto", "descricao", "din_custo"], {"id_md_abc_projeto": ("Projeto", "P", "o"), "descricao": ("Descrição", "D", "a"), "din_custo": ("Custo", "U", "o")}),
    }


def contrato_rel():
    """N:N com PK composta."""
    return {
        "entidade": {"tabela": "md_abc_rel_contrato_proj", "singular": "Associação", "plural": "Associações", "artigo": "a", "campoPrincipal": "id_md_abc_contrato", "comentario": "Associação entre contrato e projeto."},
        "colunas": [
            coluna("id_md_abc_contrato", "int", "Contrato associado.", pk=True, fk=True),
            coluna("id_md_abc_projeto", "int", "Projeto associado.", pk=True, fk=True),
            coluna("dta_associacao", "date", "Data da associação."),
        ],
        "relacionamentos": [relacao("id_md_abc_contrato", "md_abc_contrato", "numero"), relacao("id_md_abc_projeto", "md_abc_projeto", "identificacao")],
        "relacionamentosNn": [
            {"tabelaOrigem": "md_abc_contrato", "classeInt": "MdAbcContratoINT", "metodoInt": "montarSelectNumero", "rotulo": "Contrato", "artigo": "o", "teclaAtalho": "O"},
            {"tabelaOrigem": "md_abc_projeto", "classeInt": "MdAbcProjetoINT", "metodoInt": "montarSelectIdentificacao", "rotulo": "Projeto", "artigo": "o", "teclaAtalho": "P"},
        ],
        "regrasGeracao": {"campoSinAtivo": None},
        "ui": ui(["dta_associacao"], {"dta_associacao": ("Data de Associação", "D", "a")}),
    }


def contrato_sonda():
    """Casos fora do dominio de referencia: dth_, numeric sem din_, int opcional, FK opcional e duas FKs para a mesma tabela."""
    return {
        "entidade": {"tabela": "md_abc_sonda", "singular": "Sonda", "plural": "Sondas", "artigo": "a", "campoPrincipal": "nome", "comentario": "Entidade de sonda."},
        "colunas": [
            coluna("id_md_abc_sonda", "int", "Identificador.", obrigatorio=False, pk=True),
            coluna("nome", "varchar", "Nome.", 100),
            coluna("dth_entrega", "timestamp", "Data e hora de entrega."),
            coluna("percentual", "numeric", "Percentual sem prefixo monetário."),
            coluna("num_ordem", "int", "Ordem opcional.", obrigatorio=False),
            coluna("id_unidade_origem", "int", "Unidade de origem.", fk=True),
            coluna("id_unidade_destino", "int", "Unidade de destino.", obrigatorio=False, fk=True),
        ],
        "relacionamentos": [
            relacao("id_unidade_origem", "unidade", "sigla"),
            relacao("id_unidade_destino", "unidade", "sigla", tipo="opcional"),
        ],
        "regrasGeracao": {"campoSinAtivo": None},
        "ui": ui(
            ["nome", "dth_entrega", "percentual", "num_ordem", "id_unidade_origem", "id_unidade_destino"],
            {"nome": ("Nome", "N", "o"), "dth_entrega": ("Entrega", "G", "a"), "percentual": ("Percentual", "P", "o"), "num_ordem": ("Ordem", "O", "a"), "id_unidade_origem": ("Unidade de Origem", "I", "a"), "id_unidade_destino": ("Unidade de Destino", "D", "a")},
        ),
    }


INFRA = ROOT / "fontes" / "sei" / "src" / "main" / "php" / "infra" / "infra_php"

# Stub de web/SEI.php: carrega o InfraPHP real (sem banco) para exercitar DTO e BD gerados.
SEI_STUB = """<?php
define('INFRA_TAM_MAX_LOG_SQL', '8192');
if (!class_exists('mysqli')) { class mysqli { public function __construct() {} } }
foreach (['InfraException', 'InfraValidacaoDTO', 'InfraString', 'InfraDTO', 'InfraIBanco', 'InfraMySql', 'InfraMySqli', 'InfraBD', 'InfraUtil', 'InfraData', 'InfraArray'] as $classe) {
  require_once '%s/' . $classe . '.php';
}
"""

# Driver falso: herda o InfraMySqli real (formatacao e bind) e captura o SQL em vez de executar.
BD_HARNESS = """<?php
require_once $argv[2];
class BancoFalso extends InfraMySqli {
  public array $sqls = [];
  public function getServidor() { return ''; } public function getPorta() { return ''; } public function getBanco() { return ''; }
  public function getUsuario() { return ''; } public function getSenha() { return ''; }
  public function abrirConexao() {} public function fecharConexao() {}
  public function abrirTransacao() {} public function confirmarTransacao() {} public function cancelarTransacao() {}
  public function consultarSql($sql, $arrCamposBind = null) { $this->sqls[] = $sql; return (stripos($sql, 'COUNT(') !== false) ? [['total' => 0]] : []; }
  public function executarSql($sql, $arrCamposBind = null) { $this->sqls[] = $sql; return 1; }
  public function getIdConexao() { return null; }
  public function proximoSequencial($tabela) { return 1; }
  public function proximoSequencialNativo($tabela, $campo = null) { return 1; }
  public function getUltimoSequencialNativo($tabela = null, $campo = null) { return 1; }
}
$dir = $argv[1]; $banco = new BancoFalso(); $saida = [];
foreach (glob($dir . '/dto/*DTO.php') as $file) {
  require_once $file;
  $classe = basename($file, '.php'); $base = substr($classe, 0, -3);
  require_once $dir . '/bd/' . $base . 'BD.php';
  $dto = new $classe(); $bdClasse = $base . 'BD'; $bd = new $bdClasse($banco);
  $dto->retTodos(true); $atributos = $dto->getArrAtributos();
  $nomes = []; foreach ($atributos as $nome => $def) { $nomes[] = $def[InfraDTO::$POS_ATRIBUTO_PREFIXO] . $nome; }
  foreach ($nomes as $nome) { $dto->{'ret' . $nome}(); }
  $pk = $nomes[0]; foreach ($nomes as $n) { if (substr($n, 3, 2) === 'Id') { $pk = $n; break; } }
  $dto->{'setOrd' . $pk}(InfraDTO::$TIPO_ORDENACAO_ASC); $dto->{'set' . $pk}(1);
  $inicio = count($banco->sqls);
  $bd->listar($dto); $bd->contar($dto); $bd->consultar($dto);
  $novo = new $classe();
  foreach ($atributos as $nome => $def) {
    if ($def[InfraDTO::$POS_ATRIBUTO_TAB_ORIGEM] != '') { continue; }
    $p = $def[InfraDTO::$POS_ATRIBUTO_PREFIXO];
    $valor = ['Num' => 1, 'Str' => ($nome === 'SinAtivo' ? 'S' : 'x'), 'Dta' => '01/01/2026', 'Dth' => '01/01/2026 10:00:00', 'Din' => '1.234,56', 'Dbl' => '12.5'][$p];
    $novo->{'set' . $p . $nome}($valor);
  }
  $bd->cadastrar($novo); $bd->alterar($novo); $bd->excluir($novo);
  if (array_key_exists('SinAtivo', $atributos)) { $bd->desativar($novo); $bd->reativar($novo); }
  $unico = new $classe(); $unico->{'ret' . $pk}(); $unico->{'set' . $pk}(null, InfraDTO::$OPER_DIFERENTE); $bd->consultar($unico);
  $saida[$classe] = array_slice($banco->sqls, $inicio);
}
echo json_encode($saida);
"""


class GeradorCrudTest(unittest.TestCase):
    maxDiff = None

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.work = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    # ---------- utilitarios ----------
    def write_contract(self, contract, name="contrato.json"):
        path = self.work / name
        path.write_text(json.dumps(contract, ensure_ascii=False), encoding="utf-8")
        return path

    def generate(self, contract, subdir="gerado", *extra, expect_ok=True):
        contract_path = self.write_contract(contract, re.sub(r"\W", "_", subdir) + ".json")
        output = self.work / subdir
        process = subprocess.run(
            [sys.executable, str(GENERATOR), str(contract_path), str(output), *extra],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        if expect_ok:
            self.assertEqual(0, process.returncode, process.stderr)
            return output, json.loads(process.stdout)
        self.assertNotEqual(0, process.returncode, process.stdout)
        return output, process.stderr

    def read(self, path):
        return path.read_text(encoding="latin-1")

    def run_auditor(self, name, target, *extra):
        process = subprocess.run(
            [sys.executable, str(AUDITORS[name]), "--input", str(target), "--format", "json", "--exit-code", *extra],
            cwd=ROOT, text=True, capture_output=True, check=False,
        )
        self.assertTrue(process.stdout, process.stderr)
        return process, json.loads(process.stdout)

    @staticmethod
    def codes(payload, field="erros"):
        return {issue["codigo"] for result in payload.get("results", []) for issue in result.get(field, [])}

    def php_files(self, output):
        return sorted(output.rglob("*.php"))

    def assert_lint_and_encoding(self, output):
        files = self.php_files(output)
        self.assertEqual(6, len(files), files)
        for path in files:
            raw = path.read_bytes()
            self.assertFalse(raw.startswith(b"\xef\xbb\xbf"), f"BOM em {path.name}")
            self.assertNotIn(b"\xef\xbf\xbd", raw, f"U+FFFD em {path.name}")
            self.assertNotIn(b"\r\n", raw, f"CRLF em {path.name}")
            self.assertNotIn(b"array(", raw, f"array() em {path.name}")
            self.assertNotIn(b"$_GET", raw, f"$_GET em {path.name}")
            self.assertNotIn(b"$_POST", raw, f"$_POST em {path.name}")
            if PHP:
                lint = subprocess.run([PHP, "-l", str(path)], text=True, capture_output=True, check=False)
                self.assertEqual(0, lint.returncode, lint.stdout + lint.stderr)

    def assert_gates(self, output):
        process, payload = self.run_auditor("rn", output / "rn")
        self.assertNotEqual(2, process.returncode, payload)
        pages = ",".join(str(p) for p in output.glob("*.php"))
        process, payload = self.run_auditor("pagina", pages, "--pagina", "nova")
        self.assertNotEqual(2, process.returncode, payload)
        process, payload = self.run_auditor("banco", output, "--mode", "audit", "--type", "php")
        self.assertNotEqual(2, process.returncode, payload)

    # ---------- geracao completa ----------
    def test_entidade_com_sin_ativo_gera_seis_arquivos_conformes(self):
        output, report = self.generate(contrato_projeto(), "projeto", "--niveis", "3")
        self.assert_lint_and_encoding(output)
        self.assert_gates(output)
        self.assertEqual({"temSinAtivo": True, "temFk": False, "numeroFks": 0, "nn": False}, report["flags"])
        self.assertEqual(3, report["niveis"])

        rn = self.read(output / "rn" / "MdAbcProjetoRN.php")
        self.assertIn("require_once __DIR__ . '/../../../../SEI.php';", rn)
        self.assertIn("validarAuditarPermissao('md_abc_projeto_consultar', __METHOD__", rn)
        self.assertIn("protected function bloquearControlado(", rn)
        self.assertNotIn("bloquearConectado", rn)
        self.assertNotIn("validarAuditarPermissao('md_abc_projeto_listar', __METHOD__, $objMdAbcProjetoDTO);\n\n      //Regras de Negocio\n      //$objInfraException = new InfraException();\n\n      //$objInfraException->lancarValidacoes();\n\n      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());\n      return $objMdAbcProjetoBD->consultar", rn)
        self.assertEqual(2, rn.count("_listar', __METHOD__"))
        self.assertEqual(2, rn.count("_consultar', __METHOD__"))
        self.assertIn("protected function desativarControlado(", rn)
        self.assertNotIn("/* protected function desativarControlado", rn)
        self.assertIn("Identificação não informada.", rn)
        self.assertIn("Data de Cadastramento inválida.", rn)
        self.assertIn("Sinalizador de Exclusão Lógica não informado.", rn)
        self.assertIn("   * @throws InfraException", rn)

        dto = self.read(output / "dto" / "MdAbcProjetoDTO.php")
        self.assertIn(" * @table md_abc_projeto Cadastro de projetos.", dto)
        self.assertIn(" * @column dta_cadastramento Data de cadastramento do projeto.", dto)
        self.assertIn("configurarPK('IdMdAbcProjeto', InfraDTO::$TIPO_PK_NATIVA);", dto)
        self.assertIn("configurarExclusaoLogica('SinAtivo', 'N');", dto)

        lista = self.read(output / "md_abc_projeto_lista.php")
        self.assertIn("require_once __DIR__ . '/../../../SEI.php';", lista)
        self.assertIn("    $bolCheck = false;", lista)
        self.assertIn("case 'md_abc_projeto_reativar':", lista)
        self.assertNotIn("acao_confirmada", lista)
        self.assertIn("'<tr class=\"trVermelha\">'", lista)
        self.assertIn("PaginaSEI::GET('id_md_abc_projeto') !== null", lista)
        self.assertIn("setNumIdMdAbcProjeto((int)$strId);", lista)
        self.assertIn("  PaginaSEI::getInstance()->prepararPaginacao($objMdAbcProjetoDTO);", lista)
        self.assertIn("  PaginaSEI::getInstance()->processarPaginacao($objMdAbcProjetoDTO);", lista)
        self.assertIn("//$objMdAbcProjetoDTO->retStrDescricao();", lista)
        self.assertIn("vertical-align: middle", lista)
        self.assertNotIn("vertical-align: center", lista)
        self.assertIn("A\xe7\xe3o '\".$strAcao.\"' n\xe3o reconhecida.", lista)

        cadastro = self.read(output / "md_abc_projeto_cadastro.php")
        self.assertIn("if (PaginaSEI::POST('sbmCadastrarMdAbcProjeto') !== null) {", cadastro)
        self.assertIn("setNumIdMdAbcProjeto((int)PaginaSEI::GET('id_md_abc_projeto'));", cadastro)
        self.assertIn("setNumIdMdAbcProjeto((int)PaginaSEI::POST('hdnIdMdAbcProjeto'));", cadastro)
        self.assertNotIn("adicionarMensagem('Projeto \"'.PaginaSEI::tratarHTML(", cadastro)
        self.assertIn("alert('Informe a Identifica\xe7\xe3o.');", cadastro)
        self.assertIn('accesskey="m"', cadastro)

        int_ = self.read(output / "int" / "MdAbcProjetoINT.php")
        self.assertIn("adicionarCriterio(['SinAtivo', 'IdMdAbcProjeto'], [InfraDTO::$OPER_IGUAL", int_)
        self.assertNotIn("setStrSinAtivo('S')", int_)
        self.assertIn("   * @throws InfraException", int_)

    def test_entidade_sem_sin_ativo_comenta_blocos_e_valida_dinheiro(self):
        output, report = self.generate(contrato_aquisicao(), "aquisicao", "--niveis", "2")
        self.assert_lint_and_encoding(output)
        self.assert_gates(output)
        self.assertEqual({"temSinAtivo": False, "temFk": True, "numeroFks": 1, "nn": False}, report["flags"])

        rn = self.read(output / "rn" / "MdAbcAquisicaoRN.php")
        self.assertIn("require_once __DIR__ . '/../../../SEI.php';", rn)
        self.assertIn("/* protected function desativarControlado(", rn)
        self.assertIn("/* protected function reativarControlado(", rn)
        self.assertIn("/* protected function bloquearControlado(", rn)
        self.assertIn("} elseif (!InfraUtil::validarDin($objMdAbcAquisicaoDTO->getDinCusto())) {", rn)
        self.assertNotIn("str_replace(',', '.'", rn)
        self.assertIn("Custo inválido.", rn)
        self.assertIn("Projeto não informado.", rn)

        dto = self.read(output / "dto" / "MdAbcAquisicaoDTO.php")
        self.assertIn("adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, 'IdentificacaoMdAbcProjeto', 'identificacao', 'md_abc_projeto');", dto)
        self.assertIn("configurarFK('IdMdAbcProjeto', 'md_abc_projeto', 'id_md_abc_projeto');", dto)

        lista = self.read(output / "md_abc_aquisicao_lista.php")
        self.assertIn("require_once __DIR__ . '/../../SEI.php';", lista)
        self.assertIn("/*\n    case 'md_abc_aquisicao_desativar':", lista)
        self.assertIn("<?php /* if ($bolAcaoDesativar??false) { ?>", lista)
        self.assertIn("<?php } */ ?>", lista)
        self.assertIn("      $bolAcaoDesativar = false;", lista)
        self.assertIn("salvarCamposPost(['selMdAbcProjeto']);", lista)
        self.assertIn("setNumIdMdAbcProjeto((int)$numIdMdAbcProjeto);", lista)
        self.assertIn("MdAbcProjetoINT::montarSelectIdentificacao('', 'Todos', $numIdMdAbcProjeto);", lista)
        self.assertNotIn("acaoDesativar(", lista.split("<?php /* if ($bolAcaoDesativar??false)")[0].split("/*\n      if ($bolAcaoDesativar")[0])

        cadastro = self.read(output / "md_abc_aquisicao_cadastro.php")
        self.assertIn('onkeydown="return infraMascaraDinheiro(this, event)"', cadastro)
        self.assertIn("alert('Selecione um Projeto.');", cadastro)
        self.assertIn("MdAbcProjetoINT::montarSelectIdentificacao('null','&nbsp;',$objMdAbcAquisicaoDTO->getNumIdMdAbcProjeto());", cadastro)
        self.assertIn("throw new InfraException('Aquisi\xe7\xe3o n\xe3o encontrada.');", cadastro)

    def test_relacao_nn_gera_pk_composta_e_paginas_com_rotulos(self):
        output, report = self.generate(contrato_rel(), "rel")
        self.assert_lint_and_encoding(output)
        self.assert_gates(output)
        self.assertTrue(report["flags"]["nn"])
        self.assertTrue(any("fora de web/modulos/" in alert for alert in report["developer_alerts"]))

        dto = self.read(output / "dto" / "MdAbcRelContratoProjDTO.php")
        self.assertEqual(2, dto.count("InfraDTO::$TIPO_PK_INFORMADO"))
        self.assertNotIn("configurarExclusaoLogica", dto)
        self.assertIn("'NumeroMdAbcContrato', 'numero', 'md_abc_contrato'", dto)

        rn = self.read(output / "rn" / "MdAbcRelContratoProjRN.php")
        self.assertIn("validarNumIdMdAbcContrato(", rn)
        self.assertIn("/* protected function desativarControlado(", rn)

        lista = self.read(output / "md_abc_rel_contrato_proj_lista.php")
        self.assertIn("count($arrStrIdComposto)!=2 || !ctype_digit($arrStrIdComposto[0])", lista)
        self.assertIn("PaginaSEI::GET('id_md_abc_contrato') !== null && PaginaSEI::GET('id_md_abc_projeto') !== null", lista)
        self.assertIn("getThOrdenacao($objMdAbcRelContratoProjDTO,'Contrato','NumeroMdAbcContrato'", lista)
        self.assertNotIn("abrirAreaDados('5em');\n  ?>\n  <?php\n  PaginaSEI::getInstance()->fecharAreaDados();", lista)

        cadastro = self.read(output / "md_abc_rel_contrato_proj_cadastro.php")
        self.assertIn('id="lblAssociacao" for="txtAssociacao" accesskey="d"', cadastro)
        self.assertIn("Data de Associa\xe7\xe3o", cadastro)
        self.assertIn("#imgCalAssociacao", cadastro)
        self.assertIn('title="Selecionar Data de Associa\xe7\xe3o"', cadastro)
        self.assertIn("alert('Selecione um Contrato.');", cadastro)
        self.assertIn("alert('Informe a Data de Associa\xe7\xe3o.');", cadastro)
        self.assertIn("setNumIdMdAbcContrato((int)PaginaSEI::GET('id_md_abc_contrato'));", cadastro)
        self.assertNotIn("montarBarraComandosSuperior($arrComandos??false);\nPaginaSEI::getInstance()->abrirAreaDados('5em');\n?>\n<?php\nPaginaSEI::getInstance()->fecharAreaDados();", cadastro)

        int_ = self.read(output / "int" / "MdAbcRelContratoProjINT.php")
        self.assertIn("public static function montarSelectNumeroMdAbcContrato(", int_)
        self.assertIn("'IdMdAbcContrato', 'NumeroMdAbcContrato');", int_)

    def test_sonda_cobre_dth_dbl_opcionais_e_duas_fks_para_mesma_tabela(self):
        output, report = self.generate(contrato_sonda(), "sonda")
        self.assert_lint_and_encoding(output)
        self.assert_gates(output)
        self.assertTrue(any("num prefixo din_" in alert or "sem prefixo din_" in alert for alert in report["developer_alerts"]))
        self.assertTrue(any("id_unidade_origem" in alert for alert in report["developer_alerts"]))

        dto = self.read(output / "dto" / "MdAbcSondaDTO.php")
        self.assertIn("adicionarAtributoTabela(InfraDTO::$PREFIXO_DTH, 'Entrega', 'dth_entrega');", dto)
        self.assertIn("adicionarAtributoTabela(InfraDTO::$PREFIXO_DBL, 'Percentual', 'percentual');", dto)
        self.assertIn("adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, 'SiglaUnidadeOrigem', 'sigla', 'unidade');", dto)
        self.assertIn("adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, 'SiglaUnidadeDestino', 'u2.sigla', 'unidade u2');", dto)
        self.assertIn("configurarFK('IdUnidadeOrigem', 'unidade', 'id_unidade');", dto)
        self.assertIn("configurarFK('IdUnidadeDestino', 'unidade u2', 'u2.id_unidade', InfraDTO::$TIPO_FK_OPCIONAL);", dto)

        rn = self.read(output / "rn" / "MdAbcSondaRN.php")
        self.assertIn("} elseif (!InfraData::validarDataHora($objMdAbcSondaDTO->getDthEntrega())) {", rn)
        self.assertIn("} elseif (!is_numeric($objMdAbcSondaDTO->getDblPercentual())) {", rn)
        self.assertIn("if (InfraString::isBolVazia($objMdAbcSondaDTO->getNumOrdem())) {\n      $objMdAbcSondaDTO->setNumOrdem(null);", rn)
        self.assertIn("if (InfraString::isBolVazia($objMdAbcSondaDTO->getNumIdUnidadeDestino())) {\n      $objMdAbcSondaDTO->setNumIdUnidadeDestino(null);", rn)
        self.assertIn("Unidade de Origem não informada.", rn)

        cadastro = self.read(output / "md_abc_sonda_cadastro.php")
        self.assertIn('onkeypress="return infraMascaraDataHora(this, event)"', cadastro)
        self.assertIn("infraValidarDataHora(document.getElementById('txtEntrega'))", cadastro)
        self.assertIn('onkeypress="return infraMascaraNumero(this, event)"', cadastro)
        self.assertIn('id="selUnidadeOrigem"', cadastro)
        self.assertIn('id="selUnidadeDestino"', cadastro)
        self.assertIn("salvarCamposPost(['selUnidadeOrigem', 'selUnidadeDestino']);", cadastro)
        self.assertIn("setNumIdUnidadeOrigem(PaginaSEI::POST('selUnidadeOrigem'));", cadastro)
        self.assertIn("setNumIdUnidadeDestino(PaginaSEI::POST('selUnidadeDestino'));", cadastro)
        self.assertIn("alert('Selecione uma Unidade de Origem.');", cadastro)
        self.assertNotIn("alert('Selecione uma Unidade de Destino.');", cadastro)
        self.assertIn('id="lblUnidadeDestino" for="selUnidadeDestino" accesskey="d" class="infraLabelOpcional"', cadastro)

        lista = self.read(output / "md_abc_sonda_lista.php")
        self.assertIn("setNumIdUnidadeOrigem((int)$numIdUnidadeOrigem);", lista)
        self.assertIn("setNumIdUnidadeDestino((int)$numIdUnidadeDestino);", lista)
        self.assertIn("UnidadeINT::montarSelectSigla('', 'Todos', $numIdUnidadeDestino);", lista)
        self.assertNotIn("setNumIdUnidade(", lista)

    def test_exemplos_da_skill_geram_e_passam_nos_gates(self):
        for example in sorted(EXAMPLES.glob("*.json")):
            with self.subTest(example=example.name):
                contract = json.loads(example.read_text(encoding="utf-8"))
                output, _ = self.generate(contract, example.stem)
                self.assert_lint_and_encoding(output)
                self.assert_gates(output)

    # ---------- profundidade do require ----------
    def test_profundidade_do_require_e_derivada_do_diretorio_em_web_modulos(self):
        fake_web = self.work / "sei" / "web" / "modulos" / "inst" / "mod"
        output, report = self.generate(contrato_projeto(), str(fake_web.relative_to(self.work)))
        self.assertEqual(3, report["niveis"])
        self.assertIn("'/../../../../SEI.php'", self.read(output / "dto" / "MdAbcProjetoDTO.php"))
        self.assertIn("'/../../../SEI.php'", self.read(output / "md_abc_projeto_lista.php"))
        um_nivel = self.work / "sei" / "web" / "modulos" / "mod1"
        output, report = self.generate(contrato_projeto(), str(um_nivel.relative_to(self.work)))
        self.assertEqual(2, report["niveis"])
        self.assertIn("'/../../../SEI.php'", self.read(output / "rn" / "MdAbcProjetoRN.php"))

    # ---------- validacoes do contrato ----------
    def test_contrato_invalido_falha_com_mensagem_clara(self):
        base = contrato_projeto()
        casos = []

        c = copy.deepcopy(base); c["colunas"].append(coluna("sta_situacao", "char", "Status.", 1)); c["ui"]["ordemFormulario"].append("sta_situacao"); casos.append(("sta_", c, "sta_"))
        c = copy.deepcopy(base); del c["regrasGeracao"]; casos.append(("sem regrasGeracao", c, "regrasGeracao.campoSinAtivo"))
        c = copy.deepcopy(base); c["entidade"]["artigo"] = "x"; casos.append(("artigo", c, "entidade.artigo"))
        c = copy.deepcopy(base); del c["entidade"]["plural"]; casos.append(("sem plural", c, "entidade.plural"))
        c = copy.deepcopy(base); c["ui"]["ordemFormulario"] = ["identificacao"]; casos.append(("ordemFormulario", c, "faltam: descricao, dta_cadastramento"))
        c = copy.deepcopy(base); c["ui"]["campos"]["descricao"]["teclaAtalho"] = "S"; casos.append(("tecla reservada", c, "colide com tecla reservada"))
        c = copy.deepcopy(base); c["colunas"][3]["tipoBanco"] = "timestamp"; casos.append(("timestamp sem dth_", c, "prefixo dth_"))
        c = copy.deepcopy(base); c["entidade"]["tabela"] = "md_abc_rel_contrato_projeto"; c["colunas"][0]["nome"] = "id_md_abc_rel_contrato_projeto"; casos.append(("27 caracteres", c, "exceeds 26"))
        c = copy.deepcopy(base); c["regrasGeracao"]["campoSinAtivo"] = "ativo"; casos.append(("campoSinAtivo", c, "deve ser 'sin_ativo' ou null"))
        c = copy.deepcopy(base); c["entidade"]["campoPrincipal"] = "nome"; casos.append(("campoPrincipal", c, "campoPrincipal"))
        c = copy.deepcopy(base); del c["colunas"][1]["obrigatorio"]; casos.append(("sem obrigatorio", c, "'obrigatorio' booleano"))
        c = copy.deepcopy(base); c["entidade"]["tabela"] = "projeto"; c["colunas"][0]["nome"] = "id_projeto"; casos.append(("sem md_", c, "md_<sigla>_<entidade>"))
        c = copy.deepcopy(contrato_aquisicao()); c["relacionamentos"][0]["tipoFk"] = "opcional"; casos.append(("tipoFk x obrigatorio", c, "tipoFk opcional mas a coluna e obrigatoria"))
        c = copy.deepcopy(contrato_aquisicao()); c["relacionamentos"][0]["tabelaReferencia"] = "usuario"; c["relacionamentos"][0]["campoExibicao"] = "nome"; casos.append(("helper INT inexistente no core", c, "UsuarioINT::montarSelectNome nao existe"))

        for nome, contract, trecho in casos:
            with self.subTest(caso=nome):
                _, stderr = self.generate(contract, re.sub(r"\W", "_", nome), expect_ok=False)
                self.assertIn(trecho, stderr)

    def test_json_invalido_e_no_overwrite(self):
        path = self.work / "quebrado.json"
        path.write_text("{\"entidade\": ", encoding="utf-8")
        process = subprocess.run([sys.executable, str(GENERATOR), str(path), str(self.work / "out")], cwd=ROOT, text=True, capture_output=True, check=False)
        self.assertEqual(1, process.returncode)
        self.assertIn("Contrato JSON invalido", process.stderr)
        self.assertNotIn("Traceback", process.stderr)

        output, _ = self.generate(contrato_projeto(), "dup")
        _, stderr = self.generate(contrato_projeto(), "dup", expect_ok=False)
        self.assertIn("already exists", stderr)

    def test_textos_com_apostrofo_sao_escapados_e_caracteres_proibidos_rejeitados(self):
        contract = contrato_projeto()
        contract["entidade"]["singular"] = "Projeto d'\u00e1gua"
        contract["entidade"]["plural"] = "Projetos d'\u00e1gua"
        contract["ui"]["campos"]["identificacao"]["rotulo"] = "Identifica\u00e7\u00e3o d'\u00e1gua"
        output, _ = self.generate(contract, "apostrofo")
        self.assert_lint_and_encoding(output)
        rn = self.read(output / "rn" / "MdAbcProjetoRN.php")
        self.assertIn("'Erro cadastrando Projeto d\\'\xe1gua.'", rn)
        self.assertIn("'Identifica\xe7\xe3o d\\'\xe1gua possui tamanho superior", rn)
        cadastro = self.read(output / "md_abc_projeto_cadastro.php")
        self.assertIn("alert('Informe a Identifica\xe7\xe3o d\\'\xe1gua.');", cadastro)
        self.assertIn("dentifica\xe7\xe3o d'\xe1gua:</label>", cadastro)
        self.assertIn("throw new InfraException('Projeto d\\'\xe1gua n\xe3o encontrado.');", cadastro)

        for campo, valor in (("singular", 'Projeto "x"'), ("comentario", "Fecha */ o docblock"), ("plural", "A <b>B</b>")):
            with self.subTest(campo=campo):
                bad = contrato_projeto()
                bad["entidade"][campo] = valor
                _, stderr = self.generate(bad, f"texto_{campo}", expect_ok=False)
                self.assertIn(f"entidade.{campo}", stderr)

    def test_escopo_por_unidade_unicidade_dependentes_e_paginacao_desligada(self):
        contract = contrato_projeto()
        contract["colunas"].insert(1, coluna("id_unidade", "int", "Unidade dona do projeto.", fk=True))
        contract["colunas"][2]["unico"] = True
        contract["regrasGeracao"].update({
            "escopoUnidade": "id_unidade",
            "paginacao": False,
            "dependentes": [{"tabela": "md_abc_aquisicao", "coluna": "id_md_abc_projeto", "rotulo": "Aquisição", "artigo": "a"}],
        })
        output, report = self.generate(contract, "escopo")
        self.assert_lint_and_encoding(output)
        self.assert_gates(output)

        dto = self.read(output / "dto" / "MdAbcProjetoDTO.php")
        self.assertIn("adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, 'SiglaUnidade', 'sigla', 'unidade');", dto)
        self.assertIn("configurarFK('IdUnidade', 'unidade', 'id_unidade');", dto)

        rn = self.read(output / "rn" / "MdAbcProjetoRN.php")
        self.assertIn("Unidade não informada.", rn)
        self.assertIn("$objMdAbcProjetoUnicoDTO = new MdAbcProjetoDTO();", rn)
        self.assertIn("$objMdAbcProjetoUnicoDTO->setBolExclusaoLogica(false);", rn)
        self.assertIn("$objMdAbcProjetoUnicoDTO->setNumIdMdAbcProjeto($objMdAbcProjetoDTO->getNumIdMdAbcProjeto(), InfraDTO::$OPER_DIFERENTE);", rn)
        self.assertIn("$objMdAbcProjetoUnicoDTO->setNumIdUnidade($objMdAbcProjetoDTO->getNumIdUnidade());", rn)
        self.assertIn("$objMdAbcProjetoUnicoDTO->setStrIdentificacao($objMdAbcProjetoDTO->getStrIdentificacao());", rn)
        self.assertIn("'Existe outro Projeto com esta Identifica\xe7\xe3o.'", rn)
        self.assertIn("'Existe ocorr\xeancia inativa de Projeto com esta Identifica\xe7\xe3o.'", rn)
        self.assertIn("$objMdAbcAquisicaoDTO->setNumIdMdAbcProjeto($objMdAbcProjetoDTO->getNumIdMdAbcProjeto());", rn)
        self.assertIn("if ($objMdAbcAquisicaoRN->contar($objMdAbcAquisicaoDTO) > 0) {", rn)
        self.assertIn("'Existe Aquisi\xe7\xe3o vinculada ao Projeto.'", rn)
        self.assertEqual(2, rn.count("$objMdAbcAquisicaoRN->contar("), "dependentes em excluir e desativar")

        cadastro = self.read(output / "md_abc_projeto_cadastro.php")
        self.assertNotIn("selUnidade", cadastro)
        self.assertNotIn("txtIdUnidade", cadastro)
        self.assertEqual(4, cadastro.count("setNumIdUnidade(SessaoSEI::getInstance()->getNumIdUnidadeAtual());"), "cadastrar, alterar por GET, alterar por POST e consultar")

        lista = self.read(output / "md_abc_projeto_lista.php")
        self.assertIn("$objMdAbcProjetoDTO->setNumIdUnidade(SessaoSEI::getInstance()->getNumIdUnidadeAtual());", lista)
        self.assertIn("  //PaginaSEI::getInstance()->prepararPaginacao($objMdAbcProjetoDTO);", lista)
        self.assertIn("  //PaginaSEI::getInstance()->processarPaginacao($objMdAbcProjetoDTO);", lista)

        int_ = self.read(output / "int" / "MdAbcProjetoINT.php")
        self.assertIn("$objMdAbcProjetoDTO->setNumIdUnidade(SessaoSEI::getInstance()->getNumIdUnidadeAtual());", int_)

        for nome, mutate, trecho in (
            ("escopo em relacionamentos", lambda c: c["relacionamentos"].append(relacao("id_unidade", "unidade", "sigla")), "nao pode estar em relacionamentos"),
            ("escopo em ordemFormulario", lambda c: c["ui"]["ordemFormulario"].append("id_unidade"), "nao entra em ui.ordemFormulario"),
            ("unico na PK", lambda c: c["colunas"][0].update({"unico": True}), "'unico' nao se aplica a PK"),
            ("dependente sem rotulo", lambda c: c["regrasGeracao"].update({"dependentes": [{"tabela": "md_abc_x", "coluna": "id_md_abc_projeto"}]}), "dependentes exige entradas"),
            ("paginacao nao booleana", lambda c: c["regrasGeracao"].update({"paginacao": "sim"}), "paginacao deve ser booleano"),
        ):
            with self.subTest(caso=nome):
                bad = copy.deepcopy(contract)
                mutate(bad)
                _, stderr = self.generate(bad, "escopo_" + re.sub(r"\W", "_", nome), expect_ok=False)
                self.assertIn(trecho, stderr)

    @unittest.skipUnless(PHP and (INFRA / "InfraBD.php").exists(), "PHP e InfraPHP do repositorio necessarios")
    def test_dto_e_bd_gerados_montam_sql_com_o_infrabd_real(self):
        """Carrega DTO e BD gerados com o InfraDTO e o InfraBD reais e confere o SQL montado, sem banco."""
        modulo = self.work / "sei" / "web" / "modulos" / "inst" / "mod"
        (self.work / "sei" / "web").mkdir(parents=True)
        (self.work / "sei" / "web" / "SEI.php").write_text(SEI_STUB % INFRA, encoding="utf-8")
        for contract, name in ((contrato_projeto(), "p"), (contrato_aquisicao(), "a"), (contrato_rel(), "r"), (contrato_sonda(), "s")):
            self.generate(contract, str(modulo.relative_to(self.work)))
        harness = self.work / "harness.php"
        harness.write_text(BD_HARNESS, encoding="utf-8")
        process = subprocess.run([PHP, str(harness), str(modulo), str(self.work / "sei" / "web" / "SEI.php")], capture_output=True, check=False)
        stdout = process.stdout.decode("latin-1")
        self.assertEqual(0, process.returncode, process.stderr.decode("latin-1") + stdout)
        sqls = {k: [re.sub(r"\s+", " ", v) for v in vs] for k, vs in json.loads(stdout.strip().splitlines()[-1]).items()}
        self.assertEqual({"MdAbcProjetoDTO", "MdAbcAquisicaoDTO", "MdAbcRelContratoProjDTO", "MdAbcSondaDTO"}, set(sqls))

        aquisicao = " ".join(sqls["MdAbcAquisicaoDTO"])
        self.assertIn("INNER JOIN md_abc_projeto ON md_abc_aquisicao.id_md_abc_projeto=md_abc_projeto.id_md_abc_projeto", aquisicao)
        self.assertIn("md_abc_projeto.identificacao AS identificacaomdabcprojeto", aquisicao)
        self.assertIn("INSERT INTO seq_md_abc_aquisicao", aquisicao)
        self.assertRegex(aquisicao, r"INSERT INTO md_abc_aquisicao \([^)]*din_custo[^)]*\) VALUES \(1234\.56,")

        projeto = " ".join(sqls["MdAbcProjetoDTO"])
        self.assertIn("md_abc_projeto.sin_ativo='S'", projeto)
        self.assertIn("UPDATE md_abc_projeto SET md_abc_projeto.sin_ativo='N'", projeto)
        self.assertIn("id_md_abc_projeto IS NOT NULL", projeto)

        rel = " ".join(sqls["MdAbcRelContratoProjDTO"])
        self.assertIn("INNER JOIN md_abc_contrato ON", rel)
        self.assertIn("INNER JOIN md_abc_projeto ON", rel)
        self.assertIn("WHERE md_abc_rel_contrato_proj.id_md_abc_contrato=1 AND md_abc_rel_contrato_proj.id_md_abc_projeto=1", rel)
        self.assertNotIn("seq_md_abc_rel_contrato_proj", rel)

        sonda = " ".join(sqls["MdAbcSondaDTO"])
        self.assertIn("INNER JOIN unidade ON md_abc_sonda.id_unidade_origem=unidade.id_unidade", sonda)
        self.assertIn("LEFT JOIN unidade u2 ON md_abc_sonda.id_unidade_destino=u2.id_unidade", sonda)
        self.assertIn("u2.sigla AS siglaunidadedestino", sonda)
        self.assertIn("'2026-01-01 10:00:00'", sonda)

    def test_nn_sem_rel_gera_com_alerta(self):
        contract = contrato_rel()
        contract["entidade"]["tabela"] = "md_abc_contrato_projeto"
        _, report = self.generate(contract, "nn_sem_rel")
        self.assertTrue(any("md_<sigla>_rel_" in alert for alert in report["developer_alerts"]))


if __name__ == "__main__":
    unittest.main()
