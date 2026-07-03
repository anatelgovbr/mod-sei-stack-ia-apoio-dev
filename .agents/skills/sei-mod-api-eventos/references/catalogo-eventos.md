# Catálogo de Eventos do SEI (v5.0 — Cap. 9)

> Fonte: `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_9_eventos.md`
> Uso: localizar o hook correto em `*Integracao.php` antes de propor interceptacao propria ou alteracao no core.

Se a duvida ainda estiver ambigua entre API, evento e operacao, usar primeiro
`sei-direcionador-integracao`. Se o caso for apenas menu interno SIP ou pagina
de modulo sem hook no core, a skill principal passa a ser `sei-menu-pagina`.

## Roteamento e Controladores

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| processarControlador | Dispatch principal de requisicoes para o modulo | Requisicoes internas do SEI | Roteamento central de modulo; raramente usado diretamente |
| processarControladorAjax | Dispatch de requisicoes AJAX internas | Chamadas AJAX internas (mesma origem) | Implementar endpoints AJAX internos do modulo |
| processarControladorAjaxExterno | Dispatch de requisicoes AJAX de origem externa | Chamadas AJAX externas (origens diferentes) | Integracoes externas via AJAX; CORS |
| processarControladorExterno | Dispatch de requisicoes de paginas externas (usuario externo) | Páginas de usuário externo autenticado | Páginas externas do modulo; interface publica |
| processarControladorPublicacoes | Dispatch de requisicoes de publicacoes | Páginas de pesquisa de publicações | Área pública de publicações; listagens |
| processarControladorWebServices | Dispatch de requisicoes de WebServices | Chamadas WS (SOAP/REST) | Integracao via WebServices; APIs externas |
| tratarLinkSemAssinatura | Tratamento de links sem assinatura digital | Links publicados sem assinatura | Processar link de acesso externo sem login; cautela |
| obterAcoesAjaxExternasSemLogin | Acoes disponiveis sem login para AJAX externo | Contexto AJAX sem sessao | Endpoints publicos; ações sem autenticação |
| obterAcoesExternasSemLogin | Acoes disponiveis sem login para pagina externa | Paginas externas sem sessao | Menu inicial de usuario externo; Tela de login |

## Ciclo de Vida de Processo e Documento

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| gerarProcesso | Apos geracao de novo processo | ProcedimentoAPI preenchido | Executar logica apos geracao de processo; integrar com outro sistema |
| alterarProcesso | Apos alteracao de processo (dadosbasicos, interessado, etc.) | ProcedimentoAPI com alteracoes | Reagir a mudanca de dados do processo; atualizar sistema externo |
| gerarDocumento | Apos geracao de documento | DocumentoAPI preenchido | Executar logica apos geracao de documento; integracao |
| alterarDocumento | Apos alteracao de documento | DocumentoAPI com alteracoes | Reagir a alteracao de documento; atualizar sistema |
| atualizarConteudoDocumento | Apos atualizacao de conteudo de documento | DocumentoAPI com novo conteudo | Atualizar indexacao; notificar sistema externo |
| anexarProcesso | Apos anexar processo a processo principal | IdProtocolo principal e anexado | Reagir ao vinculo de anexacao; sincronizar |
| desanexarProcesso | Apos desanexar processo | IdProtocolo principal e anexado, motivo | Reagir a desanexacao; atualizar sistemas |
| relacionarProcesso | Apos criar relacionamento lateral entre processos | Ids dos processos relacionados | Reagir ao vinculo lateral; atualizar sistema |
| removerRelacionamentoProcesso | Aps remover relacionamento entre processos | Ids dos processos | Reagir a remocao de vinculo |
| enviarProcesso | Apos envio de processo a outra unidade | ProcedimentoAPI, lista de unidades | Reagir a envio; notificar sistema externo |
| concluirProcesso | Aps conclusao de processo na unidade | ProcedimentoAPI | Reagir a conclusao; atualizar carga |
| reabrirProcesso | Aps reabertura de processo na unidade | ProcedimentoAPI | Reagir a reabertura; reativar carga |
| bloquearProcesso | Aps bloqueio de processo | ProcedimentoAPI, motivo | Reagir a bloqueio; restringir acesso externo |
| desbloquearProcesso | Aps desbloqueio de processo | ProcedimentoAPI | Reagir a desbloqueio; restaurar acesso |
| sobrestarProcesso | Aps sobrestamento de processo | ProcedimentoAPI, motivo | Reagir a sobrestamento; impedir tramite |
| removerSobrestamentoProcesso | Aps remover sobrestamento | ProcedimentoAPI | Reagir a remoção de sobrestamento |
| moverDocumento | Aps mover documento na árvore | IdDocumento, IdProtocoloPai novo | Reagir a reorganização de documento na árvore |
| cancelarDocumento | Aps cancelamento de documento | DocumentoAPI | Reagir a cancelamento; invalidar copia |
| eliminarDocumento | Aps eliminacao de documento | DocumentoAPI | Reagir a eliminacao; remover vínculo externo |
| eliminarProcesso | Aps eliminacao de processo | ProcedimentoAPI | Reagir a eliminacao; remover vínculo |
| confirmarAtualizacaoConteudoDocumento | Confirma atualizacao de conteudo de documento | DocumentoAPI | Confirmar atualização; aceitar ou recusar mudanca |
| prepararCloneDocumento | Prepara clone de documento para geracao | DocumentoAPI | Interceptar geracao de documento clone |
| darCienciaDocumento | Aps receber ciencia de documento | DocumentoAPI | Reagir a ciencia; marcar como visualizado |
| darCienciaProcesso | Aps receber ciencia de processo | ProcedimentoAPI | Reagir a ciencia de processo |
| permitirAndamentoConcluido | Antes de permitir conclusao de processo | ProcedimentoAPI | Validar condicoes para conclusao; bloquear se necessário |

