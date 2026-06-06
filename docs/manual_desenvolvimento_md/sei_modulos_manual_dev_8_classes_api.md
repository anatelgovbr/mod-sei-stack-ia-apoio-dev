# 8. Classes API

A troca de informações do sistema com os módulos deve ser feita utilizando as classes específicas da API (diretório `sei/web/api`). Na classe de integração do módulo, ao interceptar eventos, o sistema disponibilizará objetos dessas classes API com atributos específicos preenchidos. Da mesma forma, quando o módulo realizar uma operação por meio da classe SeiRN deverá criar objetos dessas classes API informando os atributos adequados.

- Ver mais detalhes nas seções **Eventos** e **Operações**.
- **Atenção**: Não é recomendado o uso de outras classes ou objetos internos do sistema.

## AcessoExternoAPI

| IdAcessoExterno | Identificador do Acesso Externo |
|---|---|
| DataValidade | Data de validade do acesso externo |
| Procedimento | Ocorrência de ProcedimentoAPI |
| Documento | Ocorrência de DocumentoAPI |
| SinAcessoProcesso | S/N -- indica se o acesso externo possibilita visualização integral do processo |

## AndamentoAPI

| IdAndamento | Identificador do Andamento |
|---|---|
| IdTarefa | Identificador da tarefa associada |
| IdTarefaModulo | Identificador da tarefa de módulo associada |
| Descricao | Descrição do andamento |
| DataHora | Data/hora do andamento |
| Usuario | Ocorrência de UsuarioAPI |
| Unidade | Ocorrência de UnidadeAPI |
| Atributos | Conjunto de ocorrências de AtributoAndamentoAPI |
| IdProtocolo | Identificador do protocolo do andamento |

## AnexoAPI

| IdAnexo | Identificador do Anexo |
|---|---|
| Nome | Nome do anexo |
| DataHora | Data/hora do anexo |
| Tamanho | Tamanho do anexo |
| Conteudo | Conteúdo do anexo |

## AndamentoMarcadorAPI

| IdAndamentoMarcador | Identificador do andamento de marcador |
|---|---|
| Texto | Texto do andamento |
| DataHora | Data/hora do andamento |
| Usuario | Ocorrência de UsuarioAPI |
| Marcador | Ocorrência de MarcadorAPI |

## ArquivoExtensaoAPI

| IdArquivoExtensao | Identificador do registro |
|---|---|
| Extensao | Extensão de arquivo |
| Descricao | Descrição da extensão |

## ArvoreAcaoItemAPI

| Tipo | Rótulo que serve como agrupador para nós do mesmo tipo (caso seja necessário varrer todos os nós posteriormente filtrando pelo tipo). Para agrupar os itens do módulo utilizar MD + instituição + tipo. Exemplo:<br> `$objArvoreAcaoItemAPI->setTipo('MD_ABC_AUDIENCIAS')`;|
|---|---|
| Id | Identificador do nó na árvore. Deve ser único sendo recomendado utilizar o MD + instituição + descrição + ID do protocolo. Exemplo:<br> `$objArvoreAcaoItemAPI->setId('MD_ABC_AUDIENCIA_'. $dblIdDocumento);`|
| IdPai | Identificador do nó pai na árvore. O SEI monta os nós de processo e documentos usando o identificador do protocolo como valor para o campo Id. Exemplo:<br> `$objArvoreAcaoItemAPI->setIdPai($dblIdDocumento);`|
| Href | Pode ser um link ou um código javascript. Exemplo:<br>  `$objArvoreAcaoItemAPI->setHref('...link...');`<br> `$objArvoreAcaoItemAPI->setHref('javascript:alert(\'Ícone Processo ABC\');');` |
| Target | Indica qual o destino para execução do link em href:<br>**_blank** = nova janela<br>**ifrVisualizacao** = área ao lado da árvore de processo em que é exibido o conteúdo do documento<br>**null** = se o href é um javascript |
| Title | Texto que será exibido ao passar o mouse sobre o ícone |
| Icone | Caminho para a imagem sendo recomendado utilizar o formato SVG com tamanho 24x24. Exemplo:<br> `$objArvoreAcaoItemAPI->setIcone('modulos/abc/exemplo/imagens/abc_pequeno.svg');`|
| SinHabilitado | S/N -- indica se o ícone será clicável ou não |

## AssinaturaAPI

| Nome | Nome do assinante |
|---|---|
| CargoFuncao | Cargo/função utilizado na assinatura |
| DataHora | Data/hora da assinatura |
| IdUsuario | ID do usuário |
| IdOrigem | ID Origem associado com o usuário no SIP |
| IdOrgao | ID do órgão do usuário |
| Sigla | Sigla do usuário |
| Cpf | CPF do usuário |
| StaFormaAutenticacao | Tipo da autenticação:<br>C = Certificado Digital<br>S = Senha<br>M = Módulo |
| Agrupador | Identificador associado com assinaturas ainda não confirmadas |

## AssuntoAPI

| CodigoEstruturado | Código do assunto |
|---|---|
| Descricao | Descrição do assunto |

## AtributoAndamentoAPI

| Nome | Nome do atributo, corresponde a variável que será substituída no texto. Exemplo:<br> \@SALA@ |
|---|---|
| Valor | Valor do atributo. Exemplo:<br>   302 |
| IdOrigem | Identificador opcional associado com o andamento (campo texto com até 50 posições). Exemplo:<br>   76232 = identificador interno da sala |

## AtributoOuvidoriaAPI

| Id | Identificador do atributo da ouvidoria. Exemplo: P |
|---|---|
| Nome | Nome interno do atributo. Exemplo: RELACAO |
| Titulo | Título do atributo para exibição no formulário gerado no processo. Exemplo: Relação com a Justiça Federal |
| Valor | Valor do atributo para exibição associado com o título. Exemplo: Procurador Público |

## BlocoAPI

