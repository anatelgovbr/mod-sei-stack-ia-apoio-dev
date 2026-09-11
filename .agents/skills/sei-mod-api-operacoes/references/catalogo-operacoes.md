# Catálogo de Operações (SeiRN) do SEI (v5.0 — Cap. 10)

> Fonte: `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_10_operacoes.md`
> Uso: identificar qual operacao oficial usar antes de criar logica propria equivalente.

Se a duvida ainda estiver ambigua entre API, evento e operacao, usar primeiro
`sei-direcionador-integracao`. Se a operacao ja estiver escolhida e faltar
apenas o contrato de entrada/saida, complementar com `sei-mod-api-classes`.

## Procedimentos e Documentos

| Nome | Descrição | Quando usar |
|---|---|---|
| gerarProcedimento | Gera novo processo com tipo, especificacao, interessados, documentos, relacionados e unidades de envio | Criar processo automaticamente; geracao em lote; processo inicial de fluxo |
| consultarProcedimento | Consulta dados detalhados de processo por id ou protocolo com opcoes de retorno (andamentos, assuntos, interessados, etc.) | Ler dados completos de processo; montar tela de detalhe |
| consultarProcedimentoIndividual | Consulta processo restrito a orgao/tipo/usuario | Consulta individual com restricao de contexto |
| incluirDocumento | Inclui documento em processo existente (tipo, numero, conteudo base64 em blocos) | Gerar documento em processo; upload de arquivo |
| consultarDocumento | Consulta dados detalhados de documento por id ou protocolo | Ler dados de documento; verificar detalhes de assinatura/publicacao |
| bloquearDocumento | Bloqueia documento, entrada `EntradaBloquearDocumentoAPI` com `IdDocumento` ou `ProtocoloDocumento`, sem campo de motivo | Bloquear documento; suspender acesso |
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
| concluirProcesso | Conclui processo na unidade atual | `EntradaConcluirProcessoAPI` com `IdProcedimento` ou `ProtocoloProcedimento`, sem campo de unidade | Sem retorno documentado no catalogo | `conclusao`, `encerramento`, `unidade atual` | Finalizar tramite; encerrar participacao da unidade |
| reabrirProcesso | Reabre processo na unidade | `EntradaReabrirProcessoAPI` com `IdProcedimento` ou `ProtocoloProcedimento`, sem campo de unidade | Sem retorno documentado no catalogo | `reabertura`, `reativacao`, `unidade` | Reativar processo; permitir novo tramite |
| sobrestarProcesso | Sobresta processo com motivo especifico | `EntradaSobrestarProcessoAPI` | Sem retorno documentado no catalogo | `sobrestamento`, `impedimento`, `motivo` | Impedir tramite; suspender andamento |

### Outras operacoes de fluxo

| Nome | Descrição | Quando usar |
|---|---|---|
| bloquearProcesso | Bloqueia processo, entrada `EntradaBloquearProcessoAPI` com `IdProcedimento` ou `ProtocoloProcedimento`, sem campo de motivo | Bloquear processo; restringir acesso |
| desbloquearProcesso | Desbloqueia processo bloqueado | Desbloquear; restaurar acesso |
| removerSobrestamentoProcesso | Remove sobrestamento de processo | Liberar tramite; desatrelhar |
| anexarProcesso | Anexa processo anexado a processo principal | Vincular processo; criar dependencia |
| desanexarProcesso | Desanexa processo com motivo | Desvincular; remover dependencia |
| relacionarProcesso | Relaciona exatamente dois processos, `IdProcedimento1` ou `ProtocoloProcedimento1` e `IdProcedimento2` ou `ProtocoloProcedimento2` | Relacionar processos; vinculo lateral |
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
| listarUsuarios | Lista usuarios, entrada `EntradaListarUsuariosAPI` com `IdUsuario` | Popular combo de usuarios; atribuicao |
| listarCargos | Lista cargos com filtro opcional por id | Popular combo de cargo |
| listarCidades | Lista cidades com filtro por pais e estado | Popular combo de cidade; endereco |
| listarEstados | Lista estados, entrada `EntradaListarEstadosAPI` com `IdPais` | Popular combo de estado; endereco |
| listarPaises | Lista paises | Popular combo de pais; endereco |
| listarHipotesesLegais | Lista hipoteses legais, entrada `EntradaListarHipotesesLegaisAPI` com `NivelAcesso` (1 Restrito, 2 Sigiloso) | Popular combo de hipotese legal; classificacao |
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