## UI — Ícones e Botões

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| montarIconeControleProcessos | Adiciona icones na tela de Controle de Processos | Lista de ProcedimentoAPI (ate 200) | Adicionar icone customizado na linha do processo; status especial |
| montarIconeProcesso | Adiciona icone na visualizacao de processo | ProcedimentoAPI | Adicionar icone na tela de processo; badge |
| montarIconeDocumento | Adiciona icone na arvore de documentos | DocumentoAPI | Adicionar icone no documento; indicador de status |
| montarIconeSistema | Adiciona icone na barra de titulo do SEI | Sem parametro | Icone na barra superior do sistema; logo customizado |
| montarIconeAcompanhamentoEspecial | Adiciona icone na tela de Acompanhamento Especial | ProcedimentoAPI | Badge de acompanhamento especial |
| montarIconeOrdenarArvore | Adiciona controle de ordenacao na árvore | Sem parametro | Botao de ordenacao personalizado |
| alterarIconeArvoreDocumento | Altera icone de documento na arvore | DocumentoAPI, icone default | Substituir icone padrao por customizado |
| montarBotaoControleProcessos | Adiciona botoes na tela de Controle de Processos | Lista de ProcedimentoAPI | Adicionar botao de acao rapida; shortcut |
| montarBotaoProcesso | Adiciona botoes na tela de visualizacao de processo | ProcedimentoAPI | Botao de acao no processo; ferramenta |
| montarBotaoDocumento | Adiciona botoes na arvore de documentos | DocumentoAPI | Botao de acao no documento; download, info |
| montarBotaoCadastroDocumento | Adiciona botoes na tela de cadastro de documento | Sem parametro especifico | Acoes na tela de inclusao de documento |
| montarBotaoChatIA | Adiciona botao de chat IA na interface | Sem parametro | Botao de interacao com IA; integração |
| montarBotaoLoginExterno | Adiciona botao na tela de login externo | Sem parametro | Botao customizado no login externo |
| montarBotaoAcessoExternoAutorizado | Adiciona botoes na área de acesso externo autorizado | Contexto de acesso externo | Acoes para usuário externo autenticado |
| montarBotaoControleAcessoExterno | Adiciona botoes no controle de acesso externo | Contexto de acesso externo | Acoes de controle; revogar, limitar |
| montarBotaoAssinaturaInterno | Adiciona botoes na area de assinatura interno | DocumentoAPI | Acoes complementares na assinatura interna |
| montarBotaoAssinaturaExterno | Adiciona botoes na area de assinatura externo | DocumentoAPI | Acoes complementares na assinatura externa |
| montarBotaoVeiculoPublicacao | Adiciona botoes na tela de veiculo de publicacao | VeiculoPublicacaoAPI | Acoes no veiculo de publicacao |