| IdBloco | Identificador do bloco |
|---|---|
| Descricao | Descrição associada com o bloco |
| Tipo | A = Assinatura<br>R = Reunião<br>I = Interno |
| Estado | A = Aberto<br>D = Disponibilizado<br>B = Recebido<br>R = Retornado<br>C = Concluído |
| Unidade | Unidade que gerou o bloco (ocorrência de UnidadeAPI) |
| Usuario | Usuário que gerou o bloco (ocorrência de UsuarioAPI) |
| SinPrioridade | S/N -- Indica se o bloco foi sinalizado como prioritário na unidade |
| SinRevisao | S/N -- Indica se o bloco foi sinalizado como revisado na unidade |
| UsuarioAtribuicao | Dados do usuário para o qual o bloco foi atribuído na unidade (ocorrência de UsuarioAPI) |
| UnidadesDisponibilizacao | Unidades configuradas para disponibilização (conjunto de UnidadeAPI) |

## CampoAPI

| Nome | Nome do campo do formulário |
|---|---|
| Valor | Valor do campo do formulário |

## CargoAPI

| IdCargo | Identificador interno do cargo |
|---|---|
| ExpressaoCargo | Descrição do cargo (Exemplo: Governador) |
| ExpressaoTratamento | Tratamento para o cargo (Exemplo: A Sua Excelência o Senhor) |
| ExpressaoVocativo | Vocativo para o cargo (Exemplo: Senhor Governador) |

## CidadeAPI

| IdCidade | Identificador da cidade |
|---|---|
| IdEstado | Identificador do estado |
| IdPais | Identificador do país |
| Nome | Nome da cidade |
| CodigoIbge | Código IBGE da cidade |
| SinCapital | S/N -- indica se a cidade é capital do estado |
| Latitude | Latitude da cidade |
| Longitude | Longitude da cidade |

## ConfiguracoesAssinaturaAPI

| NomeModulo | Nome do módulo responsável pela assinatura |
|---|---|
| TipoAssinturaSenha | true/false -- assinatura com senha |
| TipoAssinaturaCertificado | true/false -- assinatura com certificado digital |
| GerarAgrupador | true/false -- gerar ID para agrupar para as assinaturas |
| GerarIndexacao | true/false -- indexar após assinatura |
| UtilizaRevalidacao | true/false -- cadastrar assinatura como inativa até que o mecanismo revalide |
| UsuarioComCpf | true/false -- indica se o assinante precisa ter CPF cadastrado |
| ValidacaoCertificado | true/false |
| LinkValidacao | Link para validação da assinatura |
| TipoTarjaAssinatura | Tipo da tarja de assinatura existente no banco que será utilizada |
| TipoTarjaAutenticacao | Tipo da tarja de autenticação existente no banco que será utilizada |

## ContatoAPI

| StaOperacao | A = Cadastrar/Alterar<br>E = Excluir<br>D = Desativar<br>R = Reativar |
|---|---|
| IdContato | Identificador do contato |
| IdTipoContato | Tipo do contato |
| NomeTipoContato | Nome do tipo de contato |
| Sigla | Sigla do contato |
| Nome | Nome do contato |
| NomeSocial | Nome Social do Contato |
| StaNatureza | F/J = Pessoa Física/Jurídica |
| IdContatoAssociado | Identificador do contato associado |
| NomeContatoAssociado | Nome do contato associado |
| SinEnderecoAssociado | S/N -- indica se o contato utiliza ou não o endereço do contato associado |
| CnpjAssociado | CNPJ do contato associado |
| Endereco | Dados de endereçamento do contato - Endereço |
| Complemento | Dados de endereçamento do contato - Complemento do Endereço |
| Bairro | Dados de endereçamento do contato - Bairro |
| IdCidade | Dados de endereçamento do contato - id da Cidade |
| NomeCidade | Dados de endereçamento do contato - Nome da Cidade |
| IdEstado | Dados de endereçamento do contato - id do Estado |
| SiglaEstado | Dados de endereçamento do contato - Sigla do Estado |
| IdPais | Dados de endereçamento do contato - id do País |
| NomePais | Dados de endereçamento do contato - Nome do País |
| Cep | Dados de endereçamento do contato - CEP |
| StaGenero | M/F = Masculino/Feminino |
| IdCargo | Identificador interno do cargo |
| ExpressaoCargo | Descrição do cargo |
| ExpressaoTratamento | Descrição do tratamento |
| ExpressaoVocativo | Descrição do vocativo |
| Cpf | Número do CPF sem formatação |
| Cnpj | Número do CNPJ sem formatação |
| Rg | Número do RG |
| OrgaoExpedidor | Órgão expedidor |
| Matricula | Número de matrícula |
| MatriculaOab | Matrícula OAB |
| NumeroPassaporte | Número do passaporte |
| IdPaisPassaporte | País de emissão do passaporte |
| NomePaisPassaporte | Nome do país do passaporte |
| TelefoneFixo | Telefone fixo |
| TelefoneCelular | Telefone celular |
| DataNascimento | Data de nascimento |
| Email | E-mail |
| SitioInternet | Sítio na internet |
| Observacao | Texto de observação associado |
| SinAtivo | S/N -- Sinalizador indica se o registro está ativo |

## DefinicaoMarcadorAPI

| IdMarcador | Identificador do marcador |
|---|---|
| IdProcedimento | Identificador do processo |
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| Texto | Texto associado com a definição |

## DestinatarioAPI

| Sigla | Sigla do destinatário |
|---|---|
| Nome | Nome do destinatário |
| IdContato | Identificador interno do destinatário |
| Cpf | CPF do destinatário |
| Cnpj | CNPJ do destinatário |

## DocumentoAPI

