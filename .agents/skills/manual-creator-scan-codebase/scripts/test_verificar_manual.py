"""Casos de aceitação e rejeição do contrato de publicação dos manuais."""

import contextlib
import hashlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from verificar_manual import EntradaInvalida, main, verificar


VALID = '''![Logo de teste](imagens-manual-teste/logo.svg)

# Manual de teste

## Sumário

- [Como registrar](#como-registrar)
    - [Campos e opções](#campos-e-opções)
- [Como consultar](#como-consultar)

## Como registrar

1. Informe o assunto.
2. Selecione **Salvar**.

### Campos e opções

Informe até 200 caracteres.

![Campo Assunto](imagens-manual-teste/campo.svg)

## Como consultar

Selecione **Consultar**.
'''

NOTICE = '> **[NECESSÁRIO INSERIR IMAGEM DE PRINT DA TELA DESTA FUNCIONALIDADE]** - **caminho no sistema**: Solicitações > Registrar solicitação'


class TestManual(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name).resolve()
        self.directory = self.root / "docs" / "manuais"
        self.images = self.directory / "imagens-manual-teste"
        self.images.mkdir(parents=True)
        for name in ("logo.svg", "campo.svg"):
            (self.images / name).write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>', encoding="utf-8")
        self.manual = self.directory / "manual-teste.md"

    def run_check(self, content=VALID):
        self.manual.write_text(content, encoding="utf-8")
        def hashes():
            return {str(p.relative_to(self.root)): hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in self.root.rglob("*") if p.is_file()}
        before = hashes()
        issues = verificar(self.root, self.manual)
        self.assertEqual(before, hashes())
        return issues

    def test_manual_completo_acentos_e_subtopicos(self):
        self.assertEqual(self.run_check(), [])
        self.assertEqual(verificar(self.root, "docs/manuais/manual-teste.md"), [])

    def test_manual_com_lf_e_crlf_sem_escrita(self):
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                content = VALID.replace("\n", newline).encode("utf-8")
                self.manual.write_bytes(content)
                self.assertEqual(verificar(self.root, self.manual), [])
                self.assertEqual(self.manual.read_bytes(), content)

    def test_base64_em_lf_e_crlf_sem_escrita(self):
        for newline in ("\n", "\r\n"):
            with self.subTest(newline=repr(newline)):
                content = (VALID + "\n" + "A" * 120 + "\n").replace("\n", newline).encode("utf-8")
                self.manual.write_bytes(content)
                before = hashlib.sha256(content).hexdigest()
                self.assertTrue(any(i[0] == "M05" for i in verificar(self.root, self.manual)))
                self.assertEqual(hashlib.sha256(self.manual.read_bytes()).hexdigest(), before)

    def montar_em_pasta_de_modulo(self, content):
        directory = self.root / "docs" / "manuais" / "modulo-teste"
        (directory / "imagens").mkdir(parents=True)
        for name in ("logo.svg", "campo.svg"):
            (directory / "imagens" / name).write_text('<svg xmlns="http://www.w3.org/2000/svg"></svg>', encoding="utf-8")
        manual = directory / "manual-teste.md"
        manual.write_text(content, encoding="utf-8")
        return manual

    def test_destino_e_pasta_de_imagens_declarados(self):
        manual = self.montar_em_pasta_de_modulo(VALID.replace("imagens-manual-teste/", "imagens/"))
        self.assertEqual(verificar(self.root, manual, "imagens"), [])
        self.assertEqual(verificar(self.root, "docs/manuais/modulo-teste/manual-teste.md", "imagens"), [])

    def test_manual_usa_somente_a_pasta_de_imagens_declarada(self):
        manual = self.montar_em_pasta_de_modulo(VALID)
        self.assertTrue(any(i[0] == "M05" for i in verificar(self.root, manual, "imagens")))
        self.assertTrue(any(i[0] == "M05" for i in verificar(self.root, manual)))
        self.assertTrue(any(i[0] == "M05" for i in self.run_check(VALID.replace("imagens-manual-teste/", "imagens/"))))

    def test_pasta_de_imagens_invalida(self):
        self.manual.write_text(VALID, encoding="utf-8")
        for pasta in ("../imagens", "a/b", ".", ".."):
            with self.subTest(pasta=pasta), self.assertRaises(EntradaInvalida):
                verificar(self.root, self.manual, pasta)

    def test_logo_em_html_recusada(self):
        for bloco in ('<p align="center">', '<p style="text-align: center;">'):
            with self.subTest(bloco=bloco):
                html = bloco + '\n  <img src="imagens-manual-teste/logo.svg" alt="Logo de teste" width="240">\n</p>'
                codes = {i[0] for i in self.run_check(VALID.replace("![Logo de teste](imagens-manual-teste/logo.svg)", html))}
                self.assertTrue({"M04", "M06"} <= codes)

    def test_data_de_revisao_nao_e_uri_data(self):
        for phrase in ("Data: 5 de outubro de 2026.", "Data: 06/10/2026.", "Formato da data: dd/mm/aaaa."):
            with self.subTest(phrase=phrase):
                self.assertEqual(self.run_check(VALID.replace("# Manual de teste", "# Manual de teste\n\n" + phrase)), [])

    def test_uri_data_informa_linha(self):
        content = VALID.replace("imagens-manual-teste/campo.svg", "data:image/png;base64,AAAA")
        line = content.splitlines().index("![Campo Assunto](data:image/png;base64,AAAA)") + 1
        self.assertIn(("M05", line, "Imagem embutida, URI data ou bloco base64 proibido."), self.run_check(content))

    def test_aviso_markdown_pendente(self):
        content = VALID.replace("Informe até 200 caracteres.", "Informe até 200 caracteres.\n\n" + NOTICE)
        self.assertEqual([i[0] for i in self.run_check(content)], ["M09"])

    def test_caminho_escapado_e_navegacao_nao_confirmada(self):
        for navigation in (r"Cadastros & consultas > Registrar \[solicitação\]", "Navegação não confirmada; tela: Registrar solicitação"):
            notice = NOTICE.replace("Solicitações > Registrar solicitação", navigation)
            self.assertEqual([i[0] for i in self.run_check(VALID + "\n" + notice + "\n")], ["M09"])

    def test_colchetes_escapados_fora_do_aviso(self):
        tabela = "\n| Mensagem | Quando aparece |\n|---|---|\n| Unidade {0}*sigla*{1} sem acesso. | Sem acesso. |\n"
        self.assertTrue(any(i[0] == "M06" for i in self.run_check(VALID + tabela.format(r"\[", r"\]"))))
        self.assertTrue(any(i[0] == "M06" for i in self.run_check(VALID + "\nUnidade \\[*sigla*\\] sem acesso.\n")))
        for aberto, fechado in (("[", "]"), ("&#91;", "&#93;")):
            with self.subTest(colchete=aberto):
                self.assertEqual(self.run_check(VALID + tabela.format(aberto, fechado)), [])
        self.assertEqual(self.run_check(VALID + "\nDigite `\\[x\\]` no campo.\n"), [])

    def test_avisos_malformados_e_html_livre_rejeitados(self):
        for notice in (
            NOTICE.replace("Solicitações > Registrar solicitação", ""),
            NOTICE.replace("Solicitações > Registrar solicitação", "   "),
            NOTICE.replace("Solicitações > Registrar solicitação", "&lt;informar caminho&gt;"),
            NOTICE.replace("**caminho no sistema**", "caminho no sistema"),
            '<p align="center">' + NOTICE + '</p>',
            NOTICE.replace("Registrar solicitação", "<span>Registrar solicitação</span>"),
            NOTICE.replace("Registrar solicitação", "<script>alert(1)</script>"),
            NOTICE.replace(" - ", "\n - "),
            "    " + NOTICE,
            NOTICE.removeprefix("> "),
        ):
            with self.subTest(notice=notice):
                self.assertTrue(any(i[0] == "M06" for i in self.run_check(VALID + "\n" + notice + "\n")))

    def test_variantes_do_marcador_nao_geram_falso_pass(self):
        for notice in (
            NOTICE.replace("FUNCIONALIDADE]", "FUNCIONALIDADE"),
            NOTICE.replace("[NECESSÁRIO", r"\[NECESSÁRIO").replace("FUNCIONALIDADE]", r"FUNCIONALIDADE\]"),
            NOTICE.replace("[NECESSÁRIO", "&#91;NECESSÁRIO").replace("FUNCIONALIDADE]", "FUNCIONALIDADE&#93;"),
            NOTICE.replace("NECESSÁRIO", "NECESSARIO"),
            NOTICE.replace("NECESSÁRIO INSERIR", "necessário inserir"),
        ):
            with self.subTest(notice=notice):
                self.assertTrue(any(i[0] == "M06" for i in self.run_check(VALID + "\n" + notice + "\n")))

    def test_aviso_em_paragrafo_isolado_e_no_conteudo(self):
        for content in (
            VALID + NOTICE + "\n",
            VALID + "\n" + NOTICE + "\nTexto sem separação.\n",
            VALID.replace("# Manual de teste", NOTICE + "\n\n# Manual de teste"),
            VALID.replace("## Sumário", NOTICE + "\n\n## Sumário"),
            VALID.replace("- [Como registrar]", NOTICE + "\n\n- [Como registrar]"),
        ):
            with self.subTest(content=content):
                self.assertTrue(any(i[0] == "M06" for i in self.run_check(content)))

    def test_aviso_em_comentario_ou_codigo_nao_e_pendencia_visivel(self):
        for suffix in ("\n<!-- " + NOTICE + " -->\n", "\n```html\n" + NOTICE + "\n```\n"):
            self.assertEqual(self.run_check(VALID + suffix), [])

    def test_substituir_aviso_por_arquivo_remove_pendencia_estrutural(self):
        pending = VALID.replace("![Campo Assunto](imagens-manual-teste/campo.svg)", NOTICE)
        self.assertEqual([i[0] for i in self.run_check(pending)], ["M09"])
        # Arquivo sintético testa a referência, sem comprovar autenticidade de print.
        complete = pending.replace(NOTICE, "![Campo Assunto](imagens-manual-teste/campo.svg)")
        self.assertEqual(self.run_check(complete), [])

    def test_ancora_explicita_em_html_recusada(self):
        for ancora in ('<a name="campos"></a>', '<a id="campos"></a>'):
            content = VALID.replace("(#campos-e-opções)", "(#campos)").replace(
                "### Campos e opções", ancora + "\n\n### Campos e opções"
            )
            with self.subTest(ancora=ancora):
                self.assertTrue(any(i[0] == "M06" for i in self.run_check(content)))

    def test_base64_em_diferentes_construcoes(self):
        cases = (
            VALID.replace("imagens-manual-teste/campo.svg", "data:image/png;base64,AAAA"),
            VALID.replace("imagens-manual-teste/logo.svg", "data:image/png;base64,AAAA"),
            VALID + "\n<!-- data:image/png;base64,AAAA -->\n",
            VALID + "\n```text\ndata:image/png;base64,AAAA\n```\n",
            VALID + "\n[imagem]: data:image/png;base64,AAAA\n",
            VALID + "\n<!-- d&#97;ta:image/png;base64,AAAA -->\n",
            VALID + "\n" + "A" * 120 + "\n",
        )
        for content in cases:
            with self.subTest(content=content[-70:]):
                self.assertTrue(any(i[0] == "M05" for i in self.run_check(content)))

    def test_imagem_fora_do_destino(self):
        for source in (
            "../logo.svg", "/logo.svg", "https://example.invalid/logo.svg",
            "C:/logo.svg", "imagens-outro/campo.svg",
            "https://[",
            "imagens-manual-teste/../campo.svg", "imagens-manual-teste/%2e%2e/campo.svg",
        ):
            with self.subTest(source=source):
                issues = self.run_check(VALID.replace("imagens-manual-teste/campo.svg", source))
                self.assertTrue(any(i[0] == "M05" for i in issues))

    def test_imagem_ausente_vazia_tipo_ou_sem_alt(self):
        for content in (
            VALID.replace("campo.svg", "ausente.png"),
            VALID.replace("![Campo Assunto]", "![]"),
            VALID.replace("![Logo de teste]", "![]"),
        ):
            with self.subTest(content=content):
                self.assertTrue(any(i[0] == "M05" for i in self.run_check(content)))
        (self.images / "campo.svg").write_bytes(b"")
        self.assertTrue(any(i[0] == "M05" for i in self.run_check()))
        (self.images / "arquivo.txt").write_text("texto", encoding="utf-8")
        self.assertTrue(any(i[0] == "M05" for i in self.run_check(VALID.replace("campo.svg", "arquivo.txt"))))

    def test_symlink_nao_permite_escape_fisico(self):
        outside = self.root / "fora.svg"
        outside.write_text("imagem", encoding="utf-8")
        link = self.images / "atalho.svg"
        try:
            link.symlink_to(outside)
        except OSError as exc:
            self.skipTest(f"Criação de symlink indisponível: {exc.errno}")
        self.assertTrue(any(i[0] == "M05" for i in self.run_check(VALID.replace("campo.svg", "atalho.svg"))))

    def test_sumario_incompleto_fora_de_ordem_ou_nivel(self):
        for content in (
            VALID.replace("    - [Campos e opções](#campos-e-opções)\n", ""),
            VALID.replace("    - [Campos e opções]", "- [Campos e opções]"),
            VALID.replace("[Como registrar](#como-registrar)", "[Como registrar](#ausente)"),
            VALID.replace("- [Como registrar](#como-registrar)", "- [Como consultar](#como-consultar)"),
        ):
            with self.subTest(content=content):
                self.assertTrue(any(i[0] == "M06" for i in self.run_check(content)))

    def test_titulos_logo_e_hierarquia_invalidos(self):
        for content in (
            VALID.replace("### Campos e opções", "#### Campos e opções"),
            VALID + "\n# Segundo título\n",
            VALID + "\n## Como consultar\n\nOutro texto.\n",
            VALID.replace("![Logo de teste](imagens-manual-teste/logo.svg)\n", ""),
            "Introdução fora do lugar.\n\n" + VALID,
        ):
            with self.subTest(content=content):
                self.assertTrue(self.run_check(content))

    def test_legado_nao_suportado_sem_escrita(self):
        content = VALID.replace(
            "![Campo Assunto](imagens-manual-teste/campo.svg)",
            "![Campo Assunto][campo]\n\n[campo]: imagens-manual-teste/campo.svg"
        )
        self.assertTrue(any("não suportada" in i[2] for i in self.run_check(content)))
        self.assertTrue(self.run_check(VALID.replace("### Campos e opções", "Campos e opções\n---------------")))
        self.assertTrue(self.run_check(VALID + '\n<img src="imagens-manual-teste/campo.svg" alt="Campo">\n'))

    def test_fences_nao_criam_titulos_ou_links_falsos(self):
        content = VALID + '\n````text\n```\n# Ignorado\n[Link](#inexistente)\n````\n'
        self.assertEqual(self.run_check(content), [])
        self.assertTrue(self.run_check(VALID + '\n```text\n# Sem fechamento\n'))

    def test_probes_adversariais_de_formato_nao_passam(self):
        cases = (
            VALID + '\n<img\n src="https://example.invalid/imagem.png"\n alt="Imagem externa">\n',
            VALID + '\n<img\n src="../fora.png"\n alt="Imagem externa">\n',
            VALID.replace("1. Informe o assunto.", "<!--\n\n1. Informe o assunto."),
            VALID + '\n ## Tópico omitido\n\nTexto.\n',
            VALID + '\n##\tTópico omitido\n\nTexto.\n',
            VALID + '\n[Texto][sec]\n\n[sec]: #inexistente\n',
        )
        for content in cases:
            with self.subTest(content=content[-90:]):
                self.assertTrue(any(i[0] == "M06" for i in self.run_check(content)))

    def test_base64_png_real_dividido_em_linhas(self):
        payload = "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR42mNk+A8AAQUBAScY42YAAAAASUVORK5CYII="
        for width in (8, 40, 60):
            wrapped = "\n".join(payload[i:i + width] for i in range(0, len(payload), width))
            with self.subTest(width=width):
                issues = self.run_check(VALID + "\n```text\n" + wrapped + "\n```\n")
                self.assertTrue(any(i[0] == "M05" for i in issues))

    def test_entrada_invalida(self):
        self.manual.write_text(VALID, encoding="utf-8")
        fora = tempfile.TemporaryDirectory()
        self.addCleanup(fora.cleanup)
        externo = Path(fora.name) / "manual-externo.md"
        externo.write_text(VALID, encoding="utf-8")
        with self.assertRaises(EntradaInvalida):
            verificar(self.root, externo)
        for path in ("README.md",):
            candidate = self.root / path
            candidate.parent.mkdir(parents=True, exist_ok=True)
            candidate.write_text(VALID, encoding="utf-8")
            with self.subTest(path=path), self.assertRaises(EntradaInvalida):
                verificar(self.root, candidate)
        invalid = self.directory / "Manual Teste.md"
        invalid.write_text(VALID, encoding="utf-8")
        with self.assertRaises(EntradaInvalida):
            verificar(self.root, invalid)
        self.manual.write_bytes(b"\xff\xfe")
        with self.assertRaises(EntradaInvalida):
            verificar(self.root, self.manual)

    def test_codigos_de_saida(self):
        for content, expected in ((VALID, 0), (VALID.replace("campo.svg", "ausente.png"), 1)):
            self.manual.write_text(content, encoding="utf-8")
            with patch("sys.argv", ["verificar_manual.py", str(self.manual), "--raiz-repo", str(self.root)]), contextlib.redirect_stdout(io.StringIO()):
                self.assertEqual(main(), expected)
        with patch("sys.argv", ["verificar_manual.py", "ausente.md", "--raiz-repo", str(self.root)]), contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(main(), 2)

    def test_cli_distingue_pendencia_de_falha_sem_pass(self):
        for notice, summary in ((NOTICE, "PENDENTE:"), (NOTICE.removeprefix("> "), "FAIL:")):
            self.manual.write_text(VALID + "\n" + notice + "\n", encoding="utf-8")
            before = self.manual.read_bytes()
            output = io.StringIO()
            with patch("sys.argv", ["verificar_manual.py", str(self.manual), "--raiz-repo", str(self.root)]), contextlib.redirect_stdout(output):
                self.assertEqual(main(), 1)
            self.assertIn(summary, output.getvalue())
            self.assertNotIn("PASS:", output.getvalue())
            self.assertEqual(before, self.manual.read_bytes())


if __name__ == "__main__":
    unittest.main()
