"""Valida a forma de um relatório de sei-revisao-tecnica contra o template.

Uso:
    python3 validar_relatorio.py <relatório.md>

Exit codes: 0 PASS, 1 WARN, 2 BLOCK.
Falha fechado: arquivo inexistente, vazio ou sem as seções do template retorna 2.
Aceita o relatório com ou sem o bloco de código ```markdown externo.
"""
import os
import re
import sys

SECOES = ['## Revisao tecnica', '### Resultado', '### Gates acionados',
          '### Achados', '### Passo a passo do achado']
CAB_GATES = ['Gate', 'Artefatos', 'Estado', 'Evidencia']
CAB_ACHADOS = ['#', 'Estado', 'Severidade', 'Origem', 'Local', 'Achado', 'Menor ajuste']
ESTADOS = {'✅ PASS', '⚠️ WARN', '❌ BLOCK'}
SEVERIDADES = {'BLOQUEANTE', 'ALTA', 'MEDIA', 'BAIXA'}
ORIGENS = {'introduzido', 'ampliado', 'preexistente', 'incerto'}
LIMITES = {'Gate': 6, 'Artefatos': 6, 'Evidencia': 30, 'Achado': 30, 'Menor ajuste': 15}
RE_LOCAL = re.compile(r'(?:[\w.\-]+/)?[\w.\-]+:\d+')
RE_ANCORA = re.compile(r'`[\w.\-]+:\d+`')
RE_ATALHO = re.compile(r'`:\d+`')
RE_RESULTADO = re.compile(r'✅ PASS|❌ BLOCKED')


def palavras(celula):
    """Conta palavras tratando cada trecho em crase como uma palavra."""
    return len(re.sub(r'`[^`]*`', 'X', celula).split())


def celulas(linha):
    return [c.strip() for c in linha.strip().strip('|').split('|')]


def _tabelas(linhas):
    achadas, atual = [], None
    for i, linha in enumerate(linhas, 1):
        if linha.strip().startswith('|'):
            if atual is None:
                atual = []
                achadas.append(atual)
            atual.append((i, linha))
        else:
            atual = None
    return achadas


def _validar_tabela(nome, linhas_tabela, cabecalho, erros):
    if celulas(linhas_tabela[0][1]) != cabecalho:
        erros.append(f'F4 cabeçalho da tabela {nome} diverge do template')
        return
    for num, linha in linhas_tabela[2:]:
        cols = celulas(linha)
        if len(cols) != len(cabecalho):
            erros.append(f'F5 linha {num} tem {len(cols)} colunas, esperado {len(cabecalho)}')
            continue
        campo = dict(zip(cabecalho, cols))
        if campo['Estado'] not in ESTADOS:
            erros.append(f'F6 linha {num}: estado inválido "{campo["Estado"]}"')
        if nome == 'achados':
            if campo['Severidade'] not in SEVERIDADES:
                erros.append(f'F7 linha {num}: severidade inválida "{campo["Severidade"]}"')
            if campo['Origem'] not in ORIGENS:
                erros.append(f'F8 linha {num}: origem inválida "{campo["Origem"]}"')
            local = campo['Local'].strip('`')
            if not RE_LOCAL.fullmatch(local):
                erros.append(f'F9 linha {num}: Local fora de arquivo:linha -> "{local}"')
        for coluna, limite in LIMITES.items():
            if coluna in campo and palavras(campo[coluna]) > limite:
                erros.append(f'F10 linha {num}: coluna {coluna} com '
                             f'{palavras(campo[coluna])} palavras, limite {limite}')


def _sem_cerca(texto):
    """Remove o bloco de código ```markdown que envolve o relatório, se houver."""
    linhas = texto.strip().splitlines()
    if len(linhas) >= 2 and linhas[0].strip() in ('```markdown', '```md', '```') \
            and linhas[-1].strip() == '```':
        return '\n'.join(linhas[1:-1])
    return texto


def validar(texto):
    """Devolve (erros, avisos) sobre a forma do relatório."""
    erros, avisos = [], []
    if not texto.strip():
        return ['F0 relatório vazio'], []
    linhas = _sem_cerca(texto).splitlines()

    if [l for l in linhas if l.startswith('#')] != SECOES:
        erros.append('F1 seções ausentes, extras ou fora da ordem do template')
    if not any(l.startswith('**Escopo**:') for l in linhas):
        erros.append('F2 falta o campo Escopo')
    if not any(l.startswith('**Revisao gerada por**:') for l in linhas):
        erros.append('F2 falta o campo Revisao gerada por')

    tabelas = _tabelas(linhas)
    if len(tabelas) != 2:
        erros.append(f'F3 esperadas 2 tabelas, encontradas {len(tabelas)}')
    else:
        _validar_tabela('gates', tabelas[0], CAB_GATES, erros)
        _validar_tabela('achados', tabelas[1], CAB_ACHADOS, erros)

    for num, linha in enumerate(linhas, 1):
        if not linha.startswith('**Achado'):
            continue
        nomeado = False
        for salto in linha.split(':', 1)[1].split('->'):
            salto = salto.strip()
            if RE_ANCORA.search(salto):
                nomeado = True
            elif not (nomeado and RE_ATALHO.search(salto)):
                erros.append(f'F11 linha {num}: salto sem arquivo:linha -> "{salto[:45]}"')

    if '### Resultado' in linhas:
        ini = linhas.index('### Resultado') + 1
        fim = next((i for i in range(ini, len(linhas))
                    if linhas[i].startswith('#') or linhas[i].startswith('**')), len(linhas))
        corpo = [l for l in linhas[ini:fim] if l.strip()]
        if len(corpo) != 1:
            erros.append(f'F12 Resultado tem {len(corpo)} linhas, esperado 1')
        elif not RE_RESULTADO.fullmatch(corpo[0]):
            erros.append(f'F12 Resultado fora do padrão: "{corpo[0]}"')

    if '### Gates acionados' in linhas:
        for i in range(linhas.index('### Gates acionados') + 1, len(linhas)):
            linha = linhas[i]
            if (not linha.strip() or linha.startswith('#') or linha.strip().startswith('|')
                    or linha.startswith('**') or RE_RESULTADO.fullmatch(linha)):
                continue
            avisos.append(f'F13 linha {i + 1}: prosa fora de célula -> "{linha[:60]}"')
    return erros, avisos


def main(argv):
    if len(argv) != 2:
        print('uso: python3 validar_relatorio.py <relatório.md>')
        return 2
    if not os.path.isfile(argv[1]):
        print(f'ERRO   F0 arquivo inexistente: {argv[1]}')
        return 2
    erros, avisos = validar(open(argv[1], encoding='utf-8').read())
    for item in erros:
        print('ERRO  ', item)
    for item in avisos:
        print('AVISO ', item)
    print(f'\nRESUMO  erros: {len(erros)}  avisos: {len(avisos)}')
    return 2 if erros else (1 if avisos else 0)


if __name__ == '__main__':
    sys.exit(main(sys.argv))
