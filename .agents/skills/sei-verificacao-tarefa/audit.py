#!/usr/bin/env python3
"""
sei-verificacao-tarefa
Skill de gate para validar IDs de tarefa de modulo SEI/SIP.
Valida: range >= 1000, prefixo MD_, max 50 chars, unicidade e, no cadastro por
TarefaDTO ou INSERT INTO tarefa, origem do id (seq_tarefa) e sinalizadores S/N.
Com --exit-code: 0=PASS, 1=WARN, 2=BLOCK
"""

import sys
import os
import re
import json
import argparse
import bisect
from datetime import datetime, timezone

VERSION = "1.0.0"
SKILL_NAME = "sei-verificacao-tarefa"


# ═══════════════════════════════════════════════════════════════
# REGEX PATTERNS
# ═══════════════════════════════════════════════════════════════

RE_ID_TAREFA = re.compile(r"['\"]id_tarefa['\"]\s*=>\s*([^,\]\)\r\n]+)", re.IGNORECASE)
RE_ID_TAREFA_MODULO = re.compile(r"['\"]id_tarefa_modulo['\"]\s*=>\s*([^,\]\)\r\n]+)", re.IGNORECASE)
RE_SET_ID_TAREFA = re.compile(r"setNumIdTarefa\s*\(\s*(\d+)\s*\)")
RE_SET_ID_TAREFA_MODULO = re.compile(r"setStrIdTarefaModulo\s*\(\s*(['\"])([^'\"]+)\1\s*\)")
RE_MAP_PAIR = re.compile(r"(?<![\w'\"])\b(\d+)\s*=>\s*(['\"])(MD_[A-Z0-9_]+)\2")
RE_DESCRICAO_VALOR = re.compile(r"['\"]DESCRICAO['\"]\s*=>\s*(['\"])(.*?)\1", re.DOTALL)
RE_DESCRICAO_CONSTRUTOR = re.compile(r"['\"]DESCRICAO['\"]\s*,\s*(['\"])(.*?)\1", re.DOTALL)
RE_NEW_TAREFA_DTO = re.compile(r"(\$\w+)\s*=\s*new\s+TarefaDTO\b(?:\s*\(\s*\))?")
RE_CADASTRAR_NEW_TAREFA_DTO = re.compile(r"->cadastrar\s*\(\s*new\s+TarefaDTO\b")
RE_ATRIBUICAO = re.compile(r"(?P<var>\$\w+)\s*=(?![=>])")
RE_LADO_DIREITO = re.compile(r"([^;]*);?")
RE_RETORNO_DE_CADASTRAR = re.compile(r"\s*\$\w+\s*->\s*cadastrar\s*\(\s*(\$\w+)\s*\)\s*")
RE_EVENTO_TAREFA_DTO = re.compile(
    r"(?P<var>\$\w+)->(?:(?P<limpa>unSetTodos)|unSet(?:Num|Str)(?P<remove>\w+)|set(?:Num|Str)(?P<define>\w+))\s*\("
    r"|->cadastrar\s*\(\s*(?P<cadastrado>\$\w+)\s*\)"
)
RE_INSERT_TAREFA = re.compile(r"insert\s+into\s+tarefa\s*\(", re.IGNORECASE)
RE_VALUES = re.compile(r"\)\s*values\s*\(", re.IGNORECASE)
RE_PROXIMA_TUPLA = re.compile(r"""(?:\s|["']\s*\.\s*["'])*,(?:\s|["']\s*\.\s*["'])*\(""")
RE_VIRGULA_SEGUINTE = re.compile(r"""(?:\s|["']\s*\.\s*["'])*,""")
RE_LITERAL_SEM_INTERPOLACAO = re.compile(r"'([^']*)'|\"([^\"$]*)\"")
RE_CHAMADA_SEQ_TAREFA = re.compile(
    r"(?:[\w$]+(?:\s*::\s*\w+\s*\(\s*\))?(?:\s*->\s*\w+\s*\(\s*\))*\s*->\s*)?"
    r"getValorSequencia\s*\(\s*['\"]seq_tarefa['\"]\s*\)",
    re.IGNORECASE,
)
# Forma do core: recria a sequence a partir do proximo id, nos quatro bancos.
RE_REALINHA_PELO_CORE = re.compile(
    r"criarSequencialNativa\s*\(\s*\\?['\"]seq_tarefa\b|atualizarSequencias\s*\(",
    re.IGNORECASE,
)
# SQL proprio: o auditor nao le o valor, que pode ser o ultimo id gravado e colidir.
RE_REALINHA_POR_SQL = re.compile(
    r"insert\s+into\s+seq_tarefa\b|create\s+sequence\s+seq_tarefa\b|alter\s+(?:table|sequence)\s+seq_tarefa\b"
    r"|checkident\s*\(\s*\\?['\"]?seq_tarefa\b|setval\s*\(\s*\\?['\"]seq_tarefa\b",
    re.IGNORECASE,
)