| IdDocumento | Identificador do documento |
|---|---|
| Tipo | Tipo interno do documento:<br>G = Gerado<br>R = Recebido |
| SubTipo | Subtipos do tipo G (Gerado):<br>E = Editor eDoc (descontinuado)<br>I = Editor Interno HTML<br>A = Formulário automático XML (email, ouvidoria)<br>F = Formulário gerado<br>Subtipo do tipo R (Recebido):<br>X = Externo |
| IdProcedimento | Identificador do processo |
| ProtocoloProcedimento | Número do processo visível para o usuário.<br>Exemplo: 12.1.000000077-4 |
| IdSerie | Identificador do tipo do documento visível para o usuário |
| NomeSerie | Nome do tipo do documento visível para o usuário |
| Numero | Número do documento. Exemplo: Portaria 123 |
| NomeArvore | Nome complementar a ser exibido na árvore de documentos do processo |
| DinValor | Valor monetário. Exemplo: 133.050,95 ou 133050,95 |
| Data | Data do documento |
| Descricao | Descrição associada com o documento |
| IdTipoConferencia | Identificador do tipo de conferência |
| SinArquivamento | S/N -- Sinalizador indica se o documento deve ser arquivado |
| Remetente | Obrigatório para documentos externos, passar null para documentos gerados (ver estrutura RemetenteAPI). Todos os campos da estrutura são opcionais e o sistema tentará identificar o contato na ordem: IdContato, Cpf, Cnpj, Sigla+Nome, Sigla ou Nome. Por exemplo, se passados CPF, Sigla e Nome então a busca será apenas pelo CPF. Caso exista um registro com o CPF informado ele será usado mesmo que a Sigla/Nome sejam diferentes. Caso não encontre então será cadastrado um contato com o CPF, Sigla e Nome informados. Se o contato pode não existir então é importante passar o Nome para permitir o cadastro automático. |
| Interessados | Lista de instâncias de InteressadoAPI. Se não existirem interessados deve ser informado um conjunto vazio. Todos os campos da estrutura são opcionais e o sistema tentará identificar o contato na ordem: IdContato, Cpf, Cnpj, Sigla+Nome, Sigla ou Nome. Por exemplo, se passados CPF, Sigla e Nome então a busca será apenas pelo CPF. Caso exista um registro com o CPF informado ele será usado mesmo que a Sigla/Nome sejam diferentes. Caso não encontre então será cadastrado um contato com o CPF, Sigla e Nome informados. Se o contato pode não existir então é importante passar o Nome para permitir o cadastro automático. |
| Destinatarios | Lista de instâncias de DestinatarioAPI. Se não existirem destinatários deve ser informado um conjunto vazio. Todos os campos da estrutura são opcionais e o sistema tentará identificar o contato na ordem: IdContato, Cpf, Cnpj, Sigla+Nome, Sigla ou Nome. Por exemplo, se passados CPF, Sigla e Nome então a busca será apenas pelo CPF. Caso exista um registro com o CPF informado ele será usado mesmo que a Sigla/Nome sejam diferentes. Caso não encontre então será cadastrado um contato com o CPF, Sigla e Nome informados. Se o contato pode não existir então é importante passar o Nome para permitir o cadastro automático. |
| Observacao | Texto da observação |
| NomeArquivo | Nome do arquivo associado com o documento Tipo = R |
| NivelAcesso | 0 = Público<br>1 = Restrito<br>2 = Sigiloso |
| IdHipoteseLegal | Identificador da hipótese legal associada |
| Conteudo | Conteúdo do documento externo codificado em Base64 |
| ConteudoMTOM | Conteúdo do documento externo em formato binário |
| SinBloqueado | S/N -- se o documento estiver bloqueado então seu conteúdo não poderá ser alterado |
| IdArquivo | Identificador do arquivo no repositório (ver método adicionar Arquivo) |
| Campos | Lista de instâncias de CampoAPI |
| IdUnidadeGeradora | Identificador da unidade geradora do documento |
| NumeroProtocolo | Número SEI do documento |
| SinAssinado | S/N -- indica se o documento está assinado |
| SinPublicado | S/N -- indica se o documento está publicado |
| CodigoAcesso | Valor numérico utilizado pelo sistema para indicar se o usuário tem acesso a determinado protocolo. O usuário tem acesso se esse valor for MAIOR que zero (zero ou negativo indica falta de acesso). |
| IdOrgaoUnidadeGeradora | Identificador do órgão associado com a unidade geradora |
| IdUsuarioGerador | Identificador do usuário gerador |
| IdPlanoTrabalho | Identificador do Plano de Trabalho |
| IdEtapaTrabalho | Identificador da Etapa de Trabalho |
| IdItemEtapa | Identificador do Item da Etapa |
| IdOperacao | Identificador único gerado para a operação iniciada pelo usuário na interface |
| AtributosModulo | Conjunto chave-valor com os atributos do módulo |

## EntradaAdicionarArquivoAPI

| Nome | Nome do arquivo |
|---|---|
| Tamanho | Tamanho em bytes do arquivo |
| Hash | MD5 do conteúdo total |
| Conteudo | Conteúdo total ou parcial do arquivo |

## EntradaAdicionarConteudoArquivoAPI

| IdArquivo | Identificador do arquivo no repositório |
|---|---|
| Conteudo | Conteúdo parcial do arquivo |

## EntradaAgendarPublicacaoAPI

| IdDocumento | Identificador do documento |
|---|---|
| ProtocoloDocumento | Número do documento visível para o usuário.<br>Exemplo: 0003934 |
| StaMotivo | 1 = Publicação<br>2 = Retificação<br>3 = Republicação<br>4 = Apostilamento |
| IdVeiculoPublicacao | Identificador do veículo de publicação |
| DataDisponibilizacao | Data de disponibilização |
| Resumo | Texto do resumo de publicação |
| ImprensaNacional | Ocorrência de PublicacaoImprensaNacionalAPI preenchida com IdVeiculo, Pagina, IdSecao e Data. |

## EntradaAlterarPublicacaoAPI

| IdPublicacao | Identificador da publicação |
|---|---|
| IdDocumento | Identificador do documento |
| ProtocoloDocumento | Número do documento visível para o usuário.<br>Exemplo: 0003934 |
| StaMotivo | 1 = Publicação<br>2 = Retificação<br>3 = Republicação<br>4 = Apostilamento |
| IdVeiculoPublicacao | Identificador do veículo de publicação |
| DataDisponibilizacao | Data de disponibilização |
| Resumo | Texto do resumo de publicação |
| ImprensaNacional | Ocorrência de PublicacaoImprensaNacionalAPI preenchida com IdVeiculo, Pagina, IdSecao e Data. |

## EntradaAnexarProcessoAPI

