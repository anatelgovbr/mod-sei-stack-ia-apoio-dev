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
| desanexarProcesso | Apos desanexar processo | `objProcedimentoAPIPrincipal` e `objProcedimentoAPIAnexado`, cada um com IdProcedimento e NumeroProtocolo, sem motivo | Reagir a desanexacao; atualizar sistemas |
| relacionarProcesso | Apos criar relacionamento lateral entre processos | Ids dos processos relacionados | Reagir ao vinculo lateral; atualizar sistema |
| removerRelacionamentoProcesso | Aps remover relacionamento entre processos | Ids dos processos | Reagir a remocao de vinculo |
| enviarProcesso | Apos envio de processo a outra unidade | ProcedimentoAPI, lista de unidades | Reagir a envio; notificar sistema externo |
| concluirProcesso | Aps conclusao de processo na unidade | ProcedimentoAPI | Reagir a conclusao; atualizar carga |
| reabrirProcesso | Aps reabertura de processo na unidade | ProcedimentoAPI | Reagir a reabertura; reativar carga |
| bloquearProcesso | Aps bloqueio de processo | `arrObjProcedimentoAPI` com IdProcedimento e NumeroProtocolo, sem motivo | Reagir a bloqueio; restringir acesso externo |
| desbloquearProcesso | Aps desbloqueio de processo | ProcedimentoAPI | Reagir a desbloqueio; restaurar acesso |
| sobrestarProcesso | Aps sobrestamento de processo | `objProcedimentoAPI` e `objProcedimentoAPIVinculado`, o vinculado nulo quando nao houver, sem motivo | Reagir a sobrestamento; impedir tramite |
| removerSobrestamentoProcesso | Aps remover sobrestamento | ProcedimentoAPI | Reagir a remoção de sobrestamento |
| moverDocumento | Aps mover documento na árvore | `objDocumentoAPI`, `objProcedimentoAPIOrigem` e `objProcedimentoAPIDestino` | Reagir a reorganização de documento na árvore |
| cancelarDocumento | Aps cancelamento de documento | DocumentoAPI | Reagir a cancelamento; invalidar copia |
| eliminarDocumento | Aps eliminacao de documento | DocumentoAPI | Reagir a eliminacao; remover vínculo externo |
| eliminarProcesso | Aps eliminacao de processo | ProcedimentoAPI | Reagir a eliminacao; remover vínculo |
| confirmarAtualizacaoConteudoDocumento | Confirma atualizacao de conteudo de documento | DocumentoAPI | Confirmar atualização; aceitar ou recusar mudanca |
| prepararCloneDocumento | Prepara clone de documento para geracao | DocumentoAPI | Interceptar geracao de documento clone |
| darCienciaDocumento | Aps receber ciencia de documento | DocumentoAPI | Reagir a ciencia; marcar como visualizado |
| darCienciaProcesso | Aps receber ciencia de processo | ProcedimentoAPI | Reagir a ciencia de processo |
| permitirAndamentoConcluido | Antes de permitir conclusao de processo | `objAndamentoAPI` com IdProtocolo e IdTarefa, mais `bolPermitir` | Validar condicoes para conclusao; bloquear se necessário |

## UI — Ícones e Botões

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| montarIconeControleProcessos | Adiciona icones na tela de Controle de Processos | Lista de ProcedimentoAPI (ate 200) | Adicionar icone customizado na linha do processo; status especial |
| montarIconeProcesso | Adiciona icone na visualizacao de processo | ProcedimentoAPI | Adicionar icone na tela de processo; badge |
| montarIconeDocumento | Adiciona icone na arvore de documentos | DocumentoAPI | Adicionar icone no documento; indicador de status |
| montarIconeSistema | Adiciona icone na barra de titulo do SEI | Sem parametro | Icone na barra superior do sistema; logo customizado |
| montarIconeAcompanhamentoEspecial | Adiciona icone na tela de Acompanhamento Especial | ProcedimentoAPI | Badge de acompanhamento especial |
| montarIconeOrdenarArvore | Adiciona controle de ordenacao na árvore | `objProcedimentoAPI` com IdProcedimento, mais `strIcone` | Botao de ordenacao personalizado |
| alterarIconeArvoreDocumento | Altera icone de documento na arvore | `objProcedimentoAPI`, `arrObjDocumentoAPI`, `arrIcones` indexado por id de documento | Substituir icone padrao por customizado |
| montarBotaoControleProcessos | Adiciona botoes na tela de Controle de Processos | `arrBotoes`, array PHP com um item por botao, SVG 24x24 | Adicionar botao de acao rapida; shortcut |
| montarBotaoProcesso | Adiciona botoes na tela de visualizacao de processo | ProcedimentoAPI | Botao de acao no processo; ferramenta |
| montarBotaoDocumento | Adiciona botoes na arvore de documentos | DocumentoAPI | Botao de acao no documento; download, info |
| montarBotaoCadastroDocumento | Adiciona botoes na tela de cadastro de documento | `objDocumentoAPI` com IdProcedimento, IdDocumento, IdSerie, Data, IdUnidadeGeradora, Numero, NomeArvore, DinValor, IdPlanoTrabalho e Tipo, mais `arrBotoes` | Acoes na tela de inclusao de documento |
| montarBotaoChatIA | Adiciona botao de chat IA na interface | Sem parametro | Botao de interacao com IA; integração |
| montarBotaoLoginExterno | Adiciona botao na tela de login externo | Sem parametro | Botao customizado no login externo |
| montarBotaoAcessoExternoAutorizado | Adiciona botoes na área de acesso externo autorizado | Contexto de acesso externo | Acoes para usuário externo autenticado |
| montarBotaoControleAcessoExterno | Adiciona botoes no controle de acesso externo | Contexto de acesso externo | Acoes de controle; revogar, limitar |
| montarBotaoAssinaturaInterno | Adiciona botoes na area de assinatura interno | `objUsuarioAPI` com IdUsuario, Sigla, Nome e StaTipo, mais `strHtml` | Acoes complementares na assinatura interna |
| montarBotaoAssinaturaExterno | Adiciona botoes na area de assinatura externo | `objUsuarioAPI` com IdUsuario, Sigla, Nome e StaTipo, mais `strHtml` | Acoes complementares na assinatura externa |
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
| ocultarAcaoAlterarPublicacao | Oculta acao de alterar publicacao | entrada `arrObjPublicacaoAPI`, saida `arrIdPublicacao` a ocultar | Ocultar botão de alteração de publicação |
| ocultarAcaoCancelarAgendamentoPublicacao | Oculta acao de cancelar agendamento | entrada `arrObjPublicacaoAPI` com IdPublicacao, IdDocumento e Estado, saida `arrIdPublicacao` | Ocultar botão de cancelamento |
| ocultarBotaoSalvarPublicacao | Oculta botao de salvar publicacao | entrada `arrObjVeiculoPublicacaoAPI`, saida `arrIdVeiculoPublicacao` | Ocultar botão de salvar publicação |
| ocultarDadosImprensaNacionalPublicacao | Oculta dados da Imprensa Nacional na publicacao | entrada `arrObjVeiculoPublicacaoAPI` com IdVeiculoPublicacao e Tipo, saida `arrIdVeiculoPublicacao` | Ocultar seção de DOU na publicação |

