#!/usr/bin/env python3
"""Verifica os artefatos Markdown atuais de um dicionario de dados.

Subcomandos:
    formato          valida dicionario_tabelas.md ou dicionario_colunas.md
    tabelas-colunas  cruza os dois dicionarios do mesmo alvo
    changelog        valida CHANGELOG.md e, quando presente, cruza as colunas
    diff             compara duas versoes da estrutura atual de colunas

Saida: 0 sem achado, 1 com divergencia, 2 para entrada invalida.
"""
import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

VERSION = "1.0.0"
SKILL_NAME = "dicionario-de-dados-codebase"

HEADER_TABELAS = "| Tabela | Descrição |"
SEPARADOR_TABELAS = "|---|---|"
HEADER_COLUNAS = "| Tabela | Coluna | Descrição |"
SEPARADOR_COLUNAS = "|---|---|---|"
HEADER_INDICE = "## Índice de Tabelas"

RE_TITULO_DICIONARIO = re.compile(r"^# (\S(?:.*\S)?) - (\S(?:.*\S)?)$")
RE_TITULO_CHANGELOG = re.compile(r"^# \S(?:.*\S)?$")
RE_SECAO = re.compile(r"^## (.+)$")

# Separador entre o termo e o motivo: hifen entre espacos. Travessao nao e usado.
RE_MARCADOR_LACUNA = re.compile(
    r"TODO:\s*([^.|]*?)"
    r"(?:\s+-\s+((?:(?!TODO:)[^|])*?))?"
    r"\s*(?=\.(?:\s|$)|TODO:|\||$)"
)

TERMOS_COLUNA = (
    "propriedade ou conceito",
    "entidade ou evento",
    "significado e criterio",
    "momento, periodo ou condicao",
    "unidade, moeda, escala, dominio ou referencia",
    "captura, origem ou regra",
    "semantica da ausencia",
    "funcao",
    "distincao ou limitacao",
)

TERMOS_TABELA = (
    "entidade, evento, relacao ou resultado de negocio",
    "granularidade",
    "evento ou criterio",
    "escopo",
    "exclusoes relevantes",
    "estado atual, historico, vigencia, fotografia ou agregacao",
    "momento ou periodo",
    "origem",
    "processos, operacoes ou decisoes",
    "limitacoes",
)
RE_ITEM_INDICE = re.compile(r"^- \[(.+)]\(#([^)]+)\)$")

RE_VERSAO_CHANGELOG = re.compile(r"^## \[(.*)]$")
RE_CATEGORIA_CHANGELOG = re.compile(r"^### (.+)$")
RE_TABELA_CHANGELOG = re.compile(
    r"^- \*\*Tabela `([^`]+)`\*\*(?: \((.+)\))?$"
)
RE_TOPICO_CHANGELOG = re.compile(
    r"^  - \*\*(Colunas|Chaves primárias|Chaves estrangeiras|Índices|"
    r"Restrições|Propriedades da tabela)\*\*$"
)
RE_OBJETO_CHANGELOG = re.compile(
    r"^    - \*\*(Nova|Alterada|Excluída|Novo|Alterado|Excluído) `([^`]+)`\*\*"
    r"(?:: (.+)| \((.+)\))?$"
)
RE_RENOMEACAO = re.compile(r"^renomeada de `([^`]+)`\.$", re.IGNORECASE)
RE_RENOMEACAO_TABELA = re.compile(r"^renomeada de `([^`]+)`$", re.IGNORECASE)

CATEGORIAS = ("Adicionado", "Alterado", "Excluído")
TOPICOS = (
    "Colunas",
    "Chaves primárias",
    "Chaves estrangeiras",
    "Índices",
    "Restrições",
    "Propriedades da tabela",
)


class EntradaInvalida(Exception):
    """Entrada ausente, ilegivel ou fora do contrato."""


def ler_texto(caminho):
    """Le um artefato em UTF-8 e converte falha de entrada em codigo 2."""
    try:
        return Path(caminho).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as e:
        print(f"ERRO: {caminho}: {e}", file=sys.stderr)
        raise EntradaInvalida from e


def compilar_regex(valor):
    try:
        return re.compile(valor)
    except re.error as e:
        raise argparse.ArgumentTypeError(f"regex invalida: {e}") from e


def parse_ordem_versoes(valor):
    versoes = [item.strip() for item in valor.split(",")]
    if not versoes or any(not item for item in versoes):
        raise argparse.ArgumentTypeError("informe versoes nao vazias separadas por virgula")
    if len(versoes) != len(set(versoes)):
        raise argparse.ArgumentTypeError("a ordem de versoes nao pode conter duplicidades")
    return versoes


def linha_markdown(linha, quantidade):
    """Separa uma linha Markdown sem dividir pipes escapados com barra."""
    texto = linha.strip()
    if not texto.startswith("|") or not texto.endswith("|"):
        return None
    if re.search(r"&(?:#0*124|#x0*7c|vert|verbar|verticalline);", texto, re.IGNORECASE):
        return None
    if re.search(r"\\{2,}\|", texto):
        return None
    celulas = []
    celula = []
    pos = 1
    while pos < len(texto) - 1:
        caractere = texto[pos]
        if caractere == "\\" and pos + 1 < len(texto) - 1 and texto[pos + 1] == "|":
            celula.extend((caractere, "|"))
            pos += 2
            continue
        if caractere == "|":
            celulas.append("".join(celula).strip())
            celula = []
        else:
            celula.append(caractere)
        pos += 1
    celulas.append("".join(celula).strip())
    return celulas if len(celulas) == quantidade else None


def validar_titulo_dicionario(linhas, erros, padrao_versao=None):
    if not linhas:
        erros.append("titulo ausente")
        return None
    if sum(1 for linha in linhas if linha.startswith("# ")) != 1:
        erros.append("o dicionario deve conter exatamente um titulo H1")
    match = RE_TITULO_DICIONARIO.fullmatch(linhas[0])
    if not match:
        erros.append("titulo deve seguir '# <titulo> - <versao nao vazia>'")
        return None
    versao = match.group(2)
    if padrao_versao and not padrao_versao.fullmatch(versao):
        erros.append(f"versao '{versao}' nao corresponde a --padrao-versao")
    return match.group(1), versao