# Colunas S/N da tabela tarefa e o atributo correspondente em TarefaDTO.
SINALIZADORES = {
    "sin_historico_resumido": "SinHistoricoResumido",
    "sin_historico_completo": "SinHistoricoCompleto",
    "sin_lancar_andamento_fechado": "SinLancarAndamentoFechado",
    "sin_permite_processo_fechado": "SinPermiteProcessoFechado",
    "sin_fechar_andamentos_abertos": "SinFecharAndamentosAbertos",
}
COLUNAS_AUDITADAS = {"id_tarefa": "IdTarefa", "id_tarefa_modulo": "IdTarefaModulo", **SINALIZADORES}


# ═══════════════════════════════════════════════════════════════
# VALIDATORS
# ═══════════════════════════════════════════════════════════════

def mask_php_comments(content):
    chars = list(content)
    index = 0
    quote = None
    while index < len(chars):
        char = chars[index]
        if quote:
            if char == "\\":
                index += 2
                continue
            if char == quote:
                quote = None
            index += 1
            continue
        if char in "'\"`":
            quote = char
            index += 1
            continue
        if content.startswith("//", index) or char == "#":
            end = content.find("\n", index)
            end = len(chars) if end < 0 else end
            chars[index:end] = " " * (end - index)
            index = end
            continue
        if content.startswith("/*", index):
            end = content.find("*/", index + 2)
            end = len(chars) if end < 0 else end + 2
            for position in range(index, end):
                if chars[position] not in "\r\n":
                    chars[position] = " "
            index = end
            continue
        index += 1
    return "".join(chars)


def record_end(content, start):
    stack = []
    pairs = {")": "(", "]": "[", "}": "{"}
    quote = None
    for index in range(start, len(content)):
        char = content[index]
        if quote:
            if char == "\\":
                continue
            if char == quote:
                quote = None
            continue
        if char in "'\"`":
            quote = char
        elif char in "([{":
            stack.append(char)
        elif char in pairs:
            if not stack:
                return index
            if stack[-1] == pairs[char]:
                stack.pop()
    return len(content)


def parse_tarefas(content):
    tarefas = []

    def line(position):
        return content[:position].count("\n") + 1

    def parse_value(raw):
        value = raw.strip()
        if re.fullmatch(r"\d+", value):
            return int(value)
        if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
            return value[1:-1]
        return value.strip("'\"")

    def has_description(segment):
        match = RE_DESCRICAO_VALOR.search(segment) or RE_DESCRICAO_CONSTRUTOR.search(segment)
        return bool(match and match.group(2).strip())

    consumed_module_positions = set()

    for match in RE_MAP_PAIR.finditer(content):
        tarefas.append({"id": int(match.group(1)), "nome": match.group(3), "descr": False, "linha": line(match.start()), "linha_nome": line(match.start())})

    id_matches = list(RE_ID_TAREFA.finditer(content))
    for match in id_matches:
        end = record_end(content, match.end())
        segment = content[match.end():end]
        module_match = RE_ID_TAREFA_MODULO.search(segment)
        if module_match:
            consumed_module_positions.add(match.end() + module_match.start())
        tarefas.append({
            "id": parse_value(match.group(1)),
            "nome": parse_value(module_match.group(1)) if module_match else None,
            "descr": has_description(segment),
            "linha": line(match.start()),
            "linha_nome": line(match.end() + module_match.start()) if module_match else None,
        })

    for match in RE_ID_TAREFA_MODULO.finditer(content):
        if match.start() not in consumed_module_positions:
            tarefas.append({"id": None, "nome": parse_value(match.group(1)), "descr": False, "linha": None, "linha_nome": line(match.start())})

    consumed_setter_positions = set()
    setter_matches = list(RE_SET_ID_TAREFA.finditer(content))
    for index, match in enumerate(setter_matches):
        end = setter_matches[index + 1].start() if index + 1 < len(setter_matches) else len(content)
        segment = content[match.end():end]
        module_match = RE_SET_ID_TAREFA_MODULO.search(segment)
        if module_match:
            consumed_setter_positions.add(match.end() + module_match.start())
        tarefas.append({
            "id": int(match.group(1)),
            "nome": module_match.group(2) if module_match else None,
            "descr": has_description(segment),
            "linha": line(match.start()),
            "linha_nome": line(match.end() + module_match.start()) if module_match else None,
        })

    for match in RE_SET_ID_TAREFA_MODULO.finditer(content):
        if match.start() not in consumed_setter_positions:
            tarefas.append({"id": None, "nome": match.group(2), "descr": False, "linha": None, "linha_nome": line(match.start())})

    return tarefas


