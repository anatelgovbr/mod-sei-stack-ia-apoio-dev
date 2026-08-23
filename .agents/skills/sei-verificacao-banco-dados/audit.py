#!/usr/bin/env python3
"""
sei-verificacao-banco-dados
Skill autonoma de code review para validacao de modelagem de dados SEI/SIP
contra os padroes dos manuais TRF4.

Aceita: arquivo PHP (dto/bd), multiplos arquivos, diretorio de modulo, DDL raw
Output: JSON ou Markdown com erros/avisos e veredito (BLOCK/WARN/PASS)
Com --exit-code: 0=PASS, 1=WARN, 2=BLOCK
"""

import sys
import os
import re
import json
import argparse
from datetime import datetime, timezone
from pathlib import Path
from typing import Optional


VERSION = "1.0.0"
SKILL_NAME = "sei-verificacao-banco-dados"


# ═══════════════════════════════════════════════════════════════
# REGEX PATTERNS: PHP (InfraPHP DTO/BD)
# ═══════════════════════════════════════════════════════════════

RE_TABELA = re.compile(
    r"getStrNomeTabela\s*\([^)]*\)\s*(?::\s*\??string)?\s*\{[^}]*?return\s+['\"]([^'\"]+)['\"]",
    re.DOTALL
)
RE_COLUNA_DTO = re.compile(
    r"adicionarAtributoTabela\s*\(\s*([^,]+)\s*,\s*['\"]?([^,'\"]+)['\"]?\s*,\s*['\"]?([^),]+)['\"]?",
    re.DOTALL
)
RE_PK = re.compile(
    r"configurarPK\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*([^)]+)\)",
    re.DOTALL
)
RE_FK = re.compile(
    r"configurarFK\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]",
    re.DOTALL
)
RE_EXC_LOGICA = re.compile(
    r"configurarExclusaoLogica\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*\)",
    re.DOTALL
)
RE_COLUNA_RELACIONADA = re.compile(
    r"adicionarAtributoTabelaRelacionada\s*\(\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^,]+)\s*,\s*([^)]+)\)",
    re.DOTALL
)
RE_DOCBLOCK_TABLE = re.compile(r"@table\s+(.+)")
RE_DOCBLOCK_COLUMN = re.compile(r"@column\s+(\w+)\s+(.+)")
RE_META_PK_CALL = re.compile(
    r"adicionarChavePrimaria\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*\[([^\]]*)\]",
    re.IGNORECASE,
)
RE_META_FK_CALL = re.compile(
    r"adicionarChaveEstrangeira\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*\[([^\]]*)\]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*\[([^\]]*)\]",
    re.IGNORECASE,
)
RE_META_INDEX_CALL = re.compile(
    r"criarIndice\s*\(\s*['\"]([^'\"]+)['\"]\s*,\s*['\"]([^'\"]+)['\"]\s*,\s*\[([^\]]*)\]",
    re.IGNORECASE,
)
RE_SIN_ATIVO_COLUNA = re.compile(r"['\"]sin_ativo['\"]", re.IGNORECASE)
RE_FK_CONSTRAINT = re.compile(r"fk_md_\w+_\w+_\w+")
RE_PK_CONSTRAINT = re.compile(r"pk_md_\w+_\w+")
RE_AK_CONSTRAINT = re.compile(r"ak_md_\w+_\w+(?:_\w+)*")
RE_SEQ_NOME = re.compile(r"seq_\w+")
RE_INDEX_CREATE = re.compile(r"CREATE\s+INDEX", re.IGNORECASE)
RE_INFRA_SEQUENCIA = re.compile(r"InfraSequencia", re.IGNORECASE)

RE_TIPO_PK_SEQUENCIAL = re.compile(r"TIPO_PK_SEQUENCIAL|TIPO_PK_NATIVA", re.IGNORECASE)

RE_VARCHAR = re.compile(r"varchar\s*\(\s*\d+\s*\)", re.IGNORECASE)
RE_NUMERIC = re.compile(r"numeric\s*\(\s*\d+\s*(?:,\s*\d+)?\s*\)", re.IGNORECASE)
RE_CHAR = re.compile(r"char\s*\(\s*\d+\s*\)", re.IGNORECASE)
RE_INTEGER = re.compile(r"\b(integer|int)\b", re.IGNORECASE)
RE_SMALLINT = re.compile(r"\bsmallint\b", re.IGNORECASE)
RE_BOOLEAN = re.compile(r"\bboolean\b", re.IGNORECASE)
RE_DATE = re.compile(r"\bdate\b", re.IGNORECASE)
RE_TIMESTAMP = re.compile(r"\btimestamp\b", re.IGNORECASE)
RE_BLOB = re.compile(r"\bblob\b", re.IGNORECASE)
RE_SERIAL = re.compile(r"\bserial\b", re.IGNORECASE)
RE_MONEY = re.compile(r"\bmoney\b", re.IGNORECASE)
RE_TEXT = re.compile(r"\btext\b", re.IGNORECASE)
RE_SEQ_TABLE = re.compile(r"^seq_")


# ═══════════════════════════════════════════════════════════════
# REGEX PATTERNS: SQL/DDL
# ═══════════════════════════════════════════════════════════════

RE_CREATE_TABLE = re.compile(
    r'CREATE\s+TABLE\s+(\w+)\s*\((.+)\)\s*;?',
    re.DOTALL | re.IGNORECASE
)
RE_PRIMARY_KEY = re.compile(r'PRIMARY\s+KEY\s*\(([^)]+)\)', re.IGNORECASE)
RE_FOREIGN_KEY_SQL = re.compile(
    r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)\s*\(([^)]+)\)',
    re.IGNORECASE
)
RE_UNIQUE_SQL = re.compile(r'UNIQUE\s*\(([^)]+)\)', re.IGNORECASE)
RE_CREATE_INDEX_SQL = re.compile(
    r'CREATE\s+(?:UNIQUE\s+)?INDEX\s+(?:(\w+)\s+)?ON\s+(\w+)\s*\(([^)]+)\)',
    re.DOTALL | re.IGNORECASE
)
RE_COMMENT_ON = re.compile(
    r'COMMENT\s+ON\s+(?:TABLE\s+\w+|COLUMN\s+\w+\.\w+)\s+IS\s+(["\'])(.+?)\1',
    re.IGNORECASE
)
RE_SEQ_NATIVE = re.compile(r'criarSequencialNativa\s*\(\s*[\'"]seq_(\w+)', re.IGNORECASE)
RE_SEQ_MYSQL = re.compile(
    r'create\s+table\s+seq_(\w+)\s*\(',
    re.IGNORECASE
)
RE_SEQ_SQLSERVER = re.compile(
    r'identity\s*\(\s*1\s*,\s*1\s*\)',
    re.IGNORECASE
)
RE_GENERATED_IDENTITY = re.compile(r'\bGENERATED\s+(?:ALWAYS|BY\s+DEFAULT)\s+AS\s+IDENTITY\b', re.IGNORECASE)
RE_TEXT_TYPE = re.compile(r'^TEXT\b', re.IGNORECASE)
RE_AUTOINCREMENT = re.compile(r'AUTO_INCREMENT\s*=\s*(\d+)', re.IGNORECASE)
RE_BIGINT = re.compile(r'\bbigint\b', re.IGNORECASE)
RE_BLOB2 = re.compile(r'\bblob\b', re.IGNORECASE)
RE_TEXT2 = re.compile(r'\btext\b', re.IGNORECASE)
RE_SERIAL2 = re.compile(r'\bserial\b', re.IGNORECASE)
RE_MONEY2 = re.compile(r'\bmoney\b', re.IGNORECASE)
RE_NUMERIC_COL = re.compile(
    r'numeric\s*\(\s*(\d+)\s*,\s*(\d+)\s*\)',
    re.IGNORECASE
)
RE_INTEGER_COL = re.compile(
    r'(?:(?:big|small|tiny)\s*int|integer|int)\s*(\(\s*\d+\s*\))?',
    re.IGNORECASE
)
RE_VARCHAR_COL = re.compile(
    r'(?:var)?char\s*\(\s*(\d+)\s*\)',
    re.IGNORECASE
)


