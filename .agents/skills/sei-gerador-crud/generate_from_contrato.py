#!/usr/bin/env python3

import json
import sys
from pathlib import Path
from textwrap import dedent


ROOT = Path(__file__).resolve().parents[3]


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def pascal_case(value: str) -> str:
    return "".join(part.capitalize() for part in value.split("_") if part)


def strip_common_prefixes(column_name: str) -> str:
    for prefix in ("num_", "str_", "din_", "dta_", "dth_"):
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
        return "Din"
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
        return "InfraDTO::$PREFIXO_DIN"
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

CLASS_REQUIRE_SEI = "require_once dirname(__FILE__) . '/../../../SEI.php';\n\n"
PAGE_REQUIRE_SEI = "  require_once dirname(__FILE__) . '/../../SEI.php';\n\n\n"


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
    entidade = data.get("entidade", {})
    table_name = entidade.get("tabela", "")
    comentario_tabela = entidade.get("comentario")
    if not comentario_tabela:
        raise ValueError("Entity comentario is required")

    validate_physical_name(table_name, "table")

    field_names = {column.get("nome") for column in data.get("colunas", [])}
    campo_principal = entidade.get("campoPrincipal")
    if not campo_principal or campo_principal not in field_names:
        raise ValueError("entidade.campoPrincipal must reference an existing column")

    pk_count = 0
    pk_columns = []
    supported_types = {"int", "integer", "varchar", "datetime", "date", "timestamp", "char", "numeric"}
    for column in data.get("colunas", []):
        validate_physical_name(column.get("nome", ""), "column")
        if not column.get("comentario"):
            raise ValueError(f"Column comentario is required: {column.get('nome')}")
        if column.get("tipoBanco") not in supported_types:
            raise ValueError(
                f"Unsupported v1 type: {column.get('tipoBanco')} for {column.get('nome')}"
            )
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

    if pk_count == 2:
        if "_rel_" not in table_name:
            raise ValueError(
                "N:N table names must follow md_<sigla>_rel_<entidade_a>_<entidade_b>"
            )
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

    for relation in data.get("relacionamentos", []):
        if relation.get("coluna") not in field_names:
            raise ValueError(
                f"Relationship coluna not found in colunas: {relation.get('coluna')}"
            )


def is_nn(data: dict) -> bool:
    """Returns True when the entity has a composite PK (N:N relationship table)."""
    return sum(1 for c in data.get("colunas", []) if c.get("chavePrimaria")) == 2


def ui_label(column: dict) -> str:
    ui = column.get("_ui") or {}
    return ui.get("rotulo", pascal_case(strip_common_prefixes(column["nome"]))).replace(
        "_", " "
    )


def attr_suffix_from_attr(attr: str) -> str:
    for prefix in ("Num", "Str", "Din", "Dta", "Dth"):
        if attr.startswith(prefix):
            return attr[len(prefix):]
    return attr


def related_attribute_name(relation: dict) -> str:
    return "Str" + pascal_case(relation["campoExibicao"]) + pascal_case(
        relation["tabelaReferencia"]
    )


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
    }


def developer_alerts(data: dict) -> list[str]:
    entity = data.get("entidade", {})
    return [
        "Revise os textos de domínio exibidos ao usuário antes de entregar o CRUD: títulos, singular/plural, rótulos, cabeçalhos, captions, mensagens, title e alt.",
        "O gerador corrige apenas textos padrão universais do CRUD; acentuação e termos de negócio devem vir revisados no contrato JSON.",
        f"Entidade no contrato: singular='{entity.get('singular', '')}', plural='{entity.get('plural', '')}', campoPrincipal='{entity.get('campoPrincipal', '')}'.",
    ]


def relation_for_column(data: dict, column_name: str):
    for relation in data.get("relacionamentos", []):
        if relation.get("coluna") == column_name:
            return relation
    return None


