#!/usr/bin/env python3

import argparse
import json
import re
import sys
from pathlib import Path
from textwrap import dedent, indent


ROOT = Path(__file__).resolve().parents[3]


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def pascal_case(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_") if part)


def q(text: str) -> str:
    """Escapa texto do contrato para literal PHP ou JavaScript delimitado por aspas simples."""
    return text.replace("\\", "\\\\").replace("'", "\\'")


TEXT_FORBIDDEN = set('"\\<>&')


def validate_display_text(value, where: str) -> None:
    """Texto exibido (singular, plural, rotulo, comentario) sem caracteres que quebram literal PHP, JS ou HTML."""
    if not isinstance(value, str):
        raise ValueError(f"{where} deve ser texto")
    bad = sorted({c for c in value if c in TEXT_FORBIDDEN or ord(c) < 32})
    if bad:
        raise ValueError(f"{where} contem caractere nao permitido em texto exibido: {' '.join(repr(c) for c in bad)}")
    if "*/" in value:
        raise ValueError(f"{where} nao pode conter '*/' (fecha o docblock gerado)")


def strip_common_prefixes(column_name: str) -> str:
    for prefix in ("num_", "str_", "din_", "dbl_", "dta_", "dth_"):
        if column_name.startswith(prefix):
            return column_name[len(prefix) :]
    return column_name


def dto_prefix(column: dict) -> str:
    column_type = column["tipoBanco"]
    column_name = column.get("nome", "")
    if column_type in {"int", "integer"}:
        return "Num"
    if column_type == "varchar":
        return "Str"
    if column_type in {"date", "datetime", "timestamp"}:
        return "Dth" if column_name.startswith("dth_") else "Dta"
    if column_type == "char":
        return "Str"
    if column_type == "numeric":
        return "Din" if column_name.startswith("din_") else "Dbl"
    raise ValueError(f"Unsupported type: {column_type}")


def infra_prefix_constant(column: dict) -> str:
    column_type = column["tipoBanco"]
    column_name = column.get("nome", "")
    if column_type in {"int", "integer"}:
        return "InfraDTO::$PREFIXO_NUM"
    if column_type == "varchar":
        return "InfraDTO::$PREFIXO_STR"
    if column_type in {"date", "datetime", "timestamp"}:
        return "InfraDTO::$PREFIXO_DTH" if column_name.startswith("dth_") else "InfraDTO::$PREFIXO_DTA"
    if column_type == "char":
        return "InfraDTO::$PREFIXO_STR"
    if column_type == "numeric":
        return "InfraDTO::$PREFIXO_DIN" if column_name.startswith("din_") else "InfraDTO::$PREFIXO_DBL"
    raise ValueError(f"Unsupported type: {column_type}")


def attribute_name(column: dict) -> str:
    prefix = dto_prefix(column)
    stripped = strip_common_prefixes(column["nome"])
    return prefix + pascal_case(stripped)


def class_base(table_name: str) -> str:
    return pascal_case(table_name)


CLASS_LAYER_DIRS = {
    "DTO": "dto",
    "BD": "bd",
    "RN": "rn",
    "INT": "int",
}

# Profundidade da pagina em relacao a web/SEI.php: modulos/<inst>/<modulo>/ = 3; modulos/<modulo>/ = 2.
DEFAULT_PAGE_LEVELS = 3
PAGE_LEVELS = DEFAULT_PAGE_LEVELS
RESERVED_ACCESSKEYS_CADASTRO = {"s", "c", "f"}
RESERVED_ACCESSKEYS_LISTA = {"n", "e", "f", "t", "r"}


def set_page_levels(levels: int) -> None:
    global PAGE_LEVELS
    PAGE_LEVELS = levels


def class_require_sei() -> str:
    return "require_once __DIR__ . '/" + "/".join([".."] * (PAGE_LEVELS + 1)) + "/SEI.php';\n\n"


def page_require_sei() -> str:
    return "  require_once __DIR__ . '/" + "/".join([".."] * PAGE_LEVELS) + "/SEI.php';\n\n\n"


def page_levels_from_output_dir(output_dir: Path):
    """Deriva a profundidade quando a saida esta em .../web/modulos/...; senao devolve None."""
    parts = output_dir.resolve().parts
    for index in range(len(parts) - 1):
        if parts[index] == "web" and parts[index + 1] == "modulos":
            return len(parts) - (index + 1)
    return None


def expected_files(table_name: str) -> list[str]:
    base = class_base(table_name)
    return [
        f"dto/{base}DTO.php",
        f"bd/{base}BD.php",
        f"rn/{base}RN.php",
        f"int/{base}INT.php",
        f"{table_name}_lista.php",
        f"{table_name}_cadastro.php",
    ]


def physical_pk_name(table_name: str) -> str:
    return f"id_{table_name}"


def php_header() -> str:
    return "<?php\n"


def read_latin1(path: Path) -> str:
    return path.read_text(encoding="latin-1")


def validate_physical_name(name: str, kind: str) -> None:
    if len(name) > 26:
        raise ValueError(f"{kind} name exceeds 26 characters: {name}")
    if name.lower() != name:
        raise ValueError(f"{kind} name must be lowercase: {name}")
    allowed = set("abcdefghijklmnopqrstuvwxyz0123456789_")
    if any(char not in allowed for char in name):
        raise ValueError(f"{kind} name contains unsupported characters: {name}")


def validate_supported_input(data: dict) -> None:
    if not isinstance(data, dict):
        raise ValueError("Contrato deve ser um objeto JSON")
    entidade = data.get("entidade")
    if not isinstance(entidade, dict):
        raise ValueError("Chave obrigatoria ausente: entidade")
    table_name = entidade.get("tabela", "")
    if not table_name:
        raise ValueError("Chave obrigatoria ausente: entidade.tabela")
    for key in ("singular", "plural", "comentario", "campoPrincipal"):
        if not entidade.get(key):
            raise ValueError(f"Chave obrigatoria ausente ou vazia: entidade.{key}")
    for key in ("singular", "plural", "comentario"):
        validate_display_text(entidade[key], f"entidade.{key}")
    if entidade.get("artigo") not in {"o", "a"}:
        raise ValueError("entidade.artigo deve ser 'o' ou 'a'")

    validate_physical_name(table_name, "table")
    if not re.match(r"^md_[a-z0-9]+_", table_name):
        raise ValueError(f"Tabela de modulo deve seguir md_<sigla>_<entidade>: {table_name}")

    columns = data.get("colunas")
    if not isinstance(columns, list) or not columns:
        raise ValueError("Chave obrigatoria ausente ou vazia: colunas")
    field_names = {column.get("nome") for column in columns}
    campo_principal = entidade.get("campoPrincipal")
    if campo_principal not in field_names:
        raise ValueError("entidade.campoPrincipal must reference an existing column")

    pk_count = 0
    pk_columns = []
    supported_types = {"int", "integer", "varchar", "datetime", "date", "timestamp", "char", "numeric"}
    for column in columns:
        name = column.get("nome", "")
        validate_physical_name(name, "column")
        if not column.get("comentario"):
            raise ValueError(f"Column comentario is required: {name}")
        validate_display_text(column["comentario"], f"colunas.{name}.comentario")
        if column.get("tipoBanco") not in supported_types:
            raise ValueError(
                f"Unsupported v1 type: {column.get('tipoBanco')} for {name}"
            )
        if not isinstance(column.get("obrigatorio"), bool):
            raise ValueError(f"Coluna sem 'obrigatorio' booleano: {name}")
        if name.startswith("sta_"):
            raise ValueError(
                f"Coluna de status multivalorado (sta_) nao e suportada pelo gerador: {name}"
            )
        if column.get("tipoBanco") == "timestamp" and not name.startswith("dth_"):
            raise ValueError(f"Coluna timestamp deve usar o prefixo dth_: {name}")
        if column.get("tipoBanco") == "date" and name.startswith("dth_"):
            raise ValueError(f"Coluna date nao pode usar o prefixo dth_ (use dta_): {name}")
        if column.get("tipoBanco") == "numeric":
            for key in ("precisao", "escala"):
                if key in column and not isinstance(column[key], int):
                    raise ValueError(f"Coluna numeric com '{key}' nao inteiro: {name}")
        if column.get("chavePrimaria"):
            pk_count += 1
            pk_columns.append(column)

    if pk_count == 0 or pk_count > 2:
        raise ValueError("One or two primary key columns are required")

    if pk_count == 1:
        expected_pk = physical_pk_name(table_name)
        if pk_columns[0]["nome"] != expected_pk:
            raise ValueError(
                f"Sequential PK must be named {expected_pk}: {pk_columns[0]['nome']}"
            )
        regras = data.get("regrasGeracao")
        if not isinstance(regras, dict) or "campoSinAtivo" not in regras:
            raise ValueError(
                "Chave obrigatoria ausente: regrasGeracao.campoSinAtivo (nome da coluna ou null)"
            )
        campo_sin_ativo = regras.get("campoSinAtivo")
        if campo_sin_ativo is not None:
            if campo_sin_ativo != "sin_ativo":
                raise ValueError(
                    f"regrasGeracao.campoSinAtivo deve ser 'sin_ativo' ou null: {campo_sin_ativo}"
                )
            sin_column = next((c for c in columns if c.get("nome") == "sin_ativo"), None)
            if sin_column is None or sin_column.get("tipoBanco") != "char":
                raise ValueError(
                    "regrasGeracao.campoSinAtivo exige coluna sin_ativo do tipo char em colunas"
                )

    if pk_count == 2:
        if data.get("regrasGeracao", {}).get("campoSinAtivo") is not None:
            raise ValueError(
                "N:N entities must set regrasGeracao.campoSinAtivo to null"
            )
        # N:N: validate that relacionamentosNn has exactly 2 entries with metodoInt
        nn_rels = data.get("relacionamentosNn", [])
        if len(nn_rels) != 2:
            raise ValueError(
                "N:N entity (2 PKs) requires 'relacionamentosNn' with exactly 2 entries"
            )
        for rel in nn_rels:
            if not rel.get("metodoInt"):
                raise ValueError(f"relacionamentosNn entry missing 'metodoInt': {rel}")
            if not rel.get("classeInt"):
                raise ValueError(f"relacionamentosNn entry missing 'classeInt': {rel}")
            validate_physical_name(rel.get("tabelaOrigem", ""), "table")
            if rel.get("rotulo") is not None:
                validate_display_text(rel["rotulo"], f"relacionamentosNn.{rel.get('tabelaOrigem')}.rotulo")

    for relation in data.get("relacionamentos", []):
        if relation.get("coluna") not in field_names:
            raise ValueError(
                f"Relationship coluna not found in colunas: {relation.get('coluna')}"
            )
        validate_physical_name(relation.get("tabelaReferencia", ""), "table")
        if not relation.get("campoExibicao"):
            raise ValueError(f"Relationship sem campoExibicao: {relation.get('coluna')}")
        fk_column = next(c for c in columns if c.get("nome") == relation.get("coluna"))
        tipo_fk = (relation.get("tipoFk") or "").lower()
        if tipo_fk == "obrigatoria" and not fk_column.get("obrigatorio"):
            raise ValueError(
                f"FK {relation.get('coluna')} declara tipoFk obrigatoria mas a coluna nao e obrigatoria"
            )
        if tipo_fk == "opcional" and fk_column.get("obrigatorio"):
            raise ValueError(
                f"FK {relation.get('coluna')} declara tipoFk opcional mas a coluna e obrigatoria"
            )

    regras_geracao = data.get("regrasGeracao") or {}
    if "paginacao" in regras_geracao and not isinstance(regras_geracao["paginacao"], bool):
        raise ValueError("regrasGeracao.paginacao deve ser booleano")
    escopo = regras_geracao.get("escopoUnidade")
    if escopo is not None:
        if pk_count == 2:
            raise ValueError("regrasGeracao.escopoUnidade nao se aplica a entidade N:N")
        scope_col = next((c for c in columns if c.get("nome") == escopo), None)
        if scope_col is None or scope_col.get("tipoBanco") not in {"int", "integer"}:
            raise ValueError(f"regrasGeracao.escopoUnidade deve apontar para coluna int existente: {escopo}")
        if scope_col.get("chavePrimaria") or not scope_col.get("obrigatorio"):
            raise ValueError(f"regrasGeracao.escopoUnidade exige coluna obrigatoria e nao PK: {escopo}")
        if any(r.get("coluna") == escopo for r in data.get("relacionamentos", [])):
            raise ValueError(
                f"regrasGeracao.escopoUnidade '{escopo}' nao pode estar em relacionamentos: a unidade vem da sessao, nao de select"
            )
    for column in columns:
        if "unico" in column:
            if not isinstance(column["unico"], bool):
                raise ValueError(f"Coluna com 'unico' nao booleano: {column.get('nome')}")
            if column["unico"] and (column.get("chavePrimaria") or pk_count == 2):
                raise ValueError(f"'unico' nao se aplica a PK nem a entidade N:N: {column.get('nome')}")
            if column["unico"] and column.get("nome") == escopo:
                raise ValueError(f"'unico' nao se aplica a coluna de escopo por unidade: {column.get('nome')}")
    for dep in regras_geracao.get("dependentes") or []:
        if not isinstance(dep, dict) or not dep.get("tabela") or not dep.get("coluna") or not dep.get("rotulo"):
            raise ValueError("regrasGeracao.dependentes exige entradas com tabela, coluna e rotulo")
        validate_physical_name(dep["tabela"], "table")
        validate_physical_name(dep["coluna"], "column")
        validate_display_text(dep["rotulo"], f"regrasGeracao.dependentes.{dep['tabela']}.rotulo")
        if pk_count == 2:
            raise ValueError("regrasGeracao.dependentes nao se aplica a entidade N:N")

    ui = data.get("ui") or {}
    ordem = ui.get("ordemFormulario")
    if pk_count == 1 and ordem:
        if escopo and escopo in ordem:
            raise ValueError(f"regrasGeracao.escopoUnidade '{escopo}' nao entra em ui.ordemFormulario: a unidade vem da sessao")
        expected = [
            c["nome"]
            for c in columns
            if not c.get("chavePrimaria") and c["nome"] not in {"sin_ativo", escopo}
        ]
        missing = [name for name in expected if name not in ordem]
        if missing:
            raise ValueError(
                "ui.ordemFormulario deve conter toda coluna de formulario; faltam: "
                + ", ".join(missing)
            )
    relation_columns = {r.get("coluna") for r in data.get("relacionamentos", [])}
    for name, campo_ui in (ui.get("campos") or {}).items():
        if (campo_ui or {}).get("rotulo") is not None:
            validate_display_text(campo_ui["rotulo"], f"ui.campos.{name}.rotulo")
        tecla = (campo_ui or {}).get("teclaAtalho") or ""
        if not tecla:
            continue
        reserved = set(RESERVED_ACCESSKEYS_CADASTRO)
        if name in relation_columns or pk_count == 2:
            reserved |= RESERVED_ACCESSKEYS_LISTA
        if tecla.lower() in reserved:
            raise ValueError(
                f"ui.campos.{name}.teclaAtalho '{tecla}' colide com tecla reservada da pagina "
                f"(cadastro: S, C, F; filtros da lista: N, E, F, T, R)"
            )


def is_nn(data: dict) -> bool:
    """Returns True when the entity has a composite PK (N:N relationship table)."""
    return sum(1 for c in data.get("colunas", []) if c.get("chavePrimaria")) == 2


def ui_label(column: dict) -> str:
    if column["nome"] == "sin_ativo":
        return "Sinalizador de Exclusão Lógica"
    if column.get("_escopo_unidade") and not (column.get("_ui") or {}).get("rotulo"):
        return "Unidade"
    ui = column.get("_ui") or {}
    return ui.get("rotulo", pascal_case(strip_common_prefixes(column["nome"]))).replace(
        "_", " "
    )


def column_article(column: dict) -> str:
    """Artigo do rotulo da coluna (ui.campos.<coluna>.artigo); padrao masculino."""
    if column["nome"] == "sin_ativo":
        return "o"
    ui = column.get("_ui") or {}
    if column.get("_escopo_unidade") and not ui.get("artigo"):
        return "a"
    return "a" if ui.get("artigo") == "a" else "o"


def concord(column: dict, masculino: str, feminino: str) -> str:
    return feminino if column_article(column) == "a" else masculino


def attr_suffix_from_attr(attr: str) -> str:
    for prefix in ("Num", "Str", "Din", "Dbl", "Dta", "Dth"):
        if attr.startswith(prefix):
            return attr[len(prefix):]
    return attr


def related_display_prefix(relation: dict) -> str:
    """Prefixo do atributo relacionado: tipo de campoExibicao (tipoExibicao), varchar por padrao."""
    return dto_prefix({"tipoBanco": relation.get("tipoExibicao") or "varchar", "nome": relation["campoExibicao"]})


def related_display_constant(relation: dict) -> str:
    return infra_prefix_constant({"tipoBanco": relation.get("tipoExibicao") or "varchar", "nome": relation["campoExibicao"]})


def related_suffix(data: dict, relation: dict) -> str:
    """Sufixo do atributo relacionado: campoExibicao + sufixo da coluna FK sem o 'Id' inicial.

    id_md_abc_projeto + identificacao -> IdentificacaoMdAbcProjeto (igual ao gabarito);
    id_unidade_origem + sigla -> SiglaUnidadeOrigem (duas FKs para a mesma tabela).
    """
    fk_column = next(c for c in data["colunas"] if c["nome"] == relation["coluna"])
    fk_suffix = attr_suffix_from_attr(attribute_name(fk_column))
    if fk_suffix.startswith("Id"):
        fk_suffix = fk_suffix[2:]
    return pascal_case(strip_common_prefixes(relation["campoExibicao"])) + fk_suffix


def related_attribute_name(data: dict, relation: dict) -> str:
    return related_display_prefix(relation) + related_suffix(data, relation)


def relation_aliases(data: dict) -> dict:
    """Alias SQL por coluna FK quando a mesma tabela aparece em mais de uma FK (idioma do core: 'usuario u2')."""
    aliases = {}
    seen = {}
    used = set()
    for relation in all_relations(data):
        table = relation["tabelaReferencia"]
        seen[table] = seen.get(table, 0) + 1
        if seen[table] == 1:
            aliases[relation["coluna"]] = None
            continue
        index = seen[table]
        alias = f"{table[0]}{index}"
        while alias in used:
            index += 1
            alias = f"{table[0]}{index}"
        used.add(alias)
        aliases[relation["coluna"]] = alias
    return aliases


def fk_suffix_of(data: dict, relation: dict) -> str:
    fk_column = next(c for c in data["colunas"] if c["nome"] == relation["coluna"])
    return attr_suffix_from_attr(attribute_name(fk_column))


def genero_words(article: str) -> dict:
    if article == "a":
        return {
            "novo": "Nova",
            "cadastrado": "cadastrada",
            "alterado": "alterada",
            "nenhum": "Nenhuma",
            "selecionado": "selecionada",
            "selecionados": "selecionadas",
            "do": "da",
            "dos": "das",
            "encontrado": "encontrada",
        }

    return {
        "novo": "Novo",
        "cadastrado": "cadastrado",
        "alterado": "alterado",
        "nenhum": "Nenhum",
        "selecionado": "selecionado",
        "selecionados": "selecionados",
        "do": "do",
        "dos": "dos",
        "encontrado": "encontrado",
    }


def int_helper_calls(data: dict) -> list[dict]:
    """Chamadas <Classe>INT::<metodo> que o CRUD gerado faz para tabelas fora do contrato."""
    calls = []
    if is_nn(data):
        for rel in data.get("relacionamentosNn", []):
            calls.append({"classe": rel["classeInt"], "metodo": rel["metodoInt"], "tabela": rel["tabelaOrigem"]})
        return calls
    for relation in data.get("relacionamentos", []):
        calls.append(
            {
                "classe": class_base(relation["tabelaReferencia"]) + "INT",
                "metodo": "montarSelect" + pascal_case(strip_common_prefixes(relation["campoExibicao"])),
                "tabela": relation["tabelaReferencia"],
            }
        )
    return calls


def check_int_helpers(data: dict, output_dir: Path) -> tuple[list[str], list[str]]:
    """Confere se cada helper INT chamado existe no core (web/int) ou no modulo de saida.

    Devolve (erros, alertas). Classe encontrada sem o metodo e erro; classe ausente nos dois lugares e alerta,
    porque pode ser gerada depois no mesmo modulo.
    """
    errors = []
    alerts = []
    core_int = ROOT / "fontes" / "sei" / "src" / "main" / "php" / "sei" / "web" / "int"
    for call in int_helper_calls(data):
        candidates = [core_int / f"{call['classe']}.php", output_dir / "int" / f"{call['classe']}.php"]
        found = [path for path in candidates if path.exists()]
        if not found:
            alerts.append(
                f"Helper {call['classe']}::{call['metodo']} (tabela {call['tabela']}) nao foi encontrado em web/int nem em {output_dir / 'int'}; "
                "gere ou confirme a classe INT antes de abrir o cadastro e a lista."
            )
            continue
        pattern = re.compile(r"function\s+" + re.escape(call["metodo"]) + r"\s*\(")
        if not any(pattern.search(path.read_text(encoding="latin-1")) for path in found):
            errors.append(
                f"Helper {call['classe']}::{call['metodo']} nao existe em {', '.join(str(p) for p in found)}; "
                "ajuste campoExibicao (ou metodoInt na N:N) para um metodo montarSelect existente."
            )
    return errors, alerts


def developer_alerts(data: dict) -> list[str]:
    entity = data.get("entidade", {})
    alerts = [
        "Revise os textos de domínio exibidos ao usuário antes de entregar o CRUD: títulos, singular/plural, rótulos, cabeçalhos, captions, mensagens, title e alt.",
        "O gerador corrige apenas textos padrão universais do CRUD; acentuação e termos de negócio devem vir revisados no contrato JSON.",
        f"Entidade no contrato: singular='{entity.get('singular', '')}', plural='{entity.get('plural', '')}', campoPrincipal='{entity.get('campoPrincipal', '')}'.",
    ]
    table_name = entity.get("tabela", "")
    if is_nn(data) and "_rel_" not in table_name:
        alerts.append(
            f"Tabela N:N '{table_name}' sem o padrão md_<sigla>_rel_<a>_<b>; o padrão de modelagem admite nome de conceito forte, confirme a escolha."
        )
    for relation in data.get("relacionamentos", []):
        if relation["coluna"] != physical_pk_name(relation["tabelaReferencia"]):
            alerts.append(
                f"FK {relation['coluna']} não repete o nome da PK de origem ({physical_pk_name(relation['tabelaReferencia'])}); "
                "aceito para papéis distintos (ex.: origem e destino), confirme se é intencional."
            )
    for column in data.get("colunas", []):
        if column.get("tipoBanco") == "numeric" and not column["nome"].startswith("din_"):
            alerts.append(
                f"Coluna numeric '{column['nome']}' sem prefixo din_ foi tratada como número (Dbl, sem máscara monetária); use din_ para valor monetário."
            )
    return alerts


def relation_for_column(data: dict, column_name: str):
    for relation in data.get("relacionamentos", []):
        if relation.get("coluna") == column_name:
            return relation
    return None


def regras(data: dict) -> dict:
    return data.get("regrasGeracao") or {}


def scope_column(data: dict):
    """Coluna de escopo por unidade (regrasGeracao.escopoUnidade), preenchida com a unidade atual da sessao."""
    name = regras(data).get("escopoUnidade")
    if not name:
        return None
    return next(c for c in data["colunas"] if c["nome"] == name)


def scope_relation(data: dict):
    column = scope_column(data)
    if column is None:
        return None
    return {"coluna": column["nome"], "tabelaReferencia": "unidade", "campoExibicao": "sigla", "tipoFk": "obrigatoria", "filtroFk": "on"}


def all_relations(data: dict) -> list:
    """Relacionamentos do contrato mais a FK implicita de escopo por unidade (so para DTO e alias)."""
    relations = list(data.get("relacionamentos", []))
    scope = scope_relation(data)
    if scope is not None and all(r["coluna"] != scope["coluna"] for r in relations):
        relations.append(scope)
    return relations


def has_pagination(data: dict) -> bool:
    return regras(data).get("paginacao", True) is not False


def dependents(data: dict) -> list:
    return regras(data).get("dependentes") or []


def render_dto(data: dict) -> str:
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    pk_columns = [c for c in data["colunas"] if c.get("chavePrimaria")]
    aliases = relation_aliases(data)
    docblock = [
        "/**\n",
        f" * @table {table_name} {data['entidade']['comentario']}\n",
    ]
    docblock.extend(f" * @column {column['nome']} {column['comentario']}\n" for column in data["colunas"])
    docblock.append(" */\n")
    lines = [
        php_header(),
        class_require_sei(),
        *docblock,
        f"class {base}DTO extends InfraDTO\n",
        "{\n",
        "  public function getStrNomeTabela(): ?string\n",
        "  {\n",
        f"    return '{table_name}';\n",
        "  }\n\n",
        "  /**\n",
        "   * @throws InfraException\n",
        "   */\n",
        "  public function montar(): void\n",
        "  {\n",
    ]

    for column in data["colunas"]:
        attr = attribute_name(column)
        suffix = (
            attr[len(dto_prefix(column)) :]
            if attr.startswith(dto_prefix(column))
            else attr
        )
        lines.append(
            f"    $this->adicionarAtributoTabela({infra_prefix_constant(column)}, '{suffix}', '{column['nome']}');\n"
        )

    for relation in all_relations(data):
        alias = aliases.get(relation["coluna"])
        related_table = f"{relation['tabelaReferencia']} {alias}" if alias else relation["tabelaReferencia"]
        related_field = f"{alias}.{relation['campoExibicao']}" if alias else relation["campoExibicao"]
        lines.append(
            f"\n    $this->adicionarAtributoTabelaRelacionada({related_display_constant(relation)}, '{related_suffix(data, relation)}', '{related_field}', '{related_table}');\n"
        )

    for relation in all_relations(data):
        fk_column = next(
            column for column in data["colunas"] if column["nome"] == relation["coluna"]
        )
        fk_attr = attribute_name(fk_column)
        fk_suffix = (
            fk_attr[len(dto_prefix(fk_column)) :]
            if fk_attr.startswith(dto_prefix(fk_column))
            else fk_attr
        )
        relation_type = (relation.get("tipoFk") or "").lower()
        filter_type = (relation.get("filtroFk") or "").lower()
        alias = aliases.get(relation["coluna"])
        fk_table = f"{relation['tabelaReferencia']} {alias}" if alias else relation["tabelaReferencia"]
        fk_field = physical_pk_name(relation["tabelaReferencia"])
        if alias:
            fk_field = f"{alias}.{fk_field}"
        fk_args = [
            f"'{fk_suffix}'",
            f"'{fk_table}'",
            f"'{fk_field}'",
        ]
        if relation_type == "opcional" or not fk_column.get("obrigatorio", False):
            fk_args.append("InfraDTO::$TIPO_FK_OPCIONAL")
        elif filter_type == "where":
            fk_args.append("InfraDTO::$TIPO_FK_OBRIGATORIA")

        if filter_type == "where":
            if len(fk_args) == 3:
                fk_args.append("InfraDTO::$TIPO_FK_OBRIGATORIA")
            fk_args.append("InfraDTO::$FILTRO_FK_WHERE")

        lines.append(f"\n    $this->configurarFK({', '.join(fk_args)});\n")

    if is_nn(data):
        # N:N: two informado PKs, no exclusao logica
        for pk_col in pk_columns:
            pk_attr = attribute_name(pk_col)
            pk_suffix = pk_attr[3:] if pk_attr.startswith("Num") else pk_attr
            lines.append(
                f"\n    $this->configurarPK('{pk_suffix}', InfraDTO::$TIPO_PK_INFORMADO);\n"
            )
    else:
        pk_col = pk_columns[0]
        pk_attr = attribute_name(pk_col)
        lines.append(
            f"\n    $this->configurarPK('{pk_attr[3:] if pk_attr.startswith('Num') else pk_attr}', InfraDTO::$TIPO_PK_NATIVA);\n"
        )
        if data["regrasGeracao"].get("campoSinAtivo"):
            lines.append("\n    $this->configurarExclusaoLogica('SinAtivo', 'N');\n")

    lines.append("\n  }\n}\n")
    return "".join(lines)


def render_bd(data: dict) -> str:
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    return (
        php_header()
        + class_require_sei()
        + f"class {base}BD extends InfraBD\n"
        + "{\n"
        + "  public function __construct(InfraIBanco $objInfraIBanco)\n"
        + "  {\n"
        + "    parent::__construct($objInfraIBanco);\n"
        + "  }\n"
        + "}\n"
    )


def validator_method_name(column: dict) -> str:
    return f"validar{attribute_name(column)}"


def validator_message(column: dict) -> str:
    return f"{q(ui_label(column))} não {concord(column, 'informado', 'informada')}."


def invalid_message(column: dict) -> str:
    return f"{q(ui_label(column))} {concord(column, 'inválido', 'inválida')}."


def render_validator(column: dict) -> str:
    table_base = class_base(column["_table"])
    attr = attribute_name(column)
    getter = f"get{attr}()"
    setter = f"set{attr}"
    method = validator_method_name(column)
    label = ui_label(column)
    required = column["obrigatorio"] or bool(column.get("chavePrimaria"))
    lines = [
        "  /**\n",
        "   * @throws InfraException\n",
        "   */\n",
        f"  private function {method}({table_base}DTO $obj{table_base}DTO, InfraException $objInfraException): void\n",
        "  {\n",
        f"    if (InfraString::isBolVazia($obj{table_base}DTO->{getter})) {{\n",
    ]
    if required:
        lines.append(f"      $objInfraException->adicionarValidacao('{validator_message(column)}');\n")
    else:
        lines.append(f"      $obj{table_base}DTO->{setter}(null);\n")

    unique_block = unique_check_lines(column, table_base, attr) if column.get("unico") else []

    if column["tipoBanco"] == "varchar":
        lines.append("    } else {\n")
        lines.append(
            f"      $obj{table_base}DTO->{setter}(trim($obj{table_base}DTO->{getter}));\n"
        )
        if column.get("tamanho"):
            lines.append(
                f"      if (strlen($obj{table_base}DTO->{getter})>{column['tamanho']}) {{\n"
            )
            lines.append(
                f"        $objInfraException->adicionarValidacao('{q(label)} possui tamanho superior a {column['tamanho']} caracteres.');\n"
            )
            lines.append("      }\n")
        lines.extend(unique_block)
        lines.append("    }\n")
    elif column["tipoBanco"] in {"datetime", "date", "timestamp"}:
        validar = "validarDataHora" if attr.startswith("Dth") else "validarData"
        lines.append(
            f"    }} elseif (!InfraData::{validar}($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(f"      $objInfraException->adicionarValidacao('{invalid_message(column)}');\n")
        if unique_block:
            lines.append("    } else {\n")
            lines.extend(unique_block)
        lines.append("    }\n")
    elif column["tipoBanco"] == "numeric" and attr.startswith("Din"):
        lines.append(
            f"    }} elseif (!InfraUtil::validarDin($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(f"      $objInfraException->adicionarValidacao('{invalid_message(column)}');\n")
        if unique_block:
            lines.append("    } else {\n")
            lines.extend(unique_block)
        lines.append("    }\n")
    elif column["tipoBanco"] == "numeric":
        lines.append(
            f"    }} elseif (!is_numeric($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(f"      $objInfraException->adicionarValidacao('{invalid_message(column)}');\n")
        if unique_block:
            lines.append("    } else {\n")
            lines.extend(unique_block)
        lines.append("    }\n")
    elif column["tipoBanco"] == "char":
        lines.append(
            f"    }} elseif (!InfraUtil::isBolSinalizadorValido($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(f"      $objInfraException->adicionarValidacao('{invalid_message(column)}');\n")
        lines.append("    }\n")
    elif unique_block:
        lines.append("    } else {\n")
        lines.extend(unique_block)
        lines.append("    }\n")
    else:
        lines.append("    }\n")

    lines.append("  }\n\n")
    return "".join(lines)


def unique_check_lines(column: dict, table_base: str, attr: str) -> list:
    """Chave candidata unica no idioma de trf4/julgamento (MotivoAusenciaRN): consulta outro registro com o mesmo valor."""
    ctx = column["_ctx"]
    dto = f"$obj{table_base}DTO"
    other = f"$obj{table_base}UnicoDTO"
    label = q(ui_label(column))
    este = "esta" if column_article(column) == "a" else "este"
    outro = "outra" if ctx["artigo"] == "a" else "outro"
    singular = ctx["singular"]
    lines = [
        f"\n      {other} = new {table_base}DTO();\n",
    ]
    if ctx["has_logical_delete"]:
        lines.append(f"      {other}->setBolExclusaoLogica(false);\n")
        lines.append(f"      {other}->retStrSinAtivo();\n")
    else:
        lines.append(f"      {other}->ret{ctx['pk_attr']}();\n")
    lines.append(f"      {other}->set{ctx['pk_attr']}({dto}->get{ctx['pk_attr']}(), InfraDTO::$OPER_DIFERENTE);\n")
    if ctx.get("scope_attr"):
        lines.append(f"      {other}->set{ctx['scope_attr']}({dto}->get{ctx['scope_attr']}());\n")
    lines.append(f"      {other}->set{attr}({dto}->get{attr}());\n")
    lines.append(f"      $obj{table_base}BD = new {table_base}BD($this->getObjInfraIBanco());\n")
    lines.append(f"      {other} = $obj{table_base}BD->consultar({other});\n")
    lines.append(f"      if ({other} !== null) {{\n")
    if ctx["has_logical_delete"]:
        lines.append(f"        if ({other}->getStrSinAtivo() === 'S') {{\n")
        lines.append(f"          $objInfraException->adicionarValidacao('Existe {outro} {singular} com {este} {label}.');\n")
        lines.append("        } else {\n")
        lines.append(f"          $objInfraException->adicionarValidacao('Existe ocorrência inativa de {singular} com {este} {label}.');\n")
        lines.append("        }\n")
    else:
        lines.append(f"        $objInfraException->adicionarValidacao('Existe {outro} {singular} com {este} {label}.');\n")
    lines.append("      }\n")
    return lines


def dependents_check_lines(data: dict, base: str, pk_attr: str, singular: str, article: str) -> str:
    """Bloqueia exclusao ou desativacao quando ha registro dependente, no idioma de MotivoAusenciaRN (contar na RN filha)."""
    deps = dependents(data)
    if not deps:
        return ""
    out = [f"      foreach ($arrObj{base}DTO as $obj{base}DTO) {{\n"]
    for dep in deps:
        child = class_base(dep["tabela"])
        child_attr = attribute_name({"nome": dep["coluna"], "tipoBanco": "int"})
        vinculo = "vinculada" if dep.get("artigo") == "a" else "vinculado"
        preposicao = "à" if article == "a" else "ao"
        out.append(f"        $obj{child}DTO = new {child}DTO();\n")
        out.append(f"        $obj{child}DTO->set{child_attr}($obj{base}DTO->get{pk_attr}());\n")
        out.append(f"        $obj{child}RN = new {child}RN();\n")
        out.append(f"        if ($obj{child}RN->contar($obj{child}DTO) > 0) {{\n")
        out.append(f"          $objInfraException->lancarValidacao('Existe {q(dep['rotulo'])} {vinculo} {preposicao} {singular}.');\n")
        out.append("        }\n")
    out.append("      }\n\n")
    return "".join(out)


def rn_method(base: str, signature: str, resource: str, singular_msg: str, body: str, doc_return: str, doc_param: str, commented: bool = False) -> str:
    """Monta um metodo da RN no formato do gabarito TRF4: PHPDoc, permissao auditada, ancoras e try/catch."""
    docblock = (
        "  /**\n"
        f"   * @param {doc_param}\n"
        f"   * @return {doc_return}\n"
        "   * @throws InfraException\n"
        "   */\n"
    )
    text = (
        f"  protected function {signature}\n"
        "  {\n"
        "    try {\n"
        f"      SessaoSEI::getInstance()->validarAuditarPermissao('{resource}', __METHOD__, {'$arrObj' if 'array $arrObj' in signature else '$obj'}{base}DTO);\n\n"
        + body
        + "\n    } catch (Exception $e) {\n"
        f"      throw new InfraException('{singular_msg}', $e);\n"
        "    }\n"
        "  }\n"
    )
    if commented:
        # docblock vivo e corpo comentado, como o gabarito TRF4 faz sem sin_ativo
        return docblock + "/* " + text[2:] + "*/\n"
    return docblock + text


RN_ANCHORS = (
    "      //Regras de Negocio\n"
    "      //$objInfraException = new InfraException();\n\n"
    "      //$objInfraException->lancarValidacoes();\n\n"
)


def render_rn(data: dict) -> str:
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = q(data["entidade"]["singular"])
    plural = q(data["entidade"]["plural"])
    nn = is_nn(data)
    has_logical_delete = (not nn) and bool(data["regrasGeracao"].get("campoSinAtivo"))
    scope = scope_column(data)
    pk_attr = attribute_name([c for c in data["colunas"] if c.get("chavePrimaria")][0])
    article = data["entidade"]["artigo"]
    ctx = {
        "singular": singular,
        "artigo": article,
        "pk_attr": pk_attr,
        "has_logical_delete": has_logical_delete,
        "scope_attr": attribute_name(scope) if scope else None,
    }
    columns = []
    for column in data["colunas"]:
        cloned = dict(column)
        cloned["_table"] = table_name
        cloned["_ui"] = data.get("ui", {}).get("campos", {}).get(column["nome"])
        cloned["_ctx"] = ctx
        if scope is not None and column["nome"] == scope["nome"]:
            cloned["_escopo_unidade"] = True
        columns.append(cloned)

    # N:N: as duas PKs sao informadas pelo usuario e recebem validador; CRUD simples: a PK e nativa e nao valida
    validator_columns = columns if nn else [c for c in columns if not c.get("chavePrimaria")]
    validators = [render_validator(column) for column in validator_columns]
    dependents_block = dependents_check_lines(data, base, pk_attr, singular, article)
    dependents_prefix = ("      $objInfraException = new InfraException();\n\n" + dependents_block) if dependents_block else RN_ANCHORS

    create_lines = "".join(
        f"      $this->{validator_method_name(column)}($obj{base}DTO, $objInfraException);\n"
        for column in validator_columns
    )
    update_lines = "".join(
        f"      if ($obj{base}DTO->isSet{attribute_name(column)}()) {{\n"
        f"        $this->{validator_method_name(column)}($obj{base}DTO, $objInfraException);\n"
        "      }\n\n"
        for column in validator_columns
    )
    bd_line = f"      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n"
    def loop(op: str) -> str:
        return (
            f"      foreach ($arrObj{base}DTO as $obj{base}DTO) {{\n"
            f"        $obj{base}BD->{op}($obj{base}DTO);\n"
            "      }\n"
        )
    dto_param = f"{base}DTO $obj{base}DTO"
    arr_param = f"{base}DTO[] $arrObj{base}DTO"

    methods = [
        rn_method(base, f"cadastrarControlado({base}DTO $obj{base}DTO): {base}DTO", f"{table_name}_cadastrar",
                  f"Erro cadastrando {singular}.",
                  "      $objInfraException = new InfraException();\n\n" + create_lines
                  + "      $objInfraException->lancarValidacoes();\n\n" + bd_line
                  + f"      return $obj{base}BD->cadastrar($obj{base}DTO);\n",
                  f"{base}DTO", dto_param),
        rn_method(base, f"alterarControlado({base}DTO $obj{base}DTO): void", f"{table_name}_alterar",
                  f"Erro alterando {singular}.",
                  "      $objInfraException = new InfraException();\n\n" + update_lines
                  + "      $objInfraException->lancarValidacoes();\n\n" + bd_line
                  + f"      $obj{base}BD->alterar($obj{base}DTO);\n",
                  "void", dto_param),
        rn_method(base, f"excluirControlado(array $arrObj{base}DTO): void", f"{table_name}_excluir",
                  f"Erro excluindo {singular}.",
                  dependents_prefix + bd_line + loop("excluir"),
                  "void", arr_param),
        rn_method(base, f"consultarConectado({base}DTO $obj{base}DTO): ?{base}DTO", f"{table_name}_consultar",
                  f"Erro consultando {singular}.",
                  RN_ANCHORS + bd_line + f"      return $obj{base}BD->consultar($obj{base}DTO);\n",
                  f"{base}DTO|null", dto_param),
        rn_method(base, f"listarConectado({base}DTO $obj{base}DTO): array", f"{table_name}_listar",
                  f"Erro listando {plural}.",
                  RN_ANCHORS + bd_line + f"      return $obj{base}BD->listar($obj{base}DTO);\n",
                  f"{base}DTO[]", dto_param),
        rn_method(base, f"contarConectado({base}DTO $obj{base}DTO): int", f"{table_name}_listar",
                  f"Erro contando {plural}.",
                  RN_ANCHORS + bd_line + f"      return $obj{base}BD->contar($obj{base}DTO);\n",
                  "int", dto_param),
        # desativar, reativar e bloquear: ativos com sin_ativo; comentados em bloco sem sin_ativo (gabarito TRF4)
        rn_method(base, f"desativarControlado(array $arrObj{base}DTO): void", f"{table_name}_desativar",
                  f"Erro desativando {singular}.",
                  dependents_prefix + bd_line + loop("desativar"),
                  "void", arr_param, commented=not has_logical_delete),
        rn_method(base, f"reativarControlado(array $arrObj{base}DTO): void", f"{table_name}_reativar",
                  f"Erro reativando {singular}.",
                  RN_ANCHORS + bd_line + loop("reativar"),
                  "void", arr_param, commented=not has_logical_delete),
        # bloquear: Controlado (manual cap. 4, lock ate o fim da transacao) e recurso de consultar (decisao D-02)
        rn_method(base, f"bloquearControlado({base}DTO $obj{base}DTO): ?{base}DTO", f"{table_name}_consultar",
                  f"Erro bloqueando {singular}.",
                  RN_ANCHORS + bd_line + f"      return $obj{base}BD->bloquear($obj{base}DTO);\n",
                  f"{base}DTO|null", dto_param, commented=not has_logical_delete),
    ]

    return (
        php_header()
        + class_require_sei()
        + "/**\n"
        + f" * @method {base}DTO cadastrar({base}DTO $obj{base}DTO)\n"
        + f" * @method {base}DTO[] listar({base}DTO $obj{base}DTO)\n"
        + f" * @method {base}DTO|null consultar({base}DTO $obj{base}DTO)\n"
        + f" * @method {base}DTO|null bloquear({base}DTO $obj{base}DTO)\n"
        + f" * @method void alterar({base}DTO $obj{base}DTO)\n"
        + f" * @method void excluir({base}DTO[] $arrObj{base}DTO)\n"
        + f" * @method void desativar({base}DTO[] $arrObj{base}DTO)\n"
        + f" * @method void reativar({base}DTO[] $arrObj{base}DTO)\n"
        + " */\n"
        + f"class {base}RN extends InfraRN\n"
        + "{\n"
        + "  protected function inicializarObjInfraIBanco(): InfraIBanco\n  {\n    return BancoSEI::getInstance();\n  }\n\n"
        + "".join(validators)
        + "\n".join(methods)
        + "}\n"
    )


def render_lista_nn(data: dict) -> str:
    """Render lista page for N:N (composite PK) entities."""
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = q(data["entidade"]["singular"])
    plural = q(data["entidade"]["plural"])
    article = data["entidade"]["artigo"]
    nn_rels = data["relacionamentosNn"]
    pk1_col = [c for c in data["colunas"] if c.get("chavePrimaria")][0]
    pk2_col = [c for c in data["colunas"] if c.get("chavePrimaria")][1]
    pk1_attr = attribute_name(pk1_col)
    pk2_attr = attribute_name(pk2_col)
    pk1_suffix = pk1_attr[3:] if pk1_attr.startswith("Num") else pk1_attr
    pk2_suffix = pk2_attr[3:] if pk2_attr.startswith("Num") else pk2_attr
    pk1_param = pk1_col["nome"]
    pk2_param = pk2_col["nome"]
    words = genero_words(article)
    new_label = words["novo"]

    display_infos = []
    for index, pk_col in enumerate((pk1_col, pk2_col)):
        relation = relation_for_column(data, pk_col["nome"])
        if relation is None:
            continue
        display_infos.append(
            {
                "attr": related_attribute_name(data, relation),
                "label": nn_rels[index].get("rotulo", pascal_case(pk_col["nome"])),
            }
        )

    display_return_lines = "".join(
        f"  $obj{base}DTO->ret{info['attr']}();\n" for info in display_infos
    )
    header_columns = "".join(
        f"    $strResultado .= '<th class=\"infraTh\">'.PaginaSEI::getInstance()->getThOrdenacao($obj{base}DTO,'{q(info['label'])}','{attr_suffix_from_attr(info['attr'])}',$arrObj{base}DTO).'</th>'.\"\\n\";\n"
        for info in display_infos
    )
    row_columns = "".join(
        f"      $strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObj{base}DTO[$i]->get{info['attr']}()).'</td>';\n"
        for info in display_infos
    )
    if display_infos:
        display_expr = ".' - '.".join(
            f"$arrObj{base}DTO[$i]->get{info['attr']}()" for info in display_infos
        )
        check_description = display_expr
        sort_field = attr_suffix_from_attr(display_infos[0]["attr"])
    else:
        check_description = f"$arrObj{base}DTO[$i]->get{pk1_attr}()"
        sort_field = pk1_suffix

    # build filter selects from relacionamentosNn
    sel_names = ", ".join("'sel" + class_base(r["tabelaOrigem"]) + "'" for r in nn_rels)
    filter_apply = ""
    filter_selects = ""
    filter_form = ""
    style_parts = ""
    for rel in nn_rels:
        rel_base = class_base(rel["tabelaOrigem"])
        rel_var = f"$numId{rel_base}"
        label = rel.get("rotulo", rel_base)
        ak = label[0].lower()
        filter_apply += (
            f"  {rel_var} = PaginaSEI::getInstance()->recuperarCampo('sel{rel_base}');\n"
            f"  if ({rel_var}!=='') {{\n"
            f"    $obj{base}DTO->set{pk1_attr if rel == nn_rels[0] else pk2_attr}({rel_var});\n"
            f"  }}\n\n"
        )
        filter_selects += f"  $strItensSel{rel_base} = {rel['classeInt']}::{rel['metodoInt']}('', 'Todos', {rel_var});\n"
        filter_form += (
            f"  <?php\n  PaginaSEI::getInstance()->abrirAreaDados('5em');\n  ?>\n"
            f'  <label id="lbl{rel_base}" for="sel{rel_base}" accesskey="{ak}" class="infraLabelOpcional">'
            f"{label}:</label>\n"
            f'  <select id="sel{rel_base}" name="sel{rel_base}" onchange="this.form.submit();" '
            f'class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" >\n'
            f"  <?=$strItensSel{rel_base}??false?>\n  </select>\n"
            f"  <?php\n  PaginaSEI::getInstance()->fecharAreaDados();\n  ?>\n\n"
        )
        style_parts += (
            f"#lbl{rel_base} {{position:absolute;left:0;top:0;width:25%;}}\n"
            f"#sel{rel_base} {{position:absolute;left:0;top:40%;width:25%;}}\n\n"
        )

    return (
        php_header()
        + "\n\ntry {\n"
        + page_require_sei()
        + "  session_start();\n\n"
        + "  //////////////////////////////////////////////////////////////////////////////\n"
        + "  //InfraDebug::getInstance()->setBolLigado(false);\n"
        + "  //InfraDebug::getInstance()->setBolDebugInfra(true);\n"
        + "  //InfraDebug::getInstance()->limpar();\n"
        + "  //////////////////////////////////////////////////////////////////////////////\n\n"
        + "  SessaoSEI::getInstance()->validarLink();\n\n"
        + "  $strAcao = PaginaSEI::GET('acao');\n"
        + "  SessaoSEI::getInstance()->validarPermissao($strAcao);\n\n"
        + f"  PaginaSEI::getInstance()->prepararSelecao('{table_name}_selecionar');\n\n"
        + f"  PaginaSEI::getInstance()->salvarCamposPost([{sel_names}]);\n\n"
        + "  switch ($strAcao) {\n"
        + f"    case '{table_name}_excluir':\n"
        + "      try {\n"
        + f"        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();\n"
        + f"        $arrObj{base}DTO = [];\n"
        + f"        foreach ($arrStrIds as $strId) {{\n"
        + f"          $obj{base}DTO = new {base}DTO();\n"
        + f"          $arrStrIdComposto = explode('-',$strId);\n"
        + f"          if (count($arrStrIdComposto)!=2 || !ctype_digit($arrStrIdComposto[0]) || !ctype_digit($arrStrIdComposto[1])) {{\n"
        + f"            throw new InfraException('Identificador {words['do']} {singular} inválido.');\n"
        + f"          }}\n"
        + f"          $obj{base}DTO->set{pk1_attr}((int)$arrStrIdComposto[0]);\n"
        + f"          $obj{base}DTO->set{pk2_attr}((int)$arrStrIdComposto[1]);\n"
        + f"          $arrObj{base}DTO[] = $obj{base}DTO;\n"
        + "        }\n"
        + f"        $obj{base}RN = new {base}RN();\n"
        + f"        $obj{base}RN->excluir($arrObj{base}DTO);\n"
        + f"        PaginaSEI::getInstance()->adicionarMensagem('Opera\u00e7\u00e3o realizada com sucesso.');\n"
        + "      } catch (Exception $e) {\n"
        + "        PaginaSEI::getInstance()->processarExcecao($e);\n"
        + "      } \n"
        + f"      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.$strAcao));\n"
        + "      die;\n\n"
        + f"    case '{table_name}_selecionar':\n"
        + f"      $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar {singular}','Selecionar {plural}');\n\n"
        + f"      //Se cadastrou alguem\n"
        + f"      if (PaginaSEI::GET('acao_origem')==='{table_name}_cadastrar' && PaginaSEI::GET('{pk1_param}') !== null && PaginaSEI::GET('{pk2_param}') !== null) {{\n"
        + f"        PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('{pk1_param}').'-'.PaginaSEI::GET('{pk2_param}'));\n"
        + "      }\n"
        + "      break;\n\n"
        + f"    case '{table_name}_listar':\n"
        + f"      $strTitulo = '{plural}';\n"
        + "      break;\n\n"
        + "    default:\n"
        + "      throw new InfraException(\"Ação '\".$strAcao.\"' não reconhecida.\");\n"
        + "  }\n\n"
        + "  $arrComandos = [];\n"
        + f"  if ($strAcao==='{table_name}_selecionar') {{\n"
        + f'    $arrComandos[] = \'<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>\';\n'
        + "  }\n\n"
        + f"  $bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_cadastrar');\n"
        + f"  if ($bolAcaoCadastrar) {{\n"
        + f"    $arrComandos[] = '<button type=\"button\" accesskey=\"N\" id=\"btn{new_label}\" value=\"{new_label}\" onclick=\"location.href=\\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_cadastrar&acao_origem='.$strAcao.'&acao_retorno='.$strAcao).'\\'\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">N</span>{new_label[1:]}</button>';\n"
        + "  }\n\n"
        + f"  $obj{base}DTO = new {base}DTO();\n"
        + f"  $obj{base}DTO->ret{pk1_attr}();\n"
        + f"  $obj{base}DTO->ret{pk2_attr}();\n"
        + display_return_lines
        + filter_apply
        + f"  PaginaSEI::getInstance()->prepararOrdenacao($obj{base}DTO, '{sort_field}', InfraDTO::$TIPO_ORDENACAO_ASC);\n"
        + f"  {'' if has_pagination(data) else '//'}PaginaSEI::getInstance()->prepararPaginacao($obj{base}DTO);\n\n"
        + f"  $obj{base}RN = new {base}RN();\n"
        + f"  $arrObj{base}DTO = $obj{base}RN->listar($obj{base}DTO);\n\n"
        + f"  {'' if has_pagination(data) else '//'}PaginaSEI::getInstance()->processarPaginacao($obj{base}DTO);\n\n"
        + f"  /** @var {base}DTO[] $arrObj{base}DTO */\n\n"
        + f"  $numRegistros = count($arrObj{base}DTO);\n\n"
        + "  if ($numRegistros > 0) {\n\n"
        + "    $bolCheck = false;\n\n"
        + f"    if ($strAcao==='{table_name}_selecionar') {{\n"
        + f"      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');\n"
        + f"      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');\n"
        + "      $bolAcaoExcluir = false;\n"
        + "      $bolCheck = true;\n"
        + "    } else {\n"
        + f"      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');\n"
        + f"      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');\n"
        + f"      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('{table_name}_excluir');\n"
        + "    }\n\n"
        + "    if ($bolAcaoExcluir) {\n"
        + "      $bolCheck = true;\n"
        + f'      $arrComandos[] = \'<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>\';\n'
        + f"      $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_excluir&acao_origem='.$strAcao);\n"
        + "    }\n\n"
        + "    $strResultado = '';\n"
        + f"    $strCaptionTabela = '{plural}';\n\n"
        + '    $strResultado .= \'<table style="width: 99%" class="infraTable">\'."\\n";\n'
        + "    $strResultado .= '<caption class=\"infraCaption\">'.PaginaSEI::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';\n"
        + "    $strResultado .= '<thead><tr>';\n"
        + "    if ($bolCheck) {\n"
        + '       $strResultado .= \'<th class="infraTh" style="width: 1%">\'.PaginaSEI::getInstance()->getThCheck().\'</th>\'."\\n";\n'
        + "    }\n"
        + header_columns
        + '    $strResultado .= \'<th class="infraTh">Ações</th>\'."\\n";\n'
        + "    $strResultado .= '</tr></thead><tbody>'.\"\\n\";\n"
        + "    $strCssTr='';\n"
        + "    for($i = 0;$i < $numRegistros; $i++) {\n\n"
        + "      $strCssTr = ($strCssTr==='<tr class=\"infraTrClara\">')?'<tr class=\"infraTrEscura\">':'<tr class=\"infraTrClara\">';\n"
        + "      $strResultado .= $strCssTr;\n\n"
        + "      if ($bolCheck) {\n"
        + f"        $strResultado .= '<td style=\"vertical-align: middle\">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObj{base}DTO[$i]->get{pk1_attr}().'-'.$arrObj{base}DTO[$i]->get{pk2_attr}(),{check_description}).'</td>';\n"
        + "      }\n"
        + row_columns
        + "      $strResultado .= '<td style=\"text-align: center\">';\n\n"
        + f"      $strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObj{base}DTO[$i]->get{pk1_attr}().'-'.$arrObj{base}DTO[$i]->get{pk2_attr}());\n\n"
        + "      if ($bolAcaoConsultar) {\n"
        + f"        $strResultado .= '<a href=\"'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_consultar&acao_origem='.$strAcao.'&acao_retorno='.$strAcao.'&{pk1_param}='.$arrObj{base}DTO[$i]->get{pk1_attr}().'&{pk2_param}='.$arrObj{base}DTO[$i]->get{pk2_attr}()).'\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeConsultar().'\" title=\"Consultar {singular}\" alt=\"Consultar {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        + "      }\n\n"
        + "      if ($bolAcaoAlterar) {\n"
        + f"        $strResultado .= '<a href=\"'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_alterar&acao_origem='.$strAcao.'&acao_retorno='.$strAcao.'&{pk1_param}='.$arrObj{base}DTO[$i]->get{pk1_attr}().'&{pk2_param}='.$arrObj{base}DTO[$i]->get{pk2_attr}()).'\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeAlterar().'\" title=\"Alterar {singular}\" alt=\"Alterar {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        + "      }\n\n"
        + "      if ($bolAcaoExcluir) {\n"
        + f"        $strId = $arrObj{base}DTO[$i]->get{pk1_attr}().'-'.$arrObj{base}DTO[$i]->get{pk2_attr}();\n"
        + f"        $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript({check_description});\n"
        + f"        $strResultado .= '<a href=\"'.PaginaSEI::getInstance()->montarAncora($strId).'\" onclick=\"acaoExcluir(\\''.$strId.'\\',\\''.$strDescricao.'\\');\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeExcluir().'\" title=\"Excluir {singular}\" alt=\"Excluir {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        + "      }\n\n"
        + "      $strResultado .= '</td></tr>'.\"\\n\";\n"
        + "    }\n"
        + "    $strResultado .= '</tbody>'.\"\\n\";\n"
        + "    $strResultado .= '</table>';\n"
        + "  }\n"
        + f"  if ($strAcao==='{table_name}_selecionar') {{\n"
        + '    $arrComandos[] = \'<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>\';\n'
        + "  } else {\n"
        + '    $arrComandos[] = \'<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.$strAcao).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>\';\n'
        + "  }\n\n"
        + filter_selects
        + "} catch (Exception $e) {\n"
        + "  PaginaSEI::getInstance()->processarExcecao($e);\n"
        + "}\n\n"
        + "PaginaSEI::getInstance()->montarDocType();\n"
        + "PaginaSEI::getInstance()->abrirHtml();\n"
        + "PaginaSEI::getInstance()->abrirHead();\n"
        + "PaginaSEI::getInstance()->montarMeta();\n"
        + "PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema().' - '.($strTitulo??false));\n"
        + "PaginaSEI::getInstance()->montarStyle();\n"
        + "PaginaSEI::getInstance()->abrirStyle();\n"
        + "?>\n"
        + "<?php if(0){?><style><?php }?>\n"
        + style_parts
        + "<?php if(0){?></style><?php }?>\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharStyle();\n"
        + "PaginaSEI::getInstance()->montarJavaScript();\n"
        + "PaginaSEI::getInstance()->abrirJavaScript();\n"
        + "?>\n"
        + '<?php if(0){?><script type="text/javascript"><?php }?>\n\n'
        + "function inicializar()\n{\n"
        + f"  if ('<?=$strAcao??false?>' === '{table_name}_selecionar') {{\n"
        + "    infraReceberSelecao();\n"
        + "    document.getElementById('btnFecharSelecao').focus();\n"
        + "  } else {\n"
        + "    document.getElementById('btnFechar').focus();\n"
        + "  }\n"
        + "  infraEfeitoTabelas(true);\n}\n\n"
        + "<?php if ($bolAcaoExcluir??false) { ?>\n"
        + "function acaoExcluir(id,desc)\n{\n"
        + f"  if (confirm('Confirma exclus\u00e3o d{article} {singular} \"' + desc + '\"?')) {{\n"
        + "    document.getElementById('hdnInfraItemId').value=id;\n"
        + f"    document.getElementById('frm{base}Lista').action='<?=$strLinkExcluir??false?>';\n"
        + f"    document.getElementById('frm{base}Lista').submit();\n"
        + "  }\n}\n\n"
        + "function acaoExclusaoMultipla()\n{\n"
        + f"  if (document.getElementById('hdnInfraItensSelecionados').value=='') {{\n"
        + f"    alert('Nenhum{'' if article == 'o' else 'a'} {singular} selecionad{article}.');\n"
        + "    return;\n  }\n"
        + f"  if (confirm('Confirma exclus\u00e3o d{article}s {singular}s selecionad{article}s?')) {{\n"
        + "    document.getElementById('hdnInfraItemId').value='';\n"
        + f"    document.getElementById('frm{base}Lista').action='<?=$strLinkExcluir??false?>';\n"
        + f"    document.getElementById('frm{base}Lista').submit();\n"
        + "  }\n}\n"
        + "<?php } ?>\n\n"
        + "<?php if(0){?></script><?php }?>\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharJavaScript();\n"
        + "PaginaSEI::getInstance()->fecharHead();\n"
        + "PaginaSEI::getInstance()->abrirBody($strTitulo??false, 'onload=\"inicializar();\"');\n"
        + "?>\n"
        + f"<form id=\"frm{base}Lista\" method=\"post\" action=\"<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.$strAcao.'&acao_origem='.$strAcao)?>\">\n"
        + "  <?php\n"
        + "  PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);\n"
        + "  ?>\n"
        + filter_form
        + "  <?php\n"
        + "  PaginaSEI::getInstance()->montarAreaTabela($strResultado??false,$numRegistros??false);\n"
        + "  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);\n"
        + "  ?>\n"
        + "</form>\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharBody();\n"
        + "PaginaSEI::getInstance()->fecharHtml();\n"
    )


def render_cadastro_nn(data: dict) -> str:
    """Render cadastro page for N:N (composite PK) entities."""
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = q(data["entidade"]["singular"])
    article = data["entidade"]["artigo"]
    nn_rels = data["relacionamentosNn"]
    pk1_col = [c for c in data["colunas"] if c.get("chavePrimaria")][0]
    pk2_col = [c for c in data["colunas"] if c.get("chavePrimaria")][1]
    pk1_attr = attribute_name(pk1_col)
    pk2_attr = attribute_name(pk2_col)
    pk1_param = pk1_col["nome"]
    pk2_param = pk2_col["nome"]

    # extra (non-PK) columns, com os rotulos de ui.campos
    ui_map = data.get("ui", {}).get("campos", {})
    extra_cols = []
    for c in data["colunas"]:
        if c.get("chavePrimaria"):
            continue
        cloned = dict(c)
        cloned["_ui"] = ui_map.get(c["nome"])
        extra_cols.append(cloned)
    words = genero_words(article)

    sel_names = ", ".join("'sel" + class_base(r["tabelaOrigem"]) + "'" for r in nn_rels)

    # build select blocks for each FK
    select_vars = ""
    select_post_blocks = ""
    select_form_blocks = ""
    style_parts = ""
    for rel in nn_rels:
        rel_base = class_base(rel["tabelaOrigem"])
        pk_attr_here = pk1_attr if rel == nn_rels[0] else pk2_attr
        label = rel.get("rotulo", rel_base)
        ak = (rel.get("teclaAtalho") or label[0]).lower()
        select_vars += (
            f"  $numId{rel_base} = PaginaSEI::getInstance()->recuperarCampo('sel{rel_base}');\n"
            f"  if ($numId{rel_base} !=='') {{\n"
            f"    $obj{base}DTO->set{pk_attr_here}($numId{rel_base});\n"
            f"  }} else {{\n"
            f"    $obj{base}DTO->set{pk_attr_here}(null);\n"
            f"  }}\n\n"
        )
        select_post_blocks += (
            "      $obj"
            + base
            + "DTO->set"
            + pk_attr_here
            + "(PaginaSEI::POST('hdn"
            + (pk_attr_here[3:] if pk_attr_here.startswith("Num") else pk_attr_here)
            + "'));\n"
        )
        select_form_blocks += (
            f"<?php\nPaginaSEI::getInstance()->abrirAreaDados('5em');\n?>\n"
            f'  <label id="lbl{rel_base}" for="sel{rel_base}" accesskey="{ak}" class="infraLabelObrigatorio">{_label_with_accesskey(label, ak)}:</label>\n'
            f'  <select id="sel{rel_base}" name="sel{rel_base}" class="infraSelect" '
            f'tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" <?=$strDesabilitar?>>\n'
            f"  <?=$strItensSel{rel_base}??false?>\n  </select>\n"
            f"<?php\nPaginaSEI::getInstance()->fecharAreaDados();\n?>\n"
        )
        style_parts += (
            f"#lbl{rel_base} {{position:absolute;left:0;top:0;width:25%;}}\n"
            f"#sel{rel_base} {{position:absolute;left:0;top:40%;width:25%;}}\n\n"
        )

    # build extra field form blocks and validation
    extra_form = ""
    extra_js_validation = ""
    extra_post_block = ""
    for col in extra_cols:
        col_attr = attribute_name(col)
        col_label = ui_label(col)
        col_suffix = attr_suffix_from_attr(col_attr)
        html_name = "txt" + col_suffix
        col_ui = col.get("_ui") or {}
        ak = (col_ui.get("teclaAtalho") or "").lower()
        ak_attr = f' accesskey="{ak}"' if ak else ""
        artigo = column_article(col)
        extra_post_block += (
            f"      $obj{base}DTO->set{col_attr}(PaginaSEI::POST('{html_name}'));\n"
        )
        style_parts += (
            f"#lbl{col_suffix} {{position:absolute;left:0;top:0;width:25%;}}\n"
            f"#{html_name} {{position:absolute;left:0;top:40%;width:25%;}}\n\n"
        )
        col_is_required = col.get("obrigatorio", False)
        col_label_class = "infraLabelObrigatorio" if col_is_required else "infraLabelOpcional"
        label_html = _label_with_accesskey(col_label, ak)
        if col["tipoBanco"] in {"datetime", "date", "timestamp"}:
            is_datetime = col_attr.startswith("Dth")
            mascara = "infraMascaraDataHora" if is_datetime else "infraMascaraData"
            validar = "infraValidarDataHora" if is_datetime else "infraValidarData"
            style_parts += f"#imgCal{col_suffix} {{position:absolute;left:26%;top:45%;}}\n\n"
            extra_form += (
                f"<?php\nPaginaSEI::getInstance()->abrirAreaDados('5em');\n?>\n"
                f'  <label id="lbl{col_suffix}" for="{html_name}"{ak_attr} class="{col_label_class}">{label_html}:</label>\n'
                f'  <input type="text" id="{html_name}" name="{html_name}" onkeypress="return {mascara}(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{col_attr}())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                f'  <img id="imgCal{col_suffix}" title="Selecionar {col_label}" alt="Selecionar {col_label}" src="<?=PaginaSEI::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario(\'{html_name}\',this);" />\n'
                f"<?php\nPaginaSEI::getInstance()->fecharAreaDados();\n?>\n"
            )
            if col_is_required:
                extra_js_validation += (
                    f"\n  if (infraTrim(document.getElementById('{html_name}').value)=='') {{\n"
                    f"    alert('Informe {artigo} {q(col_label)}.');\n"
                    f"    document.getElementById('{html_name}').focus();\n"
                    f"    return false;\n  }}\n\n"
                    f"  if (!{validar}(document.getElementById('{html_name}'))) {{\n"
                    f"    return false;\n  }}\n"
                )
        else:
            if col["tipoBanco"] == "numeric" and col_attr.startswith("Din"):
                mascara_attr = ' onkeydown="return infraMascaraDinheiro(this, event)"'
            elif col["tipoBanco"] == "numeric":
                mascara_attr = ' onkeypress="return infraMascaraNumero(this, event)"'
            elif col.get("tamanho"):
                mascara_attr = f' onkeypress="return infraMascaraTexto(this,event,{col["tamanho"]});" maxlength="{col["tamanho"]}"'
            else:
                mascara_attr = ""
            extra_form += (
                f"<?php\nPaginaSEI::getInstance()->abrirAreaDados('5em');\n?>\n"
                f'  <label id="lbl{col_suffix}" for="{html_name}"{ak_attr} class="{col_label_class}">{label_html}:</label>\n'
                f'  <input type="text" id="{html_name}" name="{html_name}" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{col_attr}())?>"{mascara_attr} tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                f"<?php\nPaginaSEI::getInstance()->fecharAreaDados();\n?>\n"
            )
            if col_is_required:
                extra_js_validation += (
                    f"\n  if (infraTrim(document.getElementById('{html_name}').value)=='') {{\n"
                    f"    alert('Informe {artigo} {q(col_label)}.');\n"
                    f"    document.getElementById('{html_name}').focus();\n"
                    f"    return false;\n  }}\n"
                )

    # JS validation for selects
    js_sel_validation = ""
    for rel in nn_rels:
        rel_base = class_base(rel["tabelaOrigem"])
        label = rel.get("rotulo", rel_base)
        rel_article = "a" if rel.get("artigo") == "a" else "o"
        js_sel_validation += (
            f"  if (!infraSelectSelecionado('sel{rel_base}')) {{\n"
            f"    alert('Selecione {'uma' if rel_article == 'a' else 'um'} {q(label)}.');\n"
            f"    document.getElementById('sel{rel_base}').focus();\n"
            f"    return false;\n  }}\n\n"
        )

    # hidden fields for alterar
    hidden_pks = "".join(
        f'  <input type="hidden" id="hdn{attr_suffix_from_attr(pk_attr)}" name="hdn{attr_suffix_from_attr(pk_attr)}" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{pk_attr}())?>" />\n'
        for pk_attr in [pk1_attr, pk2_attr]
    )

    # select_int calls
    sel_int_calls = ""
    for rel in nn_rels:
        rel_base = class_base(rel["tabelaOrigem"])
        pk_attr_here = pk1_attr if rel == nn_rels[0] else pk2_attr
        sel_int_calls += f"  $strItensSel{rel_base} = {rel['classeInt']}::{rel['metodoInt']}('null','&nbsp;',$obj{base}DTO->get{pk_attr_here}());\n"

    pk1_suffix = pk1_attr[3:] if pk1_attr.startswith("Num") else pk1_attr
    pk2_suffix = pk2_attr[3:] if pk2_attr.startswith("Num") else pk2_attr

    return (
        php_header()
        + "\n\ntry {\n"
        + page_require_sei()
        + "  session_start();\n\n"
        + "  //////////////////////////////////////////////////////////////////////////////\n"
        + "  //InfraDebug::getInstance()->setBolLigado(false);\n"
        + "  //InfraDebug::getInstance()->setBolDebugInfra(true);\n"
        + "  //InfraDebug::getInstance()->limpar();\n"
        + "  //////////////////////////////////////////////////////////////////////////////\n\n"
        + "  SessaoSEI::getInstance()->validarLink();\n\n"
        + "  $strAcao = PaginaSEI::GET('acao');\n"
        + "  SessaoSEI::getInstance()->validarPermissao($strAcao);\n\n"
        + f"  PaginaSEI::getInstance()->verificarSelecao('{table_name}_selecionar');\n\n"
        + f"  PaginaSEI::getInstance()->salvarCamposPost([{sel_names}]);\n\n"
        + f"  $obj{base}DTO = new {base}DTO();\n"
        + "  $strDesabilitar = '';\n"
        + "  $arrComandos = [];\n\n"
        + "  switch ($strAcao) {\n"
        + f"    case '{table_name}_cadastrar':\n"
        + f"      $strTitulo = 'Nov{article} {singular}';\n"
        + f'      $arrComandos[] = \'<button type="submit" accesskey="S" name="sbmCadastrar{base}" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>\';\n'
        + f'      $arrComandos[] = \'<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.$strAcao).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>\';\n\n'
        + select_vars
        + extra_post_block
        + f"\n      if (PaginaSEI::POST('sbmCadastrar{base}') !== null) {{\n"
        + f"        try {{\n"
        + f"          $obj{base}RN = new {base}RN();\n"
        + f"          $obj{base}DTO = $obj{base}RN->cadastrar($obj{base}DTO);\n"
        + f"          PaginaSEI::getInstance()->adicionarMensagem('{singular} cadastrad{article} com sucesso.');\n"
        + f"          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$strAcao.'&{pk1_param}='.$obj{base}DTO->get{pk1_attr}().'&{pk2_param}='.$obj{base}DTO->get{pk2_attr}().PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk1_attr}().'-'.$obj{base}DTO->get{pk2_attr}())));\n"
        + "          die;\n"
        + "        } catch (Exception $e) {\n"
        + "          PaginaSEI::getInstance()->processarExcecao($e);\n"
        + "        }\n"
        + "      }\n"
        + "      break;\n\n"
        + f"    case '{table_name}_alterar':\n"
        + f"      $strTitulo = 'Alterar {singular}';\n"
        + f'      $arrComandos[] = \'<button type="submit" accesskey="S" name="sbmAlterar{base}" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>\';\n'
        + "      $strDesabilitar = 'disabled=\"disabled\"';\n\n"
        + f"      if (PaginaSEI::GET('{pk1_param}') !== null && PaginaSEI::GET('{pk2_param}') !== null) {{\n"
        + f"        $obj{base}DTO->set{pk1_attr}((int)PaginaSEI::GET('{pk1_param}'));\n"
        + f"        $obj{base}DTO->set{pk2_attr}((int)PaginaSEI::GET('{pk2_param}'));\n"
        + f"        $obj{base}DTO->retTodos();\n"
        + f"        $obj{base}RN = new {base}RN();\n"
        + f"        $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n"
        + f"        if ($obj{base}DTO===null) {{\n"
        + f"          throw new InfraException('{singular} não {words['encontrado']}.');\n"
        + "        }\n"
        + "      } else {\n"
        + select_post_blocks
        + extra_post_block
        + "      }\n\n"
        + f'      $arrComandos[] = \'<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.$strAcao.PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk1_attr}().\'-\'.$obj{base}DTO->get{pk2_attr}())).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>\';\n\n'
        + f"      if (PaginaSEI::POST('sbmAlterar{base}') !== null) {{\n"
        + f"        try {{\n"
        + f"          $obj{base}RN = new {base}RN();\n"
        + f"          $obj{base}RN->alterar($obj{base}DTO);\n"
        + f"          PaginaSEI::getInstance()->adicionarMensagem('{singular} alterad{'o' if article == 'o' else 'a'} com sucesso.');\n"
        + f"          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$strAcao.PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk1_attr}().'-'.$obj{base}DTO->get{pk2_attr}())));\n"
        + "          die;\n"
        + "        } catch (Exception $e) {\n"
        + "          PaginaSEI::getInstance()->processarExcecao($e);\n"
        + "        }\n"
        + "      }\n"
        + "      break;\n\n"
        + f"    case '{table_name}_consultar':\n"
        + f"      $strTitulo = 'Consultar {singular}';\n"
        + f"      $arrComandos[] = '<button type=\"button\" accesskey=\"F\" name=\"btnFechar\" value=\"Fechar\" onclick=\"location.href=\\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$strAcao.PaginaSEI::getInstance()->montarAncora(PaginaSEI::GET('{pk1_param}').'-'.PaginaSEI::GET('{pk2_param}'))).'\\';\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">F</span>echar</button>';\n"
        + f"      $obj{base}DTO->set{pk1_attr}((int)PaginaSEI::GET('{pk1_param}'));\n"
        + f"      $obj{base}DTO->set{pk2_attr}((int)PaginaSEI::GET('{pk2_param}'));\n"
        + f"      $obj{base}DTO->setBolExclusaoLogica(false);\n"
        + f"      $obj{base}DTO->retTodos();\n"
        + f"      $obj{base}RN = new {base}RN();\n"
        + f"      $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n"
        + f"      if ($obj{base}DTO===null) {{\n"
        + f"        throw new InfraException('{singular} não {words['encontrado']}.');\n"
        + "      }\n"
        + "      break;\n\n"
        + "    default:\n"
        + "      throw new InfraException(\"Ação '\" . $strAcao . \"' não reconhecida.\");\n"
        + "  }\n\n"
        + sel_int_calls
        + "\n} catch(Exception $e) {\n"
        + "  PaginaSEI::getInstance()->processarExcecao($e);\n"
        + "}\n\n"
        + "PaginaSEI::getInstance()->montarDocType();\n"
        + "PaginaSEI::getInstance()->abrirHtml();\n"
        + "PaginaSEI::getInstance()->abrirHead();\n"
        + "PaginaSEI::getInstance()->montarMeta();\n"
        + "PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema() . ' - ' . ($strTitulo??false));\n"
        + "PaginaSEI::getInstance()->montarStyle();\n"
        + "PaginaSEI::getInstance()->abrirStyle();\n"
        + "?>\n"
        + "<?php if(0){?><style><?php }?>\n"
        + style_parts
        + "<?php if(0){?></style><?php }?>\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharStyle();\n"
        + "PaginaSEI::getInstance()->montarJavaScript();\n"
        + "PaginaSEI::getInstance()->abrirJavaScript();\n"
        + "?>\n"
        + '<?php if(0){?><script type="text/javascript"><?php }?>\n\n'
        + "function inicializar()\n{\n"
        + f"  if ('<?=$strAcao??false?>' === '{table_name}_cadastrar') {{\n"
        + "    document.getElementById('sel"
        + class_base(nn_rels[0]["tabelaOrigem"])
        + "').focus();\n"
        + f"  }} else if ('<?=$strAcao??false?>' === '{table_name}_consultar') {{\n"
        + "    infraDesabilitarCamposAreaDados();\n"
        + "  } else {\n"
        + "    document.getElementById('btnCancelar').focus();\n"
        + "  }\n"
        + "  infraEfeitoTabelas(true);\n}\n\n"
        + "function validarCadastro()\n{\n"
        + js_sel_validation
        + extra_js_validation
        + "\n  return true;\n}\n\n"
        + "function OnSubmitForm()\n{\n  return validarCadastro();\n}\n\n"
        + "<?php if(0){?></script><?php }?>\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharJavaScript();\n"
        + "PaginaSEI::getInstance()->fecharHead();\n"
        + "PaginaSEI::getInstance()->abrirBody($strTitulo??false,'onload=\"inicializar();\"');\n"
        + "?>\n"
        + f"<form id=\"frm{base}Cadastro\" method=\"post\" onsubmit=\"return OnSubmitForm();\" action=\"<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.$strAcao.'&acao_origem='.$strAcao)?>\">\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);\n"
        + "?>\n"
        + select_form_blocks
        + extra_form
        + hidden_pks
        + "  <?php\n"
        + "  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);\n"
        + "  ?>\n"
        + "</form>\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharBody();\n"
        + "PaginaSEI::getInstance()->fecharHtml();\n"
    )


def php_block_comment(block: str) -> str:
    """Envolve um bloco PHP em /* */ preservando a indentacao, como o gabarito TRF4 faz sem sin_ativo."""
    return "/*\n" + block + "\n*/"


def id_loop_lines(base: str, pk_attr: str, singular: str, words: dict) -> str:
    return (
        f"$arrObj{base}DTO = [];\n"
        f"foreach ($arrStrIds as $strId) {{\n"
        f"  if (!ctype_digit((string)$strId)) {{\n"
        f"    throw new InfraException('Identificador {words['do']} {singular} inválido.');\n"
        f"  }}\n"
        f"  $obj{base}DTO = new {base}DTO();\n"
        f"  $obj{base}DTO->set{pk_attr}((int)$strId);\n"
        f"  $arrObj{base}DTO[] = $obj{base}DTO;\n"
        f"}}"
    )


def bulk_action_case(table_name: str, base: str, pk_attr: str, singular: str, words: dict, action: str) -> str:
    return (
        f"case '{table_name}_{action}':\n"
        f"  try {{\n"
        f"    $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();\n"
        + indent(id_loop_lines(base, pk_attr, singular, words), "    ")
        + f"\n    $obj{base}RN = new {base}RN();\n"
        f"    $obj{base}RN->{action}($arrObj{base}DTO);\n"
        f"    PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');\n"
        f"  }} catch (Exception $e) {{\n"
        f"    PaginaSEI::getInstance()->processarExcecao($e);\n"
        f"  }}\n"
        f"  header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.$strAcao));\n"
        f"  die;"
    )


def confirm_js(base: str, action: str, verbo: str, singular: str, plural: str, words: dict, flag: str, link: str) -> str:
    fn = {"desativar": "Desativar", "reativar": "Reativar", "excluir": "Excluir"}[action]
    multi = {"desativar": "Desativacao", "reativar": "Reativacao", "excluir": "Exclusao"}[action]
    return (
        f"<?php if (${flag}??false) {{ ?>\n"
        f"function acao{fn}(id,desc)\n{{\n"
        f"  if (confirm('Confirma {verbo} {words['do']} {singular} \"' + desc + '\"?')) {{\n"
        f"    document.getElementById('hdnInfraItemId').value=id;\n"
        f"    document.getElementById('frm{base}Lista').action='<?=${link}??false?>';\n"
        f"    document.getElementById('frm{base}Lista').submit();\n"
        f"  }}\n}}\n\n"
        f"function acao{multi}Multipla()\n{{\n"
        f"  if (document.getElementById('hdnInfraItensSelecionados').value=='') {{\n"
        f"    alert('{words['nenhum']} {singular} {words['selecionado']}.');\n"
        f"    return;\n  }}\n"
        f"  if (confirm('Confirma {verbo} {words['dos']} {plural} {words['selecionados']}?')) {{\n"
        f"    document.getElementById('hdnInfraItemId').value='';\n"
        f"    document.getElementById('frm{base}Lista').action='<?=${link}??false?>';\n"
        f"    document.getElementById('frm{base}Lista').submit();\n"
        f"  }}\n}}\n"
        f"<?php }} ?>"
    )


def render_lista(data: dict) -> str:
    if is_nn(data):
        return render_lista_nn(data)
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = q(data["entidade"]["singular"])
    plural = q(data["entidade"]["plural"])
    article = data["entidade"]["artigo"]
    display_field = data["entidade"]["campoPrincipal"]
    display_column = next(
        column for column in data["colunas"] if column["nome"] == display_field
    )
    display_attr = attribute_name(display_column)
    display_suffix = attr_suffix_from_attr(display_attr)
    pk_column = next(
        column for column in data["colunas"] if column.get("chavePrimaria")
    )
    pk_attr = attribute_name(pk_column)
    pk_param = pk_column["nome"]
    has_logical_delete = bool(data["regrasGeracao"].get("campoSinAtivo"))
    ui_map = data.get("ui", {}).get("campos", {})
    display_label = q(ui_map.get(display_field, {}).get(
        "rotulo", ui_label(display_column)
    ))
    words = genero_words(article)
    new_label = words["novo"]

    relations = data.get("relacionamentos", [])
    post_persistence = ""
    filter_apply_parts = []
    filter_select_parts = []
    filter_form_parts = []
    style_parts = []
    if relations:
        sel_names = []
        for rel in relations:
            fk_column = next(c for c in data["colunas"] if c["nome"] == rel["coluna"])
            fk_attr = attribute_name(fk_column)
            sel_key = fk_suffix_of(data, rel)
            sel_key = sel_key[2:] if sel_key.startswith("Id") else sel_key
            rel_base = class_base(rel["tabelaReferencia"])
            rel_ui = ui_map.get(rel["coluna"], {})
            rel_label = rel_ui.get("rotulo", pascal_case(rel["coluna"]))
            rel_accesskey = rel_ui.get("teclaAtalho", "")
            rel_var = f"$numId{sel_key}"
            rel_helper = f"montarSelect{pascal_case(strip_common_prefixes(rel['campoExibicao']))}"
            sel_names.append(f"'sel{sel_key}'")

            filter_apply_parts.append(
                f"{rel_var} = PaginaSEI::getInstance()->recuperarCampo('sel{sel_key}');\n"
                f"if ({rel_var}!=='') {{\n"
                f"  $obj{base}DTO->set{fk_attr}((int){rel_var});\n"
                f"}}"
            )
            filter_select_parts.append(
                f"$strItensSel{sel_key} = {rel_base}INT::{rel_helper}('', 'Todos', {rel_var});"
            )
            label_html = _label_with_accesskey(rel_label, rel_accesskey)
            accesskey_attr = f' accesskey="{rel_accesskey.lower()}"' if rel_accesskey else ""
            filter_form_parts.append(
                "PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                "?>\n"
                f'  <label id="lbl{sel_key}" for="sel{sel_key}"{accesskey_attr} class="infraLabelOpcional">{label_html}:</label>\n'
                f'  <select id="sel{sel_key}" name="sel{sel_key}" onchange="this.form.submit();" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>">\n'
                f"  <?=$strItensSel{sel_key}??false?>\n"
                "  </select>\n"
                "<?php\n"
                "PaginaSEI::getInstance()->fecharAreaDados();"
            )
            style_parts.append(
                f"#lbl{sel_key} {{position:absolute;left:0;top:0;width:25%;}}\n"
                f"#sel{sel_key} {{position:absolute;left:0;top:40%;width:25%;}}"
            )
        post_persistence = f"PaginaSEI::getInstance()->salvarCamposPost([{', '.join(sel_names)}]);"

    # Blocos de sin_ativo: identicos nos dois modos; sem sin_ativo saem comentados, como o gabarito TRF4
    logical_cases = (
        bulk_action_case(table_name, base, pk_attr, singular, words, "desativar")
        + "\n\n"
        + bulk_action_case(table_name, base, pk_attr, singular, words, "reativar")
    )
    logical_bulk = (
        "if ($bolAcaoDesativar) {\n"
        "  $bolCheck = true;\n"
        "  $arrComandos[] = '<button type=\"button\" accesskey=\"t\" id=\"btnDesativar\" value=\"Desativar\" onclick=\"acaoDesativacaoMultipla();\" class=\"infraButton\">Desa<span class=\"infraTeclaAtalho\">t</span>ivar</button>';\n"
        f"  $strLinkDesativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_desativar&acao_origem='.$strAcao);\n"
        "}\n\n"
        "if ($bolAcaoReativar) {\n"
        "  $bolCheck = true;\n"
        "  $arrComandos[] = '<button type=\"button\" accesskey=\"R\" id=\"btnReativar\" value=\"Reativar\" onclick=\"acaoReativacaoMultipla();\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">R</span>eativar</button>';\n"
        f"  $strLinkReativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_reativar&acao_origem='.$strAcao);\n"
        "}"
    )
    logical_row = (
        f"if ($bolAcaoDesativar && $arrObj{base}DTO[$i]->getStrSinAtivo() == 'S') {{\n"
        f"  $strResultado .= '<a href=\"'.PaginaSEI::getInstance()->montarAncora($strId).'\" onclick=\"acaoDesativar(\\''.$strId.'\\',\\''.$strDescricao.'\\');\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeDesativar().'\" title=\"Desativar {singular}\" alt=\"Desativar {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        "}\n\n"
        f"if ($bolAcaoReativar && $arrObj{base}DTO[$i]->getStrSinAtivo() == 'N') {{\n"
        f"  $strResultado .= '<a href=\"'.PaginaSEI::getInstance()->montarAncora($strId).'\" onclick=\"acaoReativar(\\''.$strId.'\\',\\''.$strDescricao.'\\');\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeReativar().'\" title=\"Reativar {singular}\" alt=\"Reativar {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        "}"
    )
    logical_js = (
        confirm_js(base, "desativar", "desativação", singular, plural, words, "bolAcaoDesativar", "strLinkDesativar")
        + "\n\n"
        + confirm_js(base, "reativar", "reativação", singular, plural, words, "bolAcaoReativar", "strLinkReativar")
    )
    if has_logical_delete:
        logical_flags_else = (
            f"  $bolAcaoReativar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_reativar');\n"
            f"  $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_desativar');\n"
        )
        filter_apply_extra = (
            f"$obj{base}DTO->setBolExclusaoLogica(false);\n"
            f"if ($strAcao==='{table_name}_selecionar') {{\n"
            f"  $obj{base}DTO->setStrSinAtivo('S');\n"
            f"}}"
        )
        tr_color_logic = (
            f"if ($arrObj{base}DTO[$i]->getStrSinAtivo() == 'S') {{\n"
            "  $strCssTr = ($strCssTr === '<tr class=\"infraTrClara\">') ? '<tr class=\"infraTrEscura\">' : '<tr class=\"infraTrClara\">';\n"
            "} else {\n"
            "  $strCssTr = '<tr class=\"trVermelha\">';\n"
            "}\n"
            "$strResultado .= $strCssTr;"
        )
    else:
        logical_cases = php_block_comment(logical_cases)
        logical_bulk = php_block_comment(logical_bulk)
        logical_row = php_block_comment(logical_row)
        logical_js = "<?php /* " + logical_js[len("<?php "):-len(" ?>")] + " */ ?>"
        logical_flags_else = "  $bolAcaoReativar = false;\n  $bolAcaoDesativar = false;\n"
        filter_apply_extra = ""
        tr_color_logic = (
            "$strCssTr = ($strCssTr === '<tr class=\"infraTrClara\">') ? '<tr class=\"infraTrEscura\">' : '<tr class=\"infraTrClara\">';\n"
            "$strResultado .= $strCssTr;"
        )

    action_flags = (
        f"if ($strAcao==='{table_name}_selecionar') {{\n"
        "  $bolAcaoReativar = false;\n"
        f"  $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');\n"
        f"  $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');\n"
        "  $bolAcaoImprimir = false;\n"
        "  $bolAcaoExcluir = false;\n"
        "  $bolAcaoDesativar = false;\n"
        "  $bolCheck = true;\n"
        "} else {\n"
        + logical_flags_else
        + f"  $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');\n"
        f"  $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');\n"
        "  $bolAcaoImprimir = true;\n"
        f"  $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('{table_name}_excluir');\n"
        "}"
    )
    bulk_commands = (
        logical_bulk
        + "\n\n"
        "if ($bolAcaoExcluir) {\n"
        "  $bolCheck = true;\n"
        "  $arrComandos[] = '<button type=\"button\" accesskey=\"E\" id=\"btnExcluir\" value=\"Excluir\" onclick=\"acaoExclusaoMultipla();\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">E</span>xcluir</button>';\n"
        f"  $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_excluir&acao_origem='.$strAcao);\n"
        "}"
    )
    js_functions = (
        logical_js
        + "\n\n"
        + confirm_js(base, "excluir", "exclusão", singular, plural, words, "bolAcaoExcluir", "strLinkExcluir")
    )

    switch_cases = (
        bulk_action_case(table_name, base, pk_attr, singular, words, "excluir")
        + "\n\n"
        + logical_cases
        + "\n\n"
        f"case '{table_name}_selecionar':\n"
        f"  $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar {singular}','Selecionar {plural}');\n"
        "  //Se cadastrou alguem\n"
        f"  if (PaginaSEI::GET('acao_origem')==='{table_name}_cadastrar' && PaginaSEI::GET('{pk_param}') !== null) {{\n"
        f"    PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('{pk_param}'));\n"
        "  }\n"
        "  break;\n\n"
        f"case '{table_name}_listar':\n"
        f"  $strTitulo = '{plural}';\n"
        "  break;"
    )

    top_commands = (
        f"if ($strAcao==='{table_name}_selecionar') {{\n"
        "  $arrComandos[] = '<button type=\"button\" accesskey=\"T\" id=\"btnTransportarSelecao\" value=\"Transportar\" onclick=\"infraTransportarSelecao();\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">T</span>ransportar</button>';\n"
        "}\n\n"
        f"$bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_cadastrar');\n"
        "if ($bolAcaoCadastrar) {\n"
        f"  $arrComandos[] = '<button type=\"button\" accesskey=\"N\" id=\"btn{new_label}\" value=\"{new_label}\" onclick=\"location.href=\\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_cadastrar&acao_origem='.$strAcao.'&acao_retorno='.$strAcao).'\\'\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">N</span>{new_label[1:]}</button>';\n"
        "}"
    )

    # Retornos: PK e campo principal ativos; demais colunas e atributos relacionados comentados (andaime do gabarito)
    return_lines = [f"$obj{base}DTO->ret{pk_attr}();", f"$obj{base}DTO->ret{display_attr}();"]
    if has_logical_delete:
        return_lines.append(f"$obj{base}DTO->retStrSinAtivo();")
    for column in data["colunas"]:
        if column.get("chavePrimaria") or column["nome"] in {display_field, "sin_ativo"}:
            continue
        return_lines.append(f"//$obj{base}DTO->ret{attribute_name(column)}();")
    for rel in relations:
        return_lines.append(f"//$obj{base}DTO->ret{related_attribute_name(data, rel)}();")
    dto_return_lines = "\n".join(return_lines)

    filter_apply_lines = "\n".join(filter_apply_parts)
    if filter_apply_extra:
        filter_apply_lines = (filter_apply_lines + "\n" + filter_apply_extra).strip()
    scope_line = scope_filter_line(data, base, "").rstrip("\n")
    if scope_line:
        filter_apply_lines = (filter_apply_lines + "\n" + scope_line).strip()
    pagination_comment = "" if has_pagination(data) else "//"

    header_lines = (
        "if ($bolCheck) {\n"
        "  $strResultado .= '<th class=\"infraTh\" style=\"width: 1%\">'.PaginaSEI::getInstance()->getThCheck().'</th>' . \"\\n\";\n"
        "}\n"
        f"$strResultado .= '<th class=\"infraTh\">'.PaginaSEI::getInstance()->getThOrdenacao($obj{base}DTO,'{display_label}','{display_suffix}',$arrObj{base}DTO).'</th>' . \"\\n\";\n"
        "$strResultado .= '<th class=\"infraTh\">Ações</th>' . \"\\n\";"
    )

    row_lines = (
        "if ($bolCheck) {\n"
        f"  $strResultado .= '<td style=\"vertical-align: middle\">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObj{base}DTO[$i]->get{pk_attr}(),$arrObj{base}DTO[$i]->get{display_attr}()).'</td>';\n"
        "}\n"
        f"$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObj{base}DTO[$i]->get{display_attr}()).'</td>';\n"
        "$strResultado .= '<td style=\"text-align: center\">';\n"
        f"$strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObj{base}DTO[$i]->get{pk_attr}());\n\n"
        "if ($bolAcaoConsultar) {\n"
        f"  $strResultado .= '<a href=\"'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_consultar&acao_origem='.$strAcao.'&acao_retorno='.$strAcao.'&{pk_param}='.$arrObj{base}DTO[$i]->get{pk_attr}()).'\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeConsultar().'\" title=\"Consultar {singular}\" alt=\"Consultar {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        "}\n\n"
        "if ($bolAcaoAlterar) {\n"
        f"  $strResultado .= '<a href=\"'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_alterar&acao_origem='.$strAcao.'&acao_retorno='.$strAcao.'&{pk_param}='.$arrObj{base}DTO[$i]->get{pk_attr}()).'\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeAlterar().'\" title=\"Alterar {singular}\" alt=\"Alterar {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        "}\n\n"
        "if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {\n"
        f"  $strId = $arrObj{base}DTO[$i]->get{pk_attr}();\n"
        f"  $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript($arrObj{base}DTO[$i]->get{display_attr}());\n"
        "}\n\n"
        + logical_row
        + "\n\n"
        "if ($bolAcaoExcluir) {\n"
        f"  $strResultado .= '<a href=\"'.PaginaSEI::getInstance()->montarAncora($strId).'\" onclick=\"acaoExcluir(\\''.$strId.'\\',\\''.$strDescricao.'\\');\" tabindex=\"'.PaginaSEI::getInstance()->getProxTabTabela().'\"><img src=\"'.PaginaSEI::getInstance()->getIconeExcluir().'\" title=\"Excluir {singular}\" alt=\"Excluir {singular}\" class=\"infraImg\" /></a>&nbsp;';\n"
        "}"
    )

    bottom_commands = (
        f"if ($strAcao==='{table_name}_selecionar') {{\n"
        "  $arrComandos[] = '<button type=\"button\" accesskey=\"F\" id=\"btnFecharSelecao\" value=\"Fechar\" onclick=\"window.close();\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">F</span>echar</button>';\n"
        "} else {\n"
        "  $arrComandos[] = '<button type=\"button\" accesskey=\"F\" id=\"btnFechar\" value=\"Fechar\" onclick=\"location.href=\\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$strAcao).'\\'\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">F</span>echar</button>';\n"
        "}"
    )

    initialize_lines = (
        f"if ('<?=$strAcao??false?>' === '{table_name}_selecionar') {{\n"
        "  infraReceberSelecao();\n"
        "  document.getElementById('btnFecharSelecao').focus();\n"
        "} else {\n"
        "  document.getElementById('btnFechar').focus();\n"
        "}\n"
        "infraEfeitoTabelas(true);"
    )

    template_path = Path(__file__).resolve().parent / "templates/lista.php.tpl"
    template = read_latin1(template_path)
    replacements = {
        "{{REQUIRE_SEI}}": page_require_sei().rstrip("\n"),
        "{{TABLE_NAME}}": table_name,
        "{{CLASS_NAME}}": base,
        "{{ENTITY_LABEL_PLURAL}}": plural,
        "{{LIST_POST_PERSISTENCE_LINES}}": indent(post_persistence, "  ") + ("\n" if post_persistence else ""),
        "{{LIST_SWITCH_CASES}}": indent(switch_cases, "    "),
        "{{LIST_TOP_COMMANDS}}": indent(top_commands, "  "),
        "{{LIST_DTO_RETURN_LINES}}": indent(dto_return_lines, "  "),
        "{{LIST_FILTER_APPLY_LINES}}": indent(filter_apply_lines, "  "),
        "{{LIST_SORT_FIELD}}": display_suffix,
        "{{LIST_PREPARE_PAGINATION}}": f"  {pagination_comment}PaginaSEI::getInstance()->prepararPaginacao($obj{base}DTO);",
        "{{LIST_PROCESS_PAGINATION}}": f"  {pagination_comment}PaginaSEI::getInstance()->processarPaginacao($obj{base}DTO);",
        "{{LIST_ACTION_FLAG_LINES}}": indent(action_flags, "    "),
        "{{LIST_BULK_COMMAND_LINES}}": "\n" + indent(bulk_commands, "    ") + "\n",
        "{{LIST_HEADER_LINES}}": indent(header_lines, "    "),
        "{{LIST_TR_COLOR_LOGIC}}": indent(tr_color_logic, "      "),
        "{{LIST_ROW_LINES}}": indent(row_lines, "      "),
        "{{LIST_BOTTOM_COMMANDS}}": indent(bottom_commands, "  "),
        "{{LIST_FILTER_SELECT_LINES}}": indent("\n".join(filter_select_parts), "  "),
        "{{LIST_STYLE_LINES}}": "\n".join(style_parts),
        "{{LIST_INITIALIZE_LINES}}": indent(initialize_lines, "  "),
        "{{LIST_JAVASCRIPT_FUNCTIONS}}": js_functions,
        "{{LIST_FILTER_FORM_BLOCK}}": "\n".join(filter_form_parts),
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    return template


def render_cadastro(data: dict) -> str:
    if is_nn(data):
        return render_cadastro_nn(data)
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = q(data["entidade"]["singular"])
    plural = q(data["entidade"]["plural"])
    article = data["entidade"]["artigo"]
    display_field = data["entidade"]["campoPrincipal"]
    pk_column = next(
        column for column in data["colunas"] if column.get("chavePrimaria")
    )
    pk_attr = attribute_name(pk_column)
    pk_param = pk_column["nome"]
    ui_map = data.get("ui", {}).get("campos", {})
    relations = data.get("relacionamentos", [])
    has_sin_ativo = bool(data["regrasGeracao"].get("campoSinAtivo"))
    words = genero_words(article)

    display_column = next(
        column for column in data["colunas"] if column["nome"] == display_field
    )
    display_attr = attribute_name(display_column)
    scope = scope_column(data)
    scope_name = scope["nome"] if scope else None
    scope_set_line = scope_filter_line(data, base, "      ")

    new_word = "Novo" if article == "o" else "Nova"
    created_word = "cadastrado" if article == "o" else "cadastrada"
    altered_word = "alterado" if article == "o" else "alterada"

    def col_suffix(column: dict) -> str:
        attr = attribute_name(column)
        prefix = dto_prefix(column)
        return attr[len(prefix) :] if attr.startswith(prefix) else attr

    def css_width(column: dict) -> str:
        if column.get("chaveEstrangeira"):
            return "25%"
        tipo = column["tipoBanco"]
        if tipo in {"datetime", "date", "timestamp"}:
            return "25%"
        if tipo == "varchar":
            sz = column.get("tamanho") or 0
            if sz <= 0:
                return "50%"
            if sz <= 30:
                return "20%"
            if sz <= 100:
                return "50%"
            return "95%"
        return "25%"

    # Build relation lookup
    rel_map = {}
    for rel in relations:
        rel_map[rel["coluna"]] = rel

    # Build ordered field list (from ui.ordemFormulario or colunas order)
    field_order = data.get("ui", {}).get("ordemFormulario", [])
    if not field_order:
        field_order = [
            col["nome"]
            for col in data["colunas"]
            if not col.get("chavePrimaria") and col["nome"] not in {"sin_ativo", scope_name}
        ]

    # Build field info list
    fields = []
    for fname in field_order:
        col = next((c for c in data["colunas"] if c["nome"] == fname), None)
        if col is None or col.get("chavePrimaria") or col["nome"] in {"sin_ativo", scope_name}:
            continue
        ui = ui_map.get(fname, {})
        suf = col_suffix(col)
        attr = attribute_name(col)
        label = ui.get("rotulo", pascal_case(strip_common_prefixes(fname)))
        accesskey = ui.get("teclaAtalho", "")
        artigo = "a" if ui.get("artigo") == "a" else "o"
        required = col.get("obrigatorio", False)
        rel = rel_map.get(fname)
        is_fk = rel is not None

        if is_fk:
            widget = "select"
            rel_base = class_base(rel["tabelaReferencia"])
            sel_key = suf[2:] if suf.startswith("Id") else suf
            fk_helper = f"montarSelect{pascal_case(strip_common_prefixes(rel['campoExibicao']))}"
        else:
            rel_base = ""
            sel_key = ""
            fk_helper = ""
            tipo = col["tipoBanco"]
            if tipo in {"datetime", "date", "timestamp"}:
                widget = "datetime" if attr.startswith("Dth") else "date"
            elif tipo == "numeric":
                widget = "money" if attr.startswith("Din") else "number"
            elif tipo == "char":
                widget = "char"
            else:
                widget = "text"

        fields.append(
            {
                "col": col,
                "name": fname,
                "suffix": suf,
                "attr": attr,
                "label": label,
                "accesskey": accesskey,
                "artigo": artigo,
                "required": required,
                "widget": widget,
                "is_fk": is_fk,
                "rel_base": rel_base,
                "sel_key": sel_key,
                "fk_helper": fk_helper,
                "css_width": css_width(col),
                "maxlength": col.get("tamanho"),
            }
        )

    fk_fields = [f for f in fields if f["is_fk"]]
    non_fk_fields = [f for f in fields if not f["is_fk"]]

    # --- Build salvarCamposPost ---
    salvar_campos = ""
    if fk_fields:
        sel_names = ", ".join(f"'sel{f['sel_key']}'" for f in fk_fields)
        salvar_campos = (
            f"  PaginaSEI::getInstance()->salvarCamposPost([{sel_names}]);\n\n"
        )

    # --- Build case cadastrar: field assignments ---
    def render_cadastrar_fields():
        lines = []
        lines.append(f"      $obj{base}DTO->set{pk_attr}(null);\n")
        for f in fields:
            if f["is_fk"]:
                var = f"$numId{f['sel_key']}"
                lines.append(
                    f"      {var} = PaginaSEI::getInstance()->recuperarCampo('sel{f['sel_key']}');\n"
                )
                lines.append(f"      if ({var} !=='') {{\n")
                lines.append(f"        $obj{base}DTO->set{f['attr']}((int){var});\n")
                lines.append(f"      }} else {{\n")
                lines.append(f"        $obj{base}DTO->set{f['attr']}(null);\n")
                lines.append(f"      }}\n\n")
            else:
                html_id = _html_id(f)
                lines.append(
                    f"      $obj{base}DTO->set{f['attr']}(PaginaSEI::POST('{html_id}'));\n"
                )
        if has_sin_ativo:
            lines.append(f"      $obj{base}DTO->setStrSinAtivo('S');\n")
        lines.append(scope_set_line)
        return "".join(lines)

    # --- Build case alterar: POST field assignments ---
    def render_alterar_post_fields():
        lines = []
        lines.append(
            f"        $obj{base}DTO->set{pk_attr}((int)PaginaSEI::POST('hdnId{base}'));\n"
        )
        for f in fields:
            if f["is_fk"]:
                lines.append(
                    f"        $obj{base}DTO->set{f['attr']}(PaginaSEI::POST('sel{f['sel_key']}'));\n"
                )
            else:
                html_id = _html_id(f)
                lines.append(
                    f"        $obj{base}DTO->set{f['attr']}(PaginaSEI::POST('{html_id}'));\n"
                )
        if has_sin_ativo:
            lines.append(f"        $obj{base}DTO->setStrSinAtivo('S');\n")
        lines.append(scope_filter_line(data, base, "        "))
        return "".join(lines)

    # --- Build FK select items ---
    def render_fk_selects():
        lines = []
        for f in fk_fields:
            lines.append(
                f"  $strItensSel{f['sel_key']} = {f['rel_base']}INT::{f['fk_helper']}('null','&nbsp;',$obj{base}DTO->get{f['attr']}());\n"
            )
        return "".join(lines)

    # --- Build CSS style lines ---
    def render_style():
        lines = []
        for f in fields:
            if f["is_fk"]:
                lines.append(
                    f"#lbl{f['sel_key']} {{position:absolute;left:0;top:0;width:{f['css_width']};}}"
                )
                lines.append(
                    f"#sel{f['sel_key']} {{position:absolute;left:0;top:40%;width:{f['css_width']};}}"
                )
            elif f["widget"] in {"date", "datetime"}:
                lines.append(
                    f"#lbl{f['suffix']} {{position:absolute;left:0;top:0;width:{f['css_width']};}}"
                )
                lines.append(
                    f"#txt{f['suffix']} {{position:absolute;left:0;top:40%;width:{f['css_width']};}}"
                )
                lines.append(
                    f"#imgCal{f['suffix']} {{position:absolute;left:26%;top:45%;}}"
                )
            else:
                lines.append(
                    f"#lbl{f['suffix']} {{position:absolute;left:0;top:0;width:{f['css_width']};}}"
                )
                lines.append(
                    f"#txt{f['suffix']} {{position:absolute;left:0;top:40%;width:{f['css_width']};}}"
                )
            lines.append("")
        return "\n".join(lines)

    # --- Build JS validarCadastro ---
    def render_js_validation():
        lines = []
        for f in fields:
            if not f["required"]:
                continue
            artigo = f["artigo"]
            if f["is_fk"]:
                sel_id = f"sel{f['sel_key']}"
                lines.append(f"  if (!infraSelectSelecionado('{sel_id}')) {{")
                lines.append(f"    alert('Selecione {'uma' if artigo == 'a' else 'um'} {q(f['label'])}.');")
                lines.append(f"    document.getElementById('{sel_id}').focus();")
                lines.append(f"    return false;")
                lines.append(f"  }}")
                lines.append("")
            elif f["widget"] in {"date", "datetime"}:
                html_id = _html_id(f)
                validar = "infraValidarDataHora" if f["widget"] == "datetime" else "infraValidarData"
                lines.append(
                    f"  if (infraTrim(document.getElementById('{html_id}').value)=='') {{"
                )
                lines.append(f"    alert('Informe {artigo} {q(f['label'])}.');")
                lines.append(f"    document.getElementById('{html_id}').focus();")
                lines.append(f"    return false;")
                lines.append(f"  }}")
                lines.append("")
                lines.append(
                    f"  if (!{validar}(document.getElementById('{html_id}'))) {{"
                )
                lines.append(f"    return false;")
                lines.append(f"  }}")
                lines.append("")
            else:
                html_id = _html_id(f)
                lines.append(
                    f"  if (infraTrim(document.getElementById('{html_id}').value)=='') {{"
                )
                lines.append(f"    alert('Informe {artigo} {q(f['label'])}.');")
                lines.append(f"    document.getElementById('{html_id}').focus();")
                lines.append(f"    return false;")
                lines.append(f"  }}")
                lines.append("")
        lines.append("  return true;")
        return "\n".join(lines)

    # --- Build form fields HTML ---
    def render_form_fields():
        blocks = []
        for f in fields:
            label_class = (
                "infraLabelObrigatorio" if f["required"] else "infraLabelOpcional"
            )
            label_html = _label_with_accesskey(f["label"], f["accesskey"])

            accesskey_attr = f' accesskey="{f["accesskey"].lower()}"' if f["accesskey"] else ""
            if f["is_fk"]:
                sel_id = f"sel{f['sel_key']}"
                block = (
                    f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                    f"?>\n"
                    f'  <label id="lbl{f["sel_key"]}" for="{sel_id}"{accesskey_attr} class="{label_class}">{label_html}:</label>\n'
                    f'  <select id="{sel_id}" name="{sel_id}" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>">\n'
                    f"  <?=$strItensSel{f['sel_key']}??false?>\n"
                    f"  </select>\n"
                    f"<?php\n"
                    f"PaginaSEI::getInstance()->fecharAreaDados();"
                )
            elif f["widget"] in {"date", "datetime"}:
                html_id = _html_id(f)
                mascara = "infraMascaraDataHora" if f["widget"] == "datetime" else "infraMascaraData"
                block = (
                    f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                    f"?>\n"
                    f'  <label id="lbl{f["suffix"]}" for="{html_id}"{accesskey_attr} class="{label_class}">{label_html}:</label>\n'
                    f'  <input type="text" id="{html_id}" name="{html_id}" onkeypress="return {mascara}(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{f["attr"]}())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                    f'  <img id="imgCal{f["suffix"]}" title="Selecionar {f["label"]}" alt="Selecionar {f["label"]}" src="<?=PaginaSEI::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario(\'{html_id}\',this);" />\n'
                    f"<?php\n"
                    f"PaginaSEI::getInstance()->fecharAreaDados();"
                )
            elif f["widget"] in {"money", "number"}:
                html_id = _html_id(f)
                mascara = 'onkeydown="return infraMascaraDinheiro(this, event)"' if f["widget"] == "money" else 'onkeypress="return infraMascaraNumero(this, event)"'
                block = (
                    f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                    f"?>\n"
                    f'  <label id="lbl{f["suffix"]}" for="{html_id}"{accesskey_attr} class="{label_class}">{label_html}:</label>\n'
                    f'  <input type="text" id="{html_id}" name="{html_id}" {mascara} class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{f["attr"]}())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                    f"<?php\n"
                    f"PaginaSEI::getInstance()->fecharAreaDados();"
                )
            else:
                html_id = _html_id(f)
                maxlen_attr = ""
                mascara_attr = ""
                if f["maxlength"]:
                    maxlen_attr = f' maxlength="{f["maxlength"]}"'
                    mascara_attr = f' onkeypress="return infraMascaraTexto(this,event,{f["maxlength"]});"'
                else:
                    mascara_attr = ' onkeypress="return infraMascaraTexto(this,event);"'
                block = (
                    f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                    f"?>\n"
                    f'  <label id="lbl{f["suffix"]}" for="{html_id}"{accesskey_attr} class="{label_class}">{label_html}:</label>\n'
                    f'  <input type="text" id="{html_id}" name="{html_id}" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{f["attr"]}())?>"{mascara_attr}{maxlen_attr} tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                    f"<?php\n"
                    f"PaginaSEI::getInstance()->fecharAreaDados();"
                )
            blocks.append(block)
        return "\n".join(blocks)

    # Determine first focus element
    if fk_fields:
        first_focus = f"sel{fk_fields[0]['sel_key']}"
    elif non_fk_fields:
        first_focus = _html_id(non_fk_fields[0])
    else:
        first_focus = "btnCancelar"

    # Assemble the full PHP file
    out = []
    out.append(php_header())
    out.append("\n\ntry {\n")
    out.append(page_require_sei())
    out.append("  session_start();\n\n")
    out.append(
        "  //////////////////////////////////////////////////////////////////////////////\n"
    )
    out.append("  //InfraDebug::getInstance()->setBolLigado(false);\n")
    out.append("  //InfraDebug::getInstance()->setBolDebugInfra(true);\n")
    out.append("  //InfraDebug::getInstance()->limpar();\n")
    out.append(
        "  //////////////////////////////////////////////////////////////////////////////\n\n"
    )
    out.append("  SessaoSEI::getInstance()->validarLink();\n\n")
    out.append("  $strAcao = PaginaSEI::GET('acao');\n")
    out.append("  SessaoSEI::getInstance()->validarPermissao($strAcao);\n\n")
    out.append(
        f"  PaginaSEI::getInstance()->verificarSelecao('{table_name}_selecionar');\n\n"
    )
    out.append(salvar_campos)
    out.append(f"  $obj{base}DTO = new {base}DTO();\n")
    out.append("  $strDesabilitar = '';\n")
    out.append("  $arrComandos = [];\n")
    out.append("  \n")
    out.append("  switch ($strAcao) {\n")

    # case cadastrar
    out.append(f"    case '{table_name}_cadastrar':\n")
    out.append(f"      $strTitulo = '{new_word} {singular}';\n")
    out.append(
        f'      $arrComandos[] = \'<button type="submit" accesskey="S" name="sbmCadastrar{base}" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>\';\n'
    )
    out.append(
        f'      $arrComandos[] = \'<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.$strAcao).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>\';\n\n'
    )
    out.append(render_cadastrar_fields())
    out.append(f"\n      if (PaginaSEI::POST('sbmCadastrar{base}') !== null) {{\n")
    out.append(f"        try {{\n")
    out.append(f"          $obj{base}RN = new {base}RN();\n")
    out.append(f"          $obj{base}DTO = $obj{base}RN->cadastrar($obj{base}DTO);\n")
    out.append(
        f"          PaginaSEI::getInstance()->adicionarMensagem('{singular} \"'.$obj{base}DTO->get{display_attr}().'\" {created_word} com sucesso.');\n"
    )
    out.append(
        f"          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').'&{pk_param}='.$obj{base}DTO->get{pk_attr}().PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk_attr}())));\n"
    )
    out.append("          die;\n")
    out.append(f"        }} catch (Exception $e) {{\n")
    out.append(f"          PaginaSEI::getInstance()->processarExcecao($e);\n")
    out.append("        }\n")
    out.append("      }\n")
    out.append("      break;\n\n")

    # case alterar
    out.append(f"    case '{table_name}_alterar':\n")
    out.append(f"      $strTitulo = 'Alterar {singular}';\n")
    out.append(
        f'      $arrComandos[] = \'<button type="submit" accesskey="S" name="sbmAlterar{base}" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>\';\n'
    )
    out.append("      $strDesabilitar = 'disabled=\"disabled\"';\n\n")
    out.append(f"      if (PaginaSEI::GET('{pk_param}') !== null) {{\n")
    out.append(f"        $obj{base}DTO->set{pk_attr}((int)PaginaSEI::GET('{pk_param}'));\n")
    out.append(scope_filter_line(data, base, "        "))
    out.append(f"        $obj{base}DTO->retTodos();\n")
    out.append(f"        $obj{base}RN = new {base}RN();\n")
    out.append(f"        $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n")
    out.append(f"        if ($obj{base}DTO===null) {{\n")
    out.append(f"          throw new InfraException('{singular} não {words['encontrado']}.');\n")
    out.append("        }\n")
    out.append("      } else {\n")
    out.append(render_alterar_post_fields())
    out.append("      }\n\n")
    out.append(
        f'      $arrComandos[] = \'<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.PaginaSEI::GET(\'acao\').PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk_attr}())).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>\';\n\n'
    )
    out.append(f"      if (PaginaSEI::POST('sbmAlterar{base}') !== null) {{\n")
    out.append(f"        try {{\n")
    out.append(f"          $obj{base}RN = new {base}RN();\n")
    out.append(f"          $obj{base}RN->alterar($obj{base}DTO);\n")
    out.append(
        f"          PaginaSEI::getInstance()->adicionarMensagem('{singular} \"'.$obj{base}DTO->get{display_attr}().'\" {altered_word} com sucesso.');\n"
    )
    out.append(
        f"          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk_attr}())));\n"
    )
    out.append("          die;\n")
    out.append(f"        }} catch (Exception $e) {{\n")
    out.append(f"          PaginaSEI::getInstance()->processarExcecao($e);\n")
    out.append("        }\n")
    out.append("      }\n")
    out.append("      break;\n\n")

    # case consultar
    out.append(f"    case '{table_name}_consultar':\n")
    out.append(f"      $strTitulo = 'Consultar {singular}';\n")
    out.append(
        f"      $arrComandos[] = '<button type=\"button\" accesskey=\"F\" name=\"btnFechar\" value=\"Fechar\" onclick=\"location.href=\\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora(PaginaSEI::GET('{pk_param}'))).'\\';\" class=\"infraButton\"><span class=\"infraTeclaAtalho\">F</span>echar</button>';\n"
    )
    out.append(f"      $obj{base}DTO->set{pk_attr}((int)PaginaSEI::GET('{pk_param}'));\n")
    out.append(scope_set_line)
    out.append(f"      $obj{base}DTO->setBolExclusaoLogica(false);\n")
    out.append(f"      $obj{base}DTO->retTodos();\n")
    out.append(f"      $obj{base}RN = new {base}RN();\n")
    out.append(f"      $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n")
    out.append(f"      if ($obj{base}DTO===null) {{\n")
    out.append(f"        throw new InfraException('{singular} não {words['encontrado']}.');\n")
    out.append("      }\n")
    out.append("      break;\n\n")

    # default
    out.append("    default:\n")
    out.append(
        "      throw new InfraException(\"Ação '\" . $strAcao . \"' não reconhecida.\");\n"
    )
    out.append("  }\n\n")

    # FK select items
    if fk_fields:
        out.append(render_fk_selects())
        out.append("\n")

    out.append("} catch(Exception $e) {\n")
    out.append("  PaginaSEI::getInstance()->processarExcecao($e);\n")
    out.append("}\n\n")

    # HTML head
    out.append("PaginaSEI::getInstance()->montarDocType();\n")
    out.append("PaginaSEI::getInstance()->abrirHtml();\n")
    out.append("PaginaSEI::getInstance()->abrirHead();\n")
    out.append("PaginaSEI::getInstance()->montarMeta();\n")
    out.append(
        "PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema() . ' - ' . ($strTitulo??false));\n"
    )
    out.append("PaginaSEI::getInstance()->montarStyle();\n")
    out.append("PaginaSEI::getInstance()->abrirStyle();\n")
    out.append("?>\n")
    out.append("<?php if(0){?><style><?php }?>\n")
    out.append(render_style())
    out.append("<?php if(0){?></style><?php }?>\n")
    out.append("<?php\n")
    out.append("PaginaSEI::getInstance()->fecharStyle();\n")
    out.append("PaginaSEI::getInstance()->montarJavaScript();\n")
    out.append("PaginaSEI::getInstance()->abrirJavaScript();\n")
    out.append("?>\n")
    out.append('<?php if(0){?><script type="text/javascript"><?php }?>\n\n')

    # JS inicializar
    out.append("function inicializar()\n{\n")
    out.append(
        f"  if ('<?=$strAcao??false?>' === '{table_name}_cadastrar') {{\n"
    )
    out.append(f"    document.getElementById('{first_focus}').focus();\n")
    out.append(
        f"  }} else if ('<?=$strAcao??false?>' === '{table_name}_consultar') {{\n"
    )
    out.append("    infraDesabilitarCamposAreaDados();\n")
    out.append("  } else {\n")
    out.append("    document.getElementById('btnCancelar').focus();\n")
    out.append("  }\n")
    out.append("  infraEfeitoTabelas(true);\n")
    out.append("}\n\n")

    # JS validarCadastro
    out.append("function validarCadastro()\n{\n")
    out.append(render_js_validation())
    out.append("\n}\n\n")

    # JS OnSubmitForm
    out.append("function OnSubmitForm()\n{\n")
    out.append("  return validarCadastro();\n")
    out.append("}\n\n")

    out.append("<?php if(0){?></script><?php }?>\n")
    out.append("<?php\n")
    out.append("PaginaSEI::getInstance()->fecharJavaScript();\n")
    out.append("PaginaSEI::getInstance()->fecharHead();\n")
    out.append(
        "PaginaSEI::getInstance()->abrirBody($strTitulo??false,'onload=\"inicializar();\"');\n"
    )
    out.append("?>\n")

    # Form
    out.append(
        f"<form id=\"frm{base}Cadastro\" method=\"post\" onsubmit=\"return OnSubmitForm();\" action=\"<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.$strAcao.'&acao_origem='.$strAcao)?>\">\n"
    )
    out.append("<?php\n")
    out.append(
        "PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);\n"
    )
    out.append("//PaginaSEI::getInstance()->montarAreaValidacao();\n")
    out.append(render_form_fields())
    out.append("\n?>\n")
    out.append(
        f'  <input type="hidden" id="hdnId{base}" name="hdnId{base}" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{pk_attr}())?>" />\n'
    )
    out.append("  <?php\n")
    out.append("  //PaginaSEI::getInstance()->montarAreaDebug();\n")
    out.append(
        "  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);\n"
    )
    out.append("  ?>\n")
    out.append("</form>\n")
    out.append("<?php\n")
    out.append("PaginaSEI::getInstance()->fecharBody();\n")
    out.append("PaginaSEI::getInstance()->fecharHtml();\n")

    content = "".join(out)
    content = content.replace("PaginaSEI::GET('acao')", "$strAcao")
    return content.replace("$strAcao = $strAcao;", "$strAcao = PaginaSEI::GET('acao');")


def _html_id(field: dict) -> str:
    """Return the HTML element id for a non-FK field (e.g., txtNumero)."""
    return f"txt{field['suffix']}"


def _label_with_accesskey(label: str, accesskey: str) -> str:
    """Wrap the access key character in the label with infraTeclaAtalho span."""
    if not accesskey:
        return label
    lower = accesskey.lower()
    idx = label.lower().find(lower)
    if idx >= 0:
        return (
            label[:idx]
            + f'<span class="infraTeclaAtalho">{label[idx]}</span>'
            + label[idx + 1 :]
        )
    return f'<span class="infraTeclaAtalho">{accesskey}</span>{label}'


def scope_filter_line(data: dict, base: str, indent_text: str = "    ") -> str:
    """Filtro pela unidade atual da sessao quando regrasGeracao.escopoUnidade estiver definido."""
    scope = scope_column(data)
    if scope is None:
        return ""
    return f"{indent_text}$obj{base}DTO->set{attribute_name(scope)}(SessaoSEI::getInstance()->getNumIdUnidadeAtual());\n"


def render_int(data: dict) -> str:
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    display_field = data["entidade"]["campoPrincipal"]
    display_column = next(
        column for column in data["colunas"] if column["nome"] == display_field
    )
    display_attr = attribute_name(display_column)
    display_prefix = dto_prefix(display_column)
    display_suffix = (
        display_attr[len(display_prefix) :]
        if display_attr.startswith(display_prefix)
        else display_attr
    )
    pk_columns = [c for c in data["colunas"] if c.get("chavePrimaria")]
    pk_column = pk_columns[0]
    pk_attr = attribute_name(pk_column)
    method_name = f"montarSelect{display_suffix}"

    lines = [
        php_header(),
        class_require_sei(),
        f"class {base}INT extends InfraINT\n",
        "{\n",
        "  /**\n",
        "   * @throws InfraException\n",
        "   */\n",
    ]

    if is_nn(data):
        # N:N INT: method receives both PKs as optional filters
        pk1, pk2 = pk_columns[0], pk_columns[1]
        pk1_attr = attribute_name(pk1)
        pk2_attr = attribute_name(pk2)
        pk1_var = "$" + pk1_attr[0].lower() + pk1_attr[1:]
        pk2_var = "$" + pk2_attr[0].lower() + pk2_attr[1:]
        pk1_suffix = pk1_attr[3:] if pk1_attr.startswith("Num") else pk1_attr
        pk1_relation = relation_for_column(data, pk1["nome"])
        desc_attr = related_attribute_name(data, pk1_relation) if pk1_relation else pk1_attr
        desc_suffix = attr_suffix_from_attr(desc_attr)
        method_name_nn = f"montarSelect{desc_suffix}"
        lines.extend(
            [
                f"  public static function {method_name_nn}($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, {pk1_var}='', {pk2_var}=''): string\n",
                "  {\n",
                f"    $obj{base}DTO = new {base}DTO();\n",
                f"    $obj{base}DTO->ret{pk1_attr}();\n",
                f"    $obj{base}DTO->ret{pk2_attr}();\n",
                (f"    $obj{base}DTO->ret{desc_attr}();\n" if pk1_relation else ""),
                "\n",
                f"    if ({pk1_var}!=='') {{\n",
                f"      $obj{base}DTO->set{pk1_attr}({pk1_var});\n",
                "    }\n\n",
                f"    if ({pk2_var}!=='') {{\n",
                f"      $obj{base}DTO->set{pk2_attr}({pk2_var});\n",
                "    }\n\n",
                f"    $obj{base}DTO->setOrd{desc_attr}(InfraDTO::$TIPO_ORDENACAO_ASC);\n\n",
                f"    $obj{base}RN = new {base}RN();\n",
                f"    $arrObj{base}DTO = $obj{base}RN->listar($obj{base}DTO);\n\n",
                f"    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObj{base}DTO, '{pk1_suffix}', '{desc_suffix}');\n",
                "  }\n",
            ]
        )
    else:
        relations = data.get("relacionamentos", [])
        if relations:
            fk_params = []
            fk_filter_blocks = []
            for rel in relations:
                fk_col = next(
                    column
                    for column in data["colunas"]
                    if column["nome"] == rel["coluna"]
                )
                fk_attr = attribute_name(fk_col)
                fk_var = "$" + fk_attr[0].lower() + fk_attr[1:]
                fk_params.append(f"{fk_var}=''")
                fk_filter_blocks.append(
                    f"    if ({fk_var}!=='') {{\n"
                    f"      $obj{base}DTO->set{fk_attr}({fk_var});\n"
                    "    }\n"
                )

            params_str = ", ".join(fk_params)
            lines.extend(
                [
                    f"  public static function {method_name}($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, {params_str}): string\n",
                    "  {\n",
                    f"    $obj{base}DTO = new {base}DTO();\n",
                    f"    $obj{base}DTO->ret{pk_attr}();\n",
                    f"    $obj{base}DTO->ret{display_attr}();\n",
                    scope_filter_line(data, base),
                    "\n",
                ]
            )
            for i, block in enumerate(fk_filter_blocks):
                lines.append(block)
                if i < len(fk_filter_blocks) - 1:
                    lines.append("\n")
            if data["regrasGeracao"].get("campoSinAtivo"):
                lines.extend(
                    [
                        "\n    if ($strValorItemSelecionado!=null) {\n",
                        f"      $obj{base}DTO->setBolExclusaoLogica(false);\n",
                        f"      $obj{base}DTO->adicionarCriterio(['SinAtivo', '{attr_suffix_from_attr(pk_attr)}'], [InfraDTO::$OPER_IGUAL, InfraDTO::$OPER_IGUAL], ['S', $strValorItemSelecionado], InfraDTO::$OPER_LOGICO_OR);\n",
                        "    }\n",
                    ]
                )
            lines.extend(
                [
                    f"\n    $obj{base}DTO->setOrd{display_attr}(InfraDTO::$TIPO_ORDENACAO_ASC);\n\n",
                    f"    $obj{base}RN = new {base}RN();\n",
                    f"    $arrObj{base}DTO = $obj{base}RN->listar($obj{base}DTO);\n\n",
                    f"    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObj{base}DTO, '{pk_attr[3:] if pk_attr.startswith('Num') else pk_attr}', '{display_suffix}');\n",
                    "  }\n",
                ]
            )
        else:
            lines.extend(
                [
                    f"  public static function {method_name}($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado): string\n",
                    "  {\n",
                    f"    $obj{base}DTO = new {base}DTO();\n",
                    f"    $obj{base}DTO->ret{pk_attr}();\n",
                    f"    $obj{base}DTO->ret{display_attr}();\n",
                    scope_filter_line(data, base),
                    "\n",
                ]
            )
            if data["regrasGeracao"].get("campoSinAtivo"):
                lines.extend(
                    [
                        "    if ($strValorItemSelecionado!=null) {\n",
                        f"      $obj{base}DTO->setBolExclusaoLogica(false);\n",
                        f"      $obj{base}DTO->adicionarCriterio(['SinAtivo', '{attr_suffix_from_attr(pk_attr)}'], [InfraDTO::$OPER_IGUAL, InfraDTO::$OPER_IGUAL], ['S', $strValorItemSelecionado], InfraDTO::$OPER_LOGICO_OR);\n",
                        "    }\n\n",
                    ]
                )
            lines.extend(
                [
                    f"    $obj{base}DTO->setOrd{display_attr}(InfraDTO::$TIPO_ORDENACAO_ASC);\n\n",
                    f"    $obj{base}RN = new {base}RN();\n",
                    f"    $arrObj{base}DTO = $obj{base}RN->listar($obj{base}DTO);\n\n",
                    f"    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObj{base}DTO, '{pk_attr[3:] if pk_attr.startswith('Num') else pk_attr}', '{display_suffix}');\n",
                    "  }\n",
                ]
            )

    lines.append("}\n")
    return "".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Gera os 6 arquivos CRUD InfraPHP (dto/, bd/, rn/, int/, lista e cadastro) a partir do contrato JSON."
    )
    parser.add_argument("contrato", help="caminho do contrato JSON")
    parser.add_argument("output_dir", help="diretorio de saida (normalmente o modulo em web/modulos/...)")
    parser.add_argument(
        "--niveis",
        type=int,
        default=None,
        help="profundidade das paginas em relacao a web/SEI.php (modulos/<inst>/<modulo>/ = 3, modulos/<modulo>/ = 2); "
        "derivada do diretorio de saida quando ele esta em web/modulos/",
    )
    args = parser.parse_args()

    contrato_path = Path(args.contrato).resolve()
    output_dir = Path(args.output_dir).resolve()

    if not contrato_path.exists():
        return fail(f"Contrato nao encontrado: {contrato_path}")

    try:
        data = json.loads(contrato_path.read_text(encoding="utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as exc:
        return fail(f"Contrato JSON invalido ({contrato_path}): {exc}")

    try:
        validate_supported_input(data)
    except ValueError as exc:
        return fail(str(exc))

    table_name = data["entidade"]["tabela"]
    alerts = developer_alerts(data)

    levels = args.niveis
    if levels is None:
        levels = page_levels_from_output_dir(output_dir)
    if levels is None:
        levels = DEFAULT_PAGE_LEVELS
        alerts.append(
            f"Diretorio de saida fora de web/modulos/: require_once gerado para modulo em modulos/<instituicao>/<modulo>/ ({levels} niveis); use --niveis para outro leiaute."
        )
    if levels < 1:
        return fail("--niveis deve ser maior ou igual a 1")
    set_page_levels(levels)

    helper_errors, helper_alerts = check_int_helpers(data, output_dir)
    if helper_errors:
        return fail("\n".join(helper_errors))
    alerts.extend(helper_alerts)

    files = expected_files(table_name)
    output_dir.mkdir(parents=True, exist_ok=True)

    for file_name in files:
        destination = output_dir / file_name
        if destination.exists():
            return fail(f"Target file already exists: {destination}")

    base = class_base(table_name)
    generated_content = {
        f"dto/{base}DTO.php": render_dto(data),
        f"bd/{base}BD.php": render_bd(data),
        f"rn/{base}RN.php": render_rn(data),
        f"int/{base}INT.php": render_int(data),
        f"{table_name}_lista.php": render_lista(data),
        f"{table_name}_cadastro.php": render_cadastro(data),
    }

    for file_name in files:
        destination = output_dir / file_name
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(generated_content[file_name], encoding="latin-1")

    relations = data.get("relacionamentos", [])
    print(
        json.dumps(
            {
                "contrato": str(contrato_path),
                "table": table_name,
                "output_dir": str(output_dir),
                "niveis": levels,
                "flags": {
                    "temSinAtivo": bool((data.get("regrasGeracao") or {}).get("campoSinAtivo")),
                    "temFk": bool(relations),
                    "numeroFks": len(relations),
                    "nn": is_nn(data),
                },
                "generated_files": [str(output_dir / name) for name in files],
                "developer_alerts": alerts,
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
