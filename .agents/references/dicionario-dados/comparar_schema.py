#!/usr/bin/env python3
"""
sei-dicionario-dados
Compara um dicionario de dados (.md) contra o schema real de um banco (via
`docker exec <container> mysql`), ou compara duas versoes de um dicionario
entre si para gerar a base de um changelog.

Modo `schema` (0=sem divergencia, 1=divergencia, 2=erro/versao incorreta):
    comparar_schema.py schema --dicionario docs/dicionario_dados/sei/dicionario.md \
        --db sei --container mysql --versao-alvo 5.0.0 \
        --arquivo-env caminho/do/ambiente.env [--checar-ordem]

Modo `diff` (0=sem diferenca, 1=diferenca encontrada, 2=entrada invalida):
    comparar_schema.py diff --antigo antigo.md --novo novo.md [--json]
"""

import argparse
from collections import Counter
import json
import os
import re
import subprocess
import sys

VERSION = "1.0.0"
SKILL_NAME = "sei-dicionario-dados"

RE_ROW = re.compile(r"^\|\s*([a-zA-Z0-9_]+)\s*\|\s*(.*?)\s*\|$")
RE_INDICE_ITEM = re.compile(r"^- \[([^\]]+)\]\(#", re.MULTILINE)


def parse_dicionario(path):
    """Retorna tabelas, ordem, descricoes, indice e erros de formato."""
    with open(path, encoding="utf-8") as f:
        content = f.read()

    sections = re.split(r"^## (.+)$", content, flags=re.MULTILINE)
    tabelas = {}
    ordem_colunas = {}
    descricoes = {}
    nomes_secoes = []
    erros = []
    for i in range(1, len(sections), 2):
        nome = sections[i].strip()
        if nome == "Índice de Tabelas":
            continue
        corpo = sections[i + 1]
        colunas = {}
        ordem = []
        frase = ""
        nomes_secoes.append(nome)
        if nome in tabelas:
            erros.append(f"secao duplicada: {nome}")
        for linha in corpo.splitlines():
            linha = linha.strip()
            if not linha:
                continue
            m = RE_ROW.match(linha)
            if m and m.group(1).lower() != "coluna":
                coluna = m.group(1)
                if coluna in colunas:
                    erros.append(f"coluna duplicada em {nome}: {coluna}")
                colunas[coluna] = m.group(2)
                ordem.append(coluna)
            elif not linha.startswith("|") and not frase:
                frase = linha
        tabelas[nome] = colunas
        ordem_colunas[nome] = ordem
        descricoes[nome] = frase
        if not frase:
            erros.append(f"descricao ausente: {nome}")
        if not colunas:
            erros.append(f"tabela sem colunas: {nome}")

    indice = RE_INDICE_ITEM.findall(content)
    for nome, quantidade in Counter(indice).items():
        if quantidade > 1:
            erros.append(f"entrada duplicada no indice: {nome}")
    if indice != nomes_secoes:
        erros.append("indice deve corresponder 1:1 e na mesma ordem as secoes de tabela")
    if nomes_secoes != sorted(nomes_secoes):
        erros.append("secoes de tabela fora de ordem alfabetica")

    return tabelas, ordem_colunas, descricoes, indice, erros


def ler_arquivo_env(path):
    """Le um arquivo KEY=VALUE sem executar seu conteudo."""
    valores = {}
    with open(path, encoding="utf-8") as f:
        for numero, linha in enumerate(f, 1):
            linha = linha.strip()
            if not linha or linha.startswith("#"):
                continue
            if linha.startswith("export "):
                linha = linha[7:].lstrip()
            if "=" not in linha:
                raise ValueError(f"linha invalida no arquivo de ambiente ({numero})")
            chave, valor = linha.split("=", 1)
            chave = chave.strip()
            valor = valor.strip()
            if len(valor) >= 2 and valor[0] == valor[-1] and valor[0] in "\"'":
                valor = valor[1:-1]
            valores[chave] = valor
    return valores


def obter_credenciais(db, arquivo_env=None):
    """Obtem usuario e senha sem recebe-los pela linha de comando."""
    valores = ler_arquivo_env(arquivo_env) if arquivo_env else {}
    prefixo = db.upper()
    chaves = [f"{prefixo}_DATABASE_USER", f"{prefixo}_DATABASE_PASSWORD"]
    for chave in chaves:
        if chave in os.environ:
            valores[chave] = os.environ[chave]

    ausentes = [chave for chave in chaves if not valores.get(chave)]
    if ausentes:
        raise ValueError(
            "credenciais ausentes: exporte " + ", ".join(ausentes) + " ou use --arquivo-env"
        )
    return valores[chaves[0]], valores[chaves[1]]