def normalizar_identificador(identificador):
    """Compara o identificador renderizado, removendo o escape Markdown de pipe."""
    return identificador.replace(r"\|", "|").strip()


def ancora_markdown(identificador):
    """Calcula a ancora de heading usada pelo Markdown para o subconjunto aceito."""
    texto = normalizar_identificador(identificador).lower()
    texto = re.sub(r"[^\w\s-]", "", texto)
    return re.sub(r"\s", "-", texto)


def ancoras_markdown(identificadores):
    """Resolve colisoes de ancora na ordem das secoes."""
    ocorrencias = Counter()
    resultado = []
    for identificador in identificadores:
        base = ancora_markdown(identificador)
        sufixo = ocorrencias[base]
        resultado.append(base if sufixo == 0 else f"{base}-{sufixo}")
        ocorrencias[base] += 1
    return resultado


def parse_dicionario_tabelas(caminho, padrao_versao=None):
    """Retorna descricoes, ordem e erros do dicionario_tabelas.md atual."""
    linhas = ler_texto(caminho).splitlines()
    while linhas and linhas[-1] == "":
        linhas.pop()
    erros = []
    descricoes = {}
    ordem = []
    validar_titulo_dicionario(linhas, erros, padrao_versao)

    if len(linhas) < 2 or linhas[1] != "":
        erros.append("linha em branco obrigatoria entre titulo e tabela")
    if len(linhas) < 3 or linhas[2] != HEADER_TABELAS:
        erros.append(f"cabecalho exato obrigatorio: {HEADER_TABELAS}")
        return descricoes, ordem, erros
    if len(linhas) < 4 or linhas[3] != SEPARADOR_TABELAS:
        erros.append(f"separador exato obrigatorio: {SEPARADOR_TABELAS}")

    for numero, linha in enumerate(linhas[4:], start=5):
        if linha == "":
            erros.append(f"linha em branco inesperada na tabela de tabelas: {numero}")
            continue
        celulas = linha_markdown(linha, 2)
        if celulas is None:
            erros.append(f"linha {numero} invalida na tabela de tabelas")
            continue
        nome_renderizado, descricao = celulas
        nome = normalizar_identificador(nome_renderizado)
        if not nome:
            erros.append(f"identificador de tabela vazio na linha {numero}")
            continue
        if not descricao:
            erros.append(f"descricao vazia: {nome}")
        if nome in descricoes:
            erros.append(f"tabela duplicada: {nome}")
        descricoes[nome] = descricao
        ordem.append(nome)

    if not descricoes:
        erros.append("nenhuma tabela encontrada")
    if ordem != sorted(ordem):
        erros.append("tabelas fora de ordem alfabetica")
    return descricoes, ordem, erros


