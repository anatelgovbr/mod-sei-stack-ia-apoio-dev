---
name: sei-direcionador-integracao
description: >
  Reuso do core: procura nos catálogos dos capítulos "Classes API", "Eventos" e
  "Operações" do manual de Módulos o contrato oficial do SEI antes de o módulo
  criar função, método, hook, página ou JS que lê ou altera dado do core ou que
  reage a ação ou tela do core, e dá o veredito "Reuso do core". Use também
  quando o pedido for ambíguo entre API, evento e operação ("existe algo para
  fazer X", "qual usar: evento ou operação") e para conferir se o código já
  escrito usou classe interna do core onde existe contrato oficial ("confira o
  reuso do core"). Não implementa: encaminha para a skill padrão.
---

# sei-direcionador-integracao

## Objetivo

Dar o veredito de reuso do core antes de o modulo criar codigo que toca o core:
o contrato oficial que ja faz o que se quer, nos catalogos dos capitulos
"Classes API", "Eventos" e "Operações" do manual de Modulos, ou a ausencia dele.
Depois do codigo escrito, conferir no diff se a entrega usou classe interna do
core onde existe contrato oficial.
Quando a intencao for ambigua entre API, evento e operacao, mostrar as opcoes
encontradas e perguntar qual o caminho antes de encaminhar.

## Quando usar

- Antes de planejar funcao, metodo, hook, pagina ou JS de modulo que le ou altera dado do core (processo, documento, andamento, assinatura, bloco, usuario, unidade, contato) ou que reage a acao ou tela do core, mesmo quando o pedido nao cita API, evento ou operacao.
- O desenvolvedor pergunta se ja existe algo no SEI para resolver seu caso.
- A intencao pode ser interpretavel como evento, operacao ou contrato API.
- O desenvolvedor nao sabe se precisa de `SeiRN`, de um hook em `*Integracao` ou de um contrato `*API`.
- Promptlike: "existe algo para fazer X", "qual usar: evento ou operacao", "como interceptar a geracao de documento", "preciso de um metodo que faca Y".
- Conferir código já escrito: pedido do desenvolvedor ("confira o reuso do core") ou aviso do auditor de reuso no `sei-validacao-padrao` ou no `sei-revisao-tecnica`.

## Procedimento

1. **Receber a intencao** do desenvolvedor (textual, informal, em portugues).
2. **Consultar os tres catalogos padrao** nesta ordem:
   - `sei-mod-api-classes`: `.agents/skills/sei-mod-api-classes/references/catalogo-api.md`
   - `sei-mod-api-eventos`: `.agents/skills/sei-mod-api-eventos/references/catalogo-eventos.md`
   - `sei-mod-api-operacoes`: `.agents/skills/sei-mod-api-operacoes/references/catalogo-operacoes.md`
3. **Pesquisar nos catalogos** usando esta prioridade:
   - nome oficial do recurso
   - sinais de dominio
   - descricao
   - entrada principal
   - saida principal
4. **Avaliar os resultados**:
    - Se encontrar **uma única** correspondência forte: dar o veredito no formato abaixo e encaminhar para a skill padrão, sem esperar resposta.
    - Se encontrar **2 ou 3** correspondências plausíveis, no mesmo catálogo ou em catálogos diferentes: listar cada opção com uma frase curta explicando por que se aplica.
    - Se houver muitas correspondencias no mesmo catalogo: priorizar as que tenham mais sinais de dominio aderentes a intencao textual.
    - Se uma correspondencia de API for apenas o **contrato de suporte** de uma
      operacao ou evento ja identificado, priorizar a operacao/evento como
      caminho principal e mencionar a API apenas como complemento, nao como
      opcao concorrente.
5. **Formular a pergunta objetiva** ao desenvolvedor, so quando houver 2 ou 3 opcoes plausiveis:
   - Apresentar no maximo 3 opcoes.
   - Cada opcao deve ter: nome do recurso, catalogo de origem, uma linha de contexto e, quando existir, o principal sinal de dominio encontrado.
   - Pergunta deve ser do tipo "qual" ou "voce quer", nunca "deveria".
   - Usar o formato de resposta padrao abaixo.
6. **Aguardar resposta** do desenvolvedor, quando houve pergunta, e **encaminhar** para a skill padrao correta:
   - Resposta indica API/contrato -> `sei-mod-api-classes`
   - Resposta indica evento/hook -> `sei-mod-api-eventos`
   - Resposta indica operacao/metodo `SeiRN` -> `sei-mod-api-operacoes`
7. **Se nenhuma correspondencia** for encontrada em nenhum catalogo:
   - Os catalogos cobrem o core 5.0.6; em core mais novo, procurar tambem o nome em `SeiIntegracao.php`, na pasta `api/` e em `SeiRN.php` antes de concluir.
   - Informar que nenhum contrato oficial foi encontrado no catalogo.
   - Sinalizar que sera necessaria implementacao propria com justificativa de seguranca.
   - Encaminhar para `sei-guardrails-modulo` para avaliar o risco.
8. **Registrar o veredito no plano**, na linha `Reuso do core: <NomeOficial> (<catalogo>)` ou `Reuso do core: sem contrato no catalogo`; com mais de uma funcao, metodo, hook, pagina ou JS, uma linha para cada, com o nome dele antes do veredito.

### Conferir código já escrito

1. Rodar `python3 .agents/skills/sei-direcionador-integracao/audit.py --base <ref>`: padrao `HEAD` para a entrega nao commitada; a branch de origem para os commits da branch.
2. Para cada chamada e cada funcao listada, seguir os passos 2 a 8 com a intencao daquele codigo.
3. Antes de trocar a chamada interna pelo contrato, comparar no `SeiRN.php` os campos gravados, os filtros e as validacoes do contrato com os da chamada interna. Diferenca que muda o resultado mantem a chamada interna, com a diferenca na linha `Reuso do core:`.

### Formato de resposta padrao

Quando houver 1 correspondencia forte:

```text
Reuso do core: <NomeOficial> (<sei-mod-api-classes|sei-mod-api-eventos|sei-mod-api-operacoes>)
Contexto: <descricao curta + sinal de dominio>
Proximo passo: <skill padrao>
```

Quando houver 2 ou 3 correspondencias plausiveis:

```text
Encontrei estas opcoes oficiais relacionadas ao que voce descreveu:

1. <NomeOficial>
   Catalogo: <sei-mod-api-classes|sei-mod-api-eventos|sei-mod-api-operacoes>
   Contexto: <descricao curta + sinal de dominio>

2. <NomeOficial>
   Catalogo: <sei-mod-api-classes|sei-mod-api-eventos|sei-mod-api-operacoes>
   Contexto: <descricao curta + sinal de dominio>

Qual destas opcoes corresponde melhor ao seu caso?
```

Quando nao houver correspondencia:

```text
Reuso do core: sem contrato no catalogo
Nao encontrei contrato oficial claro nos catalogos de API, eventos ou operacoes para esse caso.

Se a necessidade continuar a mesma, o proximo passo e avaliar implementacao propria com `sei-guardrails-modulo`.
```

## Critérios de validação

- [ ] A skill leu os 3 catalogos antes de formular resposta.
- [ ] Nao implementou nem sugeriu implementacao propria antes do veredito.
- [ ] O plano traz a linha `Reuso do core`.
- [ ] Na conferencia, cada item do auditor tem veredito, e a troca por contrato comparou campos, filtros e validacoes.
- [ ] A pergunta ao desenvolvedor tem no maximo 3 opcoes.
- [ ] Contrato API de suporte nao foi apresentado como concorrente de uma operacao/evento ja claramente identificado.
- [ ] A triagem considerou sinais de dominio antes de concluir que nao havia correspondencia relevante.
- [ ] Com 2 ou 3 opcoes, o encaminhamento respeita a escolha do desenvolvedor.
- [ ] Se nenhuma correspondencia foi encontrada, a resposta informa isso claramente.
- [ ] A skill nao tem catalogo proprio: usa os catalogos das 3 skills padrao e, em core mais novo que o dos catalogos, o codigo do core do passo 7.

## Referências

- Catalogo `sei-mod-api-classes`: `.agents/skills/sei-mod-api-classes/references/catalogo-api.md`
- Catalogo `sei-mod-api-eventos`: `.agents/skills/sei-mod-api-eventos/references/catalogo-eventos.md`
- Catalogo `sei-mod-api-operacoes`: `.agents/skills/sei-mod-api-operacoes/references/catalogo-operacoes.md`
- Skill padrao `sei-mod-api-classes`: `.agents/skills/sei-mod-api-classes/SKILL.md`
- Skill padrao `sei-mod-api-eventos`: `.agents/skills/sei-mod-api-eventos/SKILL.md`
- Skill padrao `sei-mod-api-operacoes`: `.agents/skills/sei-mod-api-operacoes/SKILL.md`
- Auditor de reuso no diff, chamado pelo `sei-validacao-padrao` e pelo `sei-revisao-tecnica`: `.agents/skills/sei-direcionador-integracao/audit.py`
