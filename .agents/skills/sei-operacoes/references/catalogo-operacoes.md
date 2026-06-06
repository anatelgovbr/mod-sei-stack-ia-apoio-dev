# Catálogo de Operações (SeiRN) do SEI (v5.0 — Cap. 10)

> Fonte: `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_10_operacoes.md`
> Uso: identificar qual operacao oficial usar antes de criar logica propria equivalente.

## Procedimentos e Documentos

| Nome | Descrição | Quando usar |
|---|---|---|
| gerarProcedimento | Gera novo processo com tipo, especificacao, interessados, documentos, relacionados e unidades de envio | Criar processo automaticamente; geracao em lote; processo inicial de fluxo |
| consultarProcedimento | Consulta dados detalhados de processo por id ou protocolo com opcoes de retorno (andamentos, assuntos, interessados, etc.) | Ler dados completos de processo; montar tela de detalhe |
| consultarProcedimentoIndividual | Consulta processo restrito a orgao/tipo/usuario | Consulta individual com restricao de contexto |
| incluirDocumento | Inclui documento em processo existente (tipo, numero, conteudo base64 em blocos) | Gerar documento em processo; upload de arquivo |
| consultarDocumento | Consulta dados detalhados de documento por id ou protocolo | Ler dados de documento; verificar detalhes de assinatura/publicacao |
| bloquearDocumento | Bloqueia documento com motivo | Bloquear documento; suspender acesso |
| cancelarDocumento | Cancela documento com motivo | Invalidar documento; cancelar por erro |
| excluirDocumento | Exclui documento | Remover documento; exclusao a pedido |
| adicionarArquivo | Adiciona arquivo ao repositorio (nome, tamanho, hash, conteudo base64) | Upload de arquivo para documento externo; geracao de Binario |
| adicionarConteudoArquivo | Adiciona conteudo em blocos a um arquivo ja criado | Upload de arquivo grande em chunks de 1Mb |
| excluirProcesso | Exclui processo e documentos asociados | Exclusao definitiva; remocao a pedido |

## Fluxo Processual

### Operacoes com contrato detalhado

| Nome | Descrição | Entrada principal | Saída principal | Sinais de domínio | Quando usar |
|---|---|---|---|---|---|
| enviarProcesso | Envia processo a unidades com opcao de retorno programado e notificacao por email | `EntradaEnviarProcessoAPI` com `IdProcedimento ou ProtocoloProcedimento`, `UnidadesDestino`, `SinManterAbertoUnidade`, `SinRemoverAnotacao`, `SinEnviarEmailNotificacao`, `DataRetornoProgramado`, `DiasRetornoProgramado`, `SinDiasUteisRetornoProgramado` e `SinReabrir` | Sem retorno documentado no catalogo | `fluxo de trabalho`, `tramitacao`, `unidades destino`, `retorno programado`, `reabrir` | Tramitar processo; enviar para outra unidade; modelar fluxo de trabalho entre unidades |
| atribuirProcesso | Atribui processo a usuario dentro da unidade | `EntradaAtribuirProcessoAPI` com `IdProcedimento ou ProtocoloProcedimento`, `IdUsuario` e `SinReabrir` | Sem retorno documentado no catalogo | `atribuicao`, `carga de trabalho`, `responsavel`, `redistribuicao` | Atribuir carga de trabalho; redistribuir processo; definir responsavel |
| concluirProcesso | Conclui processo na unidade atual | `EntradaConcluirProcessoAPI` | Sem retorno documentado no catalogo | `conclusao`, `encerramento`, `unidade atual` | Finalizar tramite; encerrar participacao da unidade |
| reabrirProcesso | Reabre processo na unidade | `EntradaReabrirProcessoAPI` | Sem retorno documentado no catalogo | `reabertura`, `reativacao`, `unidade` | Reativar processo; permitir novo tramite |
| sobrestarProcesso | Sobresta processo com motivo especifico | `EntradaSobrestarProcessoAPI` | Sem retorno documentado no catalogo | `sobrestamento`, `impedimento`, `motivo` | Impedir tramite; suspender andamento |

### Outras operacoes de fluxo