def parse_dicionario_colunas(caminho, padrao_versao=None):
    """Retorna tabelas, colunas, descricoes, indice e erros da estrutura atual."""
    linhas = ler_texto(caminho).splitlines()
    while linhas and linhas[-1] == "":
        linhas.pop()
    erros = []
    tabelas = {}
    ordem_colunas = {}
    descricoes = {}
    indice = []
    destinos = []
    validar_titulo_dicionario(linhas, erros, padrao_versao)

    cabecalhos = [i for i, linha in enumerate(linhas) if linha.startswith("## ")]
    indices = [i for i in cabecalhos if linhas[i] == HEADER_INDICE]
    if len(indices) != 1:
        erros.append("indice de tabelas obrigatorio e unico")
        indice_pos = None
    else:
        indice_pos = indices[0]

    if len(linhas) < 2 or linhas[1] != "" or len(linhas) < 3 or linhas[2] != HEADER_INDICE:
        erros.append("o indice deve vir imediatamente apos o titulo")

    if indice_pos is not None:
        fim_indice = next((i for i in cabecalhos if i > indice_pos), len(linhas))
        corpo_indice = linhas[indice_pos + 1:fim_indice]
        if not corpo_indice or corpo_indice[0] != "":
            erros.append("linha em branco obrigatoria depois do titulo do indice")
        if not corpo_indice or corpo_indice[-1] != "":
            erros.append("linha em branco obrigatoria entre indice e primeira secao")
        inicio_itens = 1 if corpo_indice and corpo_indice[0] == "" else 0
        fim_itens = len(corpo_indice) - 1 if corpo_indice and corpo_indice[-1] == "" else len(corpo_indice)
        for deslocamento, linha in enumerate(corpo_indice[inicio_itens:fim_itens], start=inicio_itens):
            numero = indice_pos + deslocamento + 2
            if linha == "":
                erros.append(f"linha em branco inesperada no indice na linha {numero}")
                continue
            match = RE_ITEM_INDICE.fullmatch(linha)
            if not match:
                erros.append(f"entrada invalida no indice na linha {numero}")
                continue
            nome = normalizar_identificador(match.group(1))
            destino = match.group(2).strip()
            if not nome or not destino:
                erros.append(f"entrada invalida no indice na linha {numero}")
                continue
            indice.append(nome)
            destinos.append(destino)
        if not indice:
            erros.append("indice de tabelas vazio")

    nomes_secoes = []
    secoes = [i for i in cabecalhos if i != indice_pos]
    for posicao, inicio in enumerate(secoes):
        fim = secoes[posicao + 1] if posicao + 1 < len(secoes) else len(linhas)
        match_secao = RE_SECAO.fullmatch(linhas[inicio])
        if not match_secao or not match_secao.group(1).strip():
            erros.append(f"cabecalho de secao invalido na linha {inicio + 1}")
            continue
        nome_renderizado = match_secao.group(1).strip()
        nome = normalizar_identificador(nome_renderizado)
        if nome == "Índice de Tabelas":
            continue
        nomes_secoes.append(nome)
        if nome in tabelas:
            erros.append(f"secao duplicada: {nome}")

        corpo = linhas[inicio + 1:fim]
        if corpo and corpo[-1] == "":
            corpo = corpo[:-1]
        if len(corpo) < 1 or corpo[0] != "":
            erros.append(f"{nome}: linha em branco obrigatoria depois do cabecalho da secao")
        descricao = corpo[1].strip() if len(corpo) > 1 else ""
        if not descricao:
            erros.append(f"descricao ausente: {nome}")
        if len(corpo) < 3 or corpo[2] != "":
            erros.append(f"{nome}: linha em branco obrigatoria depois da descricao")
        if len(corpo) < 4 or corpo[3] != HEADER_COLUNAS:
            erros.append(f"{nome}: cabecalho exato obrigatorio: {HEADER_COLUNAS}")
        if len(corpo) < 5 or corpo[4] != SEPARADOR_COLUNAS:
            erros.append(f"{nome}: separador exato obrigatorio: {SEPARADOR_COLUNAS}")

        colunas = {}
        ordem = []
        for deslocamento, linha in enumerate(corpo[5:], start=inicio + 7):
            if linha == "":
                erros.append(f"linha {deslocamento} invalida na secao {nome}")
                continue
            celulas = linha_markdown(linha, 3)
            if celulas is None:
                erros.append(f"linha {deslocamento} invalida na secao {nome}")
                continue
            tabela_renderizada, coluna_renderizada, descricao_coluna = celulas
            tabela_valor = normalizar_identificador(tabela_renderizada)
            coluna = normalizar_identificador(coluna_renderizada)
            if tabela_valor != nome:
                erros.append(
                    f"coluna Tabela diverge do cabecalho da secao em {nome}: '{tabela_valor}'"
                )
            if not coluna:
                erros.append(f"identificador de coluna vazio em {nome}")
                continue
            if not descricao_coluna:
                erros.append(f"descricao vazia: {nome}.{coluna}")
            if coluna in colunas:
                erros.append(f"coluna duplicada em {nome}: {coluna}")
            colunas[coluna] = descricao_coluna
            ordem.append(coluna)

        if not colunas:
            erros.append(f"tabela sem colunas: {nome}")
        tabelas[nome] = colunas
        ordem_colunas[nome] = ordem
        descricoes[nome] = descricao

    if not nomes_secoes:
        erros.append("nenhuma secao de tabela encontrada")
    for nome, quantidade in Counter(indice).items():
        if quantidade > 1:
            erros.append(f"entrada duplicada no indice: {nome}")
    for destino, quantidade in Counter(destinos).items():
        if quantidade > 1:
            erros.append(f"destino duplicado no indice: #{destino}")
    if indice != nomes_secoes:
        erros.append("indice deve corresponder 1:1 e na mesma ordem as secoes de tabela")
    for nome, destino, esperado in zip(indice, destinos, ancoras_markdown(indice)):
        if not esperado or destino != esperado:
            erros.append(
                f"ancora incorreta para {nome}: esperado '#{esperado}', encontrado '#{destino}'"
            )
    if nomes_secoes != sorted(nomes_secoes):
        erros.append("secoes de tabela fora de ordem alfabetica")

    return tabelas, ordem_colunas, descricoes, indice, erros


def resolver_padrao_pk(padrao, tabela):
    return padrao.replace("{tabela}", tabela) if padrao else None


def checar_ordem_colunas(ordem_colunas, padrao_pk=None):
    problemas = 0
    for tabela, colunas in ordem_colunas.items():
        pk = resolver_padrao_pk(padrao_pk, tabela)
        if pk and pk in colunas:
            if colunas[0] != pk:
                print(f"  ORDEM: {tabela} tem '{pk}' mas nao e a primeira coluna.")
                problemas += 1
                continue
            resto = colunas[1:]
        else:
            resto = colunas
        if resto != sorted(resto):
            print(f"  ORDEM: {tabela} tem colunas fora de ordem alfabetica.")
            problemas += 1
    return problemas


def detalhe_fisico_valido(detalhe):
    """Exige uma afirmacao fisica completa; semantica continua sob revisao manual."""
    if RE_RENOMEACAO.fullmatch(detalhe):
        return True
    if not detalhe.strip() or not detalhe.endswith("."):
        return False
    return bool(re.search(
        r"`|→|\bpara\b|\b(?:adicionad|exclu[ií]d|removid|recriad|finalizad|"
        r"renomead|referenciad|compost|formad|sobre|somente|existente)\w*\b",
        detalhe,
        re.IGNORECASE,
    ))


def validar_ordem_changelog(versoes, ordem_fornecida, erros):
    if ordem_fornecida:
        posicoes = {versao: i for i, versao in enumerate(ordem_fornecida)}
        ausentes = [versao for versao in versoes if versao not in posicoes]
        if ausentes:
            erros.append("versoes ausentes de --ordem-versoes: " + ", ".join(ausentes))
            return
        ordem = [posicoes[versao] for versao in versoes]
        if ordem != sorted(ordem):
            erros.append("versoes fora da ordem fornecida")
        return

    # Versoes numericas com qualquer quantidade de componentes possuem ordem
    # inequivoca sem impor SemVer aos demais formatos.
    if versoes and all(re.fullmatch(r"\d+(?:[._-]\d+)*", versao) for versao in versoes):
        chaves = [tuple(int(parte) for parte in re.split(r"[._-]", versao)) for versao in versoes]
        if chaves != sorted(chaves, reverse=True):
            erros.append("versoes fora de ordem decrescente")


