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

## Criacao e ativacao de um modulo

1. **Diretorio.** Criar o diretorio dentro do diretorio ja existente de modulos do sistema, `sei/web/modulos`, com um nivel opcional de instituicao antes do nome do modulo. Exemplo: `sei/web/modulos/abc/exemplo`.
2. **Classe de integracao.** Criar uma classe que estenda `SeiIntegracao` do core e implemente `getNome`, `getVersao` e `getInstituicao`. A classe e salva em arquivo com o mesmo nome, incluindo a caixa.
3. **Registro no core.** Adicionar no `ConfiguracaoSEI.php`, na chave `Modulos`, a referencia do nome da classe para o diretorio onde ela se encontra. Este passo exige autorizacao explicita do desenvolvedor, conforme o guardrail de Core no `AGENTS.md`.
4. **Verificacao.** Confirmar que o modulo carregou pelo menu Infra/Modulos do SEI. Ausencia na lista indica erro de nome de classe ou de diretorio na chave.

Exemplo do registro:

```php
'SEI' => array(
    'Modulos' => array('AbcExemploIntegracao' => 'abc/exemplo')
),
```
