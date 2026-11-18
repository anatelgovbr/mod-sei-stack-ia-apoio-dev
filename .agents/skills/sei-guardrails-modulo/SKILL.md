---
name: sei-guardrails-modulo
description: Guardrails obrigatorios para qualquer trabalho em modulos SEI — verifica scripts de instalacao existentes, impede criacao de arquivos duplicados (scripts, CSS, JS), avalia dependências com registros do core (inclusive protocolos), garante escopo, permissao/link assinado, transacao/auditoria e aciona skills especializadas quando necessario.
---

# Skill: Guardrails de Modulo SEI


## Quando NÃO usar
- Mudanças no core fora de `.../sei/web/modulos/**` (isso exige governança e proposta).

## Fonte de verdade
- `AGENTS.md` (guardrails universais, padrão transacional e fontes de contexto)
- `.agents/security/matriz-vulnerabilidades-sei.md`
- `.agents/references/padrao-codificacao-php.md`

## Passo a passo
1. Confirmar **módulo-alvo** e escopo (ver `AGENTS.md`).
2. **Verificar scripts de instalacao existentes** consultando
   `.agents/references/mapa-modulos-scripts.md`:
   - Se o modulo estiver no mapa:
     - novo DTO, nova entidade CRUD base, nova tabela, ou alteracao de colunas
       em DTO existente **exige** atualizacao dos scripts mapeados;
     - a skill deve avisar explicitamente o desenvolvedor sobre esse impacto de
       release;
     - nunca criar novos arquivos de script para esse modulo.
   - Se o modulo nao estiver no mapa: verificar fisicamente em `sei/scripts/` e
     `sip/scripts/` antes de concluir ausencia (nomes podem fugir do padrao convencional).
3. **Verificar assets existentes** (CSS e JS) na pasta do modulo-alvo:
   - Se `css/` ja contiver arquivos: **nao criar novos arquivos CSS**. Editar os existentes.
   - Se `js/` ja contiver arquivos: **nao criar novos arquivos JS**. Editar os existentes.
   - Regra identica para arquivos PHP de asset (`*_css.php`, `*_js.php`) na raiz do modulo.
4. Antes de implementar, inventariar dependências módulo → core afetadas, inclusive protocolos e mudança apenas em RN. Aplicar a matriz de [proteção das dependências](../sei-mod-api-eventos/references/protecao-dependencias-core.md), distinguir FK física de metadado DTO e política funcional, e encaminhar a interceptação a `sei-mod-api-eventos`. Cobertura depende do callsite eficaz e dos testes, não apenas da existência de hook.

   Identificar os pontos de impacto do módulo: menu/página, eventos, botões/ícones, operações/WS, BD/scripts.
5. Garantir **bases obrigatórias** antes de implementar:
   - link assinado + permissão por ação
   - transação quando houver escrita relevante
   - auditoria quando aplicável
   - interface visual criada ou alterada, inclusive CSS/JS sem PHP: aplicar `.agents/references/padrao-acessibilidade-cores-sei.md` e acionar `sei-validacao-padrao`
   - página com filtro, formulário, barra de comandos ou grid criada ou alterada: aplicar `.agents/references/padrao-interacao-telas-sei.md`
6. Acionar as skills específicas quando necessário:
   - **Implementacao**: `sei-menu-pagina`, `sei-mod-api-eventos`, `sei-mod-api-operacoes`,
      `sei-gerador-scripts-release`, `sip-gerador-scripts-release`, `sei-validacao-padrao`
   - **Gates de verificacao** (obrigatorios conforme artefatos presentes):
     - `sei-verificacao-pagina` — para toda pagina `*_lista.php` ou `*_cadastro.php`
     - `sei-verificacao-controladores` — para metodos de controlador em `*Integracao.php`
     - `sei-verificacao-rn` — para `*RN.php`
     - `sei-verificacao-banco-dados` — para `*DTO.php`, `*BD.php` ou DDL de release
     - `sei-verificacao-tarefa` — quando houver atribuicao de andamento/tarefa
   - Se o desenvolvedor escolheu `sei-gerador-crud` para o CRUD, delegar
     ao gerador e considerar que a skill dele deve cobrir tambem a fase de
     release.
   - Se o CRUD for manual, manter esta skill como guardrail central e acionar
     `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` para a parte de release.
7. Validar a entrega contra escopo, segurança, impacto de release e gates obrigatórios aplicáveis.

## Saída esperada
- Uma implementação (ou revisão) que respeita escopo, camadas, guardrails de segurança e impacto de release do módulo, com evidências de validação.
