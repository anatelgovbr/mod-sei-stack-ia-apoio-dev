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
# REGEX PATTERNS — PHP (InfraPHP DTO/BD)
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
# REGEX PATTERNS — SQL/DDL
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
# REGRAS — definicao e validadores
# ═══════════════════════════════════════════════════════════════

REGRAS = [
    {
        "id": "R1",
        "nome": "Nome tabela md_<sigla>_<entidade>",
        "severidade": "erro",
        "base": "Manual SEI MD §Tabela",
    },
    {
        "id": "R2",
        "nome": "Relacionamento N:N",
        "severidade": "erro",
        "base": "Manual SEI MD §Tabela",
    },
    {
        "id": "R3",
        "nome": "Limite de 26 caracteres",
        "severidade": "erro",
        "base": "Manual SEI MD §Regras Gerais",
    },
    {
        "id": "R3b",
        "nome": "Tabela funcional sem folga para seq_ (Oracle 30)",
        "severidade": "erro",
        "base": "Manual SEI MD §Regras Gerais / Sequências",
    },
    {
        "id": "R4",
        "nome": "PK sequencial",
        "severidade": "erro",
        "base": "Manual SEI MD §Colunas",
    },
    {
        "id": "R5",
        "nome": "FK constraint naming",
        "severidade": "erro",
        "base": "Manual SEI MD §Chave Estrangeira",
    },
    {
        "id": "R6",
        "nome": "sin_ativo em exclusao logica",
        "severidade": "erro",
        "base": "Manual SEI MD §Colunas",
    },
    {
        "id": "R7",
        "nome": "PK constraint naming",
        "severidade": "erro",
        "base": "Manual SEI MD §Chave Primária",
    },
    {
        "id": "R8",
        "nome": "Tipos SQL-99",
        "severidade": "erro",
        "base": "Manual SEI MD §Tipos de Dados",
    },
    {
        "id": "R9",
        "nome": "Indice em FK",
        "severidade": "aviso",
        "base": "Manual SEI MD §Índices",
    },
    {
        "id": "R10",
        "nome": "Sequence naming",
        "severidade": "aviso",
        "base": "Manual SEI MD §Sequências",
    },
    {
        "id": "R11",
        "nome": "AK constraint naming",
        "severidade": "aviso",
        "base": "Manual SEI MD §Chave Alternativa",
    },
    {
        "id": "R12",
        "nome": "Comentarios/Docblock",
        "severidade": "aviso",
        "base": "Manual SEI MD §Regras Gerais",
    },
    {
        "id": "R13",
        "nome": "Sem verbos no nome",
        "severidade": "aviso",
        "base": "Manual SEI MD §Tabela",
    },
    {
        "id": "R14",
        "nome": "Singular",
        "severidade": "aviso",
        "base": "Manual SEI MD §Regras Gerais",
    },
    {
        "id": "R15",
        "nome": "Formato do nome",
        "severidade": "aviso",
        "base": "Manual SEI MD §Regras Gerais",
    },
]


# ═══════════════════════════════════════════════════════════════
# ENTITIES — estruturas extraidas de PHP/DDL
# ═══════════════════════════════════════════════════════════════

class Entity:
    def __init__(self, nome_tabela: str, arquivos: list[str]):
        self.nome_tabela = nome_tabela
        self.arquivos = arquivos
        self.colunas = []
        self.pk_coluna = None
        self.pk_tipo = None
        self.fks = []
        self.tem_exclusao_logica = False
        self.campo_exclusao_logica = None
        self.tem_docblock = False
        self.constraint_pk = None
        self.constraints_fk = []
        self.constraints_ak = []
        self.constraints_index = []
        self.tem_sequence = False
        self.tipos_invalidos = []
        self.sequencias_encontradas = []
        self.tem_bigint = False
        self.tem_blob = False
        self.tem_text = False

    def adicionar_coluna(self, nome: str, tipo: str = None):
        self.colunas.append({"nome": nome, "tipo": tipo})

    def adicionar_fk(self, coluna: str, tabela_ref: str, coluna_ref: str):
        self.fks.append({"coluna": coluna, "tabela_ref": tabela_ref, "coluna_ref": coluna_ref})


