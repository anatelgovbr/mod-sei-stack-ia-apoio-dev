#!/usr/bin/env python3
import argparse
import re
import sys
from pathlib import Path


RE_DIC_SECTION = re.compile(r"^## (?!Índice de Tabelas$)(.+)$", re.MULTILINE)
RE_CHANGELOG_VERSION = re.compile(r"^## \[(.+)\]$", re.MULTILINE)
RE_CHANGELOG_ADDED = re.compile(r"^- \*\*Tabela `([^`]+)`\*\*$")
RE_CHANGELOG_TOP = re.compile(r"^- \*\*Tabela `([^`]+)`\*\*(.*)$")


def parse_dictionary(path):
    text = Path(path).read_text(encoding="utf-8")
    return set(m.group(1).strip() for m in RE_DIC_SECTION.finditer(text))


def parse_changelog(path):
    text = Path(path).read_text(encoding="utf-8")
    added = []
    removed = []
    current_category = None
    for line in text.splitlines():
        if line.startswith("### "):
            current_category = line[4:].strip()
            continue
        m = RE_CHANGELOG_TOP.match(line)
        if not m:
            continue
        table = m.group(1)
        if current_category == "Adicionado":
            added.append(table)
        elif current_category == "Excluído" and line.rstrip().endswith("**"):
            removed.append(table)
    return added, removed


def main():
    parser = argparse.ArgumentParser(description="Verifica consistência básica entre dicionario.md e CHANGELOG.md")
    parser.add_argument("diretorios", nargs="+", help="diretórios de módulos em docs/dicionario_dados")
    args = parser.parse_args()

    problems = 0
    for directory in args.diretorios:
        base = Path(directory)
        dic = base / "dicionario.md"
        changelog = base / "CHANGELOG.md"
        if not dic.exists() or not changelog.exists():
            continue
        dic_tables = parse_dictionary(dic)
        added, removed = parse_changelog(changelog)

        last_state = {}
        for table in added:
            last_state[table] = "added"
        for table in removed:
            last_state[table] = "removed"

        impossible_removed = sorted(
            table for table, state in last_state.items()
            if state == "removed" and table in dic_tables
        )
        impossible_added = sorted(
            table for table, state in last_state.items()
            if state == "added" and table not in dic_tables and not table.startswith("seq_")
        )

        if impossible_removed:
            problems += len(impossible_removed)
            print(f"{base}: tabelas marcadas como excluídas ainda presentes no dicionário:")
            for table in impossible_removed:
                print(f"  - {table}")

        if impossible_added:
            problems += len(impossible_added)
            print(f"{base}: tabelas marcadas como adicionadas ausentes do dicionário final:")
            for table in impossible_added:
                print(f"  - {table}")

    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
