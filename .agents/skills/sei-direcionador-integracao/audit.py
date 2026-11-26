#!/usr/bin/env python3
"""
sei-direcionador-integracao: auditor de reuso do core no diff.

So olha linhas novas de PHP de modulo do SEI (catraca: o legado nao aparece).
Gatilhos:
  1. chamada nova a metodo interno do core que uma operacao do SeiRN executa;
     reescrever uma chamada que a base ja tinha no arquivo nao conta;
  2. funcao nova, ausente do arquivo de base, que usa classe do core
     (*RN, *DTO, *BD e *INT fora de modulos/); so constante do core nao conta.
Arquivo em pasta tests/ do modulo fica fora dos gatilhos.
Sem gatilho, imprime uma linha. Com --exit-code: 0=PASS, 1=WARN, 2=BLOCK.
"""

import argparse
import bisect
import collections
import json
from pathlib import Path
import re
import subprocess
import sys

MODULOS = 'fontes/sei/src/main/php/sei/web/modulos'
CORE_WEB = 'fontes/sei/src/main/php/sei/web'
CATALOGO = Path(__file__).resolve().parents[1] / 'sei-mod-api-operacoes' / 'references' / 'catalogo-operacoes.md'
CATALOGO_REL = '.agents/skills/sei-mod-api-operacoes/references/catalogo-operacoes.md'

# Metodo interno do core -> operacao do SeiRN que o executa. Entra so metodo de
# escrita que a operacao chama; test_audit.py confere cada par contra o core.
OPERACAO_DO_METODO = {
    ('AtividadeRN', 'atribuirRN0985'): ['atribuirProcesso'],
    ('AtividadeRN', 'enviarRN0023'): ['enviarProcesso'],
    ('AtividadeRN', 'gerarInternaRN0727'): ['lancarAndamento'],
    ('AndamentoMarcadorRN', 'cadastrar'): ['definirMarcador'],
    ('AnexoRN', 'adicionar'): ['adicionarArquivo'],
    ('AnexoRN', 'adicionarConteudo'): ['adicionarConteudoArquivo'],
    ('AnotacaoRN', 'registrar'): ['registrarAnotacao'],
    ('BlocoRN', 'alterarRN1274'): ['alterarBloco'],
    ('BlocoRN', 'cadastrarRN1273'): ['gerarBloco'],
    ('BlocoRN', 'cancelarDisponibilizacao'): ['cancelarDisponibilizacaoBloco'],
    ('BlocoRN', 'concluir'): ['concluirBloco'],
    ('BlocoRN', 'disponibilizar'): ['disponibilizarBloco'],
    ('BlocoRN', 'excluirRN1275'): ['excluirBloco'],
    ('BlocoRN', 'reabrir'): ['reabrirBloco'],
    ('BlocoRN', 'retornar'): ['devolverBloco'],
    ('ContatoRN', 'alterarRN0323'): ['atualizarContatos'],
    ('ContatoRN', 'cadastrarRN0322'): ['atualizarContatos'],
    ('ContatoRN', 'desativarRN0451'): ['atualizarContatos'],
    ('ContatoRN', 'excluirRN0326'): ['atualizarContatos'],
    ('ContatoRN', 'reativarRN0452'): ['atualizarContatos'],
    ('ControlePrazoRN', 'concluir'): ['concluirControlePrazo'],
    ('ControlePrazoRN', 'definir'): ['definirControlePrazo'],
    ('ControlePrazoRN', 'excluir'): ['removerControlePrazo'],
    ('DocumentoRN', 'bloquearConteudo'): ['bloquearDocumento'],
    ('DocumentoRN', 'cadastrarRN0003'): ['incluirDocumento'],
    ('DocumentoRN', 'cancelar'): ['cancelarDocumento'],
    ('DocumentoRN', 'excluirRN0006'): ['excluirDocumento'],
    ('EmailRN', 'enviar'): ['enviarEmail'],
    ('OuvidoriaRN', 'registrarOuvidoriaRN1148'): ['registrarOuvidoria'],
    ('ProcedimentoRN', 'anexar'): ['anexarProcesso'],
    ('ProcedimentoRN', 'bloquear'): ['bloquearProcesso'],
    ('ProcedimentoRN', 'concluir'): ['concluirProcesso'],
    ('ProcedimentoRN', 'desanexar'): ['desanexarProcesso'],
    ('ProcedimentoRN', 'desbloquear'): ['desbloquearProcesso'],
    ('ProcedimentoRN', 'excluirRN0280'): ['excluirProcesso'],
    ('ProcedimentoRN', 'gerarRN0156'): ['gerarProcedimento'],
    ('ProcedimentoRN', 'reabrirRN0966'): ['reabrirProcesso'],
    ('ProcedimentoRN', 'relacionarProcedimentoRN1020'): ['relacionarProcesso'],
    ('ProcedimentoRN', 'removerRelacionamentoProcedimentoRN1021'): ['removerRelacionamentoProcesso'],
    ('ProcedimentoRN', 'removerSobrestamentoRN1017'): ['removerSobrestamentoProcesso'],
    ('ProcedimentoRN', 'sobrestarRN1014'): ['sobrestarProcesso'],
    ('PublicacaoRN', 'agendarRN1041'): ['agendarPublicacao'],
    ('PublicacaoRN', 'alterarAgendamentoRN1042'): ['alterarPublicacao'],
    ('PublicacaoRN', 'cancelarAgendamentoRN1043'): ['cancelarAgendamentoPublicacao'],
    ('PublicacaoRN', 'confirmarDisponibilizacaoRN1115'): ['confirmarDisponibilizacaoPublicacao'],
    ('RelBlocoProtocoloRN', 'cadastrarMultiplo'): ['incluirDocumentoBloco', 'incluirProcessoBloco'],
    ('RelBlocoProtocoloRN', 'excluirRN1289'): ['retirarDocumentoBloco', 'retirarProcessoBloco'],
}