# ═══════════════════════════════════════════════════════════════
# PARSERS
# ═══════════════════════════════════════════════════════════════

def parse_php_dto(caminho: str, conteudo: str) -> Optional[Entity]:
    nome_tabela = None
    colunas = []
    pk_coluna = None
    pk_tipo = None
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

    for match_fk in RE_FK.finditer(conteudo):
        attr = match_fk.group(1).strip()
        tabela_ref = match_fk.group(2).strip()
        campo_ref = match_fk.group(3).strip()
        fks.append({"coluna": attr, "tabela_ref": tabela_ref, "coluna_ref": campo_ref})

    for match_exc in RE_EXC_LOGICA.finditer(conteudo):
        tem_exclusao_logica = True
        campo_exclusao_logica = match_exc.group(1).strip()

    if RE_DOCBLOCK_TABLE.search(conteudo):
        tem_docblock = True

    for match_col_rel in RE_COLUNA_RELACIONADA.finditer(conteudo):
        pass

    entity = Entity(nome_tabela, [caminho])
    entity.colunas = colunas
    entity.pk_coluna = pk_coluna_sql
    entity.pk_tipo = pk_tipo
    entity.fks = fks
    entity.tem_exclusao_logica = tem_exclusao_logica
    entity.campo_exclusao_logica = campo_exclusao_logica
    entity.tem_docblock = tem_docblock

    return entity


def parse_php_bd(caminho: str, conteudo: str, entities: dict):
    has_sequence = RE_INFRA_SEQUENCIA.search(conteudo) is not None

    for nome_tabela, entity in entities.items():
        if has_sequence:
            entity.tem_sequence = True

    fk_pattern = re.compile(r'fk_md_\w+')
    pk_pattern = re.compile(r'pk_md_\w+')
    ak_pattern = re.compile(r'ak_md_\w+(?:_\w+)*')
    index_pattern = re.compile(r'(?:fk_md_\w+|i\d+_\w+)')

    for fk_match in fk_pattern.finditer(conteudo):
        constraint_nome = fk_match.group(0)
        if constraint_nome not in entities[nome_tabela].constraints_fk:
            entities[nome_tabela].constraints_fk.append(constraint_nome)

    for pk_match in pk_pattern.finditer(conteudo):
        constraint_nome = pk_match.group(0)
        pk_val = entities[nome_tabela].constraint_pk
        if pk_val is None or pk_val == "" or pk_val == "pk_md_" + nome_tabela.split("_")[-1]:
            entities[nome_tabela].constraint_pk = constraint_nome

    for ak_match in ak_pattern.finditer(conteudo):
        constraint_nome = ak_match.group(0)
        if constraint_nome not in entities[nome_tabela].constraints_ak:
            entities[nome_tabela].constraints_ak.append(constraint_nome)

    for idx_match in index_pattern.finditer(conteudo):
        constraint_nome = idx_match.group(0)
        if constraint_nome not in entities[nome_tabela].constraints_index:
            entities[nome_tabela].constraints_index.append(constraint_nome)


