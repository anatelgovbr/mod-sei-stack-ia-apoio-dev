#!/usr/bin/env python3
"""
sei-verificacao-controladores
Valida dispatch e regex de controladores de integracao SEI.
Com --exit-code: 0=PASS, 1=WARN, 2=BLOCK
"""

import argparse
from datetime import datetime, timezone
import json
import os
import re
import sys

VERSION = "1.0.0"
SKILL_NAME = "sei-verificacao-controladores"

RE_PROCESSAR_AJAX = re.compile(r"function\s+processarControladorAjax\s*\(", re.DOTALL)
RE_PROCESSAR_AJAX_EXTERNO = re.compile(r"function\s+processarControladorAjaxExterno\s*\(", re.DOTALL)
RE_PROCESSAR_WS = re.compile(r"function\s+processarControladorWebServices\s*\(", re.DOTALL)
RE_TRATAR_LINK = re.compile(r"function\s+tratarLinkSemAssinatura\s*\(", re.DOTALL)
RE_PREG_MATCH = re.compile(r"preg_match\s*\(", re.DOTALL)
RE_SWITCH_ACAO = re.compile(r"switch\s*\(\s*\$strAcao\s*\)|switch\s*\(\s*\$strAcaoAjax\s*\)", re.DOTALL)
RE_SWITCH_SERVICO = re.compile(r"switch\s*\(\s*\$strServico\s*\)", re.DOTALL)
RE_CASE_LITERAL = re.compile(r"case\s+'[^']+'|case\s+\"[^\"]+\"", re.DOTALL)
RE_PREG_PATTERN = re.compile(r"preg_match\s*\(\s*(['\"])((?:\\.|(?!\1).)*)\1", re.DOTALL)

SENSITIVE_PATTERNS = [
    r'"senha"\s*:',
    r"['\"]senha['\"]\s*=>",
    r'"token"\s*:',
    r"['\"]token['\"]\s*=>",
    r'"password"\s*:',
    r"['\"]password['\"]\s*=>",
    r'"api_key"\s*:',
    r"['\"]api_key['\"]\s*=>",
    r'"secret"\s*:',
    r"['\"]secret['\"]\s*=>",
    r'session_id',
]


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


def build_issue(code, rule, message, content, match=None, position=None):
    line = None
    if position is not None:
        line = content[:position].count("\n") + 1
    elif match is not None:
        line = content[:match.start()].count("\n") + 1
    return {"codigo": code, "regra": rule, "mensagem": message, "linha": line}


def extract_method(content, method_name):
    match = re.search(rf"function\s+{re.escape(method_name)}\s*\([^)]*\)\s*(?::\s*[^{{]+)?\{{", content)
    if not match:
        return None, None
    opening = content.find("{", match.start(), match.end())
    depth = 0
    for index in range(opening, len(content)):
        if content[index] == "{":
            depth += 1
        elif content[index] == "}":
            depth -= 1
            if depth == 0:
                return content[opening:index + 1], match
    return content[opening:], match


def dispatch_case_groups(body):
    matches = list(re.finditer(r"\bcase\s+(['\"])([^'\"]+)\1\s*:", body))
    index = 0
    while index < len(matches):
        labels = [matches[index].group(2)]
        first_match = matches[index]
        body_start = matches[index].end()
        while index + 1 < len(matches):
            between = body[body_start:matches[index + 1].start()]
            without_comments = re.sub(r"/\*.*?\*/|//[^\n]*|#[^\n]*", "", between, flags=re.DOTALL)
            if without_comments.strip():
                break
            index += 1
            labels.append(matches[index].group(2))
            body_start = matches[index].end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(body)
        default = re.search(r"\bdefault\s*:", body[body_start:end])
        if default:
            end = body_start + default.start()
        yield labels, body[body_start:end], first_match
        index += 1


def extract_dispatch_switch(body, variables):
    for match in re.finditer(r"\bswitch\s*\(\s*(\$\w+)\s*\)\s*\{", body):
        if match.group(1) not in variables:
            continue
        opening = body.find("{", match.start(), match.end())
        depth = 0
        for index in range(opening, len(body)):
            if body[index] == "{":
                depth += 1
            elif body[index] == "}":
                depth -= 1
                if depth == 0:
                    return body[opening + 1:index], match.group(1), opening + 1
    return None, None, None