def parse_changelog(caminho, padrao_versao=None, ordem_versoes=None):
    """Valida a gramatica e retorna o estado mais recente de tabelas e colunas."""
    linhas = ler_texto(caminho).splitlines()
    erros = []
    if not linhas or not RE_TITULO_CHANGELOG.fullmatch(linhas[0]):
        erros.append("titulo do changelog ausente ou invalido")
    if sum(1 for linha in linhas if linha.startswith("# ")) != 1:
        erros.append("o changelog deve conter exatamente um titulo H1")

    versoes = []
    categorias_vistas = set()
    tabelas_vistas = set()
    topicos_vistos = set()
    objetos_vistos = set()
    categorias_com_itens = Counter()
    tabelas_com_topicos = Counter()
    topicos_com_objetos = Counter()
    eventos_tabela = []
    eventos_coluna = []

    versao = categoria = tabela = topico = None
    ultima_categoria = -1

    for numero, linha in enumerate(linhas[1:], start=2):
        if not linha:
            continue

        match = RE_VERSAO_CHANGELOG.fullmatch(linha)
        if match:
            valor = match.group(1).strip()
            if not valor:
                erros.append(f"cabecalho de versao vazio na linha {numero}")
                versao = None
            else:
                if valor in versoes:
                    erros.append(f"versao duplicada: {valor}")
                versoes.append(valor)
                if padrao_versao and not padrao_versao.fullmatch(valor):
                    erros.append(f"versao '{valor}' nao corresponde a --padrao-versao")
                versao = valor
            categoria = tabela = topico = None
            ultima_categoria = -1
            continue
        if linha.startswith("##") and not linha.startswith("###"):
            erros.append(f"cabecalho de versao invalido na linha {numero}")
            versao = categoria = tabela = topico = None
            continue

        match = RE_CATEGORIA_CHANGELOG.fullmatch(linha)
        if match:
            nome = match.group(1)
            if versao is None:
                erros.append(f"categoria fora de uma versao na linha {numero}")
                categoria = tabela = topico = None
                continue
            if nome not in CATEGORIAS:
                erros.append(f"categoria nao permitida: {nome}")
                categoria = None
            else:
                chave = (versao, nome)
                if chave in categorias_vistas:
                    erros.append(f"categoria duplicada em {versao}: {nome}")
                categorias_vistas.add(chave)
                posicao = CATEGORIAS.index(nome)
                if posicao <= ultima_categoria:
                    erros.append(f"categorias fora de ordem em {versao}")
                ultima_categoria = posicao
                categoria = nome
            tabela = topico = None
            continue
        if linha.startswith("###"):
            erros.append(f"categoria invalida na linha {numero}")
            categoria = tabela = topico = None
            continue

        match = RE_TABELA_CHANGELOG.fullmatch(linha)
        if match:
            nome = normalizar_identificador(match.group(1))
            nome_antigo = (
                normalizar_identificador(match.group(2)) if match.group(2) else None
            )
            if not versao or not categoria:
                erros.append(f"bullet de tabela fora de categoria na linha {numero}")
                tabela = topico = None
                continue
            if not nome:
                erros.append(f"identificador de tabela vazio na linha {numero}")
            chave = (versao, categoria, nome)
            if chave in tabelas_vistas:
                erros.append(f"tabela duplicada em {versao}/{categoria}: {nome}")
            tabelas_vistas.add(chave)
            categorias_com_itens[(versao, categoria)] += 1
            nome_antigo_match = RE_RENOMEACAO_TABELA.fullmatch(nome_antigo or "")
            nome_antigo = nome_antigo_match.group(1) if nome_antigo_match else None
            eventos_tabela.append((versao, categoria, nome, nome_antigo, chave))
            tabela = nome
            topico = None
            continue
        if linha.startswith("- "):
            erros.append(f"bullet de tabela malformado na linha {numero}")
            tabela = topico = None
            continue

        match = RE_TOPICO_CHANGELOG.fullmatch(linha)
        if match:
            nome = match.group(1)
            if categoria not in ("Alterado", "Excluído") or not tabela:
                erros.append(f"topico fora de tabela alterada/excluida na linha {numero}")
                topico = None
                continue
            chave = (versao, categoria, tabela, nome)
            if chave in topicos_vistos:
                erros.append(f"topico duplicado em {tabela}: {nome}")
            topicos_vistos.add(chave)
            tabelas_com_topicos[(versao, categoria, tabela)] += 1
            topico = nome
            continue
        if linha.startswith("  - "):
            erros.append(f"topico malformado na linha {numero}")
            topico = None
            continue

        match = RE_OBJETO_CHANGELOG.fullmatch(linha)
        if match:
            tipo = match.group(1)
            nome = normalizar_identificador(match.group(2))
            detalhe = match.group(3) or match.group(4)
            if not topico or not tabela:
                erros.append(f"bullet de objeto fora de topico na linha {numero}")
                continue
            femininos = topico != "Índices"
            permitidos = {
                "Alterado": ("Nova", "Alterada") if femininos else ("Novo", "Alterado"),
                "Excluído": ("Excluída",) if femininos else ("Excluído",),
            }.get(categoria, ())
            if tipo not in permitidos:
                erros.append(f"tipo '{tipo}' invalido em {categoria}/{topico}")
            if not nome:
                erros.append(f"identificador de objeto vazio na linha {numero}")
            chave = (versao, categoria, tabela, topico, nome)
            if chave in objetos_vistos:
                erros.append(f"objeto duplicado em {tabela}/{topico}: {nome}")
            objetos_vistos.add(chave)
            topicos_com_objetos[(versao, categoria, tabela, topico)] += 1
            if tipo in ("Alterada", "Alterado"):
                if not detalhe:
                    erros.append(f"alteracao sem detalhe: {tabela}.{nome}")
                elif not detalhe_fisico_valido(detalhe):
                    erros.append(f"gramatica de alteracao invalida: {tabela}.{nome}")
            elif detalhe and not detalhe_fisico_valido(detalhe):
                erros.append(f"gramatica de detalhe invalida: {tabela}.{nome}")
            if topico == "Colunas":
                eventos_coluna.append((versao, categoria, tabela, tipo, nome, detalhe))
            continue
        if linha.startswith("    - "):
            erros.append(f"bullet de objeto malformado na linha {numero}")
            continue

        erros.append(f"conteudo inesperado na linha {numero}")

    if not versoes:
        erros.append("nenhum cabecalho de versao encontrado")
    for item in categorias_vistas:
        if not categorias_com_itens[item]:
            erros.append(f"categoria vazia em {item[0]}: {item[1]}")
    for versao_item in versoes:
        if not any(chave[0] == versao_item for chave in categorias_vistas):
            erros.append(f"versao sem categoria: {versao_item}")
    for versao_item, categoria_item, tabela_item in tabelas_vistas:
        if categoria_item == "Alterado" and not tabelas_com_topicos[
            (versao_item, categoria_item, tabela_item)
        ]:
            erros.append(f"tabela alterada sem topico: {tabela_item}")
    for chave in topicos_vistos:
        if not topicos_com_objetos[chave]:
            erros.append(f"topico vazio em {chave[2]}: {chave[3]}")

    validar_ordem_changelog(versoes, ordem_versoes, erros)

    tabelas_com_subitem = {
        (versao_item, categoria_item, tabela_item)
        for versao_item, categoria_item, tabela_item, _ in topicos_vistos
    }
    estado_tabela = {}
    for _, categoria_item, nome, nome_antigo, chave in eventos_tabela:
        if categoria_item == "Adicionado":
            estado_tabela.setdefault(nome, "adicionada")
            if nome_antigo:
                estado_tabela.setdefault(nome_antigo, "renomeada")
        elif categoria_item == "Excluído" and chave not in tabelas_com_subitem:
            estado_tabela.setdefault(nome, "excluida")

    estado_coluna = {}
    for _, _, nome_tabela, tipo, nome, detalhe in eventos_coluna:
        renomeacao = RE_RENOMEACAO.fullmatch(detalhe or "")
        if renomeacao:
            nome_antigo = normalizar_identificador(renomeacao.group(1))
            estado_coluna.setdefault((nome_tabela, nome_antigo), "renomeada")
            estado_coluna.setdefault((nome_tabela, nome), "renomeada_nova")
        elif tipo == "Nova":
            estado_coluna.setdefault((nome_tabela, nome), "adicionada")
        elif tipo == "Alterada":
            estado_coluna.setdefault((nome_tabela, nome), "alterada")
        elif tipo == "Excluída":
            estado_coluna.setdefault((nome_tabela, nome), "excluida")

    return estado_tabela, estado_coluna, versoes, erros


