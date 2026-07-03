# Catálogo de Classes API do SEI (v5.0 — Cap. 8)

> Fonte: `docs/manual_desenvolvimento_md/sei_modulos_manual_dev_8_classes_api.md`
> Uso: localizar o contrato oficial antes de propor acesso ao core, classe interna ou implementacao propria.

Se a duvida do desenvolvedor ainda estiver ambigua entre API, evento e
operacao, usar primeiro `sei-direcionador-integracao`.

## Objetos de Domínio

| Nome | Descrição | Quando usar |
|---|---|---|
| ProcedimentoAPI | Dados completos de um processo (id, protocolo, tipo, assuntos, interessados, nivel acesso, etc.) | Ler dados de processo; consultar informacoes de geracao |
| DocumentoAPI | Dados de um documento (id, protocolo, tipo, numero, nivel acesso,Tree nome, etc.) | Ler dados de documento; verificar documento em processo |
| AndamentoAPI | Dado de um registro no historico (id, tarefa, descricao, data/hora, usuario, unidade, atributos) | Ler historico; recuperar detalhes de andamento |
| PublicacaoAPI | Dado de publicacao de documento (id, documento, veiculo, tipo, numero, data, estado) | Verificar status de publicacao; consultar veiculos |
| UsuarioAPI | Dado de usuario do sistema (id, nome, sigla, orgao) | Identificar usuario em andamentos; contexto de atribuicao |
| UnidadeAPI | Dado de unidade organizacional (id, sigla, descricao) | Identificar unidade em andamentos; filtrar por origem |
| TipoProcedimentoAPI | Dado de tipo de processo (id, nome, especie) | Identificar tipo de processo em consulta; filtrar por especie |
| SerieAPI | Dado de tipo de documento (id, nome, descricao) | Identificar tipo de documento em consulta; filtrar series |
| HipoteseLegalAPI | Dado de hipotese legal (id, base legal, descricao) | Identificar hipotese legal em procedimento; auditoria |
| ContatoAPI | Dado de pessoa (fisica/juridica) com atributos completos (id, nome, cpf, cnpj, matricula, endereco, etc.) | Gerar ou atualizar contatos; associar interessado |
| AssinaturaAPI | Dado de assinatura em documento (nome, cargo, data/hora, cpf, tipo autenticacao) | Verificar assinatura; confirmar autenticidade |
| BlocoAPI | Dado de bloco de documentos (id, titulo, estado, criador) | Consultar bloco; gerenciar documento em bloco |
| MarcadorAPI | Dado de marcador de unidade (id, nome, descricao) | Listar marcadores; associar marcador a processo |
| AcessoExternoAPI | Dado de acesso externo concedido (id, validade, procedimento, documento, tipo) | Verificar acesso externo ativo; controlar visibilidade |
| AtributoAndamentoAPI | Par nome/valor para variaveis em texto de andamento (@VAR@) | Preencher textos com variaveis em lancarAndamento |

## Entradas (Objetos de Consulta / Acao)

### Contratos com sinais de dominio detalhados

| Nome | Descrição | Campos de domínio relevantes | Quando usar |
|---|---|---|---|
| EntradaGerarProcedimentoAPI | Dados para geracao de processo: procedimento, documentos, relacionados, envio, prazo, marcador | `UnidadesEnvio`, `SinManterAbertoUnidade`, `SinEnviarEmailNotificacao`, `DataRetornoProgramado`, `DiasRetornoProgramado`, `IdMarcador`, `TextoMarcador`, `DataControlePrazo`, `DiasControlePrazo` | Gerar novo processo via sei-mod-api-operacoes; geracao automatica; fluxo de trabalho com prazo, envio e organizacao |
| EntradaEnviarProcessoAPI | Dados para enviar processo a unidades | `UnidadesDestino`, `SinManterAbertoUnidade`, `SinRemoverAnotacao`, `SinEnviarEmailNotificacao`, `DataRetornoProgramado`, `DiasRetornoProgramado`, `SinDiasUteisRetornoProgramado`, `SinReabrir` | Enviar processo a outra unidade; fluxo de trabalho; retorno programado |
| EntradaAtribuirProcessoAPI | Dados para atribuir processo a usuario na unidade | `IdUsuario`, `SinReabrir` | Atribuir processo; redistribuir carga; definir responsavel |
| EntradaDefinirControlePrazoAPI | Dados para definir prazo em processo | `DataPrazo`, `Dias`, `SinDiasUteis` | Definir controle de prazo em processo; vencimento; acompanhamento |
| EntradaIncluirDocumentoBlocoAPI | Dados para incluir documento em bloco | `IdBloco`, `IdDocumento ou ProtocoloDocumento`, `Anotacao` | Disponibilizar documento em bloco; organizacao de analise |
| EntradaIncluirProcessoBlocoAPI | Dados para incluir processo em bloco | `IdBloco`, `IdProcedimento ou ProtocoloProcedimento`, `Anotacao` | Adicionar processo a bloco; agrupamento de trabalho |
| EntradaLancarAndamentoAPI | Dados para lancar andamento em processo | `IdTarefa`, `IdTarefaModulo`, `Atributos` | Registrar andamento; historico; atualizacao de trabalho |
| DefinicaoMarcadorAPI | Contrato para associar marcador a processo | `IdProcedimento ou ProtocoloProcedimento`, `IdMarcador`, `Texto` | Marcar processo; categorizar; organizar trabalho |