def has_restrictive_preg_match(body):
    for match in RE_PREG_PATTERN.finditer(body):
        literal = match.group(2)
        if len(literal) < 3:
            continue
        delimiter = literal[0]
        closing = literal.rfind(delimiter)
        if delimiter.isalnum() or delimiter == "\\" or closing <= 0:
            continue
        pattern = literal[1:closing]
        if pattern.startswith("^") and pattern.endswith("$") and not has_top_level_alternation(pattern[1:-1]) and not re.search(r"(?<!\\)\.\*|(?<!\\)\.\+", pattern):
            return True
    return False


def has_top_level_alternation(pattern):
    depth = 0
    in_character_class = False
    escaped = False
    for character in pattern:
        if escaped:
            escaped = False
        elif character == "\\":
            escaped = True
        elif character == "[":
            in_character_class = True
        elif character == "]" and in_character_class:
            in_character_class = False
        elif not in_character_class:
            if character == "(":
                depth += 1
            elif character == ")":
                depth = max(0, depth - 1)
            elif character == "|" and depth == 0:
                return True
    return False


def first_executable_position(case_body):
    candidates = []
    for match in re.finditer(r"(?:->|::)\s*(\w+)\s*\(|\b([A-Za-z_]\w*)\s*\(", case_body):
        name = match.group(1) or match.group(2)
        statement_end = case_body.find(";", match.start())
        statement = case_body[match.start():statement_end if statement_end >= 0 else len(case_body)]
        if "validarPermissao" in statement or "validarAuditarPermissao" in statement:
            continue
        if name.lower() not in {"if", "elseif", "switch", "while", "for", "foreach", "isset", "empty"}:
            candidates.append(match.start())
    candidates.extend(match.start() for match in re.finditer(r"\b(?:return|echo|print|throw)\b", case_body))
    return min(candidates) if candidates else len(case_body)


OPERATION_GROUPS = (
    {"consultar", "listar", "contar", "pesquisar"},
    {"cadastrar", "incluir"},
    {"alterar", "atualizar", "desativar", "reativar", "bloquear"},
    {"excluir", "remover"},
)


def resource_parts(value):
    tokens = value.split("_")
    for index, token in enumerate(tokens):
        for group in OPERATION_GROUPS:
            if token in group:
                return "_".join(tokens[:index]), group
    return None, None


def resource_authorizes_action(resource, action):
    if resource == action or action.startswith(f"{resource}_"):
        return True
    resource_entity, resource_group = resource_parts(resource)
    action_entity, action_group = resource_parts(action)
    return bool(resource_entity and resource_entity == action_entity and resource_group == action_group)


def validar_ci1(content):
    body, method_match = extract_method(content, "tratarLinkSemAssinatura")
    if body is None:
        return None
    if has_restrictive_preg_match(body):
        return None
    return build_issue("CI001", "CI1", "tratarLinkSemAssinatura sem preg_match restritivo", content, method_match)


def validar_ci2(content):
    body, method_match = extract_method(content, "processarControladorWebServices")
    if body is None:
        return None
    switch_body, _, _ = extract_dispatch_switch(body, {"$strServico"})
    if switch_body is not None and RE_CASE_LITERAL.search(switch_body):
        return None
    return build_issue("CI002", "CI2", "processarControladorWebServices sem dispatch explicito por servico", content, method_match)


def validar_ci3(content):
    errors = []
    for method_name in ("processarControladorAjax", "processarControladorAjaxExterno"):
        body, method_match = extract_method(content, method_name)
        if body is None:
            continue
        switch_body, _, _ = extract_dispatch_switch(body, {"$strAcao", "$strAcaoAjax"})
        if switch_body is None or not RE_CASE_LITERAL.search(switch_body):
            errors.append(build_issue("CI003", "CI3", f"{method_name} sem dispatch explicito por acao", content, method_match))
    return errors


