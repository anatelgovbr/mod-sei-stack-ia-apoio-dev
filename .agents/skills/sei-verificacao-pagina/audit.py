#!/usr/bin/env python3
"""
sei-verificacao-pagina
Valida controles de pagina SEI: validarLink, validarPermissao, assinarLink,
compatibilidade de encoding e guardrails locais de pagina.
Com --exit-code: 0=PASS, 1=WARN, 2=BLOCK
"""

import argparse
from datetime import datetime, timezone
import json
import os
import re
import sys

VERSION = "1.0.0"
SKILL_NAME = "sei-verificacao-pagina"

RE_VALIDAR_LINK = re.compile(r"SessaoSEI\s*::\s*getInstance\s*\(\s*\)\s*->\s*validarLink\s*\(", re.DOTALL)
RE_VALIDAR_PERMISSAO = re.compile(r"SessaoSEI\s*::\s*getInstance\s*\(\s*\)\s*->\s*validarPermissao\s*\(", re.DOTALL)
RE_ASSINAR_LINK = re.compile(r"SessaoSEI\s*::\s*getInstance\s*\(\s*\)\s*->\s*assinarLink\s*\(", re.DOTALL)
RE_VERIFICAR_PERMISSAO = re.compile(r"SessaoSEI\s*::\s*getInstance\s*\(\s*\)\s*->\s*verificarPermissao\s*\(", re.DOTALL)
RE_REQUEST = re.compile(r"\$_REQUEST\s*\[", re.DOTALL)
RE_GET_POST_DIRECT = re.compile(r"\$_(GET|POST)\s*\[\s*['\"](?!acao['\"])\w+['\"]\s*\]", re.DOTALL)
RE_HREF_ACTION = re.compile(r"href\s*=\s*['\"][^'\"]*\?acao=", re.DOTALL | re.IGNORECASE)
RE_JS_ACTION = re.compile(r"(?:location\.href|window\.location|form\.action)\s*=\s*['\"][^'\"]*\?acao=", re.DOTALL | re.IGNORECASE)
RE_ECHO_PRINT = re.compile(r"\b(echo|print)\b", re.DOTALL)
RE_TRATAR_HTML = re.compile(r"PaginaSEI\s*::\s*tratarHTML\s*\(|tratarHTML\s*\(", re.DOTALL)
RE_INNER_HTML = re.compile(r"innerHTML\s*=|document\.write", re.DOTALL | re.IGNORECASE)
RE_WRITE_GET = re.compile(r"(cadastrar|alterar|excluir|desativar|remover|bloquear|atualizar|reativar)", re.IGNORECASE)
RE_INNER_HTML_ALVO = re.compile(r"(?:innerHTML\s*=|document\.write\s*\()\s*([A-Za-z_$][\w$.]*)", re.IGNORECASE)
RE_FONTE_CONFIRMADA = re.compile(r"response(?:Text|JSON|XML)?\b|\$_(?:GET|POST|REQUEST)\b|PaginaSEI\s*::\s*(?:GET|POST)\s*\(|<\?=|<\?php\s+echo", re.IGNORECASE)
RE_ECHO_VAR = re.compile(r"\b(?:echo|print)\b[^;\n]*?(\$\w+)", re.IGNORECASE)


def build_issue(code, rule, message, content, match=None):
    line = None
    if match is not None:
        line = content[:match.start()].count("\n") + 1
    return {"codigo": code, "regra": rule, "mensagem": message, "linha": line}


def validar_p1(content):
    match = RE_VALIDAR_LINK.search(content)
    if match:
        return None
    return build_issue("P001", "P1", "validarLink() ausente na entrada da pagina", content)


def validar_p2(content):
    match = RE_VALIDAR_PERMISSAO.search(content)
    if match:
        return None
    return build_issue("P002", "P2", "validarPermissao() ausente na entrada da pagina", content)