def cmd_formato(args):
    nome = Path(args.dicionario).name
    if nome == "dicionario_tabelas.md":
        _, _, erros = parse_dicionario_tabelas(args.dicionario, args.padrao_versao)
        ordem = None
        rotulo = "dicionario_tabelas.md"
    elif nome == "dicionario_colunas.md":
        _, ordem, _, _, erros = parse_dicionario_colunas(
            args.dicionario, args.padrao_versao
        )
        rotulo = "dicionario_colunas.md"
    else:
        print(
            "ERRO: formato aceita somente dicionario_tabelas.md ou dicionario_colunas.md.",
            file=sys.stderr,
        )
        raise EntradaInvalida

    problemas = len(erros)
    if erros:
        print(f"Problemas de formato ({len(erros)}):")
        for erro in erros:
            print(f"  - {erro}")
    if ordem is not None and args.checar_ordem:
        if not args.padrao_pk:
            print(
                "AVISO: --padrao-pk nao informado. A posicao da coluna identificadora "
                "nao foi checada; apenas a ordem alfabetica.",
                file=sys.stderr,
            )
        problemas += checar_ordem_colunas(ordem, args.padrao_pk)
    if problemas == 0:
        print(f"OK: formato de {rotulo} integro.")
        return 0
    return 1


def cmd_tabelas_colunas(args):
    if Path(args.tabelas).name != "dicionario_tabelas.md" or Path(args.colunas).name != "dicionario_colunas.md":
        print(
            "ERRO: tabelas-colunas aceita somente dicionario_tabelas.md e "
            "dicionario_colunas.md.",
            file=sys.stderr,
        )
        raise EntradaInvalida
    desc_tabelas, _, erros_tabelas = parse_dicionario_tabelas(args.tabelas)
    tabelas_colunas, _, desc_colunas, _, erros_colunas = parse_dicionario_colunas(args.colunas)
    if erros_tabelas or erros_colunas:
        for rotulo, erros in (
            ("dicionario_tabelas.md", erros_tabelas),
            ("dicionario_colunas.md", erros_colunas),
        ):
            for erro in erros:
                print(f"ERRO de formato em {rotulo}: {erro}", file=sys.stderr)
        return 2

    so_em_tabelas = sorted(set(desc_tabelas) - set(tabelas_colunas))
    so_em_colunas = sorted(set(tabelas_colunas) - set(desc_tabelas))
    divergentes = sorted(
        tabela
        for tabela in set(desc_tabelas) & set(tabelas_colunas)
        if desc_tabelas[tabela].strip() != desc_colunas[tabela].strip()
    )
    titulo_tabelas = RE_TITULO_DICIONARIO.fullmatch(ler_texto(args.tabelas).splitlines()[0])
    titulo_colunas = RE_TITULO_DICIONARIO.fullmatch(ler_texto(args.colunas).splitlines()[0])
    identidade_divergente = titulo_tabelas.groups() != titulo_colunas.groups()
    problemas = (
        len(so_em_tabelas)
        + len(so_em_colunas)
        + len(divergentes)
        + int(identidade_divergente)
    )

    blocos = (
        ("Tabelas sem secao em dicionario_colunas.md", so_em_tabelas),
        ("Secoes sem linha em dicionario_tabelas.md", so_em_colunas),
        ("Descricoes de tabela divergentes entre os dicionarios", divergentes),
    )
    for titulo, itens in blocos:
        if itens:
            print(f"{titulo}:")
            for item in itens:
                print(f"  - {item}")
    if identidade_divergente:
        print("Titulo ou versao diverge entre os dicionarios.")
    if problemas == 0:
        print("OK: dicionario_tabelas.md e dicionario_colunas.md consistentes.")
        return 0
    return 1


def localizar_changelog(entrada):
    caminho = Path(entrada)
    if caminho.is_file():
        if caminho.name != "CHANGELOG.md":
            print(f"ERRO: arquivo isolado deve se chamar CHANGELOG.md: {caminho}", file=sys.stderr)
            raise EntradaInvalida
        return caminho, caminho.parent / "dicionario_colunas.md"
    return caminho / "CHANGELOG.md", caminho / "dicionario_colunas.md"


