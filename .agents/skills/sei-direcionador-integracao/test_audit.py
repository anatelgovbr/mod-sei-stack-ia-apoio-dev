"""Testes do auditor de reuso do core da skill sei-direcionador-integracao.

    python3 .agents/skills/sei-direcionador-integracao/test_audit.py

Os cenarios rodam o auditor em repositorios git temporarios. A tabela
OPERACAO_DO_METODO e conferida contra o core real quando os fontes existem.
"""

import importlib.util
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

AQUI = Path(__file__).resolve().parent
AUDITOR = AQUI / 'audit.py'
RAIZ = AQUI.parents[2]
CORE = RAIZ / 'fontes' / 'sei' / 'src' / 'main' / 'php' / 'sei' / 'web'
CATALOGO = RAIZ / '.agents' / 'skills' / 'sei-mod-api-operacoes' / 'references' / 'catalogo-operacoes.md'
MODULO = 'fontes/sei/src/main/php/sei/web/modulos/mod/rn/MdModRN.php'

RN_DE_BASE = (
    "<?php\n"
    "class MdModRN extends InfraRN {\n"
    "  protected function legadoControlado(ProcedimentoDTO $objProcedimentoDTO) {\n"
    "    $objAtividadeRN = new AtividadeRN();\n"
    "    $objAtividadeRN->gerarInternaRN0727($objProcedimentoDTO);\n"
    "    //CORPO\n"
    "  }\n"
    "  //NOVA\n"
    "}\n"
)


def carregar_auditor():
    spec = importlib.util.spec_from_file_location('audit_reuso', AUDITOR)
    modulo = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(modulo)
    return modulo


class Repositorio:
    """Repositorio git temporario com um core falso e um modulo commitado na main."""

    def __init__(self, pasta):
        self.pasta = Path(pasta)
        self.git('init', '-q', '-b', 'main')
        self.git('config', 'user.email', 'teste@example.invalid')
        self.git('config', 'user.name', 'teste')
        self.git('config', 'core.autocrlf', 'false')
        for classe, pasta_core in [('AtividadeRN', 'rn'), ('ProcedimentoRN', 'rn'), ('DocumentoRN', 'rn'),
                                   ('SeiRN', 'rn'), ('ProcedimentoDTO', 'dto')]:
            self.escrever(f'fontes/sei/src/main/php/sei/web/{pasta_core}/{classe}.php', f'<?php\nclass {classe} {{}}\n')
        self.escrever(MODULO, RN_DE_BASE)
        self.git('add', '-A')
        self.git('commit', '-q', '-m', 'base')

    def git(self, *args):
        subprocess.run(['git', '-C', str(self.pasta), *args], check=True, capture_output=True)

    def escrever(self, caminho, conteudo, encoding='utf-8'):
        arquivo = self.pasta / caminho
        arquivo.parent.mkdir(parents=True, exist_ok=True)
        arquivo.write_bytes(conteudo.encode(encoding))

    def trocar(self, marca, trecho, caminho=MODULO):
        arquivo = self.pasta / caminho
        arquivo.write_bytes(arquivo.read_bytes().replace(marca.encode(), trecho.encode('latin-1')))


def nada(repo):
    pass


def corpo_legado(trecho):
    return lambda repo: repo.trocar('//CORPO', trecho)


def funcao_nova(trecho):
    return lambda repo: repo.trocar('//NOVA', trecho)


def arquivo_novo(caminho, conteudo, encoding='utf-8'):
    return lambda repo: repo.escrever(caminho, conteudo, encoding)


def commit_em_branch(repo):
    repo.git('checkout', '-q', '-b', 'tarefa')
    repo.trocar('//NOVA', 'public function novaConectado() { return new ProcedimentoDTO(); }')
    repo.git('commit', '-q', '-am', 'tarefa')