| Nome | Descrição | Quando usar |
|---|---|---|
| bloquearProcesso | Bloqueia processo com motivo | Bloquear processo; restringir acesso |
| desbloquearProcesso | Desbloqueia processo bloqueado | Desbloquear; restaurar acesso |
| removerSobrestamentoProcesso | Remove sobrestamento de processo | Liberar tramite; desatrelhar |
| anexarProcesso | Anexa processo anexado a processo principal | Vincular processo; criar dependencia |
| desanexarProcesso | Desanexa processo com motivo | Desvincular; remover dependencia |
| relacionarProcesso | Cria relacionamento lateral entre processos | Relacionar processos; vinculo lateral |
| removerRelacionamentoProcesso | Remove relacionamento entre processos | Remover vinculo; desatrelhar |

## Blocos

### Operacoes com contrato detalhado

| Nome | Descrição | Entrada principal | Saída principal | Sinais de domínio | Quando usar |
|---|---|---|---|---|---|
| gerarBloco | Cria novo bloco com titulo e usuario responsavel | `EntradaGerarBlocoAPI` com `Tipo`, `Descricao`, `UnidadesDisponibilizacao`, `Documentos ou IdDocumentos` e `SinDisponibilizar` | `IdBloco` | `bloco`, `reuniao`, `assinatura`, `workspace`, `colaboracao`, `disponibilizacao` | Criar bloco de analise; workspace de grupo; organizar colaboracao |
| disponibilizarBloco | Disponibiliza bloco para outras unidades | `EntradaDisponibilizarBlocoAPI` com `IdBloco` | Sem retorno documentado no catalogo | `bloco`, `compartilhamento`, `unidades`, `colaboracao` | Compartilhar bloco; colaboracao inter-unidades |
| incluirDocumentoBloco | Inclui documento em bloco ja existente | `EntradaIncluirDocumentoBlocoAPI` com `IdBloco`, `IdDocumento ou ProtocoloDocumento` e `Anotacao` | Sem retorno documentado no catalogo | `bloco`, `documento`, `anotacao`, `organizacao`, `analise` | Adicionar documento a bloco; organizar para analise |
| incluirProcessoBloco | Inclui processo em bloco | `EntradaIncluirProcessoBlocoAPI` com `IdBloco`, `IdProcedimento ou ProtocoloProcedimento` e `Anotacao` | Sem retorno documentado no catalogo | `bloco`, `processo`, `anotacao`, `agrupamento`, `analise` | Adicionar processo a bloco; agrupar para analise |

### Outras operacoes de bloco

| Nome | Descrição | Quando usar |
|---|---|---|
| consultarBloco | Consulta dados detalhados de bloco | Ver detalhes do bloco; listar documentos |
| concluirBloco | Conclui bloco disponível | Finalizar bloco; encerrar colaboracao |
| reabrirBloco | Reabre bloco ja concluido | Reabrir para nova colaboracao |
| devolverBloco | Devolve bloco ao criador | Devolver bloco; transferencia de controle |
| cancelarDisponibilizacaoBloco | Cancela disponibilizacao de bloco | Revogar acesso; remover compartilhamento |
| excluirBloco | Exclui bloco | Remover bloco; exclusao definitiva |
| retirarDocumentoBloco | Retira documento de bloco | Remover documento; desorganizar |
| retirarProcessoBloco | Retira processo de bloco | Remover processo; desagrupar |

## Histórico e Anotações

| Nome | Descrição | Quando usar |
|---|---|---|
| lancarAndamento | Lanca andamento em processo (tarefa, tarefa modulo, atributos com @VAR@) | Registrar historico; criar registro de atividade; notificar |
| listarAndamentos | Lista andamentos de processo com filtros (andamentos, tarefas, tarefas modulo) | Consultar historico; exibir timeline de atividade |
| listarAndamentosMarcadores | Lista andamentos de processo filtrados por marcadores | Filtrar historico por marcador; busca direcionada |
| registrarAnotacao | Registra anotacao em procedimento | Adicionar nota interna; observacao de trabalho |
| registrarOuvidoria | Registra registro de ouvidoria com atributos | Criar registro de ouvidoria; demanda externa |

## Prazos e Marcadores

### Operacoes com contrato detalhado

| Nome | Descrição | Entrada principal | Saída principal | Sinais de domínio | Quando usar |
|---|---|---|---|---|---|
| definirControlePrazo | Define prazo em processo (data exata ou dias uteis/corridos) | Conjunto de `EntradaDefinirControlePrazoAPI` com `IdProcedimento ou ProtocoloProcedimento`, `DataPrazo`, `Dias` e `SinDiasUteis` | Sem retorno documentado no catalogo | `prazo`, `controle de prazo`, `dias uteis`, `vencimento`, `agenda` | Criar controle de prazo; notificacao de vencimento; planejar acompanhamento |
| definirMarcador | Define marcador de unidade em processo | Conjunto de `DefinicaoMarcadorAPI` com `IdProcedimento ou ProtocoloProcedimento`, `IdMarcador` e `Texto` | Sem retorno documentado no catalogo | `marcador`, `classificacao`, `organizacao`, `filtro`, `texto de marcador` | Marcar processo; categorizar para filtro; organizar trabalho |