def cmd_changelog(args):
    problemas = 0
    entrada_invalida = False
    for entrada in args.alvos:
        chg, dic = localizar_changelog(entrada)
        if not chg.exists():
            print(f"ERRO: CHANGELOG.md ausente em {entrada}.", file=sys.stderr)
            raise EntradaInvalida

        estado_tabela, estado_coluna, _, erros = parse_changelog(
            chg, args.padrao_versao, args.ordem_versoes
        )
        if erros:
            problemas += len(erros)
            print(f"Problemas de formato em {chg} ({len(erros)}):")
            for erro in erros:
                print(f"  - {erro}")
            continue

        if not dic.exists():
            continue
        tabelas, _, _, _, erros_dic = parse_dicionario_colunas(dic)
        if erros_dic:
            entrada_invalida = True
            for erro in erros_dic:
                print(f"ERRO de formato em {dic}: {erro}", file=sys.stderr)
            continue

        excluidas_presentes = sorted(
            tabela for tabela, estado in estado_tabela.items()
            if estado == "excluida" and tabela in tabelas
        )
        renomeadas_presentes = sorted(
            tabela for tabela, estado in estado_tabela.items()
            if estado == "renomeada" and tabela in tabelas
        )
        adicionadas_ausentes = sorted(
            tabela for tabela, estado in estado_tabela.items()
            if estado == "adicionada" and tabela not in tabelas
        )
        colunas_ausentes = []
        colunas_excedentes = []
        for (tabela, coluna), estado in sorted(estado_coluna.items()):
            if estado_tabela.get(tabela) in ("excluida", "renomeada") or tabela not in tabelas:
                continue
            if estado in ("adicionada", "alterada", "renomeada_nova") and coluna not in tabelas[tabela]:
                colunas_ausentes.append(f"{tabela}.{coluna}")
            elif estado in ("excluida", "renomeada") and coluna in tabelas[tabela]:
                colunas_excedentes.append(f"{tabela}.{coluna}")

        blocos = (
            ("tabelas marcadas como excluidas ainda presentes no dicionario", excluidas_presentes),
            ("tabelas renomeadas ainda presentes no dicionario", renomeadas_presentes),
            ("tabelas marcadas como adicionadas ausentes do dicionario", adicionadas_ausentes),
            ("colunas novas, alteradas ou renomeadas ausentes do dicionario", colunas_ausentes),
            ("colunas excluidas ou renomeadas ainda presentes no dicionario", colunas_excedentes),
        )
        for titulo, itens in blocos:
            if not itens:
                continue
            problemas += len(itens)
            print(f"{chg.parent}: {titulo}:")
            for item in itens:
                print(f"  - {item}")

    if entrada_invalida:
        return 2
    if problemas == 0:
        print("OK: CHANGELOG.md integro e cruzamento disponivel coerente.")
        return 0
    return 1


def normalizar_termo(texto):
    """Reduz um nome de termo a forma comparavel: minusculas e sem acento."""
    tabela = str.maketrans("aaaaaeeeeiiiiooooouuuuc", "aaaaaeeeeiiiiooooouuuuc")
    baixo = texto.strip().lower().translate(tabela)
    for de, para in (
        ("\u00e1", "a"), ("\u00e0", "a"), ("\u00e2", "a"), ("\u00e3", "a"), ("\u00e4", "a"),
        ("\u00e9", "e"), ("\u00e8", "e"), ("\u00ea", "e"), ("\u00eb", "e"),
        ("\u00ed", "i"), ("\u00ec", "i"), ("\u00ee", "i"), ("\u00ef", "i"),
        ("\u00f3", "o"), ("\u00f2", "o"), ("\u00f4", "o"), ("\u00f5", "o"), ("\u00f6", "o"),
        ("\u00fa", "u"), ("\u00f9", "u"), ("\u00fb", "u"), ("\u00fc", "u"),
        ("\u00e7", "c"),
    ):
        baixo = baixo.replace(de, para)
    baixo = " ".join(baixo.split())
    # O sufixo que torna a frase publicada gramatical nao integra o nome do termo.
    for sufixo in (
        "nao confirmados", "nao confirmadas", "nao confirmado", "nao confirmada",
        "nao determinados", "nao determinadas", "nao determinado", "nao determinada",
    ):
        if baixo.endswith(" " + sufixo):
            baixo = baixo[: -len(sufixo) - 1].strip()
            break
    return baixo


def casar_termo(bruto, vocabulario):
    """Reduz o texto capturado ao nome de termo do vocabulario, pelo prefixo mais longo.

    Aceita tanto a forma canonica, `TODO: <termo> - <motivo>`, quanto a forma livre
    herdada, em que o marcador emenda na oracao seguinte da propria formula.
    """
    normalizado = normalizar_termo(bruto)
    candidatos = [t for t in vocabulario if normalizado.startswith(normalizar_termo(t))]
    if not candidatos:
        return normalizado, None
    melhor = max(candidatos, key=lambda t: len(normalizar_termo(t)))
    return normalizar_termo(melhor), melhor


def extrair_lacunas(descricao, vocabulario):
    """Retorna [(termo_normalizado, termo_exibido, motivo, reconhecido)] dos marcadores."""
    achados = []
    for bruto, motivo in RE_MARCADOR_LACUNA.findall(descricao or ""):
        normalizado, canonico = casar_termo(bruto, vocabulario)
        achados.append(
            (
                normalizado,
                canonico if canonico else bruto.strip(),
                (motivo or "").strip(),
                canonico is not None,
            )
        )
    return achados


