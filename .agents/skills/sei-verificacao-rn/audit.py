#!/usr/bin/env python3
"""
sei-verificacao-rn
Valida nucleo robusto de RN SEI: inicializacao de banco, isolamento de BD por RN
e avisos contextuais de sufixo CRUD/controle manual.
Com --exit-code: 0=PASS, 1=WARN, 2=BLOCK
"""

import argparse
from datetime import datetime, timezone
import json
import os
import re
import sys

VERSION = "1.1.0"
SKILL_NAME = "sei-verificacao-rn"

CRUD_WRITE = ["cadastrar", "alterar", "excluir", "desativar", "reativar", "bloquear", "incluir", "remover"]
CRUD_READ = ["consultar", "listar", "contar"]
# Recurso auditado por operacao de leitura (AGENTS.md, "Permissao/auditoria RN, leitura"):
# consultar e bloquear compartilham _consultar; listar e contar compartilham _listar.
READ_RESOURCE_SUFFIX = {"consultar": "_consultar", "bloquear": "_consultar", "listar": "_listar", "contar": "_listar"}

RE_CLASS_EXTENDS = re.compile(r"class\s+\w+\s+extends\s+InfraRN")
RE_INIT_METHOD = re.compile(r"protected\s+function\s+inicializarObjInfraIBanco\s*\(\s*\)(\s*:\s*[\w\\]+)?\s*\{[^}]*return\s+BancoSEI\s*::\s*getInstance\s*\(\s*\)", re.DOTALL)
RE_METHOD_SUFFIX = re.compile(r"function\s+(\w+)(Controlado|Conectado)\s*\(")
RE_METHOD_DEF = re.compile(r"function\s+(\w+)\s*\(")
RE_FECHAR_CONEXAO = re.compile(r"fecharConexao\s*\(|commitTransacao\s*\(|confirmarTransacao\s*\(|cancelarTransacao\s*\(", re.DOTALL)
RE_THROW_INFRA = re.compile(r"throw\s+new\s+InfraException", re.DOTALL)
RE_OTHER_BD_CALL = re.compile(r"new\s+(\w+BD)\s*\(", re.DOTALL)
RE_VALIDA_AUDITAR = re.compile(r"validarAuditarPermissao\s*\(")
RE_VALIDA_PERMISSAO = re.compile(r"validarPermissao\s*\(")
RE_AUDIT_RESOURCE = re.compile(r"validarAuditarPermissao\s*\(\s*['\"]([^'\"]+)['\"]")
RE_EXTERNAL_EFFECT = re.compile(
    r"(?:\bmail\s*\(|new\s+(?:SoapClient|HttpClient|WebService\w*)\s*\(|\bcurl_\w+\s*\(|(?:->|::)\s*(?:notificar|enviar\w*|indexar\w*|reindexar\w*|publicar|integrar\w*|executarRequisicao|chamarWebService|consumirServico)\s*\()",
    re.IGNORECASE,
)
RE_HTTP_CLIENT_CALL = re.compile(
    r"\$(\w*(?:http|client|cliente|guzzle|requester)\w*)\s*->\s*(?:request|post|get|send)\s*\(",
    re.IGNORECASE,
)
RE_GUZZLE_CLIENT = re.compile(r"\$(\w+)\s*=\s*new\s+(?:\\)?GuzzleHttp\\Client\s*\(", re.IGNORECASE)
RE_INTEGRATION_CALL = re.compile(r"(?:\b[A-Z][A-Za-z0-9_\\]*Integracao\s*::|\$\w*Integracao\s*->)\s*(\w+)\s*\(")
RE_PURE_INTEGRATION_METHOD = re.compile(r"^(?:get|set|is|has|obter|validar|verificar|checar)\w*$", re.IGNORECASE)


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


def extract_method_body(content, opening_brace_pos):
    depth = 0
    i = opening_brace_pos
    while i < len(content):
        if content[i] == '{':
            depth += 1
        elif content[i] == '}':
            depth -= 1
            if depth == 0:
                return content[opening_brace_pos:i + 1]
        i += 1
    return content[opening_brace_pos:]


def iter_methods(content):
    for match in RE_METHOD_DEF.finditer(content):
        brace_pos = content.find('{', match.end())
        if brace_pos >= 0:
            yield match.group(1), extract_method_body(content, brace_pos), match


def build_issue(code, rule, message, content, match=None):
    line = None
    if match is not None:
        line = content[:match.start()].count("\n") + 1
    return {"codigo": code, "regra": rule, "mensagem": message, "linha": line}


def crud_operation(method_name, operations):
    lower = method_name.lower()
    return next((operation for operation in operations if lower.startswith(operation)), None)


def infer_module_prefix(content):
    match = re.search(r"class\s+(Md\w+RN)\s+extends\s+InfraRN", content)
    if not match:
        return None
    stem = match.group(1)[2:-2]
    sigla = re.match(r"[A-Z][a-z0-9]*", stem)
    return f"md_{sigla.group(0).lower()}_" if sigla else None