def render_dto(data: dict) -> str:
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    pk_columns = [c for c in data["colunas"] if c.get("chavePrimaria")]
    lines = [
        php_header(),
        CLASS_REQUIRE_SEI,
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

    for relation in data.get("relacionamentos", []):
        related_name = pascal_case(relation["campoExibicao"]) + pascal_case(
            relation["tabelaReferencia"]
        )
        lines.append(
            f"\n    $this->adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, '{related_name}', '{relation['campoExibicao']}', '{relation['tabelaReferencia']}');\n"
        )

    for relation in data.get("relacionamentos", []):
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
        fk_args = [
            f"'{fk_suffix}'",
            f"'{relation['tabelaReferencia']}'",
            f"'{physical_pk_name(relation['tabelaReferencia'])}'",
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
        + CLASS_REQUIRE_SEI
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
    return f"{ui_label(column)} não informado."


def render_validator(column: dict) -> str:
    table_base = class_base(column["_table"])
    attr = attribute_name(column)
    getter = f"get{attr}()"
    setter = f"set{attr}"
    method = validator_method_name(column)
    label = ui_label(column)
    lines = [
        f"  private function {method}({table_base}DTO $obj{table_base}DTO, InfraException $objInfraException): void\n",
        "  {\n",
    ]

    if column["tipoBanco"] == "varchar":
        lines.append(
            f"    if (InfraString::isBolVazia($obj{table_base}DTO->{getter})) {{\n"
        )
        if column["obrigatorio"]:
            lines.append(
                f"      $objInfraException->adicionarValidacao('{label} não informado.');\n"
            )
        else:
            lines.append(f"      $obj{table_base}DTO->{setter}(null);\n")
        lines.append("    } else {\n")
        lines.append(
            f"      $obj{table_base}DTO->{setter}(trim($obj{table_base}DTO->{getter}));\n"
        )
        if column.get("tamanho"):
            lines.append(
                f"      if (strlen($obj{table_base}DTO->{getter})>{column['tamanho']}) {{\n"
            )
            lines.append(
                f"        $objInfraException->adicionarValidacao('{label} possui tamanho superior a {column['tamanho']} caracteres.');\n"
            )
            lines.append("      }\n")
        lines.append("    }\n")
    elif column["tipoBanco"] in {"datetime", "date", "timestamp"}:
        lines.append(
            f"    if (InfraString::isBolVazia($obj{table_base}DTO->{getter})) {{\n"
        )
        if column["obrigatorio"]:
            lines.append(
                f"      $objInfraException->adicionarValidacao('{label} não informado.');\n"
            )
        else:
            lines.append(f"      $obj{table_base}DTO->{setter}(null);\n")
        lines.append("    } else {\n")
        lines.append(
            f"      if (!InfraData::validarData($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(
            f"        $objInfraException->adicionarValidacao('{label} inválida.');\n"
        )
        lines.append("      }\n")
        lines.append("    }\n")
    elif column["tipoBanco"] == "numeric":
        lines.append(
            f"    if (InfraString::isBolVazia($obj{table_base}DTO->{getter})) {{\n"
        )
        if column["obrigatorio"]:
            lines.append(
                f"      $objInfraException->adicionarValidacao('{label} não informado.');\n"
            )
        else:
            lines.append(f"      $obj{table_base}DTO->{setter}(null);\n")
        lines.append("      return;\n")
        lines.append("    }\n\n")
        lines.append(
            f"    $din{attr_suffix_from_attr(attr)} = str_replace(',', '.', $obj{table_base}DTO->{getter});\n"
        )
        lines.append(
            f"    if (!is_numeric($din{attr_suffix_from_attr(attr)}) || $din{attr_suffix_from_attr(attr)} < 0) {{\n"
        )
        lines.append(
            f"      $objInfraException->adicionarValidacao('{label} deve ser numérico e não negativo.');\n"
        )
        lines.append("    } else {\n")
        lines.append(f"      $obj{table_base}DTO->{setter}($din{attr_suffix_from_attr(attr)});\n")
        lines.append("    }\n")
    elif column["tipoBanco"] == "char":
        lines.append(
            f"    if (InfraString::isBolVazia($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(
            f"      $objInfraException->adicionarValidacao('{label} não informado.');\n"
        )
        lines.append("    } else {\n")
        lines.append(
            f"      if (!InfraUtil::isBolSinalizadorValido($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(
            f"        $objInfraException->adicionarValidacao('{label} inválido.');\n"
        )
        lines.append("      }\n")
        lines.append("    }\n")
    else:
        lines.append(
            f"    if (InfraString::isBolVazia($obj{table_base}DTO->{getter})) {{\n"
        )
        lines.append(
            f"      $objInfraException->adicionarValidacao('{validator_message(column)}');\n"
        )
        lines.append("    }\n")

    lines.append("  }\n\n")
    return "".join(lines)


def render_rn(data: dict) -> str:
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = data["entidade"]["singular"]
    plural = data["entidade"]["plural"]
    nn = is_nn(data)
    pk_columns = [c for c in data["colunas"] if c.get("chavePrimaria")]
    pk_attr = attribute_name(pk_columns[0])
    columns = []
    for column in data["colunas"]:
        cloned = dict(column)
        cloned["_table"] = table_name
        cloned["_ui"] = data.get("ui", {}).get("campos", {}).get(column["nome"])
        columns.append(cloned)

    # N:N: validate ALL columns including PKs (they are FK references, always required)
    # Simple: skip PKs in validators (they are auto-generated sequences, not user input)
    if nn:
        validator_columns = [c for c in columns if not c.get("chavePrimaria") or True]
        # Actually for N:N all columns are user-provided (PKs are FK references)
        validator_columns = columns
    else:
        validator_columns = [c for c in columns if not c.get("chavePrimaria")]

    validators = [render_validator(column) for column in validator_columns]

    def create_validation_line(column: dict) -> str:
        return f"      $this->{validator_method_name(column)}($obj{base}DTO, $objInfraException);\n"

    def update_validation_block(column: dict) -> str:
        attr = attribute_name(column)
        return (
            f"      if ($obj{base}DTO->isSet{attr}()) {{\n"
            f"        $this->{validator_method_name(column)}($obj{base}DTO, $objInfraException);\n"
            "      }\n\n"
        )

    logical_doc = (
        f" * @method void desativar({base}DTO[] $arrObj{base}DTO)\n"
        f" * @method void reativar({base}DTO[] $arrObj{base}DTO)\n"
    )
    reactivation_validation_lines = "".join(
        f"          $this->{validator_method_name(column)}($obj{base}AtualDTO, $objInfraException);\n"
        for column in validator_columns
        if not column.get("chavePrimaria")
    )

    if not nn and data["regrasGeracao"].get("campoSinAtivo"):
        logical_methods = (
            f"  protected function desativarControlado(array $arrObj{base}DTO): void\n  {{\n"
            f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_desativar', __METHOD__, $arrObj{base}DTO);\n\n"
            f"      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      foreach ($arrObj{base}DTO as $obj{base}DTO) {{\n        $obj{base}BD->desativar($obj{base}DTO);\n      }}\n\n"
            f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro desativando {singular}.', $e);\n    }}\n  }}\n\n"
            f"  protected function reativarControlado(array $arrObj{base}DTO): void\n  {{\n"
            f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_reativar', __METHOD__, $arrObj{base}DTO);\n\n"
            f"      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      foreach ($arrObj{base}DTO as $obj{base}DTO) {{\n        $objInfraException = new InfraException();\n        $obj{base}AtualDTO = new {base}DTO();\n        $obj{base}AtualDTO->setBolExclusaoLogica(false);\n        $obj{base}AtualDTO->retTodos();\n        $obj{base}AtualDTO->set{pk_attr}($obj{base}DTO->get{pk_attr}());\n        $obj{base}AtualDTO = $obj{base}BD->consultar($obj{base}AtualDTO);\n        if ($obj{base}AtualDTO===null) {{\n          $objInfraException->adicionarValidacao('{singular} nao encontrado.');\n        }} else {{\n"
            + reactivation_validation_lines
            + f"        }}\n        $objInfraException->lancarValidacoes();\n\n        $obj{base}BD->reativar($obj{base}DTO);\n      }}\n\n"
            + f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro reativando {singular}.', $e);\n    }}\n  }}\n\n"
            f"  protected function bloquearConectado({base}DTO $obj{base}DTO): ?{base}DTO\n  {{\n"
            f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_consultar', __METHOD__, $obj{base}DTO);\n\n"
            f"      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      return $obj{base}BD->bloquear($obj{base}DTO);\n\n"
            f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro bloqueando {singular}.', $e);\n    }}\n  }}\n"
        )
    else:
        logical_methods = (
            f"/*   protected function desativarControlado(array $arrObj{base}DTO): void\n  {{\n    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_desativar', __METHOD__, $arrObj{base}DTO);\n\n"
            f"      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      foreach ($arrObj{base}DTO as $obj{base}DTO) {{\n        $obj{base}BD->desativar($obj{base}DTO);\n      }}\n\n"
            f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro desativando {singular}.', $e);\n    }}\n  }}\n */\n"
            f"/*   protected function reativarControlado(array $arrObj{base}DTO): void\n  {{\n    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_reativar', __METHOD__, $arrObj{base}DTO);\n\n"
            f"      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      foreach ($arrObj{base}DTO as $obj{base}DTO) {{\n        $obj{base}BD->reativar($obj{base}DTO);\n      }}\n\n"
            f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro reativando {singular}.', $e);\n    }}\n  }}\n */\n"
            f"/*   protected function bloquearConectado({base}DTO $obj{base}DTO): ?{base}DTO\n  {{\n    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_consultar', __METHOD__, $obj{base}DTO);\n\n"
            f"      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      return $obj{base}BD->bloquear($obj{base}DTO);\n\n"
            f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro bloqueando {singular}.', $e);\n    }}\n  }} */\n"
        )

    create_lines = "".join(
        create_validation_line(column) for column in validator_columns
    )
    update_lines = "".join(
        update_validation_block(column) for column in validator_columns
    )
    return (
        php_header()
        + CLASS_REQUIRE_SEI
        + "/**\n"
        + f" * @method {base}DTO cadastrar({base}DTO $obj{base}DTO)\n"
        + f" * @method {base}DTO[] listar({base}DTO $obj{base}DTO)\n"
        + f" * @method {base}DTO|null consultar({base}DTO $obj{base}DTO)\n"
        + f" * @method {base}DTO|null bloquear({base}DTO $obj{base}DTO)\n"
        + f" * @method void alterar({base}DTO $obj{base}DTO)\n"
        + f" * @method void excluir({base}DTO[] $arrObj{base}DTO)\n"
        + logical_doc
        + " */\n"
        + f"class {base}RN extends InfraRN\n"
        + "{\n"
        + "  protected function inicializarObjInfraIBanco(): InfraIBanco\n  {\n    return BancoSEI::getInstance();\n  }\n\n"
        + "".join(validators)
        + f"  protected function cadastrarControlado({base}DTO $obj{base}DTO): {base}DTO\n  {{\n"
        + f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_cadastrar', __METHOD__, $obj{base}DTO);\n\n      $objInfraException = new InfraException();\n\n"
        + create_lines
        + f"      $objInfraException->lancarValidacoes();\n\n      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      return $obj{base}BD->cadastrar($obj{base}DTO);\n\n"
        + f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro cadastrando {singular}.', $e);\n    }}\n  }}\n\n"
        + f"  protected function alterarControlado({base}DTO $obj{base}DTO): void\n  {{\n"
        + f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_alterar', __METHOD__, $obj{base}DTO);\n\n      $objInfraException = new InfraException();\n\n"
        + update_lines
        + f"      $objInfraException->lancarValidacoes();\n\n      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      $obj{base}BD->alterar($obj{base}DTO);\n\n"
        + f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro alterando {singular}.', $e);\n    }}\n  }}\n\n"
        + f"  protected function excluirControlado(array $arrObj{base}DTO): void\n  {{\n"
        + f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_excluir', __METHOD__, $arrObj{base}DTO);\n\n      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      foreach ($arrObj{base}DTO as $obj{base}DTO) {{\n        $obj{base}BD->excluir($obj{base}DTO);\n      }}\n\n"
        + f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro excluindo {singular}.', $e);\n    }}\n  }}\n\n"
        + f"  protected function consultarConectado({base}DTO $obj{base}DTO): ?{base}DTO\n  {{\n"
        + f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_consultar', __METHOD__, $obj{base}DTO);\n\n      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      return $obj{base}BD->consultar($obj{base}DTO);\n\n"
        + f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro consultando {singular}.', $e);\n    }}\n  }}\n\n"
        + f"  protected function listarConectado({base}DTO $obj{base}DTO): array\n  {{\n"
        + f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_listar', __METHOD__, $obj{base}DTO);\n\n      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      return $obj{base}BD->listar($obj{base}DTO);\n\n"
        + f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro listando {plural}.', $e);\n    }}\n  }}\n\n"
        + f"  protected function contarConectado({base}DTO $obj{base}DTO): int\n  {{\n"
        + f"    try {{\n      SessaoSEI::getInstance()->validarAuditarPermissao('{table_name}_listar', __METHOD__, $obj{base}DTO);\n\n      $obj{base}BD = new {base}BD($this->getObjInfraIBanco());\n      return $obj{base}BD->contar($obj{base}DTO);\n\n"
        + f"    }} catch (Exception $e) {{\n      throw new InfraException('Erro contando {singular}.', $e);\n    }}\n  }}\n\n"
        + logical_methods
        + "}\n"
    )


def render_lista_nn(data: dict) -> str:
    """Render lista page for N:N (composite PK) entities."""
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = data["entidade"]["singular"]
    plural = data["entidade"]["plural"]
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
                "attr": related_attribute_name(relation),
                "label": nn_rels[index].get("rotulo", pascal_case(pk_col["nome"])),
            }
        )

    display_return_lines = "".join(
        f"  $obj{base}DTO->ret{info['attr']}();\n" for info in display_infos
    )
    header_columns = "".join(
        f"    $strResultado .= '<th class=\"infraTh\">{info['label']}</th>'.\"\\n\";\n"
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
            f"  <?php\n  PaginaSEI::getInstance()->fecharAreaDados();\n"
            f"  PaginaSEI::getInstance()->abrirAreaDados('5em');\n  ?>\n"
            f'  <label id="lbl{rel_base}" for="sel{rel_base}" accesskey="{ak}" class="infraLabelOpcional">'
            f"{label}:</label>\n"
            f'  <select id="sel{rel_base}" name="sel{rel_base}" onchange="this.form.submit();" '
            f'class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" >\n'
            f"  <?=$strItensSel{rel_base}??false?>\n  </select>\n\n"
        )
        style_parts += (
            f"#lbl{rel_base} {{position:absolute;left:0;top:0;width:25%;}}\n"
            f"#sel{rel_base} {{position:absolute;left:0;top:40%;width:25%;}}\n\n"
        )

    return (
        php_header()
        + "\n\ntry {\n"
        + PAGE_REQUIRE_SEI
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
        + f"  PaginaSEI::getInstance()->salvarCamposPost(array({sel_names}));\n\n"
        + "  switch ($strAcao) {\n"
        + f"    case '{table_name}_excluir':\n"
        + "      try {\n"
        + f"        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();\n"
        + f"        $arrObj{base}DTO = array();\n"
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
        + f"      if (PaginaSEI::GET('acao_origem')==='{table_name}_cadastrar' && isset($_GET['{pk1_param}'], $_GET['{pk2_param}'])) {{\n"
        + f"        PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('{pk1_param}').'-'.PaginaSEI::GET('{pk2_param}'));\n"
        + "      }\n"
        + "      break;\n\n"
        + f"    case '{table_name}_listar':\n"
        + f"      $strTitulo = '{plural}';\n"
        + "      break;\n\n"
        + "    default:\n"
        + "      throw new InfraException(\"Ação '\".$strAcao.\"' não reconhecida.\");\n"
        + "  }\n\n"
        + "  $arrComandos = array();\n"
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
        + f"  PaginaSEI::getInstance()->prepararOrdenacao($obj{base}DTO, '{sort_field}', InfraDTO::$TIPO_ORDENACAO_ASC);\n\n"
        + f"  $obj{base}RN = new {base}RN();\n"
        + f"  $arrObj{base}DTO = $obj{base}RN->listar($obj{base}DTO);\n\n"
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
        + f"        $strResultado .= '<td style=\"vertical-align: center\">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObj{base}DTO[$i]->get{pk1_attr}().'-'.$arrObj{base}DTO[$i]->get{pk2_attr}(),{check_description}).'</td>';\n"
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
        + "  PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
        + "  ?>\n"
        + filter_form
        + "  <?php\n"
        + "  PaginaSEI::getInstance()->fecharAreaDados();\n"
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
    singular = data["entidade"]["singular"]
    article = data["entidade"]["artigo"]
    nn_rels = data["relacionamentosNn"]
    pk1_col = [c for c in data["colunas"] if c.get("chavePrimaria")][0]
    pk2_col = [c for c in data["colunas"] if c.get("chavePrimaria")][1]
    pk1_attr = attribute_name(pk1_col)
    pk2_attr = attribute_name(pk2_col)
    pk1_param = pk1_col["nome"]
    pk2_param = pk2_col["nome"]

    # extra (non-PK) columns
    extra_cols = [c for c in data["colunas"] if not c.get("chavePrimaria")]

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
        ak = label[0].lower()
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
            f"<?php\nPaginaSEI::getInstance()->fecharAreaDados();\n"
            f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n?>\n"
            f'  <label id="lbl{rel_base}" for="sel{rel_base}" accesskey="{ak}" class="infraLabelObrigatorio">{label}:</label>\n'
            f'  <select id="sel{rel_base}" name="sel{rel_base}" class="infraSelect" '
            f'tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" <?=$strDesabilitar?>>\n'
            f"  <?=$strItensSel{rel_base}??false?>\n  </select>\n"
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
        html_name = "txt" + (
            col_attr[3:]
            if col_attr.startswith(("Str", "Num", "Din", "Dta"))
            else col_attr
        )
        ak = col_label[0].lower() if col_label else "x"
        extra_post_block += (
            f"      $obj{base}DTO->set{col_attr}(PaginaSEI::POST('{html_name}'));\n"
        )
        style_parts += (
            f"#{html_name.replace('txt', 'lbl', 1).replace('lbl', 'lbl')} {{position:absolute;left:0;top:0;width:25%;}}\n"
            f"#{html_name} {{position:absolute;left:0;top:40%;width:25%;}}\n\n"
        )
        col_is_required = col.get("obrigatorio", False)
        col_label_class = "infraLabelObrigatorio" if col_is_required else "infraLabelOpcional"
        if col["tipoBanco"] in {"datetime", "date", "timestamp"}:
            html_id_cal = (
                f"imgCal{col_attr[3:] if col_attr.startswith(('Dta', 'Dth')) else col_attr}"
            )
            extra_form += (
                f"<?php\nPaginaSEI::getInstance()->fecharAreaDados();\n"
                f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n?>\n"
                f'  <label id="lbl{col_attr}" for="{html_name}" accesskey="{ak}" class="{col_label_class}">{col_label}:</label>\n'
                f'  <input type="text" id="{html_name}" name="{html_name}" onkeypress="return infraMascaraData(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{col_attr}())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                f'  <img id="{html_id_cal}" src="<?=PaginaSEI::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario(\'{html_name}\',this);" />\n'
            )
            if col_is_required:
                extra_js_validation += (
                    f"\n  if (infraTrim(document.getElementById('{html_name}').value)=='') {{\n"
                    f"    alert('Informe {col_label}.');\n"
                    f"    document.getElementById('{html_name}').focus();\n"
                    f"    return false;\n  }}\n\n"
                    f"  if (!infraValidarData(document.getElementById('{html_name}'))) {{\n"
                    f"    return false;\n  }}\n"
                )
        else:
            extra_form += (
                f"<?php\nPaginaSEI::getInstance()->fecharAreaDados();\n"
                f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n?>\n"
                f'  <label id="lbl{col_attr}" for="{html_name}" accesskey="{ak}" class="{col_label_class}">{col_label}:</label>\n'
                f'  <input type="text" id="{html_name}" name="{html_name}" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{col_attr}())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
            )
            if col_is_required:
                extra_js_validation += (
                    f"\n  if (infraTrim(document.getElementById('{html_name}').value)=='') {{\n"
                    f"    alert('Informe {col_label}.');\n"
                    f"    document.getElementById('{html_name}').focus();\n"
                    f"    return false;\n  }}\n"
                )

    # JS validation for selects
    js_sel_validation = ""
    for rel in nn_rels:
        rel_base = class_base(rel["tabelaOrigem"])
        label = rel.get("rotulo", rel_base)
        js_sel_validation += (
            f"  if (!infraSelectSelecionado('sel{rel_base}')) {{\n"
            f"    alert('Selecione um{'' if article == 'o' else 'a'} {label}.');\n"
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
        + PAGE_REQUIRE_SEI
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
        + f"  PaginaSEI::getInstance()->salvarCamposPost(array({sel_names}));\n\n"
        + f"  $obj{base}DTO = new {base}DTO();\n"
        + "  $strDesabilitar = '';\n"
        + "  $arrComandos = array();\n\n"
        + "  switch ($strAcao) {\n"
        + f"    case '{table_name}_cadastrar':\n"
        + f"      $strTitulo = 'Nov{article} {singular}';\n"
        + f'      $arrComandos[] = \'<button type="submit" accesskey="S" name="sbmCadastrar{base}" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>\';\n'
        + f'      $arrComandos[] = \'<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.$strAcao).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>\';\n\n'
        + select_vars
        + extra_post_block
        + f"\n      if (isset($_POST['sbmCadastrar{base}'])) {{\n"
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
        + f"      if (isset($_GET['{pk1_param}'], $_GET['{pk2_param}'])) {{\n"
        + f"        $obj{base}DTO->set{pk1_attr}(PaginaSEI::GET('{pk1_param}'));\n"
        + f"        $obj{base}DTO->set{pk2_attr}(PaginaSEI::GET('{pk2_param}'));\n"
        + f"        $obj{base}DTO->retTodos();\n"
        + f"        $obj{base}RN = new {base}RN();\n"
        + f"        $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n"
        + f"        if ($obj{base}DTO===null) {{\n"
        + '          throw new InfraException("Registro n\u00e3o encontrado.");\n'
        + "        }\n"
        + "      } else {\n"
        + select_post_blocks
        + extra_post_block
        + "      }\n\n"
        + f'      $arrComandos[] = \'<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.$strAcao.PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk1_attr}().\'-\'.$obj{base}DTO->get{pk2_attr}())).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>\';\n\n'
        + f"      if (isset($_POST['sbmAlterar{base}'])) {{\n"
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
        + f"      $obj{base}DTO->set{pk1_attr}(PaginaSEI::GET('{pk1_param}'));\n"
        + f"      $obj{base}DTO->set{pk2_attr}(PaginaSEI::GET('{pk2_param}'));\n"
        + f"      $obj{base}DTO->setBolExclusaoLogica(false);\n"
        + f"      $obj{base}DTO->retTodos();\n"
        + f"      $obj{base}RN = new {base}RN();\n"
        + f"      $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n"
        + f"      if ($obj{base}DTO===null) {{\n"
        + '        throw new InfraException("Registro n\u00e3o encontrado.");\n'
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
        + "PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
        + "?>\n"
        + select_form_blocks
        + extra_form
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharAreaDados();\n"
        + "?>\n"
        + hidden_pks
        + "  <?php\n"
        + "  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);\n"
        + "  ?>\n"
        + "</form>\n"
        + "<?php\n"
        + "PaginaSEI::getInstance()->fecharBody();\n"
        + "PaginaSEI::getInstance()->fecharHtml();\n"
    )


def render_lista(data: dict) -> str:
    if is_nn(data):
        return render_lista_nn(data)
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = data["entidade"]["singular"]
    plural = data["entidade"]["plural"]
    article = data["entidade"]["artigo"]
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
    pk_column = next(
        column for column in data["colunas"] if column.get("chavePrimaria")
    )
    pk_attr = attribute_name(pk_column)
    pk_suffix = pk_attr[3:] if pk_attr.startswith("Num") else pk_attr
    pk_param = pk_column["nome"]
    has_logical_delete = bool(data["regrasGeracao"].get("campoSinAtivo"))
    ui_map = data.get("ui", {}).get("campos", {})
    display_label = ui_map.get(display_field, {}).get(
        "rotulo", ui_label(display_column)
    )
    words = genero_words(article)
    new_label = words["novo"]
    new_button_id = f"btn{new_label}"
    new_label_tail = new_label[1:]

    relation_block = {
        "post_persistence": "",
        "filter_apply": "",
        "filter_select": "",
        "filter_form": "",
        "style": "",
    }

    relations = data.get("relacionamentos", [])
    if relations:
        # Build arrays for salvarCamposPost
        sel_names = [f"'sel{class_base(rel['tabelaReferencia'])}'" for rel in relations]
        post_persistence = f"  PaginaSEI::getInstance()->salvarCamposPost(array({','.join(sel_names)}));\n"

        filter_apply_parts = []
        filter_select_parts = []
        filter_form_parts = []
        style_parts = []

        for rel in relations:
            rel_base = class_base(rel["tabelaReferencia"])
            rel_label = ui_map.get(rel["coluna"], {}).get(
                "rotulo", pascal_case(rel["coluna"])
            )
            rel_ui = ui_map.get(rel["coluna"], {})
            rel_accesskey = rel_ui.get("teclaAtalho", rel_label[0] if rel_label else "")
            rel_var = f"$numId{rel_base}"
            rel_helper = f"montarSelect{pascal_case(strip_common_prefixes(rel['campoExibicao']))}"

            filter_apply_parts.append(
                dedent(
                    f"""
                  {rel_var} = PaginaSEI::getInstance()->recuperarCampo('sel{rel_base}');
                  if ({rel_var}!=='') {{
                    $obj{base}DTO->setNumId{rel_base}({rel_var});
                  }}
                """
                ).rstrip()
            )

            filter_select_parts.append(
                f"  $strItensSel{rel_base} = {rel_base}INT::{rel_helper}('', 'Todos', {rel_var});\n"
            )

            # Build the label with accesskey highlighting
            label_lower = rel_accesskey.lower()
            idx = rel_label.lower().find(label_lower)
            if idx >= 0:
                label_html = (
                    rel_label[:idx]
                    + f'<span class="infraTeclaAtalho">{rel_label[idx]}</span>'
                    + rel_label[idx + 1 :]
                )
            else:
                label_html = (
                    f'<span class="infraTeclaAtalho">{rel_accesskey}</span>{rel_label}'
                )

            filter_form_parts.append(
                dedent(
                    f"""
                PaginaSEI::getInstance()->abrirAreaDados('5em');
                ?>
                  <label id="lbl{rel_base}" for="sel{rel_base}" accesskey="{label_lower}" class="infraLabelOpcional">{label_html}:</label>
                  <select id="sel{rel_base}" name="sel{rel_base}" onchange="this.form.submit();" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>">
                  <?=$strItensSel{rel_base}??false?>
                  </select>
                <?php
                PaginaSEI::getInstance()->fecharAreaDados();
                """
                ).rstrip()
            )

            style_parts.append(
                dedent(
                    f"""
                #lbl{rel_base} {{position:absolute;left:0;top:0;width:25%;}}
                #sel{rel_base} {{position:absolute;left:0;top:40%;width:25%;}}
                """
                ).rstrip()
            )

        relation_block = {
            "post_persistence": post_persistence,
            "filter_apply": "\n".join(filter_apply_parts),
            "filter_select": "".join(filter_select_parts),
            "filter_form": "\n".join(filter_form_parts),
            "style": "\n".join(style_parts),
        }

    if has_logical_delete:
        logical_cases = dedent(
            f"""
                case '{table_name}_desativar':
                  try {{
                    $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
                    $arrObj{base}DTO = array();
                    foreach ($arrStrIds as $strId) {{
                      $obj{base}DTO = new {base}DTO();
                      $obj{base}DTO->set{pk_attr}($strId);
                      $arrObj{base}DTO[] = $obj{base}DTO;
                    }}
                    $obj{base}RN = new {base}RN();
                    $obj{base}RN->desativar($arrObj{base}DTO);
                    PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
                  }} catch (Exception $e) {{
                    PaginaSEI::getInstance()->processarExcecao($e);
                  }}
                  header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.$strAcao));
                  die;

                case '{table_name}_reativar':
                  try {{
                    $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
                    $arrObj{base}DTO = array();
                    foreach ($arrStrIds as $strId) {{
                      $obj{base}DTO = new {base}DTO();
                      $obj{base}DTO->set{pk_attr}($strId);
                      $arrObj{base}DTO[] = $obj{base}DTO;
                    }}
                    $obj{base}RN = new {base}RN();
                    $obj{base}RN->reativar($arrObj{base}DTO);
                    PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
                  }} catch (Exception $e) {{
                    PaginaSEI::getInstance()->processarExcecao($e);
                  }}
                  header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.$strAcao));
                  die;
            """
        ).rstrip()
        filter_apply_extra = dedent(
            f"""
                $obj{base}DTO->setBolExclusaoLogica(false);
                if ($strAcao==='{table_name}_selecionar') {{
                  $obj{base}DTO->setStrSinAtivo('S');
                }}
            """
        ).rstrip()
        action_flags = dedent(
            f"""
                if ($strAcao==='{table_name}_selecionar') {{
                  $bolAcaoReativar = false;
                  $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');
                  $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');
                  $bolAcaoImprimir = false;
                  $bolAcaoExcluir = false;
                  $bolAcaoDesativar = false;
                  $bolCheck = true;
                }} else {{
                  $bolAcaoReativar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_reativar');
                  $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');
                  $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');
                  $bolAcaoImprimir = true;
                  $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('{table_name}_excluir');
                  $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_desativar');
                }}
            """
        ).rstrip()
        bulk_commands = dedent(
            f"""
                if ($bolAcaoDesativar) {{
                  $bolCheck = true;
                  $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
                  $strLinkDesativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_desativar&acao_origem='.$strAcao);
                }}

                if ($bolAcaoReativar) {{
                  $bolCheck = true;
                  $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
                  $strLinkReativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_reativar&acao_origem='.$strAcao.'&acao_confirmada=sim');
                }}

                if ($bolAcaoExcluir) {{
                  $bolCheck = true;
                  $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
                  $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_excluir&acao_origem='.$strAcao);
                }}
            """
        ).rstrip()
        js_extra = (
            dedent(
                """
                <?php if ($bolAcaoDesativar??false) { ?>
                function acaoDesativar(id,desc)
                {
                  if (confirm('Confirma desativação __DO__ __SINGULAR__ "' + desc + '"?')) {
                    document.getElementById('hdnInfraItemId').value=id;
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkDesativar??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }

                function acaoDesativacaoMultipla()
                {
                  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
                    alert('__NENHUM__ __SINGULAR__ __SELECIONADO__.');
                    return;
                  }
                  if (confirm('Confirma desativação __DOS__ __PLURAL__ __SELECIONADOS__?')) {
                    document.getElementById('hdnInfraItemId').value='';
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkDesativar??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }
                <?php } ?>

                <?php if ($bolAcaoReativar??false) { ?>
                function acaoReativar(id,desc)
                {
                  if (confirm('Confirma reativação __DO__ __SINGULAR__ "' + desc + '"?')) {
                    document.getElementById('hdnInfraItemId').value=id;
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkReativar??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }

                function acaoReativacaoMultipla()
                {
                  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
                    alert('__NENHUM__ __SINGULAR__ __SELECIONADO__.');
                    return;
                  }
                  if (confirm('Confirma reativação __DOS__ __PLURAL__ __SELECIONADOS__?')) {
                    document.getElementById('hdnInfraItemId').value='';
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkReativar??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }
                <?php } ?>

                <?php if ($bolAcaoExcluir??false) { ?>
                function acaoExcluir(id,desc)
                {
                  if (confirm('Confirma exclusão __DO__ __SINGULAR__ "' + desc + '"?')) {
                    document.getElementById('hdnInfraItemId').value=id;
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkExcluir??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }

                function acaoExclusaoMultipla()
                {
                  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
                    alert('__NENHUM__ __SINGULAR__ __SELECIONADO__.');
                    return;
                  }
                  if (confirm('Confirma exclusão __DOS__ __PLURAL__ __SELECIONADOS__?')) {
                    document.getElementById('hdnInfraItemId').value='';
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkExcluir??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }
                <?php } ?>
            """
            )
            .replace("__SINGULAR__", singular)
            .replace("__PLURAL__", plural)
            .replace("__NENHUM__", words["nenhum"])
            .replace("__SELECIONADO__", words["selecionado"])
            .replace("__SELECIONADOS__", words["selecionados"])
            .replace("__DO__", words["do"])
            .replace("__DOS__", words["dos"])
            .replace("__BASE__", base)
            .rstrip()
        )
    else:
        logical_cases = dedent(
            f"""
                /*
                case '{table_name}_desativar':
                case '{table_name}_reativar':
                */
            """
        ).rstrip()
        filter_apply_extra = ""
        action_flags = dedent(
            f"""
                if ($strAcao==='{table_name}_selecionar') {{
                  $bolAcaoReativar = false;
                  $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');
                  $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');
                  $bolAcaoImprimir = false;
                  $bolAcaoExcluir = false;
                  $bolAcaoDesativar = false;
                  $bolCheck = true;
                }} else {{
                  $bolAcaoReativar = false;
                  $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_consultar');
                  $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_alterar');
                  $bolAcaoImprimir = true;
                  $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('{table_name}_excluir');
                  $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_desativar');
                }}
            """
        ).rstrip()
        bulk_commands = dedent(
            f"""
                if ($bolAcaoExcluir) {{
                  $bolCheck = true;
                  $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
                  $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_excluir&acao_origem='.$strAcao);
                }}
            """
        ).rstrip()
        js_extra = (
            dedent(
                """
                <?php /* if ($bolAcaoDesativar??false) { ?>
                function acaoDesativar(id,desc) {}
                function acaoDesativacaoMultipla() {}
                <?php } */ ?>

                <?php if ($bolAcaoExcluir??false) { ?>
                function acaoExcluir(id,desc)
                {
                  if (confirm('Confirma exclusão __DO__ __SINGULAR__ "' + desc + '"?')) {
                    document.getElementById('hdnInfraItemId').value=id;
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkExcluir??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }

                function acaoExclusaoMultipla()
                {
                  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
                    alert('__NENHUM__ __SINGULAR__ __SELECIONADO__.');
                    return;
                  }
                  if (confirm('Confirma exclusão __DOS__ __PLURAL__ __SELECIONADOS__?')) {
                    document.getElementById('hdnInfraItemId').value='';
                    document.getElementById('frm__BASE__Lista').action='<?=$strLinkExcluir??false?>';
                    document.getElementById('frm__BASE__Lista').submit();
                  }
                }
                <?php } ?>
            """
            )
            .replace("__SINGULAR__", singular)
            .replace("__PLURAL__", plural)
            .replace("__NENHUM__", words["nenhum"])
            .replace("__SELECIONADO__", words["selecionado"])
            .replace("__SELECIONADOS__", words["selecionados"])
            .replace("__DO__", words["do"])
            .replace("__DOS__", words["dos"])
            .replace("__BASE__", base)
            .rstrip()
        )

    switch_cases = dedent(
        f"""
            case '{table_name}_excluir':
              try {{
                $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
                $arrObj{base}DTO = array();
                foreach ($arrStrIds as $strId) {{
                  $obj{base}DTO = new {base}DTO();
                  $obj{base}DTO->set{pk_attr}($strId);
                  $arrObj{base}DTO[] = $obj{base}DTO;
                }}
                $obj{base}RN = new {base}RN();
                $obj{base}RN->excluir($arrObj{base}DTO);
                PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
              }} catch (Exception $e) {{
                PaginaSEI::getInstance()->processarExcecao($e);
              }}
              header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.$strAcao));
              die;

            {logical_cases}

            case '{table_name}_selecionar':
              $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar {singular}','Selecionar {plural}');
              if (PaginaSEI::GET('acao_origem')==='{table_name}_cadastrar' && isset($_GET['{pk_param}'])) {{
                PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('{pk_param}'));
              }}
              break;

            case '{table_name}_listar':
              $strTitulo = '{plural}';
              break;
        """
    ).rstrip()

    top_commands = dedent(
        f"""
            if ($strAcao==='{table_name}_selecionar') {{
              $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
            }}

            $bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('{table_name}_cadastrar');
            if ($bolAcaoCadastrar) {{
              $arrComandos[] = '<button type="button" accesskey="N" id="{new_button_id}" value="{new_label}" onclick="location.href=\\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_cadastrar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao')).'\\'" class="infraButton"><span class="infraTeclaAtalho">N</span>{new_label_tail}</button>';
            }}
        """
    ).rstrip()

    dto_return_lines = dedent(
        f"""
            $obj{base}DTO->ret{pk_attr}();
            $obj{base}DTO->ret{display_attr}();
            {"$obj" + base + "DTO->retStrSinAtivo();" if has_logical_delete else ""}
        """
    ).rstrip()

    if has_logical_delete:
        tr_color_logic = (
            f'      if ($arrObj{base}DTO[$i]->getStrSinAtivo() == \'S\') {{\n'
            f'        $strCssTr = ($strCssTr === \'<tr class="infraTrClara">\') ? \'<tr class="infraTrEscura">\' : \'<tr class="infraTrClara">\';\n'
            f'      }} else {{\n'
            f'        $strCssTr = \'<tr class="infraTrVermelha">\';\n'
            f'      }}\n'
            f'      $strResultado .= $strCssTr;'
        )
    else:
        tr_color_logic = (
            '      $strCssTr = ($strCssTr === \'<tr class="infraTrClara">\') ? \'<tr class="infraTrEscura">\' : \'<tr class="infraTrClara">\';\n'
            '      $strResultado .= $strCssTr;'
        )

    filter_apply_lines = relation_block["filter_apply"]
    if filter_apply_extra:
        filter_apply_lines = (filter_apply_lines + "\n" + filter_apply_extra).strip()

    header_lines = dedent(
        f"""
            if ($bolCheck) {{
              $strResultado .= '<th class="infraTh" style="width: 1%">'.PaginaSEI::getInstance()->getThCheck().'</th>' . "\n";
            }}
            $strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($obj{base}DTO,'{display_label}','{display_suffix}',$arrObj{base}DTO).'</th>' . "\n";
            $strResultado .= '<th class="infraTh">Ações</th>' . "\n";
        """
    ).rstrip()

    desativar_cond = (
        f"$bolAcaoDesativar && $arrObj{base}DTO[$i]->getStrSinAtivo() == 'S'"
        if has_logical_delete
        else "$bolAcaoDesativar"
    )
    reativar_cond = (
        f"$bolAcaoReativar && $arrObj{base}DTO[$i]->getStrSinAtivo() == 'N'"
        if has_logical_delete
        else "$bolAcaoReativar"
    )

    row_lines = dedent(
        f"""
            if ($bolCheck) {{
              $strResultado .= '<td style="vertical-align: center">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObj{base}DTO[$i]->get{pk_attr}(),$arrObj{base}DTO[$i]->get{display_attr}()).'</td>';
            }}
            $strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObj{base}DTO[$i]->get{display_attr}()).'</td>';
            $strResultado .= '<td style="text-align: center">';
            $strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObj{base}DTO[$i]->get{pk_attr}());

            if ($bolAcaoConsultar) {{
              $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_consultar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&{pk_param}='.$arrObj{base}DTO[$i]->get{pk_attr}()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeConsultar().'" title="Consultar {singular}" alt="Consultar {singular}" class="infraImg" /></a>&nbsp;';
            }}

            if ($bolAcaoAlterar) {{
              $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao={table_name}_alterar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&{pk_param}='.$arrObj{base}DTO[$i]->get{pk_attr}()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeAlterar().'" title="Alterar {singular}" alt="Alterar {singular}" class="infraImg" /></a>&nbsp;';
            }}

            if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {{
              $strId = $arrObj{base}DTO[$i]->get{pk_attr}();
              $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript($arrObj{base}DTO[$i]->get{display_attr}());
            }}

            if ({desativar_cond}) {{
              $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\\''.$strId.'\\',\\''.$strDescricao.'\\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeDesativar().'" title="Desativar {singular}" alt="Desativar {singular}" class="infraImg" /></a>&nbsp;';
            }}

            if ({reativar_cond}) {{
              $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\\''.$strId.'\\',\\''.$strDescricao.'\\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeReativar().'" title="Reativar {singular}" alt="Reativar {singular}" class="infraImg" /></a>&nbsp;';
            }}

            if ($bolAcaoExcluir) {{
              $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\\''.$strId.'\\',\\''.$strDescricao.'\\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeExcluir().'" title="Excluir {singular}" alt="Excluir {singular}" class="infraImg" /></a>&nbsp;';
            }}
        """
    ).rstrip()

    bottom_commands = dedent(
        f"""
            if (PaginaSEI::GET('acao')==='{table_name}_selecionar') {{
              $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
            }} else {{
              $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao')).'\\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
            }}
        """
    ).rstrip()

    initialize_lines = dedent(
        f"""
            if ('<?=$strAcao??false?>' === '{table_name}_selecionar') {{
              infraReceberSelecao();
              document.getElementById('btnFecharSelecao').focus();
            }} else {{
              document.getElementById('btnFechar').focus();
            }}
            infraEfeitoTabelas(true);
        """
    ).rstrip()

    js_functions = dedent(
        f"""
            {js_extra}
        """
    ).strip()

    template_path = Path(__file__).resolve().parent / "templates/lista.php.tpl"
    template = read_latin1(template_path)
    replacements = {
        "{{TABLE_NAME}}": table_name,
        "{{CLASS_NAME}}": base,
        "{{ENTITY_LABEL_PLURAL}}": plural,
        "{{LIST_POST_PERSISTENCE_LINES}}": relation_block["post_persistence"].rstrip(),
        "{{LIST_SWITCH_CASES}}": switch_cases,
        "{{LIST_TOP_COMMANDS}}": top_commands,
        "{{LIST_DTO_RETURN_LINES}}": dto_return_lines,
        "{{LIST_FILTER_APPLY_LINES}}": filter_apply_lines,
        "{{LIST_SORT_FIELD}}": display_suffix,
        "{{LIST_ACTION_FLAG_LINES}}": action_flags,
        "{{LIST_BULK_COMMAND_LINES}}": bulk_commands,
        "{{LIST_HEADER_LINES}}": header_lines,
        "{{LIST_TR_COLOR_LOGIC}}": tr_color_logic,
        "{{LIST_ROW_LINES}}": row_lines,
        "{{LIST_BOTTOM_COMMANDS}}": bottom_commands,
        "{{LIST_FILTER_SELECT_LINES}}": relation_block["filter_select"].rstrip(),
        "{{LIST_STYLE_LINES}}": relation_block["style"],
        "{{LIST_INITIALIZE_LINES}}": initialize_lines,
        "{{LIST_JAVASCRIPT_FUNCTIONS}}": js_functions,
        "{{LIST_FILTER_FORM_BLOCK}}": relation_block["filter_form"],
    }
    for placeholder, value in replacements.items():
        template = template.replace(placeholder, value)
    template = template.replace("PaginaSEI::GET('acao')", "$strAcao")
    template = template.replace("$strAcao = $strAcao;", "$strAcao = PaginaSEI::GET('acao');")
    return template


def render_cadastro(data: dict) -> str:
    if is_nn(data):
        return render_cadastro_nn(data)
    table_name = data["entidade"]["tabela"]
    base = class_base(table_name)
    singular = data["entidade"]["singular"]
    plural = data["entidade"]["plural"]
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

    display_column = next(
        column for column in data["colunas"] if column["nome"] == display_field
    )
    display_attr = attribute_name(display_column)

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
            if not col.get("chavePrimaria") and col["nome"] != "sin_ativo"
        ]

    # Build field info list
    fields = []
    for fname in field_order:
        col = next((c for c in data["colunas"] if c["nome"] == fname), None)
        if col is None or col.get("chavePrimaria") or col["nome"] == "sin_ativo":
            continue
        ui = ui_map.get(fname, {})
        suf = col_suffix(col)
        attr = attribute_name(col)
        label = ui.get("rotulo", pascal_case(strip_common_prefixes(fname)))
        accesskey = ui.get("teclaAtalho", "")
        required = col.get("obrigatorio", False)
        rel = rel_map.get(fname)
        is_fk = rel is not None

        if is_fk:
            widget = "select"
            rel_base = class_base(rel["tabelaReferencia"])
            fk_helper = f"montarSelect{pascal_case(strip_common_prefixes(rel['campoExibicao']))}"
        else:
            rel_base = ""
            fk_helper = ""
            tipo = col["tipoBanco"]
            if tipo in {"datetime", "date", "timestamp"}:
                widget = "date"
            elif tipo == "numeric":
                widget = "money"
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
                "required": required,
                "widget": widget,
                "is_fk": is_fk,
                "rel_base": rel_base,
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
        sel_names = ", ".join(f"'sel{f['rel_base']}'" for f in fk_fields)
        salvar_campos = (
            f"  PaginaSEI::getInstance()->salvarCamposPost(array({sel_names}));\n\n"
        )

    # --- Build case cadastrar: field assignments ---
    def render_cadastrar_fields():
        lines = []
        lines.append(f"      $obj{base}DTO->set{pk_attr}(null);\n")
        for f in fields:
            if f["is_fk"]:
                var = f"$numId{f['rel_base']}"
                lines.append(
                    f"      {var} = PaginaSEI::getInstance()->recuperarCampo('sel{f['rel_base']}');\n"
                )
                lines.append(f"      if ({var} !=='') {{\n")
                lines.append(f"        $obj{base}DTO->set{f['attr']}({var});\n")
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
        return "".join(lines)

    # --- Build case alterar: POST field assignments ---
    def render_alterar_post_fields():
        lines = []
        lines.append(
            f"        $obj{base}DTO->set{pk_attr}(PaginaSEI::POST('hdnId{base}'));\n"
        )
        for f in fields:
            if f["is_fk"]:
                lines.append(
                    f"        $obj{base}DTO->set{f['attr']}(PaginaSEI::POST('sel{f['rel_base']}'));\n"
                )
            else:
                html_id = _html_id(f)
                lines.append(
                    f"        $obj{base}DTO->set{f['attr']}(PaginaSEI::POST('{html_id}'));\n"
                )
        if has_sin_ativo:
            lines.append(f"        $obj{base}DTO->setStrSinAtivo('S');\n")
        return "".join(lines)

    # --- Build FK select items ---
    def render_fk_selects():
        lines = []
        for f in fk_fields:
            lines.append(
                f"  $strItensSel{f['rel_base']} = {class_base(rel_map[f['name']]['tabelaReferencia'])}INT::{f['fk_helper']}('null','&nbsp;',$obj{base}DTO->get{f['attr']}());\n"
            )
        return "".join(lines)

    # --- Build CSS style lines ---
    def render_style():
        lines = []
        for f in fields:
            if f["is_fk"]:
                lines.append(
                    f"#lbl{f['rel_base']} {{position:absolute;left:0;top:0;width:{f['css_width']};}}"
                )
                lines.append(
                    f"#sel{f['rel_base']} {{position:absolute;left:0;top:40%;width:{f['css_width']};}}"
                )
            elif f["widget"] == "date":
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
            if f["is_fk"]:
                sel_id = f"sel{f['rel_base']}"
                lines.append(f"  if (!infraSelectSelecionado('{sel_id}')) {{")
                lines.append(f"    alert('Selecione um {f['label']}.');")
                lines.append(f"    document.getElementById('{sel_id}').focus();")
                lines.append(f"    return false;")
                lines.append(f"  }}")
                lines.append("")
            elif f["widget"] == "date":
                html_id = _html_id(f)
                lines.append(
                    f"  if (infraTrim(document.getElementById('{html_id}').value)=='') {{"
                )
                lines.append(f"    alert('Informe {f['label']}.');")
                lines.append(f"    document.getElementById('{html_id}').focus();")
                lines.append(f"    return false;")
                lines.append(f"  }}")
                lines.append("")
                lines.append(
                    f"  if (!infraValidarData(document.getElementById('{html_id}'))) {{"
                )
                lines.append(f"    return false;")
                lines.append(f"  }}")
                lines.append("")
            else:
                html_id = _html_id(f)
                lines.append(
                    f"  if (infraTrim(document.getElementById('{html_id}').value)=='') {{"
                )
                lines.append(f"    alert('Informe {f['label']}.');")
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

            if f["is_fk"]:
                sel_id = f"sel{f['rel_base']}"
                block = (
                    f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                    f"?>\n"
                    f'  <label id="lbl{f["rel_base"]}" for="{sel_id}" accesskey="{f["accesskey"].lower()}" class="{label_class}">{label_html}:</label>\n'
                    f'  <select id="{sel_id}" name="{sel_id}" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>">\n'
                    f"  <?=$strItensSel{f['rel_base']}??false?>\n"
                    f"  </select>\n"
                    f"<?php\n"
                    f"PaginaSEI::getInstance()->fecharAreaDados();"
                )
            elif f["widget"] == "date":
                html_id = _html_id(f)
                block = (
                    f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                    f"?>\n"
                    f'  <label id="lbl{f["suffix"]}" for="{html_id}" accesskey="{f["accesskey"].lower()}" class="{label_class}">{label_html}:</label>\n'
                    f'  <input type="text" id="{html_id}" name="{html_id}" onkeypress="return infraMascaraData(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{f["attr"]}())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                    f'  <img id="imgCal{f["suffix"]}" title="Selecionar {f["label"]}" alt="Selecionar {f["label"]}" src="<?=PaginaSEI::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario(\'{html_id}\',this);" />\n'
                    f"<?php\n"
                    f"PaginaSEI::getInstance()->fecharAreaDados();"
                )
            elif f["widget"] == "money":
                html_id = _html_id(f)
                block = (
                    f"PaginaSEI::getInstance()->abrirAreaDados('5em');\n"
                    f"?>\n"
                    f'  <label id="lbl{f["suffix"]}" for="{html_id}" accesskey="{f["accesskey"].lower()}" class="{label_class}">{label_html}:</label>\n'
                    f'  <input type="text" id="{html_id}" name="{html_id}" onkeydown="return infraMascaraDinheiro(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{f["attr"]}())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
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
                    f'  <label id="lbl{f["suffix"]}" for="{html_id}" accesskey="{f["accesskey"].lower()}" class="{label_class}">{label_html}:</label>\n'
                    f'  <input type="text" id="{html_id}" name="{html_id}" class="infraText" value="<?=PaginaSEI::tratarHTML($obj{base}DTO->get{f["attr"]}())?>"{mascara_attr}{maxlen_attr} tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />\n'
                    f"<?php\n"
                    f"PaginaSEI::getInstance()->fecharAreaDados();"
                )
            blocks.append(block)
        return "\n".join(blocks)

    # Determine first focus element
    if fk_fields:
        first_focus = f"sel{fk_fields[0]['rel_base']}"
    elif non_fk_fields:
        first_focus = _html_id(non_fk_fields[0])
    else:
        first_focus = "btnCancelar"

    # Assemble the full PHP file
    out = []
    out.append(php_header())
    out.append("\n\ntry {\n")
    out.append(PAGE_REQUIRE_SEI)
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
    out.append("  $arrComandos = array();\n")
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
    out.append(f"\n      if (isset($_POST['sbmCadastrar{base}'])) {{\n")
    out.append(f"        try {{\n")
    out.append(f"          $obj{base}RN = new {base}RN();\n")
    out.append(f"          $obj{base}DTO = $obj{base}RN->cadastrar($obj{base}DTO);\n")
    out.append(
        f"          PaginaSEI::getInstance()->adicionarMensagem('{singular} \"'.PaginaSEI::tratarHTML($obj{base}DTO->get{display_attr}()).'\" {created_word} com sucesso.');\n"
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
    out.append(f"      if (isset($_GET['{pk_param}'])) {{\n")
    out.append(f"        $obj{base}DTO->set{pk_attr}(PaginaSEI::GET('{pk_param}'));\n")
    out.append(f"        $obj{base}DTO->retTodos();\n")
    out.append(f"        $obj{base}RN = new {base}RN();\n")
    out.append(f"        $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n")
    out.append(f"        if ($obj{base}DTO===null) {{\n")
    out.append('          throw new InfraException("Registro não encontrado.");\n')
    out.append("        }\n")
    out.append("      } else {\n")
    out.append(render_alterar_post_fields())
    out.append("      }\n\n")
    out.append(
        f'      $arrComandos[] = \'<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\\\'\'.SessaoSEI::getInstance()->assinarLink(\'controlador.php?acao=\'.PaginaSEI::getInstance()->getAcaoRetorno().\'&acao_origem=\'.PaginaSEI::GET(\'acao\').PaginaSEI::getInstance()->montarAncora($obj{base}DTO->get{pk_attr}())).\'\\\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>\';\n\n'
    )
    out.append(f"      if (isset($_POST['sbmAlterar{base}'])) {{\n")
    out.append(f"        try {{\n")
    out.append(f"          $obj{base}RN = new {base}RN();\n")
    out.append(f"          $obj{base}RN->alterar($obj{base}DTO);\n")
    out.append(
        f"          PaginaSEI::getInstance()->adicionarMensagem('{singular} \"'.PaginaSEI::tratarHTML($obj{base}DTO->get{display_attr}()).'\" {altered_word} com sucesso.');\n"
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
    out.append(f"      $obj{base}DTO->set{pk_attr}(PaginaSEI::GET('{pk_param}'));\n")
    out.append(f"      $obj{base}DTO->setBolExclusaoLogica(false);\n")
    out.append(f"      $obj{base}DTO->retTodos();\n")
    out.append(f"      $obj{base}RN = new {base}RN();\n")
    out.append(f"      $obj{base}DTO = $obj{base}RN->consultar($obj{base}DTO);\n")
    out.append(f"      if ($obj{base}DTO===null) {{\n")
    out.append('        throw new InfraException("Registro não encontrado.");\n')
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
        CLASS_REQUIRE_SEI,
        f"class {base}INT extends InfraINT\n",
        "{\n\n",
    ]

    if is_nn(data):
        # N:N INT: method receives both PKs as optional filters
        pk1, pk2 = pk_columns[0], pk_columns[1]
        pk1_attr = attribute_name(pk1)
        pk2_attr = attribute_name(pk2)
        pk1_var = "$" + pk1_attr[0].lower() + pk1_attr[1:]
        pk2_var = "$" + pk2_attr[0].lower() + pk2_attr[1:]
        pk1_suffix = pk1_attr[3:] if pk1_attr.startswith("Num") else pk1_attr
        method_name_nn = f"montarSelect{pk1_suffix}"
        lines.extend(
            [
                f"  public static function {method_name_nn}($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, {pk1_var}='', {pk2_var}=''): string\n",
                "  {\n",
                f"    $obj{base}DTO = new {base}DTO();\n",
                f"    $obj{base}DTO->ret{pk1_attr}();\n",
                f"    $obj{base}DTO->ret{pk2_attr}();\n\n",
                f"    if ({pk1_var}!=='') {{\n",
                f"      $obj{base}DTO->set{pk1_attr}({pk1_var});\n",
                "    }\n\n",
                f"    if ({pk2_var}!=='') {{\n",
                f"      $obj{base}DTO->set{pk2_attr}({pk2_var});\n",
                "    }\n\n",
                f"    $obj{base}DTO->setOrd{pk1_attr}(InfraDTO::$TIPO_ORDENACAO_ASC);\n\n",
                f"    $obj{base}RN = new {base}RN();\n",
                f"    $arrObj{base}DTO = $obj{base}RN->listar($obj{base}DTO);\n\n",
                f"    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObj{base}DTO, '{pk1_suffix}', '{pk1_suffix}');\n",
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
                    f"    $obj{base}DTO->ret{display_attr}();\n\n",
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
                        f"      $obj{base}DTO->adicionarCriterio(array('SinAtivo', '{attr_suffix_from_attr(pk_attr)}'), array(InfraDTO::$OPER_IGUAL, InfraDTO::$OPER_IGUAL), array('S', $strValorItemSelecionado), InfraDTO::$OPER_LOGICO_OR);\n",
                        "    } else {\n",
                        f"      $obj{base}DTO->setStrSinAtivo('S');\n",
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
                    f"    $obj{base}DTO->ret{display_attr}();\n\n",
                ]
            )
            if data["regrasGeracao"].get("campoSinAtivo"):
                lines.extend(
                    [
                        "    if ($strValorItemSelecionado!=null) {\n",
                        f"      $obj{base}DTO->setBolExclusaoLogica(false);\n",
                        f"      $obj{base}DTO->adicionarCriterio(array('SinAtivo', '{attr_suffix_from_attr(pk_attr)}'), array(InfraDTO::$OPER_IGUAL, InfraDTO::$OPER_IGUAL), array('S', $strValorItemSelecionado), InfraDTO::$OPER_LOGICO_OR);\n",
                        "    } else {\n",
                        f"      $obj{base}DTO->setStrSinAtivo('S');\n",
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
    if len(sys.argv) != 3:
        return fail("Usage: generate_from_contrato.py <contrato.json> <output-dir>")

    contrato_path = Path(sys.argv[1]).resolve()
    output_dir = Path(sys.argv[2]).resolve()

    if not contrato_path.exists():
        return fail(f"Contrato nao encontrado: {contrato_path}")

    data = json.loads(contrato_path.read_text(encoding="utf-8"))
    table_name = data.get("entidade", {}).get("tabela")
    if not table_name:
        return fail("Contrato sem entidade.tabela")

    try:
        validate_supported_input(data)
    except ValueError as exc:
        return fail(str(exc))

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

    print(
        json.dumps(
            {
                "contrato": str(contrato_path),
                "table": table_name,
                "output_dir": str(output_dir),
                "generated_files": [str(output_dir / name) for name in files],
                "generated_from_metadata": [str(output_dir / name) for name in files],
                "developer_alerts": developer_alerts(data),
            },
            ensure_ascii=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
