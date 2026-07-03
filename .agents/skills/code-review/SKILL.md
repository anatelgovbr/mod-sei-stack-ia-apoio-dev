---
name: code-review
description: >
  Realizar code review complementar focado em correção funcional, qualidade,
  manutenibilidade e testes, sem executar gates SEI. Use para review genérico
  ou como complemento de `sei-code-review-security`; para diff, PR ou módulo
  SEI use `sei-code-review-security`.
---

# Code Review

Realize um code review crítico e construtivo de **correção funcional, qualidade,
manutenibilidade e testes**. **Não faça alterações de código** — apenas analise
e documente problemas e sugestões.

Esta skill é complementar. Em diff, PR, branch ou módulo SEI, use
`sei-code-review-security` para gates, segurança, impacto SEI e veredito de
merge; use `code-review` apenas para a dimensão de qualidade/manutenibilidade.

## Antes de Revisar

1. Delimite o escopo: objetivo da alteração, arquivos modificados, camada
   afetada e comportamento esperado.
2. Se o escopo for diff, PR, branch ou módulo SEI, encaminhe para
   `sei-code-review-security`; não emita veredito de merge por esta skill.
3. Consulte o contexto necessário antes de comentar:
   - `AGENTS.md` — guardrails técnicos e convenções operacionais
   - documentação funcional existente no repositório e contexto do desenvolvedor
   - `.agents/decisions/` — ADRs relevantes para entender decisões existentes
4. Leia o diff completo primeiro; depois leia o contexto do arquivo ou método
   quando necessário para confirmar ou derrubar um achado.
5. Classifique cada achado como `[introduzido]`, `[pre-existente]` ou `[incerto]`.
   Achado preexistente não deve bloquear a mudança atual, mas pode entrar como
   risco residual.

## Limites

- Não recrie a matriz V01-V10 nem os gates SEI.
- Segurança SEI, gates por artefato, impacto de release e veredito final são
  responsabilidade de `sei-code-review-security`.
- Se encontrar evidência clara de vulnerabilidade enquanto revisa qualidade,
  registre o local e recomende acionar `sei-code-review-security`; não faça uma
  análise V01-V10 paralela nesta skill.
- A ausência de ferramenta externa, cobertura perfeita ou automação não é achado
  por si só; reporte apenas lacunas com risco concreto para a mudança.

## Dimensões de Revisão

Avalie cada dimensão. Use os níveis de severidade para classificar achados.

### 1. Correção Funcional

- O código faz o que deveria fazer?
- Há casos de borda não tratados?
- A lógica está correta?
- Há regressão provável em fluxo existente?
- Há tratamento adequado para entradas vazias, nulas, inválidas ou limites?

### 2. Qualidade de Código

- Legibilidade e clareza dos nomes — variáveis, métodos e classes autoexplicativos e consistentes com o projeto?
- Coesão alta e acoplamento baixo — responsabilidade única (SRP), sem responsabilidades misturadas?
- Complexidade sob controle — ciclomática, aninhamento profundo, métodos longos demais?
- Tratamento de erro consistente — sem engolir exceção (`catch` vazio), com contexto útil e sem mascarar falhas relevantes?
- Código morto, branches/condições inalcançáveis ou redundantes, comentários enganosos ou desatualizados?
- Duplicação de lógica que deveria ser extraída por reutilização real, não por preferência estética?

### 3. Arquitetura e Padrões

- Respeitando as camadas definidas no projeto e na documentação existente?
- Dependências fluem na direção correta?
- Sem acoplamento indevido entre módulos?
- A mudança cria abstração prematura, helper desnecessário ou compatibilidade sem requisito concreto?
- A solução é a menor mudança objetiva que resolve o problema?

### 4. Testes

- Novos comportamentos cobertos por testes?
- Testes testam comportamento (não implementação)?
- Edge cases mais importantes cobertos?
- Se não houver teste automatizado viável, há evidência manual suficiente ou lacuna explicitada?

