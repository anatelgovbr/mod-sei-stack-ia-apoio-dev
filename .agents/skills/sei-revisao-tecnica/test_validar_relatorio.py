"""Testes de `validar_relatorio.py`.

Independente de proposito: não importa helper de outra skill nem de pasta
compartilhada.
"""
import unittest

from validar_relatorio import validar

APROVADO = """## Revisao tecnica

### Resultado

❌ BLOCKED

**Escopo**: fontes/sei/src/main/php/sei/web/módulos/abc/exemplo (8 PHP, 3 PNG, 2 SVG)
**Revisao gerada por**: sei-revisao-tecnica

### Gates acionados

| Gate | Artefatos | Estado | Evidencia |
|---|---|---|---|
| G6 escopo de escrita | 8 arquivos PHP | ✅ PASS | Todos em `módulos/**`, caminho permitido |
| G2 `php -l`, via `sei-validacao-padrao` | 8 arquivos PHP | ✅ PASS | 8 de 8 sem erro de sintaxe |
| G1 encoding Latin-1 | 8 arquivos PHP | ✅ PASS | 8 de 8 em ISO-8859-1, nenhum BOM |
| `sei-verificacao-pagina` | 5 páginas `*_exemplo.php` | ❌ BLOCK | P1 e P2 ok em 4 de 5; P5 e P6 violados nas 5, com 53 leituras cruas de superglobal e zero uso de `PaginaSEI::GET/POST`; P8 ok, saída com `tratarHTML` |
| `sei-verificacao-controladores` | `MdAbcExemploIntegracao.php` | ❌ BLOCK | CI4 violado: `md_abc_auto_completar` executa sem `validarPermissao` |
| `sei-verificacao-rn` | `rn/MdAbcTesteRN.php`, `rn/ABCTesteRN.php` | ⚠️ WARN | T1 ok em `MdAbcTesteRN.php:6`; `validarAuditarPermissao` nos 2 métodos de escrita; `ABCTesteRN.php` e orfao com as validações comentadas |
| `sei-verificacao-tarefa` | `rn/MdAbcTesteRN.php` | ✅ PASS | `ID_TAREFA=65` com atributo `DESCRIÇÃO`, exceção documentada, linhas 24 e 70 |

### Achados

| # | Estado | Severidade | Origem | Local | Achado | Menor ajuste |
|---|---|---|---|---|---|---|
| 1 | ❌ BLOCK | BLOQUEANTE | preexistente | `MdAbcExemploIntegracao.php:406` | Ação AJAX `md_abc_auto_completar` executa sem `validarPermissao`, vetor V03, gate G8, CWE-862. Permite enumerar até 50 assuntos por consulta sem deter recurso do módulo | Inserir `SessaoSEI::getInstance()->validarPermissao('md_abc_auto_completar');` como primeira linha do case |
| 2 | ❌ BLOCK | ALTA | preexistente | `MdAbcExemploIntegracao.php:407` | `$_POST['palavras_pesquisa']` lido sem normalização, vetor V06, gate G5. O core faz a mesma chamada corretamente em `controlador_ajax.php:130` | Trocar por `PaginaSEI::POST('palavras_pesquisa')` |
| 3 | ❌ BLOCK | ALTA | preexistente | `processo_exemplo.php:58` | `$_POST['txtCampo1']` atribuido direto, vetor V06, gate G5. O arquivo tem 15 leituras cruas de superglobal | Usar `PaginaSEI::POST('txtCampo1')` e `PaginaSEI::GET('id_procedimento', 'int')` nas demais |
| 4 | ❌ BLOCK | ALTA | preexistente | `documento_exemplo.php:63` | `$_POST['txtCampo1']` atribuido direto, vetor V06, gate G5. O arquivo tem 17 leituras cruas de superglobal | Usar `PaginaSEI::POST('txtCampo1')` e `PaginaSEI::GET('id_documento', 'int')` nas demais |
| 5 | ❌ BLOCK | ALTA | preexistente | `controle_processos_exemplo.php:49` | `$_POST['txtTextoAndamento']` entregue a `lancarAndamentosManual()` sem normalização, vetor V06, gate G5. O arquivo tem 14 leituras cruas de superglobal | Usar `PaginaSEI::POST('txtTextoAndamento')` e `PaginaSEI::GET('id', 'int')` nas demais |
| 6 | ⚠️ WARN | MEDIA | preexistente | `rn/ABCTesteRN.php:16` | Arquivo orfao, sem nenhuma referência no repositório. E copia de `MdAbcTesteRN.php` com `validarAuditarPermissao` comentado nas linhas 16 e 59. Em módulo gabarito, e armadilha para quem copia | Remover o arquivo |
| 7 | ⚠️ WARN | BAIXA | preexistente | `MdAbcTesteRN.php:13` | `validarAuditarPermissao` chamado depois de `abrirTransacao()`, entao a verificação de permissão roda dentro da transação | Validar a permissão antes de abrir a transação |

### Passo a passo do achado

**Achado 1**: `controlador_ajax.php:8` faz só `validarLink()`, sem validar permissão -> `MdAbcExemploIntegracao.php:401` recebe o dispatch em `processarControladorAjax` -> `:406` entra no case sem `validarPermissao` -> `:407` chama `AssuntoINT::autoCompletarAssuntosRI1223()` -> `AssuntoINT.php:45` executa `AssuntoRN::pesquisarRN0246`, retornando até 50 assuntos com código e descrição

**Achado 2**: `$_POST['palavras_pesquisa']` em `MdAbcExemploIntegracao.php:407` -> `AssuntoINT.php:38` em `setStrPalavrasPesquisa()` -> `AssuntoINT.php:45` em `pesquisarRN0246`. Trafega por DTO, entao não e SQL injection: o risco e ausência de normalização de tipo

**Achado 5**: `$_POST['txtTextoAndamento']` em `controle_processos_exemplo.php:49` -> `MdAbcTesteRN.php:10` parametro `$strTextoAndamento` -> `MdAbcTesteRN.php:30` em `setValor()` do atributo `DESCRIÇÃO` -> `MdAbcTesteRN.php:36` em `SeiRN::lancarAndamento()`, persistindo no andamento do processo
"""


