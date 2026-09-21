# Plano de Implementacao: [FEATURE]

**Branch**: `[###-nome-feature]` | **Data**: [DATA] | **Spec**: [link]
**Entrada**: Especificacao de feature em `/specs/[###-nome-feature]/spec.md`

**Nota**: Este template e copiado por `.specify/scripts/bash/setup-plan.sh` e preenchido pelo comando `/speckit.plan` ativo.

## Resumo

[Extrair da spec da feature: requisito principal + abordagem tecnica a partir da pesquisa]

## Contexto Tecnico

**Linguagem/Versao**: PHP 8.2
**Encoding**: ISO-8859-1 (Latin-1) — obrigatorio em todos os arquivos PHP
**Framework**: InfraPHP (DTO / RN / BD / paginas)
**Armazenamento**: [tabelas afetadas ou N/A]
**SGBD**: multi-SGBD obrigatorio (MySQL, PostgreSQL, Oracle, SQL Server)
**Testes**: `php -l` + `composer test` / `phpcs` / `phpstan`
**Modulo-alvo**: `fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/`
**Restricoes**: encoding, transacoes, permissao/link assinado, compatibilidade multi-SGBD

## Verificacao da Constitution

*GATE: Deve ser aprovado antes da Fase 0 de pesquisa. Reverificar apos a Fase 1 de design.*

[Gates determinados com base no arquivo constitution]

## Roteamento de Skills e Contratos

> Preencher usando `.agents/references/roteamento-de-skills.md`.
> Esse arquivo e a fonte autoritativa de contratos e gates — nao redefinir aqui;
> apenas registrar o status para esta feature.
> Se nenhuma skill SEI for necessaria, definir statuses como `nao-aplicavel` e explicar.

- **Tipo de Demanda**: [CRUD/menu-pagina/evento/API-WS/release/novo-modulo/hardening/validacao/outro]
- **Skill Necessaria**: [nome da skill ou nao-aplicavel]
- **Skills de Suporte**: [ex.: `sei-validacao-padrao`, `sei-guardrails-modulo`]
- **Status do Roteamento de Skills**: [PASS/BLOCKED/nao-aplicavel]

| Contrato | Localizacao | Status | Regra de Bloqueio |
| --- | --- | --- | --- |
| [nome do contrato] | [caminho do arquivo ou secao do plano] | [PASS/BLOCKED/nao-aplicavel] | [o que bloqueia plan/tasks/implement] |

**Notas sobre Contratos**: [questoes abertas, premissas ou motivo de nao-aplicabilidade]

## Gate do Gerador de CRUD

> **Preencher SOMENTE quando o desenvolvedor optar pelo gerador para uma ou mais entidades CRUD base novas**
> Fonte de regras: `.specify/memory/constitution.md` secao `Gerador de CRUD InfraPHP`.
> Se o gerador nao for escolhido, definir `Gerador Necessario: nao` e `Status do Gate de Planejamento: nao-aplicavel`.

- **Gerador Necessario**: [sim/nao]
- **Entidades Candidatas**: [ex.: `md_ri_filme`, `md_ri_ator`]
- **Diretorio de Contratos**: [ex.: `specs/[###-nome-feature]/crud-contratos/`]
- **Status do Diretorio**: [criado/confirmado/pendente/nao-aplicavel]
- **Status dos Contratos JSON**: [entidade -> ausente/rascunho/confirmado]
- **Status do Gate de Planejamento**: [PASS/BLOCKED/nao-aplicavel]
- **Regra de Bloqueio**: [Obrigatorio apenas quando `Gerador Necessario: sim`; o plano nao pode ser reportado como OK se depender de entidade CRUD gerada sem confirmacao explicita do desenvolvedor e contrato(s) JSON salvos]

## Estrutura do Projeto

### Documentacao (esta feature)