def classificar_valor(raw):
    """Classifica valor PHP ou SQL em int, str, null, seq (chamada getValorSequencia de seq_tarefa) ou expr."""
    texto = raw.strip().replace("\\'", "'").replace('\\"', '"')
    texto = re.sub(r"^(['\"])\s*\.\s*", "", texto)
    texto = re.sub(r"\s*\.\s*(['\"])$", "", texto).strip()
    if RE_CHAMADA_SEQ_TAREFA.fullmatch(texto):
        return {"tipo": "seq", "valor": None}
    if texto.lower() == "null":
        return {"tipo": "null", "valor": None}
    # Literal inteiro; no fim do INSERT, aceita a interpolacao PHP de valores acrescentados, como $strValores.
    literal = re.fullmatch(r"(['\"])((?:(?!\1).|\1\1)*)\1(?:\$\w+)?", texto, re.DOTALL)
    valor = literal.group(2) if literal else texto
    if re.fullmatch(r"-?\d+", valor):
        return {"tipo": "int", "valor": int(valor)}
    return {"tipo": "str" if literal else "expr", "valor": valor}


def decodificar_php(content, inicio, delimitador_php):
    """Gera (char, posicao) a partir de inicio, com \\\\ e a aspa escapada da string PHP ja decodificadas."""
    posicao = inicio
    while posicao < len(content):
        par = content[posicao:posicao + 2]
        if par == "\\\\" or (delimitador_php and par == "\\" + delimitador_php):
            yield par[1], posicao + 1
            posicao += 2
            continue
        yield content[posicao], posicao
        posicao += 1


def dividir_valores(content, inicio, delimitador_php):
    """Divide uma tupla de VALUES em valores de topo; devolve (valores, fim) ou None se nao fechar.

    Le o SQL ja decodificado da string PHP; dentro de texto SQL, a barra invertida escapa o caractere seguinte.
    """
    valores, atual, profundidade, aspas, pular = [], [], 0, None, False
    for char, posicao in decodificar_php(content, inicio, delimitador_php):
        if pular:
            pular = False
        elif aspas:
            if char == "\\":
                pular = True
            elif char == aspas:
                aspas = None
        elif char in "'\"":
            aspas = char
        elif char == "(":
            profundidade += 1
        elif char == ")":
            if profundidade == 0:
                valores.append("".join(atual))
                return valores, posicao
            profundidade -= 1
        elif profundidade == 0 and char == ",":
            valores.append("".join(atual))
            atual = []
            continue
        atual.append(char)
    return None


def ler_tuplas(content, inicio, delimitador_php):
    """Le todas as tuplas de VALUES (...), (...); devolve None se alguma nao fechar ou a continuacao nao for lida."""
    tuplas = []
    while True:
        tupla = dividir_valores(content, inicio, delimitador_php)
        if tupla is None:
            return None
        valores, fim = tupla
        tuplas.append(valores)
        proxima = RE_PROXIMA_TUPLA.match(content, fim + 1)
        if proxima:
            aspas_concatenadas = re.findall(r"[\"']", proxima.group(0))
            delimitador_php = aspas_concatenadas[-1] if aspas_concatenadas else delimitador_php
            inicio = proxima.end()
            continue
        return None if RE_VIRGULA_SEGUINTE.match(content, fim + 1) else tuplas