def parse_php_release_script(caminho: str, conteudo: str) -> list[Entity]:
    if "CREATE TABLE" not in conteudo.upper():
        return []

    entities = []
    create_pattern = re.compile(
        r'CREATE\s+TABLE\s+(\w+)\s*\((.+?)\)\s*[\'"]',
        re.DOTALL | re.IGNORECASE
    )
    for match in create_pattern.finditer(conteudo):
        nome_tabela = match.group(1).strip()

        if nome_tabela.lower() == "sei_teste":
            continue

        is_sequence_table = nome_tabela.startswith("seq_")

        entity = Entity(nome_tabela, [caminho])
        # Release scripts are not DTOs, so docblock checks do not apply.
        entity.tem_docblock = True

        if is_sequence_table:
            entity.tem_sequence = True
            entity.sequencias_encontradas.append(nome_tabela[4:])
            seq_pat = re.compile(r'seq_(\w+)', re.IGNORECASE)
            for sm in seq_pat.finditer(nome_tabela):
                if sm.group(1) not in entity.sequencias_encontradas:
                    entity.sequencias_encontradas.append(sm.group(1))
            entities.append(entity)
            continue

        pk_match = RE_PRIMARY_KEY.search(match.group(2))
        if pk_match:
            pk_cols = pk_match.group(1).strip()
            entity.pk_coluna = pk_cols.strip('"').strip("'")
            entity.pk_tipo = "sequencial"

        fk_pattern = re.compile(
            r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)\s*\(([^)]+)\)',
            re.IGNORECASE
        )
        for fk_m in fk_pattern.finditer(match.group(2)):
            col = fk_m.group(1).strip().strip('"').strip("'")
            ref_tbl = fk_m.group(2).strip()
            ref_col = fk_m.group(3).strip().strip('"').strip("'")
            entity.adicionar_fk(col, ref_tbl, ref_col)
            entity.constraints_fk.append(f"fk_{nome_tabela}_{ref_tbl}")

        if RE_BIGINT.search(match.group(2)):
            entity.tem_bigint = True
        if RE_BLOB2.search(match.group(2)):
            entity.tem_blob = True
        if RE_TEXT2.search(match.group(2)):
            entity.tem_text = True
        if RE_SERIAL2.search(match.group(2)):
            entity.tipos_invalidos.append("serial")
        if RE_MONEY2.search(match.group(2)):
            entity.tipos_invalidos.append("money")

        col_pat = re.compile(
            r'(\w+)\s+(?:varchar\s*\(\s*\d+\s*\)|var?char\s*\(\s*\d+\s*\)|'
            r'numeric\s*\(\s*\d+\s*(?:,\s*\d+)?\s*\)|'
            r'(?:big|small|tiny)?\s*int(?:eger)?\s*(?:\(\s*\d+\s*\))?|'
            r'date|timestamp|datetime|boolean|clob|blob|text|money|decimal)',
            re.IGNORECASE
        )
        for cm in col_pat.finditer(match.group(2)):
            entity.adicionar_coluna(cm.group(1).strip(), "")

        entities.append(entity)

    return entities