| IdProcedimentoPrincipal | Identificador do processo que conterá o anexo |
|---|---|
| ProtocoloProcedimentoPrincipal | Número do processo que conterá o anexo visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdProcedimentoAnexado | Identificador do processo que será anexado |
| ProtocoloProcedimentoAnexado | Número do processo que será anexado visível para o usuário. Exemplo: 12.1.000001213-6 |

## EntradaAtribuirProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdUsuario | Identificador do usuário |
| SinReabrir | S/N -- indica se o processo deve ser reaberto caso esteja concluído |

## EntradaBloquearDocumentoAPI

| IdDocumento | Identificador do documento |
|---|---|
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |

## EntradaBloquearProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaCancelarAgendamentoPublicacaoAPI

| IdPublicacao | Identificador da publicação |
|---|---|
| IdDocumento | Identificador do documento |
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |

## EntradaCancelarDisponibilizacaoBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|

## EntradaCancelarDocumentoAPI

| IdDocumento | Identificador do documento |
|---|---|
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |
| Motivo | Texto do motivo para cancelamento |

## EntradaConcluirBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|

## EntradaConcluirControlePrazoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaConcluirProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaConfirmarDisponibilizacaoPublicacaoAPI

| IdVeiculoPublicacao | Identificador do veículo de publicação |
|---|---|
| DataDisponibilizacao | Data de disponibilização efetiva |
| DataPublicacao | Data de publicação efetiva |
| Numero | Número da edição de publicação |
| IdDocumentos | Identificadores internos dos documentos |

## EntradaConsultarBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|
| SinRetornarProtocolos | S/N -- indica se além dos dados do bloco também devem ser retornados os protocolos que ele contém |

## EntradaConsultarDocumentoAPI

| IdDocumento | Identificador do documento |
|---|---|
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |
| SinRetornarAndamentoGeracao | S/N -- indica se deve ser retornado o andamento de geração do documento |
| SinRetornarAssinaturas | S/N -- indica se devem ser retornadas as assinaturas |
| SinRetornarPublicacao | S/N -- indica se devem ser retornadas as informações de publicação |
| SinRetornarCampos | S/N -- indica se devem ser retornados os campos (para formulários) |
| SinRetornarBlocos | S/N -- indica se devem ser retornados os blocos na unidade atual que contém o documento |

## EntradaConsultarProcedimentoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| SinRetornarAssuntos | S/N -- indica se devem ser retornados os assuntos associados (conjunto de AssuntoAPI) |
| SinRetornarInteressados | S/N -- indica se devem ser retornados os interessados (conjunto de InteressadoAPI) |
| SinRetornarObservacoes | S/N -- indica se devem ser retornadas as observações (conjunto de ObservacaoAPI) |
| SinRetornarAndamentoGeracao | S/N -- indica se deve ser retornado o andamento de geração (ocorrência de AndamentoAPI) |
| SinRetornarAndamentoConclusao | S/N -- indica se deve ser retornado o andamento de conclusão na unidade (ocorrência de AndamentoAPI) |
| SinRetornarUltimoAndamento | S/N -- indica se deve ser retornado o último andamento na unidade (ocorrência de AndamentoAPI) |
| SinRetornarUnidadesProcedimentoAberto | S/N -- indica se devem ser retornadas as unidades onde o processo está aberto (conjunto de UnidadeProcedimentoAbertoAPI) |
| SinRetornarProcedimentosRelacionados | S/N -- indica se deve ser retornados os processos relacionados (conjunto de ProcedimentoResumidoAPI) |
| SinRetornarProcedimentosAnexados | S/N -- indica se deve ser retornados os processos anexados (conjunto de ProcedimentoResumidoAPI) |

## EntradaConsultarProcedimentoIndividualAPI

| IdOrgaoProcedimento | Identificador do órgão do processo |
|---|---|
| IdTipoProcedimento | Identificador do tipo do processo |
| IdOrgaoUsuario | Identificador do órgão do usuário |
| SiglaUsuario | Sigla do usuário |

## EntradaConsultarPublicacaoAPI

| IdPublicacao | Identificador da publicação |
|---|---|
| IdDocumento | Identificador do documento |
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |
| SinRetornarAndamento | S/N -- indica se deve ser retornado o andamento de publicação |
| SinRetornarAssinaturas | S/N -- indica se devem ser retornadas as assinaturas do documento |

## EntradaDefinirControlePrazoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| DataPrazo | Data certa para o prazo |
| Dias | Número de dias para o controle de prazo |
| SinDiasUteis | S/N -- indica se o valor passado no atributo Dias corresponde a dias úteis ou não |

## EntradaDesanexarProcessoAPI

| IdProcedimentoPrincipal | Identificador do processo que contém o anexo |
|---|---|
| ProtocoloProcedimentoPrincipal | Número do processo que contém o anexo visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdProcedimentoAnexado | Identificador do processo anexado |
| ProtocoloProcedimentoAnexado | Número do processo anexado visível para o usuário. Exemplo: 12.1.000001213-6 |
| Motivo | Texto indicando o motivo da desanexação |

## EntradaDesbloquearProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaDevolverBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|

## EntradaDisponibilizarBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|

## EntradaEnviarEmailAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| De | Endereço do remetente |
| Para | Endereços dos destinatários (separados por ponto e vírgula `;`) |
| CCO | Endereços dos destinatários para envio com cópia oculta (separados por ponto e vírgula `;` ) |
| Assunto | Assunto da mensagem |
| Mensagem | Conteúdo da mensagem |
| NivelAcesso | Opcional<br>0 = Público (valor padrão)<br>1 = Restrito |
| IdHipoteseLegal | Opcional, Identificador interno da hipótese legal associada |
| IdDocumentos | Conjunto de identificadores internos dos documentos do processo que devem ser anexados no email |
| Arquivos | Conjunto de arquivos avulsos que devem ser anexados no email |

## EntradaEnviarProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| UnidadesDestino | Identificadores das unidades para envio |
| SinManterAbertoUnidade | S/N -- indica se o processo deve ficar aberto na unidade origem |
| SinRemoverAnotacao | S/N -- indica se a anotação deve ser removida do processo após o envio |
| SinEnviarEmailNotificacao | S/N -- indica se deve ser enviado email de notificação para as unidades destino |
| DataRetornoProgramado | Data para retorno no formado dd/mm/aaaa |
| DiasRetornoProgramado | Número de dias para retorno |
| SinDiasUteisRetornoProgramado | S/N -- indica se os dias informados são úteis |
| SinReabrir | S/N -- indica se o processo deve ser reaberto automaticamente na unidade de origem antes do envio |

## EntradaExcluirBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|

## EntradaExcluirDocumentoAPI

| IdDocumento | Identificador do documento |
|---|---|
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |

## EntradaExcluirProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaGerarBlocoAPI

| Tipo | Tipo do bloco:<br>A = Assinatura<br>R = Reunião<br>I = Interno |
|---|---|
| Descricao | Descrição do bloco |
| UnidadesDisponibilizacao | Identificadores internos das unidades para disponibilização. Passar um conjunto vazio caso o bloco não deva ser disponibilizado. |
| Documentos | Lista de protocolos de documentos (número visível para o usuário. Exemplo: 0003934) |
| IdDocumentos | Listas dos identificadores internos dos documentos |
| SinDisponibilizar | S/N -- sinalizador indicando se o bloco deve ser automaticamente disponibilizado |

## EntradaGerarProcedimentoAPI

| Procedimento | Dados do processo |
|---|---|
| Documentos | Informar os documentos que devem ser gerados em conjunto com o processo (conjunto de DocumentoAPI). Se nenhum documento for gerado informar um conjunto vazio. |
| ProcedimentosRelacionados | Identificadores dos processos que devem ser relacionados automaticamente com o novo processo |
| UnidadesEnvio | Identificadores das unidades para envio do processo após a geração. O processo ficará aberto na unidade geradora e nas unidades informadas nesse parâmetro. |
| SinManterAbertoUnidade | S/N -- sinalizador indica se o processo deve ser mantido aberto na unidade de origem |
| SinEnviarEmailNotificacao | S/N -- sinalizador indicando se deve ser enviado email de aviso para as unidades destinatárias |
| DataRetornoProgramado | Data para definição de Retorno Programado (opcional) |
| DiasRetornoProgramado | Número de dias para o Retorno Programado (opcional) |
| SinDiasUteisRetornoProgramado | S/N -- sinalizador indica se o valor passado no parâmetro DiasRetornoProgramado corresponde a dias úteis ou não (opcional) |
| IdMarcador | Identificador de um marcador da unidade para associação (opcional) |
| TextoMarcador | Texto do marcador (opcional) |
| DataControlePrazo | Data para definição do prazo (opcional) |
| DiasControlePrazo | Número de dias para definição do prazo (opcional) |
| SinDiasUteisControlePrazo | S/N -- sinalizador indica se o valor passado no parâmetro DiasControlePrazo corresponde a dias úteis ou não (opcional) |

## EntradaIncluirDocumentoBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|
| IdDocumento | Identificador interno do documento |
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |
| Anotacao | Texto de anotação associado com o documento no bloco |

## EntradaIncluirProcessoBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|
| IdProcedimento | Identificador do processo |
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| Anotacao | Texto de anotação associado com o documento no bloco |

## EntradaLancarAndamentoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdTarefa | Identificador da tarefa |
| IdTarefaModulo | Identificador da tarefa de módulo |
| Atributos | Atributos associados com o andamento (conjunto de AtributoAndamentoAPI) |

## EntradaListarAndamentosAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| SinRetornarAtributos | S/N -- indica se devem ser retornados os atributos associados com o andamento |
| Andamentos | Identificadores dos andamentos para filtro |
| Tarefas | Identificadores das tarefas para filtro |
| TarefasModulos | Identificadores das tarefas de módulos para filtro |

## EntradaListarAndamentosMarcadoresAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| Marcadores | Identificadores dos marcadores para filtro |

## EntradaListarCargosAPI

| IdCargo | Opcional. Identificador do cargo para filtro |
|---|---|

## EntradaListarCidadesAPI

| IdPais | Identificador do país para filtro |
|---|---|
| IdEstado | Identificador do estado para filtro |

## EntradaListarContatosAPI

| IdContatos | Opcional. Filtra por identificadores de contatos. |
|---|---|
| IdTipoContato | Opcional. Filtra o tipo de contato. |
| PaginaRegistros | Opcional. Informa o número máximo de registros que devem ser retornados por página de consulta (1 a 1000 com valor padrão 1). |
| PaginaAtual | Opcional. Informa o número da página atual (valor padrão 1). |
| Sigla | Opcional. Filtra contato pela sigla. |
| Nome | Opcional. Filtra contato pelo nome. |
| CPF | Opcional. Filtra contato pelo CPF. |
| CNPJ | Opcional. Filtra contato pelo CNPJ. |
| Matricula | Opcional. Filtra contato pelo número de matrícula. |

## EntradaListarEstadosAPI

| IdPais | Identificador do país para filtro |
|---|---|

## EntradaListarExtensoesPermitidasAPI

| IdArquivoExtensao | Identificador interno de uma extensão de arquivo |
|---|---|

## EntradaListarFeriadosAPI

| IdOrgao | Identificador do órgão associado com os feriados |
|---|---|
| DataInicial | Data inicial para filtro |
| DataFinal | Data final para filtro |

## EntradaListarHipotesesLegaisAPI

| NivelAcesso | 1 = Restrito<br>2 = Sigiloso |
|---|---|

## EntradaListarUnidadesAPI

| IdUnidade | Identificador interno de uma unidade para filtro |
|---|---|
| IdOrgao | Identificador interno de um órgão para filtro |
| PalavrasPesquisa | Texto para filtro na sigla/descrição das unidades |

## EntradaListarUsuariosAPI

| IdUsuario | Identificador interno de um usuário para filtro |
|---|---|

## EntradaReabrirBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|

## EntradaReabrirProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaRegistrarAnotacaoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| Descricao | Texto da anotação |
| SinPrioridade | S/N -- Sinalizador indicando se a anotação é prioritária |

## EntradaRegistrarOuvidoriaAPI