def resolver_colunas(content, colunas, posicao):
    """Lista de colunas em variavel: ultima atribuicao antes do INSERT e acrescimos .= seguintes, todos literais."""
    colunas = re.sub(r"^(['\"])\s*\.\s*(\$\w+)\s*\.\s*\1$", r"\2", colunas)
    colunas = re.sub(r"^\{(\$\w+)\}$", r"\1", colunas)
    if not re.fullmatch(r"\$\w+", colunas):
        return None if "$" in colunas else colunas
    operacoes = list(re.finditer(re.escape(colunas) + r"\s*(\.?)=(?![=>])\s*([^;]*);", content[:posicao]))
    inicio = max((indice for indice, operacao in enumerate(operacoes) if not operacao.group(1)), default=None)
    if inicio is None:
        return None
    resolvida = ""
    for operacao in operacoes[inicio:]:
        literal = RE_LITERAL_SEM_INTERPOLACAO.fullmatch(operacao.group(2).strip())
        if not literal:
            return None
        texto = literal.group(1) if literal.group(1) is not None else literal.group(2)
        resolvida = resolvida + texto if operacao.group(1) else texto
    return resolvida


def montar_cadastro(origem, atributos, posicao, line):
    """Registro de cadastro a partir dos atributos de TarefaDTO: nome do atributo -> (valor, posicao)."""
    ausente = ({"tipo": "ausente", "valor": None}, posicao)
    id_valor, posicao_id = atributos.get("IdTarefa", ausente)
    nome_valor, posicao_nome = atributos.get("IdTarefaModulo", ausente)
    return {
        "origem": origem,
        "id": id_valor["valor"] if id_valor["tipo"] == "int" else None,
        "id_tipo": id_valor["tipo"],
        "id_expr": id_valor["valor"] if id_valor["tipo"] in ("expr", "str") else None,
        "nome": nome_valor["valor"] if nome_valor["tipo"] == "str" else None,
        "nome_expr": nome_valor["valor"] if nome_valor["tipo"] == "expr" else None,
        "sinalizadores": {coluna: atributos[atributo][0] for coluna, atributo in SINALIZADORES.items() if atributo in atributos},
        "linha": line(posicao_id),
        "linha_nome": line(posicao_nome),
        "posicao_id": posicao_id,
    }


def agrupar_por_variavel(padrao, content, *grupos):
    """Uma passada do padrao no arquivo, agrupada pela variavel: {var: ([inicio, ...], [ocorrencia, ...])}."""
    por_variavel = {}
    for ocorrencia in padrao.finditer(content):
        var = next(ocorrencia.group(grupo) for grupo in grupos if ocorrencia.group(grupo))
        inicios, ocorrencias = por_variavel.setdefault(var, ([], []))
        inicios.append(ocorrencia.start())
        ocorrencias.append(ocorrencia)
    return por_variavel


def a_partir_de(por_variavel, var, posicao):
    """Ocorrencias da variavel que comecam em posicao ou depois, em ordem, sem varrer as anteriores."""
    inicios, ocorrencias = por_variavel.get(var, ([], []))
    for indice in range(bisect.bisect_left(inicios, posicao), len(ocorrencias)):
        yield ocorrencias[indice]


def parse_cadastros(content):
    """Extrai cadastros de tarefa: TarefaDTO passado a cadastrar() e cada tupla de INSERT INTO tarefa."""
    registros = []

    def line(position):
        return content[:position].count("\n") + 1

    # Atribuicoes e eventos lidos uma vez e agrupados por variavel: cada TarefaDTO consulta so os seus.
    atribuicoes = agrupar_por_variavel(RE_ATRIBUICAO, content, "var")
    eventos = agrupar_por_variavel(RE_EVENTO_TAREFA_DTO, content, "var", "cadastrado")
    for novo in RE_NEW_TAREFA_DTO.finditer(content):
        var = novo.group(1)
        # A reatribuicao fecha o segmento depois do lado direito; $dto = $rn->cadastrar($dto) mantem o mesmo DTO.
        fim_segmento = len(content)
        for atribuicao in a_partir_de(atribuicoes, var, novo.end()):
            reatribuicao = RE_LADO_DIREITO.match(content, atribuicao.end())
            retorno = RE_RETORNO_DE_CADASTRAR.fullmatch(reatribuicao.group(1))
            if not (retorno and retorno.group(1) == var):
                fim_segmento = reatribuicao.end()
                break
        estado = {}
        for evento in a_partir_de(eventos, var, novo.end()):
            if evento.end() > fim_segmento:
                break
            if evento.group("limpa"):
                estado = {}
            elif evento.group("remove"):
                estado.pop(evento.group("remove"), None)
            elif evento.group("define"):
                fim = record_end(content, evento.end())
                estado[evento.group("define")] = (classificar_valor(content[evento.end():fim]), evento.start())
            else:
                registros.append(montar_cadastro("TarefaDTO", estado, evento.start(), line))

    for inline in RE_CADASTRAR_NEW_TAREFA_DTO.finditer(content):
        registros.append({"origem": "TarefaDTO", "erro_parser": "TarefaDTO criado dentro de cadastrar()", "linha": line(inline.start())})

    for insert in RE_INSERT_TAREFA.finditer(content):
        delimitador_php = content[:insert.start()].rstrip()[-1:]
        delimitador_php = delimitador_php if delimitador_php in ("'", '"') else ""
        fim_colunas = record_end(content, insert.end())
        colunas = resolver_colunas(content, content[insert.end():fim_colunas].strip(), insert.start())
        inicio = RE_VALUES.match(content, fim_colunas)
        tuplas = ler_tuplas(content, inicio.end(), delimitador_php) if inicio else None
        if colunas is None or tuplas is None:
            registros.append({"origem": "INSERT", "erro_parser": "lista de colunas ou de valores nao interpretada", "linha": line(insert.start())})
            continue
        nomes = [coluna.strip().lower() for coluna in colunas.split(",")]
        for valores in tuplas:
            if len(valores) > len(nomes) or set(nomes[len(valores):]) & COLUNAS_AUDITADAS.keys():
                registros.append({"origem": "INSERT", "erro_parser": "colunas e valores do INSERT nao correspondem", "linha": line(insert.start())})
                continue
            atributos = {
                COLUNAS_AUDITADAS[nome]: (classificar_valor(valor), insert.start())
                for nome, valor in zip(nomes, valores) if nome in COLUNAS_AUDITADAS
            }
            registros.append(montar_cadastro("INSERT", atributos, insert.start(), line))

    return registros