### Outras operacoes de prazo e marcador

| Nome | Descrição | Quando usar |
|---|---|---|
| concluirControlePrazo | Conclui controle de prazo de processo | Finalizar prazo; marcar como cumprido |
| removerControlePrazo | Remove controle de prazo de processo | Cancelar prazo; remover notificacao |

## Publicação

| Nome | Descrição | Quando usar |
|---|---|---|
| agendarPublicacao | Agenda publicacao de documento em veiculo (interno, externo ou modulo) | Publicar documento; agendar veiculo oficial |
| alterarPublicacao | Altera dados de publicacao agendada (veiculo, tipo, numero, data) | Corrigir publicacao; atualizar dados |
| consultarPublicacao | Consulta dados de publicacao (andamento, assinaturas) | Verificar status de publicacao |
| cancelarAgendamentoPublicacao | Cancela agendamento de publicacao | Cancelar publicacao; remover agendamento |

## Catálogos (Consultas Auxiliares)

| Nome | Descrição | Quando usar |
|---|---|---|
| listarTiposProcedimento | Lista tipos de processo cadastrados | Popular combo; filtrar por tipo |
| listarSeries | Lista tipos de documento (series) cadastradas | Popular combo de tipo de documento |
| listarUnidades | Lista unidades organizacionais | Popular combo de unidades; filtrar por contexto |
| listarUsuarios | Lista usuarios com filtro opcional por unidade | Popular combo de usuarios; atribuicao |
| listarCargos | Lista cargos com filtro opcional por id | Popular combo de cargo |
| listarCidades | Lista cidades com filtro por pais e estado | Popular combo de cidade; endereco |
| listarEstados | Lista estados (sem filtro) | Popular combo de estado; endereco |
| listarPaises | Lista paises | Popular combo de pais; endereco |
| listarHipotesesLegais | Lista hipoteses legais cadastradas | Popular combo de hipotese legal; classificacao |
| listarFeriados | Lista feriados cadastrados | Calculo de prazo; dias uteis |
| listarExtensoesPermitidas | Lista extensoes de arquivo permitidas para upload | Validar tipo de arquivo; upload |
| listarMarcadoresUnidade | Lista marcadores da unidade | Popular combo de marcador; associar |
| listarTiposConferencia | Lista tipos de conferencia | Popular combo de conferencia |
| listarContatos | Lista contatos com filtros (id, tipo, sigla, nome, cpf, cnpj, matricula) e paginacao | Busca de pessoa; autocomplete; populacao |
| listarAndamentosMarcadores | Lista andamentos filtrados por marcadores | Busca direcionada no historico |

## Email

| Nome | Descrição | Quando usar |
|---|---|---|
| enviarEmail | Envia email a partir de template com parametros (destinatarios, assunto, corpo, campos) | Notificacao automatica; alerta a unidade |

## Notas sobre ambiguidades do manual

1. `ConfirmarDisponibilizacaoPublicacao` aparece com "C" maiusculo no capitulo 10, mas pode ser `confirmarDisponibilizacaoPublicacao` (minusculo) no codigo. Verificar no fonte do SEI antes de usar.

2. `definirControlePrazo` e `definirMarcador` usam cabecalho "Saida" nos exemplos, mas os campos correspondem a entrada. Tratar como operacao de escrita (entrada).

3. `consultarPublicacao` retorna `SaidaConsultarPublicacaoAPI` segundo o catalogo da `sei-api` (cap 8), nao `PublicacaoAPI` como mencionado na secao de operacao.

4. `RetornoInclusaoDocumentoAPI` aparece em `SaidaGerarProcedimentoAPI` mas nao tem definicao propria. Pode ser subclasse interna nao exposta como API publica.

## Aviso

**Nao e recomendado usar classes internas do sistema alem das classes API documentadas no capitulo 8 e operacoes listadas acima.**
Antes de criar logica propria equivalente a uma operacao existente, usar `sei-api` para confirmar que nao ha contrato oficial.
