# Exemplo de Relatorio Tecnico

Exemplo ficticio de saida da skill `sei-revisao-tecnica`. O caso demonstra
cobertura positiva, um desvio introduzido, passivo preexistente sem agravamento
e a segunda passada obrigatoria. Nenhum requisito funcional e avaliado.

## Contexto tecnico

Diff do modulo `relacionamento-institucional` contra `origin/main`. O delta
altera `restaurante_lista.php` e `rn/MdRiRestauranteRN.php`. O primeiro arquivo
adiciona uma acao; o segundo adiciona o metodo `listarPorCidadeConectado()`.

## Saida

```text
## Escopo tecnico
Entrada: diff
Modo: somente leitura
Base tecnica: origin/main
Arquivos e dimensoes: 2 arquivos; todas as dimensoes tecnicas
Fora do escopo: requisito, especificacao, regra de negocio e produto nao avaliados

## Cobertura e gates
| Gate | Artefatos | Controles/evidencia | Estado |
| sei-verificacao-pagina | restaurante_lista.php | P1 e P3-P10 executados; P2 falhou na linha 42 | BLOCK |
| sei-verificacao-rn | rn/MdRiRestauranteRN.php | T1-T6 e A1-A3 aplicaveis executados; sem desvio no delta | PASS |
| sei-testes-validacao | 2 arquivos PHP | php -l executado nos 2 arquivos, sem erro | PASS |
| sei-verificacao-banco-dados | nenhum DTO, BD ou DDL | sem artefato compativel | NOT_APPLICABLE |
| sei-verificacao-controladores | nenhum controlador no delta | sem artefato compativel | NOT_APPLICABLE |
| sei-verificacao-tarefa | nenhuma tarefa no delta | sem artefato compativel | NOT_APPLICABLE |

## Dimensoes
| Dimensao | Estado | Evidencia ou risco residual |
| Escopo | PASS | 2 arquivos em modulos/**, AGENTS.md Escopo e Limites de Escrita |
| Arquitetura | PASS | camadas preservadas nos 2 arquivos |
| Permissoes | BLOCK | restaurante_lista.php:42, P2/G3/V02; MdRiRestauranteRN.php, A1-A3 aplicaveis sem desvio |
| Transacao | PASS | MdRiRestauranteRN.php:70-106, T1-T6 |
| Controladores | NOT_APPLICABLE | nenhum controlador no delta |
| Entrada/saida | PASS | restaurante_lista.php, P5-P10 executados |
| Seguranca | BLOCK | fluxo alcancavel da acao sem autorizacao, V02 |
| Banco | NOT_APPLICABLE | nenhum DTO, BD ou DDL |
| Release | NOT_APPLICABLE | nenhum artefato ou impacto de release no delta |
| Integracoes | NOT_APPLICABLE | nenhuma API, evento ou chamada externa |
| Qualidade | WARN | duplicacao tecnica descrita abaixo |
| Testes | PASS | php -l executado nos 2 arquivos |

## Achados tecnicos
- [BLOCK][BLOQUEANTE][introduzido] restaurante_lista.php:42 - a acao valida o link, mas nao valida permissao antes da chamada RN. Origem: P2/G3/V02. Ajuste minimo: validar o recurso da acao antes da execucao.
- [WARN][ALTA][introduzido] MdRiRestauranteRN.php:88 - o novo metodo listarPorCidadeConectado() repete a mesma montagem de DTO de listarConectado() na linha 51. Origem: U1. Ajuste minimo: reutilizar o metodo existente.

## Passivo preexistente
- [WARN][preexistente] MdRiRestauranteRN.php:34 - TODO: de tipagem ja existia em origin/main e as linhas nao foram alteradas. Nao houve agravamento.

## Candidatos a tarefas
- [RT-01] Titulo: Avaliar tipagem da RN | Prioridade/severidade: baixa/BAIXA | Estado temporal: preexistente | Evidencia: MdRiRestauranteRN.php:34, TODO: | Risco: manutencao sem contrato de tipos explicito | Acao minima: avaliar tipagem em mudanca separada | Dependencia: nenhuma | Persistencia: nao realizada

## Segunda passada
Executada: sim. A protecao do controlador central nao substitui a permissao por acao, portanto P2 foi mantido. O TODO: foi confirmado na base e reclassificado de incerto para preexistente. Nenhum gate aplicavel ficou sem cobertura.

## Parecer
**bloquear tecnicamente**
```