CENARIOS = {
    'sem PHP de modulo no diff': {
        'preparar': nada, 'args': [],
        'resultadoEsperado': ('BLOCK', [], [])},
    'linha nova sem gatilho em funcao legada': {
        'preparar': corpo_legado('$intTotal = 1;'), 'args': [],
        'resultadoEsperado': ('PASS', [], [])},
    'chamada nova a metodo interno com operacao': {
        'preparar': corpo_legado('$objAtividadeRN->gerarInternaRN0727($objProcedimentoDTO);'), 'args': [],
        'resultadoEsperado': ('WARN', ['lancarAndamento'], [])},
    'chamada nova com new direto': {
        'preparar': corpo_legado('(new ProcedimentoRN())->concluir($objProcedimentoDTO);'), 'args': [],
        'resultadoEsperado': ('WARN', ['concluirProcesso'], [])},
    'chamada nova por atributo da classe': {
        'preparar': corpo_legado('$this->objDocumentoRN = new DocumentoRN(); $this->objDocumentoRN->bloquearConteudo($objDocumentoDTO);'),
        'args': [], 'resultadoEsperado': ('WARN', ['bloquearDocumento'], [])},
    'chamada interna reescrita sem uso novo': {
        'preparar': lambda repo: repo.trocar('$objAtividadeRN->gerarInternaRN0727($objProcedimentoDTO);', '(new AtividadeRN())->gerarInternaRN0727($objProcedimentoDTO);'),
        'args': [], 'resultadoEsperado': ('PASS', [], [])},
    'metodo homonimo em classe do modulo': {
        'preparar': corpo_legado('$objMdModRN = new MdModRN(); $objMdModRN->concluir(1);'), 'args': [],
        'resultadoEsperado': ('PASS', [], [])},
    'funcao nova que usa classe do core': {
        'preparar': funcao_nova('public function novaConectado() { $objProcedimentoDTO = new ProcedimentoDTO(); return $objProcedimentoDTO; }'),
        'args': [], 'resultadoEsperado': ('WARN', [], ['MdModRN::novaConectado'])},
    'funcao nova so com constante do core': {
        'preparar': funcao_nova('public function nivel() { return ProcedimentoRN::$TA_SIGILOSO . ProcedimentoDTO::NIVEL; }'),
        'args': [], 'resultadoEsperado': ('PASS', [], [])},
    'funcao nova com metodo estatico do core': {
        'preparar': funcao_nova('public function selecao() { return ProcedimentoRN::montarSelect(); }'),
        'args': [], 'resultadoEsperado': ('WARN', [], ['MdModRN::selecao'])},
    'teste em pasta tests do modulo': {
        'preparar': arquivo_novo('fontes/sei/src/main/php/sei/web/modulos/mod/tests/MdModTest.php',
                                 '<?php\nclass MdModTest {\n  public function preparar() { return new ProcedimentoDTO(); }\n}\n'),
        'args': [], 'resultadoEsperado': ('PASS', [], [])},
    'funcao nova sem classe do core': {
        'preparar': funcao_nova('public function somar($intA, $intB) { return $intA + $intB; }'), 'args': [],
        'resultadoEsperado': ('PASS', [], [])},
    'funcao legada com assinatura alterada': {
        'preparar': lambda repo: repo.trocar('$objProcedimentoDTO) {', '$objProcedimentoDTO): void {'), 'args': [],
        'resultadoEsperado': ('PASS', [], [])},
    'classe do core so em comentario e texto': {
        'preparar': funcao_nova('public function texto() {\n    // new ProcedimentoRN()\n    return "ProcedimentoRN";\n  }'),
        'args': [], 'resultadoEsperado': ('PASS', [], [])},
    'funcao abstrata sem corpo': {
        'preparar': funcao_nova('abstract public function nova(ProcedimentoDTO $objProcedimentoDTO);'), 'args': [],
        'resultadoEsperado': ('PASS', [], [])},
    'arquivo novo nao rastreado': {
        'preparar': arquivo_novo('fontes/sei/src/main/php/sei/web/modulos/mod/rn/MdModNovoRN.php',
                                 '<?php\nclass MdModNovoRN extends InfraRN {\n  protected function incluirControlado($objDocumentoDTO) {\n'
                                 '    $objDocumentoRN = new DocumentoRN();\n    return $objDocumentoRN->cadastrarRN0003($objDocumentoDTO);\n  }\n}\n'),
        'args': [], 'resultadoEsperado': ('WARN', ['incluirDocumento'], ['MdModNovoRN::incluirControlado'])},
    'arquivo Latin-1 com acento': {
        'preparar': funcao_nova("public function rotulo() { $strNome = 'ação'; return new ProcedimentoDTO(); }"),
        'args': [], 'resultadoEsperado': ('WARN', [], ['MdModRN::rotulo'])},
    'pagina com apostrofo no HTML antes do PHP': {
        'preparar': arquivo_novo('fontes/sei/src/main/php/sei/web/modulos/mod/md_mod_pagina.php',
                                 "<p>d'agua</p>\n<?php\n$objProcedimentoRN = new ProcedimentoRN();\n$objProcedimentoRN->concluir($objDTO);\n?>\n"),
        'args': [], 'resultadoEsperado': ('WARN', ['concluirProcesso'], [])},
    'mudanca so fora de modulos': {
        'preparar': arquivo_novo('fontes/sei/src/main/php/sei/web/rn/ProcedimentoRN.php', '<?php\nclass ProcedimentoRN { }\n'),
        'args': [], 'resultadoEsperado': ('BLOCK', [], [])},
    'commit na branch comparado com a origem': {
        'preparar': commit_em_branch, 'args': ['--base', 'main'],
        'resultadoEsperado': ('WARN', [], ['MdModRN::novaConectado'])},
    'commit na branch sem base': {
        'preparar': commit_em_branch, 'args': [],
        'resultadoEsperado': ('BLOCK', [], [])},
    'ref de base inexistente': {
        'preparar': corpo_legado('$intTotal = 1;'), 'args': ['--base', 'nao-existe'],
        'resultadoEsperado': ('BLOCK', [], [])},
}


