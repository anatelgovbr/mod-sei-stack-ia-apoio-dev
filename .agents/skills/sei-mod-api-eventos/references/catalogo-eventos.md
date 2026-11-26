# Catálogo de Eventos do SEI (v5.0 — Cap. 9)

> Fonte: `docs/manuais/sei/manual_md/sei_modulos_manual_dev_9_eventos.md`, conferida com o core 5.0.6 pelo `.agents/skills/sei-mod-api-eventos/evals/verificar_stack.py`; onde o manual diverge do core, vale o core.
> Uso: localizar o hook correto em `*Integracao.php` antes de propor interceptacao propria ou alteracao no core.

Se a duvida ainda estiver ambigua entre API, evento e operacao, usar primeiro
`sei-direcionador-integracao`. Se o caso for apenas menu interno SIP ou pagina
de modulo sem hook no core, a skill principal passa a ser `sei-menu-pagina`.

## Roteamento e Controladores

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| processarControlador | Dispatch principal de requisicoes para o modulo | `$strAcao` (texto da ação), nas requisições internas do SEI | Roteamento central de modulo; raramente usado diretamente |
| processarControladorAjax | Dispatch de requisicoes AJAX internas | `$strAcaoAjax` (texto da ação AJAX), nas chamadas AJAX internas, de mesma origem | Implementar endpoints AJAX internos do modulo |
| processarControladorAjaxExterno | Dispatch de requisicoes AJAX de origem externa | `$strAcaoAjax` (texto da ação AJAX), nas chamadas AJAX de origem externa | Integracoes externas via AJAX; CORS |
| processarControladorExterno | Dispatch de requisicoes de paginas externas (usuario externo) | `$strAcao` (texto da ação), nas páginas de usuário externo autenticado | Páginas externas do modulo; interface publica |
| processarControladorPublicacoes | Dispatch de requisicoes de publicacoes | `$strAcao` (texto da ação), nas páginas de pesquisa de publicações | Área pública de publicações; listagens |
| processarControladorWebServices | Dispatch de requisicoes de WebServices | `$strServico` (texto do serviço), nas chamadas de WebServices (SOAP/REST) | Integracao via WebServices; APIs externas |
| tratarLinkSemAssinatura | Tratamento de links sem assinatura digital | `$strLink` (texto do link), de link publicado sem assinatura | Processar link de acesso externo sem login; cautela |
| obterAcoesAjaxExternasSemLogin | Acoes disponiveis sem login para AJAX externo | Sem parâmetro; chamado no AJAX externo sem sessão | Endpoints publicos; ações sem autenticação |
| obterAcoesExternasSemLogin | Acoes disponiveis sem login para pagina externa | Sem parâmetro; chamado na página externa sem sessão | Menu inicial de usuario externo; Tela de login |

## Ciclo de Vida de Processo e Documento

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| gerarProcesso | Apos geracao de novo processo | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Executar logica apos geracao de processo; integrar com outro sistema |
| alterarProcesso | Apos alteracao de processo (dadosbasicos, interessado, etc.) | `$objProcedimentoAPI` (`ProcedimentoAPI`) com alteracoes | Reagir a mudanca de dados do processo; atualizar sistema externo |
| gerarDocumento | Apos geracao de documento | `$objDocumentoAPI` (`DocumentoAPI`) | Executar logica apos geracao de documento; integracao |
| alterarDocumento | Apos alteracao de documento | `$objDocumentoAPI` (`DocumentoAPI`) com alteracoes | Reagir a alteracao de documento; atualizar sistema |
| atualizarConteudoDocumento | Apos atualizacao de conteudo de documento | `$objDocumentoAPI` (`DocumentoAPI`) com novo conteudo | Atualizar indexacao; notificar sistema externo |
| anexarProcesso | Apos anexar processo a processo principal | `$objProcedimentoAPIPrincipal` (`ProcedimentoAPI`) e `$objProcedimentoAPIAnexado` (`ProcedimentoAPI`) | Reagir ao vinculo de anexacao; sincronizar |
| desanexarProcesso | Apos desanexar processo | `objProcedimentoAPIPrincipal` e `objProcedimentoAPIAnexado`, cada um com IdProcedimento e NumeroProtocolo, sem motivo | Reagir a desanexacao; atualizar sistemas |
| relacionarProcesso | Apos criar relacionamento lateral entre processos | `$objProcedimentoAPI1` (`ProcedimentoAPI`) e `$objProcedimentoAPI2` (`ProcedimentoAPI`) | Reagir ao vinculo lateral; atualizar sistema |
| removerRelacionamentoProcesso | Após remover relacionamento entre processos | `$objProcedimentoAPI1` (`ProcedimentoAPI`) e `$objProcedimentoAPI2` (`ProcedimentoAPI`) | Reagir a remocao de vinculo |
| enviarProcesso | Apos envio de processo a outra unidade | `$arrObjProcedimentoAPI` (`ProcedimentoAPI[]`) e `$arrObjUnidadeAPI` (`UnidadeAPI[]`) | Reagir a envio; notificar sistema externo |
| concluirProcesso | Após conclusao de processo na unidade | `$arrObjProcedimentoAPI` (`ProcedimentoAPI[]`) | Reagir a conclusao; atualizar carga |
| reabrirProcesso | Após reabertura de processo na unidade | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Reagir a reabertura; reativar carga |
| bloquearProcesso | Após bloqueio de processo | `arrObjProcedimentoAPI` com IdProcedimento e NumeroProtocolo, sem motivo | Reagir a bloqueio; restringir acesso externo |
| desbloquearProcesso | Após desbloqueio de processo | `$arrObjProcedimentoAPI` (`ProcedimentoAPI[]`) | Reagir a desbloqueio; restaurar acesso |
| sobrestarProcesso | Após sobrestamento de processo | `objProcedimentoAPI` e `objProcedimentoAPIVinculado`, o vinculado nulo quando nao houver, sem motivo | Reagir a sobrestamento; impedir tramite |
| removerSobrestamentoProcesso | Após remover sobrestamento | `$objProcedimentoAPI` (`ProcedimentoAPI`) e `$objProcedimentoAPIVinculado` (`ProcedimentoAPI`, nulo quando não houver) | Reagir a remoção de sobrestamento |
| moverDocumento | Após mover documento na árvore | `objDocumentoAPI`, `objProcedimentoAPIOrigem` e `objProcedimentoAPIDestino` | Reagir a reorganização de documento na árvore |
| cancelarDocumento | Após cancelamento de documento | `$objDocumentoAPI` (`DocumentoAPI`) | Reagir a cancelamento; invalidar copia |
| eliminarDocumento | Após eliminacao de documento | `$arrObjDocumentoAPI` (`DocumentoAPI[]`) | Reagir a eliminacao; remover vínculo externo |
| eliminarProcesso | Após eliminacao de processo | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Reagir a eliminacao; remover vínculo |
| confirmarAtualizacaoConteudoDocumento | Confirma atualizacao de conteudo de documento | `$objDocumentoAPI` (`DocumentoAPI`) | Confirmar atualização; aceitar ou recusar mudanca |
| prepararCloneDocumento | Prepara clone de documento para geracao | `$objDocumentoAPI` (`DocumentoAPI`) | Interceptar geracao de documento clone |
| darCienciaDocumento | Após receber ciencia de documento | `$objDocumentoAPI` (`DocumentoAPI`) | Reagir a ciencia; marcar como visualizado |
| darCienciaProcesso | Após receber ciencia de processo | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Reagir a ciencia de processo |
| permitirAndamentoConcluido | Antes de permitir conclusao de processo | `objAndamentoAPI` com IdProtocolo e IdTarefa, mais `bolPermitir` | Validar condicoes para conclusao; bloquear se necessário |

