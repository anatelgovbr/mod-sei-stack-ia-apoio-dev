---
name: code-review
description: Realizar code review estruturado focado em correção, segurança, qualidade e aderência aos padrões do projeto. Use quando o usuário pedir revisão de código, quando houver mudanças significativas para avaliar, ou após implementação de uma feature. Não faz alterações — apenas analisa e documenta.
---

# Code Review

Realize um code review crítico e construtivo. **Não faça alterações de código** — apenas analise e documente problemas e sugestões.

## Antes de Revisar

1. Consulte os padrões do projeto:
   - `AGENTS.md` — guardrails técnicos e convenções operacionais
   - `PRD.md` — contexto de produto e objetivos gerais
   - `.agents/decisions/` — ADRs relevantes para entender decisões existentes
2. Entenda o contexto da mudança:
   - Qual o objetivo da alteração?
   - Quais arquivos foram modificados?
   - Se for um diff ou PR, leia o diff completo antes de comentar

## Dimensões de Revisão

Avalie cada dimensão. Use os níveis de severidade para classificar achados.

### 1. Correção Funcional
- O código faz o que deveria fazer?
- Há casos de borda não tratados?
- A lógica está correta?

### 2. Segurança (OWASP Top 10)
- Validação de entradas externas?
- SQL injection / XSS / command injection?
- Dados sensíveis sendo logados ou expostos?
- Controle de acesso adequado?

### 3. Qualidade de Código
- Nomenclatura clara e consistente com o projeto?
- Single Responsibility respeitado?
- Complexidade ciclomática aceitável?
- Ausência de código duplicado?

### 4. Arquitetura e Padrões
- Respeitando as camadas definidas no PRD?
- Dependências fluem na direção correta?
- Sem acoplamento indevido entre módulos?

### 5. Testes
- Novos comportamentos cobertos por testes?
- Testes testam comportamento (não implementação)?
- Edge cases mais importantes cobertos?

### 6. Manutenibilidade
- Fácil de entender para alguém novo?
- Performance aceitável (sem N+1, sem alocações desnecessárias)?
- Logging adequado para debugging em produção?

## Formato do Output

Organize os achados por severidade:

- **🔴 Crítico** — bloqueia merge: vulnerabilidades, erros lógicos graves, exposição de dados
- **🟠 Alto** — deve ser corrigido: violação de padrões, falta de validação, código sem testes
- **🟡 Médio** — atenção: nomes fracos, complexidade desnecessária, responsabilidade misturada
- **🟢 Sugestão** — opcional: otimizações de legibilidade, melhorias menores

Para cada achado:
- **Local**: arquivo + linha (se possível)
- **Descrição**: o que está errado e por quê
- **Sugestão**: como corrigir

## Regras

- Priorize bugs, regressões e riscos de segurança antes de sugestões cosméticas
- Não reescreva grandes trechos por preferência pessoal
- Se a mudança tiver impacto arquitetural, recomende usar o bom senso ou consultar um especialista em arquitetura antes de prosseguir.
- Se identificar uma decisão significativa implícita no código, recomende usar a skill `escrever-adr`