def validar_p3(path):
    try:
        raw = open(path, "rb").read()
    except Exception:
        return None
    if raw.startswith(b"\xef\xbb\xbf"):
        return {"codigo": "P003", "regra": "P3", "mensagem": "arquivo com BOM UTF-8", "linha": None}
    try:
        text = raw.decode("utf-8")
    except UnicodeDecodeError:
        return None
    for chunk in (text[i:i + 1024] for i in range(0, len(text), 1024)):
        try:
            chunk.encode("iso-8859-1")
        except UnicodeEncodeError:
            return {"codigo": "P003", "regra": "P3", "mensagem": "arquivo contem caracteres nao convertiveis para Latin-1", "linha": None}
    return None


def validar_p4(content):
    match = RE_HREF_ACTION.search(content) or RE_JS_ACTION.search(content)
    if match:
        snippet = content[max(0, match.start() - 120):match.end() + 120]
        if "assinarLink" not in snippet:
            return build_issue("P004", "P4", "acao exposta sem assinarLink()", content, match)
    return None


def validar_p5(content):
    match = RE_REQUEST.search(content)
    if match:
        return build_issue("P005", "P5", "$_REQUEST usado em pagina", content, match)
    return None


def validar_p6(content):
    match = RE_GET_POST_DIRECT.search(content)
    if match:
        return build_issue("P006", "P6", "$_GET/$_POST direto sem normalizacao explicita", content, match)
    return None


def validar_p7(content):
    has_ui = any(token in content for token in ["href=", "<button", "infraButton", "botaoSEI"])
    if has_ui and not RE_VERIFICAR_PERMISSAO.search(content):
        return build_issue("P007", "P7", "UI de acao sem verificarPermissao() condicional", content)
    return None


def validar_p8(content):
    """Devolve (issue, severidade) ou None.

    Segue a variavel ate a atribuicao que a originou. Origem ja tratada por
    tratarHTML() nao gera achado; origem em entrada HTTP e erro; origem
    desconhecida fica em aviso, para nao bloquear em cima de heuristica.
    """
    if not RE_ECHO_PRINT.search(content):
        return None
    linhas = content.split("\n")
    for index, line in enumerate(linhas, start=1):
        alvo = RE_ECHO_VAR.search(line)
        if not alvo:
            continue
        if RE_TRATAR_HTML.search(line):
            continue
        variavel = alvo.group(1)
        origem = None
        atribuicao = re.compile(r"^\s*" + re.escape(variavel) + r"\s*=\s*(.+?);", re.MULTILINE)
        for anterior in atribuicao.finditer("\n".join(linhas[:index - 1])):
            origem = anterior.group(1)
        if origem is not None and RE_TRATAR_HTML.search(origem):
            continue
        confirmada = origem is not None and RE_FONTE_CONFIRMADA.search(origem)
        if origem is None:
            confirmada = any(token in line for token in ("$_GET", "$_POST", "$str", "getStr"))
        if confirmada:
            return {"codigo": "P008", "regra": "P8", "mensagem": "saida HTML com entrada HTTP sem tratarHTML()", "linha": index}, "erro"
        return {"codigo": "P008", "regra": "P8", "mensagem": "saida HTML com variavel de origem nao confirmada", "linha": index}, "aviso"
    return None


def validar_p9(content):
    """Devolve (issue, severidade) ou None.

    Fluxo confirmado (a origem que alcanca o sink e resposta de requisicao ou
    entrada HTTP) e erro. Variavel de origem desconhecida fica em aviso, para
    o auditor nao bloquear em cima de heuristica.
    """
    match = RE_INNER_HTML.search(content)
    if not match:
        return None
    alvo = RE_INNER_HTML_ALVO.search(content, match.start())
    origem = alvo.group(1) if alvo else ""
    confirmado = bool(RE_FONTE_CONFIRMADA.search(origem))
    if not confirmado and origem:
        atribuicao = re.compile(r"\b" + re.escape(origem) + r"\s*=\s*([^;\n]+)")
        for anterior in atribuicao.finditer(content[:match.start()]):
            if RE_FONTE_CONFIRMADA.search(anterior.group(1)):
                confirmado = True
                break
    if confirmado:
        return build_issue("P009", "P9", "innerHTML/document.write recebe resposta ou entrada HTTP sem tratamento", content, match), "erro"
    return build_issue("P009", "P9", "innerHTML/document.write com variavel de origem nao confirmada", content, match), "aviso"