## UI — Ícones e Botões

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| montarIconeControleProcessos | Adiciona icones na tela de Controle de Processos | `$arrObjProcedimentoAPI` (`ProcedimentoAPI[]`, até 200) | Adicionar icone customizado na linha do processo; status especial |
| montarIconeProcesso | Adiciona icone na visualizacao de processo | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Adicionar icone na tela de processo; badge |
| montarIconeDocumento | Adiciona icone na arvore de documentos | `$objProcedimentoAPI` (`ProcedimentoAPI`) e `$arrObjDocumentoAPI` (`DocumentoAPI[]`) | Adicionar icone no documento; indicador de status |
| montarIconeSistema | Adiciona icone na barra de titulo do SEI | Sem parâmetro | Icone na barra superior do sistema; logo customizado |
| montarIconeAcompanhamentoEspecial | Adiciona icone na tela de Acompanhamento Especial | `$arrObjProcedimentoAPI` (`ProcedimentoAPI[]`) | Badge de acompanhamento especial |
| montarIconeOrdenarArvore | Adiciona controle de ordenacao na árvore | `objProcedimentoAPI` com IdProcedimento, mais `strIcone` | Botao de ordenacao personalizado |
| alterarIconeArvoreDocumento | Altera icone de documento na arvore | `objProcedimentoAPI`, `arrObjDocumentoAPI`, `arrIcones` indexado por id de documento | Substituir icone padrao por customizado |
| montarBotaoControleProcessos | Adiciona botões no Controle de Processos | Sem parâmetros | Retornar uma lista de botões da barra de ações, com SVG de 24×24 recomendado |
| montarBotaoProcesso | Adiciona botões na barra do processo na árvore | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Retornar uma lista de botões do processo |
| montarBotaoDocumento | Adiciona botões na barra do documento na árvore | `$objProcedimentoAPI` (`ProcedimentoAPI`) e `$arrObjDocumentoAPI` (`DocumentoAPI[]`) | Retornar uma lista de botões por ID de documento |
| montarBotaoCadastroDocumento | Adiciona botoes na tela de cadastro de documento | `objDocumentoAPI` com IdProcedimento, IdDocumento, IdSerie, Data, IdUnidadeGeradora, Numero, NomeArvore, DinValor, IdPlanoTrabalho e Tipo, mais `arrBotoes` | Acoes na tela de inclusao de documento |
| montarBotaoChatIA | Adiciona botao de chat IA na interface | Sem parâmetro | Botao de interacao com IA; integração |
| montarBotaoChatIAexterno | Adiciona botão de chat IA na área do usuário externo (SEI 5.0.6) | Sem parâmetro; o core só chama com usuário externo logado | Botão de IA para usuário externo |
| montarBotaoLoginExterno | Adiciona botao na tela de login externo | Sem parâmetro | Botao customizado no login externo |
| montarBotaoAcessoExternoAutorizado | Adiciona botoes na área de acesso externo autorizado | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Acoes para usuário externo autenticado |
| montarBotaoControleAcessoExterno | Adiciona botoes no controle de acesso externo | Sem parâmetro | Acoes de controle; revogar, limitar |
| montarBotaoAssinaturaInterno | Adiciona botoes na area de assinatura interno | `objUsuarioAPI` com IdUsuario, Sigla, Nome e StaTipo, mais `strHtml` | Acoes complementares na assinatura interna |
| montarBotaoAssinaturaExterno | Adiciona botoes na area de assinatura externo | `objUsuarioAPI` com IdUsuario, Sigla, Nome e StaTipo, mais `strHtml` | Acoes complementares na assinatura externa |
| montarBotaoVeiculoPublicacao | Adiciona botoes na tela de veiculo de publicacao | `$arrObjVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI[]`) | Acoes no veiculo de publicacao |

### Filtro de botões por acesso recente

A preferência **Filtrar botões acessados recentemente**, em **Alterar Configuração**, vale para o Controle de Processos e para as barras do processo e do documento na árvore. O core mantém histórico distinto para cada um dos três contextos.

- Devolva uma string HTML por botão, com um `<a>` como filho direto da barra e o `<img>` como filho direto do link, no formato `<a ...><img ... alt="Nome da ação" title="Nome da ação"></a>`. Para documentos, indexe a lista de botões pelo ID do documento recebido no evento.
- Use um `title` no próprio `<img>`, estável entre acessos e distinto para ações diferentes na mesma barra. Use o nome da ação, sem número de processo, ID de documento ou estado variável. O core usa o CRC32 desse título para decidir a visibilidade do link e registrar o clique no histórico.
- Entregue todos os botões permitidos no contexto. O core decide quais ficam visíveis e monta **Exibir mais Botões** quando há ações visíveis e ocultas. A barra fica completa quando a preferência está desligada ou o filtro ocultaria todos os botões. Mantenha a autorização na ação e a assinatura nos links.
- Na árvore, prefira o link assinado no `href` e aspas duplas nos atributos, como em `julgamento`. O core incorpora os fragmentos a um literal JavaScript e remonta a barra ao trocar de nó. Preserve o escape do HTML nesse contexto e mantenha o clique funcional após a remontagem.

**Verificação.** Na superfície alterada, teste a preferência desligada e ligada, com uma ação recente e outra fora do histórico. Expanda, recolha e execute a ação do módulo após expandir. Ao reabrir a mesma superfície, confirme que o clique foi registrado. Na árvore, alterne entre processo e documento para conferir a montagem e o destino dos links.

Fontes no checkout do SEI: filtro e registro no core (`fontes/sei/src/main/php/sei/web/js/sei.js`), Controle de Processos (`fontes/sei/src/main/php/sei/web/procedimento_controlar.php`), processo (`fontes/sei/src/main/php/sei/web/int/ProcedimentoINT.php`), documento (`fontes/sei/src/main/php/sei/web/int/ProtocoloINT.php`) e exemplos do módulo julgamento (`fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento/MdJulgarIntegracao.php`).

