# Gates de Implementacao do SEI

Fonte autoritativa para condicoes de bloqueio da stack. Verificar antes de qualquer entrega.

## Regras de Aplicacao

1. Gates C aplicam-se quando o desenvolvedor optar por `sei-gerador-crud`.
2. Gates G e R aplicam-se em qualquer trabalho no repositorio.
3. Gates D aplicam-se no Fluxo Direto quando a demanda envolver tipo reconhecido pela matriz de roteamento.
4. `TODO:` e contexto de review. Nao e gate de bloqueio isolado e nao dispensa nenhum gate abaixo.
5. Severidade do risco e estado do gate sao dimensoes independentes. A severidade qualifica o impacto; `PASS`, `WARN` e `BLOCK` registram o resultado da verificacao.
6. Violacao confirmada de gate bloqueante retorna `BLOCK`, independentemente da severidade atribuida ao risco.
7. Condicao de bloqueio confirmada exige parar e resolver antes de continuar.

## Estados dos Gates

| Estado | Uso |
| --- | --- |
| `PASS` | Gate executado sobre ao menos um artefato compativel, sem desvio |
| `WARN` | Risco nao bloqueante ou heuristica inconclusiva |
| `BLOCK` | Violacao confirmada de gate bloqueante |

Zero artefatos analisados nao equivale a `PASS`.

## Tabela de Gates