def validar_k1_range(tarefas):
    errors = []
    for t in tarefas:
        if t["id"] is None:
            errors.append({
                "codigo": "K001", "regra": "K1", "id": None, "nome": t["nome"],
                "mensagem": "registro sem id_tarefa numerico", "linha": t.get("linha_nome"),
            })
            continue
        if not isinstance(t["id"], int):
            errors.append({
                "codigo": "K001", "regra": "K1", "id": t["id"], "nome": t["nome"],
                "mensagem": "id_tarefa deve ser numerico", "linha": t.get("linha"),
            })
            continue
        if t["id"] < 1000 and t["id"] != 65:
            errors.append({
                "codigo": "K001",
                "regra": "K1",
                "id": t["id"],
                "nome": t["nome"],
                "mensagem": f"ID {t['id']} < 1000, reservado para SEI core (use >= 1000 ou ID=65)",
                "linha": t.get("linha"),
            })
        elif t["id"] == 65 and not t.get("descr"):
            errors.append({
                "codigo": "K007",
                "regra": "K7",
                "id": 65,
                "nome": t["nome"],
                "mensagem": "ID=65 usado sem atributo DESCRICAO não vazio; tarefa free-text deve ter descricao",
                "linha": t.get("linha"),
            })
    return errors


def validar_k3_prefixo(tarefas):
    errors = []
    for t in tarefas:
        nome = t["nome"]
        if nome is None:
            mensagem = (
                f"id_tarefa_modulo nao literal ({t['nome_expr']}); confirme prefixo, tamanho e unicidade na revisao"
                if t.get("nome_expr") else "registro sem id_tarefa_modulo"
            )
            errors.append({
                "codigo": "K003", "regra": "K3", "id": t["id"], "nome": None,
                "mensagem": mensagem, "linha": t.get("linha_nome") or t.get("linha"),
            })
            continue
        if not re.match(r'^MD_[A-Z0-9]+_[A-Z0-9_]+$', nome):
            errors.append({
                "codigo": "K003",
                "regra": "K3",
                "id": t["id"],
                "nome": nome,
                "mensagem": f"Nome '{nome}' nao segue padrao MD_<INST>_<NOME> em maiusculas",
                "linha": t.get("linha_nome"),
            })
    return errors


def validar_k4_tamanho(tarefas):
    errors = []
    for t in tarefas:
        if t["nome"] is None:
            continue
        if len(t["nome"]) > 50:
            errors.append({
                "codigo": "K004",
                "regra": "K4",
                "id": t["id"],
                "nome": t["nome"],
                "mensagem": f"Nome '{t['nome']}' excede 50 caracteres ({len(t['nome'])})",
                "linha": t.get("linha_nome"),
            })
    return errors