```text
specs/[###-feature]/
├── plan.md              # Este arquivo (saida do comando /speckit.plan)
├── crud-contratos/      # Obrigatorio quando `Gerador Necessario: sim`
├── research.md          # Saida da Fase 0 (comando /speckit.plan)
├── data-model.md        # Saida da Fase 1 (comando /speckit.plan)
├── quickstart.md        # Saida da Fase 1 (comando /speckit.plan)
├── contracts/           # Saida da Fase 1 (comando /speckit.plan)
└── tasks.md             # Saida da Fase 2 (comando /speckit.tasks — NAO criado por /speckit.plan)
```

### Codigo-Fonte — Modulo SEI

```text
fontes/sei/src/main/php/sei/web/modulos/<inst>/<modulo>/
├── <Modulo>Integracao.php   # extend SeiIntegracao (+ SipIntegracao)
├── <ModuloListar>.php       # paginas (acao = controlador)
├── <ModuloCadastrar>.php
├── dto/
│   └── <Modulo>DTO.php
├── rn/
│   └── <Modulo>RN.php
├── bd/
│   └── <Modulo>BD.php
├── int/
│   └── <Modulo>API.php      # Entrada*API / Saida*API (quando aplicavel)
├── css/                     # editar existente; nunca criar novo arquivo
├── js/                      # editar existente; nunca criar novo arquivo
├── svg/
├── imagens/
└── menu/

fontes/sei/src/main/php/sei/scripts/
└── <inst>_<modulo>_<versao>.php   # script de instalacao/upgrade SEI

fontes/sei/src/main/php/sip/scripts/
└── <inst>_<modulo>_<versao>.php   # script de instalacao/upgrade SIP
```

**Decisao de Estrutura**: [documentar quais camadas serao criadas/alteradas e por que]

## Impacto em BD

<!--
  Preencher apenas se houver mudanca em banco de dados.
-->

- **Novas tabelas**: [lista ou N/A]
- **Colunas novas em tabelas existentes**: [lista ou N/A]
- **Indices/sequences necessarios**: [lista ou N/A]
- **Compatibilidade multi-SGBD**: [pontos de atencao para Oracle/SQL Server, se aplicavel]
- **Script de migracao**: [nome do script ou "a criar"]

## Impacto em Menus, Recursos e Perfis

<!--
  Preencher apenas se houver mudanca em SIP ou menus externos.
-->

- **Novo recurso SIP**: [nome: `md_<inst/mod>_<acao>` ou N/A]
- **Novo menu no SIP**: [sim/nao — item vinculado ao recurso acima]
- **Novo perfil SIP**: [nome: `MD_<inst/mod>` ou N/A]
- **Menu externo (usuario externo / publicacoes)**: [evento usado ou N/A]
- **Icone de menu**: [SVG a criar? diretorio via `obterDiretorioIconesMenu`?]

## Impacto em Indexacao e Pesquisa

<!--
  Preencher apenas se houver impacto em pesquisa, feed, Solr, publicacao ou
  metadados pesquisaveis.
-->

- **Origem dos dados indexados**: [processo/documento/tabela/evento ou N/A]
- **Momento da indexacao**: [apos commit/evento/lote/manual ou N/A]
- **Reprocessamento/reindexacao**: [necessario? como executar?]
- **Risco transacional**: [indexacao fora de transacao critica?]

## Criterios de Entrega

- [ ] `php -l` sem erros em todos os arquivos PHP alterados
- [ ] Encoding ISO-8859-1 verificado nos arquivos gerados/alterados
- [ ] `validarLink` + `validarPermissao` em toda acao exposta
- [ ] Links de acao usam `assinarLink`
- [ ] Testes manuais documentados nas historias de usuario cobertos
- [ ] Script de release criado (se houver mudanca em BD ou SIP)
- [ ] Versoes SEI/SIP sincronizadas no script

## Registro de Complexidade

> **Preencher SOMENTE se a Verificacao da Constitution tiver violacoes que precisam ser justificadas**

| Violacao | Por que e Necessaria | Alternativa Mais Simples Rejeitada Porque |
|----------|---------------------|------------------------------------------|
| [ex.: nova camada fora do padrao] | [motivo] | [por que a alternativa padrao e insuficiente] |