# ═══════════════════════════════════════════════════════════════
# REGRAS: definicao e validadores
# ═══════════════════════════════════════════════════════════════

REGRAS = [
    {
        "id": "DB01",
        "nome": "Nome tabela md_<sigla>_<entidade>",
        "severidade": "erro",
        "base": "Manual SEI MD §Tabela",
    },
    {
        "id": "DB02",
        "nome": "Relacionamento N:N",
        "severidade": "erro",
        "base": "Manual SEI MD §Tabela",
    },
    {
        "id": "DB03",
        "nome": "Limite de 26 caracteres",
        "severidade": "erro",
        "base": "Manual SEI MD §Regras Gerais",
    },
    {
        "id": "DB04",
        "nome": "PK sequencial",
        "severidade": "erro",
        "base": "Manual SEI MD §Colunas",
    },
    {
        "id": "DB05",
        "nome": "FK constraint naming",
        "severidade": "erro",
        "base": "Manual SEI MD §Chave Estrangeira",
    },
    {
        "id": "DB06",
        "nome": "sin_ativo em exclusao logica",
        "severidade": "erro",
        "base": "Manual SEI MD §Colunas",
    },
    {
        "id": "DB07",
        "nome": "PK constraint naming",
        "severidade": "erro",
        "base": "Manual SEI MD §Chave Primária",
    },
    {
        "id": "DB08",
        "nome": "Tipos SQL-99",
        "severidade": "erro",
        "base": "Manual SEI MD §Tipos de Dados",
    },
    {
        "id": "DB09",
        "nome": "Indice em FK",
        "severidade": "aviso",
        "base": "Manual SEI MD §Índices",
    },
    {
        "id": "DB10",
        "nome": "Sequence naming",
        "severidade": "aviso",
        "base": "Manual SEI MD §Sequências",
    },
    {
        "id": "DB11",
        "nome": "AK constraint naming",
        "severidade": "aviso",
        "base": "Manual SEI MD §Chave Alternativa",
    },
    {
        "id": "DB12",
        "nome": "Comentarios/Docblock",
        "severidade": "aviso",
        "base": "Manual SEI MD §Regras Gerais",
    },
    {
        "id": "DB13",
        "nome": "Sem verbos no nome",
        "severidade": "aviso",
        "base": "Manual SEI MD §Tabela",
    },
    {
        "id": "DB14",
        "nome": "Singular",
        "severidade": "aviso",
        "base": "Manual SEI MD §Regras Gerais",
    },
    {
        "id": "DB15",
        "nome": "Formato do nome",
        "severidade": "aviso",
        "base": "Manual SEI MD §Regras Gerais",
    },
]


# ═══════════════════════════════════════════════════════════════
# ENTITIES: estruturas extraidas de PHP/DDL
# ═══════════════════════════════════════════════════════════════

class Entity:
    def __init__(self, nome_tabela: str, arquivos: list[str]):
        self.nome_tabela = nome_tabela
        self.arquivos = arquivos
        self.colunas = []
        self.pk_coluna = None
        self.pk_tipo = None
        self.pk_colunas = []
        self.pk_tipos = {}
        self.fks = []
        self.fk_constraints = []
        self.colunas_relacionadas = []
        self.tem_exclusao_logica = False
        self.campo_exclusao_logica = None
        self.tem_docblock = False
        self.constraint_pk = None
        self.constraints_fk = []
        self.constraints_ak = []
        self.constraints_index = []
        self.indices = []
        self.supplemental_constraints_fk = []
        self.tem_sequence = False
        self.tipos_invalidos = []
        self.sequencias_encontradas = []
        self.tem_bigint = False
        self.tem_blob = False
        self.tem_text = False
        self.tem_geracao_automatica = False
        self.evidencias = {}

    def registrar_evidencia(self, tipo: str, arquivo: str, linha: int, objeto: str = None):
        evidencia = {"arquivo": arquivo, "linha": linha}
        chaves = [tipo]
        if objeto:
            chaves.insert(0, f"{tipo}:{objeto.lower()}")
        for chave in chaves:
            if evidencia not in self.evidencias.setdefault(chave, []):
                self.evidencias[chave].append(evidencia)

    def obter_evidencia(self, tipo: str = "tabela", objeto: str = None) -> dict:
        chave = f"{tipo}:{objeto.lower()}" if objeto else tipo
        candidatas = self.evidencias.get(chave) or self.evidencias.get(tipo) or self.evidencias.get("tabela")
        if candidatas:
            return candidatas[0].copy()
        return {"arquivo": self.arquivos[0] if self.arquivos else "", "linha": 1}

    def adicionar_coluna(self, nome: str, tipo: str = None, arquivo: str = None, linha: int = None):
        self.colunas.append({"nome": nome, "tipo": tipo})
        if arquivo and linha:
            self.registrar_evidencia("coluna", arquivo, linha, nome)

    def adicionar_fk(self, coluna: str, tabela_ref: str, coluna_ref: str, arquivo: str = None, linha: int = None):
        self.fks.append({
            "coluna": coluna,
            "coluna_sql": coluna,
            "tabela_ref": tabela_ref,
            "tabela_ref_base": normalize_table_ref(tabela_ref),
            "coluna_ref": coluna_ref,
            "coluna_ref_base": normalize_column_ref(coluna_ref),
        })
        if arquivo and linha:
            self.registrar_evidencia("fk", arquivo, linha, coluna)


def parse_php_array_items(raw: str) -> list[str]:
    return [match.group(1).strip() for match in re.finditer(r"['\"]([^'\"]+)['\"]", raw)]


def split_php_args(raw: str) -> list[str]:
    args = []
    start = 0
    depth = 0
    quote = None
    for index, char in enumerate(raw):
        if quote:
            if char == quote and (index == 0 or raw[index - 1] != "\\"):
                quote = None
        elif char in "'\"":
            quote = char
        elif char in "([":
            depth += 1
        elif char in ")]":
            depth -= 1
        elif char == "," and depth == 0:
            args.append(raw[start:index].strip())
            start = index + 1
    args.append(raw[start:].strip())
    return args


def extract_php_calls(content: str, function_name: str):
    pattern = re.compile(rf"\b{re.escape(function_name)}\s*\(", re.IGNORECASE)
    for match in pattern.finditer(content):
        opening = content.find("(", match.start(), match.end())
        depth = 0
        quote = None
        for index in range(opening, len(content)):
            char = content[index]
            if quote:
                if char == quote and content[index - 1] != "\\":
                    quote = None
            elif char in "'\"":
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    yield split_php_args(content[opening + 1:index]), match.start()
                    break


def php_literal(raw: str) -> str:
    value = raw.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "'\"":
        return value[1:-1]
    return value


def get_entity(entities: dict[str, Entity], table_name: str, path: str) -> Entity:
    entity = entities.get(table_name)
    if entity is None:
        entity = Entity(table_name, [path])
        entity.tem_docblock = True
        entities[table_name] = entity
    elif path not in entity.arquivos:
        entity.arquivos.append(path)
    return entity


