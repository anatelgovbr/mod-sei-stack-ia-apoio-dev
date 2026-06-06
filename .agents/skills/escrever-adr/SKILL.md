---
name: escrever-adr
description: Documentar uma decisão arquitetural significativa como ADR (Architecture Decision Record) em .agents/decisions/. Use quando o usuário discutir escolhas de tecnologia, padrões, estrutura, ou quando uma decisão for difícil de reverter e precisar ser explicada para o time.
---

# Write ADR

Documente uma decisão arquitetural significativa usando o template do projeto.

## Quando Criar um ADR

Crie um ADR quando a decisão:
- Afeta a arquitetura do sistema (escolha de tecnologia, padrão, estrutura)
- É difícil de reverter posteriormente
- Vale ser explicada para quem não estava presente na discussão
- Documenta *por que não* algo foi escolhido (tão importante quanto o que foi)

**Não crie um ADR** para:
- Mudanças triviais de implementação
- Refatorações locais sem impacto arquitetural
- Decisões que já estão documentadas em um ADR existente

## Antes de Criar

1. Consulte `.agents/decisions/` — verificar se já existe um ADR similar
2. Leia `PRD.md` — contexto arquitetural para embasar a decisão
3. Se o usuário não forneceu detalhes suficientes, **pergunte**:
   - Qual é o problema ou contexto que levou à decisão?
   - Quais opções foram consideradas?
   - Qual foi a decisão final e por quê?
   - Quais são as consequências esperadas?

## Processo

1. **Determine o próximo número** de ADR contando arquivos em `.agents/decisions/` (excluindo `_TEMPLATE_ADR.md`)
2. **Colete todas as informações** — faça perguntas se necessário
3. **Crie o arquivo** `ADR-XXX-titulo-em-kebab-case.md` em `.agents/decisions/`
4. **Preencha todos os campos** do template `.agents/decisions/_TEMPLATE_ADR.md`:
   - Contexto com descrição clara do problema
   - Opções consideradas com prós, contras e esforço
   - Decisão com justificativa concreta
   - Consequências positivas e negativas
5. **Confirme** o arquivo criado
6. **Verifique** se algum ADR existente deve ser marcado como "Superado por ADR-XXX"

## Regras

- ADRs são **imutáveis** — para revisar uma decisão, crie um novo ADR que referencia e supera o anterior
- Use linguagem objetiva e permanente — o ADR será lido por pessoas que não estavam na discussão
- Inclua as opções rejeitadas e por que foram rejeitadas — isso é tão valioso quanto a decisão em si
- Não crie ADR para decisão trivial — use o bom senso