## UI — Menus e Ações

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| montarMenuPublicacoes | Adiciona itens no menu de publicacoes | Sem parametro | Itens no menu de pesquisa de publicações |
| montarMenuUsuarioExterno | Adiciona itens no menu do usuario externo | Sem parametro | Itens no menu do portal externo |
| montarMenuConsultaProcessual | Adiciona itens no menu de consulta processual | Sem parametro | Itens no menu de consulta pública |
| adicionarElementoMenu | Adiciona elemento HTML abaixo do menu | Sem parametro | Inserir bloco HTML abaixo do menu; banner, aviso |
| obterDiretorioIconesMenu | Retorna caminho do diretorio de icones de menu | Sem parametro | Definir pasta de ícones SVG do modulo |
| montarAcaoControleAcessoExterno | Adiciona acoes no controle de acesso externo | Contexto de acesso externo | Acoes no controle de acesso; ações customizadas |
| montarAcaoDocumentoAcessoExternoAutorizado | Adiciona acoes no documento de acesso externo autorizado | DocumentoAPI | Acoes no documento do usuário externo |
| montarAcaoDocumentoAcessoExternoNegado | Adiciona acoes no documento de acesso externo negado | DocumentoAPI | Acoes quando acesso negado; mensagem |
| montarAcaoProcessoAnexadoAcessoExternoAutorizado | Adiciona acoes no processo anexado de acesso externo | ProcedimentoAPI | Acoes em processo anexado externo |
| montarAcaoProcessoAnexadoAcessoExternoNegado | Adiciona acoes no processo anexado acesso externo | ProcedimentoAPI | Acoes quando acesso negado |
| montarAcaoPublicacao | Adiciona acoes na publicacao | PublicacaoAPI | Acoes na tela de publicacao |
| montarAcaoVeiculoPublicacao | Adiciona acoes no veiculo de publicacao | VeiculoPublicacaoAPI | Acoes no veiculo; gestão |
| ocultarAcaoAlterarPublicacao | Oculta acao de alterar publicacao | Sem parametro | Ocultar botão de alteração de publicação |
| ocultarAcaoCancelarAgendamentoPublicacao | Oculta acao de cancelar agendamento | Sem parametro | Ocultar botão de cancelamento |
| ocultarBotaoSalvarPublicacao | Oculta botao de salvar publicacao | Sem parametro | Ocultar botão de salvar publicação |
| ocultarDadosImprensaNacionalPublicacao | Oculta dados da Imprensa Nacional na publicacao | Sem parametro | Ocultar seção de DOU na publicação |

## Segurança e Acesso

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| verificarAcessoProtocolo | Verifica acesso a protocolo na tela interna | IdProtocolo | Controlar acesso a processo/documento internamente |
| verificarAcessoProtocoloExterno | Verifica acesso a protocolo via acesso externo | IdProtocolo | Controlar acesso externo; validar permissoes |
| verificarAcessoTipoContato | Verifica acesso por tipo de contato | IdTipoContato | Controlar acesso por tipo de pessoa |
| verificarLoginExterno | Verifica credenciais de login externo | Credenciais | Autenticar usuario externo; customizar login |
| cancelarDisponibilizacaoAcessoExterno | Cancela disponibilizacao de acesso externo | IdAcessoExterno | Revogar acesso externo; encerrar sessão |
| cancelarLiberacaoAssinaturaExterna | Cancela liberacao de assinatura externa | Identificador de liberacao | Revogar liberacao de assinatura; desatrelhar |

## Assinatura e Publicação

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| obterConfiguracoesAssinatura | Retorna configuracoes de assinatura | Sem parametro | Customizar comportamento de assinatura; Plugins |
| prepararAssinaturaDocumento | Prepara documento para assinatura | DocumentoAPI | Interceptar preparacao de assinatura; adicionar validacao |
| assinarDocumento | Aps assinatura de documento | DocumentoAPI, AssinaturaAPI | Reagir a assinatura; notificar sistema externo |
| agendarPublicacao | Aps agendamento de publicacao | PublicacaoAPI | Reagir a agendamento; sincronizar |
| alterarPublicacao | Aps alteracao de publicacao | PublicacaoAPI | Reagir a alteracao; atualizar veiculo |
| confirmarPublicacao | Aps confirmacao de publicacao | PublicacaoAPI | Reagir a confirmacao; notificar |
| cancelarAgendamentoPublicacao | Aps cancelamento de agendamento | IdPublicacao | Reagir a cancelamento; atualizar status |
| montarDadosImprensaNacional | Retorna dados para impressa nacional | IdPublicacao | Montar dados DOU; formatar publicacao |
| obterProximaDataPublicacao | Retorna proxima data de publicacao em veiculo | VeiculoPublicacaoAPI | Calcular data de publicacao; agenda |
| montarTextoInformativoPublicacao | Adiciona texto informativo na publicacao | Sem parametro | Texto adicional na publicacao; aviso |
| alterarVeiculoPublicacao | Aps alteracao de veiculo de publicacao | VeiculoPublicacaoAPI | Reagir a alteracao de veiculo |
| cadastrarVeiculoPublicacao | Aps cadastro de novo veiculo | VeiculoPublicacaoAPI | Reagir a cadastro de veiculo |
| desativarVeiculoPublicacao | Aps desativacao de veiculo | VeiculoPublicacaoAPI | Reagir a desativacao; remover |