def apply_php_metadata(path: str, content: str, entities: dict[str, Entity]):
    for args, position in extract_php_calls(content, "adicionarColuna"):
        if len(args) >= 2:
            entity = get_entity(entities, php_literal(args[0]), path)
            entity.adicionar_coluna(php_literal(args[1]), args[2] if len(args) > 2 else "", path, content[:position].count("\n") + 1)

    for args, position in extract_php_calls(content, "adicionarChavePrimaria"):
        if len(args) >= 3:
            entity = get_entity(entities, php_literal(args[0]), path)
            entity.constraint_pk = php_literal(args[1])
            columns = parse_php_array_items(args[2])
            if columns:
                entity.pk_coluna = columns[0]
                entity.pk_colunas = columns
                entity.pk_tipo = "informado"
                entity.pk_tipos = {column: entity.pk_tipo for column in columns}
                for column in columns:
                    entity.registrar_evidencia("pk", path, content[:position].count("\n") + 1, column)

    for args, position in extract_php_calls(content, "adicionarChaveEstrangeira"):
        if len(args) >= 5:
            constraint = php_literal(args[0])
            entity = get_entity(entities, php_literal(args[1]), path)
            columns = parse_php_array_items(args[2])
            ref_columns = parse_php_array_items(args[4])
            entity.constraints_fk.append(constraint)
            entity.fk_constraints.append({"nome": constraint, "colunas": columns, "tabela_ref": php_literal(args[3])})
            entity.supplemental_constraints_fk.append(constraint)
            entity.registrar_evidencia("constraint", path, content[:position].count("\n") + 1, constraint)
            if columns:
                entity.adicionar_fk(columns[0], php_literal(args[3]), ref_columns[0] if ref_columns else "", path, content[:position].count("\n") + 1)

    for args, position in extract_php_calls(content, "criarIndice"):
        if len(args) >= 3:
            entity = get_entity(entities, php_literal(args[0]), path)
            name = php_literal(args[1])
            columns = parse_php_array_items(args[2])
            entity.constraints_index.append(name)
            entity.indices.append({"nome": name, "colunas": columns})
            entity.registrar_evidencia("indice", path, content[:position].count("\n") + 1, name)

    for args, position in extract_php_calls(content, "criarSequencialNativa"):
        if args:
            sequence = php_literal(args[0])
            table_name = sequence[4:] if sequence.startswith("seq_") else sequence
            entity = get_entity(entities, table_name, path)
            entity.tem_sequence = True
            entity.sequencias_encontradas.append(sequence)
            entity.registrar_evidencia("sequence", path, content[:position].count("\n") + 1, sequence)


def normalize_table_ref(tabela_ref: str) -> str:
    return tabela_ref.strip().split()[0]


def normalize_column_ref(coluna_ref: str) -> str:
    return coluna_ref.strip().split('.')[-1]


def identifier_mentions_table(identifier: str, table_name: str) -> bool:
    identifier_tokens = identifier.lower().split("_")
    table_tokens = table_name.lower().split("_")
    if table_tokens[:1] == ["md"] and len(table_tokens) > 2:
        table_tokens = table_tokens[2:]
    meaningful = [token for token in table_tokens if token not in {"rel", "adm", "tipo"}]
    return bool(meaningful) and any(
        len(identifier_token) >= 3
        and len(table_token) >= 3
        and (identifier_token.startswith(table_token[:3]) or table_token.startswith(identifier_token[:3]))
        for identifier_token in identifier_tokens
        for table_token in meaningful
    )


def merge_entity(base: Entity, extra: Entity):
    for arquivo in extra.arquivos:
        if arquivo not in base.arquivos:
            base.arquivos.append(arquivo)

    if extra.pk_coluna and not base.pk_coluna:
        base.pk_coluna = extra.pk_coluna

    if extra.pk_tipo and not base.pk_tipo:
        base.pk_tipo = extra.pk_tipo

    for coluna in extra.pk_colunas:
        if coluna not in base.pk_colunas:
            base.pk_colunas.append(coluna)
    base.pk_tipos.update(extra.pk_tipos)

    if extra.constraint_pk and not base.constraint_pk:
        base.constraint_pk = extra.constraint_pk

    if extra.tem_sequence:
        base.tem_sequence = True

    for seq in extra.sequencias_encontradas:
        if seq not in base.sequencias_encontradas:
            base.sequencias_encontradas.append(seq)

    existing_columns = {(column["nome"], column.get("tipo")) for column in base.colunas}
    for column in extra.colunas:
        key = (column["nome"], column.get("tipo"))
        if key not in existing_columns:
            base.colunas.append(column)
            existing_columns.add(key)

    for related in extra.colunas_relacionadas:
        if related not in base.colunas_relacionadas:
            base.colunas_relacionadas.append(related)

    existing_fk_keys = {
        (
            fk.get("coluna_sql") or fk["coluna"],
            fk.get("tabela_ref_base") or normalize_table_ref(fk["tabela_ref"]),
            fk.get("coluna_ref_base") or normalize_column_ref(fk["coluna_ref"]),
        )
        for fk in base.fks
    }
    for fk in extra.fks:
        key = (
            fk.get("coluna_sql") or fk["coluna"],
            fk.get("tabela_ref_base") or normalize_table_ref(fk["tabela_ref"]),
            fk.get("coluna_ref_base") or normalize_column_ref(fk["coluna_ref"]),
        )
        if key not in existing_fk_keys:
            base.fks.append(fk)
            existing_fk_keys.add(key)

    for valor in extra.constraints_fk:
        if valor not in base.constraints_fk:
            base.constraints_fk.append(valor)
        if valor not in base.supplemental_constraints_fk:
            base.supplemental_constraints_fk.append(valor)

    for relation in extra.fk_constraints:
        if relation not in base.fk_constraints:
            base.fk_constraints.append(relation)

    for nome_lista in ("constraints_ak", "constraints_index"):
        base_lista = getattr(base, nome_lista)
        for valor in getattr(extra, nome_lista):
            if valor not in base_lista:
                base_lista.append(valor)

    existing_indices = {
        (indice.get("nome", ""), tuple(indice.get("colunas", [])))
        for indice in base.indices
    }
    for indice in extra.indices:
        key = (indice.get("nome", ""), tuple(indice.get("colunas", [])))
        if key not in existing_indices:
            base.indices.append(indice)
            existing_indices.add(key)

    base.tem_exclusao_logica = base.tem_exclusao_logica or extra.tem_exclusao_logica
    base.campo_exclusao_logica = base.campo_exclusao_logica or extra.campo_exclusao_logica
    base.tem_docblock = base.tem_docblock or extra.tem_docblock
    base.tem_bigint = base.tem_bigint or extra.tem_bigint
    base.tem_blob = base.tem_blob or extra.tem_blob
    base.tem_text = base.tem_text or extra.tem_text
    base.tem_geracao_automatica = base.tem_geracao_automatica or extra.tem_geracao_automatica
    for invalid_type in extra.tipos_invalidos:
        if invalid_type not in base.tipos_invalidos:
            base.tipos_invalidos.append(invalid_type)
    for tipo, evidencias in extra.evidencias.items():
        for evidencia in evidencias:
            base.registrar_evidencia(tipo, evidencia["arquivo"], evidencia["linha"])


# ═══════════════════════════════════════════════════════════════
# PARSERS
# ═══════════════════════════════════════════════════════════════

