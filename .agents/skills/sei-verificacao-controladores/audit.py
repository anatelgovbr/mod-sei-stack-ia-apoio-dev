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

SENSITIVE_PATTERNS = [
    r'"senha"\s*:',
    r'"token"\s*:',
    r'"password"\s*:',
    r'"api_key"\s*:',
    r'"secret"\s*:',
    r'session_id',
]


def build_issue(code, rule, message, content, match=None):
    line = None
    if match is not None:
        line = content[:match.start()].count("\n") + 1
    return {"codigo": code, "regra": rule, "mensagem": message, "linha": line}


def validar_ci1(content):
    if not RE_TRATAR_LINK.search(content):
        return None
    if RE_PREG_MATCH.search(content):
        return None
    return build_issue("CI001", "CI1", "tratarLinkSemAssinatura sem preg_match restritivo", content)


def validar_ci2(content):
    if not RE_PROCESSAR_WS.search(content):
        return None
    if RE_SWITCH_SERVICO.search(content) and RE_CASE_LITERAL.search(content):
        return None
    return build_issue("CI002", "CI2", "processarControladorWebServices sem dispatch explicito por servico", content)


def validar_ci3(content):
    if not (RE_PROCESSAR_AJAX.search(content) or RE_PROCESSAR_AJAX_EXTERNO.search(content)):
        return None
    if RE_SWITCH_ACAO.search(content) and RE_CASE_LITERAL.search(content):
        return None
    return build_issue("CI003", "CI3", "processarControladorAjax/processarControladorAjaxExterno sem dispatch explicito por acao", content)


def validar_ci4(content):
    for pattern in SENSITIVE_PATTERNS:
        match = re.search(pattern, content, re.DOTALL)
        if match:
            return build_issue("CI004", "CI4", f"payload sensivel potencial em controlador: {match.group(0)}", content, match)
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
            lines.append(f"  ✗ {error['file']}: {error['codigo']} — {error['mensagem']}{suffix}")
        lines.append(sep)

    for result in file_results:
        errors = result.get("erros", [])
        warnings = result.get("avisos", [])
        if errors:
            lines.append(f"\n✗ {result['file']}")
            for error in errors:
                suffix = f" (linha {error['linha']})" if error.get("linha") else ""
                lines.append(f"   ✗ {error['codigo']} — {error['mensagem']}{suffix}")
        if warnings:
            lines.append(f"\n⚠ {result['file']}")
            for warning in warnings:
                suffix = f" (linha {warning['linha']})" if warning.get("linha") else ""
                lines.append(f"   ⚠ {warning['codigo']} — {warning['mensagem']}{suffix}")
        if not errors and not warnings:
            lines.append(f"\n✓ {result['file']} — conformidade total")
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

    errors = []
    warnings = []
    for validator in (validar_ci1, validar_ci2, validar_ci3):
        result = validator(content)
        if result:
            errors.append(result)
    ci4 = validar_ci4(content)
    if ci4:
        warnings.append(ci4)
    status = "BLOCK" if errors else ("WARN" if warnings else "PASS")
    return {"file": os.path.basename(path), "path": path, "erros": errors, "avisos": warnings, "status": status}


def is_code_file(path):
    return os.path.basename(path).endswith(".php")


def run_audit(input_path, output_format="markdown", output_dir=None):
    file_results = []
    if os.path.isfile(input_path):
        file_results.append(audit_file(input_path))
    elif os.path.isdir(input_path):
        for name in os.listdir(input_path):
            current = os.path.join(input_path, name)
            if os.path.isfile(current) and is_code_file(current):
                file_results.append(audit_file(current))
    elif "," in input_path:
        for raw_path in input_path.split(","):
            current = raw_path.strip()
            if os.path.exists(current):
                file_results.append(audit_file(current))
    elif os.path.exists(input_path):
        file_results.append(audit_file(input_path))
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
