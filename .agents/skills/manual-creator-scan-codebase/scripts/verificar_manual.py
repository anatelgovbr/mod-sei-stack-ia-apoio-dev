#!/usr/bin/env python3
"""Verifica, sem escrita, o perfil documentado em references/formato-manual.md."""

import argparse
import html
import re
import sys
import unicodedata
from pathlib import Path
from urllib.parse import unquote, urlsplit


SLUG = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
HEADING = re.compile(r"^(#{1,6}) (.+?)\s*$")
IMAGE = re.compile(r"!\[([^\[\]\n]*)\]\(([^()\s]+)\)")
LINK = re.compile(r"(?<!!)\[([^\[\]\n]+)\]\(([^()\s]+)\)")
LOGO = re.compile(r"\A\s*!\[([^\[\]\n]*)\]\(([^()\s]+)\)[ \t]*(?=\r?\n|\Z)")
NOTICE_MARKER = "[NECESSÁRIO INSERIR IMAGEM DE PRINT DA TELA DESTA FUNCIONALIDADE]"
NOTICE = re.compile(
    r"> \*\*"
    + re.escape(NOTICE_MARKER)
    + r"\*\* - \*\*caminho no sistema\*\*: (?P<path>[^\n]*)"
)
EXTENSIONS = {".png", ".jpg", ".jpeg", ".svg", ".webp", ".gif"}
MAX_BYTES = 4 * 1024 * 1024


class EntradaInvalida(ValueError):
    pass


def ocultar(text):
    """Mantém posições e linhas para diagnósticos sem conteúdo de código/comentário."""
    text = re.sub(r"<!--[\s\S]*?-->", lambda m: re.sub(r"[^\n]", " ", m[0]), text)
    lines = text.splitlines(keepends=True)
    fence = None
    for index, line in enumerate(lines):
        marker = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if fence:
            lines[index] = re.sub(r"[^\n]", " ", line)
            if marker and marker[1][0] == fence[0] and len(marker[1]) >= len(fence) and not marker[2].strip():
                fence = None
        elif marker:
            fence = marker[1]
            lines[index] = re.sub(r"[^\n]", " ", line)
    return "".join(lines), fence is not None


def ancora_github(title):
    return "".join(
        c for c in title.lower()
        if unicodedata.category(c)[0] in "LN" or c in " _-"
    ).replace(" ", "-")