3. `consultarPublicacao` retorna `SaidaConsultarPublicacaoAPI` segundo o catalogo da `sei-mod-api-classes` (cap 8), nao `PublicacaoAPI` como mencionado na secao de operacao.

4. `RetornoInclusaoDocumentoAPI` aparece em `SaidaGerarProcedimentoAPI` mas nao tem definicao propria. Pode ser subclasse interna nao exposta como API publica.

## Aviso

**Nao e recomendado usar classes internas do sistema alem das classes API documentadas no capitulo 8 e operacoes listadas acima.**
Antes de criar logica propria equivalente a uma operacao existente, confirmar
primeiro neste catalogo se a operacao oficial ja existe. Se a duvida restante
for apenas sobre o contrato `Entrada*API`/`Saida*API`, complementar com
`sei-mod-api-classes`.

## Contratos completos das operacoes

| Operacao | Entrada | Saida |
|---|---|---|
| `adicionarArquivo` | Instância do objeto EntradaAdicionarArquivoAPI preenchida com: Nome Tamanho Hash Conteudo | Retornar o identificador do arquivo criado no repositório. |
| `adicionarConteudoArquivo` | Instância do objeto EntradaAdicionarConteudoArquivoAPI preenchida com: IdArquivo Conteudo; Observação; Ver exemplo em adicionarArquivo. | sem saida documentada |
| `agendarPublicacao` | Instância do objeto EntradaAgendarPublicacaoAPI preenchida com: IdDocumento ou ProtocoloDocumento StaMotivo IdVeiculoPublicacao DataDisponibilizacao Resumo ImprensaNacional; Observação; Para identificação é necessário informar apenas um dos atributos IdDocumento ou ProtocoloDocumento. O atributo ImprensaNacional é opcional. | sem saida documentada |
| `alterarPublicacao` | Instância do objeto EntradaAlterarPublicacaoAPI preenchida com: IdPublicacao ou IdDocumento ou ProtocoloDocumento StaMotivo IdVeiculoPublicacao DataDisponibilizacao Resumo ImprensaNacional; Observação; Para identificação é necessário informar apenas um dos atributos IdPublicacao, IdDocumento ou ProtocoloDocumento. Os demais atributos são opcionais e somente os informados serão alterados se o estado da publicação permitir. | sem saida documentada |
| `anexarProcesso` | Instância do objeto EntradaAnexarProcessoAPI preenchida com: IdProcedimentoPrincipal ou ProtocoloProcedimentoPrincipal IdProcedimentoAnexado ou ProtocoloProcedimentoAnexado | sem saida documentada |
| `atribuirProcesso` | Instância do objeto EntradaAtribuirProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento IdUsuario SinReabrir | sem saida documentada |
| `atualizarContatos` | Conjunto de Instâncias do objeto ContatoAPI preenchidas com: StaOperacao IdContato IdTipoContato Sigla Nome NomeSocial StaNatureza IdContatoAssociado SinEnderecoAssociado Endereco Complemento Bairro IdCidade IdEstado IdPais Cep StaGenero IdCargo Cpf Cnpj Rg OrgaoExpedidor Matricula MatriculaOab TelefoneFixo TelefoneCelular DataNascimento Email SitioInternet Observação NumeroPassaporte IdPaisPassaporte SinAtivo | sem saida documentada |
| `bloquearDocumento` | Instância do objeto EntradaBloquearDocumentoAPI preenchida com: IdDocumento ou ProtocoloDocumento | sem saida documentada |
| `bloquearProcesso` | Instância do objeto EntradaBloquearProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `cancelarAgendamentoPublicacao` | Instância do objeto EntradaCancelarAgendamentoPublicacaoAPI preenchida com pelo menos um dos atributos: IdPublicacao ou IdDocumento ou ProtocoloDocumento | sem saida documentada |
| `cancelarDisponibilizacaoBloco` | Instância do objeto EntradaCancelarDisponibilizacaoBlocoAPI preenchida com: IdBloco | sem saida documentada |
| `cancelarDocumento` | Instância do objeto EntradaCancelarDocumentoAPI preenchida com: IdDocumento ou ProtocoloDocumento Motivo | sem saida documentada |
| `concluirBloco` | Instância do objeto EntradaConcluirBlocoAPI preenchida com: IdBloco | sem saida documentada |
| `concluirControlePrazo` | Instâncias do objeto EntradaConcluirControlePrazoAPI preenchidas com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `concluirProcesso` | Instância do objeto EntradaConcluirProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `ConfirmarDisponibilizacaoPublicacao` | Instância do objeto EntradaConfirmarDisponibilizacaoPublicacaoAPI preenchida com: IdVeiculoDisponibilizacao DataDisponibilizacao DataPublicacao Numero IdDocumentos | sem saida documentada |
| `consultarBloco` | Instância do objeto EntradaConsultarBlocoAPI preenchida com: IdBloco SinRetornarProtocolos | Instância do objeto SaidaConsultarBlocoAPI preenchida com: IdBloco Descricao Tipo Estado Unidade (UnidadeAPI) IdUnidade Sigla Descricao Usuario (UsuarioAPI) IdUsuario Sigla Nome SinPrioridade SinRevisao UsuarioAtribuicao (UsuarioAPI) IdUsuario Sigla Nome UnidadesDisponibilizacao (array: UnidadeAPI) IdUnidade Sigla Descricao Protocolos (array: ProtocoloBlocoAPI) ProtocoloFormatado Identificacao Assinaturas (array: AssinaturaAPI) Nome CargoFuncao DataHora IdUsuario IdOrigem IdOrgao Sigla |
| `consultarDocumento` | Instância do objeto EntradaConsultarDocumentoAPI preenchida com: IdDocumento ou ProtocoloDocumento SinRetornarAndamentoGeracao SinRetornarAssinaturas SinRetornarPublicacao SinRetornarCampos SinRetornarBlocos | Instância do objeto SaidaConsultarDocumentoAPI preenchida com: IdProcedimento ProcedimentoFormatado IdDocumento DocumentoFormatado Serie IdSerie Nome Numero NomeArvore DinValor Data UnidadeElaboradora (UnidadeAPI) IdUnidade Sigla Descricao AndamentoGeracao (array:AndamentoAPI) Descricao DataHora Usuario (UsuarioAPI) IdUsuario Sigla Nome Unidade (UnidadeAPI) IdUnidade Sigla Descricao Assinaturas (array:AssinaturaAPI) Nome CargoFuncao DataHora IdUsuario IdOrigem IdOrgao Sigla Publicacao (PublicacaoAPI) IdPublicacao IdDocumento StaMotivo Resumo IdVeiculoPublicacao NomeVeiculo StaTipoVeiculo Numero DataDisponibilizacao DataPublicacao Estado ImprensaNacional (PublicacaoImprensaNacionalAPI) IdVeiculo SiglaVeiculo DescricaoVeiculo Pagina IdSecao Secao Data Campos (CampoAPI) Nome Valor NivelAcessoLocal 0=Público 1=Restrito 2=Sigiloso NivelAcessoGlobal 0=Público 1=Restrito 2=Sigiloso Blocos LinkAcesso (link não assinado para montar a árvore de processo posicionando no documento) |
| `consultarProcedimento` | Instância do objeto EntradaConsultarProcedimentoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento SinRetornarAssuntos SinRetornarInteressados SinRetornarObervacoes SinRetornarAndamentoGeracao SinRetornarAndamentoConclusao SinRetornarUltimoAndamento SinRetornarUnidadesProcedimentoAberto SinRetornarProcedimentosRelacionados SinRetornarProcedimentosAnexados | Instância do objeto SaidaConsultarProcedimentoAPI preenchida com: IdProcedimento ProcedimentoFormatado Especificacao DataAutuacao TipoProcedimento IdTipoProcedimento Nome TipoPrioridade IdTipoPrioridade Nome Assuntos (array:AssuntoAPI) CodigoEstruturado Descricao Interessados (array:InteressadoAPI) Sigla Nome Observacoes (array:ObservacaoAPI) Descricao Unidade (UnidadeAPI) IdUnidade Sigla Descricao AndamentoGeracao (array:AndamentoAPI) Descricao DataHora Usuario (UsuarioAPI) IdUsuario Sigla Nome Unidade (UnidadeAPI) IdUnidade Sigla Descricao AndamentoConclusao (array:AndamentoAPI) Descricao DataHora Usuario (UsuarioAPI) IdUsuario Sigla Nome Unidade (UnidadeAPI) IdUnidade Sigla Descricao UltimoAndamento (array:AndamentoAPI) Descricao DataHora Usuario (UsuarioAPI) IdUsuario Sigla Nome Unidade (UnidadeAPI) IdUnidade Sigla Descricao UnidadesProcedimentoAberto (array:UnidadeProcedimentoAbertoAPI) Unidade (UnidadeAPI) IdUnidade Sigla Descricao UsuarioAtribuicao (UsuarioAPI) IdUsuario Sigla Nome ProcedimentosRelacionados (array:ProcedimentoResumidoAPI) IdProcedimento ProcedimentoFormatado TipoProcedimento IdTipoProcedimento Nome ProcedimentosAnexados (array:ProcedimentoResumidoAPI) IdProcedimento ProcedimentoFormatado TipoProcedimento IdTipoProcedimento Nome NivelAcessoLocal 0=Público 1=Restrito 2=Sigiloso NivelAcessoGlobal 0=Público 1=Restrito 2=Sigiloso LinkAcesso (link não assinado para montar a árvore de processo) |
| `consultarProcedimentoIndividual` | Instância do objeto EntradaConsultarProcedimentoIndividualAPI preenchida com: IdOrgaoProcedimento IdTipoProcedimento IdOrgaoUsuario SiglaUsuario | Instância do objeto ProcedimentoResumidoAPI preenchida com: IdProcedimento ProcedimentoFormatado TipoProcedimento IdTipoProcedimento Nome |
| `consultarPublicacao` | Instância do objeto EntradaConsultarPublicacaoAPI: IdPublicacao ou IdDocumento ou ProtocoloDocumento SinRetornarAndamento SinRetornarAssinaturas | Instância do objeto PublicacaoAPI preenchida com: IdPublicacao IdDocumento StaMotivo Resumo IdVeiculoPublicacao NomeVeiculo StaTipoVeiculo Numero DataDisponibilizacao DataPublicacao Estado ImprensaNacional (PublicacaoImprensaNacionalAPI) IdVeiculo SiglaVeiculo DescricaoVeiculo Pagina IdSecao Secao Data |
| `definirControlePrazo` | sem entrada documentada | Conjunto de Instâncias do objeto EntradaDefinirControlePrazoAPI preenchidas com: IdProcedimento ou ProtocoloProcedimento DataPrazo Dias SinDiasUteis |
| `definirMarcador` | sem entrada documentada | Conjunto de Instâncias do objeto DefinicaoMarcadorAPI preenchidas com: IdProcedimento ou ProtocoloProcedimento IdMarcador Texto |
| `desanexarProcesso` | Instância do objeto EntradaDesanexarProcessoAPI preenchida com: IdProcedimentoPrincipal ou ProtocoloProcedimentoPrincipal IdProcedimentoAnexado ou ProtocoloProcedimentoAnexado Motivo | sem saida documentada |
| `desbloquearProcesso` | Instância do objeto EntradaBloquearProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `devolverBloco` | Instância do objeto EntradaDevolverBlocoAPI preenchida com: IdBloco | sem saida documentada |
| `disponibilizarBloco` | Instância do objeto EntradaDisponibilizarBlocoAPI preenchida com: IdBloco | sem saida documentada |
| `enviarEmail` | Instância do objeto EntradaEnviarEmailAPI preenchida com: IdProcedimento ou ProtocoloProcedimento De Para CCO Assunto Mensagem NivelAcesso Opcional 0 = Público (valor padrão) 1 = Restrito IdHipoteseLegal Opcional, Identificador interno da hipótese legal associada IdDocumentos Arquivos | Instância do objeto SaidaEnviarEmailAPI preenchida com: IdDocumento DocumentoFormatado LinkAcesso |
| `enviarProcesso` | Instância do objeto EntradaEnviarProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento UnidadesDestino SinManterAbertoUnidade (valor padrão N) SinRemoverAnotacao (valor padrão N) SinEnviarEmailNotificacao (valor padrão N) DataRetornoProgramado (valor padrão nulo) DiasRetornoProgramado (valor padrão nulo) SinDiasUteisRetornoProgramado (valor padrão N) SinReabrir (valor padrão N) | sem saida documentada |
| `excluirBloco` | Instância do objeto EntradaExcluirBlocoAPI preenchida com: IdBloco | sem saida documentada |
| `excluirDocumento` | Instância do objeto EntradaExcluirDocumentoAPI preenchida com: IdDocumento ou ProtocoloDocumento | sem saida documentada |
| `excluirProcesso` | Instância do objeto EntradaExcluirProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `gerarBloco` | Instância do objeto EntradaGerarBlocoAPI preenchida com: Tipo A = Assinatura R = Reunião I = Interno Descricao UnidadesDisponibilizacao Documentos ou IdDocumentos SinDisponibilizar | Retorna o ID do bloco gerado. |
| `gerarProcedimento` | Instância do objeto EntradaGerarProcedimentoAPI preenchida com: Procedimento (ProcedimentoAPI) IdTipoProcedimento NumeroProtocolo e DataAutuacao (opcionais) Especificacao Assuntos (array:AssuntoAPI preenchido com CodigoEstruturado, também adicionará automaticamente os assuntos sugeridos para o tipo de processo), Interessados (array:InteressadoAPI), Observacao NivelAcesso (se não informado assumirá o nível padrão especificado para o tipo de processo) IdHipoteseLegal Documentos - array:DocumentoAPI Tipo IdSerie Numero Data Descricao IdTipoConferencia SinArquivamento Remetente (RemetenteAPI) Interessados (array:InteressadoAPI) Destinatarios (array:DestinatarioAPI) Observacao NivelAcesso (se não informado assumirá o nível padrão especificado para o tipo de processo) IdHipoteseLegal NomeArquivo (obrigatório para documentos externos) IdArquivo ou Conteudo (Base64) ou ConteudoMTOM (Binário) Campos (array:CampoAPI preenchidos com Nome/Valor, somente para formulários) ProcedimentosRelacionados - array com os IDs dos processos UnidadesEnvio - array com os IDs das unidades SinManterAbertoUnidade SinEnviarEmailNotificacao DataRetornoProgramado DiasRetornoProgramado SinDiasUteisRetornoProgramado IdMarcador TextoMarcador DataControlePrazo DiasControlePrazo SinDiasUteisControlePrazo | Instância do objeto SaidaGerarProcedimentoAPI preenchida com: IdProcedimento ProcedimentoFormatado LinkAcesso (link não assinado para montar a árvore de processo) RetornoInclusaoDocumentos - array:SaidaIncluirDocumentoAPI IdDocumento DocumentoFormatado LinkAcesso (link não assinado para montar a árvore de processo posicionando no documento) |
| `incluirDocumento` | Instância do objeto DocumentoAPI preenchida com: Tipo IdProcedimento ou ProtocoloProcedimento IdSerie Numero NomeArvore DinValor Data Descricao IdTipoConferencia SinArquivamento Remetente (RemetenteAPI) Interessados (array:InteressadoAPI) Destinatarios (array:DestinatarioAPI) Observacao NivelAcesso (se não informado assumirá o nível padrão especificado para o tipo de processo) IdHipoteseLegal NomeArquivo (obrigatório para documentos externos) IdArquivo ou Conteudo (Base64) ou ConteudoMTOM (Binário) Campos (array:CampoAPI preenchidos com Nome/Valor, somente para formulários) SinBloqueado (valor padrão N, se informado com S então não será possível alterar o conteúdo) | Instância do objeto SaidaIncluirDocumentoAPI preenchida com: IdDocumento DocumentoFormatado LinkAcesso (link não assinado para montar a árvore de processo posicionando no documento) |
| `incluirDocumentoBloco` | Instância do objeto EntradaIncluirDocumentoBlocoAPI preenchida com: IdBloco IdDocumento ou ProtocoloDocumento Anotacao | sem saida documentada |
| `incluirProcessoBloco` | Instância do objeto EntradaIncluirProcessoBlocoAPI preenchida com: IdBloco IdProcedimento ou ProtocoloProcedimento Anotacao | sem saida documentada |
| `lancarAndamento` | Instância do objeto EntradaLancarAndamentoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento IdTarefa ou IdTarefaModulo Atributos (array:AtributoAndamentoAPI) Nome Valor IdOrigem | Instância do objeto AndamentoAPI preenchida com: IdAndamento IdTarefa IdTarefaModulo Descricao DataHora Usuario (UsuarioAPI) IdUsuario Sigla Nome Unidade (UnidadeAPI) IdUnidade Sigla Descricao Atributos (array: AtributoAndamentoAPI) Nome Valor IdOrigem |
| `listarAndamentos` | Instância do objeto EntradaListarAndamentosAPI preenchida com: IdProcedimento ou ProtocoloProcedimento SinRetornarAtributos Andamentos Tarefas TarefasModulos | Lista de instâncias do objeto AndamentoAPI preenchidas com: IdAndamento IdTarefa IdTarefaModulo Descricao DataHora Usuario (UsuarioAPI) IdUsuario Sigla Nome Unidade (UnidadeAPI) IdUnidade Sigla Descricao Atributos (array: AtributoAndamentoAPI) Nome Valor IdOrigem |
| `listarAndamentosMarcadores` | Conjunto de Instâncias do objeto EntradaListarAndamentosMarcadoresAPI preenchidas com: IdProcedimento ou ProtocoloProcedimento Marcadores | Conjunto de Instâncias do objeto AndamentoMarcadorAPI preenchidas com: IdAndamentoMarcador Texto DataHora Usuario (UsuarioAPI) IdUsuario Sigla Nome Marcador (MarcadorAPI) IdMarcador Nome Icone SinAtivo DataHora |
| `listarCargos` | Instância do objeto EntradaListarCargosAPI preenchida com: IdCargo | Conjunto de Instâncias do objeto CargoAPI preenchidas com: IdCargo ExpressaoCargo ExpressaoTratamento ExpressaoVocativo |
| `listarCidades` | Conjunto de Instâncias do objeto EntradaListarCidadesAPI preenchidas com: IdPais IdEstado | Conjunto de Instâncias do objeto EstadoAPI preenchidas com: IdCidade IdEstado IdPais Nome CodigoIbge SinCapital Latitude Longitude |
| `listarContatos` | Instância do objeto EntradaListarContatosAPI preenchidas com: IdContatos IdTipoContato PaginaRegistros (opcional 1 a 1000 com valor padrão 1) PaginaAtual (opcional começando em 1) Sigla Nome Cpf Cnpj Matricula | Conjunto de Instâncias do objeto ContatoAPI preenchidas com: IdContato IdTipoContato NomeTipoContato Sigla Nome NomeSocial StaNatureza IdContatoAssociado NomeContatoAssociado SinEnderecoAssociado CnpjAssociado Endereco Complemento Bairro IdCidade NomeCidade IdEstado SiglaEstado IdPais NomePais Cep StaGenero IdCargo ExpressaoCargo ExpressaoTratamento ExpressaoVocativo Cpf Cnpj Rg OrgaoExpedidor Matricula MatriculaOab TelefoneFixo TelefoneCelular DataNascimento Email SitioInternet Observação NumeroPassaporte IdPaisPassaporte NomePaisPassaporte SinAtivo |
| `listarEstados` | Conjunto de Instâncias do objeto EntradaListarEstadosAPI preenchidas com: IdPais | Conjunto de Instâncias do objeto EstadoAPI preenchidas com: IdEstado IdPais Sigla Nome CodigoIbge |
| `listarExtensoesPermitidas` | Conjunto de Instâncias do objeto EntradaListarExtensoesPermitidasAPI preenchidas com: IdArquivoExtensao | Conjunto de Instâncias do objeto ArquivoExtensaoAPI preenchidas com: IdArquivoExtensao Extensao Descricao |
| `listarFeriados` | Instâncias de EntradaListarFeriadosAPI preenchida com: IdOrgao DataInicial DataFinal | Conjunto de Instâncias do objeto FeriadoAPI preenchidas com: Data Descricao |
| `listarHipotesesLegais` | Conjunto de Instâncias do objeto EntradaListarHipotesesLegaisAPI preenchidas com: NivelAcesso 1 = Restrito 2 = Sigiloso | Conjunto de Instâncias do objeto HipoteseLegalAPI preenchidas com: IdHipoteseLegal Nome BaseLegal NivelAcesso |
| `listarMarcadoresUnidade` | sem entrada documentada | Conjunto de Instâncias do objeto MarcadorAPI preenchidas com: IdMarcador Nome Icone SinAtivo |
| `listarPaises` | sem entrada documentada | Conjunto de Instâncias do objeto PaisAPI preenchidas com: IdPais Nome |
| `listarSeries` | sem entrada documentada | Conjunto de Instâncias do objeto SerieAPI preenchidas com: IdSerie Nome Aplicabilidade |
| `listarTiposConferencia` | sem entrada documentada | Conjunto de Instâncias do objeto TipoConferenciaAPI preenchidas com: IdTipoConferencia Descricao |
| `listarTiposProcedimento` | sem entrada documentada | Conjunto de Instâncias do objeto TipoProcedimentoAPI preenchidas com: IdTipoProcedimento Nome |
| `listarTiposProcedimentoOuvidoria` | sem entrada documentada | Lista os tipos de processos sinalizados como de Ouvidoria retornando um conjunto de Instâncias do objeto TipoProcedimentoAPI preenchidas com: IdTipoProcedimento Nome SinOuvidoriaAnonimo |
| `listarUnidades` | Conjunto de Instâncias do objeto EntradaListarUnidadesAPI preenchidas com: IdUnidade IdOrgao PalavrasPesquisa | Conjunto de Instâncias do objeto UnidadeAPI preenchidas com: IdUnidade Sigla Descricao SinProtocolo SinArquivamento SinOuvidoria |
| `listarUsuarios` | Conjunto de Instâncias do objeto EntradaListarUsuariosAPI preenchidas com: IdUsuario | Conjunto de Instâncias do objeto UsuarioAPI preenchidas com: IdUsuario Sigla Nome |
| `reabrirBloco` | Instância do objeto EntradaReabrirBlocoAPI preenchida com: IdBloco | sem saida documentada |
| `reabrirProcesso` | Instância do objeto EntradaReabrirProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `registrarAnotacao` | sem entrada documentada | Conjunto de Instâncias do objeto EntradaRegistrarAnotacaoAPI preenchidas com: IdProcedimento ou ProtocoloProcedimento Descricao SinPrioridade |
| `registrarOuvidoria` | Instância do objeto EntradaRegistrarOuvidoriaAPI preenchida com: IdOrgao Nome NomeSocial Email Cpf (opcional se Rg/OrgaoExpedidor informados) Rg (opcional se Cpf informado) OrgaoExpedidor (opcional se Cpf informado) Telefone Estado Cidade IdTipoProcedimento Processos SinRetorno Mensagem AtributosAdicionais (opcional) | sem saida documentada |
| `relacionarProcesso` | Instância do objeto EntradaRelacionarProcessoAPI preenchida com: IdProcedimento1 ou ProtocoloProcedimento1 IdProcedimento2 ou ProtocoloProcedimento2 | sem saida documentada |
| `removerControlePrazo` | Instâncias do objeto EntradaRemoverControlePrazoAPI preenchidas com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `removerRelacionamentoProcesso` | Instância do objeto EntradaRemoverRelacionamentoProcessoAPI preenchida com: IdProcedimento1 ou ProtocoloProcedimento1 IdProcedimento2 ou ProtocoloProcedimento2 | sem saida documentada |
| `removerSobrestamentoProcesso` | Instância do objeto EntradaRemoverSobrestamentoProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `retirarDocumentoBloco` | Instância do objeto EntradaRetirarDocumentoBlocoAPI preenchida com: IdBloco IdDocumento ou ProtocoloDocumento | sem saida documentada |
| `retirarProcessoBloco` | Instância do objeto EntradaRetirarProcessoBlocoAPI preenchida com: IdBloco IdProcedimento ou ProtocoloProcedimento | sem saida documentada |
| `sobrestarProcesso` | Instância do objeto EntradaSobrestarProcessoAPI preenchida com: IdProcedimento ou ProtocoloProcedimento IdProcedimentoVinculado ou ProtocoloProcedimentoVinculado (opcional) Motivo | sem saida documentada |
