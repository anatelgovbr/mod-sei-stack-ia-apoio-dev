# Gates de Implementacao — SEI

Fonte autoritativa para condicoes de bloqueio da stack. Verificar antes de qualquer entrega.

## Regras de Aplicacao

1. Gates C aplicam-se quando o desenvolvedor optar por `sei-gerador-crud`.
2. Gates G e R aplicam-se em qualquer trabalho no repositorio.
3. Gates D aplicam-se no Fluxo Direto quando a demanda envolver tipo reconhecido pela matriz de roteamento.
4. `TODO:` e contexto de review — nao e gate de bloqueio isolado e nao dispensa nenhum gate abaixo.
5. Gate satisfeito = parar e resolver antes de continuar.

## Tabela de Gates

| ID | Categoria | Condicao de Bloqueio | Condicao de Desbloqueio | Skill associada |
| --- | --- | --- | --- | --- |
| C1 | CRUD gerador | Gerador escolhido para novo CRUD sem contrato JSON confirmado | Obter confirmacao do contrato JSON com o desenvolvedor | `sei-gerador-crud` |
| C2 | CRUD gerador | Contrato JSON com campos obrigatorios ausentes (`entidade`, `colunas`, `sin_ativo`, `relacionamentos`) | Completar todos os campos obrigatorios com confirmacao do desenvolvedor | `sei-gerador-crud` |
| C3 | CRUD gerador | Escrita manual de `DTO`, `RN`, `BD`, `*_lista.php` ou `*_cadastro.php` antes do contrato confirmado | Aguardar confirmacao do contrato; usar gerador | `sei-gerador-crud` |
| C4 | CRUD gerador | `php -l` com erro nos arquivos gerados | Corrigir erro de sintaxe antes de continuar | `sei-gerador-crud` |
| G1 | Seguranca | Arquivo PHP com BOM ou caractere fora da conversao Latin-1 | Corrigir para blob final compativel com `.gitattributes` | `sei-verificacao-pagina` (P3) |
| G2 | Seguranca | `php -l` com erro de sintaxe em qualquer arquivo PHP | Corrigir erro antes de qualquer entrega | `sei-testes-validacao` |
| G3 | Seguranca | Acao PHP sem `validarLink()` e/ou `validarPermissao()` | Adicionar as chamadas no inicio da acao | `sei-verificacao-pagina` |
| G4 | Seguranca | Link de acao sem `assinarLink()` | Corrigir link para usar `assinarLink()` | `sei-verificacao-pagina` |
| G5 | Seguranca | Uso de `$_REQUEST` ou input nao validado | Substituir por `PaginaSEI::POST/GET` com validacao de tipo | `sei-verificacao-pagina` |
| G6 | Seguranca | Mudanca em `sei/` ou `sip/` fora de `modulos/**` sem proposta | Documentar via `escrever-adr` antes de implementar | — |
| G7 | Seguranca | XSS: output sem `PaginaSEI::tratarHTML()` | Usar `tratarHTML()` ou equivalente documentado | `sei-verificacao-pagina` |
| G8 | Seguranca | Controlador AJAX/WS sem dispatch seguro e/ou sem autorizacao especifica por acao/servico | Implementar whitelist explicita, regex restritiva para link sem assinatura e validar permissao antes da execucao | `sei-verificacao-controladores` (CI1-CI4) |
| G9 | Seguranca | Operacao de escrita via GET | Usar POST com link assinado | `sei-verificacao-pagina` |
| R1 | Release | Mudanca em BD (nova tabela, coluna, indice) sem script de instalacao/upgrade | Criar script SEI e/ou SIP correspondente | `sei-gerador-scripts-release`, `sip-gerador-scripts-release` |
| R3 | Release | `getVersao()` em `*Integracao.php` diverge dos scripts SEI/SIP | Sincronizar versao antes do merge | `sei-gerador-scripts-release`, `sip-gerador-scripts-release` |
| R4 | Release | Novos recursos SIP sem script SIP correspondente | Adicionar script SIP com registro de recursos | `sip-gerador-scripts-release` |
| R5 | Release | Nome de tabela/coluna com mais de 26 chars ou indice/FK/sequence com mais de 30 chars | Reduzir: tabelas/colunas <= 26; indices/FK/sequences <= 30 | `sei-verificacao-banco-dados` (R3) |
| R6 | Release | Script novo criado para modulo que ja tem script mapeado em `mapa-modulos-scripts.md` | Atualizar script existente — nunca criar duplicata | `sei-gerador-scripts-release`, `sip-gerador-scripts-release` |
| D1 | Contrato | Novo menu/pagina sem recurso SIP e permissao definidos | Definir recurso `md_<inst/mod>_<acao>` antes de implementar | `sei-menu-pagina` |
| D2 | Contrato | Evento/hook com efeito colateral ambiguo | Documentar efeito esperado e condicoes de disparo | `sei-mod-api-eventos` |
| D3 | Contrato | Operacao API usando classe interna sem justificativa | Substituir por `Entrada*API`/`Saida*API`/`SeiRN` ou documentar excecao | `sei-mod-api-operacoes` |
| D4 | Contrato | Alteracao de indexacao/pesquisa sem declarar momento e reprocessamento | Documentar estrategia de indexacao antes de implementar | `sei-guardrails-modulo` |
| D5 | Contrato | Criterio de aceite ausente para qualquer demanda | Definir ao menos um cenario de sucesso testavel antes de implementar | — |
