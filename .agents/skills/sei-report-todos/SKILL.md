---
name: sei-report-todos
description: Gera report de pendencias `TODO:` em modulos SEI escolhidos explicitamente pelo usuario. Use quando o usuario pedir listar, auditar, mapear ou gerar relatorio de TODOs do projeto ou de modulos.
disable-model-invocation: true
---

# Skill: Report de TODOs por Modulo SEI

Skill nao destrutiva para localizar pendencias marcadas com o padrao homologado
`TODO:` e consolidar um report por modulo escolhido pelo usuario.

## Regra Principal

- Procurar somente o marcador `TODO:`.
- Nao procurar nem normalizar marcadores alternativos.
- Nao alterar codigo, nao corrigir pendencias e nao criar issue automaticamente.
- Nao executar a varredura ate o usuario escolher explicitamente um ou mais modulos.

## Quando Usar

- Pedido para listar `TODO:` de um ou mais modulos.
- Pedido para gerar report de pendencias tecnicas documentadas.
- Pedido para auditar backlog tecnico marcado no codigo.
- Pedido para mapear pendencias antes de review, planejamento ou saneamento.

## Entradas

- Modulo(s) SEI escolhidos pelo usuario.
- Opcional: formato de saida (`resumo`, `detalhado` ou `markdown`).
- Opcional: destino do report. Por padrao, responder no chat; salvar arquivo somente se o usuario pedir explicitamente.

## Descoberta de Modulos

Se o usuario ainda nao informou os modulos:

1. Listar candidatos em `fontes/sei/src/main/php/sei/web/modulos/**`.
2. Preferir diretorios que contenham `*Integracao.php`, pois representam raiz de modulo.
3. Exibir os candidatos encontrados e perguntar quais modulos devem entrar no report.
4. Aguardar resposta. Nao interpretar ausencia de selecao como todos os modulos.

Se o usuario informou nomes parciais:

1. Resolver os nomes contra os caminhos existentes em `modulos/**`.
2. Se houver ambiguidade, perguntar qual caminho correto usar.
3. Se nao houver correspondencia, informar que o modulo nao foi encontrado e pedir nova selecao.

## Varredura

Para cada modulo escolhido:

1. Pesquisar `TODO:` dentro da raiz do modulo.
2. Ignorar diretorios de dependencia, build, cache e artefatos gerados quando existirem.
3. Registrar cada ocorrencia com `arquivo:linha`, trecho da linha e modulo.
4. Nao classificar automaticamente como bloqueante. `TODO:` e contexto de review conforme `AGENTS.md` e `.agents/references/gates-de-implementacao.md`.

## Classificacao do Report

Classificar cada ocorrencia apenas pelo texto e pelo arquivo onde aparece:

| Classe | Criterio |
|---|---|
| `divida conhecida` | Pendencia preexistente, rastreada ou melhoria futura sem risco imediato evidente |
| `risco relevante` | Menciona seguranca, permissao, transacao, release, auditoria, integridade ou comportamento incompleto |
| `bloqueante potencial` | Indica falta atual de controle obrigatorio ou incompletude em fluxo executavel critico |
| `ignorar no report executivo` | Exemplo, fixture, template, comentario sem relacao com fluxo executavel ou falso positivo evidente |

Use `bloqueante potencial`, nao `bloqueante`, porque esta skill nao substitui os gates obrigatorios.

## Formato de Saida

Responder em Markdown com:

```text
## Escopo
- Modulos analisados: <lista>
- Marcador pesquisado: `TODO:`
- Total de ocorrencias: <n>

## Resumo por Modulo
| Modulo | Ocorrencias | Divida conhecida | Risco relevante | Bloqueante potencial | Ignorar |
|---|---:|---:|---:|---:|---:|

## Pendencias
### <modulo>
| Classe | Arquivo:linha | Trecho |
|---|---|---|

## Observacoes
- `TODO:` nao bloqueia por si so e nao dispensa gates obrigatorios.
- Itens classificados como `risco relevante` ou `bloqueante potencial` exigem revisao humana ou gate especifico antes de virar decisao de merge.
```

## Salvamento Opcional

Se o usuario pedir arquivo de report:

- Salvar preferencialmente em `.agents/reports/todos-<data>.md`.
- Criar o diretorio somente se necessario.
- Nao salvar fora de `.agents/**` sem confirmacao explicita.

## Limites

- Nao alterar arquivos de codigo.
- Nao editar `TODO:` encontrado.
- Nao criar tarefas, issues ou ADR sem pedido explicito.
- Nao tratar `TODO:` como anistia para falha real de seguranca, permissao, transacao, release, auditoria ou integridade.