## UI — Menus e Ações

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| montarMenuPublicacoes | Adiciona itens no menu de publicacoes | Sem parâmetro | Itens no menu de pesquisa de publicações |
| montarMenuUsuarioExterno | Adiciona itens no menu do usuario externo | Sem parâmetro | Itens no menu do portal externo |
| montarMenuConsultaProcessual | Adiciona itens no menu de consulta processual | Sem parâmetro | Itens no menu de consulta pública |
| adicionarElementoMenu | Adiciona elemento HTML abaixo do menu | Sem parâmetro | Inserir bloco HTML abaixo do menu; banner, aviso |
| obterDiretorioIconesMenu | Retorna caminho do diretorio de icones de menu | Sem parâmetro | Definir pasta de ícones SVG do modulo |
| montarAcaoControleAcessoExterno | Adiciona acoes no controle de acesso externo | `$arrObjAcessoExternoAPI` (`AcessoExternoAPI[]`) | Acoes no controle de acesso; ações customizadas |
| montarAcaoDocumentoAcessoExternoAutorizado | Adiciona acoes no documento de acesso externo autorizado | `$arrObjDocumentoAPI` (`DocumentoAPI[]`) | Acoes no documento do usuário externo |
| montarAcaoDocumentoAcessoExternoNegado | Adiciona acoes no documento de acesso externo negado | `$arrObjDocumentoAPI` (`DocumentoAPI[]`) | Acoes quando acesso negado; mensagem |
| montarAcaoProcessoAnexadoAcessoExternoAutorizado | Adiciona acoes no processo anexado de acesso externo | `$arrObjProcedimentAPI` (`ProcedimentoAPI[]`) | Acoes em processo anexado externo |
| montarAcaoProcessoAnexadoAcessoExternoNegado | Adiciona acoes no processo anexado acesso externo | `$arrObjProcedimentAPI` (`ProcedimentoAPI[]`) | Acoes quando acesso negado |
| montarAcaoPublicacao | Adiciona acoes na publicacao | `$arrObjPublicacaoAPI` (`PublicacaoAPI[]`) | Acoes na tela de publicacao |
| montarAcaoVeiculoPublicacao | Adiciona acoes no veiculo de publicacao | `$arrObjVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI[]`) | Acoes no veiculo; gestão |
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
| verificarLoginExterno | Informa ao core que o usuário externo se autentica fora do SEI; com `true`, a tela de alteração de senha bloqueia a troca | entrada `$objUsuarioAPI` (IdUsuario, Sigla, Nome e StaTipo), saída booleano | Usuário externo com autenticação fora do SEI |
| cancelarDisponibilizacaoAcessoExterno | Cancela disponibilizacao de acesso externo | `$arrObjAcessoExternoAPI` (`AcessoExternoAPI[]`) | Revogar acesso externo; encerrar sessão |
| cancelarLiberacaoAssinaturaExterna | Cancela liberacao de assinatura externa | `$arrObjAcessoExternoAPI` (`AcessoExternoAPI[]`) | Revogar liberacao de assinatura; desatrelhar |
| adicionarRestricaoOuvidoria | Após bloqueio do documento de manifestação de ouvidoria (SEI 5.0.4) | `objDocumentoAPI` com IdDocumento e IdProcedimento | Reagir à restrição de acesso da manifestação |
| removerRestricaoOuvidoria | Após desbloqueio do documento de manifestação de ouvidoria (SEI 5.0.4) | `objDocumentoAPI` com IdDocumento e IdProcedimento | Reagir à retirada da restrição |

## Assinatura e Publicação

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| obterConfiguracoesAssinatura | Retorna configuracoes de assinatura | `objConfiguracoesAssinaturaAPI` com NomeModulo | Customizar comportamento de assinatura; Plugins |
| prepararAssinaturaDocumento | Prepara documento para assinatura | `objAssinaturaAPI` com IdUsuario, Sigla, Nome, CargoFuncao, Cpf, StaFormaAutenticacao e Agrupador | Interceptar preparacao de assinatura; adicionar validacao |
| assinarDocumento | Após assinatura de documento | `arrObjDocumentoAPI` com IdDocumento, IdProcedimento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, IdUsuarioGerador | Reagir a assinatura; notificar sistema externo |
| cancelarAssinaturaDocumento | Após cancelamento das assinaturas do documento (SEI 5.0.4) | `objDocumentoAPI` com IdDocumento, IdProcedimento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SubTipo e NivelAcesso | Desfazer o que o módulo gravou na assinatura |
| montarTipoTarjaAssinaturaCustomizada | Acrescenta tipos de tarja de assinatura (SEI 4.0.0) | Sem parâmetro; retorna lista de `TipoDTO` com StaTipo e Descricao | Tarja de assinatura própria do módulo |
| agendarPublicacao | Após agendamento de publicacao | `$objPublicacaoAPI` (`PublicacaoAPI`) | Reagir a agendamento; sincronizar |
| alterarPublicacao | Após alteracao de publicacao | `$objPublicacaoAPI` (`PublicacaoAPI`) | Reagir a alteracao; atualizar veiculo |
| confirmarPublicacao | Após confirmacao de publicacao | `$arrObjPublicacaoAPI` (`PublicacaoAPI[]`) | Reagir a confirmacao; notificar |
| cancelarAgendamentoPublicacao | Após cancelamento de agendamento | `$objPublicacaoAPI` (`PublicacaoAPI`) | Reagir a cancelamento; atualizar status |
| montarDadosImprensaNacional | Retorna dados para impressa nacional | `$objPublicacaoAPI` (`PublicacaoAPI`) | Montar dados DOU; formatar publicacao |
| obterProximaDataPublicacao | Retorna proxima data de publicacao em veiculo | `objPublicacaoAPI` com IdVeiculoPublicacao e StaTipoVeiculo, mais data `InfraData` | Calcular data de publicacao; agenda |
| montarTextoInformativoPublicacao | Adiciona texto informativo na publicacao | `objPublicacaoAPI` com IdPublicacao, IdVeiculoPublicacao, StaTipoVeiculo e IdDocumento | Texto adicional na publicacao; aviso |
| alterarVeiculoPublicacao | Após alteracao de veiculo de publicacao | `$objVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI`) | Reagir a alteracao de veiculo |
| cadastrarVeiculoPublicacao | Após cadastro de novo veiculo | `$objVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI`) | Reagir a cadastro de veiculo |
| desativarVeiculoPublicacao | Evento de manutenção; conferir momento abaixo | `$arrObjVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI[]`) | Avaliar dependência e eficácia da interceptação |

## Validação e Complemento

### Paginas com contrato detalhado

| Nome | Descrição | Entrada principal | Saída principal | Sinais de domínio | Quando usar |
|---|---|---|---|---|---|
| processarPaginaCadastroDocumento | Intercepta pagina de cadastro de documento | `$objDocumentoAPI` (`DocumentoAPI`) com `IdProcedimento`, `IdDocumento`, `IdSerie`, `Data`, `IdUnidadeGeradora`, `Numero`, `NomeArvore`, `DinValor`, `IdPlanoTrabalho` e `Tipo` | `PaginaComplementoAPI` | `plano de trabalho`, `cadastro de documento`, `complemento de pagina` | Modificar tela de cadastro; adicionar campos ou comportamento quando o documento estiver vinculado a plano de trabalho |
| processarPaginaInclusaoDocumentoItemEtapa | Intercepta pagina de inclusao de documento na etapa | `$objDocumentoAPI` (`DocumentoAPI`) com `IdProcedimento`, `IdSerie`, `IdPlanoTrabalho`, `IdEtapaTrabalho`, `IdItemEtapa` e `IdOperacao` | `PaginaComplementoAPI` | `plano de trabalho`, `etapa de trabalho`, `item de etapa`, `inclusao de documento` | Modificar inclusao de documento por etapa; injetar complemento de pagina; customizar fluxo vinculado a plano de trabalho |

### Outros eventos de validacao e complemento

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| validarContato | Valida dados de contato antes de gravar | `$objContatoAPI` (`ContatoAPI`) | Validar contato; regras de negocio |
| validarEliminacaoDocumento | Valida eliminacao de documento | `$arrObjDocumentoAPI` (`DocumentoAPI[]`) | Bloquear eliminacao; validacao customizada |
| validarEliminacaoProcesso | Valida eliminacao de processo | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Bloquear eliminacao; validacao customizada |
| processarVariaveisEditor | Intercepta variaveis do editor de texto | `$objDocumentoAPI` (`DocumentoAPI`) | Adicionar variaveis customizadas ao editor |
| obterRelacaoVariaveisEditor | Retorna lista de variaveis disponiveis no editor | Sem parâmetro | Definir variaveis do editor; contexto |
| processarPesquisaRapida | Intercepta pesquisa rapida | `$strTexto` (texto da pesquisa) | Customizar pesquisa rapida; filtros |