def parse_ddl(caminho: str, conteudo: str) -> list[Entity]:
    entities_by_name = {}

    for match_tbl in RE_CREATE_TABLE.finditer(conteudo):
        nome_tabela = match_tbl.group(1).strip()
        corpo = match_tbl.group(2)

        if nome_tabela not in entities_by_name:
            entities_by_name[nome_tabela] = Entity(nome_tabela, [caminho])

        entity = entities_by_name[nome_tabela]

        pk_match = RE_PRIMARY_KEY.search(corpo)
        if pk_match:
            pk_cols = pk_match.group(1).strip()
            entity.pk_coluna = pk_cols.strip('"').strip("'")
            entity.pk_tipo = "sequencial"

        fk_pattern = re.compile(r'FOREIGN\s+KEY\s*\(([^)]+)\)\s*REFERENCES\s+(\w+)\s*\(([^)]+)\)', re.IGNORECASE)
        for fk_match in fk_pattern.finditer(corpo):
            fk_coluna = fk_match.group(1).strip().strip('"').strip("'")
            fk_tabela = fk_match.group(2).strip()
            fk_col_ref = fk_match.group(3).strip().strip('"').strip("'")
            entity.adicionar_fk(fk_coluna, fk_tabela, fk_col_ref)
            entity.constraints_fk.append(f"fk_{nome_tabela}_{fk_tabela}")

        unique_pattern = re.compile(r'UNIQUE\s+(?:KEY\s+)?(\w+)?\s*\(([^)]+)\)', re.IGNORECASE)
        for unique_match in unique_pattern.finditer(corpo):
            ak_name = unique_match.group(1) or f"ak_{nome_tabela}"
            ak_cols = unique_match.group(2).strip().strip('"').strip("'")
            entity.constraints_ak.append(f"{ak_name}_{ak_cols}")

        for fk_match in RE_FOREIGN_KEY_SQL.finditer(corpo):
            fk_coluna = fk_match.group(1).strip().strip('"').strip("'")
            fk_tabela = fk_match.group(2).strip()
            fk_col_ref = fk_match.group(3).strip().strip('"').strip("'")
            entity.adicionar_fk(fk_coluna, fk_tabela, fk_col_ref)
            if f"fk_{nome_tabela}_{fk_tabela}" not in entity.constraints_fk:
                entity.constraints_fk.append(f"fk_{nome_tabela}_{fk_tabela}")

        if RE_BIGINT.search(corpo):
            entity.tem_bigint = True
        if RE_BLOB2.search(corpo):
            entity.tem_blob = True
        if RE_TEXT2.search(corpo):
            entity.tem_text = True
        if RE_SERIAL2.search(corpo):
            entity.tipos_invalidos.append("serial")
        if RE_MONEY2.search(corpo):
            entity.tipos_invalidos.append("money")

        col_pattern = re.compile(
            r'(\w+)\s+(?:varchar\s*\(\s*\d+\s*\)|var?char\s*\(\s*\d+\s*\)|'
            r'numeric\s*\(\s*\d+\s*(?:,\s*\d+)?\s*\)|'
            r'(?:big|small|tiny)?\s*int(?:eger)?\s*(?:\(\s*\d+\s*\))?|'
            r'date|timestamp|datetime|boolean|clob|blob|text|'
            r'money|decimal\s*\(\s*\d+\s*(?:,\s*\d+)?\s*\))',
            re.IGNORECASE
        )
        for col_match in col_pattern.finditer(corpo):
            col_nome = col_match.group(1).strip()
            col_tipo = col_match.group(2).strip() if col_match.lastindex else ""
            entity.adicionar_coluna(col_nome, col_tipo)

    seq_pattern = re.compile(r'seq_(\w+)', re.IGNORECASE)
    for seq_match in seq_pattern.finditer(conteudo):
        seq_nome = seq_match.group(1).strip()
        if seq_nome not in entity.sequencias_encontradas:
            entity.sequencias_encontradas.append(seq_nome)
        entity.tem_sequence = True

    for idx_match in RE_CREATE_INDEX_SQL.finditer(conteudo):
        idx_nome = idx_match.group(1) or ""
        tbl_idx = idx_match.group(2).strip()
        cols_idx = idx_match.group(3).strip()
        if tbl_idx in entities_by_name:
            entidades_afetadas = [entities_by_name[tbl_idx]]
        else:
            entidades_afetadas = list(entities_by_name.values())
        for ent in entidades_afetadas:
            if idx_nome and idx_nome not in ent.constraints_index:
                ent.constraints_index.append(idx_nome)

    return list(entities_by_name.values())


# ═══════════════════════════════════════════════════════════════
# VALIDATORS — aplicam as 15 regras
# ═══════════════════════════════════════════════════════════════