def validar_k6_duplicidade(tarefas):
    errors = []
    seen_ids = {}
    seen_names = set()
    for t in tarefas:
        if t["id"] is not None and t["id"] in seen_ids:
            errors.append({
                "codigo": "K006",
                "regra": "K6",
                "id": t["id"],
                "nome": t["nome"],
                "mensagem": f"ID {t['id']} duplicado no modulo",
                "linha": t.get("linha"),
                "file": t.get("file"),
            })
        if t["id"] is not None:
            seen_ids[t["id"]] = t["nome"]
        if t["nome"] is not None and t["nome"] in seen_names:
            errors.append({
                "codigo": "K006", "regra": "K6", "id": t["id"], "nome": t["nome"],
                "mensagem": f"id_tarefa_modulo '{t['nome']}' duplicado no modulo",
                "linha": t.get("linha_nome"), "file": t.get("file"),
            })
        if t["nome"] is not None:
            seen_names.add(t["nome"])
    return errors


def vem_da_sequencia(expressao, content, posicao):
    """Variavel cuja ultima atribuicao antes do uso e a chamada getValorSequencia('seq_tarefa'), sem alteracao depois."""
    if not re.fullmatch(r"\$\w+", expressao or ""):
        return False
    var = re.escape(expressao)
    atribuicoes = list(re.finditer(var + r"\s*=(?![=>])([^;]*);", content[:posicao]))
    if not atribuicoes or not RE_CHAMADA_SEQ_TAREFA.fullmatch(atribuicoes[-1].group(1).strip()):
        return False
    alteracao = var + r"\s*(?:\+\+|--|[-+*/.%]=)|(?:\+\+|--)\s*" + var
    return not re.search(alteracao, content[atribuicoes[-1].end():posicao])


def inteiro_da_variavel(expressao, content, posicao):
    """Inteiro literal da ultima atribuicao da variavel antes do uso, sem alteracao depois; None se nao resolver."""
    if not re.fullmatch(r"\$\w+", expressao or ""):
        return None
    var = re.escape(expressao)
    atribuicoes = list(re.finditer(var + r"\s*=(?![=>])([^;]*);", content[:posicao]))
    if not atribuicoes:
        return None
    valor = classificar_valor(atribuicoes[-1].group(1))
    alteracao = var + r"\s*(?:\+\+|--|[-+*/.%]=)|(?:\+\+|--)\s*" + var
    if valor["tipo"] != "int" or re.search(alteracao, content[atribuicoes[-1].end():posicao]):
        return None
    return valor["valor"]


def validar_cadastro_id(tarefas, content):
    """K1 e K8 no cadastro: id de modulo >= 1000 e id fora de getValorSequencia coerente com seq_tarefa.

    Devolve os erros e os avisos: o ajuste da seq_tarefa por SQL proprio vira aviso para a revisao.
    """
    errors = []
    warnings = []
    realinha_pelo_core = bool(RE_REALINHA_PELO_CORE.search(content))
    realinha_por_sql = bool(RE_REALINHA_POR_SQL.search(content))
    for t in tarefas:
        tipo = t["id_tipo"]
        base = {"id": t["id"], "nome": t["nome"], "linha": t["linha"]}
        # Variavel com inteiro literal na ultima atribuicao vale como o literal no K1, com ou sem realinhamento.
        numero = inteiro_da_variavel(t["id_expr"], content, t["posicao_id"]) if tipo == "expr" else t["id"]
        if numero == 65:
            errors.append({**base, "id": numero, "codigo": "K001", "regra": "K1",
                           "mensagem": "tarefa 65 e do core; o modulo lanca andamento com ela e o atributo DESCRICAO, sem cadastra-la"})
        elif numero is not None and numero < 1000:
            errors.append({**base, "id": numero, "codigo": "K001", "regra": "K1",
                           "mensagem": f"ID {numero} < 1000, reservado para o core do SEI"})
        elif tipo in ("ausente", "null", "str"):
            errors.append({**base, "codigo": "K001", "regra": "K1",
                           "mensagem": "cadastro sem id_tarefa numerico; a PK de TarefaDTO e informada"})
        elif tipo in ("int", "expr") and not (realinha_pelo_core or vem_da_sequencia(t["id_expr"], content, t["posicao_id"])):
            origem = f"fixo ({t['id']})" if tipo == "int" else f"calculado ({t['id_expr']})"
            if realinha_por_sql:
                warnings.append({**base, "codigo": "K008", "regra": "K8",
                                 "mensagem": f"id_tarefa {origem} com seq_tarefa ajustada por SQL proprio; confirme que a "
                                             "sequence comeca no ultimo id gravado mais 1 nos quatro bancos, ou use o trecho do K8"})
                continue
            errors.append({**base, "codigo": "K008", "regra": "K8",
                           "mensagem": f"id_tarefa {origem} sem getValorSequencia('seq_tarefa') e sem realinhar seq_tarefa"})
    return errors, warnings