def coletar_lacunas(caminho):
    """Percorre um dos dicionarios e devolve o inventario de marcadores."""
    nome = Path(caminho).name
    if nome == "dicionario_tabelas.md":
        descricoes, _, erros = parse_dicionario_tabelas(caminho)
        alvos = [(tabela, None, texto) for tabela, texto in descricoes.items()]
        vocabulario = TERMOS_TABELA
    elif nome == "dicionario_colunas.md":
        tabelas, _, descricoes, _, erros = parse_dicionario_colunas(caminho)
        alvos = [(tabela, None, texto) for tabela, texto in descricoes.items()]
        for tabela, colunas in tabelas.items():
            for coluna, texto in colunas.items():
                alvos.append((tabela, coluna, texto))
        vocabulario = TERMOS_COLUNA + TERMOS_TABELA
    else:
        print(
            "ERRO: lacunas aceita somente dicionario_tabelas.md e dicionario_colunas.md.",
            file=sys.stderr,
        )
        raise EntradaInvalida
    if erros:
        for erro in erros:
            print(f"ERRO de formato em {nome}: {erro}", file=sys.stderr)
        raise EntradaInvalida

    itens = []
    for tabela, coluna, texto in alvos:
        for _, termo, motivo, reconhecido in extrair_lacunas(texto, vocabulario):
            itens.append(
                {
                    "tabela": tabela,
                    "coluna": coluna,
                    "termo": termo,
                    "motivo": motivo,
                    "termo_reconhecido": reconhecido,
                    "motivo_ausente": not motivo,
                }
            )
    itens.sort(key=lambda i: (i["tabela"], i["coluna"] or "", i["termo"]))
    return itens


def cmd_lacunas(args):
    itens = coletar_lacunas(args.dicionario)
    rotulo = Path(args.dicionario).name

    objetos = {(i["tabela"], i["coluna"]) for i in itens}
    tabelas_afetadas = {i["tabela"] for i in itens}
    por_termo = Counter(i["termo"] for i in itens)
    por_tabela = Counter(i["tabela"] for i in itens)
    desconhecidos = [i for i in itens if not i["termo_reconhecido"]]
    sem_motivo = [i for i in itens if i["motivo_ausente"]]

    if args.json:
        print(
            json.dumps(
                {
                    "arquivo": rotulo,
                    "marcadores": len(itens),
                    "objetos_afetados": len(objetos),
                    "tabelas_afetadas": len(tabelas_afetadas),
                    "por_termo": dict(por_termo.most_common()),
                    "por_tabela": dict(por_tabela.most_common()),
                    "termos_fora_do_vocabulario": len(desconhecidos),
                    "marcadores_sem_motivo": len(sem_motivo),
                    "itens": itens,
                },
                ensure_ascii=False,
                indent=2,
                sort_keys=False,
            )
        )
        return 1 if itens else 0

    if not itens:
        print(f"OK: {rotulo} sem marcadores de lacuna.")
        return 0

    print(
        f"Lacunas em {rotulo}: {len(itens)} marcadores em {len(objetos)} objetos, "
        f"{len(tabelas_afetadas)} tabelas."
    )
    print("Por termo da formula:")
    for termo, quantidade in por_termo.most_common():
        print(f"  {quantidade:5d}  {termo}")
    print("Por tabela:")
    for tabela, quantidade in por_tabela.most_common():
        print(f"  {quantidade:5d}  {tabela}")
    if desconhecidos:
        print(f"AVISO: {len(desconhecidos)} marcadores fora do vocabulario de termos:", file=sys.stderr)
        for item in desconhecidos:
            alvo = f"{item['tabela']}.{item['coluna']}" if item["coluna"] else item["tabela"]
            print(f"  - {alvo}: '{item['termo']}'", file=sys.stderr)
    if sem_motivo:
        print(f"AVISO: {len(sem_motivo)} marcadores sem motivo depois do separador:", file=sys.stderr)
        for item in sem_motivo:
            alvo = f"{item['tabela']}.{item['coluna']}" if item["coluna"] else item["tabela"]
            print(f"  - {alvo}: '{item['termo']}'", file=sys.stderr)
    return 1