def validar_entity(entity: Entity) -> tuple[list, list]:
    erros = []
    avisos = []

    tbl = entity.nome_tabela
    is_sequence_table = tbl.startswith("seq_")

    if not is_sequence_table and not re.match(r'^md_[a-z]+_[a-z_][a-z0-9_]*$', tbl):
        erros.append({
            "codigo": "E001", "regra": 1,
            "mensagem": f"Nome de tabela '{tbl}' nao segue padrao md_<sigla>_<entidade>",
            "remedio": "Usar formato: md_<sigla>_<entidade> (ex: md_ri_restaurante)",
            "base": "Manual SEI MD §Tabela"
        })

    # R2 — N:N com _rel_
    # N:N real: 2+ FKs E PK composta por múltiplas colunas FK
    fks = entity.fks
    pk_e_fk_composta = (
        len(fks) >= 2 and
        len(entity.colunas) <= 4 and
        entity.pk_coluna and
        any(fk["coluna"].lower().replace("_", "").isalpha() for fk in fks)
    )
    if pk_e_fk_composta and '_rel_' not in tbl:
        erros.append({
            "codigo": "E002", "regra": 2,
            "mensagem": f"Tabela '{tbl}' tem 2+ FKs mas nome nao usa _rel_ (possivel N:N sem padrao)",
            "remedio": "Renomear para md_<sigla>_rel_<a>_<b>",
            "base": "Manual SEI MD §Tabela"
        })

    # R3 — limite 26 chars (para seq_* e funcional)
    # seq_* table > 26: apenas aviso (W008), pois a restricao Oracle (30) e para a seq em si
    if len(tbl) > 26:
        if is_sequence_table:
            avisos.append({
                "codigo": "W008", "regra": 3,
                "mensagem": f"Sequence table '{tbl}' tem {len(tbl)} chars (max 30 Oracle). "
                            f"Nao bloqueia, mas indica que a tabela funcional relacionada "
                            f"esta com nome longo demais.",
                "remedio": "Considerar encurtar a tabela funcional para <= 26 chars para folga ao seq_",
                "base": "Manual SEI MD §Regras Gerais"
            })
        else:
            erros.append({
                "codigo": "E003", "regra": 3,
                "mensagem": f"Tabela '{tbl}' excede 26 caracteres ({len(tbl)}). "
                            f"Regra: tabela funcional deve ter <= 26 para acomodar prefixo seq_ (max 30 no Oracle).",
                "remedio": "Encurtar nome (ex: md_ri_tp_ctrl_demanda)",
                "base": "Manual SEI MD §Regras Gerais"
            })

    # R3b — folga para seq_ (tabela funcional com exatamente 26 chars = no room for seq_)
    if not is_sequence_table and len(tbl) == 26:
        avisos.append({
            "codigo": "W009", "regra": "3b",
            "mensagem": f"Tabela '{tbl}' tem 26 chars (maximo). Nao ha folga para prefixo seq_ "
                        f"(seq_+'{tbl}' = 30 = limite Oracle). Funciona, mas nao aceita crescimento.",
            "remedio": "Se possivel, encurtar para < 26 chars para folga futura.",
            "base": "Manual SEI MD §Regras Gerais / Sequências"
        })

    # R4 — PK sequencial id_md_<sigla>_<entidade>
    if entity.pk_tipo == "sequencial" and entity.pk_coluna:
        if not re.match(r'^id_md_\w+_\w+$', entity.pk_coluna):
            erros.append({
                "codigo": "E004", "regra": 4,
                "mensagem": f"PK '{entity.pk_coluna}' nao segue padrao id_md_<sigla>_<entidade>",
                "remedio": f"Renomear para id_{tbl}",
                "base": "Manual SEI MD §Colunas"
            })

    # R5 — FK constraint naming
    for fk in entity.fks:
        fk_nome_esperado = f"fk_{tbl}_{fk['tabela_ref']}"
        fk_nome_encontrado = None
        for cfk in entity.constraints_fk:
            if fk['coluna'].lower() in cfk.lower() or fk['tabela_ref'].lower() in cfk.lower():
                fk_nome_encontrado = cfk
                break
        if fk_nome_encontrado and not re.match(r'^fk_md_\w+_\w+_\w+$', fk_nome_encontrado):
            erros.append({
                "codigo": "E005", "regra": 5,
                "mensagem": f"FK constraint '{fk_nome_encontrado}' nao segue padrao fk_md_<sigla>_<ent>_<ref>",
                "remedio": f"Renomear para fk_{tbl}_{fk['tabela_ref']}",
                "base": "Manual SEI MD §Chave Estrangeira"
            })

    # R6 — sin_ativo em exclusao logica
    if entity.tem_exclusao_logica:
        tem_sin_ativo = any(
            col['nome'].lower() == 'sin_ativo'
            for col in entity.colunas
        )
        if not tem_sin_ativo:
            erros.append({
                "codigo": "E006", "regra": 6,
                "mensagem": f"Entidade tem configurarExclusaoLogica() mas sem coluna 'sin_ativo'",
                "remedio": "Adicionar coluna sin_ativo char(1) default 'S'",
                "base": "Manual SEI MD §Colunas"
            })

    # R7 — PK constraint pk_<nome>
    if entity.constraint_pk and not re.match(r'^pk_md_\w+_\w+$', entity.constraint_pk):
        erros.append({
            "codigo": "E007", "regra": 7,
            "mensagem": f"PK constraint '{entity.constraint_pk}' nao segue padrao pk_<nome>",
            "remedio": "Usar formato: pk_md_<sigla>_<entidade>",
            "base": "Manual SEI MD §Chave Primária"
        })

    # R8 — tipos SQL-99 + bigint em contextos nao apropriados
    for tipo in entity.tipos_invalidos:
        erros.append({
            "codigo": "E008", "regra": 8,
            "mensagem": f"Tipo '{tipo}' nao e permitido em modulo SEI (serial, money, text)",
            "remedio": "Usar tipo portavel: integer, numeric, varchar, char",
            "base": "Manual SEI MD §Tipos de Dados"
        })

    if entity.tem_bigint and entity.pk_tipo == "sequencial":
        pk_name = entity.pk_coluna or ""
        if pk_name and "bigint" not in pk_name.lower() and entity.pk_tipo != "informado":
            erros.append({
                "codigo": "E008b", "regra": 8,
                "mensagem": f"Coluna PK '{pk_name}' usa bigint com tipo sequencial, verificar se e intencional",
                "remedio": "Para PK sequencial usar tipoNumero() (integer), nao tipoNumeroGrande() (bigint)",
                "base": "InfraMetaBD.php tipoNumero() / tipoNumeroGrande()"
            })

    # R9 — indice em FK
    for fk in entity.fks:
        fk_nome = f"fk_{tbl}_{fk['tabela_ref']}"
        tem_indice = any(
            idx == fk_nome or idx.startswith('i') and '_' in idx
            for idx in entity.constraints_index
        )
        if not tem_indice:
            avisos.append({
                "codigo": "W001", "regra": 9,
                "mensagem": f"FK '{fk['coluna']}' sem indice explicito",
                "remedio": "Criar indice para FK (i01_ ou mesmo nome da FK)",
                "base": "Manual SEI MD §Índices"
            })

    # R10 — sequence naming
    if entity.tem_sequence:
        tem_seq_naming = any(re.match(r'^seq_\w+$', s) for s in [entity.constraint_pk] if s)
        if not tem_seq_naming:
            avisos.append({
                "codigo": "W002", "regra": 10,
                "mensagem": "Sequence detectada mas nome pode nao seguir padrao seq_<nome>",
                "remedio": "Usar formato: seq_<nome> (sem prefixo md_)",
                "base": "Manual SEI MD §Sequências"
            })

    # R11 — AK constraint
    for ak in entity.constraints_ak:
        if not re.match(r'^ak_md_\w+', ak):
            avisos.append({
                "codigo": "W003", "regra": 11,
                "mensagem": f"AK/Unique constraint '{ak}' pode nao seguir padrao ak_<nome>_<campos>",
                "remedio": "Usar formato: ak_md_<sigla>_<entidade>_<campos>",
                "base": "Manual SEI MD §Chave Alternativa"
            })

    # R12 — comentarios/docblock
    if not entity.tem_docblock and not entity.arquivos[0].endswith('.sql'):
        avisos.append({
            "codigo": "W004", "regra": 12,
            "mensagem": f"DTO sem docblock com @table/@column descritivos",
            "remedio": "Adicionar docblock com @table e @column no DTO",
            "base": "Manual SEI MD §Regras Gerais"
        })

    # R13 — sem verbos
    verbos = ['criar', 'gerar', 'adicionar', 'inserir', 'remover', 'excluir', 'atualizar', 'alterar', 'processar', 'executar', 'realizar', 'efetuar']
    for v in verbos:
        if tbl.startswith(f'md_') and v in tbl.split('_'):
            avisos.append({
                "codigo": "W005", "regra": 13,
                "mensagem": f"Nome de tabela '{tbl}' contem verbo '{v}'",
                "remedio": "Usar substantivo no nome da tabela",
                "base": "Manual SEI MD §Tabela"
            })

    # R14 — singular
    partes = tbl.split('_')
    if partes[-1] and partes[-1][-1] == 's' and partes[-1] not in ['sin', 'sta', 'dth', 'dta', 'din']:
        avisos.append({
            "codigo": "W006", "regra": 14,
            "mensagem": f"Nome de tabela '{tbl}' esta no plural",
            "remedio": "Usar singular: {partes[-1][:-1]}",
            "base": "Manual SEI MD §Regras Gerais"
        })

    # R15 — formato min + sublinhado
    if not re.match(r'^md_[a-z]+_[a-z_]+$', tbl):
        if not any(e['codigo'] == 'E001' for e in erros):
            avisos.append({
                "codigo": "W007", "regra": 15,
                "mensagem": f"Nome '{tbl}' pode nao seguir formato: minusculas + sublinhado + sem preposicoes",
                "remedio": "Usar apenas minusculas, _ para separar, sem preposicoes",
                "base": "Manual SEI MD §Regras Gerais"
            })

    return erros, avisos