## Validação e Complemento

### Paginas com contrato detalhado

| Nome | Descrição | Entrada principal | Saída principal | Sinais de domínio | Quando usar |
|---|---|---|---|---|---|
| processarPaginaCadastroDocumento | Intercepta pagina de cadastro de documento | `DocumentoAPI` com `IdProcedimento`, `IdDocumento`, `IdSerie`, `Data`, `IdUnidadeGeradora`, `Numero`, `NomeArvore`, `DinValor`, `IdPlanoTrabalho` e `Tipo` | `PaginaComplementoAPI` | `plano de trabalho`, `cadastro de documento`, `complemento de pagina` | Modificar tela de cadastro; adicionar campos ou comportamento quando o documento estiver vinculado a plano de trabalho |
| processarPaginaInclusaoDocumentoItemEtapa | Intercepta pagina de inclusao de documento na etapa | `DocumentoAPI` com `IdProcedimento`, `IdSerie`, `IdPlanoTrabalho`, `IdEtapaTrabalho`, `IdItemEtapa` e `IdOperacao` | `PaginaComplementoAPI` | `plano de trabalho`, `etapa de trabalho`, `item de etapa`, `inclusao de documento` | Modificar inclusao de documento por etapa; injetar complemento de pagina; customizar fluxo vinculado a plano de trabalho |

### Outros eventos de validacao e complemento

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| validarContato | Valida dados de contato antes de gravar | ContatoAPI | Validar contato; regras de negocio |
| validarEliminacaoDocumento | Valida eliminacao de documento | DocumentoAPI | Bloquear eliminacao; validacao customizada |
| validarEliminacaoProcesso | Valida eliminacao de processo | ProcedimentoAPI | Bloquear eliminacao; validacao customizada |
| processarVariaveisEditor | Intercepta variaveis do editor de texto | Sem parametro especifico no catalogo; confirmar no manual | Adicionar variaveis customizadas ao editor |
| obterRelacaoVariaveisEditor | Retorna lista de variaveis disponiveis no editor | Sem parametro especifico no catalogo; confirmar no manual | Definir variaveis do editor; contexto |
| processarPesquisaRapida | Intercepta pesquisa rapida | Termo de busca | Customizar pesquisa rapida; filtros |