### Outros contratos de entrada

| Nome | Descrição | Quando usar |
|---|---|---|
| EntradaConsultarProcedimentoAPI | Filtros para consulta de processo com opcoes de retorno detalhado (assuntos, interessados, andamentos, etc.) | Consultar processo especifico via sei-mod-api-operacoes |
| EntradaConsultarProcedimentoIndividualAPI | Filtros por orgao, tipo procedimento e usuario para consulta individual | Consulta restrita a contexto de usuario/orgao |
| EntradaConsultarDocumentoAPI | Filtros para consulta de documento com opcoes de retorno (andamento, assinaturas) | Consultar documento especifico via sei-mod-api-operacoes |
| EntradaConsultarPublicacaoAPI | Filtros para consulta de publicacao (id, documento, protocolo, retornos) | Verificar publicacao de documento especifico |
| EntradaListarAndamentosAPI | Filtros para listar andamentos de processo com opcao de atributos e filtros por id | Listar historico completo com filtro granular |
| EntradaListarAndamentosMarcadoresAPI | Filtros por marcadores para listar andamentos de processo por marcador | Listar andamentos por marcador especifico |
| EntradaBloquearDocumentoAPI | Dados para bloquear documento (id documento, motivo) | Bloquear documento; suspender acesso |
| EntradaCancelarDocumentoAPI | Dados para cancelar documento (id documento, motivo) | Cancelar documento; invalidar documento |
| EntradaExcluirDocumentoAPI | Dados para excluir documento (id documento) | Excluir documento; remocao |
| EntradaSobrestarProcessoAPI | Dados para sobrestar processo (id ou protocolo, motivo) | Sobrestar processo; criar impedimento |
| EntradaAnexarProcessoAPI | Dados para anexar processo a processo principal | Anexar processo; vincular |
| EntradaDesanexarProcessoAPI | Dados para desanexar processo (ids e protocolo de principal e anexado, motivo) | Desanexar processo; desvincular |
| EntradaRelacionarProcessoAPI | Dados para relacionar processos (id principal, ids relacionados) | Relacionar processos; criar vinculo lateral |
| EntradaBloquearProcessoAPI | Dados para bloquear processo (id ou protocolo, motivo) | Bloquear processo; restringir acesso |
| EntradaConcluirProcessoAPI | Dados para concluir processo (id ou protocolo, id unidade) | Concluir processo; finalizar tramite |
| EntradaReabrirProcessoAPI | Dados para reabrir processo (id ou protocolo, id unidade) | Reabrir processo; reativar tramite |
| EntradaListarCargosAPI | Filtro opcional por id de cargo | Listar cargos; populacao de combo |
| EntradaListarCidadesAPI | Filtro por pais e estado | Listar cidades; populacao de combo |
| EntradaListarContatosAPI | Filtros por id, tipo, sigla, nome, cpf, cnpj, matricula com paginacao | Listar contatos; buscar pessoa; autocomplete |
| EntradaListarEstadosAPI | Sem filtros | Listar estados; populacao de combo |
| EntradaListarHipotesesLegaisAPI | Sem filtros | Listar hipoteses legais; populacao de combo |
| EntradaListarSeriesAPI | Sem filtros | Listar series/tipos de documento; populacao de combo |
| EntradaListarTiposProcedimentoAPI | Sem filtros | Listar tipos de processo; populacao de combo |
| EntradaListarUnidadesAPI | Sem filtros ou filtro por id | Listar unidades; populacao de combo |
| EntradaListarUsuariosAPI | Filtro opcional por id de unidade | Listar usuarios; populacao de combo |
| EntradaAgendarPublicacaoAPI | Dados para agendar publicacao (id documento, id veiculo, tipo, data) | Agendar publicacao; agendar veiculo interno |
| EntradaAlterarPublicacaoAPI | Dados para alterar publicacao agendada | Alterar publicacao ja agendada |
| EntradaCancelarAgendamentoPublicacaoAPI | Dados para cancelar agendamento de publicacao | Cancelar publicacao agendada |