def parse_php_dto(caminho: str, conteudo: str) -> Optional[Entity]:
    nome_tabela = None
    colunas = []
    pk_coluna = None
    pk_coluna_sql = None
    pk_tipo = None
    pk_colunas = []
    pk_tipos = {}
    fks = []
    tem_exclusao_logica = False
    campo_exclusao_logica = None
    tem_docblock = False

    match = RE_TABELA.search(conteudo)
    if match:
        nome_tabela = match.group(1).strip()

    if not nome_tabela:
        return None

    for match_col in RE_COLUNA_DTO.finditer(conteudo):
        pref = match_col.group(1).strip()
        nome_attr = match_col.group(2).strip().strip("'\"").rstrip("'\"")
        campo_sql = match_col.group(3).strip().strip("'\"").rstrip("'\"")
        colunas.append({"nome": campo_sql, "tipo": pref, "nome_attr": nome_attr})

    for match_pk in RE_PK.finditer(conteudo):
        pk_coluna_dto = match_pk.group(1).strip()
        pk_tipo_raw = match_pk.group(2).strip()
        pk_tipo = "sequencial" if RE_TIPO_PK_SEQUENCIAL.search(pk_tipo_raw) else "informado"
        pk_coluna_sql = None
        for col_item in colunas:
            if col_item.get("nome_attr") == pk_coluna_dto:
                pk_coluna_sql = col_item["nome"]
                break
        if pk_coluna_sql is None:
            for col_item in colunas:
                if col_item["nome"].lower() == f"id_{nome_tabela}":
                    pk_coluna_sql = col_item["nome"]
                    break
        if pk_coluna_sql is None:
            pk_coluna_sql = pk_coluna_dto
        pk_colunas.append(pk_coluna_sql)
        pk_tipos[pk_coluna_sql] = pk_tipo

    for match_fk in RE_FK.finditer(conteudo):
        attr = match_fk.group(1).strip()
        tabela_ref = match_fk.group(2).strip()
        campo_ref = match_fk.group(3).strip()
        coluna_sql = None
        for col_item in colunas:
            if col_item.get("nome_attr") == attr:
                coluna_sql = col_item["nome"]
                break
        fks.append({
            "coluna": attr,
            "coluna_sql": coluna_sql,
            "tabela_ref": tabela_ref,
            "tabela_ref_base": normalize_table_ref(tabela_ref),
            "coluna_ref": campo_ref,
            "coluna_ref_base": normalize_column_ref(campo_ref),
            "linha": conteudo[:match_fk.start()].count("\n") + 1,
        })

    for match_exc in RE_EXC_LOGICA.finditer(conteudo):
        tem_exclusao_logica = True
        campo_exclusao_logica = match_exc.group(1).strip()

    if RE_DOCBLOCK_TABLE.search(conteudo):
        tem_docblock = True

    entity = Entity(nome_tabela, [caminho])
    entity.colunas = colunas
    entity.pk_coluna = pk_coluna_sql
    entity.pk_tipo = pk_tipo
    entity.pk_colunas = pk_colunas
    entity.pk_tipos = pk_tipos
    entity.fks = fks
    entity.tem_exclusao_logica = tem_exclusao_logica
    entity.campo_exclusao_logica = campo_exclusao_logica
    entity.tem_docblock = tem_docblock
    entity.registrar_evidencia("tabela", caminho, conteudo[:match.start()].count("\n") + 1, nome_tabela)
    for match_col in RE_COLUNA_DTO.finditer(conteudo):
        column = match_col.group(3).strip().strip("'\"").rstrip("'\"")
        entity.registrar_evidencia("coluna", caminho, conteudo[:match_col.start()].count("\n") + 1, column)
    for match_pk in RE_PK.finditer(conteudo):
        attribute = match_pk.group(1).strip()
        column = next((item["nome"] for item in colunas if item.get("nome_attr") == attribute), attribute)
        entity.registrar_evidencia("pk", caminho, conteudo[:match_pk.start()].count("\n") + 1, column)
    for fk in fks:
        entity.registrar_evidencia("fk", caminho, fk.pop("linha"), fk.get("coluna_sql") or fk["coluna"])
    for match_col_rel in RE_COLUNA_RELACIONADA.finditer(conteudo):
        column = php_literal(match_col_rel.group(3))
        entity.colunas_relacionadas.append(column)
        entity.registrar_evidencia("related", caminho, conteudo[:match_col_rel.start()].count("\n") + 1, column)

    return entity


def parse_php_bd(caminho: str, conteudo: str, entities: dict):
    class_match = re.search(r"class\s+(\w+)BD\s+extends\s+InfraBD", conteudo)
    inferred_table = re.sub(r"(?<!^)(?=[A-Z])", "_", class_match.group(1)).lower() if class_match else None
    if inferred_table and inferred_table not in entities:
        entities[inferred_table] = Entity(inferred_table, [caminho])
    elif inferred_table in entities and caminho not in entities[inferred_table].arquivos:
        entities[inferred_table].arquivos.append(caminho)

    apply_php_metadata(caminho, conteudo, entities)
    has_sequence = RE_INFRA_SEQUENCIA.search(conteudo) is not None
    patterns = {
        "fk": re.compile(r"\bfk\d*_md_[a-z0-9_]+", re.IGNORECASE),
        "pk": re.compile(r"\bpk\d*_md_[a-z0-9_]+", re.IGNORECASE),
        "ak": re.compile(r"\bak\d*_md_[a-z0-9_]+", re.IGNORECASE),
        "index": re.compile(r"\bi\d+_[a-z0-9_]+", re.IGNORECASE),
    }
    for table_name, entity in entities.items():
        if has_sequence and (table_name == inferred_table or (inferred_table is None and len(entities) == 1)):
            entity.tem_sequence = True
        for kind, pattern in patterns.items():
            for match in pattern.finditer(conteudo):
                name = match.group(0)
                owners = [candidate for candidate in entities if candidate in name.lower()]
                owner = max(owners, key=len) if owners else None
                if len(entities) > 1 and owner != table_name:
                    continue
                if kind == "fk" and name not in entity.constraints_fk:
                    entity.constraints_fk.append(name)
                    entity.registrar_evidencia("constraint", caminho, conteudo[:match.start()].count("\n") + 1, name)
                elif kind == "pk" and not entity.constraint_pk:
                    entity.constraint_pk = name
                    entity.registrar_evidencia("constraint", caminho, conteudo[:match.start()].count("\n") + 1, name)
                elif kind == "ak" and name not in entity.constraints_ak:
                    entity.constraints_ak.append(name)
                    entity.registrar_evidencia("constraint", caminho, conteudo[:match.start()].count("\n") + 1, name)
                elif kind == "index" and name not in entity.constraints_index:
                    entity.constraints_index.append(name)
                    entity.registrar_evidencia("indice", caminho, conteudo[:match.start()].count("\n") + 1, name)


def parse_php_release_script(caminho: str, conteudo: str) -> list[Entity]:
    entities_by_name = {entity.nome_tabela: entity for entity in parse_ddl(caminho, conteudo)}
    apply_php_metadata(caminho, conteudo, entities_by_name)
    return list(entities_by_name.values())