def validar_k9_sinalizadores(tarefas):
    """K9: os cinco sinalizadores da tarefa ficam explicitos no cadastro, com S ou N quando literais."""
    errors = []
    for t in tarefas:
        base = {"codigo": "K009", "regra": "K9", "id": t["id"], "nome": t["nome"], "linha": t["linha"]}
        ausentes = [coluna for coluna in SINALIZADORES if coluna not in t["sinalizadores"]]
        invalidos = [
            coluna for coluna, valor in t["sinalizadores"].items()
            if valor["tipo"] in ("int", "str", "null") and valor["valor"] not in ("S", "N")
        ]
        if ausentes:
            errors.append({**base, "mensagem": "sinalizador sem valor explicito: " + ", ".join(ausentes)})
        if invalidos:
            errors.append({**base, "mensagem": "sinalizador fora de S/N: " + ", ".join(invalidos)})
    return errors


# ═══════════════════════════════════════════════════════════════
# FORMATTERS
# ═══════════════════════════════════════════════════════════════

def formatar_markdown(file_results, verdict):
    sep = "━" * 54
    lines = [f" sei-verificacao-tarefa v{VERSION}", sep]

    all_errors = []
    for r in file_results:
        for e in r.get("erros", []):
            all_errors.append({**e, "file": r["file"]})

    if all_errors:
        lines.append("\n BLOQUEIOS")
        for e in all_errors:
            suffix = f" (linha {e['linha']})" if e.get("linha") else ""
            lines.append(f"  ✗ {e['file']}: {e['codigo']} - {e['mensagem']}{suffix}")
        lines.append(sep)

    for r in file_results:
        fname = r["file"]
        tarefas = r.get("tarefas", [])
        errors = r.get("erros", [])
        warnings = r.get("avisos", [])

        if errors:
            lines.append(f"\n✗ {fname}")
            for e in errors:
                suffix = f" (linha {e['linha']})" if e.get("linha") else ""
                lines.append(f"   ✗ {e['codigo']} - ID {e.get('id', '?')}: {e['mensagem']}{suffix}")
        if warnings:
            lines.append(f"\n⚠ {fname}")
            for w in warnings:
                lines.append(f"   ⚠ {w['codigo']} - ID {w.get('id', '?')}: {w['mensagem']}")
        if tarefas and not errors and not warnings:
            lines.append(f"\n✓ {fname} ({len(tarefas)} tarefas, conformidade total)")
        if not tarefas and not errors:
            lines.append(f"\n⚠ {fname}, nenhuma tarefa encontrada")

        lines.append(sep)

    total_erros = sum(len(r.get("erros", [])) for r in file_results)
    total_warns = sum(len(r.get("avisos", [])) for r in file_results)
    verdict_label = {"PASS": "PASS", "WARN": "WARN, avisos presentes", "BLOCK": "BLOCK, corrija erros"}

    lines.append(f"\nRESUMO  Erros: {total_erros}  |  Avisos: {total_warns}")
    lines.append(f"Veredito: {verdict_label.get(verdict, verdict)}")

    return "\n".join(lines)


def formatar_json(file_results, verdict):
    all_errors = []
    all_warnings = []
    for r in file_results:
        for e in r.get("erros", []):
            e["file"] = r["file"]
            all_errors.append(e)
        for w in r.get("avisos", []):
            w["file"] = r["file"]
            all_warnings.append(w)

    return {
        "skill": SKILL_NAME,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": file_results,
        "stats": {"arquivos": len(file_results), "erros": len(all_errors), "avisos": len(all_warnings)},
        "verdict": verdict
    }


def determinar_verdict(file_results):
    if not file_results:
        return "BLOCK"
    if any(r.get("erros") for r in file_results):
        return "BLOCK"
    if any(r.get("avisos") for r in file_results):
        return "WARN"
    return "PASS"


# ═══════════════════════════════════════════════════════════════
# AUDIT FILE
# ═══════════════════════════════════════════════════════════════