def consultar_schema(container, usuario, senha, db):
    """Retorna (versao, tabelas) via information_schema e infra_parametro."""
    if "\n" in senha or "\r" in senha:
        raise ValueError("senha contem quebra de linha")

    parametro_versao = "SEI_VERSAO" if db == "sei" else "SIP_VERSAO"
    sql = (
        f"SELECT '__VERSAO__', valor FROM infra_parametro WHERE nome='{parametro_versao}' "
        f"UNION ALL SELECT table_name, column_name FROM information_schema.columns "
        f"WHERE table_schema='{db}' ORDER BY 1, 2;"
    )
    cmd = [
        "docker", "exec", "-i", container, "sh", "-c",
        'IFS= read -r MYSQL_PWD; export MYSQL_PWD; exec mysql -u "$1" "$2" -N -e "$3"',
        "sh", usuario, db, sql,
    ]
    result = subprocess.run(cmd, input=f"{senha}\n", capture_output=True, text=True)
    if result.returncode != 0:
        raise RuntimeError(f"erro ao consultar o banco: {result.stderr.strip()}")

    tabelas = {}
    versao = None
    for linha in result.stdout.splitlines():
        if not linha.strip():
            continue
        partes = linha.split("\t")
        if len(partes) != 2:
            continue
        tabela, coluna = partes
        if tabela == "__VERSAO__":
            versao = coluna
            continue
        tabelas.setdefault(tabela, set()).add(coluna)
    return versao, tabelas


def excluido(nome, prefixos):
    return any(nome.startswith(p) for p in prefixos if p)


def cmd_schema(args):
    prefixos = [p.strip() for p in args.excluir_prefixo.split(",")] if args.excluir_prefixo else []

    dict_tabelas, dict_ordem, _, _, erros_formato = parse_dicionario(args.dicionario)
    try:
        usuario, senha = obter_credenciais(args.db, args.arquivo_env)
        versao_banco, db_tabelas_full = consultar_schema(args.container, usuario, senha, args.db)
    except (OSError, RuntimeError, ValueError) as e:
        print(f"ERRO: {e}", file=sys.stderr)
        return 2

    if not versao_banco:
        print(f"ERRO: parametro {args.db.upper()}_VERSAO ausente no banco", file=sys.stderr)
        return 2
    if versao_banco != args.versao_alvo:
        print(
            f"ERRO: versao do banco ({versao_banco}) difere da versao-alvo ({args.versao_alvo})",
            file=sys.stderr,
        )
        return 2

    db_tabelas = {t: c for t, c in db_tabelas_full.items() if not excluido(t, prefixos)}

    problemas = len(erros_formato)
    if erros_formato:
        print(f"Problemas de formato ({len(erros_formato)}):")
        for erro in erros_formato:
            print(f"  - {erro}")

    so_no_dicionario = sorted(set(dict_tabelas) - set(db_tabelas))
    so_no_banco = sorted(set(db_tabelas) - set(dict_tabelas))
    if so_no_dicionario:
        problemas += len(so_no_dicionario)
        print(f"Tabelas no dicionario, ausentes do banco ({len(so_no_dicionario)}):")
        for t in so_no_dicionario:
            print(f"  - {t}")
    if so_no_banco:
        problemas += len(so_no_banco)
        print(f"Tabelas no banco, ausentes do dicionario ({len(so_no_banco)}):")
        for t in so_no_banco:
            print(f"  - {t}")

    comuns = sorted(set(dict_tabelas) & set(db_tabelas))
    divergencias_coluna = []
    for t in comuns:
        dcols = set(dict_tabelas[t])
        bcols = db_tabelas[t]
        faltam = bcols - dcols
        sobram = dcols - bcols
        if faltam or sobram:
            divergencias_coluna.append((t, sorted(faltam), sorted(sobram)))

    if divergencias_coluna:
        problemas += len(divergencias_coluna)
        print(f"\nTabelas com colunas divergentes ({len(divergencias_coluna)}):")
        for t, faltam, sobram in divergencias_coluna:
            partes = []
            if faltam:
                partes.append(f"faltam no dicionario: {', '.join(faltam)}")
            if sobram:
                partes.append(f"sobram no dicionario (nao existem no banco): {', '.join(sobram)}")
            print(f"  - {t}: {'; '.join(partes)}")

    if args.checar_ordem:
        problemas += checar_ordem_colunas(dict_ordem)

    if problemas == 0:
        print("OK: dicionario bate com o schema do banco (dentro do escopo filtrado).")
        return 0
    return 1


def checar_ordem_colunas(dict_ordem):
    problemas = 0
    for tabela, colunas in dict_ordem.items():
        if tabela.startswith("seq_") or tabela.endswith("_idx"):
            continue
        pk = f"id_{tabela}"
        if pk in colunas:
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