def find_external_effect(body):
    matches = list(RE_EXTERNAL_EFFECT.finditer(body))
    matches.extend(match for match in RE_HTTP_CLIENT_CALL.finditer(body) if not re.search(r"(?:DTO|RN|BD)$", match.group(1), re.IGNORECASE))
    for construction in RE_GUZZLE_CLIENT.finditer(body):
        call = re.search(
            rf"\${re.escape(construction.group(1))}\s*->\s*(?:request|post|get|send)\s*\(",
            body[construction.end():],
            re.IGNORECASE,
        )
        if call:
            matches.append(construction)
    matches.extend(match for match in RE_INTEGRATION_CALL.finditer(body) if not RE_PURE_INTEGRATION_METHOD.match(match.group(1)))
    return min(matches, key=lambda match: match.start()) if matches else None


def validar_t1(content):
    warnings = []
    for match in RE_METHOD_SUFFIX.finditer(content):
        method_name = match.group(1)
        found_suffix = match.group(2)
        lower = method_name.lower()
        expected = None
        if any(lower.startswith(prefix) for prefix in CRUD_WRITE):
            expected = "Controlado"
        elif any(lower.startswith(prefix) for prefix in CRUD_READ):
            expected = "Conectado"
        if expected and found_suffix != expected:
            warnings.append(build_issue("T001", "T1", f"Metodo CRUD {method_name} usa sufixo {found_suffix}; revisar expectativa {expected}", content, match))
    return warnings or None


def validar_t2(content):
    if not RE_CLASS_EXTENDS.search(content):
        return build_issue("T200", "T2", "classe nao extende InfraRN", content)
    if RE_INIT_METHOD.search(content):
        return None
    return build_issue("T002", "T2", "inicializarObjInfraIBanco() ausente ou sem BancoSEI::getInstance()", content)


def validar_t3(content):
    own_class_match = re.search(r"class\s+(\w+)RN\s+extends", content)
    own_class_name = own_class_match.group(1) if own_class_match else None
    errors = []
    for match in RE_OTHER_BD_CALL.finditer(content):
        bd_class = match.group(1)
        if own_class_name and bd_class.replace("BD", "") != own_class_name.replace("RN", ""):
            errors.append(build_issue("T003", "T3", f"RN chama BD de outra classe ({bd_class})", content, match))
    return errors or None


def validar_t4(content):
    match = RE_FECHAR_CONEXAO.search(content)
    if match:
        return build_issue("T004", "T4", "controle manual de conexao/transacao exige revisao contextual", content, match)
    return None


def validar_a1(content):
    """BLOCK: public CRUD writes implemented by Controlado require audited permission."""
    errors = []
    module_prefix = infer_module_prefix(content)
    for method_name, body, match in iter_methods(content):
        lower = method_name.lower()
        operation = crud_operation(method_name, CRUD_WRITE)
        if not lower.endswith("controlado") or operation is None:
            continue
        resources = RE_AUDIT_RESOURCE.findall(body)
        # bloquear nao tem recurso proprio no SIP: compartilha o de consultar (manual cap. 4)
        expected_suffix = READ_RESOURCE_SUFFIX.get(operation, f"_{operation}")
        compatible = any((not module_prefix or resource.startswith(module_prefix)) and resource.endswith(expected_suffix) for resource in resources)
        if not compatible:
            errors.append(build_issue(
                "A001", "A1",
                f"Metodo de escrita '{method_name}' deve auditar com recurso terminado em '{expected_suffix}' e nunca _listar",
                content, match
            ))
    return errors or None


def validar_a2(content):
    """WARN only public write-like wrappers; internal helpers do not require a user session."""
    warnings = []
    for method_name, body, match in iter_methods(content):
        lower = method_name.lower()
        if lower.endswith(("controlado", "interno", "conectado")) or not any(lower.startswith(kw) for kw in CRUD_WRITE):
            continue
        if not RE_VALIDA_AUDITAR.search(body) and not RE_VALIDA_PERMISSAO.search(body):
            warnings.append(build_issue(
                "A002", "A2",
                f"Metodo de escrita '{method_name}' sem verificacao de permissao/auditoria; confirmar se e helper interno",
                content, match
            ))
    return warnings or None


def validar_a3(content):
    """BLOCK: leitura publica audita o recurso da operacao: consultar e bloquear com _consultar; listar e contar com _listar."""
    errors = []
    module_prefix = infer_module_prefix(content)
    for method_name, body, match in iter_methods(content):
        lower = method_name.lower()
        if not lower.endswith("conectado"):
            continue
        operation = crud_operation(method_name, list(READ_RESOURCE_SUFFIX))
        if operation is None:
            continue
        expected_suffix = READ_RESOURCE_SUFFIX[operation]
        resources = RE_AUDIT_RESOURCE.findall(body)
        compatible = any((not module_prefix or resource.startswith(module_prefix)) and resource.endswith(expected_suffix) for resource in resources)
        if not compatible:
            errors.append(build_issue(
                "A003", "A3",
                f"Metodo de leitura '{method_name}' deve usar recurso terminado em '{expected_suffix}' coerente com a RN",
                content, match,
            ))
    return errors or None


