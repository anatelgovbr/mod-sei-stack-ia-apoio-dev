# Referência — Arquitetura de módulos SEI (visão prática)

Este arquivo serve como “mapa mental” para navegação rápida ao trabalhar em módulos.

## Estrutura típica de um módulo
Em `.../sei/web/modulos/<org>/<modulo>/`:
- `*Integracao.php` (classe que estende `SeiIntegracao`)
- camadas (quando aplicável): `dto/`, `rn/`, `bd/`, `int/`, `ws/`
- páginas/ações PHP do módulo
- assets do módulo: `css/`, `js/`, `svg/`, `imagens/`

## Regras de design (alto nível)
- Lógica de negócio em RN; persistência em BD; transporte por DTO.
- Interceptação e UI (hooks) concentradas em `*Integracao.php`, delegando para RN quando crescer.
- Segurança na borda: link assinado + permissão por ação; inputs normalizados.

## Onde buscar exemplos
- `abc/exemplo`: demonstra hooks e integrações mínimas.
- `trf4/julgamento`: exemplo robusto com organização madura.

## Onde buscar assinaturas/contratos
- Para eventos/hook list e assinaturas: procurar em `SeiIntegracao.php` no core.
- Para operações: procurar em `SeiRN` e classes `Entrada*API`/`Saida*API` em `sei/web/api`.