def cmd_diff(args):
    old_tabelas, _, old_descs, _, old_erros = parse_dicionario(args.antigo)
    new_tabelas, _, new_descs, _, new_erros = parse_dicionario(args.novo)

    if old_erros or new_erros:
        for rotulo, erros in (("antigo", old_erros), ("novo", new_erros)):
            for erro in erros:
                print(f"ERRO de formato em {rotulo}: {erro}", file=sys.stderr)
        return 2

    old_nomes = set(old_tabelas)
    new_nomes = set(new_tabelas)

    tabelas_adicionadas = sorted(new_nomes - old_nomes)
    tabelas_removidas = sorted(old_nomes - new_nomes)

    tabelas_alteradas = []
    for t in sorted(old_nomes & new_nomes):
        oc = set(old_tabelas[t])
        nc = set(new_tabelas[t])
        add = sorted(nc - oc)
        rem = sorted(oc - nc)
        descricoes_colunas = sorted(
            coluna for coluna in oc & nc if old_tabelas[t][coluna] != new_tabelas[t][coluna]
        )
        descricao_tabela = old_descs.get(t, "") != new_descs.get(t, "")
        if add or rem or descricoes_colunas or descricao_tabela:
            tabelas_alteradas.append({
                "tabela": t,
                "colunas_adicionadas": add,
                "colunas_removidas": rem,
                "descricao_tabela_alterada": descricao_tabela,
                "descricoes_colunas_alteradas": descricoes_colunas,
            })

    resultado = {
        "contagem": {
            "tabelas_antes": len(old_nomes),
            "tabelas_depois": len(new_nomes),
            "colunas_antes": sum(len(v) for v in old_tabelas.values()),
            "colunas_depois": sum(len(v) for v in new_tabelas.values()),
        },
        "tabelas_adicionadas": [{"tabela": t, "descricao": new_descs.get(t, "")} for t in tabelas_adicionadas],
        "tabelas_removidas": tabelas_removidas,
        "tabelas_alteradas": tabelas_alteradas,
        "contagem_alteracoes": {
            "tabelas_adicionadas": len(tabelas_adicionadas),
            "tabelas_removidas": len(tabelas_removidas),
            "tabelas_alteradas": len(tabelas_alteradas),
            "colunas_adicionadas": sum(len(t["colunas_adicionadas"]) for t in tabelas_alteradas),
            "colunas_removidas": sum(len(t["colunas_removidas"]) for t in tabelas_alteradas),
            "descricoes_colunas_alteradas": sum(len(t["descricoes_colunas_alteradas"]) for t in tabelas_alteradas),
            "descricoes_tabela_alteradas": sum(1 for t in tabelas_alteradas if t["descricao_tabela_alterada"]),
        },
    }

    if args.json:
        print(json.dumps(resultado, ensure_ascii=False, indent=2))
    else:
        c = resultado["contagem"]
        print(f"Tabelas: {c['tabelas_antes']} -> {c['tabelas_depois']}")
        print(f"Colunas: {c['colunas_antes']} -> {c['colunas_depois']}")
        print(f"\nTabelas adicionadas ({len(tabelas_adicionadas)}):")
        for t in resultado["tabelas_adicionadas"]:
            print(f"  - {t['tabela']}: {t['descricao']}")
        print(f"\nTabelas removidas ({len(tabelas_removidas)}):")
        for t in tabelas_removidas:
            print(f"  - {t}")
        print(f"\nTabelas alteradas ({len(tabelas_alteradas)}):")
        for t in tabelas_alteradas:
            print(
                f"  - {t['tabela']}: +{t['colunas_adicionadas']} "
                f"-{t['colunas_removidas']} descricoes={t['descricoes_colunas_alteradas']} "
                f"descricao_tabela={t['descricao_tabela_alterada']}"
            )

    houve_diferenca = bool(tabelas_adicionadas or tabelas_removidas or tabelas_alteradas)
    return 1 if houve_diferenca else 0


def main():
    parser = argparse.ArgumentParser(description=f"{SKILL_NAME} v{VERSION}")
    sub = parser.add_subparsers(dest="modo", required=True)

    p_schema = sub.add_parser("schema", help="compara o dicionario contra o schema real do banco")
    p_schema.add_argument("--dicionario", required=True, help="caminho do dicionario.md")
    p_schema.add_argument("--db", required=True, choices=("sei", "sip"), help="schema/database")
    p_schema.add_argument("--container", default="mysql", help="nome do container Docker do MySQL (default: mysql)")
    p_schema.add_argument("--versao-alvo", required=True, help="versao exata esperada em infra_parametro")
    p_schema.add_argument("--arquivo-env", help="arquivo com as credenciais do ambiente Docker")
    p_schema.add_argument("--excluir-prefixo", default="md_,seq_md_", help="prefixos de tabela a ignorar, separados por virgula (default: md_,seq_md_ — tabelas de modulo)")
    p_schema.add_argument("--checar-ordem", action="store_true", help="tambem valida a regra de ordenacao de colunas")
    p_schema.set_defaults(func=cmd_schema)

    p_diff = sub.add_parser("diff", help="compara duas versoes de um dicionario (base para changelog)")
    p_diff.add_argument("--antigo", required=True)
    p_diff.add_argument("--novo", required=True)
    p_diff.add_argument("--json", action="store_true")
    p_diff.set_defaults(func=cmd_diff)

    args = parser.parse_args()
    sys.exit(args.func(args))


if __name__ == "__main__":
    main()