## Cadastro e Manutenção

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| cadastrarContato | Após cadastro de contato | `$objContatoAPI` (`ContatoAPI`) | Reagir a novo contato; sincronizar |
| alterarContato | Após alteracao de contato | `$objContatoAPI` (`ContatoAPI`) | Reagir a alteracao de contato; atualizar |
| excluirContato | Evento de manutenção; conferir momento abaixo | `$arrObjContatoAPI` (`ContatoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| desativarContato | Evento de manutenção; conferir momento abaixo | `$arrObjContatoAPI` (`ContatoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarContato | Evento de manutenção; conferir momento abaixo | `$arrObjContatoAPI` (`ContatoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| substituirContato | Após substituicao de contato | `$objContatoAPI` (`ContatoAPI`) e `$arrObjContatoAPI` (`ContatoAPI[]`) | Reagir a substituicao; migrar vinculos |
| cadastrarHipoteseLegal | Após cadastro de hipotese legal | `$objHipoteseLegalAPI` (`HipoteseLegalAPI`) | Reagir a nova hipotese; sincronizar |
| alterarHipoteseLegal | Após alteracao de hipotese legal | `$objHipoteseLegalAPI` (`HipoteseLegalAPI`) | Reagir a alteracao; atualizar |
| desativarHipoteseLegal | Evento de manutenção; conferir momento abaixo | `$arrObjHipoteseLegalAPI` (`HipoteseLegalAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarHipoteseLegal | Evento de manutenção; conferir momento abaixo | `$arrObjHipoteseLegalAPI` (`HipoteseLegalAPI[]`) | Avaliar dependência e eficácia da interceptação |
| desativarArquivoExtensao | Evento de manutenção; conferir momento abaixo | `$arrObjArquivoExtensaoAPI` (`ArquivoExtensaoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarArquivoExtensao | Evento de manutenção; conferir momento abaixo | `$arrObjArquivoExtensaoAPI` (`ArquivoExtensaoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| excluirArquivoExtensao | Evento de manutenção; conferir momento abaixo | `$arrObjArquivoExtensaoAPI` (`ArquivoExtensaoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| desativarTipoDocumento | Evento de manutenção; conferir momento abaixo | `$arrObjSerieAPI` (`SerieAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarTipoDocumento | Evento de manutenção; conferir momento abaixo | `$arrObjSerieAPI` (`SerieAPI[]`) | Avaliar dependência e eficácia da interceptação |
| desativarTipoProcesso | Evento de manutenção; conferir momento abaixo | `$arrObjTipoProcedimentoAPI` (`TipoProcedimentoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarTipoProcesso | Evento de manutenção; conferir momento abaixo | `$arrObjTipoProcedimentoAPI` (`TipoProcedimentoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| desativarUnidade | Evento de manutenção; conferir momento abaixo | `$arrObjUnidadeAPI` (`UnidadeAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarUnidade | Evento de manutenção; conferir momento abaixo | `$arrObjUnidadeAPI` (`UnidadeAPI[]`) | Avaliar dependência e eficácia da interceptação |
| desativarUsuario | Evento de manutenção; conferir momento abaixo | `$arrObjUsuarioAPI` (`UsuarioAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarUsuario | Evento de manutenção; conferir momento abaixo | `$arrObjUsuarioAPI` (`UsuarioAPI[]`) | Avaliar dependência e eficácia da interceptação |
| cadastrarVeiculoPublicacao | Após cadastro de veiculo | `$objVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI`) | Reagir a novo veiculo; configurar |
| desativarVeiculoPublicacao | Evento de manutenção; conferir momento abaixo | `$arrObjVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| reativarVeiculoPublicacao | Evento de manutenção; conferir momento abaixo | `$arrObjVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| excluirVeiculoPublicacao | Evento de manutenção; conferir momento abaixo | `$arrObjVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI[]`) | Avaliar dependência e eficácia da interceptação |
| alterarVeiculoPublicacao | Após alteracao de veiculo | `$objVeiculoPublicacaoAPI` (`VeiculoPublicacaoAPI`) | Reagir a alteracao; atualizar |
| listarUnidadesEnvioProcesso | Lista unidades disponiveis para envio | entrada `arrObjProcedimentoAPI`, saida `arrObjUnidadeAPI` com IdUnidade | Filtrar unidades de envio; customizar |
| inicializar | Executa ao inicializar o modulo (boot) | `$strVersaoSEI` | Inicializar recursos; configurar ambiente |

## Mensagens e Status

| Nome | Descrição | Trigger / Entrada | Quando usar |
|---|---|---|---|
| montarMensagemProcesso | Adiciona mensagem na tela de processo | `$objProcedimentoAPI` (`ProcedimentoAPI`) | Mensagem personalizada; aviso, alerta |

## Notas sobre ambiguidades do manual

1. Varios eventos de ciclo de vida (alterarProcesso, alterarDocumento, etc.) nao deixam claro se a trigger ocorre ANTES ou DEPOIS da operacao no core. Em caso de necessidade de interceptacao antes da escrita, verificar a assinatura em `SeiIntegracao.php` e o ponto de chamada na RN do core, incluindo transação e propagação da exceção.

2. O momento varia por operação. Consulte a tabela de manutenção verificada abaixo e confirme o callsite da versão suportada. Pós-escrita dentro da transação não é pós-commit; evento posterior a um DELETE que falha por FK não chega a executar. A assinatura isolada não comprova eficácia.

3. `listarUnidadesEnvioProcesso` tem assinatura minima não especificada no manual — verificar no fonte antes de implementar.

4. `montarBotaoChatIA` aparece no catalogo mas nao tem documentação de parametro ou comportamento detalhado. Tratar como extensibilidade via botão customizado.

5. Para eventos que recebem arrays grandes (ate 200 objetos), o manual adverte sobre performance: evitar consultas individuais dentro do loop. Considerar consulta em lote com `IN` antes de implementar.

6. A entrada de `verificarLoginExterno` no manual descreve processos anexados. O core 5.0.6 envia um `UsuarioAPI` com IdUsuario, Sigla, Nome e StaTipo e chama o evento só em `usuario_externo_alteracao_senha.php`.

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
| `adicionarElementoMenu` | Sem parâmetro | `strElemento`: Conteúdo HTML para inclusão abaixo do menu. |
| `adicionarRestricaoOuvidoria` | `$objDocumentoAPI`: Instância preenchida com IdDocumento e IdProcedimento. Chamado em `SolicitacaoOuvidoriaRN::alterarControlado`, depois de gravar a alteração, quando `SinBloqueio` muda para S. | sem saida documentada |
| `agendarPublicacao` | `$objPublicacaoAPI`: Instância preenchida com IdPublicacao, IdDocumento, IdVeiculoPublicacao, StaTipoVeiculo e DataDisponibilizacao. | sem saida documentada |
| `alterarContato` | `$objContatoAPI`: Instância preenchida com IdContato, IdTipoContato, IdContatoAssociado, StaNatureza, SinEnderecoAssociado, StaGenero, Cpf, Rg, OrgaoExpedidor, Matricula, MatriculaOab, NumeroPassaporte, IdPaisPassaporte, DataNascimento, Cnpj, IdCargo, Sigla, Nome, NomeSocial, TelefoneComercial, TelefoneResidencial, TelefoneCelular, Email, SitioInternet, Endereco, Complemento, Bairro, Cep, Observacao, SinAtivo, IdPais, IdEstado e IdCidade. | sem saida documentada |
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
| `cadastrarContato` | `$objContatoAPI`: Instância preenchida com IdContato, IdTipoContato, IdContatoAssociado, StaNatureza, SinEnderecoAssociado, StaGenero, Cpf, Rg, OrgaoExpedidor, Matricula, MatriculaOab, NumeroPassaporte, IdPaisPassaporte, DataNascimento, Cnpj, IdCargo, Sigla, Nome, NomeSocial, TelefoneComercial, TelefoneResidencial, TelefoneCelular, Email, SitioInternet, Endereco, Complemento, Bairro, Cep, Observacao, SinAtivo, IdPais, IdEstado e IdCidade. | sem saida documentada |
| `cadastrarHipoteseLegal` | `$objHipoteseLegalAPI`: Instância preenchida com IdHipoteseLegal, Nome, Descricao, BaseLegal, NivelAcesso e SinAtivo. | sem saida documentada |
| `cadastrarVeiculoPublicacao` | `$objVeiculoPublicacaoAPI`: Instância preenchida com IdVeiculoPublicacao, Nome, Descricao, StaTipo, SinFonteFeriados, SinPermiteExtraordinaria, SinExibirPesquisaInterna, WebService e SinAtivo. | sem saida documentada |
| `cancelarAgendamentoPublicacao` | `$objPublicacaoAPI`: Instância preenchida com IdPublicacao, IdDocumento, IdVeiculoPublicacao, StaTipoVeiculo e DataDisponibilizacao. | sem saida documentada |
| `cancelarAssinaturaDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento, IdProcedimento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SubTipo e NivelAcesso. Chamado em `DocumentoRN::cancelarAssinaturaInternoControlado`, na transação, depois de excluir todas as assinaturas do documento e lançar o andamento. O cancelamento ocorre ao salvar o conteúdo de documento assinado (`atualizarConteudoRN1205InternoControlado`) e ao remover anexo de documento assinado (`alterarRN0004InternoControlado`). Exceção do módulo desfaz o cancelamento. | sem saida documentada |
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
| `inicializar` | `strVersaoSEI`: Número da versão do SEI (exemplo: 3.1.0). | sem saida documentada |
| `listarUnidadesEnvioProcesso` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento e IdUnidadeGeradora. | `$arrObjUnidadeAPI`: Instâncias preenchidas com IdUnidade. |
| `montarAcaoControleAcessoExterno` | `$arrObjAcessoExternoAPI`: Conjunto de ocorrências de AcessoExternoAPI preenchidas com: IdAcessoExterno, DataValidade, SinAcessoProcesso, Procedimento (ocorrência de ProcedimentoAPI preenchida com IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade e NivelAcesso), Documento (ocorrência de DocumentoAPI preenchida com IdDocumento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SinAssinado, SinPublicado e NivelAcesso). | `arrIcones`: Um array PHP indexado pelos IDs dos acessos externos onde cada posição contém outro array com o conjunto de ícones para exibição. Acessos externos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoDocumentoAcessoExternoAutorizado` | `$arrObjDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SinAssinado, SinPublicado e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém outro array com o conjunto de ícones para exibição. Documentos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoDocumentoAcessoExternoNegado` | `$arrObjDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, IdUnidadeGeradora, Tipo, SinAssinado, SinPublicado e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém outro array com o conjunto de ícones para exibição. Documentos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoProcessoAnexadoAcessoExternoAutorizado` | `$arrObjProcedimentAPI`, nome como está no core: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoProcessoAnexadoAcessoExternoNegado` | `$arrObjProcedimentAPI`, nome como está no core: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento e NivelAcesso. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoPublicacao` | `arrObjPublicacaoAPI`: Conjunto de ocorrências de PublicacaoAPI preenchidas com: IdPublicacao, IdDocumento e Estado. | `arrIcones`: Um array PHP indexado pelos IDs das publicações que possuem ações liberadas pelo módulo. Cada posição contém outro array com o conjunto de ícones para exibição. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarAcaoVeiculoPublicacao` | `arrObjVeiculoPublicacaoAPI`: Conjunto de ocorrências de VeiculoPublicacaoAPI preenchidas com: IdVeiculoPublicacao e Nome. | `arrIcones`: Um array PHP indexado pelos IDs dos veículos que possuem ações liberadas pelo módulo. Cada posição contém outro array com o conjunto de ícones para exibição. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarBotaoAcessoExternoAutorizado` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade e NivelAcesso. | `arrBotoes`: Um array PHP onde cada item representa um botão. |
| `montarBotaoAssinaturaExterno` | `objUsuarioAPI`: Ocorrência de UsuarioAPI preenchida com: IdUsuario, Sigla, Nome e StaTipo. | `strHtml`: Código HTML do botão. |
| `montarBotaoAssinaturaInterno` | `objUsuarioAPI`: Ocorrência de UsuarioAPI preenchida com: IdUsuario, Sigla, Nome e StaTipo. | `strHtml`: Código HTML do botão. |
| `montarBotaoChatIA` | Sem parâmetro | `strBotao`: Texto com o código do botão para inclusão na página. |
| `montarBotaoChatIAexterno` | Sem parâmetro; chamado em `PaginaSEIExterna` só com usuário externo logado. | `strBotao`: HTML do botão, impresso quando é texto. |
| `montarBotaoControleAcessoExterno` | Sem parâmetro | `arrBotoes`: Um array PHP onde cada item representa um botão. |
| `montarBotaoControleProcessos` | Sem parâmetro | `arrBotoes`: Um array PHP onde cada item representa um botão. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarBotaoDocumento` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto.; `$arrObjDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, NomeSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, SinAssinado, SinPublicado, SinBloqueado, CodigoAcesso, Tipo, SubTipo. | `arrBotoes`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém outro array com o conjunto de botões para exibição junto ao documento. Documentos que não devem exibir botões do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 40x40. |
| `montarBotaoCadastroDocumento` | `objDocumentoAPI`: Ocorrência de DocumentoAPI preenchida com: IdProcedimento, IdDocumento, IdSerie, Data, IdUnidadeGeradora, Numero, NomeArvore, DinValor, IdPlanoTrabalho e Tipo. | `arrBotoes`: Um array PHP onde cada item representa um botão. |
| `montarBotaoLoginExterno` | Sem parâmetro | `strHtml`: Código HTML do botão. |
| `montarBotaoProcesso` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto. | `arrBotoes`: Um array PHP onde cada item representa um botão. Para as imagens é recomendado utilizar o formato SVG com tamanho 40x40. |
| `montarBotaoVeiculoPublicacao` | `arrObjVeiculoPublicacaoAPI`: Conjunto de ocorrências de VeiculoPublicacaoAPI preenchidas com: IdVeiculoPublicacao e Tipo. | `arrBotoes`: Um array indexado pelos Ids dos veículos de publicação e pelos identificadores dos botões contendo o código html do botão. é importante que o ID do botão informado no índice do array seja o mesmo da tag id do html, pois essa informação será utilizada para controlar a visualização de acordo com o veículo selecionado na tela. |
| `montarDadosImprensaNacional` | `objPublicacaoAPI`: Instância de PublicacaoAPI preenchida com: IdPublicacao, IdVeiculoPublicacao e StaTipoVeiculo. | `texto`: Texto da Imprensa Nacional para exibição na tela de publicações do documento, na tela de pesquisa de publicações e no carimbo de publicação do documento. |
| `montarIconeAcompanhamentoEspecial` | `arrObjProcedimentoAPI`: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora e IdOrgaoUnidadeGeradora. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição junto ao processo. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarIconeControleProcessos` | `arrObjProcedimentoAPI`: Conjunto de ocorrências de ProcedimentoAPI preenchidas com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora e IdOrgaoUnidadeGeradora. | `arrIcones`: Um array PHP indexado pelos IDs dos processos onde cada posição contém outro array com o conjunto de ícones para exibição junto ao processo. Processos que não devem exibir ícones do módulo não precisam estar no array. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarIconeDocumento` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto.; `$arrObjDocumentoAPI`: Conjunto de ocorrências de DocumentoAPI preenchidas com: IdDocumento, NumeroProtocolo, IdSerie, NomeSerie, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, SinAssinado, SinPublicado, SinBloqueado, CodigoAcesso, Tipo, SubTipo. | `arrIcones`: Um array PHP indexado pelos IDs dos documentos onde cada posição contém um array de ocorrências de ArvoreAcaoItemAPI com os ícones para exibição junto ao documento. Documentos que não devem exibir ícones do módulo não precisam estar no array. |
| `montarIconeOrdenarArvore` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento. | `$strIcone`: Ícone para exibição. |
| `montarIconeProcesso` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto. | `arrObjArvoreAcaoItemAPI`: Conjunto de ocorrências da estrutura ArvoreAcaoItemAPI. |
| `montarIconeSistema` | Sem parâmetro | `arrIcones`: Um array PHP com o conjunto de ícones para exibição na barra superior. Para as imagens é recomendado utilizar o formato SVG com tamanho 24x24. |
| `montarMensagemProcesso` | `objProcedimentoAPI`: Ocorrência de ProcedimentoAPI preenchida com: IdProcedimento, NumeroProtocolo, IdTipoProcedimento, NomeTipoProcedimento, IdTipoPrioridade, NivelAcesso, GrauSigilo, IdHipoteseLegal, IdUnidadeGeradora, IdOrgaoUnidadeGeradora, CodigoAcesso e SinAberto. | `strMsg`: Texto da mensagem. |
| `montarMenuConsultaProcessual` | Sem parâmetro | `$arrItens`: Um array de itens montados com a estrutura: *[nível]\^[url]\^[título]\^[rótulo]\^[target (opcional)]* Onde o nível é representado pelo número de "hífens" informados. |
| `montarMenuPublicacoes` | Sem parâmetro | `$arrItens`: Um array de itens montados com a estrutura: *[nível]\^[url]\^[título]\^[rótulo]\^[target (opcional)]* Onde o nível é representado pelo número de hífens informados. |
| `montarMenuUsuarioExterno` | Sem parâmetro | `$arrItens`: Um array de itens montados com a estrutura: *[nível]\^[url]\^[título]\^[rótulo]\^[target (opcional)]* Onde o nível é representado pelo número de hífens informados. |
| `montarTextoInformativoPublicacao` | `objPublicacaoAPI`: Instância de PublicacaoAPI preenchida com: IdPublicacao, IdVeiculoPublicacao, StaTipoVeiculo e IdDocumento. | `texto`: Texto para exibição junto ao documento após a publicação. |
| `montarTipoTarjaAssinaturaCustomizada` | Sem parâmetro | Lista de `TipoDTO` com StaTipo e Descricao; o core acrescenta " - <nome do módulo>" à descrição em `TarjaAssinaturaRN::listarTiposTarjaAssinatura`. |
| `moverDocumento` | `$objDocumentoAPI`: Instância preenchida com IdDocumento e NumeroProtocolo.; `$objProcedimentoAPIOrigem`: Instância preenchida com IdProcedimento e NumeroProtocolo.; `$objProcedimentoAPIDestino`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `obterAcoesAjaxExternasSemLogin` | Sem parâmetro | `$arrAcoes`: Conjunto de ações. |
| `obterAcoesExternasSemLogin` | Sem parâmetro | `$arrAcoes`: Conjunto de ações. |
| `obterConfiguracoesAssinatura` | `objConfiguracoesAssinaturaAPI`: Instância de ConfiguracoesAssinaturaAPI preenchida com NomeModulo. | `$objConfiguracoesAssinaturaAPI`: Instância com as configurações do módulo. |
| `obterDiretorioIconesMenu` | Sem parâmetro | `$strDiretorio`: Caminho do diretório que contém as imagens associadas com itens de menu. |
| `obterProximaDataPublicacao` | `objPublicacaoAPI`: Instância de PublicacaoAPI preenchida com: IdVeiculoPublicacao e StaTipoVeiculo. | `data`: Próxima data disponível para o veículo no formato dd/mm/aaaa. |
| `obterRelacaoVariaveisEditor` | Sem parâmetro | `$arrVariaveis`: Conjunto onde a chave é o nome da variável e o valor é sua descrição. |
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
| `removerRestricaoOuvidoria` | `$objDocumentoAPI`: Instância preenchida com IdDocumento e IdProcedimento. Chamado em `SolicitacaoOuvidoriaRN::alterarControlado`, depois de gravar a alteração, quando `SinBloqueio` deixa de ser S. | sem saida documentada |
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
| `validarContato` | `$objContatoAPI`: Instância preenchida com IdContato, IdTipoContato, IdContatoAssociado, StaNatureza, SinEnderecoAssociado, StaGenero, Cpf, Rg, OrgaoExpedidor, Matricula, MatriculaOab, NumeroPassaporte, IdPaisPassaporte, DataNascimento, Cnpj, IdCargo, Sigla, Nome, NomeSocial, TelefoneComercial, TelefoneResidencial, TelefoneCelular, Email, SitioInternet, Endereco, Complemento, Bairro, Cep, Observacao, SinAtivo, IdPais, IdEstado e IdCidade. | sem saida documentada |
| `validarEliminacaoDocumento` | `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento e NumeroProtocolo. | sem saida documentada |
| `validarEliminacaoProcesso` | `$objProcedimentoAPI`: Instância preenchida com IdProcedimento e NumeroProtocolo. | sem saida documentada |
| `verificarAcessoProtocolo` | `$arrObjProcedimentoAPI`: Instâncias preenchidas com IdProcedimento, IdTipoProcedimento, IdUnidadeGeradora e NivelAcesso.; `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento, IdProcedimento, IdSerie, IdUnidadeGeradora, Tipo, SubTipo e NivelAcesso. | `$arrLiberacoes`: Retornar um array indexado pelo número do protocolo onde cada item possui o valor P (Permitido) ou N (Negado) indicando o tipo de acesso ao processo ou documento. Também podem ser utilizadas as constantes abaixo da classe SeiIntegracao: //TAM = Tipo Acesso Modulo public static $TAM_PERMITIDO = 'P'; public static $TAM_NEGADO = 'N'; |
| `verificarAcessoProtocoloExterno` | `$arrObjProcedimentoAPI`: Instâncias representando os processos anexados preenchidas com IdProcedimento, IdTipoProcedimento, IdUnidadeGeradora e NivelAcesso.; `$arrObjDocumentoAPI`: Instâncias preenchidas com IdDocumento, IdProcedimento, IdSerie, IdUnidadeGeradora, SinAssinado, SinPublicado, Tipo, SubTipo e NivelAcesso. | `$arrLiberacoes`: Retornar um array indexado pelo número do protocolo onde cada item possui o valor P (Permitido) ou N (Negado) indicando o tipo de acesso ao processo ou documento. Também podem ser utilizadas as constantes abaixo da classe SeiIntegracao: //TAM = Tipo Acesso Modulo public static $TAM_PERMITIDO = 'P'; public static $TAM_NEGADO = 'N'; |
| `verificarAcessoTipoContato` | `$arrObjTipoContatoAPI`: Instâncias preenchidas com IdTipoContato. | `$arrLiberacoes`: Retornar um array indexado pelo ID do tipo de contato onde cada item possui os valores: N = nenhum acesso concedido pelo módulo A = permissão para alteração de dados C = Consulta Completa R = Consulta Resumida Também podem ser utilizadas as constantes abaixo da classe TipoContatoRN: public static $TA_NENHUM = 'N'; public static $TA_ALTERACAO = 'A'; public static $TA_CONSULTA_COMPLETA = 'C'; public static $TA_CONSULTA_RESUMIDA = 'R'; |
| `verificarLoginExterno` | `$objUsuarioAPI`: Instâncias preenchidas com IdUsuario, Sigla, Nome e StaTipo. | `booleano`: Retornar true ou false. |

## Assinaturas no core 5.0.6

O método do módulo repete a assinatura do evento em `SeiIntegracao.php`. No PHP 8, assinatura incompatível gera erro fatal ao carregar a classe de integração: `Declaration of ... must be compatible with ...`. O módulo recebe todos os parâmetros do core, e parâmetro a mais só entra com valor padrão. Tipo de parâmetro e de retorno segue a seção [Tipagem Segura](../../../references/padrao-codificacao-php.md#tipagem-segura).

```php
public function adicionarElementoMenu()
public function adicionarRestricaoOuvidoria(DocumentoAPI $objDocumentoAPI)
public function agendarPublicacao(PublicacaoAPI $objPublicacaoAPI)
public function alterarContato(ContatoAPI $objContatoAPI)
public function alterarDocumento(DocumentoAPI $objDocumentoAPI)
public function alterarHipoteseLegal(HipoteseLegalAPI $objHipoteseLegalAPI)
public function alterarIconeArvoreDocumento(ProcedimentoAPI $objProcedimentoAPI, $arrObjDocumentoAPI)
public function alterarProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function alterarPublicacao(PublicacaoAPI $objPublicacaoAPI)
public function alterarVeiculoPublicacao(VeiculoPublicacaoAPI $objVeiculoPublicacaoAPI)
public function anexarProcesso(ProcedimentoAPI $objProcedimentoAPIPrincipal, ProcedimentoAPI $objProcedimentoAPIAnexado)
public function assinarDocumento($arrObjDocumentoAPI)
public function atualizarConteudoDocumento(DocumentoAPI $objDocumentoAPI)
public function bloquearProcesso($arrObjProcedimentoAPI)
public function cadastrarContato(ContatoAPI $objContatoAPI)
public function cadastrarHipoteseLegal(HipoteseLegalAPI $objHipoteseLegalAPI)
public function cadastrarVeiculoPublicacao(VeiculoPublicacaoAPI $objVeiculoPublicacaoAPI)
public function cancelarAgendamentoPublicacao(PublicacaoAPI $objPublicacaoAPI)
public function cancelarAssinaturaDocumento(DocumentoAPI $objDocumentoAPI)
public function cancelarDisponibilizacaoAcessoExterno($arrObjAcessoExternoAPI)
public function cancelarDocumento(DocumentoAPI $objDocumentoAPI)
public function cancelarLiberacaoAssinaturaExterna($arrObjAcessoExternoAPI)
public function concluirProcesso($arrObjProcedimentoAPI)
public function confirmarAtualizacaoConteudoDocumento(DocumentoAPI $objDocumentoAPI)
public function confirmarPublicacao($arrObjPublicacaoAPI)
public function darCienciaDocumento(DocumentoAPI $objDocumentoAPI)
public function darCienciaProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function desanexarProcesso(ProcedimentoAPI $objProcedimentoAPIPrincipal, ProcedimentoAPI $objProcedimentoAPIAnexado)
public function desativarArquivoExtensao($arrObjArquivoExtensaoAPI)
public function desativarContato($arrObjContatoAPI)
public function desativarHipoteseLegal($arrObjHipoteseLegalAPI)
public function desativarTipoContato($arrObjTipoContatoAPI)
public function desativarTipoDocumento($arrObjSerieAPI)
public function desativarTipoProcesso($arrObjTipoProcedimentoAPI)
public function desativarUnidade($arrObjUnidadeAPI)
public function desativarUsuario($arrObjUsuarioAPI)
public function desativarVeiculoPublicacao($arrObjVeiculoPublicacaoAPI)
public function desbloquearProcesso($arrObjProcedimentoAPI)
public function eliminarDocumento($arrObjDocumentoAPI)
public function eliminarProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function enviarProcesso($arrObjProcedimentoAPI, $arrObjUnidadeAPI)
public function excluirArquivoExtensao($arrObjArquivoExtensaoAPI)
public function excluirContato($arrObjContatoAPI)
public function excluirDocumento(DocumentoAPI $objDocumentoAPI)
public function excluirHipoteseLegal($arrObjHipoteseLegalAPI)
public function excluirProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function excluirTipoContato($arrObjTipoContatoAPI)
public function excluirTipoDocumento($arrObjSerieAPI)
public function excluirTipoProcesso($arrObjTipoProcedimentoAPI)
public function excluirUnidade($arrObjUnidadeAPI)
public function excluirUsuario($arrObjUsuarioAPI)
public function excluirVeiculoPublicacao($arrObjVeiculoPublicacaoAPI)
public function gerarDocumento(DocumentoAPI $objDocumentoAPI)
public function gerarProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function inicializar($strVersaoSEI)
public function listarUnidadesEnvioProcesso($arrObjProcedimentoAPI)
public function montarAcaoControleAcessoExterno($arrObjAcessoExternoAPI)
public function montarAcaoDocumentoAcessoExternoAutorizado($arrObjDocumentoAPI)
public function montarAcaoDocumentoAcessoExternoNegado($arrObjDocumentoAPI)
public function montarAcaoProcessoAnexadoAcessoExternoAutorizado($arrObjProcedimentAPI)
public function montarAcaoProcessoAnexadoAcessoExternoNegado($arrObjProcedimentAPI)
public function montarAcaoPublicacao($arrObjPublicacaoAPI)
public function montarAcaoVeiculoPublicacao($arrObjVeiculoPublicacaoAPI)
public function montarBotaoAcessoExternoAutorizado(ProcedimentoAPI $objProcedimentoAPI)
public function montarBotaoAssinaturaExterno(UsuarioAPI $objUsuarioAPI)
public function montarBotaoAssinaturaInterno(UsuarioAPI $objUsuarioAPI)
public function montarBotaoCadastroDocumento(DocumentoAPI $objDocumentoAPI)
public function montarBotaoChatIA()
public function montarBotaoChatIAexterno()
public function montarBotaoControleAcessoExterno()
public function montarBotaoControleProcessos()
public function montarBotaoDocumento(ProcedimentoAPI $objProcedimentoAPI, $arrObjDocumentoAPI)
public function montarBotaoLoginExterno()
public function montarBotaoProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function montarBotaoVeiculoPublicacao($arrObjVeiculoPublicacaoAPI)
public function montarDadosImprensaNacional(PublicacaoAPI $objPublicacaoAPI)
public function montarIconeAcompanhamentoEspecial($arrObjProcedimentoAPI)
public function montarIconeControleProcessos($arrObjProcedimentoAPI)
public function montarIconeDocumento(ProcedimentoAPI $objProcedimentoAPI, $arrObjDocumentoAPI)
public function montarIconeOrdenarArvore(ProcedimentoAPI $objProcedimentoAPI)
public function montarIconeProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function montarIconeSistema()
public function montarMensagemProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function montarMenuConsultaProcessual()
public function montarMenuPublicacoes()
public function montarMenuUsuarioExterno()
public function montarTextoInformativoPublicacao(PublicacaoAPI $objPublicacaoAPI)
public function montarTipoTarjaAssinaturaCustomizada()
public function moverDocumento(DocumentoAPI $objDocumentoAPI, ProcedimentoAPI $objProcedimentoAPIOrigem, ProcedimentoAPI $objProcedimentoAPIDestino)
public function obterAcoesAjaxExternasSemLogin()
public function obterAcoesExternasSemLogin()
public function obterConfiguracoesAssinatura(ConfiguracoesAssinaturaAPI $objConfiguracoesAssinaturaAPI)
public function obterDiretorioIconesMenu()
public function obterProximaDataPublicacao(PublicacaoAPI $objPublicacaoAPI)
public function obterRelacaoVariaveisEditor()
public function ocultarAcaoAlterarPublicacao($arrObjPublicacaoAPI)
public function ocultarAcaoCancelarAgendamentoPublicacao($arrObjPublicacaoAPI)
public function ocultarBotaoSalvarPublicacao($arrObjVeiculoPublicacaoAPI)
public function ocultarDadosImprensaNacionalPublicacao($arrObjVeiculoPublicacaoAPI)
public function permitirAndamentoConcluido(AndamentoAPI $objAndamentoAPI)
public function prepararAssinaturaDocumento(AssinaturaAPI $objAssinaturaAPI)
public function prepararCloneDocumento(DocumentoAPI $objDocumentoAPI)
public function processarControlador($strAcao)
public function processarControladorAjax($strAcaoAjax)
public function processarControladorAjaxExterno($strAcaoAjax)
public function processarControladorExterno($strAcao)
public function processarControladorPublicacoes($strAcao)
public function processarControladorWebServices($strServico)
public function processarPaginaCadastroDocumento(DocumentoAPI $objDocumentoAPI)
public function processarPaginaInclusaoDocumentoItemEtapa(DocumentoAPI $objDocumentoAPI)
public function processarPesquisaRapida($strTexto)
public function processarVariaveisEditor(DocumentoAPI $objDocumentoAPI)
public function reabrirProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function reativarArquivoExtensao($arrObjArquivoExtensaoAPI)
public function reativarContato($arrObjContatoAPI)
public function reativarHipoteseLegal($arrObjHipoteseLegalAPI)
public function reativarTipoContato($arrObjTipoContatoAPI)
public function reativarTipoDocumento($arrObjSerieAPI)
public function reativarTipoProcesso($arrObjTipoProcedimentoAPI)
public function reativarUnidade($arrObjUnidadeAPI)
public function reativarUsuario($arrObjUsuarioAPI)
public function reativarVeiculoPublicacao($arrObjVeiculoPublicacaoAPI)
public function relacionarProcesso(ProcedimentoAPI $objProcedimentoAPI1, ProcedimentoAPI $objProcedimentoAPI2)
public function removerRelacionamentoProcesso(ProcedimentoAPI $objProcedimentoAPI1, ProcedimentoAPI $objProcedimentoAPI2)
public function removerRestricaoOuvidoria(DocumentoAPI $objDocumentoAPI)
public function removerSobrestamentoProcesso(ProcedimentoAPI $objProcedimentoAPI, $objProcedimentoAPIVinculado)
public function sobrestarProcesso(ProcedimentoAPI $objProcedimentoAPI, $objProcedimentoAPIVinculado)
public function substituirContato(ContatoAPI $objContatoAPI, $arrObjContatoAPI)
public function tratarLinkSemAssinatura($strLink)
public function validarContato(ContatoAPI $objContatoAPI)
public function validarEliminacaoDocumento($arrObjDocumentoAPI)
public function validarEliminacaoProcesso(ProcedimentoAPI $objProcedimentoAPI)
public function verificarAcessoProtocolo($arrObjProcedimentoAPI, $arrObjDocumentoAPI)
public function verificarAcessoProtocoloExterno($arrObjProcedimentoAPI, $arrObjDocumentoAPI)
public function verificarAcessoTipoContato($arrObjTipoContatoAPI)
public function verificarLoginExterno(UsuarioAPI $objUsuarioAPI)
```

## Manutenção: pontos de chamada conferidos no checkout

Esta tabela orienta a busca; reconfirme método, linhas e transação na versão suportada. Todas as nove famílias administrativas recebem arrays de objetos API; exclusão de processo/documento recebe objeto único. Examine escritas anteriores de registros filhos e os caminhos alternativos.

| Entidade/evento de exclusão | RN do core: evento → DELETE principal | Desativação: escrita → evento, dentro de Controlado |
|---|---|---|
| TipoProcesso | TipoProcedimentoRN:482 → 487 | 517 → 537 |
| TipoDocumento | SerieRN:447 → 452 | 591 → 613 |
| Unidade | UnidadeRN:455 → 463 | 586 → 617 |
| Usuario | UsuarioRN:904 → 931 | 1080 → 1118 |
| Contato | ContatoRN:989 → 994 | 1032 → 1060 |
| TipoContato | TipoContatoRN:256 → 268 | 364 → 384 |
| ArquivoExtensao | ArquivoExtensaoRN:251 → 256 | 351 → 371 |
| HipoteseLegal | HipoteseLegalRN:300, depois do DELETE:286; tarde para FK restritiva | 406 → 420 |
| VeiculoPublicacao | VeiculoPublicacaoRN:446, depois do DELETE:440; tarde para FK restritiva | 536 → 542 |
| excluirProcesso(ProcedimentoAPI) | ProcedimentoRN:976 → 982 | não se aplica |
| excluirDocumento(DocumentoAPI) | DocumentoRN:1570 → 1642; protocolo:1648 | não se aplica |

`validarEliminacaoDocumento(DocumentoAPI[])` é chamado em DocumentoRN:6278; `validarEliminacaoProcesso(ProcedimentoAPI)` em ProcedimentoRN:1396 e 1418, incluindo processos anexados. Exclusão e eliminação são caminhos distintos: não presumir cobertura de um pelo outro ou usar `eliminar*` como veto antecipado sem examinar o chamador. Não foi encontrado hook específico para excluir/desativar o cadastro de Assinantes das Unidades em SeiIntegracao; AssinanteRN:163-194 exclui sem evento. A presença de eventos de assinatura de documento não cobre esse cadastro.

Para qualquer outro evento de SeiIntegracao que afete registro persistido referenciado pelo módulo, aplique [proteção das dependências](protecao-dependencias-core.md); esta tabela não é lista fechada de entidades elegíveis.