def parse_ddl(caminho: str, conteudo: str) -> list[Entity]:
    entities_by_name = {}
    temporary_tables = set()
    create_pattern = re.compile(
        r"CREATE\s+((?:GLOBAL\s+)?TEMPORARY\s+|TEMP\s+)?TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?([A-Za-z_][\w$#]*)\s*\(",
        re.IGNORECASE,
    )
    for match_tbl in create_pattern.finditer(conteudo):
        nome_tabela = match_tbl.group(2).strip()
        if match_tbl.group(1) or nome_tabela.lower() in {"sei_teste", "sip_teste"}:
            temporary_tables.add(nome_tabela)
            continue
        opening = conteudo.find("(", match_tbl.start(), match_tbl.end())
        depth = 0
        quote = None
        closing = None
        for index in range(opening, len(conteudo)):
            char = conteudo[index]
            if quote:
                if char == quote and conteudo[index - 1] != "\\":
                    quote = None
            elif char in "'\"":
                quote = char
            elif char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
                if depth == 0:
                    closing = index
                    break
        if closing is None:
            continue

        corpo = conteudo[opening + 1:closing]
        entity = get_entity(entities_by_name, nome_tabela, caminho)
        entity.registrar_evidencia("tabela", caminho, conteudo[:match_tbl.start()].count("\n") + 1, nome_tabela)
        for definition in split_php_args(corpo):
            definition = definition.strip()
            definition_line = conteudo[:opening].count("\n") + corpo[:corpo.find(definition)].count("\n") + 1
            constraint_match = re.search(r"\bCONSTRAINT\s+([A-Za-z_][\w$#]*)", definition, re.IGNORECASE)
            constraint_name = constraint_match.group(1) if constraint_match else None
            pk_match = RE_PRIMARY_KEY.search(definition)
            if pk_match:
                columns = [column.strip().strip('"').strip("'") for column in pk_match.group(1).split(",")]
                entity.pk_coluna = columns[0]
                entity.pk_colunas = columns
                entity.pk_tipo = "informado"
                entity.pk_tipos = {column: entity.pk_tipo for column in columns}
                for column in columns:
                    entity.registrar_evidencia("pk", caminho, definition_line, column)
                if constraint_name:
                    entity.constraint_pk = constraint_name
                    entity.registrar_evidencia("constraint", caminho, definition_line, constraint_name)
                continue
            fk_match = RE_FOREIGN_KEY_SQL.search(definition)
            if fk_match:
                entity.adicionar_fk(
                    fk_match.group(1).strip().strip('"').strip("'"),
                    fk_match.group(2).strip(),
                    fk_match.group(3).strip().strip('"').strip("'"),
                    caminho,
                    definition_line,
                )
                if constraint_name:
                    entity.constraints_fk.append(constraint_name)
                    entity.fk_constraints.append({
                        "nome": constraint_name,
                        "colunas": [fk_match.group(1).strip().strip('"').strip("'")],
                        "tabela_ref": fk_match.group(2).strip(),
                    })
                    entity.registrar_evidencia("constraint", caminho, definition_line, constraint_name)
                continue
            unique_match = RE_UNIQUE_SQL.search(definition)
            if unique_match:
                if constraint_name:
                    entity.constraints_ak.append(constraint_name)
                    entity.registrar_evidencia("constraint", caminho, definition_line, constraint_name)
                continue
            column_match = re.match(r"[\"`]?([A-Za-z_][\w$#]*)[\"`]?\s+(.+)", definition, re.DOTALL)
            if column_match and column_match.group(1).upper() not in {"PRIMARY", "FOREIGN", "UNIQUE", "CONSTRAINT", "CHECK"}:
                column_type = column_match.group(2).strip()
                entity.adicionar_coluna(
                    column_match.group(1),
                    column_type,
                    caminho,
                    definition_line,
                )
                if RE_TEXT_TYPE.match(column_type):
                    entity.tem_text = True
                    if "text" not in entity.tipos_invalidos:
                        entity.tipos_invalidos.append("text")
                    entity.registrar_evidencia("type", caminho, definition_line, "text")
                if RE_SEQ_SQLSERVER.search(column_type) or RE_GENERATED_IDENTITY.search(column_type):
                    entity.tem_geracao_automatica = True
                    if "identity" not in entity.tipos_invalidos:
                        entity.tipos_invalidos.append("identity")
                    entity.registrar_evidencia("type", caminho, definition_line, "identity")
                elif re.search(r"\bAUTO_INCREMENT\b", column_type, re.IGNORECASE):
                    entity.tem_geracao_automatica = True

        if RE_BIGINT.search(corpo):
            entity.tem_bigint = True
        if RE_BLOB2.search(corpo):
            entity.tem_blob = True
        if RE_SERIAL2.search(corpo):
            entity.tipos_invalidos.append("serial")
            entity.registrar_evidencia("type", caminho, conteudo[:opening].count("\n") + corpo[:RE_SERIAL2.search(corpo).start()].count("\n") + 1, "serial")
        if RE_MONEY2.search(corpo):
            entity.tipos_invalidos.append("money")
            entity.registrar_evidencia("type", caminho, conteudo[:opening].count("\n") + corpo[:RE_MONEY2.search(corpo).start()].count("\n") + 1, "money")

    alter_pattern = re.compile(
        r"ALTER\s+TABLE\s+([A-Za-z_][\w$#]*)\s+ADD\s+(.+?)(?=;|['\"]\s*\)|$)",
        re.IGNORECASE | re.DOTALL,
    )
    for match in alter_pattern.finditer(conteudo):
        table_name = match.group(1)
        if table_name in temporary_tables:
            continue
        entity = get_entity(entities_by_name, table_name, caminho)
        entity.registrar_evidencia("tabela", caminho, conteudo[:match.start()].count("\n") + 1, table_name)
        definition = match.group(2).strip()
        constraint_match = re.search(r"\bCONSTRAINT\s+([A-Za-z_][\w$#]*)", definition, re.IGNORECASE)
        constraint_name = constraint_match.group(1) if constraint_match else None
        fk_match = RE_FOREIGN_KEY_SQL.search(definition)
        if fk_match:
            entity.adicionar_fk(fk_match.group(1).strip(), fk_match.group(2), fk_match.group(3).strip(), caminho, conteudo[:match.start()].count("\n") + 1)
            if constraint_name:
                entity.constraints_fk.append(constraint_name)
                entity.fk_constraints.append({
                    "nome": constraint_name,
                    "colunas": [fk_match.group(1).strip()],
                    "tabela_ref": fk_match.group(2),
                })
                entity.registrar_evidencia("constraint", caminho, conteudo[:match.start()].count("\n") + 1, constraint_name)
        elif RE_PRIMARY_KEY.search(definition):
            pk_match = RE_PRIMARY_KEY.search(definition)
            columns = [column.strip().strip('"').strip("'") for column in pk_match.group(1).split(",")]
            entity.pk_coluna = columns[0]
            entity.pk_colunas = columns
            entity.pk_tipo = "informado"
            entity.pk_tipos = {column: entity.pk_tipo for column in columns}
            entity.constraint_pk = constraint_name
            for column in columns:
                entity.registrar_evidencia("pk", caminho, conteudo[:match.start()].count("\n") + 1, column)
            if constraint_name:
                entity.registrar_evidencia("constraint", caminho, conteudo[:match.start()].count("\n") + 1, constraint_name)
        elif RE_UNIQUE_SQL.search(definition):
            if constraint_name:
                entity.constraints_ak.append(constraint_name)
                entity.registrar_evidencia("constraint", caminho, conteudo[:match.start()].count("\n") + 1, constraint_name)
        else:
            column_match = re.match(r"[\"`]?([A-Za-z_][\w$#]*)[\"`]?\s+(.+)", definition, re.DOTALL)
            if column_match:
                column_type = column_match.group(2).strip()
                line = conteudo[:match.start()].count("\n") + 1
                entity.adicionar_coluna(column_match.group(1), column_type, caminho, line)
                if RE_TEXT_TYPE.match(column_type):
                    entity.tem_text = True
                    if "text" not in entity.tipos_invalidos:
                        entity.tipos_invalidos.append("text")
                    entity.registrar_evidencia("type", caminho, line, "text")
                if RE_SEQ_SQLSERVER.search(column_type) or RE_GENERATED_IDENTITY.search(column_type):
                    entity.tem_geracao_automatica = True
                    if "identity" not in entity.tipos_invalidos:
                        entity.tipos_invalidos.append("identity")
                    entity.registrar_evidencia("type", caminho, line, "identity")
                elif re.search(r"\bAUTO_INCREMENT\b", column_type, re.IGNORECASE):
                    entity.tem_geracao_automatica = True

    for idx_match in RE_CREATE_INDEX_SQL.finditer(conteudo):
        idx_nome = idx_match.group(1) or ""
        table_name = idx_match.group(2).strip()
        if table_name in temporary_tables:
            continue
        entity = get_entity(entities_by_name, table_name, caminho)
        columns = [column.strip().strip('"').strip("'") for column in idx_match.group(3).split(',')]
        if idx_nome:
            entity.constraints_index.append(idx_nome)
        entity.indices.append({"nome": idx_nome, "colunas": columns})
        entity.registrar_evidencia("indice", caminho, conteudo[:idx_match.start()].count("\n") + 1, idx_nome)

    for match in re.finditer(r"CREATE\s+SEQUENCE\s+([A-Za-z_][\w$#]*)", conteudo, re.IGNORECASE):
        sequence = match.group(1)
        table_name = sequence[4:] if sequence.lower().startswith("seq_") else sequence
        entity = get_entity(entities_by_name, table_name, caminho)
        entity.tem_sequence = True
        entity.sequencias_encontradas.append(sequence)
        entity.registrar_evidencia("sequence", caminho, conteudo[:match.start()].count("\n") + 1, sequence)

    return list(entities_by_name.values())