| IdOrgao | Identificador do órgão da ouvidoria onde será gerado o processo |
|---|---|
| Nome | Nome do cidadão |
| NomeSocial | Nome Social do cidadão |
| Email | E-mail do cidadão |
| Cpf | CPF do cidadão |
| Rg | RG do cidadão |
| OrgaoExpedidor | Órgão expedidor do RG do cidadão |
| Telefone | Telefone do cidadão |
| Estado | Unidade Federativa do cidadão |
| Cidade | Cidade do cidadão |
| IdTipoProcedimento | Identificador do tipo de processo da ouvidoria |
| Processos | Relação textual de processos relacionados informados pelo cidadão |
| SinRetorno | S/N -- indica se o cidadão deseja retorno do contato |
| SinAnonimo | S/N -- indica se o contato é anônimo |
| SinSigilo | S/N -- indica se requer tratamento sigiloso |
| Mensagem | Conteúdo da mensagem enviada pelo cidadão |
| Anexos | Conjunto de ocorrências de AnexoAPI (preencher os atributos considerando que o IdAnexo deve conter o nome do arquivo do upoad existente no diretório temporário do PHP ou então o Conteudo em Base64). |
| AtributosAdicionais | Atributos adicionais do formulário da ouvidoria (conjunto de AtributoOuvidoriaAPI) |

## EntradaRelacionarProcessoAPI

| IdProcedimento1 | Identificador do processo 1 |
|---|---|
| ProtocoloProcedimento1 | Número do processo 1 visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdProcedimento2 | Identificador do processo 2 |
| ProtocoloProcedimento2 | Número do processo 2 visível para o usuário. Exemplo: 12.1.000003541-1 |

## EntradaRemoverControlePrazoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaRemoverRelacionamentoProcessoAPI

| IdProcedimento1 | Identificador do processo 1 |
|---|---|
| ProtocoloProcedimento1 | Número do processo 1 visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdProcedimento2 | Identificador do processo 2 |
| ProtocoloProcedimento2 | Número do processo 2 visível para o usuário. Exemplo: 12.1.000003541-1 |

## EntradaRemoverSobrestamentoProcessoAPI

| IdProcedimento | Identificador do processo |
|---|---|
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaRetirarDocumentoBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|
| IdDocumento | Identificador interno do documento |
| ProtocoloDocumento | Número do documento visível para o usuário. Exemplo: 0003934 |

## EntradaRetirarProcessoBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|
| IdProcedimento | Identificador do processo |
| ProtocoloProcedimento | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |

## EntradaSobrestarProcessoAPI

| IdProcedimento | Identificador do processo que deve ser sobrestado |
|---|---|
| ProtocoloProcedimento | Número do processo que deve ser sobrestado visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdProcedimentoVinculado | Identificador do processo para vinculação |
| ProtocoloProcedimentoVinculado | Número do processo para vinculação visível para o usuário. Exemplo: 12.1.000003541-1 |
| Motivo | Texto indicando o motivo do sobrestamento |

## EstadoAPI

| IdEstado | Identificador interno do estado |
|---|---|
| IdPais | Identificador interno do país |
| Sigla | Sigla do estado |
| Nome | Nome do estado |
| CodigoIbge | Código IBGE do estado |

## FeriadoAPI

| Data | Data do feriado |
|---|---|
| Descricao | Descrição do feriado |

## HipoteseLegalAPI

| IdHipoteseLegal | Identificador da hipótese legal |
|---|---|
| Nome | Nome da hipótese legal |
| BaseLegal | Base legal associada |
| NivelAcesso | 1 = Restrito<br>2 = Sigiloso |
| SinAtivo | S/N -- Indica se a hipótese legal está ativa |

## InteressadoAPI

| Sigla | Sigla do interessado |
|---|---|
| Nome | Nome do interessado |
| IdContato | Identificador interno do interessado |
| Cpf | CPF do interessado |
| Cnpj | CNPJ do interessado |

## MarcadorAPI

| IdMarcador | Identificador interno do marcador |
|---|---|
| Nome | Nome do marcador |
| Icone | Imagem PNG em formato base64 |
| SinAtivo | S/N -- indica se o marcador está ativo |

## ObservacaoAPI

| Descricao | Texto da observação |
|---|---|
| Unidade | Unidade associada com a observação (ocorrência de UnidadeAPI) |

## OrgaoAPI

| IdOrgao | Identificador interno do órgão |
|---|---|
| Sigla | Sigla do órgão |
| Descricao | Descrição do órgão |

## PaginaComplementoAPI

| Css | Código CSS para inclusão na respectiva seção da página |
|---|---|
| JavascriptGlobal | Código Javascript inserido na área global da página |
| JavascriptInicializacao | Código Javascript para execução na inicialização da página |
| JavascriptValidacao | Código Javascript para execução na validação da página |
| Html | Código HTML para inclusão na respectiva seção da página |
| AtributosModulo | Conjunto chave-valor com os atributos do módulo |

## PaisAPI

| IdPais | Identificador interno do país |
|---|---|
| Nome | Nome do país |

## ProcedimentoAPI