## Segurança e Acesso

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| verificarAcessoProtocolo | Verifica acesso a protocolo na tela interna | entrada `$arrObjProcedimentoAPI` (IdProcedimento, IdTipoProcedimento, IdUnidadeGeradora, NivelAcesso) e `$arrObjDocumentoAPI`, saida `$arrLiberacoes` indexado pelo protocolo com P ou N | Controlar acesso a processo/documento internamente |
| verificarAcessoProtocoloExterno | Verifica acesso a protocolo via acesso externo | entrada `$arrObjProcedimentoAPI` e `$arrObjDocumentoAPI` (com SinAssinado e SinPublicado), saida `$arrLiberacoes` indexado pelo protocolo com P ou N | Controlar acesso externo; validar permissoes |
| verificarAcessoTipoContato | Verifica acesso por tipo de contato | entrada `$arrObjTipoContatoAPI` com IdTipoContato, saida `$arrLiberacoes` indexado pelo tipo com N, A, C ou R | Controlar acesso por tipo de pessoa |
| verificarLoginExterno | Verifica credenciais de login externo | Credenciais | Autenticar usuario externo; customizar login |
| cancelarDisponibilizacaoAcessoExterno | Cancela disponibilizacao de acesso externo | IdAcessoExterno | Revogar acesso externo; encerrar sessão |
| cancelarLiberacaoAssinaturaExterna | Cancela liberacao de assinatura externa | Identificador de liberacao | Revogar liberacao de assinatura; desatrelhar |

## Assinatura e Publicação

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| obterConfiguracoesAssinatura | Retorna configuracoes de assinatura | `objConfiguracoesAssinaturaAPI` com NomeModulo | Customizar comportamento de assinatura; Plugins |
| prepararAssinaturaDocumento | Prepara documento para assinatura | `objAssinaturaAPI` com IdUsuario, Sigla, Nome, CargoFuncao, Cpf, StaFormaAutenticacao e Agrupador | Interceptar preparacao de assinatura; adicionar validacao |
| assinarDocumento | Aps assinatura de documento | `arrObjDocumentoAPI` com IdDocumento, IdProcedimento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, IdUsuarioGerador | Reagir a assinatura; notificar sistema externo |
| agendarPublicacao | Aps agendamento de publicacao | PublicacaoAPI | Reagir a agendamento; sincronizar |
| alterarPublicacao | Aps alteracao de publicacao | PublicacaoAPI | Reagir a alteracao; atualizar veiculo |
| confirmarPublicacao | Aps confirmacao de publicacao | PublicacaoAPI | Reagir a confirmacao; notificar |
| cancelarAgendamentoPublicacao | Aps cancelamento de agendamento | IdPublicacao | Reagir a cancelamento; atualizar status |
| montarDadosImprensaNacional | Retorna dados para impressa nacional | IdPublicacao | Montar dados DOU; formatar publicacao |
| obterProximaDataPublicacao | Retorna proxima data de publicacao em veiculo | `objPublicacaoAPI` com IdVeiculoPublicacao e StaTipoVeiculo, mais data `InfraData` | Calcular data de publicacao; agenda |
| montarTextoInformativoPublicacao | Adiciona texto informativo na publicacao | `objPublicacaoAPI` com IdPublicacao, IdVeiculoPublicacao, StaTipoVeiculo e IdDocumento | Texto adicional na publicacao; aviso |
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
| desativarTipoDocumento | Aps desativacao de tipo de documento | `arrObjSerieAPI` com IdSerie, Nome e Aplicabilidade | Reagir a desativacao; inativar |
| reativarTipoDocumento | Aps reativacao de tipo de documento | `arrObjSerieAPI` com IdSerie, Nome e Aplicabilidade | Reagir a reativacao |
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
| listarUnidadesEnvioProcesso | Lista unidades disponiveis para envio | entrada `arrObjProcedimentoAPI`, saida `arrObjUnidadeAPI` com IdUnidade | Filtrar unidades de envio; customizar |
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

