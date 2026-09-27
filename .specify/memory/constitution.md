# Constituição de Engenharia

Princípios não negociáveis. A fase de plano do SpecKit confere cada um no "Constitution Check"; violação sem justificativa registrada é erro.

## Princípios

### I. Teste primeiro (inegociável)

Todo código de produção novo ou alterado nasce de um teste que falhou antes da implementação. Defeito corrigido ganha teste de regressão.

### II. Cobertura mínima de 90% (inegociável)

Linhas e ramos, no projeto e no código novo, medidos pela skill `testes-unitarios-cobertura`. A cobertura total não pode cair. Reduzir o mínimo exige registro de decisão de arquitetura aprovado por pessoa.

### III. Segurança por padrão

Todo código novo ou alterado passa pelos tópicos de `.agents/security/guia-seguranca.md` que ele tocar. Mudança em autenticação, autorização, dado pessoal ou entrada externa inclui revisão de segurança antes do merge.

### IV. Documentação é entregável

Mudança de comportamento atualiza a documentação no mesmo pull request. Decisão de arquitetura fica registrada em `docs/adr/`.

### V. Revisão humana

Nenhuma mudança gerada por agente entra no ramo principal sem aprovação de uma pessoa no pull request, com o pipeline aprovado.

## Governança

Esta constituição prevalece sobre as demais práticas do projeto. Emenda exige pull request próprio, registro de decisão de arquitetura e aprovação humana.

**Versão**: 1.0.0 | **Ratificada**: a definir pelo projeto | **Última emenda**: 2026-09-27