def enrich_entities_with_release_scripts(entities: dict[str, Entity]):
    if not entities:
        return

    repo_root = Path(__file__).resolve().parents[3]
    siglas = set()

    for nome_tabela in entities:
        match = re.match(r'^md_([a-z]+)_', nome_tabela)
        if match:
            siglas.add(match.group(1))

    for sigla in sorted(siglas):
        for script_relpath in (
            f"fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_{sigla}.php",
            f"fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_{sigla}.php",
        ):
            script_path = repo_root / script_relpath
            if not script_path.is_file():
                continue

            for extra in audit_file(str(script_path)):
                if extra.nome_tabela in entities:
                    merge_entity(entities[extra.nome_tabela], extra)


# ═══════════════════════════════════════════════════════════════
# VALIDATORS: aplicam as 15 regras
# ═══════════════════════════════════════════════════════════════

def validar_entity(entity: Entity) -> tuple[list, list]:
    erros = []
    avisos = []

    tbl = entity.nome_tabela
    is_sequence_table = tbl.startswith("seq_")

    if not is_sequence_table and not re.match(r'^md_[a-z]+_[a-z_][a-z0-9_]*$', tbl):
        erros.append({
            "codigo": "E001", "regra": "DB01",
            "mensagem": f"Nome de tabela '{tbl}' nao segue padrao md_<sigla>_<entidade>",
            "remedio": "Usar formato: md_<sigla>_<entidade> (ex: md_ri_restaurante)",
            "base": "Manual SEI MD §Tabela"
        })

    # DB02: N:N com _rel_. A evidencia estrutural e PK composta apenas por FKs.
    fks = entity.fks
    pk_columns = entity.pk_colunas or ([entity.pk_coluna] if entity.pk_coluna else [])
    fk_columns = {
        normalize_column_ref(fk.get("coluna_sql") or fk["coluna"]).lower()
        for fk in fks
        if fk.get("coluna_sql") or fk.get("coluna")
    }
    pk_e_fk_composta = (
        len(pk_columns) >= 2
        and len(fk_columns) >= 2
        and {normalize_column_ref(column).lower() for column in pk_columns}.issubset(fk_columns)
    )
    if pk_e_fk_composta and '_rel_' not in tbl:
        erros.append({
            "codigo": "E002", "regra": "DB02",
            "mensagem": f"Tabela '{tbl}' tem 2+ FKs mas nome nao usa _rel_ (possivel N:N sem padrao)",
            "remedio": "Renomear para md_<sigla>_rel_<a>_<b>",
            "base": "Manual SEI MD §Tabela"
        })

    # DB03: limite 26 chars para tabela e coluna
    # seq_* table > 26: apenas aviso (W008), pois a restricao Oracle (30) e para a seq em si
    if len(tbl) > 26:
        if is_sequence_table:
            target = erros if len(tbl) > 30 else avisos
            target.append({
                "codigo": "E003" if len(tbl) > 30 else "W008", "regra": "DB03",
                "mensagem": f"Sequence table '{tbl}' tem {len(tbl)} chars (max 30 Oracle).",
                "remedio": "Encurtar a tabela funcional para que seq_<nome> tenha no maximo 30 caracteres",
                "base": "Manual SEI MD §Regras Gerais",
            })
        else:
            erros.append({
                "codigo": "E003", "regra": "DB03",
                "mensagem": f"Tabela '{tbl}' excede 26 caracteres ({len(tbl)}). "
                            f"Regra: tabela funcional deve ter <= 26 para acomodar prefixo seq_ (max 30 no Oracle).",
                "remedio": "Encurtar nome (ex: md_ri_tp_ctrl_demanda)",
                "base": "Manual SEI MD §Regras Gerais"
            })

    names_with_limits = []
    names_with_limits.extend(("coluna", column["nome"], 26) for column in entity.colunas)
    names_with_limits.extend(("indice", index.get("nome", ""), 30) for index in entity.indices)
    names_with_limits.extend(("indice", name, 30) for name in entity.constraints_index)
    names_with_limits.extend(("constraint FK", name, 30) for name in entity.constraints_fk)
    names_with_limits.extend(("constraint AK", name, 30) for name in entity.constraints_ak)
    if entity.constraint_pk:
        names_with_limits.append(("constraint PK", entity.constraint_pk, 30))
    names_with_limits.extend(("sequence", name, 30) for name in entity.sequencias_encontradas)
    seen_limited_names = set()
    for kind, name, limit in names_with_limits:
        key = (kind, name)
        if not name or key in seen_limited_names:
            continue
        seen_limited_names.add(key)
        if len(name) > limit:
            issue = {
                "codigo": "E003", "regra": "DB03",
                "mensagem": f"Nome de {kind} '{name}' excede {limit} caracteres ({len(name)})",
                "remedio": f"Encurtar o nome de {kind} para no maximo {limit} caracteres",
                "base": "Manual SEI MD §Regras Gerais",
            }
            evidence_type = "constraint" if kind.startswith("constraint") else kind
            issue.update(entity.obter_evidencia(evidence_type, name))
            erros.append(issue)

    # DB04: somente PK simples com evidencia de geracao automatica exige nome exato.
    if len(pk_columns) == 1 and (entity.pk_tipo == "sequencial" or entity.tem_sequence or entity.tem_geracao_automatica) and entity.pk_coluna != f"id_{tbl}":
        issue = {
            "codigo": "E004", "regra": "DB04",
            "mensagem": f"PK '{entity.pk_coluna}' nao corresponde exatamente a 'id_{tbl}'",
            "remedio": f"Renomear para id_{tbl}",
            "base": "Manual SEI MD §Colunas"
        }
        issue.update(entity.obter_evidencia("pk", entity.pk_coluna))
        erros.append(issue)
    # DB05: a constraint identifica a tabela proprietaria e a referencia.
    for constraint in dict.fromkeys(entity.constraints_fk):
        if not re.fullmatch(r'fk_md_[a-z0-9]+(?:_[a-z0-9]+)*', constraint):
            issue = {
                "codigo": "E005", "regra": "DB05",
                "mensagem": f"FK constraint '{constraint}' nao usa snake_case com prefixo fk_md_",
                "remedio": "Renomear a constraint para fk_md_<sigla>_<entidade>_<referencia>",
                "base": "Manual SEI MD §Chave Estrangeira"
            }
            issue.update(entity.obter_evidencia("constraint", constraint))
            erros.append(issue)
        else:
            relations = [relation for relation in entity.fk_constraints if relation["nome"] == constraint]
            referenced_tables = [relation["tabela_ref"] for relation in relations]
            if not referenced_tables:
                referenced_tables = [fk["tabela_ref_base"] for fk in entity.fks]
            compatible = identifier_mentions_table(constraint, tbl) and any(
                identifier_mentions_table(constraint, table_ref)
                for table_ref in referenced_tables
            )
            if compatible or not referenced_tables:
                continue
            issue = {
                "codigo": "E005", "regra": "DB05",
                "mensagem": f"FK constraint '{constraint}' nao identifica a entidade proprietaria e a referencia",
                "remedio": "Incluir abreviacoes reconheciveis da tabela proprietaria e da tabela referenciada",
                "base": "Manual SEI MD §Chave Estrangeira"
            }
            issue.update(entity.obter_evidencia("constraint", constraint))
            erros.append(issue)

    # DB06: sin_ativo em exclusao logica
    if entity.tem_exclusao_logica:
        tem_sin_ativo = any(
            col['nome'].lower() == 'sin_ativo'
            for col in entity.colunas
        )
        if not tem_sin_ativo:
            erros.append({
                "codigo": "E006", "regra": "DB06",
                "mensagem": f"Entidade tem configurarExclusaoLogica() mas sem coluna 'sin_ativo'",
                "remedio": "Adicionar coluna sin_ativo char(1) default 'S'",
                "base": "Manual SEI MD §Colunas"
            })

    # DB07: constraint PK pk_<nome>
    if entity.constraint_pk and not re.match(r'^pk_md_\w+_\w+$', entity.constraint_pk):
        issue = {
            "codigo": "E007", "regra": "DB07",
            "mensagem": f"PK constraint '{entity.constraint_pk}' nao segue padrao pk_<nome>",
            "remedio": "Usar formato: pk_md_<sigla>_<entidade>",
            "base": "Manual SEI MD §Chave Primária"
        }
        issue.update(entity.obter_evidencia("constraint", entity.constraint_pk))
        erros.append(issue)

    # DB08: tipos SQL-99 e bigint em contextos nao apropriados
    invalid_types = list(entity.tipos_invalidos)
    if entity.tem_text and "text" not in invalid_types:
        invalid_types.append("text")
    for tipo in invalid_types:
        issue = {
            "codigo": "E008", "regra": "DB08",
            "mensagem": f"Tipo ou estrategia '{tipo}' nao e permitido em modulo SEI (serial, identity, money, text)",
            "remedio": "Usar tipo portavel: integer, numeric, varchar, char",
            "base": "Manual SEI MD §Tipos de Dados"
        }
        issue.update(entity.obter_evidencia("type", tipo))
        erros.append(issue)

    for related_column in entity.colunas_relacionadas:
        if not re.fullmatch(r'[a-z][a-z0-9_]*(?:\.[a-z][a-z0-9_]*)?', related_column):
            issue = {
                "codigo": "E008", "regra": "DB08",
                "mensagem": f"Coluna SQL relacionada '{related_column}' nao usa snake_case literal",
                "remedio": "Usar coluna literal em snake_case, opcionalmente qualificada por alias",
                "base": "Manual SEI MD §Tipos de Dados"
            }
            issue.update(entity.obter_evidencia("related", related_column))
            erros.append(issue)

    if entity.tem_bigint and entity.pk_tipo == "sequencial":
        pk_name = entity.pk_coluna or ""
        if pk_name and "bigint" not in pk_name.lower() and entity.pk_tipo != "informado":
            issue = {
                "codigo": "E008b", "regra": "DB08",
                "mensagem": f"Coluna PK '{pk_name}' usa bigint com tipo sequencial, verificar se e intencional",
                "remedio": "Para PK sequencial usar tipoNumero() (integer), nao tipoNumeroGrande() (bigint)",
                "base": "InfraMetaBD.php tipoNumero() / tipoNumeroGrande()"
            }
            issue.update(entity.obter_evidencia("pk", pk_name))
            erros.append(issue)

    # DB09: indice em FK
    for fk in entity.fks:
        fk_coluna_sql = fk.get("coluna_sql")
        if fk_coluna_sql is None:
            continue

        fk_nome = f"fk_{tbl}_{fk['tabela_ref']}"
        tem_indice = any(
            fk_coluna_sql in indice.get("colunas", [])
            for indice in entity.indices
        )
        if not tem_indice:
            tem_indice = any(
                idx == fk_nome or (idx.startswith('i') and '_' in idx)
                for idx in entity.constraints_index
            )
        if not tem_indice:
            issue = {
                "codigo": "W001", "regra": "DB09",
                "mensagem": f"FK '{fk_coluna_sql}' sem indice explicito",
                "remedio": "Criar indice para FK (i01_ ou mesmo nome da FK)",
                "base": "Manual SEI MD §Índices"
            }
            issue.update(entity.obter_evidencia("fk", fk_coluna_sql))
            avisos.append(issue)

    # DB10: nome de sequence
    if entity.tem_sequence:
        nomes_seq = list(entity.sequencias_encontradas)
        if entity.constraint_pk:
            nomes_seq.append(entity.constraint_pk)
        tem_seq_naming = any(re.match(r'^md_\w+$', s) or re.match(r'^seq_\w+$', s) for s in nomes_seq if s)
        if not tem_seq_naming:
            avisos.append({
                "codigo": "W002", "regra": "DB10",
                "mensagem": "Sequence detectada mas nome pode nao seguir padrao seq_<nome>",
                "remedio": "Usar formato: seq_<nome> (sem prefixo md_)",
                "base": "Manual SEI MD §Sequências"
            })

    # DB11: constraint AK
    for ak in entity.constraints_ak:
        if not re.match(r'^ak_md_\w+', ak):
            issue = {
                "codigo": "W003", "regra": "DB11",
                "mensagem": f"AK/Unique constraint '{ak}' pode nao seguir padrao ak_<nome>_<campos>",
                "remedio": "Usar formato: ak_md_<sigla>_<entidade>_<campos>",
                "base": "Manual SEI MD §Chave Alternativa"
            }
            issue.update(entity.obter_evidencia("constraint", ak))
            avisos.append(issue)

    # DB12: comentarios/docblock
    if not entity.tem_docblock and not entity.arquivos[0].endswith('.sql'):
        avisos.append({
            "codigo": "W004", "regra": "DB12",
            "mensagem": f"DTO sem docblock com @table/@column descritivos",
            "remedio": "Adicionar docblock com @table e @column no DTO",
            "base": "Manual SEI MD §Regras Gerais"
        })

    # DB13: sem verbos
    verbos = ['criar', 'gerar', 'adicionar', 'inserir', 'remover', 'excluir', 'atualizar', 'alterar', 'processar', 'executar', 'realizar', 'efetuar']
    for v in verbos:
        if tbl.startswith(f'md_') and v in tbl.split('_'):
            avisos.append({
                "codigo": "W005", "regra": "DB13",
                "mensagem": f"Nome de tabela '{tbl}' contem verbo '{v}'",
                "remedio": "Usar substantivo no nome da tabela",
                "base": "Manual SEI MD §Tabela"
            })

    # DB14: singular
    partes = tbl.split('_')
    if partes[-1] and partes[-1][-1] == 's' and partes[-1] not in ['sin', 'sta', 'dth', 'dta', 'din']:
        avisos.append({
            "codigo": "W006", "regra": "DB14",
            "mensagem": f"Nome de tabela '{tbl}' esta no plural",
            "remedio": "Usar singular: {partes[-1][:-1]}",
            "base": "Manual SEI MD §Regras Gerais"
        })

    # DB15: formato min + sublinhado
    if not is_sequence_table and not re.match(r'^md_[a-z]+_[a-z_]+$', tbl):
        if not any(e['codigo'] == 'E001' for e in erros):
            avisos.append({
                "codigo": "W007", "regra": "DB15",
                "mensagem": f"Nome '{tbl}' pode nao seguir formato: minusculas + sublinhado + sem preposicoes",
                "remedio": "Usar apenas minusculas, _ para separar, sem preposicoes",
                "base": "Manual SEI MD §Regras Gerais"
            })

    evidence_by_rule = {
        "DB02": "pk",
        "DB03": "coluna",
        "DB04": "pk",
        "DB05": "constraint",
        "DB06": "coluna",
        "DB07": "constraint",
        "DB08": "related" if entity.colunas_relacionadas else "type",
        "DB09": "fk",
        "DB10": "sequence",
        "DB11": "constraint",
    }
    for issue in erros + avisos:
        if "arquivo" not in issue:
            issue.update(entity.obter_evidencia(evidence_by_rule.get(issue["regra"], "tabela")))

    return erros, avisos


