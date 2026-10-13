# Adaptador: Sistema Solicitações, exemplo fictício

## Reconhecimento e alcance

Reconheça o exemplo pela documentação na raiz e por `src/sistema.py` com `MENUS` e `ROTAS`. O alcance contém somente registrar e consultar solicitações. Não há outros módulos nesta fixture.

## Versão e variante

Leia `VERSAO` em `src/sistema.py` em cada execução. A última conferência foi na versão 1.0.0; este valor histórico não substitui a fonte corrente. Interface em português brasileiro, sem flags ou implantação navegável.

## Leitura da codebase

Leia `README.md`, `src/sistema.py` e `recursos/logo.svg` em UTF-8. Não existe banco, tradutor ou framework a presumir. Use busca de símbolos e leitura integral do único arquivo de código.

## Pontes de evidência

`MENUS` aponta para os renderizadores de tela. A ação e o método do formulário se conectam às chaves de `ROTAS`, que apontam para `registrar` e `consultar`. O campo `descricao` se conecta ao objeto retornado por `registrar`; `situacao` conecta opções, filtro e estado. `permitido` aplica `PERMISSOES` tanto na apresentação quanto na operação.

## Interface e textos

Labels, ajuda e ações ficam nas strings de `formulario` e `tela_consulta`. Críticas e mensagens são retornos dos manipuladores correspondentes. `SITUACOES` declara o domínio do filtro. Não há i18n, serviço externo nem texto vindo de banco nesta fixture.

## Personas e acesso

| Persona ou público | Objetivo e tarefas | Conhecimento relevante | Perfil e restrições | Fonte e confirmação |
|---|---|---|---|---|
| Solicitante | Registrar e consultar solicitações | Nenhum requisito adicional informado | Solicitante; confirmar `PERMISSOES` | README e função `permitido` |
| Consulta | Consultar solicitações | Nenhum requisito adicional informado | Consulta; sem registro | README e função `permitido` |

## Publicação e recursos

Manual: `docs/manuais/manual-solicitacoes.md`. Imagens: `docs/manuais/imagens-manual-solicitacoes/`. Copie a logo fictícia aprovada de `recursos/logo.svg`. Leitura escolhida pelo responsável: GitHub Flavored Markdown, com o manual em Markdown puro. Use âncoras automáticas do GitHub e confira-as no renderizador. Não existem capturas reais nem dados pessoais.

## Validação e limites

Confira vínculos no arquivo de código, textos literais, regras e permissões. Execute o verificador da skill para estrutura. Leitura visual e operação em ambiente não foram executadas; não há ambiente disponível nem autorização externa. Última revisão funcional: versão 1.0.0. Revalide fontes e convenções antes de atualizar o manual.