### 5. Manutenibilidade e Performance

- Fácil de entender para alguém novo?
- Performance aceitável (sem N+1, sem alocações desnecessárias)?
- Queries N+1 em loops de `listar()` — verificar se o `*BD.php` carrega coleções filhas dentro de um `foreach`, em vez de um join ou consulta em bloco via DTO.
- Consulta sem critério, sem limite ou com retorno superdimensionado (`retObj*`) para o uso real?
- Logging adequado para debugging em produção, sem ruído excessivo?

## Severidade

- **Crítico** — bloqueia a qualidade da mudança: bug grave, regressão provável,
  perda/corrupção de dados, comportamento central quebrado ou risco claro que
  exige revisão especializada.
- **Alto** — deve ser corrigido antes de considerar a mudança pronta: caso de
  borda importante quebrado, erro de integração, falta de teste em comportamento
  arriscado ou violação forte de padrão do projeto.
- **Médio** — atenção: complexidade desnecessária, responsabilidade misturada,
  duplicação relevante, nome confuso ou lacuna de teste de menor risco.
- **Sugestão** — opcional: melhoria pequena de legibilidade, simplificação local
  ou observação sem impacto direto na entrega.

Use **Crítico** ou **Alto** somente com evidência `arquivo:linha` e explicação de
impacto. Se a evidência for insuficiente, marque como `[incerto]` e faça uma
pergunta objetiva.

## Segunda Passada Obrigatória

Antes de finalizar:

1. Tente derrubar cada achado com contexto adicional do arquivo, método ou fluxo.
2. Remova achados que sejam preferência pessoal, hipótese fraca ou falso positivo.
3. Rebaixe ou marque como `[incerto]` quando faltar evidência concreta.
4. Preserve achados Críticos/Altos apenas quando houver impacto plausível e local
   verificável.

## Formato do Output

Priorize achados. Se não houver achados relevantes, diga explicitamente.

Use este formato:

```text
## Achados
- [Crítico|Alto|Médio|Sugestão][introduzido|pre-existente|incerto] <arquivo:linha> - <descrição objetiva do problema e impacto>. Sugestão: <menor ajuste que resolve>.

## Perguntas / Assunções
- <pergunta objetiva somente se bloquear a conclusão ou explicar achado incerto>

## Testes
- <lacunas de teste ou evidência revisada>

## Segurança / Gates SEI
- <não avaliados por esta skill; usar `sei-code-review-security` quando aplicável, ou registrar vulnerabilidade clara encontrada por evidência>

## Parecer de Qualidade
**sem achados relevantes | ajustes recomendados | risco alto | precisa de análise humana**
```

Para cada achado:
- **Local**: arquivo + linha (se possível)
- **Descrição**: o que está errado e por quê
- **Sugestão**: como corrigir
- **Origem**: regra de qualidade, teste, arquitetura ou documentação consultada

### Critério de Aprovação

A dimensão de qualidade está apta quando:

- zero achados **Crítico** em aberto
- zero achados **Alto** sem justificativa registrada
- achados `[incerto]` relevantes foram convertidos em pergunta objetiva ou
  encaminhados para análise humana

Este critério não substitui o veredito de merge de `sei-code-review-security`
quando a mudança estiver no escopo SEI.

## Regras

- Priorize bugs, regressões e riscos com evidência antes de sugestões cosméticas
- Não reescreva grandes trechos por preferência pessoal
- Proponha a simplificação objetiva mínima — sugira o menor ajuste que resolve; não reescreva o que já está claro
- Diferencie achados introduzidos pela mudança de problemas preexistentes
- Não bloqueie a mudança atual por problema preexistente sem evidência de agravamento
- Achados Críticos/Altos exigem evidência `arquivo:linha`
- Se a mudança tiver impacto arquitetural, recomende consultar um especialista em arquitetura antes de prosseguir.
- Se identificar uma decisão significativa implícita no código, recomende usar a skill `escrever-adr`