def validar_t6(content):
    errors = []
    controlled_operations = {
        method_name[:-10].lower()
        for method_name, body, match in iter_methods(content)
        if method_name.lower().endswith("controlado")
    }
    for method_name, body, match in iter_methods(content):
        effect = find_external_effect(body)
        if not effect:
            continue
        if method_name.lower().endswith("controlado"):
            errors.append(build_issue(
                "T006", "T6",
                f"Metodo '{method_name}' executa efeito externo dentro da transacao",
                content, match,
            ))
            continue
        direct_controlled_calls = list(re.finditer(r"\$this\s*->\s*\w+Controlado\s*\(", body))
        if direct_controlled_calls:
            errors.append(build_issue(
                "T006", "T6",
                f"Wrapper '{method_name}' chama metodo *Controlado protegido diretamente antes de efeito externo",
                content, match,
            ))
            continue
        persistence_calls = [
            call
            for call in re.finditer(r"\$this\s*->\s*(\w+)\s*\(", body)
            if call.group(1).lower() in controlled_operations
        ]
        crud_pattern = "|".join(CRUD_WRITE + CRUD_READ)
        persistence_calls.extend(re.finditer(rf"\$\w*(?:RN|BD)\s*->\s*(?:{crud_pattern})\w*\s*\(", body, re.IGNORECASE))
        if persistence_calls:
            line_start = content.rfind("\n", 0, match.start()) + 1
            signature = content[line_start:match.start()]
            is_public = "protected" not in signature and "private" not in signature
            if not is_public or any(call.start() > effect.start() for call in persistence_calls):
                errors.append(build_issue(
                    "T006", "T6",
                    f"Wrapper '{method_name}' deve ser publico e concluir toda persistencia antes do primeiro efeito externo",
                    content, match,
                ))
    return errors or None


def validar_t5(content):
    if "try" in content and RE_THROW_INFRA.search(content):
        return None
    if RE_METHOD_SUFFIX.search(content):
        return build_issue("T005", "T5", "padrao try/catch com InfraException nao encontrado; revisar contexto", content)
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
        return {"file": os.path.basename(path), "erros": [{"codigo": "T000", "regra": "?", "mensagem": f"Erro ao ler arquivo: {error}"}], "avisos": [], "status": "BLOCK"}

    code = mask_php_comments(content)
    if not RE_CLASS_EXTENDS.search(code):
        return {"file": os.path.basename(path), "erros": [{"codigo": "T200", "regra": "?", "mensagem": "nao e uma classe RN (nao extende InfraRN)"}], "avisos": [], "status": "BLOCK"}

    errors = []
    warnings = []

    t2 = validar_t2(code)
    if t2:
        errors.append(t2)

    t3 = validar_t3(code)
    if t3:
        errors.extend(t3)

    a1 = validar_a1(code)
    if a1:
        errors.extend(a1)

    a3 = validar_a3(code)
    if a3:
        errors.extend(a3)

    t6 = validar_t6(code)
    if t6:
        errors.extend(t6)

    for validator in (validar_t1, validar_t4, validar_t5, validar_a2):
        result = validator(code)
        if not result:
            continue
        if isinstance(result, list):
            warnings.extend(result)
        else:
            warnings.append(result)

    status = "BLOCK" if errors else ("WARN" if warnings else "PASS")
    return {"file": os.path.basename(path), "path": path, "erros": errors, "avisos": warnings, "status": status}


def is_rn_file(path):
    return os.path.basename(path).endswith("RN.php")


def run_audit(input_path, output_format="markdown"):
    file_results = []
    if os.path.isfile(input_path):
        if is_rn_file(input_path):
            file_results.append(audit_file(input_path))
    elif os.path.isdir(input_path):
        for name in os.listdir(input_path):
            current = os.path.join(input_path, name)
            if os.path.isfile(current) and is_rn_file(current):
                file_results.append(audit_file(current))
    elif "," in input_path:
        for raw_path in input_path.split(","):
            current = raw_path.strip()
            if os.path.exists(current) and is_rn_file(current):
                file_results.append(audit_file(current))
    if not file_results:
        file_results.append({
            "file": os.path.basename(input_path) or input_path,
            "erros": [{"codigo": "T000", "regra": "?", "mensagem": "nenhuma classe RN elegivel analisada", "linha": None}],
            "avisos": [],
            "status": "BLOCK",
        })
    verdict = determinar_verdict(file_results)
    if output_format == "json":
        return formatar_json(file_results, verdict), file_results, verdict
    return formatar_markdown(file_results, verdict), file_results, verdict


def main():
    parser = argparse.ArgumentParser(description="sei-verificacao-rn: auditor de RN SEI")
    parser.add_argument("--input", required=True, help="Arquivo RN, diretorio rn/ ou lista separada por virgula")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Formato de saida")
    parser.add_argument("--exit-code", action="store_true", help="Retorna exit code ao inves de imprimir output")
    args = parser.parse_args()
    output, file_results, verdict = run_audit(args.input, args.format)
    if args.format == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(output)
    if args.exit_code:
        sys.exit({"PASS": 0, "WARN": 1, "BLOCK": 2}.get(verdict, 0))


if __name__ == "__main__":
    main()