RE_HUNK = re.compile(r'^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@', re.M)
RE_FUNCAO = re.compile(r'\bfunction\s+&?\s*(\w+)\s*\(')
RE_CLASSE = re.compile(r'\b(?:class|trait|interface)\s+(\w+)')
RE_NEW_VAR = re.compile(r'\$(?:this->)?(\w+)\s*=\s*new\s+\\?(\w+)\s*\(')
RE_CHAMADA_VAR = re.compile(r'\$(?:this->)?(\w+)\s*->\s*(\w+)\s*\(')
RE_CHAMADA_NEW = re.compile(r'new\s+\\?(\w+)\s*\(\s*\)\s*\)\s*->\s*(\w+)\s*\(')
RE_CORE = re.compile(r'(RN|DTO|BD|INT)\.php$')


def mascarar(conteudo):
    """Troca HTML fora de <?php, comentario e texto entre aspas por espaco, preservando as linhas."""
    chars = list(conteudo)
    n = len(chars)

    def apagar(inicio, fim):
        for k in range(inicio, fim):
            if chars[k] not in '\r\n':
                chars[k] = ' '

    i, php = 0, False
    while i < n:
        if not php:
            abre = conteudo.find('<?', i)
            apagar(i, n if abre < 0 else abre)
            if abre < 0:
                break
            php = True
            i = abre + (5 if conteudo.startswith('<?php', abre) else 3 if conteudo.startswith('<?=', abre) else 2)
            continue
        c = conteudo[i]
        if conteudo.startswith('?>', i):
            php, i = False, i + 2
            continue
        if c in '\'"':
            j = i + 1
            while j < n and conteudo[j] != c:
                j += 2 if conteudo[j] == '\\' else 1
            apagar(i + 1, min(j, n))
            i = j + 1
            continue
        if conteudo.startswith('//', i) or (c == '#' and not conteudo.startswith('#[', i)):
            fim = i
            while fim < n and conteudo[fim] != '\n' and not conteudo.startswith('?>', fim):
                fim += 1
            apagar(i, fim)
            i = fim
            continue
        if conteudo.startswith('/*', i):
            fim = conteudo.find('*/', i + 2)
            fim = n if fim < 0 else fim + 2
            apagar(i, fim)
            i = fim
            continue
        i += 1
    return ''.join(chars)


def linhas_acrescentadas(diff):
    """Numeros das linhas novas nos hunks de um diff -U0."""
    linhas = set()
    for m in RE_HUNK.finditer(diff):
        inicio, qtd = int(m.group(1)), int(m.group(2) or 1)
        linhas.update(range(inicio, inicio + qtd))
    return linhas


def classes_do_core(raiz):
    """Classes *RN, *DTO, *BD e *INT do SEI fora de modulos/, menos o SeiRN."""
    return {p.stem for p in (Path(raiz) / CORE_WEB).rglob('*.php')
            if RE_CORE.search(p.name) and p.stem != 'SeiRN' and '/modulos/' not in p.as_posix()}