# ═══════════════════════════════════════════════════════════════
# FORMATTERS: output
# ═══════════════════════════════════════════════════════════════

def formatar_markdown(results: list, stats: dict, verdict: str) -> str:
    sep = "━" * 50
    sep2 = "━" * 58

    linhas = [
        f" {SKILL_NAME} v{VERSION}",
        sep,
    ]

    all_errors = []
    for r in results:
        for e in r.get("erros", []):
            all_errors.append({**e, "entidade": r["entidade"]})

    if all_errors:
        linhas.append("\n BLOQUEIOS")
        for e in all_errors:
            linhas.append(f"  ✗ {e['entidade']}: {e['codigo']} - {e['mensagem']}")
        linhas.append(sep)

    for r in results:
        entidade = r["entidade"]
        status_icon = "✓" if r["status"] == "PASS" else ("✗" if r["status"] == "BLOCK" else "⚠")

        linhas.append(f"\n📋 {entidade}")
        if r["arquivos"]:
            linhas.append(f"   Arquivos: {', '.join(r['arquivos'])}")

        for e in r["erros"]:
            linhas.append(f"\n   ✗ {e['codigo']} - {e['regra']}")
            linhas.append(f"     {e['mensagem']} [{e.get('arquivo', '?')}:{e.get('linha', '?')}]")
            linhas.append(f"     Remedio: {e['remedio']}")
            linhas.append(f"     Base: {e['base']}")

        for a in r["avisos"]:
            linhas.append(f"\n   ⚠ {a['codigo']} - {a['regra']}")
            linhas.append(f"     {a['mensagem']} [{a.get('arquivo', '?')}:{a.get('linha', '?')}]")
            linhas.append(f"     Remedio: {a['remedio']}")

        if not r["erros"] and not r["avisos"]:
            linhas.append("\n   ✓ conformidade total para todas as regras.")

        linhas.append(sep)

    labels = {"BLOCK": "BLOCK, corrija erros antes de prosseguir",
              "WARN": "WARN, avisos presentes, erros zero",
              "PASS": "PASS, conformidade total"}

    linhas.append(f"\nRESUMO")
    linhas.append(f"  Entidades auditadas: {stats['entidades']}")
    linhas.append(f"  Erros (bloqueantes):  {stats['erros']}")
    linhas.append(f"  Avisos (nao bloqueantes): {stats['avisos']}")
    linhas.append(f"  Nota de conformidade: {stats['nota']}/100")
    linhas.append(f"\n  Veredito: {labels.get(verdict, verdict)}")

    return "\n".join(linhas)