def rodar(pasta, args, formato='json'):
    return subprocess.run([sys.executable, str(AUDITOR), '--format', formato, '--exit-code', *args],
                          cwd=pasta, capture_output=True, text=True, check=False)


class AuditorReusoTest(unittest.TestCase):
    def test_veredito_e_gatilhos_por_cenario(self):
        for nome, caso in CENARIOS.items():
            with self.subTest(cenario=nome), tempfile.TemporaryDirectory() as pasta:
                repo = Repositorio(pasta)
                caso['preparar'](repo)

                processo = rodar(pasta, caso['args'])

                resultado = json.loads(processo.stdout)
                veredito, operacoes, funcoes = caso['resultadoEsperado']
                self.assertEqual(resultado['veredito'], veredito, resultado)
                self.assertEqual(processo.returncode, {'PASS': 0, 'WARN': 1, 'BLOCK': 2}[veredito])
                self.assertEqual([o for c in resultado['chamadas'] for o in c['operacoes']], operacoes)
                self.assertEqual([f['funcao'] for f in resultado['funcoes']], funcoes)

    def test_chamada_aponta_a_linha_do_catalogo(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Repositorio(pasta)
            CENARIOS['chamada nova a metodo interno com operacao']['preparar'](repo)

            resultado = json.loads(rodar(pasta, []).stdout)

            linhas = CATALOGO.read_text(encoding='utf-8').splitlines()
            apontadas = resultado['chamadas'][0]['catalogo'][0].rsplit(':', 1)[1].split(',')
            self.assertTrue(apontadas)
            for numero in apontadas:
                self.assertRegex(linhas[int(numero) - 1], r'^\|\s*`?lancarAndamento`?\s*\|')

    def test_pass_cabe_em_uma_linha(self):
        with tempfile.TemporaryDirectory() as pasta:
            repo = Repositorio(pasta)
            CENARIOS['linha nova sem gatilho em funcao legada']['preparar'](repo)

            processo = rodar(pasta, [], formato='markdown')

            self.assertEqual(processo.stdout.strip().splitlines(), ['Reuso do core: PASS. PHP de modulo no diff: 1. Sem gatilho.'])


@unittest.skipUnless((CORE / 'rn' / 'SeiRN.php').is_file(), 'sem os fontes do core')
class TabelaContraCoreTest(unittest.TestCase):
    """Cada par da tabela: o metodo existe na classe do core, a operacao do SeiRN o chama e esta no catalogo."""

    def test_cada_par_da_tabela_vale_no_core(self):
        auditor = carregar_auditor()
        seirn = (CORE / 'rn' / 'SeiRN.php').read_bytes().decode('latin-1')
        catalogo = CATALOGO.read_text(encoding='utf-8')
        arquivos = {p.stem: p for p in CORE.rglob('*.php') if '/modulos/' not in p.as_posix()}
        for (classe, metodo), operacoes in auditor.OPERACAO_DO_METODO.items():
            for operacao in operacoes:
                with self.subTest(par=f'{classe}->{metodo}', operacao=operacao):
                    fonte = arquivos[classe].read_bytes().decode('latin-1')
                    corpo = corpo_da_operacao(seirn, operacao)

                    variaveis = re.findall(r'\$(\w+)\s*=\s*new\s+' + classe + r'\s*\(', corpo)

                    self.assertRegex(fonte, r'function\s+' + metodo + r'(?:Controlado|Conectado|Interno)?\s*\(')
                    self.assertTrue(any(re.search(r'\$' + v + r'->' + metodo + r'\s*\(', corpo) for v in variaveis), operacao)
                    self.assertRegex(catalogo, r'(?m)^\|\s*`?' + operacao + r'`?\s*\|')


def corpo_da_operacao(seirn, operacao):
    """Corpos das funcoes da operacao no SeiRN, com as variantes Interno, Controlado e Conectado."""
    corpos = []
    for m in re.finditer(r'function\s+' + operacao + r'(?:Interno)?(?:Controlado|Conectado)?\s*\(', seirn):
        abre, nivel = seirn.index('{', m.end()), 0
        for i in range(abre, len(seirn)):
            nivel += {'{': 1, '}': -1}.get(seirn[i], 0)
            if nivel == 0:
                corpos.append(seirn[abre:i])
                break
    return '\n'.join(corpos)


if __name__ == '__main__':
    unittest.main()