def corpo(codigo, inicio):
    """Posicoes de abertura e fechamento do corpo da funcao, ou None sem corpo."""
    abre, ponto_virgula = codigo.find('{', inicio), codigo.find(';', inicio)
    if abre < 0 or 0 <= ponto_virgula < abre:
        return None
    nivel = 0
    for i in range(abre, len(codigo)):
        if codigo[i] == '{':
            nivel += 1
        elif codigo[i] == '}':
            nivel -= 1
            if nivel == 0:
                return abre, i
    return abre, len(codigo) - 1


def pares_de_chamada(codigo):
    """Conta as chamadas (classe, metodo) de um codigo ja mascarado."""
    tipos = dict(RE_NEW_VAR.findall(codigo))
    pares = collections.Counter((tipos.get(var), met) for var, met in RE_CHAMADA_VAR.findall(codigo))
    pares.update(RE_CHAMADA_NEW.findall(codigo))
    return pares


def analisar(arquivos, core):
    """arquivos: {caminho: (conteudo, linhas novas, conteudo de base)}. Devolve chamadas e funcoes."""
    # Classe::$X e Classe::CONSTANTE so leem constante; nao contam como uso do core.
    re_core = re.compile(r'\b(' + '|'.join(sorted(core, key=len, reverse=True)) + r')\b'
                         r'(?!\s*::\s*(?:\$|[A-Z][A-Z0-9_]*\b(?!\s*\()))')
    chamadas, funcoes = [], []
    for caminho, (conteudo, novas, base) in sorted(arquivos.items()):
        if '/tests/' in caminho:
            continue
        codigo = mascarar(conteudo)
        linhas = codigo.split('\n')
        tipos = dict(RE_NEW_VAR.findall(codigo))
        codigo_base = mascarar(base)
        usos, usos_base = pares_de_chamada(codigo), pares_de_chamada(codigo_base)
        for numero in sorted(n for n in novas if n <= len(linhas)):
            texto = linhas[numero - 1]
            pares = [(tipos.get(var), met) for var, met in RE_CHAMADA_VAR.findall(texto)]
            for cls, met in pares + RE_CHAMADA_NEW.findall(texto):
                if (cls, met) in OPERACAO_DO_METODO and usos[(cls, met)] > usos_base[(cls, met)]:
                    chamadas.append({'arquivo': caminho, 'linha': numero, 'classe': cls, 'metodo': met,
                                     'operacoes': OPERACAO_DO_METODO[(cls, met)]})
        antigas = set(RE_FUNCAO.findall(codigo_base))
        quebras = [m.start() for m in re.finditer('\n', codigo)]
        donos = [(m.start(), m.group(1)) for m in RE_CLASSE.finditer(codigo)]
        for m in RE_FUNCAO.finditer(codigo):
            numero = bisect.bisect_left(quebras, m.start()) + 1
            intervalo = corpo(codigo, m.end())
            if m.group(1) in antigas or numero not in novas or not intervalo:
                continue
            usadas = sorted(set(re_core.findall(codigo[intervalo[0]:intervalo[1] + 1])))
            if not usadas:
                continue
            dono = [nome for posicao, nome in donos if posicao < m.start()]
            funcoes.append({'arquivo': caminho, 'linha': numero, 'classes': usadas,
                            'funcao': f'{dono[-1]}::{m.group(1)}' if dono else m.group(1)})
    return chamadas, funcoes


def git(raiz, *args, check=True):
    processo = subprocess.run(['git', '-C', str(raiz), *args], capture_output=True, check=check)
    return processo.stdout.decode('utf-8', 'replace')


def coletar(raiz, base):
    """PHP de modulo do diff contra o merge-base de base com HEAD, mais os nao rastreados."""
    ponto = git(raiz, 'merge-base', base, 'HEAD').strip()
    spec = f'{MODULOS}/*.php'
    alterados = set(filter(None, git(raiz, 'diff', '-z', '--name-only', ponto, '--', spec).split('\0')))
    novos = set(filter(None, git(raiz, 'ls-files', '-z', '--others', '--exclude-standard', '--', spec).split('\0')))
    arquivos = {}
    for nome in sorted(alterados | novos):
        caminho = Path(raiz) / nome
        if not caminho.is_file():
            arquivos[nome] = ('', set(), '')
            continue
        conteudo = caminho.read_bytes().decode('latin-1')
        if nome in novos:
            arquivos[nome] = (conteudo, set(range(1, conteudo.count('\n') + 2)), '')
            continue
        diff = git(raiz, 'diff', '-U0', ponto, '--', nome)
        arquivos[nome] = (conteudo, linhas_acrescentadas(diff), git(raiz, 'show', f'{ponto}:{nome}', check=False))
    return arquivos