## Controle de acesso a protocolo e a tipo de contato

Regras que o capitulo 9 fixa para os eventos `verificarAcessoProtocolo`, `verificarAcessoProtocoloExterno` e `verificarAcessoTipoContato`. Sao eventos de seguranca, entao o valor exato importa.

### Constantes de retorno

Classe `SeiIntegracao`, usada em `verificarAcessoProtocolo` e `verificarAcessoProtocoloExterno`. O comentario do manual explica a sigla: TAM significa Tipo Acesso Modulo.

| Constante | Valor | Significado |
|---|---|---|
| `SeiIntegracao::$TAM_PERMITIDO` | `P` | acesso permitido pelo modulo |
| `SeiIntegracao::$TAM_NEGADO` | `N` | acesso negado pelo modulo |

Classe `TipoContatoRN`, usada em `verificarAcessoTipoContato`.

| Constante | Valor | Significado |
|---|---|---|
| `TipoContatoRN::$TA_NENHUM` | `N` | nenhum acesso concedido pelo modulo |
| `TipoContatoRN::$TA_ALTERACAO` | `A` | permissao para alteracao de dados |
| `TipoContatoRN::$TA_CONSULTA_COMPLETA` | `C` | consulta completa |
| `TipoContatoRN::$TA_CONSULTA_RESUMIDA` | `R` | consulta resumida |

### A negacao tem prioridade

Em situacao de conflito entre modulos, quando um modulo permite acesso e outro nega, **a negacao prevalece**.

Consequencia de projeto: um modulo nao pode assumir que a propria liberacao vence. Se o requisito for garantir acesso, a liberacao por evento nao basta, porque outro modulo instalado no mesmo SEI pode negar.

### Toda visualizacao de protocolo e auditada

O manual registra que todas as visualizacoes de processos ou documentos serao auditadas. O modulo nao precisa registrar auditoria propria de visualizacao, e nao deve suprimir a do core.

### Alerta do manual

Estes eventos exigem cuidado redobrado na elaboracao, porque falha na logica de programacao expoe indevidamente informacao restrita ou sigilosa. Tratar alteracao nesses metodos como mudanca de seguranca, com revisao proporcional.

### Sinalizacao na arvore

Quando o acesso for concedido exclusivamente pelo modulo, a arvore do processo exibe cadeado aberto identificando o modulo que liberou. Quando for negado exclusivamente pelo modulo, exibe cadeado fechado.

---

## Contratos completos dos eventos