def validar_ci4(content):
    errors = []
    for method_name in ("processarControladorWebServices", "processarControladorAjax", "processarControladorAjaxExterno"):
        body, method_match = extract_method(content, method_name)
        if body is None:
            continue
        variables = {"$strServico"} if method_name == "processarControladorWebServices" else {"$strAcao", "$strAcaoAjax"}
        switch_body, dispatch_variable, switch_offset = extract_dispatch_switch(body, variables)
        if switch_body is None:
            continue
        method_opening = content.find("{", method_match.start(), method_match.end())
        for actions, case_body, case_match in dispatch_case_groups(switch_body):
            authorized_by_dispatch = False
            authorized_actions = set()
            first_executable = first_executable_position(case_body)
            for auth in re.finditer(r"validar(?:Auditar)?Permissao\s*\(\s*([^,)]+)", case_body):
                if auth.start() > first_executable:
                    continue
                argument = auth.group(1).strip()
                if argument == dispatch_variable:
                    authorized_by_dispatch = True
                elif re.fullmatch(r"['\"][^'\"]+['\"]", argument):
                    resource = argument[1:-1]
                    if re.fullmatch(r"md_[a-z0-9]+(?:_[a-z0-9]+)+", resource):
                        authorized_actions.update(action for action in actions if resource_authorizes_action(resource, action))
            authorized = authorized_by_dispatch or set(actions).issubset(authorized_actions)
            if not authorized:
                errors.append(build_issue(
                    "CI004", "CI4",
                    f"acao ou servico '{', '.join(actions)}' sem autorizacao especifica em {method_name}",
                    content,
                    position=method_opening + switch_offset + case_match.start(),
                ))
    return errors


def validar_ci5(content):
    for method_name in ("processarControladorWebServices", "processarControladorAjax", "processarControladorAjaxExterno"):
        body, method_match = extract_method(content, method_name)
        if body is None:
            continue
        for pattern in SENSITIVE_PATTERNS:
            match = re.search(pattern, body, re.DOTALL)
            if match:
                return build_issue("CI005", "CI5", f"payload sensivel potencial em {method_name}: {match.group(0)}", content, method_match)
    return None


def formatar_markdown(file_results, verdict):
    sep = "━" * 54
    lines = [f" {SKILL_NAME} v{VERSION}", sep]

    all_errors = []
    for result in file_results:
        for error in result.get("erros", []):
            all_errors.append({**error, "file": result["file"]})

    if all_errors:
        lines.append("\n BLOQUEIOS")
        for error in all_errors:
            suffix = f" (linha {error['linha']})" if error.get("linha") else ""
            lines.append(f"  ✗ {error['file']}: {error['codigo']} - {error['mensagem']}{suffix}")
        lines.append(sep)

    for result in file_results:
        errors = result.get("erros", [])
        warnings = result.get("avisos", [])
        if errors:
            lines.append(f"\n✗ {result['file']}")
            for error in errors:
                suffix = f" (linha {error['linha']})" if error.get("linha") else ""
                lines.append(f"   ✗ {error['codigo']} - {error['mensagem']}{suffix}")
        if warnings:
            lines.append(f"\n⚠ {result['file']}")
            for warning in warnings:
                suffix = f" (linha {warning['linha']})" if warning.get("linha") else ""
                lines.append(f"   ⚠ {warning['codigo']} - {warning['mensagem']}{suffix}")
        if not errors and not warnings:
            lines.append(f"\n✓ {result['file']} - conformidade total")
        lines.append(sep)
    total_errors = sum(len(item.get("erros", [])) for item in file_results)
    total_warnings = sum(len(item.get("avisos", [])) for item in file_results)
    lines.append(f"\nRESUMO  Erros: {total_errors}  |  Avisos: {total_warnings}")
    lines.append(f"Veredito: {verdict}")
    return "\n".join(lines)


def formatar_json(file_results, verdict):
    all_errors = []
    all_warnings = []
    for result in file_results:
        for error in result.get("erros", []):
            error["file"] = result["file"]
            all_errors.append(error)
        for warning in result.get("avisos", []):
            warning["file"] = result["file"]
            all_warnings.append(warning)
    return {
        "skill": SKILL_NAME,
        "version": VERSION,
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "results": file_results,
        "stats": {"arquivos": len(file_results), "erros": len(all_errors), "avisos": len(all_warnings)},
        "verdict": verdict,
    }