## Saidas (Retornos de Consulta)

### Contratos de saida com sinais de dominio detalhados

| Nome | Descrição | Campos de domínio relevantes | Quando usar |
|---|---|---|---|
| SaidaGerarProcedimentoAPI | Retorno de geracao com identificadores do processo e dos documentos incluidos | `IdProcedimento`, `ProcedimentoFormatado`, `LinkAcesso`, `RetornoInclusaoDocumentos` | Confirmar geracao; link de acesso; acompanhar documentos gerados no fluxo |
| SaidaConsultarProcedimentoAPI | Dados detalhados de processo | `AndamentoGeracao`, `AndamentoConclusao`, `UltimoAndamento`, `UnidadesProcedimentoAberto`, `Assuntos` | Retorno de consultarProcedimento; dados para tela de processo; acompanhar unidades e historico |
| SaidaConsultarDocumentoAPI | Dados detalhados de documento | `UnidadeElaboradora`, `AndamentoGeracao`, `Assinaturas`, `Publicacao`, `Blocos`, `Campos` | Retorno de consultarDocumento; dados para tela de documento; verificar contexto de bloco e publicacao |
| SaidaConsultarBlocoAPI | Dados detalhados de bloco | `Descricao`, `Unidade`, `Usuario`, `UsuarioAtribuicao`, `Protocolos` | Retorno de consultarBloco; informacoes de colaboracao e atribuicao |

### Outros contratos de saida

| Nome | Descrição | Quando usar |
|---|---|---|
| SaidaConsultarProcedimentoAPI | Dados detalhados de processo (id, protocolo, especificacao, nivel acesso, LinkAcesso, tipo, andamentos, assuntos, unidades abertas) | Retorno de consultarProcedimento; dados para tela de processo |
| SaidaConsultarDocumentoAPI | Dados detalhados de documento (id, protocolo, nivel acesso, LinkAcesso, serie, numero, data, unidade elaboradora, andamentos, assinaturas, publicacao, blocos, campos) | Retorno de consultarDocumento; dados para tela de documento |
| SaidaConsultarPublicacaoAPI | Dados de publicacao (id, documento, veiculo, tipo, numero, data, resumo, estado, imprensa nacional) | Retorno de consultarPublicacao; verificar publicacao |
| SaidaIncluirDocumentoAPI | Retorno de inclusao de documento com identificador e protocolo | Confirmar inclusao; referenciar documento em fluxo |

## Notas sobre ambiguidades do manual

1. `consultarPublicacao` (cap 10) menciona saida como `PublicacaoAPI`, mas o cap 8 define `SaidaConsultarPublicacaoAPI`. Considerar `SaidaConsultarPublicacaoAPI` como contrato oficial.

2. `RetornoInclusaoDocumentoAPI` e citado em `SaidaGerarProcedimentoAPI` como parte do retorno de geracao, mas nao tem secao propria no cap 8. Pode existir como subclasse interna.

3. `definirControlePrazo` e `definirMarcador` no cap 10 usam cabecalho "Saida" nos exemplos, mas os campos correspondem a entrada. Tratar como entrada.

4. `ConfirmarDisponibilizacaoPublicacao` no cap 10 tem variacao de capitalizacao e nome de atributo (`IdVeiculoDisponibilizacao` vs `setIdVeiculoPublicacao`). Verificar o nome correto no codigo do SEI antes de usar.

5. Atributos com typos no manual: `SinRetornarObervacoes` (falta "s" em Observacoes), `SinAnonimoOuvidoria` vs `SinOuvidoriaAnonimo`. Em caso de duvida, verificar no codigo fonte do SEI em `sei/web/api/` para confirmar o nome exato.

## Aviso importante

**Nao e recomendado o uso de classes internas do sistema alem das classes API documentadas neste capitulo.**
Se uma necessidade nao estiver coberta por nenhuma classe API listada acima, sinalizar como gap e propor abordagem com justificativa de seguranca antes de usar classes internas.

Se a necessidade encontrada for executar uma operacao oficial ou interceptar um
hook do core, encaminhar respectivamente para `sei-mod-api-operacoes` ou
`sei-mod-api-eventos`, em vez de alongar a triagem nesta referencia.