| Evento | Entrada | Saida |
|---|---|---|
| `adicionarElementoMenu` | sem entrada documentada | `strElemento`: Conteúdo HTML para inclusão abaixo do menu. |
| `agendarPublicacao` | `$objPublicacaoAPI`: Instância preenchida com IdPublicacao, IdDocumento, IdVeiculoPublicacao, StaTipoVeiculo e DataDisponibilizacao. | sem saida documentada |
| `alterarContato` | `$objContatoAPI`: Instância preenchida com IdContato, IdTipoContato, IdContatoAssociado, StaNatureza, SinEnderecoAssociado, StaGenero, Cpf, Rg, OrgaoExpedidor, Matricula, MatriculaOab, NumeroPassaporte, IdPaisPassaporte, DataNascimento, Cnpj, IdCargo, Sigla, Nome, NomeSocial, TelefoneFixo, TelefoneCelular, Email, SitioInternet, Endereco, Complemento, Bairro, Cep, Observacao, SinAtivo, IdPais, IdEstado e IdCidade. | sem saida documentada |
| `alterarDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento, NumeroProtocolo, IdProcedimento, IdSerie, NivelAcesso, SubTipo, Numero, Data, IdUnidadeGeradora, DinValor, IdPlanoTrabalho e AtributosModulo. | sem saida documentada |
| `alterarHipoteseLegal` | `$objHipoteseLegalAPI`: Instância preenchida com IdHipoteseLegal, Nome, Descricao, BaseLegal, NivelAcesso e SinAtivo. | sem saida documentada |
| `alterarIconeArvoreDocumento` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, IdHipoteseLegal, GrauSigilo, CodigoAcesso e SinAberto.; `$arrObjDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, NomeSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, SinAssinado, SinPublicado, SinBloqueado, CodigoAcesso, Tipo e SubTipo. | `arrIcones`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém o caminho para a imagem. Documentos que não devem ter o ícone alterado pelo módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `alterarProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento, IdTipoProcedimento e IdTipoPrioridade. | sem saida documentada |
| `alterarPublicacao` | `$objPublicacaoAPI`: Instância preenchida com IdPublicacao, IdDocumento, IdVeiculoPublicacao, StaTipoVeiculo e DataDisponibilizacao. | sem saida documentada |
| `alterarVeiculoPublicacao` | `$objVeiculoPublicacaoAPI`: Instância preenchida com IdVeiculoPublicacao, Nome, Descricao, StaTipo, SinFonteFeriados, SinPermiteExtraordinaria, SinExibirPesquisaInterna, WebService e SinAtivo. | sem saida documentada |
| `anexarProcesso` | `$objProcedimentoAPIPrincipal`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPIAnexado`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `assinarDocumento` | `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento, IdProcedimento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, IdUsuarioGerador, Tipo, SubTipo e NivelAcesso. | sem saida documentada |
| `atualizarConteudoDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento. | sem saida documentada |
| `bloquearProcesso` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `cadastrarContato` | `$objContatoAPI`: Instância preenchida com IdContato, IdTipoContato, IdContatoAssociado, StaNatureza, SinEnderecoAssociado, StaGenero, Cpf, Rg, OrgaoExpedidor, Matricula, MatriculaOab, NumeroPassaporte, IdPaisPassaporte, DataNascimento, Cnpj, IdCargo, Sigla, Nome, NomeSocial, TelefoneFixo, TelefoneCelular, Email, SitioInternet, Endereco, Complemento, Bairro, Cep, Observacao, SinAtivo, IdPais, IdEstado e IdCidade. | sem saida documentada |
| `cadastrarHipoteseLegal` | `$objHipoteseLegalAPI`: Instância preenchida com IdHipoteseLegal, Nome, Descricao, BaseLegal, NivelAcesso e SinAtivo. | sem saida documentada |
| `cadastrarVeiculoPublicacao` | `$objVeiculoPublicacaoAPI`: Instância preenchida com IdVeiculoPublicacao, Nome, Descricao, StaTipo, SinFonteFeriados, SinPermiteExtraordinaria, SinExibirPesquisaInterna, WebService e SinAtivo. | sem saida documentada |
| `cancelarAgendamentoPublicacao` | `$objPublicacaoAPI`: Instância preenchida com IdPublicacao, IdDocumento, IdVeiculoPublicacao, StaTipoVeiculo e DataDisponibilizacao. | sem saida documentada |
| `cancelarDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SubTipo e NivelAcesso. | sem saida documentada |
| `cancelarDisponibilizacaoAcessoExterno` | `$arrObjAcessoExternoAPI`: Instâncias preenchidas com IdAcessoExterno e Procedimento.IdProcedimento. | sem saida documentada |
| `cancelarLiberacaoAssinaturaExterna` | `$arrObjAcessoExternoAPI`: Instâncias preenchidas com IdAcessoExterno, Procedimento.IdProcedimento e Documento.IdDocumento. | sem saida documentada |
| `confirmarAtualizacaoConteudoDocumento` | `objDocumentoAPI`: Ocorrência de DocumentoAPI preenchida com IdDocumento. | `strMensagem`: Mensagem que será exibida antes de salvar o documento seguida pelo texto Deseja salvar o documento? |
| `confirmarPublicacao` | `$arrObjPublicacaoAPI`: Instâncias preenchidas com IdPublicacao, IdDocumento, IdSerieDocumento, IdVeiculoPublicacao, StaTipoVeiculo, DataDisponibilizacao e DataPublicacao. | sem saida documentada |
| `concluirProcesso` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento. | sem saida documentada |
| `darCienciaDocumento` | `$objDocumentoAPI`: Instâncias preenchidas com IdDocumento, IdProcedimento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, IdUsuarioGerador, Tipo, SubTipo e NivelAcesso. | sem saida documentada |
| `darCienciaProcesso` | `$objProcedimentoAPI`: Instâncias preenchidas com IdProcedimento, NumeroProtocolo, IdTipoProcedimento, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, IdUsuarioGerador e NivelAcesso. | sem saida documentada |
| `desanexarProcesso` | `$objProcedimentoAPIPrincipal`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPIAnexado`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `desativarArquivoExtensao` | `$arrObjArquivoExtensaoAPI`: Instâncias preenchidas com IdArquivoExtensao e Extensao. | sem saida documentada |
| `desativarContato` | `$arrObjContatoAPI`: Instâncias preenchidas com IdContato, IdTipoContato, IdContatoAssociado, Sigla, Nome e NomeSocial. | sem saida documentada |
| `desativarHipoteseLegal` | `$arrObjHipoteseLegalAPI`: Instâncias preenchidas com IdHipoteseLegal, Nome, BaseLegal e NivelAcesso. | sem saida documentada |
| `desativarTipoContato` | `$arrObjTipoContatoAPI`: Instâncias preenchidas com IdTipoContato e Nome. | sem saida documentada |
| `desativarTipoDocumento` | `$arrObjSerieAPI`: Instâncias preenchidas com IdSerie, Nome e Aplicabilidade. | sem saida documentada |
| `desativarTipoProcesso` | `$arrObjTipoProcedimentoAPI`: Instâncias preenchidas com IdTipoProcedimento e Nome. | sem saida documentada |
| `desativarUnidade` | `$arrObjUnidadeAPI`: Instâncias preenchidas com IdUnidade, Sigla e Descricao. | sem saida documentada |
| `desativarUsuario` | `$arrObjUsuarioAPI`: Instâncias preenchidas com IdUsuario, Sigla, Nome e StaTipo. | sem saida documentada |
| `desativarVeiculoPublicacao` | `$arrObjVeiculoPublicacaoAPI`: Instâncias preenchidas com IdVeiculoPublicacao. | sem saida documentada |
| `desbloquearProcesso` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `eliminarDocumento` | `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento e NumeroProtocolo. | sem saida documentada |
| `eliminarProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `enviarProcesso` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento e IdUnidadeGeradora.; `$arrObjUnidadeAPI`: Instâncias preenchidas com IdUnidade, Sigla, Descricao e OrgaoAPI (IdOrgao, Sigla, Descricao). | sem saida documentada |
| `excluirArquivoExtensao` | `$arrObjArquivoExtensaoAPI`: Instâncias preenchidas com IdArquivoExtensao e Extensao. | sem saida documentada |
| `excluirContato` | `$arrObjContatoAPI`: Instâncias preenchidas com IdContato, IdTipoContato, IdContatoAssociado, Sigla, Nome e NomeSocial. | sem saida documentada |
| `excluirDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento. | sem saida documentada |
| `excluirHipoteseLegal` | `$arrObjHipoteseLegalAPI`: Instâncias preenchidas com IdHipoteseLegal, Nome, BaseLegal e NivelAcesso. | sem saida documentada |
| `excluirProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento. | sem saida documentada |
| `excluirTipoContato` | `$arrObjTipoContatoAPI`: Instâncias preenchidas com IdTipoContato e Nome. | sem saida documentada |
| `excluirTipoDocumento` | `$arrObjSerieAPI`: Instâncias preenchidas com IdSerie, Nome e Aplicabilidade. | sem saida documentada |
| `excluirTipoProcesso` | `$arrObjTipoProcedimentoAPI`: Instâncias preenchidas com IdTipoProcedimento e Nome. | sem saida documentada |
| `excluirUnidade` | `$arrObjUnidadeAPI`: Instâncias preenchidas com IdUnidade, Sigla e Descricao. | sem saida documentada |
| `excluirUsuario` | `$arrObjUsuarioAPI`: Instâncias preenchidas com IdUsuario, Sigla, Nome e StaTipo. | sem saida documentada |
| `excluirVeiculoPublicacao` | `$arrObjVeiculoPublicacaoAPI`: Instâncias preenchidas com IdVeiculoPublicacao. | sem saida documentada |
| `gerarDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento, NumeroProtocolo, IdProcedimento, IdSerie, NivelAcesso, SubTipo, Numero, Data, IdUnidadeGeradora, DinValor, IdPlanoTrabalho, IdEtapaTrabalho, IdItemEtapa, IdOperacao e AtributosModulo. | sem saida documentada |
| `gerarProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento, NumeroProtocolo, IdTipoProcedimento, IdTipoPrioridade e NivelAcesso. | sem saida documentada |
| `Inicializar` | `strVersaoSEI`: Número da versão do SEI (exemplo: 3.1.0). | sem saida documentada |
| `listarUnidadesEnvioProcesso` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento e IdUnidadeGeradora. | `$arrObjUnidadeAPI`: Instâncias preenchidas com IdUnidade. |
| `montarAcaoControleAcessoExterno` | `arrAcessoExternoAPI`: Conjunto de ocorrências de AcessoExternoAPI preenchidas com: IdAcessoExterno, DataValidade, SinAcessoProcesso, Procedimento (ocorrência de ProcedimentoAPI preenchida com IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade e NivelAcesso), Documento (ocorrência de DocumentoAPI preenchida com IdDocumento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SinAssinado, SinPublicado e NivelAcesso). | `arrIcones`: Um array PHP indexado pelos IDs dos acessos externos onde cada posição contém outro array com o conjunto de ícones para exibição. Acessos externos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoDocumentoAcessoExternoAutorizado` | `arrDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SinAssinado, SinPublicado e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém outro array com o conjunto de ícones para exibição. Documentos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoDocumentoAcessoExternoNegado` | `arrDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SinAssinado, SinPublicado e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém outro array com o conjunto de ícones para exibição. Documentos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoProcessoAnexadoAcessoExternoAutorizado` | `arrProcedimentoAPI`: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoProcessoAnexadoAcessoExternoNegado` | `arrProcedimentoAPI`: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoPublicacao` | `arrObjPublicacaoAPI`: Conjunto de ocorrências de PublicacaoAPI preenchidas com: IdPublicacao, IdDocumento e Estado. | `arrIcones`: Um array PHP indexado pelos IDs das publicações que possuem ações liberadas pelo módulo. Cada posição contém outro array com o conjunto de ícones para exibição. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoVeiculoPublicacao` | `arrObjVeiculoPublicacaoAPI`: Conjunto de ocorrências de VeiculoPublicacaoAPI preenchidas com: IdVeiculoPublicacao e Nome. | `arrIcones`: Um array PHP indexado pelos IDs dos veículos que possuem ações liberadas pelo módulo. Cada posição contém outro array com o conjunto de ícones para exibição. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarBotaoAcessoExternoAutorizado` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade e NivelAcesso. | `arrBotoes`: Um array PHP onde cada item representa um botão. |
| `montarBotaoAssinaturaExterno` | `objUsuarioAPI`: Ocorrência de UsuarioAPI preenchida com: IdUsuario, Sigla, Nome e StaTipo. | `strHtml`: Código HTML do botão. |
| `montarBotaoAssinaturaInterno` | `objUsuarioAPI`: Ocorrência de UsuarioAPI preenchida com: IdUsuario, Sigla, Nome e StaTipo. | `strHtml`: Código HTML do botão. |
| `montarBotaoChatIA` | sem entrada documentada | `strBotao`: Texto com o código do botão para inclusão na página. |
| `montarBotaoControleAcessoExterno` | sem entrada documentada | `arrBotoes`: Um array PHP onde cada item representa um botão. |
| `montarBotaoControleProcessos` | sem entrada documentada | `arrBotoes`: Um array PHP onde cada item representa um botão. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarBotaoDocumento` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto.; `$arrObjDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, NomeSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, SinAssinado, SinPublicado, SinBloqueado, CodigoAcesso, Tipo, SubTipo. | `arrBotoes`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém outro array com o conjunto de botões para exibição junto ao documento. Documentos que não devem exibir botões do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 40x40. |
| `montarBotaoCadastroDocumento` | `objDocumentoAPI`: Ocorrência de DocumentoAPI preenchida com: IdProcedimento, IdDocumento, IdSerie, Data, IdUnidadeGeradora, Numero, NomeArvore, DinValor, IdPlanoTrabalho e Tipo. | `arrBotoes`: Um array PHP onde cada item representa um botão. |
| `montarBotaoLoginExterno` | sem entrada documentada | `strHtml`: Código HTML do botão. |
| `montarBotaoProcesso` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto. | `arrBotoes`: Um array PHP onde cada item representa um botão. Para as imagens é recomendado utilizar o formato SVG com tamanho 40x40. |
| `montarBotaoVeiculoPublicacao` | `arrObjVeiculoPublicacaoAPI`: Conjunto de ocorrências de VeiculoPublicacaoAPI preenchidas com: IdVeiculoPublicacao e Tipo. | `arrBotoes`: Um array indexado pelos Ids dos veículos de publicação e pelos identificadores dos botões contendo o código html do botão. é importante que o ID do botão informado no índice do array seja o mesmo da tag id do html, pois essa informação será utilizada para controlar a visualização de acordo com o veículo selecionado na tela. |
| `montarDadosImprensaNacional` | `objPublicacaoAPI`: Instância de PublicacaoAPI preenchida com: IdPublicacao, IdVeiculoPublicacao e StaTipoVeiculo. | `texto`: Texto da Imprensa Nacional para exibição na tela de publicações do documento, na tela de pesquisa de publicações e no carimbo de publicação do documento. |
| `montarIconeAcompanhamentoEspecial` | `arrObjProcedimentoAPI`: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora e IdOrgaoUnidadeGeradora. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição junto ao processo. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarIconeControleProcessos` | `arrObjProcedimentoAPI`: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora e IdOrgaoUnidadeGeradora. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição junto ao processo. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarIconeDocumento` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto.; `$arrObjDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, NomeSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, SinAssinado, SinPublicado, SinBloqueado, CodigoAcesso, Tipo, SubTipo. | `arrIcones`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém um array de ocorrências de ArvoreAcaoItemAPI com os ícones para exibição junto ao documento. Documentos que não devem exibir ícones do módulo não precisam estar no array. |
| `montarIconeOrdenarArvore` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento. | `$strIcone`: Ícone para exibição. |
| `montarIconeProcesso` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto. | `arrObjArvoreAcaoItemAPI`: Conjunto de ocorrências da estrutura ArvoreAcaoItemAPI. |
| `montarIconeSistema` | sem entrada documentada | `arrIcones`: Um array PHP com o conjunto de ícones para exibição na barra superior. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarMensagemProcesso` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto. | `strMsg`: Texto da mensagem. |
| `montarMenuConsultaProcessual` | sem entrada documentada | `$arrItens`: Um array de itens montados com a estrutura: *[nível]\^[url]\^[título]\^[rótulo]\^[target (opcional)]* Onde o nível é representado pelo número de "hífens" informados. |
| `montarMenuPublicacoes` | sem entrada documentada | `$arrItens`: Um array de itens montados com a estrutura: *[nível]\^[url]\^[título]\^[rótulo]\^[target (opcional)]* Onde o nível é representado pelo número de hífens informados. |
| `montarMenuUsuarioExterno` | sem entrada documentada | `$arrItens`: Um array de itens montados com a estrutura: *[nível]\^[url]\^[título]\^[rótulo]\^[target (opcional)]* Onde o nível é representado pelo número de hífens informados. |
| `montarTextoInformativoPublicacao` | `objPublicacaoAPI`: Instância de PublicacaoAPI preenchida com: IdPublicacao, IdVeiculoPublicacao, StaTipoVeiculo e IdDocumento. | `texto`: Texto para exibição junto ao documento após a publicação. |
| `moverDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento e NumeroProtocolo.; `$objProcedimentoAPIOrigem`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPIDestino`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `obterAcoesAjaxExternasSemLogin` | sem entrada documentada | `$arrAcoes`: Conjunto de ações. |
| `obterAcoesExternasSemLogin` | sem entrada documentada | `$arrAcoes`: Conjunto de ações. |
| `obterConfiguracoesAssinatura` | `objConfiguracoesAssinaturaAPI`: Instância de ConfiguracoesAssinaturaAPI preenchida com NomeModulo. | `$objConfiguracoesAssinaturaAPI`: Instância com as configurações do módulo. |
| `obterDiretorioIconesMenu` | sem entrada documentada | `$strDiretorio`: Caminho do diretório que contém as imagens associadas com itens de menu. |
| `obterProximaDataPublicacao` | `objPublicacaoAPI`: Instância de PublicacaoAPI preenchida com: IdVeiculoPublicacao e StaTipoVeiculo. | `data`: Próxima data disponível para o veículo no formato dd/mm/aaaa. |
| `obterRelacaoVariaveisEditor` | sem entrada documentada | `$arrVariaveis`: Conjunto onde a chave é o nome da variável e o valor é sua descrição. |
| `ocultarAcaoAlterarPublicacao` | `arrObjPublicacaoAPI`: Conjunto de ocorrências de PublicacaoAPI preenchidas com: IdPublicacao, IdDocumento e Estado. | `arrIdPublicacao`: Um array com os Ids das publicações que não devem exibir o ícone padrão de alteração. |
| `ocultarAcaoCancelarAgendamentoPublicacao` | `arrObjPublicacaoAPI`: Conjunto de ocorrências de PublicacaoAPI preenchidas com: IdPublicacao, IdDocumento e Estado. | `arrIdPublicacao`: Um array com os Ids das publicações que não devem exibir o ícone padrão Cancelar Agendamento. Esse ícone é exibido quando o documento está no Estado A (Agendado). |
| `ocultarBotaoSalvarPublicacao` | `arrObjVeiculoPublicacaoAPI`: Conjunto de ocorrências de VeiculoPublicacaoAPI preenchidas com: IdVeiculoPublicacao e Tipo. | `arrIdVeiculoPublicacao`: Um array com os Ids dos veículos de publicação que não devem exibir o botão padrão Salvar. |
| `ocultarDadosImprensaNacionalPublicacao` | `arrObjVeiculoPublicacaoAPI`: Conjunto de ocorrências de VeiculoPublicacaoAPI preenchidas com: IdVeiculoPublicacao e Tipo. | `arrIdVeiculoPublicacao`: Um array com os Ids dos veículos de publicação que não devem exibir os campos para preenchimento dos dados da Imprensa Nacional. |
| `permitirAndamentoConcluido` | `$objAndamentoAPI`: Instância preenchida com IdProtocolo e IdTarefa. | `$bolPermitir`: Retornar true para permitir lançar o andamento concluído. |
| `prepararAssinaturaDocumento` | `$objAssinaturaAPI`: Instância preenchida com IdUsuario, Sigla, Nome, CargoFuncao, Cpf, StaFormaAutenticacao e Agrupador. | sem saida documentada |
| `prepararCloneDocumento` | `$objDocumentoAPI`: Instância preenchida com IdProcedimento e IdDocumento. | `$objDocumentoAPI`: Instância preenchida opcionalmente com Data e/ou AtributosModulo. |
| `processarControlador` | `$strAcao`: Ação recebida na URL. | sem saida documentada |
| `processarControladorAjax` | `$strAcaoAjax`: Ação ajax recebida na URL. | sem saida documentada |
| `processarControladorAjaxExterno` | `$strAcaoAjax`: Ação ajax recebida na URL. | sem saida documentada |
| `processarControladorExterno` | `$strAcao`: Ação recebida na URL. | sem saida documentada |
| `processarControladorPublicacoes` | `$strAcao`: Ação recebida na URL. | sem saida documentada |
| `processarControladorWebServices` | `$strServico`: Serviço recebido na URL.; Observação; O WSDL poderá ser referenciado por: https://[servidor]/sei/controlador_ws.php?servico=[nome do serviço do módulo] | sem saida documentada |
| `processarPaginaCadastroDocumento` | `$objDocumentoAPI`: Instância preenchida com IdProcedimento, IdDocumento, IdSerie, Data, IdUnidadeGeradora, Numero, NomeArvore, DinValor, IdPlanoTrabalho e Tipo. | `$objPaginaComplementoAPI`: Objeto com código para inserção de comportamento na página. |
| `processarPaginaInclusaoDocumentoItemEtapa` | `$objDocumentoAPI`: Instância preenchida com IdProcedimento, IdSerie, IdPlanoTrabalho, IdEtapaTrabalho, IdItemEtapa e IdOperacao. | `$objPaginaComplementoAPI`: Objeto com código para inserção de comportamento na página. |
| `processarPesquisaRapida` | `$strTexto`: Texto preenchido pelo usuário. | sem saida documentada |
| `processarVariaveisEditor` | `$objDocumentoAPI`: Instância preenchida com IdProcedimento e IdDocumento.. | `$arrVariaveis`: Conjunto de valores onde a chave é o nome da variável.; Observação; Serão consideradas somente as variáveis retornadas pelo método obterRelacaoVariaveisEditor. |
| `reabrirProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento. | sem saida documentada |
| `reativarArquivoExtensao` | `$arrObjArquivoExtensaoAPI`: Instâncias preenchidas com IdArquivoExtensao e Extensao. | sem saida documentada |
| `reativarContato` | `$arrObjContatoAPI`: Instâncias preenchidas com IdContato, IdTipoContato, IdContatoAssociado, Sigla, Nome e NomeSocial. | sem saida documentada |
| `reativarHipoteseLegal` | `$arrObjHipoteseLegalAPI`: Instâncias preenchidas com IdHipoteseLegal, Nome, BaseLegal e NivelAcesso. | sem saida documentada |
| `reativarTipoContato` | `$arrObjTipoContatoAPI`: Instâncias preenchidas com IdTipoContato e Nome. | sem saida documentada |
| `reativarTipoDocumento` | `$arrObjSerieAPI`: Instâncias preenchidas com IdSerie, Nome e Aplicabilidade. | sem saida documentada |
| `reativarTipoProcesso` | `$arrObjTipoProcedimentoAPI`: Instâncias preenchidas com IdTipoProcedimento e Nome. | sem saida documentada |
| `reativarUnidade` | `$arrObjUnidadeAPI`: Instâncias preenchidas com IdUnidade, Sigla e Descricao. | sem saida documentada |
| `reativarUsuario` | `$arrObjUsuarioAPI`: Instâncias preenchidas com IdUsuario, Sigla, Nome e StaTipo. | sem saida documentada |
| `reativarVeiculoPublicacao` | `$arrObjVeiculoPublicacaoAPI`: Instâncias preenchidas com IdVeiculoPublicacao. | sem saida documentada |
| `relacionarProcesso` | `$objProcedimentoAPI1`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPI2`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `removerRelacionamentoProcesso` | `$objProcedimentoAPI1`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPI2`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `removerSobrestamentoProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPIVinculado`: Instância preenchida com IdProcedimento e NumeroProtocolo (nulo se não estiver vinculado a outro processo). | sem saida documentada |
| `sobrestarProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPIVinculado`: Instância preenchida com IdProcedimento e NumeroProtocolo (nulo se não estiver vinculado a outro processo). | sem saida documentada |
| `substituirContato` | `$objContatoAPI`: Contato para substituição informado na tela Relatórios de Contatos Temporários. Instância preenchida com IdContato, IdTipoContato, Sigla e Nome.; `$arrObjContatoAPI`: Lista de contatos que serão substituídos. Instâncias preenchidas com IdContato, IdTipoContato, Sigla e Nome. | sem saida documentada |
| `tratarLinkSemAssinatura` | `$strLink`: Link sem assinatura para redirecionamento automático pelo sistema. | `$bolValido`: Retornar true ou false. |
| `validarContato` | `$objContatoAPI`: Instância preenchida com IdContato, IdTipoContato, IdContatoAssociado, StaNatureza, SinEnderecoAssociado, StaGenero, Cpf, Rg, OrgaoExpedidor, Matricula, MatriculaOab, NumeroPassaporte, IdPaisPassaporte, DataNascimento, Cnpj, IdCargo, Sigla, Nome, NomeSocial, TelefoneFixo, TelefoneCelular, Email, SitioInternet, Endereco, Complemento, Bairro, Cep, Observacao, SinAtivo, IdPais, IdEstado e IdCidade. | sem saida documentada |
| `validarEliminacaoDocumento` | `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento e NumeroProtocolo. | sem saida documentada |
| `validarEliminacaoProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `verificarAcessoProtocolo` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento, IdTipoProcedimento, IdUnidadeGeradora e NivelAcesso.; `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento, IdProcedimento, IdSerie, IdUnidadeGeradora, Tipo, SubTipo e NivelAcesso. | `$arrLiberacoes`: Retornar um array indexado pelo número do protocolo onde cada item possui o valor P (Permitido) ou N (Negado) indicando o tipo de acesso ao processo ou documento. Também podem ser utilizadas as constantes abaixo da classe SeiIntegracao: //TAM = Tipo Acesso Modulo public static $TAM_PERMITIDO = 'P'; public static $TAM_NEGADO = 'N'; |
| `verificarAcessoProtocoloExterno` | `$arrObjProcedimentoAPI`: Instâncias representando os processos anexados preenchidas com IdProcedimento, IdTipoProcedimento, IdUnidadeGeradora e NivelAcesso.; `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento, IdProcedimento, IdSerie, IdUnidadeGeradora, SinAssinado, SinPublicado, Tipo, SubTipo e NivelAcesso. | `$arrLiberacoes`: Retornar um array indexado pelo número do protocolo onde cada item possui o valor P (Permitido) ou N (Negado) indicando o tipo de acesso ao processo ou documento. Também podem ser utilizadas as constantes abaixo da classe SeiIntegracao: //TAM = Tipo Acesso Modulo public static $TAM_PERMITIDO = 'P'; public static $TAM_NEGADO = 'N'; |
| `verificarAcessoTipoContato` | `$arrObjTipoContatoAPI`: Instâncias preenchidas com IdTipoContato. | `$arrLiberacoes`: Retornar um array indexado pelo ID do tipo de contato onde cada item possui os valores: N = nenhum acesso concedido pelo módulo A = permissão para alteração de dados C = Consulta Completa R = Consulta Resumida Também podem ser utilizadas as constantes abaixo da classe TipoContatoRN: public static $TA_NENHUM = 'N'; public static $TA_ALTERACAO = 'A'; public static $TA_CONSULTA_COMPLETA = 'C'; public static $TA_CONSULTA_RESUMIDA = 'R'; |
| `verificarLoginExterno` | `$objUsuarioAPI`: Instâncias preenchidas com IdUsuario, Sigla, Nome e StaTipo. | `booleano`: Retornar true ou false. |