def verificar(raiz_repo, manual, pasta_imagens=None):
    root = Path(raiz_repo).resolve(strict=True)
    if not root.is_dir():
        raise EntradaInvalida("A raiz do repositório deve ser uma pasta existente.")
    supplied = Path(manual)
    path = (supplied if supplied.is_absolute() else root / supplied).resolve(strict=True)
    if not path.is_relative_to(root) or not path.is_file():
        raise EntradaInvalida("O manual deve ser um arquivo dentro da raiz informada.")
    if path.suffix != ".md" or not SLUG.fullmatch(path.stem):
        raise EntradaInvalida("Use nome de manual em slug, com extensão .md.")
    nome_pasta = pasta_imagens or "imagens-" + path.stem
    if not re.fullmatch(r"[A-Za-z0-9_-][A-Za-z0-9_.-]*", nome_pasta):
        raise EntradaInvalida("A pasta de imagens deve ser um nome simples, ao lado do manual.")
    folder = path.parent / nome_pasta
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise EntradaInvalida("O manual excede o limite de leitura de 4 MiB.")
    try:
        original = data.decode("utf-8-sig")
    except UnicodeDecodeError as exc:
        raise EntradaInvalida("O manual deve estar em UTF-8.") from exc
    issues = []

    def report(code, line, message):
        issues.append((code, line, message))

    decoded = html.unescape(unquote(original))
    compact = re.sub(r"\s+", "", decoded)
    image_payload = re.search(
        r"(?:iVBORw0KGgo|/9j/|R0lGOD|UklGR|Qk[A-Za-z0-9+/]|PHN2Zy|PD94bW)[A-Za-z0-9+/=]{16,}", compact
    )
    # O tipo MIME registrado evita confundir "Data: 06/10/2026" com URI data.
    embedded = re.search(
        r"(?<!\w)data\s*:\s*(?:(?:image|application|text|audio|video|font|model|multipart|message)/[a-z0-9.+-]+|[,;])"
        r"|;\s*base64|base64\s*,", decoded, re.IGNORECASE
    )
    long_line = re.search(r"(?m)^[ \t]*[A-Za-z0-9+/]{80,}={0,2}[ \t]*\r?$", original)
    if image_payload or embedded or long_line:
        line = decoded.count("\n", 0, embedded.start()) + 1 if embedded else original.count("\n", 0, long_line.start()) + 1 if long_line else 1
        report("M05", line, "Imagem embutida, URI data ou bloco base64 proibido.")
    text, unclosed = ocultar(original)
    if unclosed:
        report("M06", 1, "Bloco de código não encerrado; cobertura estrutural incompleta.")
    if folder.resolve() != folder:
        report("M05", 1, "A pasta de imagens não pode redirecionar para outro destino.")

    def check_image(alt, source, line):
        if not alt.strip():
            report("M05", line, "Imagem sem texto alternativo.")
        source = html.unescape(unquote(source))
        try:
            url = urlsplit(source)
        except ValueError:
            report("M05", line, "Referência de imagem inválida.")
            return
        if url.scheme or url.netloc or url.query or url.fragment or not re.fullmatch(r"[A-Za-z0-9_./-]+", source):
            report("M05", line, "Use um caminho relativo simples para arquivo local de imagem.")
            return
        parts = source.split("/")
        if parts[0] != folder.name or any(p in {"", ".", ".."} for p in parts):
            report("M05", line, "Imagem fora da subpasta própria do manual.")
            return
        target = (path.parent / source).resolve()
        if folder.resolve() != folder or not target.is_relative_to(folder):
            report("M05", line, "O caminho físico da imagem escapa da subpasta própria.")
        elif target.suffix.lower() not in EXTENSIONS or not target.is_file() or target.stat().st_size == 0:
            report("M05", line, "Imagem ausente, vazia ou com extensão fora do perfil.")

    logo = LOGO.match(text)
    if not logo:
        report("M04", 1, "Falta logo inicial como imagem Markdown antes do título.")
    else:
        check_image(logo[1], logo[2], original.count("\n", 0, logo.start(1)) + 1)
        text = re.sub(r"[^\n]", " ", text[:logo.end()]) + text[logo.end():]

    lines = text.splitlines()
    notices = []
    for index, line in enumerate(lines):
        candidate = unicodedata.normalize("NFD", html.unescape(line)).casefold()
        candidate = "".join(c for c in candidate if not unicodedata.combining(c))
        if "necessario inserir imagem de print" not in candidate:
            continue
        notice = NOTICE.fullmatch(line)
        if not notice:
            report("M06", index + 1, "Aviso de captura fora do parágrafo padronizado suportado.")
            continue
        navigation = html.unescape(notice["path"]).strip()
        if not navigation or re.fullmatch(r"<[^<>]*>", navigation):
            report("M06", index + 1, "Preencha o caminho do aviso ou declare a navegação não confirmada.")
        if index and lines[index - 1].strip() or index + 1 < len(lines) and lines[index + 1].strip():
            report("M06", index + 1, "Separe o aviso dos blocos vizinhos por linhas em branco.")
        report("M09", index + 1, "Captura de tela pendente; confira o plano e obtenha o print manualmente.")
        notices.append(index)
    for index, line in enumerate(lines):
        if index not in notices and re.search(r"\\\[.*\\\]", re.sub(r"`[^`]*`", "", line)):
            report("M06", index + 1, "Colchetes escapados viram fórmula em renderizadores com LaTeX; use colchetes sem barra ou &#91; e &#93;.")
    headings = []
    ids = set()
    for index, line in enumerate(lines):
        if not line.strip():
            continue
        match = HEADING.fullmatch(line)
        if not match and re.match(r"^ {0,3}#{1,6}(?:[ \t]+|$)", line):
            report("M06", index + 1, "Título ATX com recuo ou tabulação fora do perfil suportado.")
        if match:
            level, title = len(match[1]), match[2].strip()
            if any(c in title for c in "`*[]<>#"):
                report("M06", index + 1, "Título com formatação fora do perfil suportado.")
            identity = ancora_github(title)
            if identity in ids:
                report("M06", index + 1, "Âncora repetida; use títulos e âncoras únicos.")
            ids.add(identity)
            if headings and level > headings[-1][0] + 1:
                report("M04", index + 1, "Hierarquia de títulos com salto de nível.")
            if index and lines[index - 1].strip() or index + 1 < len(lines) and lines[index + 1].strip():
                report("M04", index + 1, "Separe o título dos blocos vizinhos por linhas em branco.")
            headings.append((level, title, identity, index))
        if re.match(r"^ {0,3}(?:=+|-+)\s*$", line) and index and lines[index - 1].strip():
            report("M06", index + 1, "Título Setext ou separador ambíguo fora do perfil suportado.")
    for index in notices:
        if len(headings) < 3 or index <= headings[2][3]:
            report("M06", index + 1, "O aviso deve ficar em uma seção de conteúdo, após o Sumário.")
    if len([h for h in headings if h[0] == 1]) != 1 or not headings or headings[0][0] != 1:
        report("M04", 1, "Use um único H1 como primeiro título.")
    if headings and any(line.strip() for line in lines[:headings[0][3]]):
        report("M04", 1, "O título deve seguir a logo, sem conteúdo anterior.")
    if len(headings) < 3 or headings[1][:2] != (2, "Sumário"):
        report("M06", 1, "Use Sumário como primeira seção H2, seguido do conteúdo.")
    else:
        start, end = headings[1][3] + 1, headings[2][3]
        entries = []
        for index in range(start, end):
            if not lines[index].strip():
                continue
            match = re.fullmatch(r"( *)- \[([^\[\]\n]+)\]\(#([^()\s]+)\)", lines[index])
            if not match:
                report("M06", index + 1, "Entrada de sumário fora do perfil suportado.")
            else:
                entries.append((len(match[1]), match[2], unquote(match[3])))
        expected = [((h[0] - 2) * 4, h[1], h[2]) for h in headings[2:]]
        if entries != expected:
            report("M06", start + 1, "O sumário deve cobrir todos os tópicos e subtópicos, na ordem e no nível corretos.")

    body = "\n".join(lines)
    for match in IMAGE.finditer(body):
        check_image(match[1], match[2], body.count("\n", 0, match.start()) + 1)
    remainder = IMAGE.sub("", body)
    if "![" in remainder:
        report("M06", 1, "Imagem por referência ou sintaxe não suportada; cobertura automática incompleta.")
    if re.search(r"<(?:/?[A-Za-z]|!|\?)", remainder):
        report("M06", 1, "HTML fora do perfil de Markdown puro, ou comentário não encerrado.")
    if re.search(r"\[[^\]\n]+\]:", remainder):
        report("M06", 1, "Link por referência fora do perfil; cobertura automática incompleta.")
    for match in LINK.finditer(body):
        if match[2].startswith("#") and unquote(match[2][1:]) not in ids:
            report("M06", body.count("\n", 0, match.start()) + 1, "Link interno sem âncora correspondente.")
    return issues


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manual", help="Manual no destino declarado pelo adaptador, relativo à raiz ou absoluto.")
    parser.add_argument("--raiz-repo", required=True, help="Raiz do repositório de uso.")
    parser.add_argument("--pasta-imagens", help="Pasta de imagens declarada pelo adaptador, ao lado do manual; padrão: imagens-<slug>.")
    args = parser.parse_args()
    try:
        issues = verificar(args.raiz_repo, args.manual, args.pasta_imagens)
    except (EntradaInvalida, OSError, ValueError):
        print("ENTRADA_INVALIDA: confira raiz, slug, pasta de imagens, UTF-8 e limite de 4 MiB.", file=sys.stderr)
        return 2
    for code, line, message in issues:
        print(f"{code}: linha {line}: {message}")
    state = "FAIL" if any(code != "M09" for code, _, _ in issues) else "PENDENTE" if issues else "PASS"
    print(f"{state}: perfil estrutural e avisos de captura do manual; {len(issues)} ocorrência(s).")
    return 1 if issues else 0


if __name__ == "__main__":
    sys.exit(main())