def determinar_verdict(file_results):
    if not file_results:
        return "BLOCK"
    if any(result.get("erros") for result in file_results):
        return "BLOCK"
    if any(result.get("avisos") for result in file_results):
        return "WARN"
    return "PASS"


def audit_file(path):
    try:
        content = open(path, "r", encoding="utf-8", errors="replace").read()
    except Exception as error:
        return {"file": os.path.basename(path), "erros": [{"codigo": "CI000", "regra": "?", "mensagem": f"Erro ao ler arquivo: {error}"}], "avisos": [], "status": "BLOCK"}

    code = mask_php_comments(content)
    method_names = ("tratarLinkSemAssinatura", "processarControladorWebServices", "processarControladorAjax", "processarControladorAjaxExterno")
    if not any(extract_method(code, name)[0] is not None for name in method_names):
        return {"file": os.path.basename(path), "path": path, "erros": [{"codigo": "CI000", "regra": "?", "mensagem": "parser nao extraiu metodo controlador"}], "avisos": [], "status": "BLOCK"}

    errors = []
    warnings = []
    for validator in (validar_ci1, validar_ci2):
        result = validator(code)
        if result:
            errors.append(result)
    errors.extend(validar_ci3(code))
    errors.extend(validar_ci4(code))
    ci5 = validar_ci5(code)
    if ci5:
        warnings.append(ci5)
    status = "BLOCK" if errors else ("WARN" if warnings else "PASS")
    return {"file": os.path.basename(path), "path": path, "erros": errors, "avisos": warnings, "status": status}


def is_code_file(path):
    return os.path.basename(path).endswith("Integracao.php")


def run_audit(input_path, output_format="markdown", output_dir=None):
    file_results = []
    if os.path.isfile(input_path):
        if is_code_file(input_path):
            file_results.append(audit_file(input_path))
    elif os.path.isdir(input_path):
        for name in os.listdir(input_path):
            current = os.path.join(input_path, name)
            if os.path.isfile(current) and is_code_file(current):
                file_results.append(audit_file(current))
    elif "," in input_path:
        for raw_path in input_path.split(","):
            current = raw_path.strip()
            if os.path.isfile(current) and is_code_file(current):
                file_results.append(audit_file(current))
    if not file_results:
        file_results.append({
            "file": os.path.basename(input_path) or input_path,
            "erros": [{"codigo": "CI000", "regra": "?", "mensagem": "nenhum controlador de integracao elegivel analisado", "linha": None}],
            "avisos": [],
            "status": "BLOCK",
        })
    verdict = determinar_verdict(file_results)
    json_output = formatar_json(file_results, verdict)
    if output_dir and output_format == "json":
        os.makedirs(output_dir, exist_ok=True)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        module_name = os.path.basename(input_path).replace("/", "_")
        out_file = os.path.join(output_dir, f"controladores-integracao-check_{timestamp}_{module_name}.json")
        with open(out_file, "w", encoding="utf-8") as handle:
            json.dump(json_output, handle, ensure_ascii=False, indent=2)
        print(f"Evidencia salva em: {out_file}")
    if output_format == "json":
        return json_output, file_results, verdict
    return formatar_markdown(file_results, verdict), file_results, verdict


def main():
    parser = argparse.ArgumentParser(description="sei-verificacao-controladores: auditor de controladores de integracao")
    parser.add_argument("--input", required=True, help="Arquivo, diretorio, ou lista separada por virgula")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Formato de saida")
    parser.add_argument("--output", help="Diretorio para salvar evidencia JSON")
    parser.add_argument("--exit-code", action="store_true", help="Retorna exit code ao inves de imprimir output")
    args = parser.parse_args()

    output, file_results, verdict = run_audit(args.input, args.format, args.output)
    if args.format == "json" and not args.output:
        print(json.dumps(output, ensure_ascii=False, indent=2))
    elif not args.output:
        print(output)
    if args.exit_code:
        sys.exit({"PASS": 0, "WARN": 1, "BLOCK": 2}.get(verdict, 0))


if __name__ == "__main__":
    main()