def validar_p10(content):
    match = RE_HREF_ACTION.search(content) or RE_JS_ACTION.search(content)
    if not match:
        return None
    snippet = content[match.start():match.end() + 120]
    if RE_WRITE_GET.search(snippet):
        return build_issue("P010", "P10", "mutacao de estado por GET/JS exige revisao", content, match)
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
    if not file_results:
        return "BLOCK"
    if any(result.get("erros") for result in file_results):
        return "BLOCK"
    if any(result.get("avisos") for result in file_results):
        return "WARN"
    return "PASS"


def audit_file(path, pagina_nova=False):
    try:
        content = open(path, "r", encoding="utf-8", errors="replace").read()
    except Exception as error:
        return {"file": os.path.basename(path), "erros": [{"codigo": "P000", "regra": "?", "mensagem": f"Erro ao ler arquivo: {error}"}], "avisos": [], "status": "BLOCK"}

    errors = []
    warnings = []

    for validator in (validar_p1, validar_p2, validar_p4):
        result = validator(content)
        if result:
            errors.append(result)

    p3 = validar_p3(path)
    if p3:
        errors.append(p3)

    for validator in (validar_p5, validar_p10):
        result = validator(content)
        if result:
            errors.append(result)

    # P6 e P8: erro em pagina nova, aviso em pagina preexistente.
    contextual = errors if pagina_nova else warnings

    result = validar_p6(content)
    if result:
        contextual.append(result)

    result = validar_p7(content)
    if result:
        warnings.append(result)

    p8 = validar_p8(content)
    if p8:
        contextual.append(p8[0])

    p9 = validar_p9(content)
    if p9:
        issue, severidade = p9
        (errors if severidade == "erro" else warnings).append(issue)

    status = "BLOCK" if errors else ("WARN" if warnings else "PASS")
    return {"file": os.path.basename(path), "path": path, "erros": errors, "avisos": warnings, "status": status}


def is_page_file(path):
    name = os.path.basename(path)
    if name.endswith("_css.php") or name.endswith("_js.php"):
        return False
    return name.endswith(".php") and ("_lista" in name or "_cadastro" in name or name in ["controlador.php", "index.php"])


def run_audit(input_path, output_format="markdown", pagina_nova=False):
    file_results = []
    if os.path.isfile(input_path):
        file_results.append(audit_file(input_path, pagina_nova))
    elif os.path.isdir(input_path):
        for name in os.listdir(input_path):
            current = os.path.join(input_path, name)
            if os.path.isfile(current) and is_page_file(current):
                file_results.append(audit_file(current, pagina_nova))
    elif "," in input_path:
        for raw_path in input_path.split(","):
            current = raw_path.strip()
            if os.path.exists(current):
                file_results.append(audit_file(current, pagina_nova))
    elif os.path.exists(input_path):
        file_results.append(audit_file(input_path, pagina_nova))
    verdict = determinar_verdict(file_results)
    if output_format == "json":
        return formatar_json(file_results, verdict), file_results, verdict
    return formatar_markdown(file_results, verdict), file_results, verdict


def main():
    parser = argparse.ArgumentParser(description="sei-verificacao-pagina: auditor de pagina SEI")
    parser.add_argument("--input", required=True, help="Arquivo, diretorio, ou lista separada por virgula")
    parser.add_argument("--format", choices=["json", "markdown"], default="markdown", help="Formato de saida")
    parser.add_argument("--exit-code", action="store_true", help="Retorna exit code ao inves de imprimir output")
    parser.add_argument(
        "--pagina",
        choices=["nova", "existente"],
        default="existente",
        help="Contexto da acao: 'nova' quando a pagina esta sendo criada nesta mudanca (P6 e P8 bloqueiam), "
             "'existente' quando ja existia e esta sendo alterada (P6 e P8 avisam). Padrao: existente",
    )
    args = parser.parse_args()

    output, file_results, verdict = run_audit(args.input, args.format, args.pagina == "nova")

    if args.format == "json":
        print(json.dumps(output, ensure_ascii=False, indent=2))
    else:
        print(output)

    if args.exit_code:
        sys.exit({"PASS": 0, "WARN": 1, "BLOCK": 2}.get(verdict, 0))


if __name__ == "__main__":
    main()