def cmd_diff(args):
    if any(Path(caminho).name != "dicionario_colunas.md" for caminho in (args.antigo, args.novo)):
        print(
            "ERRO: diff aceita somente arquivos dicionario_colunas.md no formato atual.",
            file=sys.stderr,
        )
        raise EntradaInvalida
    try:
        mesmo_arquivo = Path(args.antigo).samefile(args.novo)
    except OSError:
        mesmo_arquivo = False
    if mesmo_arquivo:
        print(
            "ERRO: diff exige arquivos distintos para os estados anterior e novo.",
            file=sys.stderr,
        )
        raise EntradaInvalida
    tab_ant, _, desc_ant, _, erros_ant = parse_dicionario_colunas(args.antigo)
    tab_nov, _, desc_nov, _, erros_nov = parse_dicionario_colunas(args.novo)
    if erros_ant or erros_nov:
        for rotulo, erros in (("antigo", erros_ant), ("novo", erros_nov)):
            for erro in erros:
                print(f"ERRO de formato em {rotulo}: {erro}", file=sys.stderr)
        return 2

    nomes_ant, nomes_nov = set(tab_ant), set(tab_nov)
    adicionadas = sorted(nomes_nov - nomes_ant)
    removidas = sorted(nomes_ant - nomes_nov)
    alteradas = []
    for tabela in sorted(nomes_ant & nomes_nov):
        anteriores, atuais = set(tab_ant[tabela]), set(tab_nov[tabela])
        adicionadas_colunas = sorted(atuais - anteriores)
        removidas_colunas = sorted(anteriores - atuais)
        descricoes = sorted(
            coluna for coluna in anteriores & atuais
            if tab_ant[tabela][coluna] != tab_nov[tabela][coluna]
        )
        descricao_tabela = desc_ant[tabela] != desc_nov[tabela]
        if adicionadas_colunas or removidas_colunas or descricoes or descricao_tabela:
            alteradas.append({
                "tabela": tabela,
                "colunas_adicionadas": adicionadas_colunas,
                "colunas_removidas": removidas_colunas,
                "detalhes_colunas_adicionadas": [
                    {"coluna": coluna, "descricao": tab_nov[tabela][coluna]}
                    for coluna in adicionadas_colunas
                ],
                "detalhes_colunas_removidas": [
                    {"coluna": coluna, "descricao": tab_ant[tabela][coluna]}
                    for coluna in removidas_colunas
                ],
                "descricao_tabela_alterada": descricao_tabela,
                "descricao_tabela_anterior": desc_ant[tabela] if descricao_tabela else None,
                "descricao_tabela_atual": desc_nov[tabela] if descricao_tabela else None,
                "descricoes_colunas_alteradas": descricoes,
                "alteracoes_descricao_colunas": [
                    {
                        "coluna": coluna,
                        "descricao_anterior": tab_ant[tabela][coluna],
                        "descricao_atual": tab_nov[tabela][coluna],
                    }
                    for coluna in descricoes
                ],
            })

    resultado = {
        "contagem": {
            "tabelas_antes": len(nomes_ant),
            "tabelas_depois": len(nomes_nov),
            "colunas_antes": sum(len(colunas) for colunas in tab_ant.values()),
            "colunas_depois": sum(len(colunas) for colunas in tab_nov.values()),
        },
        "tabelas_adicionadas": [
            {
                "tabela": tabela,
                "descricao": desc_nov[tabela],
                "colunas": [
                    {"coluna": coluna, "descricao": tab_nov[tabela][coluna]}
                    for coluna in sorted(tab_nov[tabela])
                ],
            }
            for tabela in adicionadas
        ],
        "tabelas_removidas": removidas,
        "detalhes_tabelas_removidas": [
            {
                "tabela": tabela,
                "descricao": desc_ant[tabela],
                "colunas": [
                    {"coluna": coluna, "descricao": tab_ant[tabela][coluna]}
                    for coluna in sorted(tab_ant[tabela])
                ],
            }
            for tabela in removidas
        ],
        "tabelas_alteradas": alteradas,
        "contagem_alteracoes": {
            "tabelas_adicionadas": len(adicionadas),
            "tabelas_removidas": len(removidas),
            "tabelas_alteradas": len(alteradas),
            "colunas_adicionadas": sum(len(item["colunas_adicionadas"]) for item in alteradas),
            "colunas_removidas": sum(len(item["colunas_removidas"]) for item in alteradas),
            "descricoes_colunas_alteradas": sum(
                len(item["descricoes_colunas_alteradas"]) for item in alteradas
            ),
            "descricoes_tabela_alteradas": sum(
                1 for item in alteradas if item["descricao_tabela_alterada"]
            ),
        },
    }

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        contagem = resultado["contagem"]
        print(f"Tabelas: {contagem['tabelas_antes']} -> {contagem['tabelas_depois']}")
        print(f"Colunas: {contagem['colunas_antes']} -> {contagem['colunas_depois']}")
        print(f"\nTabelas adicionadas ({len(adicionadas)}):")
        for tabela in resultado["tabelas_adicionadas"]:
            print(f"  - {tabela['tabela']}: {tabela['descricao']}")
        print(f"\nTabelas removidas ({len(removidas)}):")
        for tabela in removidas:
            print(f"  - {tabela}")
        print(f"\nTabelas alteradas ({len(alteradas)}):")
        for tabela in alteradas:
            print(
                f"  - {tabela['tabela']}: +{tabela['colunas_adicionadas']} "
                f"-{tabela['colunas_removidas']} "
                f"descricoes={tabela['descricoes_colunas_alteradas']} "
                f"descricao_tabela={tabela['descricao_tabela_alterada']}"
            )

    return 1 if adicionadas or removidas or alteradas else 0


def main():
    parser = argparse.ArgumentParser(description=f"{SKILL_NAME} v{VERSION}")
    sub = parser.add_subparsers(dest="modo", required=True)

    p_formato = sub.add_parser("formato", help="valida um dos dois dicionarios atuais")
    p_formato.add_argument("dicionario")
    p_formato.add_argument(
        "--checar-ordem", action="store_true",
        help="valida a ordem das colunas, alem da ordem estrutural sempre verificada",
    )
    p_formato.add_argument(
        "--padrao-pk", metavar="PADRAO", default=None,
        help="padrao da coluna identificadora, com `{tabela}` interpolado",
    )
    p_formato.add_argument(
        "--padrao-versao", type=compilar_regex, metavar="REGEX",
        help="regex opcional aplicada a versao nao vazia do titulo",
    )
    p_formato.set_defaults(func=cmd_formato)

    p_tc = sub.add_parser("tabelas-colunas", help="cruza os dois dicionarios atuais")
    p_tc.add_argument("--tabelas", required=True)
    p_tc.add_argument("--colunas", required=True)
    p_tc.set_defaults(func=cmd_tabelas_colunas)

    p_chg = sub.add_parser("changelog", help="valida CHANGELOG.md e cruza colunas se existirem")
    p_chg.add_argument("alvos", nargs="+", help="pastas ou arquivos CHANGELOG.md isolados")
    p_chg.add_argument(
        "--padrao-versao", type=compilar_regex, metavar="REGEX",
        help="regex opcional aplicada aos cabecalhos de versao",
    )
    p_chg.add_argument(
        "--ordem-versoes", type=parse_ordem_versoes, metavar="V1,V2,...",
        help="ordem opcional, da versao mais recente para a mais antiga",
    )
    p_chg.set_defaults(func=cmd_changelog)

    p_lac = sub.add_parser("lacunas", help="conta marcadores de lacuna em um dos dois dicionarios")
    p_lac.add_argument("dicionario")
    p_lac.add_argument("--json", action="store_true")
    p_lac.set_defaults(func=cmd_lacunas)

    p_diff = sub.add_parser("diff", help="compara duas estruturas atuais de dicionario_colunas")
    p_diff.add_argument("--antigo", required=True)
    p_diff.add_argument("--novo", required=True)
    p_diff.add_argument("--json", action="store_true")
    p_diff.set_defaults(func=cmd_diff)

    args = parser.parse_args()
    try:
        sys.exit(args.func(args))
    except EntradaInvalida:
        sys.exit(2)


if __name__ == "__main__":
    main()