def linhas_no_catalogo(operacao):
    try:
        texto = CATALOGO.read_text(encoding='utf-8').splitlines()
    except OSError:
        return []
    padrao = re.compile(r'\|\s*`?' + re.escape(operacao) + r'`?\s*\|')
    return [str(i) for i, linha in enumerate(texto, 1) if padrao.match(linha)]


def montar(arquivos, chamadas, funcoes, base, erro=None):
    vazio = {'analisados': 0, 'chamadas': [], 'funcoes': []}
    if erro:
        return {'veredito': 'BLOCK', 'mensagem': erro, **vazio}
    if not arquivos:
        dica = '; para commits da branch, use --base <branch de origem>' if base == 'HEAD' else ''
        return {'veredito': 'BLOCK', 'mensagem': f'nenhum PHP de modulo do SEI no diff contra {base}{dica}', **vazio}
    for chamada in chamadas:
        chamada['catalogo'] = [f"{CATALOGO_REL}:{','.join(linhas)}"
                               for linhas in map(linhas_no_catalogo, chamada['operacoes']) if linhas]
    return {'veredito': 'WARN' if chamadas or funcoes else 'PASS', 'analisados': len(arquivos),
            'chamadas': chamadas, 'funcoes': funcoes}


def em_texto(resultado):
    cabecalho = f"Reuso do core: {resultado['veredito']}."
    if resultado['veredito'] == 'BLOCK':
        return f"{cabecalho} {resultado['mensagem']}."
    if resultado['veredito'] == 'PASS':
        return f"{cabecalho} PHP de modulo no diff: {resultado['analisados']}. Sem gatilho."
    saida = [f"{cabecalho} PHP de modulo no diff: {resultado['analisados']}."]
    if resultado['chamadas']:
        saida.append('Chamada nova a metodo interno que uma operacao do SeiRN executa. '
                     'Aplique `sei-direcionador-integracao` a cada chamada, a partir da linha do catalogo indicada:')
        for c in resultado['chamadas']:
            operacoes = ', '.join('SeiRN::' + o for o in c['operacoes'])
            saida.append(f"- {c['arquivo']}:{c['linha']} {c['classe']}->{c['metodo']} -> {operacoes} ({'; '.join(c['catalogo'])})")
    if resultado['funcoes']:
        saida.append('Funcao nova que usa classe do core. Aplique `sei-direcionador-integracao` a cada funcao '
                     'e compare o veredito com a linha `Reuso do core:` do plano:')
        for f in resultado['funcoes']:
            saida.append(f"- {f['arquivo']}:{f['linha']} {f['funcao']} usa {', '.join(f['classes'])}")
    return '\n'.join(saida)


def main():
    parser = argparse.ArgumentParser(description='sei-direcionador-integracao: auditor de reuso do core no diff')
    parser.add_argument('--base', default='HEAD',
                        help='Ref de comparacao; usa o merge-base com HEAD. Padrao HEAD: a entrega nao commitada')
    parser.add_argument('--format', choices=['markdown', 'json'], default='markdown', help='Formato de saida')
    parser.add_argument('--exit-code', action='store_true', help='Sai com 0=PASS, 1=WARN, 2=BLOCK')
    args = parser.parse_args()

    arquivos, chamadas, funcoes, erro = {}, [], [], None
    try:
        raiz = git(Path.cwd(), 'rev-parse', '--show-toplevel').strip()
        arquivos = coletar(raiz, args.base)
        core = classes_do_core(raiz)
        if arquivos and not core:
            erro = f'nenhuma classe do core em {CORE_WEB}'
        elif arquivos:
            chamadas, funcoes = analisar(arquivos, core)
    except subprocess.CalledProcessError as objErroGit:
        erro = 'git falhou: ' + objErroGit.stderr.decode('utf-8', 'replace').strip()

    resultado = montar(arquivos, chamadas, funcoes, args.base, erro)
    print(json.dumps(resultado, ensure_ascii=False, indent=2) if args.format == 'json' else em_texto(resultado))
    if args.exit_code:
        sys.exit({'PASS': 0, 'WARN': 1, 'BLOCK': 2}[resultado['veredito']])


if __name__ == '__main__':
    main()
