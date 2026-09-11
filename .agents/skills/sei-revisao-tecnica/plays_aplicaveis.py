#!/usr/bin/env python3
"""Deriva do escopo a lista obrigatória de plays do owasp-playbook e de gates do SEI.

A seleção do que rodar não depende de leitura manual da ponte. Este script varre os
caminhos informados, procura os sinais declarados em
`.agents/security/mapa-seguranca-cwe-sei.md` e imprime a lista obrigatória.

Uso:
    python3 .agents/skills/sei-revisao-tecnica/plays_aplicaveis.py <caminho> [<caminho> ...]
    python3 .agents/skills/sei-revisao-tecnica/plays_aplicaveis.py --format json <caminho>

Regra de uso no relatório: a saída entra literalmente na seção de metodologia.
Play ou gate listado aqui que não for executado exige justificativa escrita ao lado.

Os `.php` do repositório são ISO-8859-1, entao a leitura decodifica em latin-1.
"""

import argparse
import json
import sys
from pathlib import Path

# Diretórios ignorados em todo play, conforme regra fixa 7 do SKILL.md.
# `upstream/` e `vendor/` só contam para sca-audit.
IGNORADOS = {".git", "node_modules", "__pycache__", ".venv", "_graficos", "_raster"}
IGNORADOS_SALVO_SCA = {"vendor", "upstream"}

SEMPRE = [
    ("code-review-security", "qualquer arquivo de código-fonte no escopo"),
    ("secrets-scan", "roda sempre, em qualquer escopo"),
]


def arquivos_do_escopo(caminhos):
    """Expande diretórios e devolve (todos, sem_dependencia)."""
    todos = []
    for bruto in caminhos:
        p = Path(bruto)
        if p.is_file():
            todos.append(p)
        elif p.is_dir():
            for f in sorted(p.rglob("*")):
                if f.is_file() and not (set(f.parts) & IGNORADOS):
                    todos.append(f)
        else:
            print(f"aviso: caminho inexistente, ignorado: {bruto}", file=sys.stderr)
    sem_dep = [f for f in todos if not (set(f.parts) & IGNORADOS_SALVO_SCA)]
    return todos, sem_dep


def ler(f):
    try:
        return f.read_bytes().decode("latin-1")
    except OSError:
        return ""


def e_fixture(f):
    """Fixture de skill não e código do produto.

    Arquivos sob `.agents/skills/<skill>/examples/` e `.../evals/` são material de
    teste, muitos vulneráveis de proposito. Não disparam play de aplicação nem gate
    do SEI. Continuam contando para `agent-security-audit`, que revisa a stack.
    """
    partes = f.parts
    if ".agents" not in partes or "skills" not in partes:
        return False
    return "examples" in partes or "evals" in partes


def detectar(todos, sem_dep):
    plays = {}
    gates = {}

    def marca(alvo, chave, evidencia):
        alvo.setdefault(chave, []).append(evidencia)

    for f in sem_dep:
        nome = f.name
        posix = f.as_posix()
        fixture = e_fixture(f)
        conteudo = None

        def corpo():
            nonlocal conteudo
            if conteudo is None:
                conteudo = ler(f)
            return conteudo

        # agent-security-audit e o único que enxerga fixture, porque revisa a stack
        if nome in ("AGENTS.md", "CLAUDE.md") or any(
            parte in (".agents", ".claude", ".claude-plugin", ".github")
            for parte in f.parts
        ):
            marca(plays, "agent-security-audit", posix)

        if fixture:
            continue

        # --- Sinais de play ---
        if nome.endswith("_lista.php") or nome.endswith("_cadastro.php"):
            marca(plays, "owasp-top10-web-review", f"{posix} e página de módulo web")
            marca(gates, "sei-verificacao-pagina", posix)

        if nome.endswith("Integracao.php"):
            if "processarControlador" in corpo():
                marca(plays, "owasp-top10-web-review", f"{posix} despacha ação web")
            for metodo in ("processarControladorAjaxExterno",
                           "processarControladorAjax",
                           "processarControladorWebServices"):
                if metodo in corpo():
                    marca(plays, "api-security-review", f"{posix} define {metodo}()")
                    break
            marca(gates, "sei-verificacao-controladores", posix)

        if nome.endswith("RN.php"):
            marca(gates, "sei-verificacao-rn", posix)
        if nome.endswith("BD.php") or nome.endswith("DTO.php"):
            marca(gates, "sei-verificacao-banco-dados", posix)
        if nome.endswith("_tarefa.php"):
            marca(gates, "sei-verificacao-tarefa", posix)

        if "/módulos/ia/" in posix or posix.startswith("módulos/ia/"):
            marca(plays, "llm-risk-assess", posix)
            marca(plays, "prompt-injection-testing (parte estatica)", posix)

        if nome == ".mcp.json" or (nome.endswith(".json") and "mcpServers" in corpo()):
            marca(plays, "mcp-server-review", posix)

        if nome in ("Dockerfile", "docker-compose.yml", "docker-compose.yaml") \
                or nome.endswith((".tf", ".tfvars")):
            marca(plays, "iac-security-review", posix)

        if nome in ("AndroidManifest.xml", "Info.plist", "pubspec.yaml"):
            marca(plays, "mobile-code-review", posix)

    # sca-audit olha tambem o que os demais plays ignoram
    vendorizados = set()
    for f in todos:
        if f.name in ("composer.json", "composer.lock", "package.json",
                      "package-lock.json", "requirements.txt", "go.mod",
                      "pom.xml", "Gemfile", "Cargo.toml"):
            marca(plays, "sca-audit", f.as_posix())
        elif "vendor" in f.parts:
            raiz = f.as_posix().split("/vendor/")[0]
            vendorizados.add(raiz)
    for raiz in sorted(vendorizados):
        marca(plays, "sca-audit", f"dependência vendorizada em {raiz}/vendor/")

    return plays, gates