| IdProcedimento | Identificador interno do processo |
|---|---|
| IdTipoProcedimento | Identificador interno do tipo de processo |
| NomeTipoProcedimento | Nome do tipo de processo |
| NumeroProtocolo | Número do processo visível para o usuário.<br>Exemplo: 12.1.000003541-1 |
| DataAutuacao | Data de autuação do processo |
| Especificacao | Texto da especificação associada |
| IdTipoPrioridade | Identificador interno do tipo de prioridade |
| Assuntos | Assuntos do processo (ocorrências de AssuntoAPI) |
| Interessados | Lista de instâncias de InteressadoAPI. Se não existirem interessados deve ser informado um conjunto vazio. Todos os campos da estrutura são opcionais e o sistema tentará identificar o contato na ordem: IdContato, Cpf, Cnpj, Sigla+Nome, Sigla ou Nome. Por exemplo, se passados CPF, Sigla e Nome então a busca será apenas pelo CPF. Caso exista um registro com o CPF informado ele será usado mesmo que a Sigla/Nome sejam diferentes. Caso não encontre então será cadastrado um contato com o CPF, Sigla e Nome informados. Se o contato pode não existir então é importante passar o Nome para permitir o cadastro automático. |
| Observacao | Texto da observação da unidade |
| NivelAcesso | 0 = Público<br>1 = Restrito<br>2 = Sigiloso |
| IdHipoteseLegal | Identificador interno da hipótese legal associada |
| CodigoAcesso | Valor numérico utilizado pelo sistema para indicar se o usuário tem acesso a determinado protocolo. O usuário tem acesso se esse valor for MAIOR que zero (zero ou negativo indica falta de acesso) |
| SinAberto | S/N -- indica se o processo está aberto na unidade |
| IdUnidadeGeradora | Identificador interno da unidade geradora |
| IdOrgaoUnidadeGeradora | Identificador interno do órgão da unidade geradora |
| IdUsuarioGerador | Identificador interno do usuário gerador do processo |
| GrauSigilo | U = Ultrassecreto<br>S = Secreto<br>R = Reservado |

## ProcedimentoResumidoAPI

| IdProcedimento | Identificador do processo que deve ser sobrestado |
|---|---|
| ProtocoloProcedimento | Número do processo que deve ser sobrestado visível para o usuário. Exemplo: 12.1.000000077-4 |
| TipoProcedimento | Tipo do processo (ocorrência de TipoProcedimentoAPI) |

## ProtocoloBlocoAPI

| ProtocoloFormatado | Número do processo ou documento visível para o usuário |
|---|---|
| Identificacao | Nome do tipo de processo ou do tipo documento (seguido da numeração associada se existir). Exemplo: Compra de Material e Contratação de Serviços, Portaria 35 |
| Assinaturas | Assinaturas associadas com os documentos (conjunto de AssinaturaAPI) |

## PublicacaoAPI

| IdPublicacao | Identificador da publicação |
|---|---|
| IdDocumento | Identificador do documento |
| IdSerieDocumento | Identificador do tipo do documento |
| IdVeiculoPublicacao | Identificador do veículo de publicação |
| NomeVeiculo | Nome do veículo cadastrado no SEI |
| StaTipoVeiculo | I = Interno<br>E = Externo<br>M = Modulo |
| StaMotivo | 1 = Publicação<br>2 = Retificação<br>3 = Republicação<br>4 = Apostilamento |
| Numero | Número da publicação |
| DataDisponibilizacao | Data da disponibilização |
| DataPublicacao | Data da publicação |
| Resumo | Texto do resumo da publicação |
| Estado | A = Agendado<br>P = Publicado |
| ImprensaNacional | Dados da Imprensa Nacional associados (ocorrência de PublicacaoImprensaNacionalAPI) |

## PublicacaoImprensaNacionalAPI

| IdVeiculo | Identificador do veículo de publicação |
|---|---|
| SiglaVeiculo | Sigla do veículo (exemplo: DOU) |
| DescricaoVeiculo | Descrição do veículo (exemplo: Diário Oficial da União) |
| Pagina | Página da publicação |
| IdSecao | Identificador interno da seção (exemplo: 100023) |
| Secao | Seção da publicação (exemplo: 2) |
| Data | Data da publicação |

## RemetenteAPI

| Sigla | Sigla do remetente |
|---|---|
| Nome | Nome do remetente |
| IdContato | Identificador interno do remetente |
| Cpf | CPF do remetente |
| Cnpj | CNPJ do remetente |

## SaidaConsultarBlocoAPI

| IdBloco | Identificador do bloco |
|---|---|
| Descricao | Descrição associada com o bloco |
| Tipo | A = Assinatura<br>R = Reunião<br>I = Interno |
| Estado | A = Aberto<br>D = Disponibilizado<br>B = Recebido<br>R = Retornado<br>C = Concluído |
| Unidade | Unidade que gerou o bloco (ocorrência de UnidadeAPI) |
| Usuario | Usuário que gerou o bloco (ocorrência de UsuarioAPI) |
| SinPrioridade | S/N -- Indica se o bloco foi sinalizado como prioritário na unidade |
| SinRevisao | S/N -- Indica se o bloco foi sinalizado como revisado na unidade |
| UsuarioAtribuicao | Dados do usuário para o qual o bloco foi atribuído na unidade (ocorrência de UsuarioAPI) |
| UnidadesDisponibilizacao | Unidades configuradas para disponibilização (conjunto de UnidadeAPI) |
| Protocolos | Protocolos do bloco (conjunto de ProtocoloBlocoAPI) |

## SaidaConsultarDocumentoAPI

| IdProcedimento | Id interno do processo no SEI. Exemplo: 1210000000774 |
|---|---|
| ProcedimentoFormatado | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| IdDocumento | Id interno do documento no SEI. Exemplo: 1140000000872 |
| DocumentoFormatado | Número do documento visível para o usuário. Exemplo: 0003934 |
| NivelAcessoLocal | Indica o nível de acesso registrado no cadastro do documento:<br>0 = Público<br>1 = Restrito<br>2 = Sigiloso |
| NivelAcessoGlobal | Indica o nível de acesso geral aplicado ao processo:<br>0 = Público<br>1 = Restrito<br>2 = Sigiloso |
| LinkAcesso | Link para acesso ao documento |
| Serie | Dados do tipo do documento (ocorrência de SerieAPI) |
| Numero | Número do documento |
| NomeArvore | Nome complementar exibido na árvore de documentos do processo |
| DinValor | Valor monetário do documento |
| Descricao | Descrição do documento |
| Data | Data de geração para documentos internos e para documentos externos é a data informada na tela de cadastro |
| UnidadeElaboradora | Dados da unidade que gerou o documento (ocorrência de UnidadeAPI) |
| AndamentoGeracao | Informações do andamento de geração (ocorrência de AndamentoAPI) |
| Assinaturas | Assinaturas do documento (conjunto de AssinaturaAPI) |
| Publicacao | Informações de publicação do documento (conjunto de PublicacaoAPI) |
| Campos | Campos do formulário (conjunto de CampoAPI) |
| Blocos | Blocos na unidade atual que contém o documento (conjunto de BlocoAPI) |

