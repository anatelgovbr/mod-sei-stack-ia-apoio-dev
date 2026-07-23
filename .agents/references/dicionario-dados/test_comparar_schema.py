import contextlib
import io
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

import comparar_schema


def documento(descricao_coluna="Descricao."):
    return f"""# Dicionario

## Índice de Tabelas

- [tabela](#tabela)

## tabela

Descricao da tabela.

| Coluna | Descricao |
|---|---|
| id_tabela | {descricao_coluna} |
"""


def documento_seq():
    return """# Dicionario

## Índice de Tabelas

- [seq_tabela](#seq_tabela)

## seq_tabela

Sequence da tabela tabela.

| Coluna | Descricao |
|---|---|
| campo | Campo. |
| id | Identificador. |
"""


def documento_sem_pk_propria():
    return """# Dicionario

## Índice de Tabelas

- [usuario_login](#usuario_login)

## usuario_login

Descricao da tabela.

| Coluna | Descricao |
|---|---|
| dth_tentativa | Data. |
| id_usuario | ID. |
| tentativas | Numero. |
"""


class CompararSchemaTest(unittest.TestCase):
    def escrever(self, diretorio, nome, conteudo):
        path = Path(diretorio, nome)
        path.write_text(conteudo, encoding="utf-8")
        return path

    def test_detecta_indice_fora_da_ordem_das_secoes(self):
        conteudo = documento().replace(
            "- [tabela](#tabela)",
            "- [tabela_b](#tabela_b)\n- [tabela](#tabela)",
        ).replace(
            "## tabela\n",
            "## tabela\n\nDescricao.\n\n| Coluna | Descricao |\n|---|---|\n| id_tabela | ID. |\n\n"
            "## tabela_b\n",
        )
        with tempfile.TemporaryDirectory() as diretorio:
            path = self.escrever(diretorio, "dicionario.md", conteudo)
            *_, erros = comparar_schema.parse_dicionario(path)

        self.assertIn("indice deve corresponder 1:1 e na mesma ordem as secoes de tabela", erros)

    def test_detecta_alteracao_na_descricao_de_coluna(self):
        with tempfile.TemporaryDirectory() as diretorio:
            antigo = self.escrever(diretorio, "antigo.md", documento("Antes."))
            novo = self.escrever(diretorio, "novo.md", documento("Depois."))
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida):
                retorno = comparar_schema.cmd_diff(
                    SimpleNamespace(antigo=antigo, novo=novo, json=True)
                )

        resultado = json.loads(saida.getvalue())
        self.assertEqual(1, retorno)
        self.assertEqual(["id_tabela"], resultado["tabelas_alteradas"][0]["descricoes_colunas_alteradas"])

    def test_detecta_coluna_duplicada(self):
        conteudo = documento().replace(
            "| id_tabela | Descricao. |",
            "| id_tabela | Descricao. |\n| id_tabela | Repetida. |",
        )
        with tempfile.TemporaryDirectory() as diretorio:
            path = self.escrever(diretorio, "dicionario.md", conteudo)
            *_, erros = comparar_schema.parse_dicionario(path)

        self.assertIn("coluna duplicada em tabela: id_tabela", erros)

    def test_seq_nao_quebra_parser(self):
        with tempfile.TemporaryDirectory() as diretorio:
            path = self.escrever(diretorio, "dicionario.md", documento_seq())
            tabelas, ordem, descricoes, indice, erros = comparar_schema.parse_dicionario(path)

        self.assertEqual(["seq_tabela"], indice)
        self.assertEqual(["campo", "id"], ordem["seq_tabela"])
        self.assertEqual("Sequence da tabela tabela.", descricoes["seq_tabela"])
        self.assertEqual([], erros)

    def test_tabela_sem_pk_propria_fica_totalmente_alfabetica(self):
        with tempfile.TemporaryDirectory() as diretorio:
            path = self.escrever(diretorio, "dicionario.md", documento_sem_pk_propria())
            tabelas, ordem, descricoes, indice, erros = comparar_schema.parse_dicionario(path)
            problemas = comparar_schema.checar_ordem_colunas(ordem)

        self.assertEqual(["dth_tentativa", "id_usuario", "tentativas"], ordem["usuario_login"])
        self.assertEqual(0, problemas)

    def test_detecta_alteracao_na_descricao_da_tabela(self):
        with tempfile.TemporaryDirectory() as diretorio:
            antigo = self.escrever(diretorio, "antigo.md", documento())
            novo = self.escrever(diretorio, "novo.md", documento().replace("Descricao da tabela.", "Outra descricao."))
            saida = io.StringIO()
            with contextlib.redirect_stdout(saida):
                retorno = comparar_schema.cmd_diff(
                    SimpleNamespace(antigo=antigo, novo=novo, json=True)
                )

        resultado = json.loads(saida.getvalue())
        self.assertEqual(1, retorno)
        self.assertTrue(resultado["tabelas_alteradas"][0]["descricao_tabela_alterada"])
        self.assertEqual(1, resultado["contagem_alteracoes"]["descricoes_tabela_alteradas"])

    def test_senha_nao_entra_nos_argumentos_do_processo(self):
        resposta = subprocess.CompletedProcess(
            args=[],
            returncode=0,
            stdout="__VERSAO__\t5.0.4\ntabela\tid_tabela\n",
            stderr="",
        )
        with patch("comparar_schema.subprocess.run", return_value=resposta) as executar:
            versao, tabelas = comparar_schema.consultar_schema(
                "mysql", "usuario", "senha-secreta", "sei"
            )

        argumentos = executar.call_args.args[0]
        self.assertNotIn("senha-secreta", " ".join(argumentos))
        self.assertEqual("senha-secreta\n", executar.call_args.kwargs["input"])
        self.assertEqual("5.0.4", versao)
        self.assertEqual({"id_tabela"}, tabelas["tabela"])


if __name__ == "__main__":
    unittest.main()
