# Referencias de roteamento — sei-direcionador-integracao

> Esta skill nao tem catalogo proprio. Ela usa os catalogos das 3 skills padrao.

## Onde buscar

| Necessidade | Skill padrão | Catalogo |
|---|---|---|
| Contrato de classe API (Entrada*API / Saida*API / *API) | `sei-mod-api-classes` | `references/catalogo-api.md` |
| Hook de extensao via sobrecarga em `*Integracao` | `sei-mod-api-eventos` | `references/catalogo-eventos.md` |
| Operacao via metodo `SeiRN` | `sei-mod-api-operacoes` | `references/catalogo-operacoes.md` |

## Como rotear

1. Receber a intencao textual do desenvolvedor.
2. Fazer busca nos 3 catalogos com esta prioridade: nome oficial do recurso, sinais de dominio, descricao, entrada principal e saida principal.
3. Se encontrar em apenas 1 catalogo: apontar aquele caminho e sugerir a skill padrao.
4. Se encontrar em 2 ou 3: listar as correspondencias e perguntar ao desenvolvedor.
5. Se houver varias correspondencias no mesmo catalogo: priorizar as que tiverem mais sinais de dominio aderentes a intencao.
6. Se uma entrada de `sei-mod-api-classes` aparecer apenas como contrato de suporte de uma operacao/evento ja identificado, nao trata-la como rota competidora; mencionar como complemento tecnico.
7. Apos confirmacao do desenvolvedor, lancar a skill padrao correspondente.

## Exemplo de fluxo

**Intencao**: "existe algo que me notifica quando um documento e gerado?"

1. Buscar nos 3 catalogos pela palavra-chave "gerarDocumento" ou "geracao documento", incluindo sinais de dominio e descricao.
2. Encontrar em `sei-mod-api-eventos`: `gerarDocumento`
3. Nao encontrar em `sei-mod-api-operacoes`
4. Nao encontrar em `sei-mod-api-classes`
5. Responder:

```
Encontrei 1 correspondencia para "gerarDocumento":

► Evento: gerarDocumento
  Catalogo: sei-mod-api-eventos
  Contexto: Apos geracao de documento

Opcao detectada: interceptar o evento apos geracao do documento via hook em *Integracao.

Voce quer seguir com a interceptacao desse evento?
  [1] Sim — usar sei-mod-api-eventos
  [2] Nao — mostrar outras correspondencias
```

6. Se o desenvolvedor escolher [1]: lancar `sei-mod-api-eventos`.

## Exemplos de saida esperada

### Exemplo 1: plano de trabalho

```text
Encontrei estas opcoes oficiais relacionadas ao que voce descreveu:

1. processarPaginaCadastroDocumento
   Catalogo: sei-mod-api-eventos
   Contexto: pagina de cadastro de documento com `IdPlanoTrabalho` na entrada.

2. processarPaginaInclusaoDocumentoItemEtapa
   Catalogo: sei-mod-api-eventos
   Contexto: pagina de inclusao de documento com `IdPlanoTrabalho`, `IdEtapaTrabalho` e `IdItemEtapa`.

Qual destas opcoes corresponde melhor ao seu caso?
```

### Exemplo 2: atribuir trabalho

```text
Encontrei estas opcoes oficiais relacionadas ao que voce descreveu:

1. atribuirProcesso
   Catalogo: sei-mod-api-operacoes
   Contexto: atribuicao de processo para usuario na unidade; sinais de dominio: atribuicao, carga de trabalho, responsavel.

Observacao: se voce seguir por essa operacao, o contrato de entrada associado e `EntradaAtribuirProcessoAPI`.

Voce quer seguir com essa operacao?
```

### Exemplo 3: organizar por bloco

```text
Encontrei estas opcoes oficiais relacionadas ao que voce descreveu:

1. gerarBloco
   Catalogo: sei-mod-api-operacoes
   Contexto: cria bloco para colaboracao; sinais de dominio: bloco, workspace, colaboracao.

2. incluirDocumentoBloco
   Catalogo: sei-mod-api-operacoes
   Contexto: adiciona documento a bloco; sinais de dominio: bloco, organizacao, analise.

3. incluirProcessoBloco
   Catalogo: sei-mod-api-operacoes
   Contexto: adiciona processo a bloco; sinais de dominio: bloco, agrupamento, analise.

Qual destas opcoes corresponde melhor ao seu caso?
```

### Exemplo 4: definir prazo do fluxo

```text
Encontrei estas opcoes oficiais relacionadas ao que voce descreveu:

1. definirControlePrazo
   Catalogo: sei-mod-api-operacoes
   Contexto: define prazo em processo; sinais de dominio: prazo, vencimento, dias uteis.

2. enviarProcesso
   Catalogo: sei-mod-api-operacoes
   Contexto: fluxo entre unidades com retorno programado.

Qual destas opcoes corresponde melhor ao seu caso?
```

## Regras de comportamento

- Esta skill **nao implementa** — apenas descobre e pergunta.
- **Nunca** sugerir implementacao propria antes de perguntar.
- Se nenhuma correspondencia for encontrada em nenhum catalogo: informar e sugerir `sei-guardrails-modulo`.
- Limite de opcoes na pergunta: **3 no maximo**. Se encontrar mais de 3, mostrar as 3 mais relevantes e sinalizar que há mais.
- Em buscas por dominio (ex.: `plano de trabalho`, `prazo`, `bloco`, `atribuicao`), priorizar linhas que exponham `Sinais de dominio`, `Entrada principal` ou `Saida principal`.
- Contrato de API que apenas suporta uma operacao/evento encontrado nao vira opcao principal separada; entra como contexto complementar.
