#!/usr/bin/env python3
"""
sei-verificacao-tarefa
Skill de gate para validar IDs de tarefa de modulo SEI/SIP.
Valida: range >= 1000, prefixo MD_, max 50 chars, unicidade.
Com --exit-code: 0=PASS, 1=WARN, 2=BLOCK
"""

import sys
import os
import re
import json
import argparse
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
            errors.append({
                "codigo": "K003", "regra": "K3", "id": t["id"], "nome": None,
                "mensagem": "registro sem id_tarefa_modulo", "linha": t.get("linha"),
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
        with open(path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
    except Exception as e:
        return {"file": os.path.basename(path), "tarefas": [], "erros": [{"codigo": "K000", "regra": "?", "mensagem": f"Erro ao ler: {e}"}], "avisos": [], "status": "BLOCK"}

    tarefas = parse_tarefas(mask_php_comments(content))
    for tarefa in tarefas:
        tarefa["file"] = os.path.basename(path)

    if not tarefas:
        return {"file": os.path.basename(path), "path": path, "tarefas": [], "erros": [{"codigo": "K000", "regra": "?", "mensagem": "parser nao extraiu definicao de tarefa"}], "avisos": [], "status": "BLOCK"}

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


def is_tarefa_file(path):
    name = os.path.basename(path)
    return 'tarefa' in name.lower() and (name.endswith('.php') or name.endswith('.php.example'))


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
    parser.add_argument("--input", required=True, help="Arquivo *_tarefa.php, diretorio scripts/, ou lista separada por virgula")
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