## Cadastro e Manutenção

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| cadastrarContato | Aps cadastro de contato | ContatoAPI | Reagir a novo contato; sincronizar |
| alterarContato | Aps alteracao de contato | ContatoAPI | Reagir a alteracao de contato; atualizar |
| excluirContato | Aps exclusao de contato | IdContato | Reagir a exclusao; remover vinculos |
| desativarContato | Aps desativacao de contato | ContatoAPI | Reagir a desativacao; inativar |
| reativarContato | Aps reativacao de contato | ContatoAPI | Reagir a reativacao; reativar |
| substituirContato | Aps substituicao de contato | ContatoAPI | Reagir a substituicao; migrar vinculos |
| cadastrarHipoteseLegal | Aps cadastro de hipotese legal | HipoteseLegalAPI | Reagir a nova hipotese; sincronizar |
| alterarHipoteseLegal | Aps alteracao de hipotese legal | HipoteseLegalAPI | Reagir a alteracao; atualizar |
| desativarHipoteseLegal | Aps desativacao de hipotese legal | HipoteseLegalAPI | Reagir a desativacao; inativar |
| reativarHipoteseLegal | Aps reativacao de hipotese legal | HipoteseLegalAPI | Reagir a reativacao |
| cadastrarArquivoExtensao | Aps cadastro de extensao de arquivo | ArquivoExtensaoAPI | Reagir a nova extensao; permitir |
| desativarArquivoExtensao | Aps desativacao de extensao | ArquivoExtensaoAPI | Reagir a desativacao; bloquear |
| reativarArquivoExtensao | Aps reativacao de extensao | ArquivoExtensaoAPI | Reagir a reativacao; permitir |
| excluirArquivoExtensao | Aps exclusao de extensao | IdArquivoExtensao | Reagir a exclusao; remover |
| cadastrarTipoDocumento | Aps cadastro de tipo de documento | TipoDocumentoAPI | Reagir a novo tipo; ativar |
| desativarTipoDocumento | Aps desativacao de tipo de documento | TipoDocumentoAPI | Reagir a desativacao; inativar |
| reativarTipoDocumento | Aps reativacao de tipo de documento | TipoDocumentoAPI | Reagir a reativacao |
| cadastrarTipoProcesso | Aps cadastro de tipo de processo | TipoProcedimentoAPI | Reagir a novo tipo; configurar |
| desativarTipoProcesso | Aps desativacao de tipo de processo | TipoProcedimentoAPI | Reagir a desativacao; inativar |
| reativarTipoProcesso | Aps reativacao de tipo de processo | TipoProcedimentoAPI | Reagir a reativacao |
| cadastrarUnidade | Aps cadastro de unidade | UnidadeAPI | Reagir a nova unidade; inicializar |
| desativarUnidade | Aps desativacao de unidade | UnidadeAPI | Reagir a desativacao; inativar |
| reativarUnidade | Aps reativacao de unidade | UnidadeAPI | Reagir a reativacao |
| cadastrarUsuario | Aps cadastro de usuario | UsuarioAPI | Reagir a novo usuario; inicializar |
| desativarUsuario | Aps desativacao de usuario | UsuarioAPI | Reagir a desativacao; bloquear acesso |
| reativarUsuario | Aps reativacao de usuario | UsuarioAPI | Reagir a reativacao; desbloquear |
| cadastrarVeiculoPublicacao | Aps cadastro de veiculo | VeiculoPublicacaoAPI | Reagir a novo veiculo; configurar |
| desativarVeiculoPublicacao | Aps desativacao de veiculo | VeiculoPublicacaoAPI | Reagir a desativacao; inativar |
| reativarVeiculoPublicacao | Aps reativacao de veiculo | VeiculoPublicacaoAPI | Reagir a reativacao |
| excluirVeiculoPublicacao | Aps exclusao de veiculo | IdVeiculoPublicacao | Reagir a exclusao; remover |
| alterarVeiculoPublicacao | Aps alteracao de veiculo | VeiculoPublicacaoAPI | Reagir a alteracao; atualizar |
| listarUnidadesEnvioProcesso | Lista unidades disponiveis para envio | Sem parametro | Filtrar unidades de envio; customizar |
| inicializar | Executa ao inicializar o modulo (boot) | Sem parametro | Inicializar recursos; configurar ambiente |

## Mensagens e Status

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| montarMensagemProcesso | Adiciona mensagem na tela de processo | ProcedimentoAPI | Mensagem personalizada; aviso, alerta |

## Notas sobre ambiguidades do manual

1. Varios eventos de ciclo de vida (alterarProcesso, alterarDocumento, etc.) nao deixam claro se a trigger ocorre ANTES ou DEPOIS da operacao no core. Em caso de necessidade de interceptacao antes da escrita, verificar a assinatura real em `SeiIntegracao.php`.

2. Eventos de cadastro/manutencao (cadastrar*, desativar*, reativar*, excluir*) parecem ser todos do tipo POS-operacao (apos a escrita no banco). Nao foram encontrados eventos PRE-operacao para essas ações.

3. `listarUnidadesEnvioProcesso` tem assinatura minima não especificada no manual — verificar no fonte antes de implementar.

4. `montarBotaoChatIA` aparece no catalogo mas nao tem documentação de parametro ou comportamento detalhado. Tratar como extensibilidade via botão customizado.

5. Para eventos que recebem arrays grandes (ate 200 objetos), o manual adverte sobre performance: evitar consultas individuais dentro do loop. Considerar consulta em lote com `IN` antes de implementar.