| ID | Categoria | Condicao de Bloqueio | Condicao de Desbloqueio | Skill associada |
| --- | --- | --- | --- | --- |
| C1 | CRUD gerador | Gerador escolhido para novo CRUD sem contrato JSON confirmado | Obter confirmacao do contrato JSON com o desenvolvedor | `sei-gerador-crud` |
| C2 | CRUD gerador | Contrato JSON com campos obrigatorios ausentes (`entidade` com `tabela`, `singular`, `plural`, `artigo`, `campoPrincipal` e `comentario`; `colunas` com `obrigatorio` e `comentario`; `regrasGeracao.campoSinAtivo` no CRUD simples; `relacionamentosNn` na N:N) | Completar todos os campos obrigatorios com confirmacao do desenvolvedor | `sei-gerador-crud` |
| C3 | CRUD gerador | Escrita manual de `DTO`, `RN`, `BD`, `*_lista.php` ou `*_cadastro.php` antes do contrato confirmado | Aguardar confirmacao do contrato; usar gerador | `sei-gerador-crud` |
| C4 | CRUD gerador | `php -l` com erro nos arquivos gerados | Corrigir erro de sintaxe antes de continuar | `sei-gerador-crud` |
| G1 | Seguranca | Arquivo PHP com BOM ou caractere fora da conversao Latin-1 | Corrigir para blob final compativel com `.gitattributes` | `sei-verificacao-pagina` (P3) |
| G2 | Seguranca | `php -l` com erro de sintaxe em qualquer arquivo PHP | Corrigir erro antes de qualquer entrega | `sei-validacao-padrao` |
| G3 | Seguranca | Acao PHP sem `validarLink()` e/ou `validarPermissao()` | Adicionar as chamadas no inicio da acao | `sei-verificacao-pagina` |
| G4 | Seguranca | Link de acao sem `assinarLink()` | Corrigir link para usar `assinarLink()` | `sei-verificacao-pagina` |
| G5 | Seguranca | Uso de `$_REQUEST` ou input nao validado | Substituir por `PaginaSEI::POST/GET` com validacao de tipo | `sei-verificacao-pagina` |
| G6 | Escopo | Mudanca direta em core proibido por `AGENTS.md`, secao `Escopo e Limites de Escrita`, sem autorizacao e proposta documentada | Obter autorizacao e documentar a proposta antes de implementar | Nao aplicavel |
| G7 | Seguranca | XSS: output sem `PaginaSEI::tratarHTML()` | Usar `tratarHTML()` ou equivalente documentado | `sei-verificacao-pagina` |
| G8 | Seguranca | Controlador AJAX/WS sem dispatch seguro e/ou sem autorizacao especifica por acao/servico | Implementar whitelist explicita, regex restritiva para link sem assinatura e validar permissao antes da execucao | `sei-verificacao-controladores` (CI1-CI4) |
| G9 | Seguranca | Operacao de escrita via GET | Usar POST com link assinado | `sei-verificacao-pagina` |
| R1 | Release | Novo DTO, nova tabela, nova entidade CRUD base ou adicao de colunas a DTO existente sem atualizacao do script de instalacao ou upgrade aplicavel | Atualizar o script SEI e, quando houver impacto SIP real, o script SIP correspondente | `sei-gerador-scripts-release`, `sip-gerador-scripts-release` |
| R3 | Release | `getVersao()` em `*Integracao.php` diverge dos scripts SEI/SIP | Sincronizar versao antes do merge | `sei-gerador-scripts-release`, `sip-gerador-scripts-release` |
| R4 | Release | Mudanca com impacto real em recurso, perfil, menu, parametro ou versionamento SIP sem atualizacao do script correspondente | Atualizar o script SIP conforme o impacto confirmado | `sip-gerador-scripts-release` |
| R5 | Release | Nome de tabela/coluna com mais de 26 chars ou indice/FK/sequence com mais de 30 chars | Reduzir: tabelas/colunas <= 26; indices/FK/sequences <= 30 | `sei-verificacao-banco-dados` (DB03) |
| R6 | Release | Script novo criado para lado SEI ou SIP que ja tem script mapeado em `mapa-modulos-scripts.md` | Atualizar o script existente; nunca criar duplicata | `sei-gerador-scripts-release`, `sip-gerador-scripts-release` |
| D1 | Contrato | Novo menu/pagina sem recurso SIP e permissao definidos | Definir recurso `md_<inst/mod>_<acao>` antes de implementar | `sei-menu-pagina` |
| D2 | Contrato | Evento/hook com efeito colateral ambiguo | Documentar efeito esperado e condicoes de disparo | `sei-mod-api-eventos` |
| D3 | Contrato | Operacao API usando classe interna sem justificativa | Substituir por `Entrada*API`/`Saida*API`/`SeiRN` ou documentar excecao | `sei-mod-api-operacoes` |
| D4 | Contrato | Alteracao de indexacao/pesquisa sem declarar momento e reprocessamento | Documentar estrategia de indexacao antes de implementar | `sei-guardrails-modulo` |
| D5 | Contrato | Criterio de aceite ausente antes de uma implementacao | Definir ao menos um cenario de sucesso testavel antes de implementar | Nao aplicavel |

## Escopo de G6

Conforme `AGENTS.md`, secao `Escopo e Limites de Escrita`, G6 nao bloqueia
alteracoes nos seguintes caminhos autorizados:

- `fontes/sei/src/main/php/sei/web/modulos/**`
- `fontes/sei/src/main/php/sei/scripts/**`
- `fontes/sei/src/main/php/sip/scripts/**`
- `docs/dicionario_dados/**`
- `specs/**`
- `.agents/**`

G6 aplica-se a mudanca direta nos seguintes caminhos de core proibido sem
autorizacao:

- `fontes/sei/src/main/php/sei/web/**` fora de `modulos/`
- `fontes/sei/src/main/php/sip/web/**`
- `infra/**`

Mudanca nesse core exige autorizacao e proposta documentada antes de qualquer
patch. Scripts SEI/SIP autorizados, `.agents/**` e `specs/**` nao sao core
proibido para efeito de G6.

## Aplicacao de D5

D5 e gate de implementacao no Fluxo Direto. Ele nao se aplica a code review ou
revisao tecnica pos-implementacao quando nao houver spec. A ausencia de spec
nesse contexto nao produz `BLOCK`.