# ═══════════════════════════════════════════════════════════════
# FORMATTERS — output
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
            linhas.append(f"  ✗ {e['entidade']}: {e['codigo']} — {e['mensagem']}")
        linhas.append(sep)

    for r in results:
        entidade = r["entidade"]
        status_icon = "✓" if r["status"] == "PASS" else ("✗" if r["status"] == "BLOCK" else "⚠")

        linhas.append(f"\n📋 {entidade}")
        if r["arquivos"]:
            linhas.append(f"   Arquivos: {', '.join(r['arquivos'])}")

        for e in r["erros"]:
            linhas.append(f"\n   ✗ {e['codigo']} — R{e['regra']}")
            linhas.append(f"     {e['mensagem']}")
            linhas.append(f"     Remedio: {e['remedio']}")
            linhas.append(f"     Base: {e['base']}")

        for a in r["avisos"]:
            linhas.append(f"\n   ⚠ {a['codigo']} — R{a['regra']}")
            linhas.append(f"     {a['mensagem']}")
            linhas.append(f"     Remedio: {a['remedio']}")

        if not r["erros"] and not r["avisos"]:
            linhas.append("\n   ✓ conformidade total para todas as regras.")

        linhas.append(sep)

    labels = {"BLOCK": "BLOCK — Corrija erros antes de prosseguir",
              "WARN": "WARN — Avisos presentes, erros zero",
              "PASS": "PASS — Conformidade total"}

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
        ddl_entities = parse_php_release_script(caminho, conteudo)
        if ddl_entities:
            return ddl_entities
    elif ext in (".sql", ".ddl"):
        return parse_ddl(caminho, conteudo)

    return []