def formatar_json(results: list, stats: dict, verdict: str, input_info: dict) -> dict:
    return {
        "skill": SKILL_NAME,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "input": input_info,
        "results": results,
        "stats": stats,
        "verdict": verdict
    }


def calcular_stats(results: list) -> dict:
    total_erros = sum(len(r["erros"]) for r in results)
    total_avisos = sum(len(r["avisos"]) for r in results)
    max_score = len(results) * 100
    earned = sum(
        100 - (len(r["erros"]) * 20) - (len(r["avisos"]) * 5)
        for r in results
    )
    nota = max(0, int(earned / max(1, len(results))))

    return {
        "entidades": len(results),
        "erros": total_erros,
        "avisos": total_avisos,
        "nota": nota
    }


def determinar_verdict(results: list) -> str:
    if not results:
        return "BLOCK"
    tem_erro = any(r["erros"] for r in results)
    tem_aviso = any(r["avisos"] for r in results)

    if tem_erro:
        return "BLOCK"
    elif tem_aviso:
        return "WARN"
    else:
        return "PASS"


def audit_file(caminho: str) -> list[Entity]:
    ext = Path(caminho).suffix.lower()
    with open(caminho, "r", encoding="utf-8", errors="replace") as f:
        conteudo = f.read()

    if ext == ".php":
        entity = parse_php_dto(caminho, conteudo)
        if entity:
            return [entity]
        if os.path.basename(caminho).endswith("BD.php"):
            entities = {}
            parse_php_bd(caminho, conteudo, entities)
            if entities:
                return list(entities.values())
        ddl_entities = parse_php_release_script(caminho, conteudo)
        if ddl_entities:
            return ddl_entities
    elif ext in (".sql", ".ddl"):
        return parse_ddl(caminho, conteudo)

    return []


def audit_content(content: str, source_type: str = "raw") -> list[Entity]:
    if source_type == "php":
        entity = parse_php_dto("input", content)
        if entity:
            return [entity]
        return parse_php_release_script("input", content)
    elif source_type in ("sql", "ddl"):
        return parse_ddl("input", content)
    return []


def run_audit(input_path: str, input_type: str = None, mode: str = "adhoc") -> tuple[list, dict, str]:
    input_info = {"type": input_type or "unknown", "path": input_path, "mode": mode}
    entities = {}

    def store(entity):
        if not entity.nome_tabela:
            return
        if entity.nome_tabela in entities:
            merge_entity(entities[entity.nome_tabela], entity)
        else:
            entities[entity.nome_tabela] = entity

    if os.path.isfile(input_path):
        if input_type:
            with open(input_path, "r", encoding="utf-8", errors="replace") as handle:
                found = audit_content(handle.read(), input_type)
        else:
            found = audit_file(input_path)
        for e in found:
            store(e)

    elif os.path.isdir(input_path):
        dto_dir = os.path.join(input_path, "dto")
        bd_dir = os.path.join(input_path, "bd")

        # If the input itself is a DTO/BD directory, audit it directly.
        # For module roots, prefer dto/ and bd/ subdirectories even when the root
        # also contains PHP pages or integration classes.
        if not os.path.isdir(dto_dir) and os.path.isdir(input_path) and any(f.endswith(".php") for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))):
            dto_dir = input_path
            bd_dir = None

        if os.path.isdir(dto_dir):
            for f in os.listdir(dto_dir):
                fpath = os.path.join(dto_dir, f)
                if f.endswith(".php") and os.path.isfile(fpath):
                    found = audit_file(fpath)
                    for e in found:
                        store(e)

        if bd_dir and os.path.isdir(bd_dir):
            for f in os.listdir(bd_dir):
                if f.endswith(".php"):
                    caminho = os.path.join(bd_dir, f)
                    with open(caminho, "r", encoding="utf-8", errors="replace") as fh:
                        conteudo = fh.read()
                    parse_php_bd(caminho, conteudo, entities)

        enrich_entities_with_release_scripts(entities)

    elif "," in input_path:
        for path in input_path.split(","):
            p = path.strip()
            if os.path.exists(p):
                found = audit_file(p)
                for e in found:
                    store(e)

    else:
        if input_type in ("php", "sql", "ddl"):
            found = audit_content(input_path, input_type)
            for e in found:
                store(e)

    results = []
    for nome, entity in entities.items():
        erros, avisos = validar_entity(entity)
        status = "BLOCK" if erros else ("WARN" if avisos else "PASS")
        results.append({
            "entidade": nome,
            "arquivos": entity.arquivos,
            "erros": erros,
            "avisos": avisos,
            "status": status
        })

    stats = calcular_stats(results)
    verdict = determinar_verdict(results)
    input_info["type"] = input_type or ("directory" if os.path.isdir(input_path) else "file")

    return results, stats, verdict, input_info


def main():
    parser = argparse.ArgumentParser(
        description="sei-verificacao-banco-dados: auditor de modelagem de dados SEI/SIP"
    )
    parser.add_argument("--input", required=True, help="Arquivo, diretorio, ou string")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown",
                        help="Formato de saida")
    parser.add_argument("--mode", choices=["adhoc", "pre_generate", "audit", "release_check"],
                        default="adhoc", help="Modo de auditoria")
    parser.add_argument("--type", choices=["php", "sql", "ddl"],
                        help="Forca tipo de input (php ou sql)")
    parser.add_argument("--exit-code", action="store_true",
                        help="Retorna exit code ao inves de imprimir output")

    args = parser.parse_args()

    results, stats, verdict, input_info = run_audit(args.input, args.type, args.mode)

    if args.format == "json":
        output = formatar_json(results, stats, verdict, input_info)
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        output = formatar_markdown(results, stats, verdict)
        print(output)

    if args.exit_code:
        exit_map = {"PASS": 0, "WARN": 1, "BLOCK": 2}
        sys.exit(exit_map.get(verdict, 0))


if __name__ == "__main__":
    main()