COMANDO_GATE = {
    "sei-verificacao-pagina":
        "python3 .agents/skills/sei-verificacao-pagina/audit.py --input {alvo} --pagina existente --format markdown",
    "sei-verificacao-rn":
        "python3 .agents/skills/sei-verificacao-rn/audit.py --input {alvo} --format markdown",
    "sei-verificacao-controladores":
        "python3 .agents/skills/sei-verificacao-controladores/audit.py --input {alvo} --format markdown",
    "sei-verificacao-banco-dados":
        "python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input {alvo} --format markdown",
    "sei-verificacao-tarefa":
        "python3 .agents/skills/sei-verificacao-tarefa/audit.py --input {alvo} --format markdown",
}

TODOS_OS_PLAYS = [
    "code-review-security", "secrets-scan", "sca-audit", "api-security-review",
    "owasp-top10-web-review", "iac-security-review", "mobile-code-review",
    "agent-security-audit", "mcp-server-review", "llm-risk-assess",
    "prompt-injection-testing (parte estatica)", "agentic-ai-risk-assess",
    "multi-agentic-threat-model", "ai-security-verification",
    "securability-engineering-review",
]

RAIZ_REPO = Path(__file__).resolve().parents[3]
PLAYS_DIR = RAIZ_REPO / ".agents/skills/owasp-playbook/upstream/plugins"


def plays_instalados():
    """Nomes de play com arquivo presente no upstream.

    A copia do upstream pode ser parcial, e o próprio SKILL.md avisa que play sem
    arquivo não roda. Devolve None quando o diretório não existe, e nesse caso o
    relatório não afirma nada sobre instalação.
    """
    if not PLAYS_DIR.is_dir():
        return None
    return {f.stem for f in PLAYS_DIR.glob("*/plays/*.md")}


def relatorio_markdown(caminhos, plays, gates, total):
    L = []
    L.append("## Plays e gates aplicáveis ao escopo")
    L.append("")
    L.append(f"Escopo: {', '.join(caminhos)}")
    L.append(f"Arquivos analisados: {total}")
    L.append("")
    L.append("### Obrigatórios")
    L.append("")
    L.append("| Play | Motivo | Rodou? |")
    L.append("|---|---|---|")
    for nome, motivo in SEMPRE:
        L.append(f"| `{nome}` | {motivo} | |")
    for nome in sorted(plays):
        ev = plays[nome]
        amostra = ev[0] if len(ev) == 1 else f"{ev[0]} e mais {len(ev) - 1}"
        L.append(f"| `{nome}` | sinal em {amostra} | |")
    L.append("")
    L.append("### Gates do SEI a executar")
    L.append("")
    if gates:
        L.append("```bash")
        for nome in sorted(gates):
            for alvo in gates[nome]:
                L.append(COMANDO_GATE[nome].format(alvo=alvo))
        L.append("```")
    else:
        L.append("Nenhum artefato de gate no escopo.")
    L.append("")
    L.append("### Sem alvo no escopo, não rodam")
    L.append("")
    acionados = {n for n, _ in SEMPRE} | set(plays)
    ausentes = [p for p in TODOS_OS_PLAYS if p not in acionados]
    L.append(", ".join(f"`{p}`" for p in ausentes) if ausentes else "Nenhum.")
    instalados = plays_instalados()
    if instalados is not None:
        nao_instalados = [p for p in TODOS_OS_PLAYS
                          if p.split(" ")[0] not in instalados]
        if nao_instalados:
            L.append("")
            L.append("Sem arquivo no `upstream/` instalado, não rodam em hipótese "
                     "nenhuma: " + ", ".join(f"`{p}`" for p in nao_instalados))
    L.append("")
    L.append("Play ou gate listado como obrigatório que não for executado exige "
             "justificativa escrita no relatório, ao lado da linha.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(
        description="Lista os plays do owasp-playbook e os gates do SEI aplicáveis a um escopo")
    ap.add_argument("caminhos", nargs="+", help="arquivos ou diretórios do escopo")
    ap.add_argument("--format", choices=["markdown", "json"], default="markdown")
    args = ap.parse_args()

    todos, sem_dep = arquivos_do_escopo(args.caminhos)
    if not todos:
        print("Escopo vazio: nenhum arquivo encontrado.", file=sys.stderr)
        return 1

    plays, gates = detectar(todos, sem_dep)

    if args.format == "json":
        print(json.dumps({
            "escopo": args.caminhos,
            "arquivos": len(todos),
            "plays_sempre": [n for n, _ in SEMPRE],
            "plays_por_sinal": {k: v for k, v in sorted(plays.items())},
            "gates": {k: v for k, v in sorted(gates.items())},
        }, ensure_ascii=False, indent=2))
    else:
        print(relatorio_markdown(args.caminhos, plays, gates, len(todos)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