def audit_content(content: str, source_type: str = "raw") -> list[Entity]:
    if source_type == "php":
        entity = parse_php_dto("input", content)
        return [entity] if entity else []
    elif source_type == "sql":
        return parse_ddl("input", content)
    return []


def run_audit(input_path: str, input_type: str = None, mode: str = "adhoc") -> tuple[list, dict, str]:
    input_info = {"type": input_type or "unknown", "path": input_path, "mode": mode}
    entities = {}

    if os.path.isfile(input_path):
        found = audit_file(input_path)
        for e in found:
            if e.nome_tabela:
                entities[e.nome_tabela] = e

    elif os.path.isdir(input_path):
        dto_dir = os.path.join(input_path, "dto")
        bd_dir = os.path.join(input_path, "bd")

        if os.path.isdir(input_path) and any(f.endswith(".php") for f in os.listdir(input_path) if os.path.isfile(os.path.join(input_path, f))):
            dto_dir = input_path
            bd_dir = None

        if os.path.isdir(dto_dir):
            for f in os.listdir(dto_dir):
                fpath = os.path.join(dto_dir, f)
                if f.endswith(".php") and os.path.isfile(fpath):
                    found = audit_file(fpath)
                    for e in found:
                        if e.nome_tabela:
                            if e.nome_tabela in entities:
                                entities[e.nome_tabela].arquivos.extend(e.arquivos)
                            else:
                                entities[e.nome_tabela] = e

        if bd_dir and os.path.isdir(bd_dir):
            for f in os.listdir(bd_dir):
                if f.endswith(".php"):
                    caminho = os.path.join(bd_dir, f)
                    with open(caminho, "r", encoding="utf-8", errors="replace") as fh:
                        conteudo = fh.read()
                    parse_php_bd(caminho, conteudo, entities)

    elif "," in input_path:
        for path in input_path.split(","):
            p = path.strip()
            if os.path.exists(p):
                found = audit_file(p)
                for e in found:
                    if e.nome_tabela:
                        entities[e.nome_tabela] = e

    else:
        if input_type in ("php", "sql"):
            found = audit_content(input_path, input_type)
            for e in found:
                if e.nome_tabela:
                    entities[e.nome_tabela] = e

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