## SaidaConsultarProcedimentoAPI

| IdProcedimento | Id interno do processo no SEI. Exemplo: 1210000000774 |
|---|---|
| ProcedimentoFormatado | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| Especificacao | Especificação do processo |
| DataAutuacao | Data de autuação do processo |
| NivelAcessoLocal | Indica o nível de acesso registrado no cadastro do processo:<br>0 = Público<br>1 = Restrito<br>2 = Sigiloso |
| NivelAcessoGlobal | Indica o nível de acesso geral aplicado ao processo:<br>0 = Público<br>1 = Restrito<br>2 = Sigiloso |
| LinkAcesso | Link para acesso ao processo |
| TipoProcedimento | Dados do tipo do processo (ocorrência de TipoProcedimentoAPI) |
| TipoPrioridade | Dados do tipo de prioridade (ocorrência de TipoPrioridadeAPI) |
| AndamentoGeracao | Dados do andamento de geração (ocorrência de AndamentoAPI) |
| AndamentoConclusao | Dados do andamento de conclusão (ocorrência de AndamentoAPI) |
| UltimoAndamento | Dados do último andamento (ocorrência de AndamentoAPI) |
| UnidadesProcedimentoAberto | Conjunto de unidades onde o processo se encontra aberto (conjunto de UnidadeProcedimentoAbertoAPI) |
| Assuntos | Conjunto de assuntos do processo (conjunto de AssuntoAPI) |
| Interessados | Conjunto de interessados do processo (conjunto de InteressadoAPI) |
| Observacoes | Conjunto de observações das unidades (conjunto de ObservacaoAPI) |
| ProcedimentosRelacionados | Conjunto de processos relacionados (conjunto ProcedimentoResumidoAPI) |
| ProcedimentosAnexados | Conjunto processos anexados (conjunto de ProcedimentoResumidoAPI) |

## SaidaConsultarPublicacaoAPI

| Publicacao | Dados da publicação (ocorrência de PublicacaoAPI) |
|---|---|
| Andamento | Andamento de publicação (ocorrência de AndamentoAPI) |
| Assinaturas | Assinaturas do documento (conjunto de AssinaturaAPI) |

## SaidaEnviarEmailAPI

| IdDocumento | Id interno do email no SEI. Exemplo: 1140000000872 |
|---|---|
| DocumentoFormatado | Número do email visível para o usuário. Exemplo: 0003934 |
| LinkAcesso | Link para acesso ao email |

## SaidaGerarProcedimentoAPI

| IdProcedimento | Id interno do processo no SEI. Exemplo: 1210000000774 |
|---|---|
| ProcedimentoFormatado | Número do processo visível para o usuário. Exemplo: 12.1.000000077-4 |
| LinkAcesso | Link para acesso ao processo |
| RetornoInclusaoDocumentos | Conjunto de ocorrências de RetornoInclusaoDocumentoAPI (com um item para cada documento informado na geração do processo) |

## SaidaIncluirDocumentoAPI

| IdDocumento | Id interno do documento no SEI. Exemplo: 1140000000872 |
|---|---|
| DocumentoFormatado | Número do documento visível para o usuário. Exemplo: 0003934 |
| LinkAcesso | Link para acesso ao documento |

## SerieAPI

| IdSerie | Identificador do tipo de documento |
|---|---|
| Nome | Nome do tipo de documento |
| Aplicabilidade | T = Documentos internos e externos<br>I = Documentos internos<br>E = Documentos externos<br>F = Formulários |

## TipoConferenciaAPI

| IdTipoConferencia | Identificador do tipo de conferência |
|---|---|
| Descricao | Descrição do tipo de conferência |

## TipoContatoAPI

| IdTipoContato | Identificador do tipo de contato |
|---|---|
| Nome | Nome do tipo de contato |

## TipoPrioridadeAPI

| IdTipoPrioridade | Identificador do tipo de prioridade |
|---|---|
| Nome | Nome do tipo de prioridade |

## TipoProcedimentoAPI

| IdTipoProcedimento | Identificador do tipo de processo |
|---|---|
| Nome | Nome do tipo de processo |
| SinAnonimoOuvidoria | S/N -- indica se o tipo da ouvidoria permite contato anônimo |

## UnidadeAPI

| IdUnidade | Identificador da unidade |
|---|---|
| Sigla | Sigla da unidade |
| Descricao | Descrição da unidade |
| Orgao | Órgão associado com a unidade (ocorrência de OrgaoAPI) |
| SinProtocolo | S/N -- indica se é uma unidade de protocolo |
| SinArquivamento | S/N -- indica se é uma unidade de arquivo |
| SinOuvidoria | S/N -- indica se é uma unidade de ouvidoria |

## UnidadeProcedimentoAbertoAPI

| Unidade | Dados da Unidade onde o processo está aberto (ocorrência de UnidadeAPI). |
|---|---|
| UsuarioAtribuicao | Dados do Usuário para o qual o processo está atribuído (ocorrência de UsuarioAPI) |

## UsuarioAPI

| IdUsuario | Identificador do usuário |
|---|---|
| Sigla | Sigla do usuário |
| Nome | Nome do usuário |
| StaTipo | Tipo do usuário:<br>0 = Interno (SIP)<br>1 = Sistema<br>2 = Externo Pendente<br>3 = Externo Liberado |

## VeiculoPublicacaoAPI

| IdVeiculoPublicacao | Identificador do veículo de publicação |
|---|---|
| Nome | Nome do veículo |
| Descrição | Descrição do veículo |
| StaTipo | I = Interno<br>E = Externo<br>M = Módulo |
| SinFonteFeriados | Indica se o veículo é fonte de feriados para o sistema (somente veículos externos) |
| SinPermiteExtraordinaria | Indica se o veículo permite publicações extraordinárias (somente veículos externos) |
| SinExibirPesquisaInterna | Indica se os documentos publicados no veículo devem ser exibidos na pesquisa de publicação interna |
| WebService | Endereço do serviço de publicação (somente veículos externos) |
| SinAtivo | S/N -- Indica se o veículo está ativo |