class TestValidarRelatorio(unittest.TestCase):

    def test_exemplo_aprovado_passa(self):
        """Freio contra regra minha que reprove o padrão acordado."""
        erros, avisos = validar(APROVADO)
        self.assertEqual([], erros)
        self.assertEqual([], avisos)

    def test_relatorio_vazio_falha_fechado(self):
        erros, _ = validar("")
        self.assertTrue(any(e.startswith('F0') for e in erros))

    def test_texto_sem_secoes_falha_fechado(self):
        erros, _ = validar("qualquer texto sem template")
        self.assertTrue(any(e.startswith('F1') for e in erros))

    def test_secao_extra_reprova(self):
        erros, _ = validar(APROVADO + "\n\n### Observações\n\ntexto extra\n")
        self.assertTrue(any(e.startswith('F1') for e in erros))

    def test_celula_acima_do_limite_reprova(self):
        inchada = APROVADO.replace(
            '| Remover o arquivo |',
            '| ' + ' palavra' * 30 + ' |')
        erros, _ = validar(inchada)
        self.assertTrue(any('Menor ajuste' in e for e in erros))

    def test_local_sem_linha_reprova(self):
        erros, _ = validar(APROVADO.replace('`rn/ABCTesteRN.php:16`', '`rn/ABCTesteRN.php`'))
        self.assertTrue(any(e.startswith('F9') for e in erros))

    def test_local_com_caminho_de_um_diretorio_passa(self):
        """`rn/ABCTesteRN.php:16` e valido, como no exemplo aprovado."""
        erros, _ = validar(APROVADO)
        self.assertFalse(any(e.startswith('F9') for e in erros))

    def test_salto_sem_ancora_reprova(self):
        quebrado = APROVADO.replace(
            '`AssuntoINT.php:38` em `setStrPalavrasPesquisa()`',
            'passa pelo INT sem citar arquivo')
        erros, _ = validar(quebrado)
        self.assertTrue(any(e.startswith('F11') for e in erros))

    def test_atalho_de_linha_apos_arquivo_nomeado_passa(self):
        """`:406` e valido depois de o arquivo já ter sido nomeado na linha."""
        erros, _ = validar(APROVADO)
        self.assertFalse(any(e.startswith('F11') for e in erros))

    def test_resultado_com_texto_anexado_reprova(self):
        erros, _ = validar(APROVADO.replace(
            '\n\u274c BLOCKED', '\n\u274c BLOCKED, parecer bloquear tecnicamente'))
        self.assertTrue(any(e.startswith('F12') for e in erros))

    def test_prosa_fora_de_celula_vira_aviso(self):
        _, avisos = validar(APROVADO + "\n\nNota fora do relatório sobre a revisão.\n")
        self.assertTrue(any(a.startswith('F13') for a in avisos))

    def test_bloco_markdown_externo_passa(self):
        """O relatório é emitido dentro de ```markdown para colar certo no GitLab."""
        erros, avisos = validar('```markdown\n' + APROVADO + '```\n')
        self.assertEqual([], erros)
        self.assertEqual([], avisos)

    def test_resultado_fora_do_topo_reprova(self):
        no_fim = APROVADO.replace('### Resultado\n\n\u274c BLOCKED\n\n', '') + '\n### Resultado\n\n\u274c BLOCKED\n'
        erros, _ = validar(no_fim)
        self.assertTrue(any(e.startswith('F1') for e in erros))

    def test_estado_invalido_reprova(self):
        erros, _ = validar(APROVADO.replace('| \u26a0\ufe0f WARN | MEDIA |', '| TALVEZ | MEDIA |'))
        self.assertTrue(any(e.startswith('F6') for e in erros))


if __name__ == '__main__':
    unittest.main()
