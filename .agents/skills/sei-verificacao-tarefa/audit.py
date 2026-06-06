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

RE_TAREFA_ID = re.compile(
    r"['\"]?(\d+)['\"]?\s*=>\s*(?:array\s*\(|['\"]|)",
    re.DOTALL
)
RE_TAREFA_ARRAY = re.compile(r"(\d+)\s*=>\s*array\s*\((.*?)\)\s*,?", re.DOTALL)
RE_NOME_TAREFA = re.compile(r"['\"]([A-Z0-9_]{5,50})['\"]")
RE_DESCRICAO = re.compile(r"['\"]descricao['\"]\s*=>\s*['\"]([^'\"]+)['\"]")
RE_ID_TAREFA_MODULO = re.compile(r"['\"]id_tarefa_modulo['\"]\s*=>\s*['\"]?(\d+)")


# ═══════════════════════════════════════════════════════════════
# VALIDATORS
# ═══════════════════════════════════════════════════════════════

def parse_tarefas(content):
    tarefas = []

    id_nome_pairs = re.findall(r"(\d+)\s*=>\s*['\"]([A-Z0-9_]{5,50})['\"]", content)

    for match_id, match_nome in id_nome_pairs:
        tid = int(match_id)
        tarefas.append({
            "id": tid,
            "nome": match_nome,
            "descr": None
        })

    for match in RE_TAREFA_ARRAY.finditer(content):
        arr_id = int(match.group(1))
        bloco = match.group(2)
        task_id_match = RE_ID_TAREFA_MODULO.search(bloco)
        if not task_id_match:
            continue
        task_id_val = int(task_id_match.group(1))
        desc_match = RE_DESCRICAO.search(bloco)

        desc = desc_match.group(1) if desc_match else None
        existing = next((t for t in tarefas if t["id"] == task_id_val), None)
        if existing:
            if desc and not existing.get("descr"):
                existing["descr"] = desc
            continue

        tarefas.append({
            "id": task_id_val,
            "nome": f"TAREFA_{arr_id}",
            "descr": desc
        })

    return tarefas


def validar_k1_range(tarefas):
    errors = []
    for t in tarefas:
        if t["id"] < 1000 and t["id"] != 65:
            errors.append({
                "codigo": "K001",
                "regra": "K1",
                "id": t["id"],
                "nome": t["nome"],
                "mensagem": f"ID {t['id']} < 1000 — reservado para SEI core (use >= 1000 ou ID=65)"
            })
        elif t["id"] == 65 and not (t.get("descr") and t["descr"].strip()):
            errors.append({
                "codigo": "K007",
                "regra": "K7",
                "id": 65,
                "nome": t["nome"],
                "mensagem": "ID=65 usado sem atributo DESCRICAO — tarefa free-text deve ter descricao"
            })
    return errors


def validar_k3_prefixo(tarefas):
    errors = []
    for t in tarefas:
        nome = t["nome"]
        if not re.match(r'^MD_[A-Z0-9]+_[A-Z0-9_]+$', nome):
            errors.append({
                "codigo": "K003",
                "regra": "K3",
                "id": t["id"],
                "nome": nome,
                "mensagem": f"Nome '{nome}' nao segue padrao MD_<INST>_<NOME> em maiusculas"
            })
    return errors


def validar_k4_tamanho(tarefas):
    errors = []
    for t in tarefas:
        if len(t["nome"]) > 50:
            errors.append({
                "codigo": "K004",
                "regra": "K4",
                "id": t["id"],
                "nome": t["nome"],
                "mensagem": f"Nome '{t['nome']}' excede 50 caracteres ({len(t['nome'])})"
            })
    return errors


def validar_k6_duplicidade(tarefas):
    warnings = []
    seen_ids = {}
    for t in tarefas:
        if t["id"] in seen_ids:
            warnings.append({
                "codigo": "K006",
                "regra": "K6",
                "id": t["id"],
                "nome": t["nome"],
                "mensagem": f"ID {t['id']} duplicado no modulo"
            })
        seen_ids[t["id"]] = t["nome"]
    return warnings


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
            lines.append(f"  ✗ {e['file']}: {e['codigo']} — {e['mensagem']}")
        lines.append(sep)

    for r in file_results:
        fname = r["file"]
        tarefas = r.get("tarefas", [])
        errors = r.get("erros", [])
        warnings = r.get("avisos", [])

        if errors:
            lines.append(f"\n✗ {fname}")
            for e in errors:
                lines.append(f"   ✗ {e['codigo']} — ID {e.get('id', '?')}: {e['mensagem']}")
        if warnings:
            lines.append(f"\n⚠ {fname}")
            for w in warnings:
                lines.append(f"   ⚠ {w['codigo']} — ID {w.get('id', '?')}: {w['mensagem']}")
        if tarefas and not errors and not warnings:
            lines.append(f"\n✓ {fname} ({len(tarefas)} tarefas — conformidade total)")
        if not tarefas and not errors:
            lines.append(f"\n⚠ {fname} — nenhuma tarefa encontrada")

        lines.append(sep)

    total_erros = sum(len(r.get("erros", [])) for r in file_results)
    total_warns = sum(len(r.get("avisos", [])) for r in file_results)
    verdict_label = {"PASS": "PASS", "WARN": "WARN — avisos presentes", "BLOCK": "BLOCK — corrija erros"}

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

    tarefas = parse_tarefas(content)

    if not tarefas:
        return {"file": os.path.basename(path), "path": path, "tarefas": [], "erros": [], "avisos": [], "status": "PASS"}

    errors.extend(validar_k1_range(tarefas))
    errors.extend(validar_k3_prefixo(tarefas))
    errors.extend(validar_k4_tamanho(tarefas))
    warnings.extend(validar_k6_duplicidade(tarefas))

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
    return 'tarefa' in name.lower() and name.endswith('.php')


def run_audit(input_path, output_format='markdown', mode='adhoc'):
    file_results = []

    if os.path.isfile(input_path):
        if is_tarefa_file(input_path) or input_path.endswith('.php'):
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
