"""Testes de `plays_aplicaveis.py`.

Independente de proposito: não importa helper de outra skill nem de pasta
compartilhada.

    python3 -m unittest test_plays_aplicaveis
"""
import shlex
import subprocess
import tempfile
import time
import unittest
from pathlib import Path

from plays_aplicaveis import arquivos_do_escopo, detectar, relatorio_markdown


class TestPlaysAplicaveis(unittest.TestCase):

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.escopo = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def escrever(self, relativo, conteudo="<?php\n"):
        caminho = self.escopo / relativo
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(conteudo, encoding="latin-1")
        return caminho

    def test_comando_do_gate_nao_executa_o_nome_do_arquivo(self):
        """Arquivo de branch alheia com `$(...)` no nome vira um argumento só na linha impressa."""
        alvo = self.escrever("x$(touch PWNED)RN.php")
        todos, sem_dep = arquivos_do_escopo([str(self.escopo)])
        plays, gates = detectar(todos, sem_dep)
        relatorio = relatorio_markdown([str(self.escopo)], plays, gates, len(todos))
        linha = next(l for l in relatorio.splitlines() if l.startswith("python3 .agents/skills/sei-verificacao-rn/"))

        subprocess.run(["bash", "-c", linha], cwd=self.escopo, capture_output=True, check=False)

        self.assertFalse((self.escopo / "PWNED").exists(), linha)
        self.assertEqual(str(alvo), shlex.split(linha)[3])

    def test_arquivo_do_modulo_ia_aciona_plays_de_llm(self):
        for caminho in (
            self.escrever("fontes/sei/src/main/php/sei/web/modulos/ia/IaIntegracao.php"),
            Path("modulos/ia/rn/IaChatRN.php"),
        ):
            with self.subTest(caminho=caminho.as_posix()):
                plays, _ = detectar([caminho], [caminho])
                self.assertIn("llm-risk-assess", plays)
                self.assertIn("prompt-injection-testing (parte estatica)", plays)

    def test_dockerfile_com_sufixo_aciona_iac(self):
        for nome in ("Dockerfile", "Dockerfile.pw", "Dockerfile.dev"):
            with self.subTest(nome=nome):
                caminho = self.escrever(f"ops/{nome}", "FROM php:8.2\n")
                plays, _ = detectar([caminho], [caminho])
                self.assertIn("iac-security-review", plays)

    def test_cadastro_de_tarefa_e_detectado_em_tempo_linear(self):
        """Mesma elegibilidade do auditor de tarefa; 8.000 `new TarefaDTO` sem cadastrar terminam em menos de 1 s."""
        casos = {
            "criado e cadastrado": ("$objTarefaDTO = new TarefaDTO();\n$objTarefaRN->cadastrar($objTarefaDTO);\n", True),
            "cadastrado antes de criado": ("$objTarefaRN->cadastrar($objTarefaDTO);\n$objTarefaDTO = new TarefaDTO();\n", False),
            "outra variavel cadastrada": ("$objTarefaDTO = new TarefaDTO();\n$objTarefaRN->cadastrar($objTarefaDTO2);\n", False),
            "cadastro em comentario": ("$objTarefaDTO = new TarefaDTO();\n// $objTarefaRN->cadastrar($objTarefaDTO);\n", False),
            "INSERT INTO tarefa": ("BancoSEI::getInstance()->executarSql('INSERT INTO tarefa (id_tarefa) VALUES (1001)');\n", True),
            "TarefaDTO criado dentro de cadastrar": ("$objTarefaRN->cadastrar(new TarefaDTO());\n", True),
            "muitos TarefaDTO sem cadastrar": ("".join(f"$objTarefa{i}DTO = new TarefaDTO();\n" for i in range(8000)), False),
        }
        for indice, (nome, (corpo, elegivel)) in enumerate(casos.items()):
            with self.subTest(caso=nome):
                caminho = self.escrever(f"caso{indice}/sei_atualizar_versao_modulo_ts.php", "<?php\n" + corpo)

                inicio = time.perf_counter()
                _, gates = detectar([caminho], [caminho])
                duracao = time.perf_counter() - inicio

                self.assertEqual(elegivel, "sei-verificacao-tarefa" in gates)
                self.assertLess(duracao, 1.0)


if __name__ == "__main__":
    unittest.main()
