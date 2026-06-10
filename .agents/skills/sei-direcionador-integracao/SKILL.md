---
name: sei-direcionador-integracao
description: >
  Skill mediadora que, a partir de uma intencao ambigua do desenvolvedor,
  consulta os catalogos de API, eventos e operacoes do SEI e pergunta
  qual caminho oficial e o correto antes de encaminhar para a skill padrao.

  Use quando:
  - O desenvolvedor nao sabe se precisa de um contrato API, de um hook de
    evento ou de uma operacao via SeiRN
  - A demanda e ambigua entre as 3 capacidades do core (API, evento, operacao)
  - Promptlike: "existe algo para fazer X", "qual usar: evento ou operacao",
    "preciso interceptar algo no SEI", "como faco para Y"

  Esta skill NAO implementa, NAO roteia diretamente e NAO tem catalogo proprio.
  A unica saida e uma pergunta objetiva ao desenvolvedor e o encaminhamento
  para a skill padrao correta.
---

# sei-direcionador-integracao

## Objetivo

Mediar a primeira etapa de descoberta quando o desenvolvedor tem uma necessidade
ambigua em relacao a API, eventos ou operacoes do core do SEI, mostrando as
opcoes encontradas nos tres catalogos padrao e perguntando qual o caminho
correto antes de encaminhar.

## Quando usar

- O desenvolvedor pergunta se ja existe algo no SEI para resolver seu caso.
- A intencao pode ser interpretavel como evento, operacao ou contrato API.
- O desenvolvedor nao sabe se precisa de `SeiRN`, de um hook em `*Integracao` ou de um contrato `*API`.
- Promptlike: "existe algo para fazer X", "qual usar: evento ou operacao", "como interceptar a geracao de documento", "preciso de um metodo que faca Y".

## Procedimento

1. **Receber a intencao** do desenvolvedor (textual, informal, em portugues).
2. **Consultar os tres catalogos padrao** nesta ordem:
   - `sei-mod-api`: `references/catalogo-api.md`
   - `sei-mod-eventos`: `references/catalogo-eventos.md`
   - `sei-mod-operacoes`: `references/catalogo-operacoes.md`
3. **Pesquisar nos catalogos** usando esta prioridade:
   - nome oficial do recurso
   - sinais de dominio
   - descricao
   - entrada principal
   - saida principal
4. **Avaliar os resultados**:
   - Se encontrar correspondência em apenas **1 catalogo**: indicar o caminho e a skill padrao correspondente.
   - Se encontrar correspondência em **2 ou 3 catalogos**: listar cada opcao com uma frase curta explicando por que se aplica.
   - Se houver muitas correspondencias no mesmo catalogo: priorizar as que tenham mais sinais de dominio aderentes a intencao textual.
5. **Formular a pergunta objetiva** ao desenvolvedor:
   - Apresentar no maximo 3 opcoes.
   - Cada opcao deve ter: nome do recurso, catalogo de origem, uma linha de contexto e, quando existir, o principal sinal de dominio encontrado.
   - Pergunta deve ser do tipo "qual" ou "voce quer", nunca "deveria".
   - Usar o formato de resposta padrao abaixo.
6. **Aguardar resposta** do desenvolvedor e **encaminhar** para a skill padrao correta:
   - Resposta indica API/contrato -> `sei-mod-api`
   - Resposta indica evento/hook -> `sei-mod-eventos`
   - Resposta indica operacao/metodo `SeiRN` -> `sei-mod-operacoes`
7. **Se nenhuma correspondencia** for encontrada em nenhum catalogo:
   - Informar que nenhum contrato oficial foi encontrado no catalogo.
   - Sinalizar que sera necessaria implementacao propria com justificativa de seguranca.
   - Encaminhar para `sei-guardrails-modulo` para avaliar o risco.

### Formato de resposta padrao

Quando houver 1 correspondencia forte:

```text
Encontrei 1 opcao oficial relacionada ao que voce descreveu:

1. <NomeOficial>
   Catalogo: <sei-mod-api|sei-mod-eventos|sei-mod-operacoes>
   Contexto: <descricao curta + sinal de dominio>

Voce quer seguir por esse caminho?
```

Quando houver 2 ou 3 correspondencias plausiveis:

```text
Encontrei estas opcoes oficiais relacionadas ao que voce descreveu:

1. <NomeOficial>
   Catalogo: <sei-mod-api|sei-mod-eventos|sei-mod-operacoes>
   Contexto: <descricao curta + sinal de dominio>

2. <NomeOficial>
   Catalogo: <sei-mod-api|sei-mod-eventos|sei-mod-operacoes>
   Contexto: <descricao curta + sinal de dominio>

Qual destas opcoes corresponde melhor ao seu caso?
```

Quando nao houver correspondencia:

```text
Nao encontrei contrato oficial claro nos catalogos de API, eventos ou operacoes para esse caso.

Se a necessidade continuar a mesma, o proximo passo e avaliar implementacao propria com `sei-guardrails-modulo`.
```

## Critérios de validação

- [ ] A skill leu os 3 catalogos antes de formular resposta.
- [ ] Nao implementou nem sugeriu implementacao propria antes de perguntar ao usuario.
- [ ] A pergunta ao desenvolvedor tem no maximo 3 opcoes.
- [ ] A triagem considerou sinais de dominio antes de concluir que nao havia correspondencia relevante.
- [ ] O encaminhamento respeita a escolha do desenvolvedor.
- [ ] Se nenhuma correspondencia foi encontrada, a resposta informa isso claramente.
- [ ] A skill nao tem catalogo proprio — usa exclusivamente os catalogos das 3 skills padrao.

## Referências

- Catalogo `sei-mod-api`: `.agents/skills/sei-mod-api/references/catalogo-api.md`
- Catalogo `sei-mod-eventos`: `.agents/skills/sei-mod-eventos/references/catalogo-eventos.md`
- Catalogo `sei-mod-operacoes`: `.agents/skills/sei-mod-operacoes/references/catalogo-operacoes.md`
- Skill padrao `sei-mod-api`: `.agents/skills/sei-mod-api/SKILL.md`
- Skill padrao `sei-mod-eventos`: `.agents/skills/sei-mod-eventos/SKILL.md`
- Skill padrao `sei-mod-operacoes`: `.agents/skills/sei-mod-operacoes/SKILL.md`