def audit_file(path):
    errors = []
    warnings = []

    try:
        content = ler_conteudo(path)
    except Exception as e:
        return {"file": os.path.basename(path), "tarefas": [], "erros": [{"codigo": "K000", "regra": "?", "mensagem": f"Erro ao ler: {e}"}], "avisos": [], "status": "BLOCK"}

    content = mask_php_comments(content)
    cadastros = parse_cadastros(content)
    if cadastros:
        tarefas = [t for t in cadastros if "erro_parser" not in t]
        errors.extend(
            {"codigo": "K000", "regra": "?", "mensagem": f"cadastro de tarefa nao interpretado: {t['erro_parser']}", "linha": t["linha"]}
            for t in cadastros if "erro_parser" in t
        )
    else:
        tarefas = parse_tarefas(content)
    for tarefa in tarefas:
        tarefa["file"] = os.path.basename(path)

    if not tarefas and not errors:
        return {"file": os.path.basename(path), "path": path, "tarefas": [], "erros": [{"codigo": "K000", "regra": "?", "mensagem": "parser nao extraiu definicao de tarefa"}], "avisos": [], "status": "BLOCK"}

    if cadastros:
        erros_do_id, avisos_do_id = validar_cadastro_id(tarefas, content)
        errors.extend(erros_do_id)
        warnings.extend(avisos_do_id)
        errors.extend(validar_k9_sinalizadores(tarefas))
    else:
        errors.extend(validar_k1_range(tarefas))
    errors.extend(validar_k3_prefixo(tarefas))
    errors.extend(validar_k4_tamanho(tarefas))

    status = "BLOCK" if errors else ("WARN" if warnings else "PASS")

    return {
        "file": os.path.basename(path),
        "path": path,
        "tarefas": tarefas,
        "erros": errors,
        "avisos": warnings,
        "status": status
    }


def ler_conteudo(path):
    with open(path, 'r', encoding='utf-8', errors='replace') as f:
        return f.read()


def is_tarefa_file(path):
    """Elegivel: definicao *tarefa* ou PHP que cadastra tarefa por TarefaDTO ou INSERT INTO tarefa."""
    name = os.path.basename(path)
    if not (name.endswith('.php') or name.endswith('.php.example')):
        return False
    if 'tarefa' in name.lower():
        return True
    try:
        return bool(parse_cadastros(mask_php_comments(ler_conteudo(path))))
    except OSError:
        return False


def run_audit(input_path, output_format='markdown', mode='adhoc'):
    file_results = []

    if os.path.isfile(input_path):
        if is_tarefa_file(input_path):
            file_results.append(audit_file(input_path))

    elif os.path.isdir(input_path):
        for f in os.listdir(input_path):
            fpath = os.path.join(input_path, f)
            if os.path.isfile(fpath) and is_tarefa_file(fpath):
                file_results.append(audit_file(fpath))

    elif ',' in input_path:
        for p in input_path.split(','):
            p = p.strip()
            if os.path.exists(p) and is_tarefa_file(p):
                file_results.append(audit_file(p))

    if not file_results:
        file_results.append({
            "file": os.path.basename(input_path) or input_path,
            "tarefas": [],
            "erros": [{"codigo": "K000", "regra": "?", "mensagem": "nenhum script de tarefa elegivel analisado"}],
            "avisos": [],
            "status": "BLOCK",
        })

    duplicate_errors = validar_k6_duplicidade([
        tarefa
        for result in file_results
        for tarefa in result.get("tarefas", [])
    ])
    for error in duplicate_errors:
        target = next((result for result in file_results if result["file"] == error.get("file")), None)
        if target is not None:
            target["erros"].append(error)
            target["status"] = "BLOCK"

    verdict = determinar_verdict(file_results)

    if output_format == 'json':
        return formatar_json(file_results, verdict), file_results, verdict
    return formatar_markdown(file_results, verdict), file_results, verdict


# ═══════════════════════════════════════════════════════════════
# MAIN
# ═══════════════════════════════════════════════════════════════

def main():
    parser = argparse.ArgumentParser(description="sei-verificacao-tarefa: auditor de IDs de tarefa SEI")
    parser.add_argument("--input", required=True, help="Script de release que cadastra tarefa, arquivo *_tarefa.php, diretorio, ou lista separada por virgula")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Formato de saida")
    parser.add_argument("--exit-code", action="store_true", help="Retorna exit code ao inves de imprimir output")

    args = parser.parse_args()

    output, file_results, verdict = run_audit(args.input, args.format)

    if args.format == 'json':
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(output)

    if args.exit_code:
        exit_map = {"PASS": 0, "WARN": 1, "BLOCK": 2}
        sys.exit(exit_map.get(verdict, 0))


if __name__ == "__main__":
    main()
