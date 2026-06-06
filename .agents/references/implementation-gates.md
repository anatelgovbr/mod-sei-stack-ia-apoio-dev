# Pontos de Bloqueio de Implementacao — SEI SDD

**Fonte autoritativa para gates de bloqueio da stack.**

---

## Gates de CRUD Generator

Aplicam-se quando o desenvolvedor optar por usar `sei-gerador-crud`,
independente do fluxo. Se o desenvolvedor optar por implementacao manual, usar
os demais gates de seguranca, contrato, release e testes aplicaveis.

| # | Condicao de Bloqueio | Condicao de Desbloqueio |
| - | -------------------- | ----------------------- |
| C1 | Gerador escolhido para novo CRUD (nova entidade/tabela/`*DTO`/`*RN`/`*BD`) sem contrato JSON | Obter confirmacao do contrato JSON com o desenvolvedor antes de gerar |
| C2 | Contrato JSON com campos obrigatorios ausentes (`entidade`, `colunas`, `sin_ativo`, `relacionamentos`) | Completar todos os campos obrigatorios com confirmacao do desenvolvedor |
| C3 | Escrita manual de `DTO`, `RN`, `BD`, `*_lista.php` ou `*_cadastro.php` antes do contrato confirmado | Aguardar confirmacao do contrato; usar gerador |
| C4 | `php -l` com erro nos arquivos gerados | Corrigir erro de sintaxe antes de continuar |

---

## Gates de Seguranca e Padroes SEI

Aplicam-se em qualquer trabalho no repositorio (Fluxo Direto ou Spec Kit).

Para validacao automatizada, usar as skills de gate:
- `sei-verificacao-pagina` (P1-P10) para seguranca de pagina
- `sei-verificacao-rn` (T1-T5) para transacoes RN
- `sei-verificacao-banco-dados` (R1-R15) para modelagem de dados
- `sei-verificacao-tarefa` (K1-K7) para IDs de tarefa
- `sei-verificacao-controladores` (CI1-CI4) para `processarControladorAjax*`, `processarControladorWebServices` e `tratarLinkSemAssinatura`
- `sei-testes-validacao` (php -l) para validacao de sintaxe

| # | Condicao de Bloqueio | Condicao de Desbloqueio | Skill associada |
| - | -------------------- | ----------------------- | --------------- |
| G1 | Arquivo PHP com BOM ou caractere fora da conversao Latin-1 | Corrigir para worktree compativel com a conversao de `.gitattributes` | `sei-verificacao-pagina` (P3) |

| G2 | `php -l` com erro de sintaxe em qualquer arquivo PHP | Corrigir erro antes de qualquer entrega | `sei-testes-validacao` |

| G3 | Acao PHP sem `validarLink()` e/ou `validarPermissao()` | Adicionar as chamadas no inicio da acao | `sei-verificacao-pagina` |

| G4 | Link de acao sem `assinarLink()` | Corrigir link para usar `assinarLink()` | `sei-verificacao-pagina` |

| G5 | Uso de `$_REQUEST` ou input nao validado | Substituir por `PaginaSEI::POST/GET` com validacao de tipo | `sei-verificacao-pagina` |

| G7 | XSS: output sem `PaginaSEI::tratarHTML()` | Usar `tratarHTML()` ou equivalente documentado no artefato | `sei-verificacao-pagina` |

| G8 | Controlador AJAX/WS sem dispatch seguro | Implementar whitelist explicita de acao/servico e regex restritiva para link sem assinatura | `sei-verificacao-controladores` (CI1-CI4) |

| G9 | Operacao de escrita via GET | Usar POST com link assinado | `sei-verificacao-pagina` |

| G6 | Mudanca em `sei/` ou `sip/` fora de `modulos/**` sem proposta | Documentar via skill `escrever-adr` antes de implementar | - |

| R1 | Mudanca em BD (nova tabela, coluna, indice) sem script de instalacao/upgrade | Criar script SEI e/ou SIP correspondente | `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` |

| R3 | `getVersao()` em `*Integracao.php` diverge dos scripts SEI/SIP | Sincronizar versao antes do merge | `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` |

| R4 | Novos recursos SIP criados sem script SIP correspondente | Adicionar script SIP com registro de recursos | `sip-gerador-scripts-release` |

| R5 | Nome de tabela ou coluna com mais de 26 chars, ou nome de indice/FK/sequence com mais de 30 chars | Reduzir para o limite correto: tabelas/colunas ≤ 26; indices/FK/sequences ≤ 30 (cap Oracle) | `sei-verificacao-banco-dados` (R3) |

| R6 | Script novo criado para modulo que ja tem script existente mapeado em `mapa-modulos-scripts.md` | Atualizar script existente — nunca criar duplicata | `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` |

---

## Gates de Contrato (demandas sem Spec Kit)

Aplicam-se no Fluxo Direto quando a demanda envolve tipo reconhecido pela matriz de roteamento.

| # | Condicao de Bloqueio | Condicao de Desbloqueio |
| - | -------------------- | ----------------------- |
| D1 | Novo menu/pagina sem recurso SIP e permissao definidos | Definir recurso `md_<inst/mod>_<acao>` antes de implementar |
| D2 | Evento/hook com efeito colateral ambiguo (sem especificacao do efeito) | Documentar efeito esperado e condicoes de disparo |
| D3 | Operacao API usando classe interna (nao-API) sem justificativa | Substituir por `Entrada*API`/`Saida*API`/`SeiRN` ou documentar excecao |
| D4 | Alteracao de indexacao/pesquisa sem declarar momento e reprocessamento | Documentar estrategia de indexacao antes de implementar |
| D5 | Criterio de aceite ausente para qualquer demanda | Definir ao menos um cenario de sucesso testavel antes de implementar |

Para a lista completa de contratos por tipo de demanda, ver:
`.agents/references/skill-routing-and-contracts.md`

Para o checklist de validacao tecnica de entrega, ver:
`.specify/templates/checklist-sei-template.md`
