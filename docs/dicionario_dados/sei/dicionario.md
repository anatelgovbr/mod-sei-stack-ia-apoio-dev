# Dicionário de Dados do SEI - v5.0.4

## Índice de Tabelas

- [acao_federacao](#acao_federacao)
- [acesso](#acesso)
- [acesso_externo](#acesso_externo)
- [acesso_federacao](#acesso_federacao)
- [acompanhamento](#acompanhamento)
- [andamento_instalacao](#andamento_instalacao)
- [andamento_marcador](#andamento_marcador)
- [andamento_plano_trabalho](#andamento_plano_trabalho)
- [andamento_situacao](#andamento_situacao)
- [anexo](#anexo)
- [anotacao](#anotacao)
- [arquivamento](#arquivamento)
- [arquivo_extensao](#arquivo_extensao)
- [assinante](#assinante)
- [assinatura](#assinatura)
- [assunto](#assunto)
- [assunto_proxy](#assunto_proxy)
- [atividade](#atividade)
- [atributo](#atributo)
- [atributo_andam_plano_trab](#atributo_andam_plano_trab)
- [atributo_andamento](#atributo_andamento)
- [atributo_instalacao](#atributo_instalacao)
- [auditoria_protocolo](#auditoria_protocolo)
- [avaliacao_documental](#avaliacao_documental)
- [aviso](#aviso)
- [base_conhecimento](#base_conhecimento)
- [base_conhecimento_idx](#base_conhecimento_idx)
- [bloco](#bloco)
- [campo_pesquisa](#campo_pesquisa)
- [cargo](#cargo)
- [cargo_funcao](#cargo_funcao)
- [categoria](#categoria)
- [cidade](#cidade)
- [codigo_acesso](#codigo_acesso)
- [comentario](#comentario)
- [conjunto_estilos](#conjunto_estilos)
- [conjunto_estilos_item](#conjunto_estilos_item)
- [contato](#contato)
- [controle_interno](#controle_interno)
- [controle_prazo](#controle_prazo)
- [controle_unidade](#controle_unidade)
- [documento](#documento)
- [documento_conteudo](#documento_conteudo)
- [documento_geracao](#documento_geracao)
- [dominio](#dominio)
- [edital_eliminacao](#edital_eliminacao)
- [edital_eliminacao_conteudo](#edital_eliminacao_conteudo)
- [edital_eliminacao_erro](#edital_eliminacao_erro)
- [email_grupo_email](#email_grupo_email)
- [email_sistema](#email_sistema)
- [email_unidade](#email_unidade)
- [email_utilizado](#email_utilizado)
- [estatisticas](#estatisticas)
- [estilo](#estilo)
- [etapa_trabalho](#etapa_trabalho)
- [feed](#feed)
- [feriado](#feriado)
- [grupo_acompanhamento](#grupo_acompanhamento)
- [grupo_bloco](#grupo_bloco)
- [grupo_contato](#grupo_contato)
- [grupo_email](#grupo_email)
- [grupo_federacao](#grupo_federacao)
- [grupo_protocolo_modelo](#grupo_protocolo_modelo)
- [grupo_serie](#grupo_serie)
- [grupo_unidade](#grupo_unidade)
- [hipotese_legal](#hipotese_legal)
- [imagem_formato](#imagem_formato)
- [infra_agendamento_tarefa](#infra_agendamento_tarefa)
- [infra_auditoria](#infra_auditoria)
- [infra_captcha](#infra_captcha)
- [infra_dado_usuario](#infra_dado_usuario)
- [infra_editor_comentario](#infra_editor_comentario)
- [infra_erro_php](#infra_erro_php)
- [infra_log](#infra_log)
- [infra_navegador](#infra_navegador)
- [infra_parametro](#infra_parametro)
- [infra_regra_auditoria](#infra_regra_auditoria)
- [infra_regra_auditoria_recurso](#infra_regra_auditoria_recurso)
- [infra_sequencia](#infra_sequencia)
- [instalacao_federacao](#instalacao_federacao)
- [item_etapa](#item_etapa)
- [lembrete](#lembrete)
- [lixeira](#lixeira)
- [localizador](#localizador)
- [lugar_localizador](#lugar_localizador)
- [mapeamento_assunto](#mapeamento_assunto)
- [marcador](#marcador)
- [modelo](#modelo)
- [monitoramento_servico](#monitoramento_servico)
- [nivel_acesso_permitido](#nivel_acesso_permitido)
- [notificacao](#notificacao)
- [novidade](#novidade)
- [numeracao](#numeracao)
- [observacao](#observacao)
- [operacao_servico](#operacao_servico)
- [ordenador_despesa](#ordenador_despesa)
- [orgao](#orgao)
- [orgao_federacao](#orgao_federacao)
- [orgao_historico](#orgao_historico)
- [pais](#pais)
- [parametro_acao_federacao](#parametro_acao_federacao)
- [participante](#participante)
- [pesquisa](#pesquisa)
- [plano_trabalho](#plano_trabalho)
- [procedimento](#procedimento)
- [protocolo](#protocolo)
- [protocolo_federacao](#protocolo_federacao)
- [protocolo_idx](#protocolo_idx)
- [protocolo_modelo](#protocolo_modelo)
- [publicacao](#publicacao)
- [publicacao_idx](#publicacao_idx)
- [publicacao_legado](#publicacao_legado)
- [reabertura_programada](#reabertura_programada)
- [rel_acesso_ext_protocolo](#rel_acesso_ext_protocolo)
- [rel_acesso_ext_serie](#rel_acesso_ext_serie)
- [rel_assinante_unidade](#rel_assinante_unidade)
- [rel_aviso_orgao](#rel_aviso_orgao)
- [rel_base_conhec_tipo_proced](#rel_base_conhec_tipo_proced)
- [rel_bloco_protocolo](#rel_bloco_protocolo)
- [rel_bloco_unidade](#rel_bloco_unidade)
- [rel_controle_interno_orgao](#rel_controle_interno_orgao)
- [rel_controle_interno_serie](#rel_controle_interno_serie)
- [rel_controle_interno_tipo_proc](#rel_controle_interno_tipo_proc)
- [rel_controle_interno_unidade](#rel_controle_interno_unidade)
- [rel_grupo_contato](#rel_grupo_contato)
- [rel_grupo_fed_orgao_fed](#rel_grupo_fed_orgao_fed)
- [rel_grupo_unidade_unidade](#rel_grupo_unidade_unidade)
- [rel_item_etapa_documento](#rel_item_etapa_documento)
- [rel_item_etapa_serie](#rel_item_etapa_serie)
- [rel_item_etapa_unidade](#rel_item_etapa_unidade)
- [rel_notificacao_documento](#rel_notificacao_documento)
- [rel_orgao_pesquisa](#rel_orgao_pesquisa)
- [rel_protocolo_assunto](#rel_protocolo_assunto)
- [rel_protocolo_atributo](#rel_protocolo_atributo)
- [rel_protocolo_protocolo](#rel_protocolo_protocolo)
- [rel_secao_mod_cj_estilos_item](#rel_secao_mod_cj_estilos_item)
- [rel_secao_modelo_estilo](#rel_secao_modelo_estilo)
- [rel_serie_assunto](#rel_serie_assunto)
- [rel_serie_plano_trabalho](#rel_serie_plano_trabalho)
- [rel_serie_veiculo_publicacao](#rel_serie_veiculo_publicacao)
- [rel_situacao_unidade](#rel_situacao_unidade)
- [rel_tipo_procedimento_assunto](#rel_tipo_procedimento_assunto)
- [rel_unidade_tipo_contato](#rel_unidade_tipo_contato)
- [rel_usuario_grupo_acomp](#rel_usuario_grupo_acomp)
- [rel_usuario_grupo_bloco](#rel_usuario_grupo_bloco)
- [rel_usuario_marcador](#rel_usuario_marcador)
- [rel_usuario_tipo_prioridade](#rel_usuario_tipo_prioridade)
- [rel_usuario_tipo_proced](#rel_usuario_tipo_proced)
- [rel_usuario_usuario_unidade](#rel_usuario_usuario_unidade)
- [replicacao_federacao](#replicacao_federacao)
- [retorno_programado](#retorno_programado)
- [revisao_avaliacao](#revisao_avaliacao)
- [secao_documento](#secao_documento)
- [secao_imprensa_nacional](#secao_imprensa_nacional)
- [secao_modelo](#secao_modelo)
- [seq_acesso](#seq_acesso)
- [seq_acesso_externo](#seq_acesso_externo)
- [seq_acompanhamento](#seq_acompanhamento)
- [seq_andamento_instalacao](#seq_andamento_instalacao)
- [seq_andamento_marcador](#seq_andamento_marcador)
- [seq_andamento_plano_trabalho](#seq_andamento_plano_trabalho)
- [seq_andamento_situacao](#seq_andamento_situacao)
- [seq_anexo](#seq_anexo)
- [seq_anotacao](#seq_anotacao)
- [seq_arquivo_extensao](#seq_arquivo_extensao)
- [seq_assinante](#seq_assinante)
- [seq_assinatura](#seq_assinatura)
- [seq_assunto](#seq_assunto)
- [seq_assunto_proxy](#seq_assunto_proxy)
- [seq_atividade](#seq_atividade)
- [seq_atributo](#seq_atributo)
- [seq_atributo_andam_plano_trab](#seq_atributo_andam_plano_trab)
- [seq_atributo_andamento](#seq_atributo_andamento)
- [seq_atributo_andamento_situaca](#seq_atributo_andamento_situaca)
- [seq_atributo_instalacao](#seq_atributo_instalacao)
- [seq_auditoria_protocolo](#seq_auditoria_protocolo)
- [seq_avaliacao_documental](#seq_avaliacao_documental)
- [seq_aviso](#seq_aviso)
- [seq_base_conhecimento](#seq_base_conhecimento)
- [seq_bloco](#seq_bloco)
- [seq_campo_pesquisa](#seq_campo_pesquisa)
- [seq_cargo](#seq_cargo)
- [seq_categoria](#seq_categoria)
- [seq_cidade](#seq_cidade)
- [seq_comentario](#seq_comentario)
- [seq_conjunto_estilos](#seq_conjunto_estilos)
- [seq_conjunto_estilos_item](#seq_conjunto_estilos_item)
- [seq_contato](#seq_contato)
- [seq_controle_interno](#seq_controle_interno)
- [seq_controle_prazo](#seq_controle_prazo)
- [seq_controle_unidade](#seq_controle_unidade)
- [seq_documento](#seq_documento)
- [seq_dominio](#seq_dominio)
- [seq_edital_eliminacao](#seq_edital_eliminacao)
- [seq_edital_eliminacao_conteudo](#seq_edital_eliminacao_conteudo)
- [seq_edital_eliminacao_erro](#seq_edital_eliminacao_erro)
- [seq_email_grupo_email](#seq_email_grupo_email)
- [seq_email_sistema](#seq_email_sistema)
- [seq_email_unidade](#seq_email_unidade)
- [seq_email_utilizado](#seq_email_utilizado)
- [seq_estatisticas](#seq_estatisticas)
- [seq_estilo](#seq_estilo)
- [seq_etapa_trabalho](#seq_etapa_trabalho)
- [seq_feed](#seq_feed)
- [seq_feriado](#seq_feriado)
- [seq_grupo_acompanhamento](#seq_grupo_acompanhamento)
- [seq_grupo_bloco](#seq_grupo_bloco)
- [seq_grupo_contato](#seq_grupo_contato)
- [seq_grupo_email](#seq_grupo_email)
- [seq_grupo_federacao](#seq_grupo_federacao)
- [seq_grupo_protocolo_modelo](#seq_grupo_protocolo_modelo)
- [seq_grupo_serie](#seq_grupo_serie)
- [seq_grupo_unidade](#seq_grupo_unidade)
- [seq_hipotese_legal](#seq_hipotese_legal)
- [seq_imagem_formato](#seq_imagem_formato)
- [seq_infra_auditoria](#seq_infra_auditoria)
- [seq_infra_log](#seq_infra_log)
- [seq_infra_navegador](#seq_infra_navegador)
- [seq_item_etapa](#seq_item_etapa)
- [seq_lembrete](#seq_lembrete)
- [seq_lixeira](#seq_lixeira)
- [seq_localizador](#seq_localizador)
- [seq_lugar_localizador](#seq_lugar_localizador)
- [seq_marcador](#seq_marcador)
- [seq_modelo](#seq_modelo)
- [seq_monitoramento_servico](#seq_monitoramento_servico)
- [seq_nivel_acesso_permitido](#seq_nivel_acesso_permitido)
- [seq_notificacao](#seq_notificacao)
- [seq_novidade](#seq_novidade)
- [seq_numeracao](#seq_numeracao)
- [seq_observacao](#seq_observacao)
- [seq_operacao_servico](#seq_operacao_servico)
- [seq_ordenador_despesa](#seq_ordenador_despesa)
- [seq_orgao_historico](#seq_orgao_historico)
- [seq_pais](#seq_pais)
- [seq_participante](#seq_participante)
- [seq_pesquisa](#seq_pesquisa)
- [seq_plano_trabalho](#seq_plano_trabalho)
- [seq_protocolo](#seq_protocolo)
- [seq_protocolo_modelo](#seq_protocolo_modelo)
- [seq_publicacao](#seq_publicacao)
- [seq_reabertura_programada](#seq_reabertura_programada)
- [seq_rel_protocolo_protocolo](#seq_rel_protocolo_protocolo)
- [seq_rel_unidade_tipo_contato](#seq_rel_unidade_tipo_contato)
- [seq_retorno_programado](#seq_retorno_programado)
- [seq_revisao_avaliacao](#seq_revisao_avaliacao)
- [seq_secao_documento](#seq_secao_documento)
- [seq_secao_imprensa_nacional](#seq_secao_imprensa_nacional)
- [seq_secao_modelo](#seq_secao_modelo)
- [seq_serie](#seq_serie)
- [seq_serie_publicacao](#seq_serie_publicacao)
- [seq_serie_restricao](#seq_serie_restricao)
- [seq_servico](#seq_servico)
- [seq_situacao](#seq_situacao)
- [seq_tabela_assuntos](#seq_tabela_assuntos)
- [seq_tarefa](#seq_tarefa)
- [seq_tarja_assinatura](#seq_tarja_assinatura)
- [seq_termo_uso](#seq_termo_uso)
- [seq_texto_padrao_interno](#seq_texto_padrao_interno)
- [seq_tipo_conferencia](#seq_tipo_conferencia)
- [seq_tipo_contato](#seq_tipo_contato)
- [seq_tipo_formulario](#seq_tipo_formulario)
- [seq_tipo_localizador](#seq_tipo_localizador)
- [seq_tipo_prioridade](#seq_tipo_prioridade)
- [seq_tipo_proced_restricao](#seq_tipo_proced_restricao)
- [seq_tipo_procedimento](#seq_tipo_procedimento)
- [seq_tipo_suporte](#seq_tipo_suporte)
- [seq_titulo](#seq_titulo)
- [seq_tratamento](#seq_tratamento)
- [seq_uf](#seq_uf)
- [seq_unidade_historico](#seq_unidade_historico)
- [seq_unidade_publicacao](#seq_unidade_publicacao)
- [seq_upload](#seq_upload)
- [seq_veiculo_imprensa_nacional](#seq_veiculo_imprensa_nacional)
- [seq_veiculo_publicacao](#seq_veiculo_publicacao)
- [seq_versao_secao_documento](#seq_versao_secao_documento)
- [seq_vocativo](#seq_vocativo)
- [serie](#serie)
- [serie_escolha](#serie_escolha)
- [serie_publicacao](#serie_publicacao)
- [serie_restricao](#serie_restricao)
- [servico](#servico)
- [sinalizacao_federacao](#sinalizacao_federacao)
- [situacao](#situacao)
- [solicitacao_ouvidoria](#solicitacao_ouvidoria)
- [tabela_assuntos](#tabela_assuntos)
- [tarefa](#tarefa)
- [tarefa_instalacao](#tarefa_instalacao)
- [tarefa_plano_trabalho](#tarefa_plano_trabalho)
- [tarja_assinatura](#tarja_assinatura)
- [termo_uso](#termo_uso)
- [texto_padrao_interno](#texto_padrao_interno)
- [tipo_conferencia](#tipo_conferencia)
- [tipo_contato](#tipo_contato)
- [tipo_formulario](#tipo_formulario)
- [tipo_localizador](#tipo_localizador)
- [tipo_prioridade](#tipo_prioridade)
- [tipo_proced_restricao](#tipo_proced_restricao)
- [tipo_procedimento](#tipo_procedimento)
- [tipo_procedimento_escolha](#tipo_procedimento_escolha)
- [tipo_suporte](#tipo_suporte)
- [titulo](#titulo)
- [tratamento](#tratamento)
- [uf](#uf)
- [unidade](#unidade)
- [unidade_federacao](#unidade_federacao)
- [unidade_historico](#unidade_historico)
- [unidade_publicacao](#unidade_publicacao)
- [usuario](#usuario)
- [usuario_configuracao](#usuario_configuracao)
- [usuario_federacao](#usuario_federacao)
- [usuario_login](#usuario_login)
- [veiculo_imprensa_nacional](#veiculo_imprensa_nacional)
- [veiculo_publicacao](#veiculo_publicacao)
- [versao_secao_documento](#versao_secao_documento)
- [vocativo](#vocativo)

## acao_federacao

Armazena as informações sobre as ações realizadas no SEI Federação.

| Coluna | Descrição |
|---|---|
| id_acao_federacao | Número ID que identifica a ação realizada no SEI Federação. |
| dth_acesso | Data correspondente ao momento do pedido de acesso. |
| dth_geracao | Data correspondente ao momento da validação do acesso. |
| id_documento_federacao | Número ID que identifica o número do documento envolvido na ação. Equivale à coluna id_protocolo_federação da Tabela protocolo_federacao. |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão participante da ação realizada no SEI Federação. |
| id_orgao_federacao | Número ID que identifica o órgão participante da ação realizada no SEI Federação. |
| id_procedimento_federacao | Número ID que identifica o número do processo envolvido na ação. Equivale à coluna id_protocolo_federação da Tabela protocolo_federacao. |
| id_unidade_federacao | Número ID que identifica a Unidade Interna do órgão participante da ação realizada no SEI Federação. |
| id_usuario_federacao | Número ID que identifica o usuário do órgão participante da ação realizada no SEI Federação. |
| sin_ativo | Variável categórica que indica se a ação está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo de ação no SEI Federação:<br><br><ul><li>1 = Visualizar Documento</li><li>2 = Gerar PDF</li><li>3 = Gerar ZIP</li></ul> |

## acesso

Armazena os Usuários ou Unidades que possuem acesso a um determinado processo e o tipo do acesso.

| Coluna | Descrição |
|---|---|
| id_acesso | Número ID que identifica o acesso. |
| id_controle_interno | Número ID que identifica o Controle Interno parametrizado na Administração do SEI. O id_controle_interno somente é apresentado se o Acesso tiver sta_tipo = C. |
| id_protocolo | Número ID que identifica o protocolo relativo ao acesso, aplicável para todos os valores de sta_tipo. |
| id_unidade | Número ID que identifica a unidade que possui acesso ao processo, aplicável para todos os valores de sta_tipo. |
| id_usuario | Número ID que identifica o usuário que possui Credencial de Acesso ao Processo, quando sta_tipo = S, A ou D. |
| sta_tipo | Status multi-valorado que identifica o Tipo de Acesso:<br><br><ul><li>R = Restrito à Unidade que pode acessar o processo conforme id_unidade, quando o protocolo do processo possui sta_nivel_acesso_global = 1 na tabela protocolo (TA_RESTRITO_UNIDADE)</li><li>S = Credencial de Acesso ao Processo, quando o protocolo do processo possui sta_nivel_acesso_global igual a 2, identifica os Usuários de determinadas Unidades que podem acessar o processo (TA_CREDENCIAL_PROCESSO)</li><li>A = Credencial de Assinatura no Processo, quando o protocolo do processo possui sta_nivel_acesso_global igual a 2, identifica os Usuários de determinadas Unidades que podem acessar o processo em razão de Credencial de Assinatura concedida sobre algum documento no processo (TA_CREDENCIAL_ASSINATURA_PROCESSO)</li><li>D = Credencial de Assinatura para Documento, quando o protocolo do processo possui sta_nivel_acesso_global igual a 2, identifica o documento disponibilizado para assinatura de determinado Usuário e Unidade por meio de Credencial de Assinatura (TA_CREDENCIAL_ASSINATURA_DOCUMENTO)</li><li>C = Identifica que o acesso ao Processo é em razão de Controle Interno parametrizado na Administração do SEI (TA_CONTROLE_INTERNO)</li></ul> |

## acesso_externo

Armazena os Usuários ou Unidades que possuem acesso do tipo Externo a um determinado processo e o tipo do acesso.

| Coluna | Descrição |
|---|---|
| id_acesso_externo | Número ID que identifica o acesso externo. |
| dta_validade | Data limite da validade do acesso externo. |
| dth_visualizacao | Registra o momento que o acesso ao processo é realizado pelo destinatário em seu ambiente de usuário externo; ou quando o link de acesso enviado ao e-mail do destinatário é clicado. |
| email_destinatario | E-mail do destinatário do acesso externo quando envolve acesso externo para Interessado. Usuário Externo e Destinatário Isolado (sta_tipo = I, E ou D). |
| email_unidade | E-mail da unidade utilizado na disponibilização do acesso externo. |
| hash_interno | Código do hash interno utilizado no link do acesso externo. |
| id_atividade | Número ID que identifica a atividade do participante no acesso externo. |
| id_documento | Número ID que identifica o documento disponibilizado no acesso externo para assinatura externa. Estará preenchido apenas com o sta_tipo igual a I, E, D e S e quando o acesso ao processo (sin_processo for igual a S) |
| id_participante | Número ID que identifica o participante do acesso externo. |
| sin_ativo | Variável categórica que indica se o acesso externo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_inclusao | Variável categórica que indica se o acesso externo teve inclusão:<br><br><ul><li>S = Teve inclusão</li><li>N = Não teve inclusão</li></ul> |
| sin_processo | Variável categórica que indica se o acesso externo concede acesso ao processo:<br><br><ul><li>S = Concede acesso ao processo</li><li>N = Não concede acesso ao processo</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo de Acesso Externo:<br><br><ul><li>I = Interessado</li><li>E = Usuário externo</li><li>D = Destinatário isolado</li><li>S = Sistema</li><li>A = Assinatura externa</li></ul> |

## acesso_federacao

Armazena as informações de acesso ocorridas entre órgãos por meio do SEI Federação.

| Coluna | Descrição |
|---|---|
| id_acesso_federacao | Número ID que identifica o acesso realizado no Sei Federação |
| dth_cancelamento | Data de cancelamento do acesso no Sei Federação |
| dth_liberacao | Data do envio do link de acesso ao órgão destino no Sei Federação |
| id_documento_federacao | Número ID que identifica o número do documento envolvido na ação. Equivale à coluna id_protocolo_federação da Tabela protocolo_federacao. |
| id_instalacao_federacao_dest | Número ID que identifica a instalação do órgão destinatário do acesso concedido no Sei Federação |
| id_instalacao_federacao_rem | Número ID que identifica a instalação do órgão remetente do acesso concedido no Sei Federação |
| id_orgao_federacao_dest | Número ID que identifica o órgão destinatário do acesso concedido no Sei Federação |
| id_orgao_federacao_rem | Número ID que identifica o órgão do órgão remetente do acesso concedido no Sei Federação |
| id_procedimento_federacao | Número ID que identifica o número do processo envolvido na ação. Equivale à coluna id_protocolo_federação da Tabela protocolo_federacao. |
| id_unidade_federacao_dest | Número ID que identifica a Unidade Interna do órgão destinatário do acesso concedido no Sei Federação |
| id_unidade_federacao_rem | Número ID que identifica a Unidade Interna do órgão remetente do acesso concedido no Sei Federação |
| id_usuario_federacao_dest | Número ID que identifica o usuário do órgão destinatário do acesso concedido no Sei Federação |
| id_usuario_federacao_rem | Número ID que identifica a usuário do órgão remetente do acesso concedido no Sei Federação |
| motivo_cancelamento | Justificativa do cancelamento do acesso, preenchida na tela de ação doSei Federação |
| motivo_liberacao | Justificativa do envio do acesso, preenchida na tela de envio do Sei Federação |
| sin_ativo | Variável categórica que indica se o acesso está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo de acesso no Sei Federação: 1= Processo enviado ao órgão |

## acompanhamento

Armazena as informações de acompanhamento de processos na Undiade.

| Coluna | Descrição |
|---|---|
| id_acompanhamento | Número ID que identifica o acompanhamento. |
| dth_alteracao | Registra o momento da última alteração feita em um acompanhamento . |
| id_grupo_acompanhamento | Número ID que identifica o grupo de acompanhamento. |
| id_protocolo | Número ID que identifica o protocolo relativo ao acompanhamento. |
| id_unidade | Número ID que identifica a unidade do acompanhamento. |
| id_usuario | Número ID que identifica o usuário gerador do acompanhamento. |
| idx_acompanhamento | Registro idx de indexação de informações e facilitação da pesquisa da tabela acompanhamento. Formado pelos campos número do processo, o texto da observação e a data da última alteração feita no acompanhamento. |
| observacao | Observação do acompanhamento. |
| tipo_visualizacao | Identifica o tipo de visualização do acompanhamento. Existem as seguintes opções:<br><br><ul><li>0 = Visualizado</li><li>1 = Não visualizado</li><li>2 = Atenção</li><li>4 = Remoção de Sobrestamento</li><li>8 = Publicado</li></ul> |

## andamento_instalacao

Armazena as informações sobre o andamento das instalações dos órgãos cadastrados no SEI Federação.

| Coluna | Descrição |
|---|---|
| id_andamento_instalacao | Número ID que identifica o andamento de instalação |
| dth_estado | Data correspondente ao momento do registro do estado |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão no Sei Federação |
| id_tarefa_instalacao | Número ID que identifica a tarefa associada à instalação no Sei Federação |
| id_unidade | Número ID que identifica a Unidade associada ao andamento da instalação |
| id_usuario | Número ID que identifica o Usuário associado ao andamento da instalação |
| sta_estado | Status multi-valorado que identifica o estado do andamento da instalação no Sei Federação:<br><br><ul><li>A = Em Análise</li><li>L = Liberada</li><li>B = Bloqueada</li></ul> |

## andamento_marcador

Armazena as informações da aplicação de Marcador sobre os processos.

| Coluna | Descrição |
|---|---|
| id_andamento_marcador | Número ID que identifica o Marcador aplicado |
| dth_execucao | Data/hora do Marcador aplicado |
| id_marcador | Número ID que identifica o Marcador aplicado |
| id_procedimento | Número ID que identifica o processo sobre o qual o Marcador foi aplicado |
| id_unidade | Número ID que identifica a unidade do Marcador aplicao |
| id_usuario | Número ID que identifica o usuário que aplicou o Marcador |
| sin_ativo | Variável categórica que indica se o Marcador está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_ultimo | Variável categórica que indica se o Marcador é o último aplicado sobre o processo:<br><br><ul><li>S = É o último aplicado sobre o processo</li><li>N = Não é o último aplicado sobre o processo</li></ul> |
| sta_operacao | Status multi-valorado que identifica o tipo de operação realizada com o marcador:<br><br><ul><li>A = Alteração do registro do Marcador em um processo</li><li>I = Inserção de um Marcador em um processo</li><li>R = Retirada de um Marcador em um processo</li></ul> |
| texto | Armazena o Texto escrito pelo usuário ao aplicar o Marcador sobre o processo |

## andamento_plano_trabalho

Registra o andamento de um plano de trabalho associado a um processo

| Coluna | Descrição |
|---|---|
| id_andamento_plano_trabalho | Número ID que identifica o andamento do plano de trabalho. |
| dth_execucao | Data/hora de execução do andamento do plano de trabalho. |
| id_plano_trabalho | Número ID que identifica o plano de trabalho. |
| id_procedimento | Número ID que identifica o processo ao qual o andamento do plano de trabalho está associado. |
| id_tarefa_plano_trabalho | Número ID que identifica a tarefa do plano de trabalho. |
| id_unidade_origem | Número ID que identifica a unidade de origem do andamento do plano de trabalho. |
| id_usuario_origem | Número ID que identifica o usuário de origem do andamento do plano de trabalho. |
| sta_situacao | Status multi-valorado que identifica a situação do andamento do plano de trabalho:<br><br><ul><li>1 = Em Andamento</li><li>2 = Pausado</li><li>3 = Finalizado</li><li>4 = Problema</li><li>5 = Não se Aplica</li><li>6 = Desconsiderado</li></ul> |

## andamento_situacao

Armazena as informações do andamentos das situações dos processos.

| Coluna | Descrição |
|---|---|
| id_andamento_situacao | Número ID que identifica o andamento da situação |
| dth_execucao | Data/hora de execução do andamento da situação |
| id_procedimento | Número ID que identifica o processo do andamento da situação, faz referência à tabela procedimento |
| id_situacao | Número ID que identifica a situação do andamento da situação, faz referência à tabela situação |
| id_unidade | Número ID que identifica a unidade do andamento da situação, faz referência à tabela unidade |
| id_usuario | Número ID que identifica o usuário de andamento da situação, faz referência à tabela usuário |
| sin_ultimo | Variável categórica que indica se o andamento da situação é o ultimo:<br><br><ul><li>S = O ultimo</li><li>N = Não o ultimo</li></ul> |

## anexo

Armazena dados sobre os arquivos carregados no sistema, salvos no Filesystem, especialmente dos Documentos Externos

| Coluna | Descrição |
|---|---|
| id_anexo | Número ID que identifica o anexo (documento externo) |
| dth_inclusao | Data/hora de inclusão do anexo (documento externo). |
| hash | Código do hash do anexo (documento externo). |
| id_base_conhecimento | Número ID que identifica a base de conhecimento do anexo (documento externo). |
| id_projeto | Número ID que identifica o projeto do anexo (documento externo). |
| id_protocolo | Número ID que identifica o protocolo relativo ao anexo (documento externo). |
| id_unidade | Número ID que identifica a unidade onde foi feita a inserção do documento externo. |
| id_usuario | Número ID que identifica o usuário que fez a inserção do documento externo. |
| nome | Armazena o nome do documento anexo (documento externo). |
| sin_ativo | Variável categórica que indica se o anexo (documento externo) está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tamanho | Tamanho do anexo (documento externo). |

## anotacao

Armazena as anotações sobre processo por cada unidade

| Coluna | Descrição |
|---|---|
| id_anotacao | Número ID que identifica a anotação. |
| descricao | Descrição textual da anotação. |
| dth_anotacao | Data/hora da anotação |
| id_protocolo | Número ID que identifica o protocolo da anotação. |
| id_unidade | Número ID que identifica a unidade onde foi inserisa a anotação. |
| id_usuario | Número ID que identifica o usuário que inseriou a anotação. |
| sin_prioridade | Variável categórica que indica se a anotação é prioritaria:<br><br><ul><li>S = Prioritaria</li><li>N = Não prioritaria</li></ul> |
| sta_anotacao | Status multi-valorado que identifica o Tipo de Anotação:<br><br><ul><li>U = Unidade</li><li>I = Individual</li></ul> |

## arquivamento

Armazena a referência de arquivamento da solicitação com a devida atividade de arquivamento

| Coluna | Descrição |
|---|---|
| id_atividade_arquivamento | Número ID que identifica a atividade de arquivamento. Este campo é preenchido apenas quando o campo sta_arquivamento for igual a 'A', ou 'D' |
| id_atividade_cancelamento | Número ID que identifica a atividade de cancelamento do arquivamento. Este campo é preenchido apenas quando o campo sta_arquivamento for igual a 'C' |
| id_atividade_desarquivamento | Número ID que identifica a atividade de desarquivamento. Este campo é preenchido apenas quando o campo sta_arquivamento for igual a 'D' |
| id_atividade_eliminacao | Número ID que identifica a atividade de eliminação. Este campo é preenchido apenas quando o campo sta_eliminacao for igual a 'E' |
| id_atividade_recebimento | Número ID que identifica a atividade de recebimento. Este campo é preenchido apenas quando o campo sta_arquivamento for igual a 'R' |
| id_atividade_solicitacao | Número ID que identifica a atividade de solicitação. Este campo é preenchido apenas quando o campo sta_arquivamento for igual a 'S' |
| id_localizador | Número ID que identifica o localizador do arquivamento |
| id_protocolo | Número ID que identifica o protocolo do arquivamento |
| sta_arquivamento | Status multi-valorado que identifica o tipo de arquivamento do protocolo:<br><br><ul><li>A = Arquivado</li><li>C = Cancelado</li><li>D = Desarquivado</li><li>N = Não Arquivado</li><li>R = Recebido</li><li>S = Solicitado Desarquivamento</li></ul> |
| sta_eliminacao | Status multi-valorado que identifica a situação de eliminação do arquivamento:<br><br><ul><li>N = Não Eliminado</li><li>P = Para Eliminação</li><li>E = Eliminado</li></ul> |

## arquivo_extensao

Administração dos tipo de extensão e do tamanho dos arquivos permitidos para armazenamento.

| Coluna | Descrição |
|---|---|
| id_arquivo_extensao | Número ID que identifica o arquivo de extensão. |
| descricao | Descrição do tipo de extensão do arquivo. |
| extensao | Tipo de extensão do arquivo. |
| sin_ativo | Variável categórica que indica se o aquivo de extensão está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_interface | Variável categórica que indica se a opção 'Interface' está habilitada:<br><br><ul><li>S = Habilitada</li><li>N = Não habilitada</li></ul> |
| sin_ouvidoria | Variável categórica que indica se a extensão de arquivo é permitida para anexos de solicitações de ouvidoria:<br><br><ul><li>S = Permitida para anexos de solicitações de ouvidoria</li><li>N = Não permitida para anexos de solicitações de ouvidoria</li></ul> |
| sin_servico | Variável categórica que indica se a opção 'Serviços' está habilitada:<br><br><ul><li>S = Habilitada</li><li>N = Não habilitada</li></ul> |
| sin_usuario_externo | Variável categórica que indica se a extensão de arquivo é permitida para envio por usuário externo:<br><br><ul><li>S = Permitida para envio por usuário externo</li><li>N = Não permitida para envio por usuário externo</li></ul> |
| tamanho_maximo | Armazena, quando informado, o tamanho máximo do tipo de extensao do arquivo |

## assinante

Administração das Assinaturas das Unidades com Cargo/Função correspondentes

| Coluna | Descrição |
|---|---|
| id_assinante | Número ID que identifica o assinante. |
| cargo_funcao | Descrição do cargo/função do assinante. |
| id_orgao | Id_orgão onde o cargo_funcao está disponível. |

## assinatura

Armazena as identificação do usuário signatário e demais informações sobre o documento assinado

| Coluna | Descrição |
|---|---|
| id_assinatura | Número ID que identifica a assinatura. |
| agrupador | Número ID que identifica o agrupador da assinatura. |
| cpf | Número do CPF do responsável pela assinatura. |
| id_atividade | Número ID que identifica a atividade. |
| id_documento | Número ID que identifica a assinatura do documento. |
| id_tarja_assinatura | Identificador da tarja da assinatura. Faz referência para a tabela tarja_assinatura |
| id_unidade | Número ID que identifica a assinatura da unidade. |
| id_usuario | Número ID que identifica a assinatura do usuário. |
| modulo_origem | Armazena o identificador do módulo de origem da assinatura. |
| nome | Armazena o nome da assinatura. |
| numero_serie_certificado | Número de serie do certificado da assinatura. Preenchida apenas quando o campo sta_forma_autenticacao for igual a 'C' |
| p7s_base64 | Criptografia do número de série da assinatura. Preenchida apenas quando o campo sta_forma_autenticacao for igual a 'C' |
| sin_ativo | Variável categórica que indica se a assinatura está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_forma_autenticacao | Status multi-valorado que identifica o Tipo de forma de autenticação:<br><br><ul><li>C = Certificado digital</li><li>S = Senha</li></ul> |
| tratamento | Descrição da forma de tratamento do responsável pela assinatura. |

## assunto

Administração das informações da tabela assunto arquivístico

| Coluna | Descrição |
|---|---|
| id_assunto | Identificador do assunto |
| codigo_estruturado | Número ID que identifica o código estruturado do assunto. |
| descricao | Descrição textual do assunto. |
| id_tabela_assuntos | Identificador da tabela de assuntos. Faz referência para a tabela tabela assuntos |
| idx_assunto | Registro idx de indexação de informações e facilitação da pesquisa da tabela assunto. Formado pelos campos id_assunto, codigo_estruturado, descricao e observação. |
| observacao | Observação do assunto. |
| prazo_corrente | Armazena o prazo corrente para o assunto |
| prazo_intermediario | Armazena o prazo intermediário pertinente ao assunto |
| sin_ativo | Variável categórica que indica se o assunto está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_estrutural | Variável categórica que indica se o assunto é estruturado:<br><br><ul><li>S = Estruturado</li><li>N = Não estruturado</li></ul> |
| sta_destinacao | Status multi-valorado que identifica a destinação do assunto:<br><br><ul><li>G = Guarda Permanente</li><li>E = Eliminação</li></ul> |

## assunto_proxy

Associa o assunto proxy ao id_assunto da tabela assuntos arquivísticos

| Coluna | Descrição |
|---|---|
| id_assunto_proxy | Número ID que identifica o assunto proxy |
| id_assunto | Número ID que identifica o assunto |

## atividade

Armazena as informações de Atividades, em que algumas serão utilizadas na montagem dos Andamentos dos Processos junto com o Atributo Andamento correspondente

| Coluna | Descrição |
|---|---|
| id_atividade | Número ID que identifica a atividade. |
| dta_prazo | Data do prazo da atividade. |
| dth_abertura | Data/hora da abertura da atividade. |
| dth_conclusao | Data/hora da conclusão da atividade. |
| id_protocolo | Número ID que identifica o protocolo da atividade. |
| id_tarefa | Número ID que identifica a tarefa da atividade. |
| id_unidade | Número ID que identifica a unidade da atividade. |
| id_unidade_origem | Número ID que identifica a unidade de origem da atividade. |
| id_usuario | Número ID que identifica o usuário da atividade. |
| id_usuario_atribuicao | Número ID que identifica o usuário de atribuição da atividade. |
| id_usuario_conclusao | Número ID que identifica o usuário de conclusão da atividade. |
| id_usuario_origem | Número ID que identifica o usuário de origem da atividade. |
| id_usuario_visualizacao | Número ID que identifica o usuário de visualização da atividade. |
| sin_inicial | Variável categórica que indica se é atividade inicial:<br><br><ul><li>S = Atividade inicial</li><li>N = Não é atividade inicial</li></ul> |
| tipo_visualizacao | Número ID que identifica o tipo de visualização da atividade:<br><br><ul><li>0 = Visualizado</li><li>1 = Não visualizado</li><li>2 = Atenção</li><li>4 = Remoção de Sobrestamento</li><li>8 = Publicado</li></ul> |

## atributo

Administração dos Formulários

| Coluna | Descrição |
|---|---|
| id_atributo | Número ID que identifica o atributo (campo) para um Tipo de Formulário na Administração. |
| decimais | Armazena as casas decimais para preenchimento sobre o atributo (campo). |
| id_tipo_formulario | Número ID que identifica o Tipo de Formulário associado com o atributo (campo) na Administração. |
| linhas | Armazena a quantidade de linhas para preenchimento sobre o atributo (campo). |
| mascara | Armazena o formato de apresentação do atributo (campo). Essa variável é preenchida apenas quando o campo sta_tipo estiver preenchido com o valor igual a "TEXTO_MASCARA" |
| nome | Armazena o nome interno do atributo (campo) na Administração. |
| ordem | Ordem de apresentação do atributo (campo) na visualização do documento Formulário na hora de sua geração no processo. |
| rotulo | Armazena o nome a ser apresentado como rótulo do atributo (campo) na tela de geração do documento. |
| sin_ativo | Variável categórica que indica se a opção 'Atributo' está habilitada:<br><br><ul><li>S = Habilitada</li><li>N = Não habilitada</li></ul> |
| sin_obrigatorio | Variável categórica que indica se o atributo é obrigatório:<br><br><ul><li>S = Obrigatório</li><li>N = Não obrigatório</li></ul><br>Este campo será marcado como não (N) quando o atributo sta-tipo estiver preenchido com o valor igual a 'INFORMACAO' |
| sta_tipo | Status multi-valorado que identifica o Tipo de atributo:<br><br>DATA = Campo de data<br>NUMERO_INTEIRO = Campo numérico inteiro<br>NUMERO_DECIMAL = Campo numérico decimal<br>TEXTO_SIMPLES = Campo de texto simples<br>TEXTO_MASCARA = Campo de texto com máscara<br>TEXTO_GRANDE = Campo de texto grande<br>LISTA = Campo de lista<br>DINHEIRO = Campo monetário<br>OPCOES = Campo de opções<br>SINALIZADOR = Campo sinalizador<br>INFORMACAO = Campo apenas informativo. |
| tamanho | Armazena o tamanho do campo para preenchimento |
| valor_maximo | Armazena o valor máximo para preenchimento dos campos |
| valor_minimo | Armazena o valor mínimo para preenchimento dos campos |
| valor_padrao | Armazena o valor padrão para preenchimento dos campos |

## atributo_andam_plano_trab

Armazena atributos complementares, em formato chave/valor, de um andamento de plano de trabalho

| Coluna | Descrição |
|---|---|
| id_atributo_andam_plano_trab | Número ID que identifica o atributo do andamento do plano de trabalho. |
| chave | Armazena a chave do atributo do andamento do plano de trabalho. |
| id_andamento_plano_trabalho | Número ID que identifica o andamento do plano de trabalho ao qual o atributo pertence. |
| id_origem | Armazena o identificador de origem do atributo do andamento do plano de trabalho. |
| valor | Armazena o valor do atributo do andamento do plano de trabalho. |

## atributo_andamento

Identifica os atributos (variáveis) a serem utilizados pelas Tarefas e Atividades na montagem dos Andamentos dos Processos

| Coluna | Descrição |
|---|---|
| id_atributo_andamento | Número ID que identifica o atributo em andamento. |
| id_atividade | Número ID que identifica o atributo de andamento da atividade. |
| id_origem | Número ID que identifica a origem do atributo em andamento. |
| nome | Armazena o nome do atributo em andamento |
| valor | Valor do atributo em andamento. |

## atributo_instalacao

Identifica os órgãos cadastrados no Sei federação

| Coluna | Descrição |
|---|---|
| id_atributo_instalacao | Número ID que identifica o atributo de instalação |
| id_andamento_instalacao | Número ID que identifica o andamento do atributo de instalação |
| id_origem | Número ID que identifica a origem do atributo de instalação. |
| nome | Nome genérico que identifica a instalação |
| valor | Nome que identifica a instalação |

## auditoria_protocolo

Armazena os registros de auditoria especificamente sobre os protocolos

| Coluna | Descrição |
|---|---|
| id_auditoria_protocolo | Número ID que identifica a auditoria de protocolo. |
| dta_auditoria | Data da alteração registrada na auditoria do protocolo. |
| id_anexo | Número ID que identifica um documento externo registrado na auditoria do protocolo. |
| id_protocolo | Número ID que identifica o protocolo de documento registrado na auditoria do protocolo. |
| id_usuario | Número ID que identifica o usuário que realizou alguma alteração em documento registrada na auditoria do protocolo. |
| versao | Número ID que identifica a versão do documento registrada na auditoria do protocolo. |

## avaliacao_documental

Registra a avaliação documental de processos quanto à destinação (guarda ou eliminação)

| Coluna | Descrição |
|---|---|
| id_avaliacao_documental | Número ID que identifica a avaliação documental. |
| dta_avaliacao | Data da avaliação documental. |
| id_assunto | Número ID que identifica o assunto original avaliado. |
| id_assunto_proxy | Número ID que identifica o assunto proxy avaliado. |
| id_procedimento | Número ID que identifica o processo avaliado. |
| id_unidade | Número ID que identifica a unidade que realizou a avaliação documental. |
| id_usuario | Número ID que identifica o usuário que realizou a avaliação documental. |
| sta_avaliacao | Status multi-valorado que identifica a situação da avaliação documental:<br><br><ul><li>A = Avaliado</li><li>R = Avaliação Revisada</li><li>P = Eliminação Parcial</li><li>E = Eliminado</li></ul> |

## aviso

Administração dos avisos exibidos aos usuários do sistema

| Coluna | Descrição |
|---|---|
| id_aviso | Número ID que identifica o aviso. |
| descricao | Armazena a descrição do aviso. |
| dth_fim | Data/hora de término da exibição do aviso. |
| dth_inicio | Data/hora de início da exibição do aviso. |
| imagem | Armazena a imagem do aviso. |
| link | Armazena o link associado ao aviso. |
| sin_liberado | Variável categórica que indica se o aviso está liberado:<br><br><ul><li>S = Liberado</li><li>N = Não liberado</li></ul> |
| sta_aviso | Status multi-valorado que identifica o formato de exibição do aviso:<br><br><ul><li>J = Janela</li><li>B = Banner</li></ul> |

## base_conhecimento

Armazena as Base de Conhecimento criadas para orientar instrução processual dos Tipos de Processos associados

| Coluna | Descrição |
|---|---|
| id_base_conhecimento | Número ID que identifica a base de conhecimento. |
| conteudo | Conteúdo da página da base de conhecimento. |
| descricao | Descrição da base de conhecimento. |
| dth_geracao | Data/hora da geração da base de conhecimento. |
| dth_liberacao | Data/hora da liberação da base de conhecimento. Será preenchido quando o campo sta_stado for 'L' ou 'V' |
| id_base_conhecimento_agrupador | Número ID que identifica o agrupador da base de conhecimento. |
| id_base_conhecimento_origem | Número ID que identifica a base de conhecimento origem. |
| id_conjunto_estilos | Número ID que identifica o conjunto de estilos da base de conhecimento. |
| id_documento_edoc | Número ID que identifica a base de conhecimento do documento edoc. |
| id_unidade | Número ID que identifica unidade que possui acesso à base de conhecimento. |
| id_usuario_gerador | Número ID que identifica o usuário gerador da base de conhecimento. |
| id_usuario_liberacao | Número ID que identifica o usuário de liberação da base de conhecimento. Será preenchido quando o campo sta_stado for 'L' ou 'V' |
| sta_documento | Status multi-valorado que identifica o a base de conhecimento:<br><br><ul><li>A = Formulário Automático</li><li>X = Externo</li><li>E = Editor EDOC</li><li>I = Editor Interno</li><li>F = Formulário Gerado'</li></ul> |
| sta_estado | Status multi-valorado que identifica o Tipo de Estado:<br><br><ul><li>V = Versão anterior</li><li>L = Liberado</li><li>R = Rascunho</li></ul> |

## base_conhecimento_idx

Registro de indexação da base de conhecimento para fins de pesquisa

| Coluna | Descrição |
|---|---|
| id_base_conhecimento | Número ID que identifica a base de conhecimento indexada. |
| id_anexo | Número ID que identifica o anexo da base de conhecimento indexado. |
| dth_indexacao | Data/hora de indexação do registro da base de conhecimento. |

## bloco

Armazena as informações referentes aos blocos criados

| Coluna | Descrição |
|---|---|
| id_bloco | Número ID que identifica o bloco. |
| descricao | Descrição do bloco. |
| id_unidade | Número ID que identifica a unidade do bloco. |
| id_usuario | Número ID que identifica o bloco de usuário. |
| idx_bloco | Registro idx de indexação de informações e facilitação da pesquisa da tabela bloco. Formado pelos campos id_bloco e descricao. |
| sta_estado | Status multi-valorado que identifica o Tipo de Estado do Bloco:<br><br><ul><li>A = Aberto</li><li>D = Disponibilizado</li><li>R = Retornado</li><li>C = Concluido</li></ul><br>Esta variável assumirá os valores de 'A' e 'C' apenas quando o campo sta_tipo for igual a 'I' |
| sta_tipo | Status multi-valorado que identifica o Tipo do Bloco:<br><br><ul><li>A = Assinatura</li><li>R = Reunião</li><li>I = Interno</li></ul> |

## campo_pesquisa

Armazena os atributos de pesquisas salvas

| Coluna | Descrição |
|---|---|
| id_campo_pesquisa | Tipo do Atributo:<br><br><ul><li>1 = Pesquisar: S - Documentos gerados</li><li>2 = Pesquisar: S - Documentos externos</li><li>3 = Com Tramitação na Unidade S</li><li>4 = ID do Orgão</li><li>5 = ID do Contato</li><li>6 = S - Interessado selecionado</li><li>7 = S - Remetente selecionado</li><li>8 = S - Destinatário selecionado</li><li>9 = Assinatura / Autenticação</li><li>10 = Especificação / Descrição</li><li>11 = Obs. desta Unidade</li><li>12 = Id do Assunto</li><li>13 = Unidade Geradora</li><li>14 = Número</li><li>15 = Tipo do Documento</li><li>16 = Nº SEI</li><li>17 = Nome na Árvore</li><li>18 = Data entre I= Data de Inclusão no SEI / G= Data do Processo/Documento</li><li>19 = Data entre (inicial)</li><li>20 = Data entre (final)</li><li>21 = Id usuário gerador</li><li>22 = Id usuário gerador</li><li>23 = Id usuário gerador</li><li>24 = Pesquisar D=Documento / P=Processo</li><li>25 = Texto para Pesquisa</li><li>26 = Tipo do Processo</li><li>27 = Usuário Gerador</li><li>28 = Usuário Gerador</li><li>29 = Usuário Gerador</li><li>30 = Assunto</li><li>31 = Unidade Geradora</li><li>32 = Assinatura / Autenticação</li><li>33 = Contato</li><li>34 = S - Restringir órgão</li></ul> |
| chave | Número de ID específico de cada atributo. |
| id_pesquisa | Número ID que identifica a pesquisa. Atributos da mesma pesquisa possui o mesmo id_pesquisa. |
| valor | Atributo usado na pesquisa. Cada linha corresponde a um atributo específico |

## cargo

Administração dos Cargos para uso nos Contatos

| Coluna | Descrição |
|---|---|
| id_cargo | Número ID que identifica o cargo. |
| expressao | Descrição da expressão do cargo. |
| id_titulo | Número ID que identifica o titulo. |
| id_tratamento | Número ID que identifica o tratamento do cargo:<br><br><ul><li>1, 3 e 5 = Os tratamentos de número 1, 3 e 5 são específicos do gênero masculino</li><li>2, 4 e 6 = enquanto que os tratamentos de número 2, 4 e 6 são específicos do gênero feminino</li></ul> |
| id_vocativo | Número ID que identifica o vocativo do cargo |
| sin_ativo | Variável categórica que indica se o cargo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_genero | Status multi-valorado que identifica o gênero do cargo:<br><br><ul><li>M = Masculino(a)</li><li>F = Feminino(a)</li></ul> |

## cargo_funcao

Funções exercidas para cada cargo

| Coluna | Descrição |
|---|---|
| id_cargo_funcao | Número ID que identifica o cargo/função. |
| id_unidade | Número ID que identifica a unidade do cargo. |
| nome | Armazena o nome do cargo/função. |
| sin_ativo | Variável categórica que indica se o cargo/função está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## categoria

Administração das Categorias para uso nos Contatos

| Coluna | Descrição |
|---|---|
| id_categoria | Número ID que identifica a categoria de um contato. |
| nome | Nome da categoria de um contato. |
| sin_ativo | Variável categórica que indica se a categoria está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## cidade

Administração das Cidades

| Coluna | Descrição |
|---|---|
| id_cidade | Número ID que identifica a cidade. |
| codigo_ibge | Número ID que identifica o código IBGE do municipio. |
| id_pais | Número ID que identifica a cidade do país. |
| id_uf | Número ID que identifica a uf. |
| latitude | Número ID que identifica a latitude da cidade. |
| longitude | Número ID que identifica a longitude da cidade. |
| nome | Armazena o nome da cidade |
| sin_capital | Variável categórica que indica se é cidade capital:<br><br><ul><li>S = Cidade capital</li><li>N = Não cidade capital</li></ul> |

## codigo_acesso

Administração dos códigos de acesso temporários enviados por e-mail para autenticação do usuário

| Coluna | Descrição |
|---|---|
| id_codigo_acesso | Número ID que identifica o código de acesso. |
| codigo | Armazena o código de acesso gerado. |
| dth_geracao | Data/hora de geração do código de acesso. |
| dth_utilizacao | Data/hora de utilização do código de acesso. |
| email | Armazena o e-mail para o qual o código de acesso foi enviado. |
| id_usuario | Número ID que identifica o usuário do código de acesso. |
| sin_ativo | Variável categórica que indica se o código de acesso está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## comentario

Armazena os atributos dos comentários inseridos nos processos e documentos

| Coluna | Descrição |
|---|---|
| id_comentario | Número ID que identifica o comentário. |
| descricao | Texto do comentário |
| dth_comentario | Data da inclusão do comentário |
| id_procedimento | Número ID que identifica do processo em que o comentário foi inserido |
| id_rel_protocolo_protocolo | Número ID que identifica do documento em que o comentário foi inserido. Fica Null se o comentário for inserido no processo. |
| id_unidade | Id da unidade onde o comentário foi inserido |
| id_usuario | Id do usuário que inseriou o comentário no processo |

## conjunto_estilos

Identifica a informação sobre o último estilo criado

| Coluna | Descrição |
|---|---|
| id_conjunto_estilos | Número ID que identifica o conjunto de estilos. |
| sin_ultimo | Variável categórica que indica se é o ultimo conjunto de estilos:<br><br><ul><li>S = O ultimo conjunto de estilos</li><li>N = Não o ultimo conjunto de estilos</li></ul> |

## conjunto_estilos_item

Administração dos conjuntos de estilos para uso no Editor

| Coluna | Descrição |
|---|---|
| id_conjunto_estilos_item | Número ID que identifica o item do conjunto de estilos. |
| formatacao | Padrão de formatação do conjunto de estilos do item. |
| id_conjunto_estilos | Número ID que identifica o item do conjunto de estilos. |
| nome | Armazena o nome do item do conjunto de estilos |

## contato

Armazena os dados dos Contatos, a serem usados como Interessado, Remetente ou Destinatário de protocolos ou associados a Órgãos, Unidades ou Usuários do sistema

| Coluna | Descrição |
|---|---|
| id_contato | Número ID que identifica o contato. |
| bairro | Bairro do contato. |
| cep | CEP do contato. |
| cnpj | Número do CNPJ do contato (caso seja pessoa jurídica). |
| complemento | Armazena os dados complementares do RG do contato |
| conjuge | Nome do Conjuge do Contato |
| cpf | Número do CPF do responsável pelo contato (caso seja pessoa física). |
| dta_nascimento | Data de nascimento do contato. |
| dth_cadastro | Data/hora de cadastro do contato. |
| email | E-mail do contato. |
| endereco | Endereço do contato. |
| funcao | Função do contato |
| id_cargo | Número ID que identifica o cargo do contato. |
| id_categoria | Número ID que identifica a categoria do contato. |
| id_cidade | Número ID que identifica a cidade do contato |
| id_contato_associado | Número ID que identifica o contato associado do contato |
| id_pais | Número ID que identifica o país do contato |
| id_pais_passaporte | Número ID que identifica o país de emissão do passaporte do contato. |
| id_tipo_contato | Número ID que identifica o tipo de contato |
| id_titulo | Número ID que identifica ao título do contato. |
| id_uf | Número ID que identifica a uf do contato |
| id_unidade_cadastro | Número ID que identifica a unidade de cadastro do contato. |
| id_usuario_cadastro | Número ID que identifica o usuário que cadastrou o contato. |
| idx_contato | Registro idx de indexação de informações e facilitação da pesquisa da tabela contato. Formado pelos campos sigla, nome, cpf ou cnpj (somente números) e cpf ou cnpj (formatado) |
| matricula | Armazena a matrícula do contato. |
| matricula_oab | Matrícula OAB do contato. |
| nome | Armazena o nome do contato (pode ser unidade ou usuário). |
| nome_registro_civil | Nome no Registro Civil do Contato |
| nome_social | Nome social do Contato |
| numero_passaporte | Número do passaporte do contato. |
| observacao | Observação do contato. |
| orgao_expedidor | Órgão expedidor do RG do contato. |
| rg | RG do contato. |
| sigla | Armazena a sigla do contato. |
| sin_ativo | Variável categórica que indica se o contato está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_endereco_associado | Variável categórica que indica se existe endereço associado:<br><br><ul><li>S = Existe endereço associado</li><li>N = Não existe endereço associado</li></ul> |
| sitio_internet | Endereço web do contato. |
| sta_genero | Status multi-valorado que identifica o gênero do contato:<br><br><ul><li>M = Masculino(a)</li><li>F = Feminino(a)</li></ul> |
| sta_natureza | Status multi-valorado que identifica a natureza do contato:<br><br><ul><li>F = Física</li><li>J = Jurídica</li></ul> |
| telefone_celular | Armazena o telefone celular do contato |
| telefone_comercial | Armazena o telefone comercial do contato, que antes no SEI 3.1 era 'telefone_fixo' |
| telefone_residencial | Armazena o telefone residencial do contato |

## controle_interno

Administração dos Controles Internos

| Coluna | Descrição |
|---|---|
| id_controle_interno | Número ID que identifica o controle interno. |
| descricao | Descrição do tipo do controle interno. |

## controle_prazo

Armazena os atributos dos controle de prazos usados nos processos

| Coluna | Descrição |
|---|---|
| id_controle_prazo | Número ID que identifica o Controle do prazo. |
| dta_conclusao | Data/hora da conclusão do Controle de prazo. |
| dta_prazo | Data/hora da inserção do Controle de prazo. |
| id_protocolo | Número do Protocolo em que o controle de prazo está associado |
| id_unidade | Id da unidade onde o controle de prazo foi inserido |
| id_usuario | Número ID que identifica o usuário o controle de prazo no processo |

## controle_unidade

Situação do controle da unidade de acordo com o procedimento da mesma

| Coluna | Descrição |
|---|---|
| id_controle_unidade | Número ID que identifica o controle da unidade. |
| dth_execucao | Data/hora de execução armazenada do controle da unidade. |
| dth_snapshot | Data/hora da snapshot do controle da unidade. |
| id_procedimento | Número ID que identifica o processo do controle da unidade. |
| id_situacao | Número ID que identifica a situação do controle da unidade. |
| id_usuario | Número ID que identifica o usuário do controle da unidade. |

## documento

Armazena as informações complementares sobre os Documentos

| Coluna | Descrição |
|---|---|
| id_documento | Número ID que identifica o documento. |
| din_valor | Armazena o valor monetário associado ao documento. |
| id_conjunto_estilos | Número ID que identifica o conjunto de estilos do documento. Esta variável será preenchida apenas quando o tipo de documento for igual a 'I' e 'A' |
| id_documento_edoc | Número ID que identifica o documento edoc. |
| id_procedimento | Número ID que identifica o Processo no qual o Documento está inserido |
| id_serie | Número ID que identifica o Tipo de Documento do Documento |
| id_tipo_conferencia | Número ID que identifica o tipo de conferencia do documento. Esta variável será preenchida apenas quando o tipo de documento for igual a 'X' |
| id_tipo_formulario | Número ID que identifica o formulário usado no documento |
| id_unidade_responsavel | Número ID que identifica a unidade responsável. |
| nome_arvore | Armazena o complemento informado do nome do documento |
| numero | Armazena os dados alfanuméricos da numeração do documento |
| sin_arquivamento | Variável categórica que indica se o documento externo é destinado para arquivamento:<br><br><ul><li>S = Destinado para arquivamento</li><li>N = Não destinado para arquivamento</li></ul> |
| sin_bloqueado | Variável categórica que indica se o documento está bloqueado:<br><br><ul><li>S = Bloqueado</li><li>N = Não bloqueado</li></ul> |
| sin_versoes | Variável categórica que indica se o documento possui versões:<br><br><ul><li>S = Possui versões</li><li>N = Não possui versões</li></ul> |
| sta_documento | Status multi-valorado que identifica o tipo do documento:<br><br><ul><li>A = Formulário Automático</li><li>X = Externo</li><li>I = Editor Interno</li><li>F = Formulário Gerado</li></ul> |
| sta_editor | Status multi-valorado que identifica o editor utilizado na criação do documento:<br><br>0 = Nenhum editor visual<br>1 = CKEditor 4<br>2 = CKEditor 5. |

## documento_conteudo

Armazena as informações do Conteúdo dos Documentos Gerados

| Coluna | Descrição |
|---|---|
| conteudo | Armazena o conteúdo do documento conteúdo |
| conteudo_assinatura | Armazena o conteúdo da assinatura digital do documento conteúdo |
| crc_assinatura | Armazena o conteúdo da crc assinatura do documento conteúdo. OBS: A verificação cíclica de redundância (do inglês, CRC - Cyclic Redundancy Check) é um método de detecção de erros normalmente usada em redes digitais e dispositivos de armazenamento para detectar mudança acidental em cadeias de dados. |
| id_documento | Número ID que identifica o documento od documento conteúdo. |
| qr_code_assinatura | Armazena a sequência alfanumérica do qr_code do documento conteúdo. |

## documento_geracao

Relaciona o documento gerado ao modelo e ao texto padrão interno utilizados em sua geração

| Coluna | Descrição |
|---|---|
| id_documento | Número ID que identifica o documento gerado. |
| id_documento_modelo | Número ID que identifica o documento utilizado como modelo na geração. |
| id_texto_padrao_interno | Número ID que identifica o texto padrão interno utilizado na geração do documento. |

## dominio

Referencia os atributos de acordo com seus domínios

| Coluna | Descrição |
|---|---|
| id_dominio | Número ID que identifica o domínio. |
| id_atributo | Número ID que identifica o atributo do dominio. |
| ordem | Armazena a ordem de apresentação do domínio. |
| rotulo | Armazena o rótulo do label para o domínio. |
| sin_ativo | Variável categórica que indica se o domínio está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_padrao | Variável categórica que indica se o domínio é padrão:<br><br><ul><li>S = Padrão</li><li>N = Não padrão</li></ul> |
| valor | Valor do dominio. |

## edital_eliminacao

Administração dos editais de eliminação de documentos

| Coluna | Descrição |
|---|---|
| id_edital_eliminacao | Número ID que identifica o edital de eliminação. |
| dta_publicacao | Data de publicação do edital de eliminação. |
| especificacao | Armazena a especificação do edital de eliminação. |
| id_documento | Número ID que identifica o documento do edital de eliminação. |
| id_procedimento | Número ID que identifica o processo do edital de eliminação. |
| id_unidade | Número ID que identifica a unidade responsável pelo edital de eliminação. |
| sta_edital_eliminacao | Status multi-valorado que identifica a situação do edital de eliminação:<br><br><ul><li>C = Cadastrado</li><li>M = Montando Edital</li><li>G = Gerado</li><li>B = Publicado</li><li>P = Eliminação Parcial</li><li>E = Eliminado</li></ul> |

## edital_eliminacao_conteudo

Relaciona as avaliações documentais que compõem o conteúdo de um edital de eliminação

| Coluna | Descrição |
|---|---|
| id_edital_eliminacao_conteudo | Número ID que identifica o conteúdo do edital de eliminação. |
| dth_inclusao | Data/hora de inclusão do conteúdo no edital de eliminação. |
| id_avaliacao_documental | Número ID que identifica a avaliação documental incluída no edital de eliminação. |
| id_edital_eliminacao | Número ID que identifica o edital de eliminação. |
| id_usuario_inclusao | Número ID que identifica o usuário que incluiu o conteúdo no edital de eliminação. |

## edital_eliminacao_erro

Registra os erros ocorridos no processamento de um conteúdo de edital de eliminação

| Coluna | Descrição |
|---|---|
| id_edital_eliminacao_erro | Número ID que identifica o erro do edital de eliminação. |
| dth_erro | Data/hora de ocorrência do erro do edital de eliminação. |
| id_edital_eliminacao_conteudo | Número ID que identifica o conteúdo do edital de eliminação em que ocorreu o erro. |
| texto_erro | Armazena o texto do erro ocorrido no processamento do edital de eliminação. |

## email_grupo_email

Armaneza as informações contidas em grupos de e-mail

| Coluna | Descrição |
|---|---|
| id_email_grupo_email | Número ID que identifica o e-mail do grupo e-mail. |
| descricao | Nome do usuário do e-mail contido no grupo. |
| email | E-mail do usuário contido no grupo de e-mail. |
| id_grupo_email | Número ID que identifica o grupo e-mail. |
| idx_email_grupo_email | Registro idx de indexação de informações e facilitação da pesquisa da tabela email_grupo_email. Formado pelos campos email e descrição. |

## email_sistema

Administração dos E-mails do Sistema

| Coluna | Descrição |
|---|---|
| id_email_sistema | Número ID que identifica o e-mail do sistema. |
| assunto | Descrição do assunto do e-mail do sistema. |
| conteudo | Descrição do conteúdo do e-mail do sistema. |
| de | Armazena o e-mail de origem do email do sistema |
| descricao | Descrição do tipo de e-mail de sistema. |
| id_email_sistema_modulo | Número ID que identifica o módulo do e-mail do sistema. Esta variável será preenchida apenas quando o tipo de email do sistema for igual a peticionamento |
| para | Armazena o e-mail de destino do email do sistema |
| sin_ativo | Variável categórica que indica se o e-mail do sistema está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## email_unidade

Armazena as parametrizações pela Administração dos Emails das Unidades

| Coluna | Descrição |
|---|---|
| id_email_unidade | Número ID que identifica o e-mail da unidade. |
| descricao | Descrição do e-mail da unidade. |
| email | E-mail da unidade |
| id_unidade | Número ID que identifica a unidade do e-mail. |
| sequencia | Armazena a ordem de apresentação do e-mail da unidade. |

## email_utilizado

Armazena os emails utilizados

| Coluna | Descrição |
|---|---|
| id_email_utilizado | Número ID que identifica o e-mail utilizado. |
| email | E-mail utilizado. |
| id_unidade | Número ID que identifica a unidade do e-mail utilizado. |

## estatisticas

Armazena as estatísticas de acesso dos usuários para cada documento

| Coluna | Descrição |
|---|---|
| id_estatisticas | Número ID que identifica a estatísticas |
| ano | Número ID que identifica o ano da estatistica. |
| dth_abertura | Data/hora da abertura |
| dth_conclusao | Data/hora da conclusão |
| dth_snapshot | Data/hora da snapshot |
| id_documento | Número ID que identifica o documento. |
| id_procedimento | Número ID que identifica o processo. |
| id_tipo_procedimento | Número ID que identifica o tipo de procedimento. |
| id_unidade | Número ID que identifica a unidade. |
| id_usuario | Número ID que identifica o usuário. |
| mes | Número ID que identifica o mês da estatistica. |
| quantidade | Número ID que identifica a quantidade de estatistica. |
| tempo_aberto | Número ID que identifica o tempo aberto da estatistica. |

## estilo

Administração dos paramentros dos Estilos do Editor HTML

| Coluna | Descrição |
|---|---|
| id_estilo | Número ID que identifica o estilo. |
| formatacao | Padrão de formatação do estilo. |
| nome | Armazena o nome do estilo |

## etapa_trabalho

Administração das etapas que compõem um plano de trabalho

| Coluna | Descrição |
|---|---|
| id_etapa_trabalho | Número ID que identifica a etapa de trabalho. |
| descricao | Armazena a descrição da etapa de trabalho. |
| id_plano_trabalho | Número ID que identifica o plano de trabalho ao qual a etapa pertence. |
| nome | Armazena o nome da etapa de trabalho. |
| ordem | Armazena a ordem de apresentação da etapa de trabalho dentro do plano de trabalho. |
| sin_ativo | Variável categórica que indica se a etapa de trabalho está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## feed

Armazena o conteúdo do Feed de notícias

| Coluna | Descrição |
|---|---|
| id_feed | Número ID que identifica o feed. |
| conteudo | Armazena o conteúdo do feed |

## feriado

Administração das parametrizações dos Feriados por Ano

| Coluna | Descrição |
|---|---|
| id_feriado | Número ID que identifica o feriado. |
| descricao | Descrição do feriado. |
| dta_feriado | Data de feriado. |
| id_orgao | Número ID que identifica o órgão. |

## grupo_acompanhamento

Armazena informações sobre os agrupamentos de acompanhamento especial

| Coluna | Descrição |
|---|---|
| id_grupo_acompanhamento | Número ID que identifica o grupo de acompanhamento. |
| id_unidade | Número ID que identifica a unidade do grupo de acompanhamento. |
| nome | Armazena o nome do grupo de acompanhamento. |

## grupo_bloco

Armazena os atributos dos grupos de blocos

| Coluna | Descrição |
|---|---|
| id_grupo_bloco | Número ID que identifica o formulário usado no documento |
| id_unidade | Número ID que identifica a unidade do grupo do bloco. |
| nome | Armazena o nome do grupo do bloco |
| sin_ativo | Variável categórica que indica se o grupo do bloco está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## grupo_contato

Armazena as informações dos grupos institucionais de contato

| Coluna | Descrição |
|---|---|
| id_grupo_contato | Número ID que identifica o grupo de contato. |
| descricao | Descrição do grupo de contato. |
| id_unidade | Número ID que identifica a unidade do grupo de contato. |
| nome | Armazena o nome do grupo de contato |
| sin_ativo | Variável categórica que indica se o grupo de contato está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo do grupo de contato:<br><br><ul><li>I = Institucional</li><li>U = Unidade</li></ul> |

## grupo_email

Armazena as informações dos grupos institucionais de e-mail

| Coluna | Descrição |
|---|---|
| id_grupo_email | Número ID que identifica o grupo de e-mail. |
| descricao | Descrição do grupo de e-mail. |
| id_unidade | Número ID que identifica a unidade do grupo de e-mail. |
| nome | Armazena o nome do grupo de e-mail |
| sin_ativo | Variável categórica que indica se o grupo do e-mail está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo:<br><br><ul><li>I = Institucional</li><li>U = Unidade</li></ul> |

## grupo_federacao

Armazena as informações dos grupos de órgãos criados no Sei Federação

| Coluna | Descrição |
|---|---|
| id_grupo_federacao | Número ID que identifica o grupo criado no Sei Federação |
| descricao | Descrição do grupo no Sei Federação |
| id_unidade | Número ID que identifica a Unidade Interna do órgão integrante de grupo no Sei Federação |
| nome | Nome que identifica o grupo no Sei Federação |
| sin_ativo | Variável categórica que indica se o grupo está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo do grupo no Sei Federação:<br><br><ul><li>I = Institucional</li><li>U = Unidade</li></ul> |

## grupo_protocolo_modelo

Armazena as informações dos grupos de documentos modelos e processos marcados nos favoritos

| Coluna | Descrição |
|---|---|
| id_grupo_protocolo_modelo | Número ID que identifica o grupo de protocolo modelo. |
| id_unidade | Número ID que identifica a unidade do grupo de protocolo modelo. |
| nome | Armazena o nome do protocolo modelo |

## grupo_serie

Administração das parametrizações dos Grupos de Tipos de Documentos

| Coluna | Descrição |
|---|---|
| id_grupo_serie | Número ID que identifica o grupo de serie. |
| descricao | Descrição do grupo de serie. |
| nome | Armazena o nome do grupo de serie |
| sin_ativo | Variável categórica que indica se o grupo de serie está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## grupo_unidade

Armazena as informações dos grupos institucionais de envio dos processos

| Coluna | Descrição |
|---|---|
| id_grupo_unidade | Número ID que identifica o grupo de unidade. |
| descricao | Descrição do grupo de unidade. |
| id_unidade | Número ID que identifica a unidade do grupo. |
| nome | Armazena o nome do grupo de unidade |
| sin_ativo | Variável categórica que indica se o grupo de unidade está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo:<br><br><ul><li>I = Institucional</li><li>U = Unidade</li></ul> |

## hipotese_legal

Administração das parametrizações das hipóteses legais

| Coluna | Descrição |
|---|---|
| id_hipotese_legal | Número ID que identifica a hipótese legal. |
| base_legal | Armazena a base legal da hipótese legal |
| descricao | Armazena a descrição textual da hipótese legal |
| nome | Armazena o nome da hipótese legal |
| sin_ativo | Variável categórica que indica se o hipótese legal está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_nivel_acesso | Status multi-valorado que identifica o Tipo de nível de acesso:<br><br><ul><li>0 = Público</li><li>1 = Restrito</li><li>2 = Sigiloso</li></ul> |

## imagem_formato

Administração dos tipo de formato permitidos de imagens

| Coluna | Descrição |
|---|---|
| id_imagem_formato | Número ID que identifica a imagem formato. |
| descricao | Descrição do tipo de extensão do arquivo imagem formato. |
| formato | Tipo de extensão do arquivo de imagem formato. |
| sin_ativo | Variável categórica que indica se a imagem formato está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## infra_agendamento_tarefa

Administração dos Agendamentos periódicos do Sistema

| Coluna | Descrição |
|---|---|
| id_infra_agendamento_tarefa | Número ID que identifica o agendamento de tarefa de infraestrutura. |
| comando | Descrição do comando da tarefa agendada de infraestrutura. |
| descricao | Descrição da tarefa agendada de infraestrutura. |
| dth_ultima_conclusao | Data/hora da ultima conclusão da tarefa agendada de infraestrutura. |
| dth_ultima_execucao | Data/hora da ultima execução da tarefa agendada de infraestrutura. |
| email_erro | E-mail cadastrado para envio em caso de erro na execução da tarefa agendada |
| parametro | Parametro da tarefa agendada de infraestrutura. |
| periodicidade_complemento | Complemento da periodicidade da tarefa agendada de infraestrutura. |
| sin_ativo | Variável categórica que indica se a infraestrutura de agendamento tarefa está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_sucesso | Variável categórica que indica o sucesso da execução da tarefa agendada de infraestrutura:<br><br><ul><li>S = Sucesso</li><li>N = Insucesso</li></ul> |
| sta_periodicidade_execucao | Status multi-valorado que identifica o tipo de periodicidade de execução:<br><br><ul><li>N = Minuto</li><li>D = Hora</li><li>S = Dia da Semana</li><li>M = Dia do Mês</li><li>A = Dia do Ano</li></ul> |

## infra_auditoria

Auditoria da infraestrutura

| Coluna | Descrição |
|---|---|
| id_infra_auditoria | Número ID que identifica a infraestrutura de auditoria. |
| descricao_unidade | Descrição da unidade executora da ação registrada na auditoria de infraestrutura. |
| dth_acesso | Data/hora de acesso da ação registrada na auditoria de infraestrutura. |
| id_orgao_unidade | Número ID que identifica o órgão de unidade executora da ação registrada na auditoria de infraestrutura. |
| id_orgao_usuario | Número ID que identifica o órgão do usuário executor da ação registrado na auditoria de infraestrutura.. |
| id_orgao_usuario_emulador | Número ID que identifica o órgão de usuário do emulador registrado na auditoria de infraestrutura. |
| id_unidade | Número ID que identifica a unidade executora da ação registrada na auditoria de infraestrutura. |
| id_usuario | Número ID que identifica o usuário executor da ação registrado na de auditoria de infraestrutura. |
| id_usuario_emulador | Número ID que identifica o usuário do emulador da auditoria de infraestrutura.. |
| ip | Endereço do IP executor da ação registrado na auditoria de infraestrutura. |
| nome_usuario | Armazena o nome do usuário executor da ação registrado na auditoria de infraestrutura.. |
| nome_usuario_emulador | Armazena o nome do usuário emulador registrado na auditoria de infraestrutura. |
| operacao | Descrição da operação execuda registrada na auditoria de infraestrutura. |
| recurso | Descrição do recurso registrado na auditoria de infraestrutura. |
| requisicao | Descrição da requição de auditoria de infraestrutura. |
| servidor | Armazena o nome e IP do servidor de auditoria de infraestrutura. |
| sigla_orgao_unidade | Armazena a sigla do órgão da unidade executora da ação registrado na auditoria de infraestrutura. |
| sigla_orgao_usuario | Armazena a sigla do órgão usuário executor da ação registrada na auditoria de infraestrutura.. |
| sigla_orgao_usuario_emulador | Armazena a sigla do órgão usuário emulador registrado na auditoria de infraestrutura. |
| sigla_unidade | Armazena a sigla da unidade executora da ação registrada na auditoria de infraestrutura. |
| sigla_usuario | Armazena a sigla do usuário executor da ação registrado na auditoria de infraestrutura. |
| sigla_usuario_emulador | Armazena a sigla do usuário emulador registrado na auditoria de infraestrutura. |
| user_agent | Descrição do user-agent de auditoria de infraestrutura. |

## infra_captcha

Controle de tentativas de resolução de captcha da infraestrutura, usado no bloqueio por excesso de erros

| Coluna | Descrição |
|---|---|
| acertos | Armazena a quantidade de acertos na resolução do captcha. |
| ano | Armazena o ano de referência do controle de captcha. |
| dia | Armazena o dia de referência do controle de captcha. |
| erros | Armazena a quantidade de erros na resolução do captcha. |
| identificacao | Armazena a identificação (sessão ou origem) do controle de captcha. |
| mes | Armazena o mês de referência do controle de captcha. |

## infra_dado_usuario

Auditoria da infraestrutura dos dados de usuário

| Coluna | Descrição |
|---|---|
| id_usuario | Número ID que identifica usuário de dados de infraestrutura. |
| nome | Armazena o nome do usuário de dados de infraestrutura. |
| valor | Valor da infraestrutura de dados do usuário. |

## infra_editor_comentario

Armazena os comentários inseridos no editor de texto interno sobre um documento

| Coluna | Descrição |
|---|---|
| id_infra_editor_comentario | Número ID que identifica o comentário do editor interno. |
| cor_comentario | Armazena a cor de destaque do comentário do editor interno. |
| dth_atualizacao | Data/hora de atualização do comentário do editor interno. |
| dth_cadastro | Data/hora de cadastro do comentário do editor interno. |
| fim_deslocamento | Armazena a posição final de deslocamento do trecho comentado no editor interno. |
| fim_posicao | Armazena a posição final do trecho comentado no editor interno. |
| hash_conteudo | Armazena o hash do conteúdo do documento no momento do comentário do editor interno. |
| id_documento_origem | Armazena o identificador do documento de origem do comentário do editor interno. |
| id_unidade_origem | Armazena o identificador da unidade de origem do comentário do editor interno. |
| id_usuario_origem | Armazena o identificador do usuário de origem do comentário do editor interno. |
| inicio_deslocamento | Armazena a posição inicial de deslocamento do trecho comentado no editor interno. |
| inicio_posicao | Armazena a posição inicial do trecho comentado no editor interno. |
| sin_ativo | Variável categórica que indica se o comentário do editor interno está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_acesso | Status multi-valorado que identifica o nível de acesso do comentário do editor interno:<br><br>0 = Público<br>1 = Unidade<br>2 = Privado<br>3 = Tramitação. |
| texto | Armazena o texto do comentário do editor interno. |

## infra_erro_php

Registro dos erros PHP ocorridos na infraestrutura do sistema

| Coluna | Descrição |
|---|---|
| id_infra_erro_php | Número ID que identifica o erro PHP registrado. |
| arquivo | Armazena o caminho do arquivo PHP em que ocorreu o erro. |
| dth_cadastro | Data/hora de cadastro do erro PHP. |
| erro | Armazena a mensagem do erro PHP. |
| linha | Armazena o número da linha do arquivo PHP em que ocorreu o erro. |
| quantidade | Armazena a quantidade de ocorrências do erro PHP registrado. |
| sta_tipo | Status multi-valorado que identifica o tipo do erro PHP registrado:<br><br>1 = Undefined array key<br>2 = Undefined variable<br>3 = Undefined property<br>4 = Attempt to read property<br>5 = Trying to access array offset<br>6 = Array to string conversion<br>7 = Resource used as offset casting to integer<br>8 = String offset cast occurred<br>9 = Uninitialized string offset<br>10 = Cannot access offset of type string on string<br>11 = Argument must be passed by reference<br>12 = A non numeric value encountered. |

## infra_log

Registros dos logs de Erro, Aviso, Informação e Debug das operações do SEI

| Coluna | Descrição |
|---|---|
| id_infra_log | Número ID que identifica a log de infraestrutura. |
| dth_log | Data/hora de log de infraestrutura. |
| ip | Endereço do IP de log de infraestrutura. Foi identificado que esta informação estará nula apenas quando a variável sta_tipo for igual a 'I' (Informação) |
| sta_tipo | Status multi-valorado que identifica o Tipo de log:<br><br><ul><li>I = Informação</li><li>E = Erro</li><li>A = Aviso</li><li>D = Debug</li></ul> |
| texto_log | Texto do log de Erro, Aviso, Informação e Debug das operações do SEI |

## infra_navegador

Armazena o log de infraestrutura dos navegadores utilizados no acesso

| Coluna | Descrição |
|---|---|
| id_infra_navegador | Número ID que identifica os dados do navegador de internet utilizado para acessar o SEI. |
| dth_acesso | Data/hora de acesso do navegador registrado nos dados de infraestrutura. |
| identificacao | Descrição do tipo de navegador utilizado no acesso. |
| ip | Endereço do IP do navegador utilizado no acesso. |
| user_agent | Descrição do user-agent do navegador |
| versao | Descrição da versão do navegador utilizado no acesso |

## infra_parametro

Administração dos Parâmetros do Sistema

| Coluna | Descrição |
|---|---|
| nome | Armazena o nome do parametro de infraestrutura. |
| valor | Valor do parametro de infraestrutura. |

## infra_regra_auditoria

Armazena as parametrizações replicadas do SIP sobre as Regras de Auditoria

| Coluna | Descrição |
|---|---|
| id_infra_regra_auditoria | Número ID que identifica a infraestrutura das regras da auditoria. |
| descricao | Descrição da regra de auditoria de infraestrutura. |
| sin_ativo | Variável categórica que indica se a regra de auditoria da infraestrutura está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## infra_regra_auditoria_recurso

Armazena as parametrizações replicadas do SIP sobre o relacionamento dos Recursos com as Regras de Auditoria

| Coluna | Descrição |
|---|---|
| id_infra_regra_auditoria | Número ID que identifica a infraestrutura de regra da auditoria:<br><br><ul><li>2 = quando houver classificação de tratamentos dos objetos persistidos no sistema.</li><li>3 = quando houver classificação referente a consulta externa ou tratamento de usuário externo</li><li>4 = Procedimentos de visualização</li><li>5 = Download e/ou visualização de documentos</li><li>6 = Parametrização de recursos do tipo 'md_pet'</li><li>7 = Parametrização de recursos do tipo 'md_pesq'</li><li>8 = Parametrização de recursos do tipo 'md_ri'</li></ul> |
| recurso | Descrição do recurso da regra de auditoria de infraestrutura. |

## infra_sequencia

Armazena a infraestrutura da sequencia de agendamento das tarefas

| Coluna | Descrição |
|---|---|
| nome_tabela | Armazena o nome da tabela de infraestrutura de sequecia. |
| num_atual | Número ID que identica a numeração atual da infraestrutura de sequencia. |
| num_maximo | Número ID que identifica a numeração máxima da sequencia. |
| qtd_incremento | Número ID que identifica a quantidade de incremento da sequencia. |

## instalacao_federacao

Armazena as informações das instalações dos órgãos cadastrados no Sei Federação

| Coluna | Descrição |
|---|---|
| id_instalacao_federacao | Número ID que identifica a instalação do órgão no Sei Federação |
| chave_privada | Chave privada de acesso que decodifica as informações recebidas das instalações do Sei integradas no Sei Federação |
| chave_publica_local | Chave pública de acesso que codifica as informações transmitidas para as instalações do Sei integradas no Sei Federação |
| chave_publica_remota | Chave pública de acesso remoto, localizada em um servidor, que codifica as informações transmitidas para as instalações do Sei integradas no Sei Federação |
| cnpj | CNPJ do órgão correspondente da instalação |
| descricao | Descrição do órgão correspondente da instalação |
| endereco | Endereço do órgão correspondente da instalação |
| sigla | Sigla do órgão correspondente da instalação |
| sin_ativo | Variável categórica que indica se a instalação está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sta_agendamento | Status multi-valorado que identifica a situação do agendamento da instalação no Sei Federação:<br><br><ul><li>N = Nenhum agendamento</li><li>L = E-mail enviado</li><li>I = Ignorado</li></ul> |
| sta_estado | Status multi-valorado que identifica o estado da instalação no Sei Federação:<br><br><ul><li>A = Em análise</li><li>L = Liberada</li><li>B = Bloqueada</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo de instalação no Sei Federação:<br><br><ul><li>L = Local</li><li>E = Enviada</li><li>R = Recebida</li><li>P = Replicada</li></ul> |

## item_etapa

Administração dos itens que compõem uma etapa de trabalho

| Coluna | Descrição |
|---|---|
| id_item_etapa | Número ID que identifica o item de etapa. |
| descricao | Armazena a descrição do item de etapa. |
| id_etapa_trabalho | Número ID que identifica a etapa de trabalho à qual o item pertence. |
| nome | Armazena o nome do item de etapa. |
| ordem | Armazena a ordem de apresentação do item dentro da etapa de trabalho. |
| sin_ativo | Variável categórica que indica se o item de etapa está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## lembrete

Tabela vazia - Não utilizada pelo SEI

| Coluna | Descrição |
|---|---|
| id_lembrete | Número ID que identifica o lembrete. - Tabela vazia - Não utilizada pelo SEI |
| altura | Indicação do tamanho da altura do bloco de lembrete - Tabela vazia - Não utilizada pelo SEI |
| conteudo | Conteúdo do bloco de lembrete - Tabela vazia - Não utilizada pelo SEI |
| cor | Indicação do tamanho da altura do bloco de lembrete - Tabela vazia - Não utilizada pelo SEI |
| cor_texto | Indicação da cor do usado no bloco de lembrete - Tabela vazia - Não utilizada pelo SEI |
| dth_lembrete | Data/hora da geração do lembrete - Tabela vazia - Não utilizada pelo SEI - Tabela vazia - Não utilizada pelo SEI |
| id_usuario | Número ID que identifica o usuário - Tabela vazia - Não utilizada pelo SEI |
| largura | Indicação do tamanho da largura do bloco de lembrete - Tabela vazia - Não utilizada pelo SEI |
| posicao_x | Indicação da posição na tela no eixo x do bloco de lembrete - Tabela vazia - Não utilizada pelo SEI |
| posicao_y | Indicação da posição na tela no eixo y do bloco de lembrete - Tabela vazia - Não utilizada pelo SEI |
| sin_ativo | Variável categórica que indica se o lembrete está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul><br>- Tabela vazia - Não utilizada pelo SEI |

## lixeira

Armazena os processos, documentos e anexos excluídos e enviados para a lixeira

| Coluna | Descrição |
|---|---|
| id_lixeira | Número ID que identifica o item da lixeira. |
| conteudo | Armazena o conteúdo do item excluído para fins de exibição na lixeira. |
| dth_lixeira | Data/hora de envio do item para a lixeira. |
| id_anexo | Número ID que identifica o anexo excluído. |
| id_documento | Número ID que identifica o documento excluído. |
| id_procedimento | Número ID que identifica o processo excluído. |
| id_unidade | Número ID que identifica a unidade em que ocorreu a exclusão. |
| id_usuario | Número ID que identifica o usuário que realizou a exclusão. |
| nome_arvore | Armazena o complemento do nome do documento excluído. |
| nome_serie | Armazena o nome do tipo de documento (série) do item excluído. |
| numero | Armazena os dados alfanuméricos da numeração do item excluído. |
| protocolo_documento | Armazena o protocolo formatado do documento excluído. |
| protocolo_processo | Armazena o protocolo formatado do processo excluído. |
| sta_lixeira | Status multi-valorado que identifica a situação do item na lixeira:<br><br><ul><li>E = Excluído</li><li>C = Cancelado</li></ul> |
| sta_nivel_acesso_global | Status multi-valorado que identifica o nível de acesso global do item excluído:<br><br>0 = Público<br>1 = Restrito<br>2 = Sigiloso. |

## localizador

Armazena o tipo, sequencia, complemento, suporte, lugar e o estado de um Localizador na Unidade de Arquivamento relacionada

| Coluna | Descrição |
|---|---|
| id_localizador | Número ID que identifica o localizador. |
| complemento | Descrição do complemento localizador. |
| id_lugar_localizador | Número ID que identifica o lugar do localizador. |
| id_tipo_localizador | Número ID que identifica o tipo de localizador. |
| id_tipo_suporte | Número ID que identifica o tipo de suporte localizador. |
| id_unidade | Número ID que identifica a unidade localizadora. |
| seq_localizador | Número ID que identifica a sequencia do localizadora. |
| sin_ativo | Variável categórica que indica se o localizador está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_estado | Status multi-valorado que identifica o Tipo de estado:<br><br><ul><li>A = Aberto</li><li>F = Fechado</li></ul> |

## lugar_localizador

Armazena as parametrizações pela Unidade de Arquivamento do endereço físico (lugar) onde fica um Localizador associado

| Coluna | Descrição |
|---|---|
| id_lugar_localizador | Número ID que identifica o lugar do localizador. |
| id_unidade | Número ID que identifica a unidade do lugar do localizador. |
| nome | Armazena o nome do lugar do localizador |
| sin_ativo | Variável categórica que indica se o lugar do localizador está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## mapeamento_assunto

Armazena a origem e o destino do assunto a ser utilizados no caso de atualização da tabela de assuntos

| Coluna | Descrição |
|---|---|
| id_assunto_destino | Número ID que identifica o destino do mapeamento do assunto |
| id_assunto_origem | Número ID que identifica a origem do mapeamento do assunto |

## marcador

Armazena as informações dos marcadores e suas respectivas unidades

| Coluna | Descrição |
|---|---|
| id_marcador | Número ID que identifica o Marcador |
| descricao | Armazena a Descrição do Marcador criado na Unidade |
| id_unidade | Número ID que identifica a unidade proprietária do Marcador |
| nome | Armazena o nome do Marcador criado na Unidade |
| sin_ativo | Variável categórica que indica se marcador está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_icone | Status multi-valorado que identifica a Cor do Marcador:<br><br><ul><li>0 = Preto</li><li>1 = Branco</li><li>2 = Cinza</li><li>3 = Vermelho</li><li>4 = Amarelo</li><li>5 = Verde</li><li>6 = Azul</li><li>7 = Rosa</li><li>8 = Roxo</li><li>9 = Ciano</li></ul> |

## modelo

Administração dos Modelos de Documentos

| Coluna | Descrição |
|---|---|
| id_modelo | Número ID que identifica o modelo |
| nome | Armazena o nome modelo |
| sin_ativo | Variável categórica que indica se o modelo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## monitoramento_servico

Monitoração dos serviços utilizados nas integrações do SEI com outro sistemas (Administração)

| Coluna | Descrição |
|---|---|
| id_monitoramento_servico | Número ID que identifica o monitoramento de serviço |
| dth_acesso | Data/hora da operação de monitoramento de serviço |
| id_servico | Número ID que identifica o serviço do monitoramento |
| ip_acesso | Armazena o IP de acesso da operação de monitoramento de serviço |
| operacao | Armazena o nome da operação de monitoramento de serviço |
| servidor | Armazena o servidor de acesso da operação de monitoramento de serviço |
| tempo_execucao | Armazena o tempo de execução da operação de monitoramento de serviço para a operação cadastrada |
| user_agent | Armazena o user agent de acesso da operação de monitoramento de serviço |

## nivel_acesso_permitido

Administração dos Níveis de Acesso Permitidos para os Tipos de Processos

| Coluna | Descrição |
|---|---|
| id_nivel_acesso_permitido | Número ID que identifica o nível de acesso permitido |
| id_tipo_procedimento | Número ID que identifica o tipo de processo do nível de acesso permitido |
| sta_nivel_acesso | Status multi-valorado que identifica o Tipo de nível de acesso:<br><br><ul><li>0 = Público</li><li>1 = Restrito</li><li>2 = Sigiloso</li></ul> |

## notificacao

Tabela vazia - Não utilizada pelo SEI

| Coluna | Descrição |
|---|---|
| id_notificacao | Número ID que identifica a notificação - Tabela vazia - Não utilizada pelo SEI |
| dth_geracao | Data/hora da geração da notificação - Tabela vazia - Não utilizada pelo SEI |
| id_atividade_confirmacao | Número ID que identifica a atividade de confirmação - Tabela vazia - Não utilizada pelo SEI |
| id_procedimento | Número ID que identifica o procedimento da notificação - Tabela vazia - Não utilizada pelo SEI |
| id_unidade | Número ID que identifica a unidade da notificação - Tabela vazia - Não utilizada pelo SEI |
| id_usuario | Número ID que identifica o usuário - Tabela vazia - Não utilizada pelo SEI |

## novidade

Administração das Novidades publicadas

| Coluna | Descrição |
|---|---|
| id_novidade | Número ID que identifica a novidade. |
| descricao | Descrição da novidade. |
| dth_liberacao | Data/hora da liberação da novidade. |
| id_usuario | Número ID que identifica o usuário que inseriou a novidade. |
| titulo | Descrição do titulo da novidade. |

## numeracao

Administração da sequência do número dos documentos numerados

| Coluna | Descrição |
|---|---|
| id_numeracao | Número ID que identifica a numeração. |
| ano | Número ID que identifica o ano sequencial da numeração. |
| id_orgao | Número ID que identifica a numeração do órgão. Quando esta variável recebe o valor '0' (zero), a unidade estará nula. |
| id_serie | Número ID que identifica a numeração de serie. |
| id_unidade | Número ID que identifica a numeração da unidade. Quando esta variável recebe valor (diferente de nulo), o órgão estará nulo (vazio) |
| sequencial | Número ID que identifica o sequencial da numeração. |

## observacao

Armazena o texto de Observações da Unidade sobre protocolos de Processo ou de Documentos

| Coluna | Descrição |
|---|---|
| id_observacao | Número ID que identifica 'Observações desta unidade' sobre protocolos de Processo ou de Documentos. |
| descricao | Descrição de Cadastro de 'Observações desta unidade' sobre protocolos de Processo ou de Documentos. |
| id_protocolo | Número ID que identifica o protocolo relativo a observação. |
| id_unidade | Número ID que identifica a unidade em que o protocolo estava aberto quando a observação foi inserida. |
| idx_observacao | Registro idx de indexação de informações e facilitação da pesquisa da tabela observação. O indexador é armazenado com os caracteres alfanuméricos em minúsculo do campo descricao. |

## operacao_servico

Administração das Operações permitidas para Integração utilizando o Serviço configurado para determinado Sistema

| Coluna | Descrição |
|---|---|
| id_operacao_servico | Número ID que identifica a operação de serviço. |
| id_serie | Número ID que identifica a serie de operação de serviço. |
| id_servico | Número ID que identifica o serviço. |
| id_tipo_procedimento | Número ID que identifica o tipo de procedimento (processo) da operação de serviço. |
| id_unidade | Número ID que identifica a unidade de operação de serviço. |
| sta_operacao_servico | Status multi-valorado que identifica o Tipo de operação de serviço:<br><br><ul><li>0 = Gerar procedimento (processo)</li><li>1 = Incluir documento</li><li>2 = Consultar procedimento (processo)</li><li>3 = Consultar documento</li><li>4 = Gerar bloco</li><li>5 = Excluir bloco</li><li>6 = Diponibilizar bloco</li><li>7 = Disponibilização bloco</li><li>8 = Documento bloco</li><li>9 = Retirar documento bloco</li><li>10 = Incluir procedimento bloco</li><li>11 = Retirar procedimento bloco</li><li>12 = Reabrir procedimento</li><li>13 = Concluir procedimento</li><li>14 = Listar extensões permitidas</li><li>15 = Enviar procedimento</li><li>16 = Listar usuários</li><li>17 = Atribuir procedimento</li><li>18 = Consultar bloco</li><li>19 = Listar hipóteses legais</li><li>20 = Cancelar documento</li><li>21 = Listar tipos conferencia</li><li>22 = Adicionar arquivo</li><li>23 = Adicionar conteúdo arquivo</li><li>24 = Listar contatos</li><li>25 = Atualizar contatos</li><li>26 = Listar países</li><li>27 = Listar estados</li><li>28 = Listar cidades</li><li>29 = Lançar andamento</li><li>30 = Listar andamentos</li><li>31 = Bloquear procedimento</li><li>32 = Desbloquear procedimento</li><li>33 = Relacionar procedimento</li><li>34 = Remover relacionamento procedimento</li><li>35 = Listar marcadores unidade</li><li>36 = Definir marcador</li><li>37 = Listar andamentos marcadores</li><li>38 = Sobrestar procedimento</li><li>39 = Remover sobrestamento procedimento</li><li>40 = Anexar procedimento</li><li>41 = Desanexar procedimento</li><li>42 = Listar cargos</li><li>43 = Consultar procedimento individual</li><li>1000 = Listar unidades</li><li>1001 = Listar tipos procedimentos</li><li>1002 = Listar series</li></ul> |

## ordenador_despesa

Tabela vazia - Não utilizada pelo SEI

| Coluna | Descrição |
|---|---|
| id_ordenador_despesa | Número ID que identifica o ordenador de despesa - Tabela vazia - Não utilizada pelo SEI |
| id_orgao | Número ID que identifica o órgão de ordenador de despesa - Tabela vazia - Não utilizada pelo SEI |
| id_unidade | Número ID que identifica a unidade - Tabela vazia - Não utilizada pelo SEI |
| id_usuario | Número ID que identifica o usuário de ordenador de despesa - Tabela vazia - Não utilizada pelo SEI |
| sin_padrao | Variável categórica que indica se possui padrão de ordenador de despesa:<br><br><ul><li>S = Possui padrão de ordenador de despesa</li><li>N = Não possui padrão de ordenador de despesa</li></ul><br>- Tabela vazia - Não utilizada pelo SEI |

## orgao

Administração do Cadastro de Órgãos

| Coluna | Descrição |
|---|---|
| id_orgao | Número ID que identifica o órgão. |
| codigo_sei | código sei do órgão. |
| descricao | Descrição do órgão. |
| id_contato | Número ID que identifica o contato do órgão. |
| id_orgao_federacao | Número ID que identifica o órgão do órgão no Sei Federação |
| id_unidade | Número ID que identifica a unidade . |
| idx_orgao | Registro idx de indexação de informações e facilitação da pesquisa da tabela Órgão. Fomado pelos campos sigla e descricao. |
| numeracao | Númeração do órgão. |
| servidor_corretor_ortografico | Armazena o servidor de corretor ortográfico do Órgão |
| sigla | Armazena a sigla do órgão |
| sin_ativo | Variável categórica que indica se o órgão está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_consulta_processual | Variável categórica que indica se o órgão está habilitado para a consulta processual:<br><br><ul><li>S = Habilitado para a consulta processual</li><li>N = Não habilitado para a consulta processual</li></ul> |
| sin_envio_processo | Variável categórica que indica se o órgão envia processo:<br><br><ul><li>S = Envia processo</li><li>N = Não envia processo</li></ul> |
| sin_federacao_envio | Variável categórica que indica se o envio de processo via SEI federação está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_federacao_recebimento | Variável categórica que indica se o recebimento de processo via SEI federação está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_publicacao | Variável categórica que indica se as unidades do órgão podem publicar documentos:<br><br><ul><li>S = Podem publicar documentos</li><li>N = Não podem publicar documentos</li></ul> |
| sta_corretor_ortografico | Status multi-valorado que identifica o Tipo de Corretor Ortográfico do Órgão:<br><br><ul><li>B = Nativo Navegador</li><li>N = Nenhum</li><li>L = Licenciado</li></ul> |
| timbre | Timbre do órgão. |

## orgao_federacao

Armazena informações sobre os órgão cadastrados no Sei Federação

| Coluna | Descrição |
|---|---|
| id_orgao_federacao | Número ID que identifica o órgão do órgão no Sei Federação |
| descricao | Descrição que identifica o órgão no Sei Federação |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão participante da ação realizada no Sei Federação |
| sigla | Sigla que identifica o órgão no Sei Federação |

## orgao_historico

Armaneza as modificações ocorridas no registro dos órgãos

| Coluna | Descrição |
|---|---|
| id_orgao_historico | Número ID que identifica o histórico do órgão. |
| descricao | Nome por extenso do órgão |
| dta_fim | Data da finalização do cadastro do órgão no SEI |
| dta_inicio | Data de cadastro do órgão no SEI |
| id_orgao | Número ID que identifica o órgão. |
| sigla | Sigla do órgão |

## pais

Administração do Cadastro de países para uso nos contatos

| Coluna | Descrição |
|---|---|
| id_pais | Número ID que identifica o país. |
| nome | Armazena o nome do país. |

## parametro_acao_federacao

Armaneza os registros de id de ações realizadas no Sei federação

| Coluna | Descrição |
|---|---|
| id_acao_federacao | Número ID que identifica a ação realizada no Sei Federação |
| nome | Nome que identifica a parametro no Sei federação |
| valor | Números do id_protocolo_federacao associados ao paramentro, separados por virgulas. |

## participante

Armazena os relacionamentos e tipo correspondente do Participante no âmbito de determinado Protocolo, de Processo ou de Documento Gerado ou Externo

| Coluna | Descrição |
|---|---|
| id_participante | Número ID que identifica o participante. |
| id_contato | Número ID que identifica o contato do participante. |
| id_protocolo | Número ID que identifica o protocolo que foi inserido a informação do participante. |
| id_unidade | Número ID que identifica a unidade que inseriou a informação do participante. |
| sequencia | Sequencia do participante. |
| sta_participacao | Status multi-valorado que identifica o Tipo de participação:<br><br><ul><li>I = Interessado</li><li>D = Destinatário</li><li>R = Remetente</li><li>A = Acesso externo</li></ul> |

## pesquisa

Armaneza os dados de registro das pesquisas salvas

| Coluna | Descrição |
|---|---|
| id_pesquisa | Número ID que identifica a pesquisa salva |
| id_unidade | Número ID que identifica o usuário que salvou a pesquisa |
| id_usuario | Número ID que identifica a unidade onde a pesquisa está salva |
| nome | Nome de identificação da pesquisa salva inserido pelo usuário |

## plano_trabalho

Administração dos planos de trabalho, usados para orientar a tramitação de processos por etapas predefinidas

| Coluna | Descrição |
|---|---|
| id_plano_trabalho | Número ID que identifica o plano de trabalho. |
| descricao | Armazena a descrição do plano de trabalho. |
| nome | Armazena o nome do plano de trabalho. |
| sin_ativo | Variável categórica que indica se o plano de trabalho está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## procedimento

Armazena a associação do processo com o Tipo de Processo

| Coluna | Descrição |
|---|---|
| id_procedimento | Número ID que identifica o processo. |
| dta_conclusao | Data de conclusão do procedimento. |
| dta_eliminacao | Data de eliminação do procedimento. |
| id_plano_trabalho | Número ID que identifica o plano de trabalho associado ao procedimento. |
| id_tipo_prioridade | Número ID que identifica o tipo de prioridade de tramitação do procedimento. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |
| sin_ciencia | Variável categórica que indica se houve ciência sobre o processo anexado:<br><br><ul><li>S = Houve ciência sobre o processo anexado</li><li>N = Não houve ciência sobre o processo anexado</li></ul> |

## protocolo

Armazena as informações dos Protocolos, seja de Processo, Documento Gerado ou Documento Externo

| Coluna | Descrição |
|---|---|
| id_protocolo | Número ID que identifica o protocolo. |
| codigo_barras | Código de barras do protocolo. |
| descricao | Descrição do protocolo. |
| dta_geracao | Data da geração do protocolo, automático ou informado manualmente. |
| dta_inclusao | Data de inclusão do protocolo no sistema, segundo a operação no sistema e constante no andamento. |
| id_hipotese_legal | Número ID que identifica a hipótese legal. |
| id_protocolo_agrupador | Número ID que identifica o protocolo agrupador. |
| id_protocolo_federacao | Número ID que identifica o número do processo ou documento compartilhado no Sei Federação. |
| id_unidade_geradora | Número ID que identifica a unidade geradora do protocolo. |
| id_usuario_gerador | Número ID que identifica o usuário gerador do protocolo. |
| protocolo_formatado | Armazena o número do protocolo formatado com os devidos caracteres alfanuméricos pertinentes ao protocolo.<br><br>Quando o campo sta_protocolo é diferente de 'P' este campo assume o formato '0000000'<br>e quando o campo sta_protocolo é igual a 'P' este campo assume a formatação de protocolo de processo '00000.000000/0000-00'. |
| protocolo_formatado_pesq_inv | Número do protocolo formatado com a ordem invertida. Se o protocolo formatado for 0199999, o protocolo invertido será 9999910. |
| protocolo_formatado_pesquisa | Armazena o número do protocolo formatado sem os devidos caracteres alfanuméricos pertinentes ao protocolo |
| sin_eliminado | Variável categórica que indica se o protocolo foi eliminado:<br><br><ul><li>S = Eliminado</li><li>N = Não eliminado</li></ul> |
| sta_estado | Status multi-valorado que identifica o estado do protocolo:<br><br><ul><li>0 = Normal</li><li>1 = Processo Sobrestado</li><li>2 = Documento Cancelado</li><li>3 = Processo Anexado</li><li>4 = Processo Bloqueado</li></ul> |
| sta_grau_sigilo | Status multi-valorado que identifica o Tipo de grau de sigilo:<br><br><ul><li>U = Ultrassecreto</li><li>S = Secreto</li><li>R = Reservado</li></ul> |
| sta_nivel_acesso_global | Status multi-valorado que identifica o Tipo de nível de acesso global do protocolo:<br><br><ul><li>0 = Público</li><li>1 = Restrito</li><li>2 = Sigiloso</li></ul> |
| sta_nivel_acesso_local | Status multi-valorado que identifica o Tipo de nível de acesso local do protocolo:<br><br><ul><li>0 = Público</li><li>1 = Restrito</li><li>2 = Sigiloso</li></ul> |
| sta_nivel_acesso_original | Status multi-valorado que identifica o Tipo de nível de acesso original:<br><br><ul><li>0 = Público</li><li>1 = Restrito</li><li>2 = Sigiloso</li></ul> |
| sta_protocolo | Status multi-valorado que identifica o Tipo de protocolo:<br><br><ul><li>P = Processo (envolve a tabela 'procedimento')</li><li>G = Documento Gerado (envolve a tabela 'documento')</li><li>R = Documento Externo (envolve as tabelas 'documento' e 'anexo')</li></ul> |

## protocolo_federacao

Armazena informações sobre os protocolos compartilhados no Sei Federação

| Coluna | Descrição |
|---|---|
| id_protocolo_federacao | Número ID que identifica o número do processo ou documento compartilhado no Sei Federação. |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão participante da ação realizada no Sei Federação |
| protocolo_formatado | Variável associada ao id_protocolo_federacao que armazena o número do protocolo formatado com os devidos caracteres alfanuméricos pertinentes ao protocolo. |
| protocolo_formatado_pesq_inv | Variável associada ao id_protocolo_federacao correspondente ao número do protocolo formatado com a ordem invertida. Se o protocolo formatado for 0199999, o protocolo invertido será 9999910. |
| protocolo_formatado_pesquisa | Variável associada ao id_protocolo_federacao que armazena o número do protocolo formatado sem os devidos caracteres alfanuméricos pertinentes ao protocolo |

## protocolo_idx

Registro de indexação do protocolo (processo ou documento) para fins de pesquisa

| Coluna | Descrição |
|---|---|
| id_protocolo | Número ID que identifica o protocolo indexado. |
| dth_indexacao | Data/hora de indexação do registro do protocolo. |

## protocolo_modelo

Armazena as informações relativa aos modelos de documentos salvos

| Coluna | Descrição |
|---|---|
| id_protocolo_modelo | Número ID que identifica o protocolo modelo. |
| descricao | Armazena a descrição textual do protocolo modelo |
| dth_alteracao | Data/hora da geração e alteração do protocolo modelo. |
| id_grupo_protocolo_modelo | Número ID que identifica o grupo de protocolo modelo. |
| id_protocolo | Número ID que identifica o protocolo relativo ao protocolo modelo. |
| id_unidade | Número ID que identifica a unidade onde foi salva o modelo. |
| id_usuario | Número ID que identifica o usuário que salvou o modelo. |
| idx_protocolo_modelo | Registro idx de indexação de informações e facilitação da pesquisa da tabela protocolo_modelo. Formado pelos campos número do protocolo_formatado (tabela protocolo), a descricao e a dth_alteracao. |

## publicacao

Armazena as informações referentes aos documentos publicados

| Coluna | Descrição |
|---|---|
| id_publicacao | Número ID que identifica a publicação. |
| dta_disponibilizacao | Data da disponibilização da publicação. |
| dta_publicacao | Data da publicação. |
| dta_publicacao_io | Data da publicação io (Em órgãos federais, normalmente o io é o Diário Oficial da União - DOU) Este campo estará preenchido apenas quando os campos id_veiculo_io e id_secao_io estiverem preenchidos |
| dth_agendamento | Data/hora do agendamento da publicação. |
| id_atividade | Número ID que identifica a atividade de publicação. |
| id_documento | Número ID que identifica o documento de publicação. |
| id_secao_io | Número ID que identifica a seção io (Em órgãos federais, normalmente o io é o Diário Oficial da União - DOU) |
| id_unidade | Número ID que identifica a unidade de publicação. |
| id_usuario | Número ID que identifica o usuário de publicação. |
| id_veiculo_io | Número ID que identifica o veiculo io (Em órgãos federais, normalmente o io é o Diário Oficial da União - DOU). |
| id_veiculo_publicacao | Número ID que identifica o veiculo de publicação. |
| numero | Armazena o número da publicação |
| pagina_io | Armazena o número da página da publicação Este campo estará preenchido apenas quando os campos id_veiculo_io e id_secao_io estiverem preenchidos |
| resumo | Armazena o resumo da publicação |
| sta_motivo | Status multi-valorado que identifica o Tipo de motivo da publicação:<br><br><ul><li>1 = Publicação</li><li>2 = Retificação</li><li>3 = Republicação</li><li>4 = Apostilamento</li></ul> |

## publicacao_idx

Registro de indexação da publicação para fins de pesquisa

| Coluna | Descrição |
|---|---|
| id_publicacao | Número ID que identifica a publicação indexada. |
| dth_indexacao | Data/hora de indexação do registro da publicação. |

## publicacao_legado

Armazena as informações referentes aos documentos publicados do legado

| Coluna | Descrição |
|---|---|
| id_publicacao_legado | Número ID que identifica a publicação de legado. |
| conteudo_documento | Armazena o conteúdo do documento da publicação legada |
| dta_geracao | Data da geração da publicação legada |
| dta_publicacao | Data da publicação legada |
| dta_publicacao_io | Data da publicação io (Em órgãos federais, normalmente o io é o Diário Oficial da União - DOU). |
| id_documento | Número ID que identifica o documento. |
| id_orgao | Número ID que identifica o órgão. |
| id_publicacao_legado_agrupador | Número ID que identifica a publicação de legado agrupador. |
| id_secao_io | Número ID que identifica a seção io. |
| id_serie | Número ID que identifica a serie. |
| id_unidade | Número ID que identifica a unidade. |
| id_veiculo_io | Número ID que identifica o veiculo io. |
| id_veiculo_publicacao | Número ID que identifica o veiculo de publicação. |
| numero | Armazena o número da publicação legada |
| pagina_io | Armazena o número da página da publicação legada |
| protocolo_formatado | Armazena o número do protocolo formatado da publicação legada |
| resumo | Armazena o resumo da publicação legada |

## reabertura_programada

Registra as reaberturas programadas de processos

| Coluna | Descrição |
|---|---|
| id_reabertura_programada | Número ID que identifica a reabertura programada. |
| dta_programada | Data programada para a reabertura do processo. |
| dth_alteracao | Data/hora da última alteração da reabertura programada. |
| dth_processamento | Data/hora de processamento da reabertura programada. |
| dth_visualizacao | Data/hora de visualização da reabertura programada. |
| erro | Armazena a mensagem de erro do processamento da reabertura programada. |
| id_atividade | Número ID que identifica a atividade relacionada à reabertura programada. |
| id_protocolo | Número ID que identifica o protocolo (processo) da reabertura programada. |
| id_unidade | Número ID que identifica a unidade da reabertura programada. |
| id_usuario | Número ID que identifica o usuário que programou a reabertura. |

## rel_acesso_ext_protocolo

Associativa entre o acesso externo e o protocolo

| Coluna | Descrição |
|---|---|
| id_acesso_externo | Número ID que identifica o acesso externo |
| id_protocolo | Número do ID do Protocolo que foi disponibilizdo no acesso externo |

## rel_acesso_ext_serie

Associativa entre o tipo de documento e o acesso externo concedido

| Coluna | Descrição |
|---|---|
| id_acesso_externo | Número ID que identifica o acesso externo |
| id_serie | Número ID que identifica o Tipo de Documento que foi dado acesso externo |

## rel_assinante_unidade

Associativa entre assinante e unidade

| Coluna | Descrição |
|---|---|
| id_assinante | Número ID que identifica o assinante. |
| id_unidade | Número ID que identifica a unidade. |

## rel_aviso_orgao

Associativa entre o aviso e os órgãos aos quais ele é destinado

| Coluna | Descrição |
|---|---|
| id_aviso | Número ID que identifica o aviso. |
| id_orgao | Número ID que identifica o órgão destinatário do aviso. |

## rel_base_conhec_tipo_proced

Associativa entre o tipo de processo e a base de conhecimento

| Coluna | Descrição |
|---|---|
| id_base_conhecimento | Número ID que identifica a base de conhecimento. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |

## rel_bloco_protocolo

Associativa entre o bloco e o protocolo

| Coluna | Descrição |
|---|---|
| anotacao | Descrição da anotação do relacionamento entre bloco e protocolo. |
| id_bloco | Número ID que identifica o bloco. |
| id_protocolo | Número ID que identifica o protocolo. |
| idx_rel_bloco_protocolo | Registro idx de indexação de informações e facilitação da pesquisa da tabela rel_bloco_protocolo. Formado pelo número formatado do processo, número formatado do documento e a descrição do bloco. |
| sequencia | Número ID que identifica a sequencia do relacionamento entre bloco e protocolo. |

## rel_bloco_unidade

Associativa entre a unidade organizacional e o bloco

| Coluna | Descrição |
|---|---|
| dth_comentario | Registro da data de marcação da Opção de Sinalização C - Comentário no bloco de assinatura |
| dth_prioridade | Registro da data de marcação da Opção de Sinalização P - Prioridade no bloco de assinatura |
| dth_revisao | Registro da data de marcação da Opção de Sinalização R - Revisão no bloco de assinatura |
| id_bloco | Número ID que identifica o bloco. |
| id_grupo_bloco | Número ID que identifica a sequencia do relacionamento entre bloco e unidade. |
| id_unidade | Número ID que identifica a unidade. |
| id_usuario_atribuicao | Número do ID do usuário atribuído para assinatura dos documentos contido no bloco de assinatura |
| id_usuario_comentario | Número do ID do usuário que ticou a Opção de Sinalização C - Comentário no bloco de assinatura |
| id_usuario_prioridade | Número do ID do usuário que ticou a Opção de Sinalização P - Prioridade no bloco de assinatura |
| id_usuario_revisao | Número do ID do usuário que ticou a Opção de Sinalização R - Revisão no bloco de assinatura |
| sin_comentario | Variável categórica que indica se a marcação de Comentário no bloco está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_prioridade | Variável categórica que indica se a marcação de Prioridade no bloco está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_retornado | Variável categórica que indica se a unidade retornou o bloco:<br><br><ul><li>S = Retornou o bloco</li><li>N = Não retornou o bloco</li></ul> |
| sin_revisao | Variável categórica que indica se a marcação de Revisão no bloco está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| texto_comentario | Texto inserido no campo comentário no bloco de assinatura |

## rel_controle_interno_orgao

Associativa entre o controle interno e o órgão

| Coluna | Descrição |
|---|---|
| id_controle_interno | Número ID que identifica o controle interno. |
| id_orgao | Número ID que identifica o órgão. |

## rel_controle_interno_serie

Associativa entre Controle Interno e Tipo de Documento parametrizados no Controle Interno pela Administração

| Coluna | Descrição |
|---|---|
| id_controle_interno | Número ID que identifica o controle interno. |
| id_serie | Número ID que identifica a serie para o controle interno da série. |

## rel_controle_interno_tipo_proc

Associativa entre o tipo de processo e o controle interno

| Coluna | Descrição |
|---|---|
| id_controle_interno | Número ID que identifica o controle interno. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |

## rel_controle_interno_unidade

Associativa entre o controle interno e a unidade organizacional

| Coluna | Descrição |
|---|---|
| id_controle_interno | Número ID que identifica o controle interno. |
| id_unidade | Número ID que identifica a unidade. |

## rel_grupo_contato

Associativa entre o grupo de contato e o contato

| Coluna | Descrição |
|---|---|
| id_contato | Número ID que identifica o contato. |
| id_grupo_contato | Número ID que identifica o grupo de contato. |

## rel_grupo_fed_orgao_fed

Associativa entre a órgão e o grupo da unidade organizacional no Sei Federação

| Coluna | Descrição |
|---|---|
| id_grupo_federacao | Número ID que identifica o grupo criado no Sei Federação |
| id_orgao_federacao | Número ID que identifica o órgão do órgão no Sei Federação |

## rel_grupo_unidade_unidade

Associativa entre a unidade organizacional e o grupo da unidade organizacional

| Coluna | Descrição |
|---|---|
| id_grupo_unidade | Número ID que identifica o grupo da unidade. |
| id_unidade | Número ID que identifica a unidade. |

## rel_item_etapa_documento

Associativa entre o item de etapa e os documentos gerados ou anexados em sua execução

| Coluna | Descrição |
|---|---|
| id_documento | Número ID que identifica o documento associado ao item de etapa. |
| id_item_etapa | Número ID que identifica o item de etapa. |

## rel_item_etapa_serie

Associativa entre o item de etapa e os tipos de documento (séries) aplicáveis

| Coluna | Descrição |
|---|---|
| id_item_etapa | Número ID que identifica o item de etapa. |
| id_serie | Número ID que identifica o tipo de documento (série) associado ao item de etapa. |

## rel_item_etapa_unidade

Associativa entre o item de etapa e as unidades responsáveis por sua execução

| Coluna | Descrição |
|---|---|
| id_item_etapa | Número ID que identifica o item de etapa. |
| id_unidade | Número ID que identifica a unidade responsável pelo item de etapa. |

## rel_notificacao_documento

Associativa entre o documento e a notificação

| Coluna | Descrição |
|---|---|
| id_documento | Número ID que identifica o documento. |
| id_notificacao | Número ID que identifica a notificação. |
| sin_processada | Variável categórica que indica se(S) ou não (N). |

## rel_orgao_pesquisa

Associativa entre órgãos considerados equivalentes para fins de pesquisa

| Coluna | Descrição |
|---|---|
| id_orgao_1 | Número ID que identifica o primeiro órgão da relação de pesquisa. |
| id_orgao_2 | Número ID que identifica o segundo órgão da relação de pesquisa. |

## rel_protocolo_assunto

Associativa entre o protocolo, a unidade organizacional e o assunto proxy

| Coluna | Descrição |
|---|---|
| id_assunto_proxy | Número ID que identifica o assunto arquivístico do protocolo. |
| id_protocolo | Número ID que identifica o protocolo. |
| id_protocolo_procedimento | Número ID que identifica o protocolo do procedimento relacionado ao assunto. |
| id_unidade | Número ID que identifica a unidade que cadastrou o assunto arquivístico do protocolo. |
| sequencia | Número ID que identifica a sequência do relacionamento entre protocolo e assunto. |

## rel_protocolo_atributo

Associativa entre o protocolo e o atributo

| Coluna | Descrição |
|---|---|
| id_atributo | Número ID que identifica o atributo (campo) relacionado com o protocolo do documento gerado que utilizou Tipo de Formulário. |
| id_protocolo | Número ID que identifica o protocolo relacionado com o atributo (campo) do documento gerado que utilizou Tipo de Formulário. |
| valor | Armazena o valor de registro de fato preenchido pelo usuário sobre o campo relacionado no momento da geração do documento que utiliza o Tipo de Formulário. Este campo fica vazio quando o atributo for do tipo "INFORMACAO", pois o usuário apenas ver uma pré informação apresentada, não sendo um campo de input de fato. |

## rel_protocolo_protocolo

Associativa entre os protocolos

| Coluna | Descrição |
|---|---|
| id_rel_protocolo_protocolo | Número ID que identifica o relacionamento de protocolos. |
| dth_associacao | Data/hora da associação |
| id_protocolo_1 | Número ID que identifica o protocolo 1, que é o protocolo pai. |
| id_protocolo_2 | Número ID que identifica o protocolo 2, que é o protocolo filho. |
| id_unidade | Número ID que identifica a unidade. |
| id_usuario | Número ID que identifica o usuário. |
| sequencia | Número ID que identifica a sequencia do relacionamento entre protocolos. |
| sin_ciencia | Variável categórica que indica se houve ciência sobre o protocolo:<br><br><ul><li>S = Houve ciência sobre o protocolo</li><li>N = Não houve ciência sobre o protocolo</li></ul> |
| sta_associacao | Status multi-valorado que identifica o Tipo de associação entre o protocolo 1 e protocolo 2:<br><br><ul><li>1 = Documento normal, onde o id_protocolo_1 é do processo e o id_protocolo_2 é do documento</li><li>2 = Processo Anexado, onde o id_protocolo_1 é do processo anexador e o id_protocolo_2 é do processo anexado</li><li>3 = Processo Relacionado, onde o id_protocolo_2 indica o processo a partir do qual o relacionamento foi realizado com o id_protocolo_1</li><li>4 = Processo vinculado a processo Sobrestado, onde o id_protocolo_2 identifica o processo que foi de fato sobrestado com vínculo ao id_protocolo_1</li><li>5 = Processo Desanexado, decorrente da alteração do sta_associacao=2 para 5, onde o id_protocolo_2 identifica o processo que foi desanexado</li><li>6 = Documento Movido, identificando a associação original de onde o documento foi movido</li><li>7 = Documento Circular, onde o protocolo 1 é o documento gerador do circular e o protocolo 2 é referente aos documentos gerados a partir do protocolo 1</li></ul> |

## rel_secao_mod_cj_estilos_item

Associativa entre a seção do modelo e os itens de conjunto de estilos

| Coluna | Descrição |
|---|---|
| id_conjunto_estilos_item | Número ID que identifica o conjunto de estilos do item. |
| id_secao_modelo | Número ID que identifica a seção modelo. |
| sin_padrao | Variável categórica que indica se o item de conjunto de estilos é o item padrão da seção do modelo:<br><br><ul><li>S = Item padrão da seção do modelo</li><li>N = Não é o item padrão da seção do modelo</li></ul> |

## rel_secao_modelo_estilo

Associativa entre a seção do modelo e o estilo

| Coluna | Descrição |
|---|---|
| id_estilo | Identificador único do estilo. |
| id_secao_modelo | Identificador único da seção de modelo. |
| sin_padrao | Variável categórica que indica se o estilo é o estilo padrão da seção do modelo:<br><br><ul><li>S = Estilo padrão da seção do modelo</li><li>N = Não é o estilo padrão da seção do modelo</li></ul> |

## rel_serie_assunto

Associativa entre Tipo de Documento e Assunto sugerido parametrizados no Tipo de Documento pela Administração

| Coluna | Descrição |
|---|---|
| id_assunto_proxy | Número ID que identifica o assunto arquivístico associado na administração do Tipo de Documento. |
| id_serie | Número ID que identifica o Tipo de Documento. |
| sequencia | Número ID que identifica a sequência do relacionamento entre o Tipo de Documento e Assunto Arquivístico. |

## rel_serie_plano_trabalho

Associativa entre o plano de trabalho e os tipos de documento (séries) aplicáveis

| Coluna | Descrição |
|---|---|
| id_plano_trabalho | Número ID que identifica o plano de trabalho. |
| id_serie | Número ID que identifica o tipo de documento (série) associado ao plano de trabalho. |

## rel_serie_veiculo_publicacao

Associativa entre Tipo de Documento e Veículo de Publicação parametrizados no Tipo de Documento pela Administração

| Coluna | Descrição |
|---|---|
| id_serie | Número ID que identifica a serie. |
| id_veiculo_publicacao | Número ID que identifica o veiculo de publicação. |

## rel_situacao_unidade

Associativa entre a unidade organizacional e a situação da unidade organizacional

| Coluna | Descrição |
|---|---|
| id_situacao | Número ID que identifica a situação. |
| id_unidade | Número ID que identifica a unidade. |

## rel_tipo_procedimento_assunto

Associativa entre o tipo de processo e o assunto

| Coluna | Descrição |
|---|---|
| id_assunto_proxy | Número ID que identifica o assunto arquivístico associado na administração do Tipo de Processo. |
| id_tipo_procedimento | Número ID que identifica o Tipo de Processo. |
| sequencia | Número ID que identifica a sequência do relacionamento entre o Tipo de Processo e Assunto Arquivístico. |

## rel_unidade_tipo_contato

Associativa entre o tipo de contato da unidade organizacional e a unidade organizacional

| Coluna | Descrição |
|---|---|
| id_rel_unidade_tipo_contato | Número ID que identifica a unidade do tipo do contato. |
| id_tipo_contato | Número ID que identifica o tipo do contato. |
| id_unidade | Número ID que identifica a unidade. |
| sta_acesso | Status multi-valorado que identifica o tipo de acesso da unidade ao tipo de contato:<br><br><ul><li>A = Alteração</li><li>C = Consulta Completa</li></ul> |

## rel_usuario_grupo_acomp

Armazena os atributos de usuário relacionado a um grupo de acompanhamento especial, oriunda das configurações salvas no Painel de Controle.

| Coluna | Descrição |
|---|---|
| id_grupo_acompanhamento | Número ID que identifica a sequencia de relacionamento entre um grupo acompanhamento especial e um usuário, oriunda das configurações salvas no Painel de Controle. |
| id_usuario | Número do ID do usuário relacionado a um grupo de acompanhamento especial, oriunda das configurações salvas no Painel de Controle. |

## rel_usuario_grupo_bloco

Armazena os atributos de relacionamento entre um bloco interno e um usuário, oriunda das configurações salvas no Painel de Controle.

| Coluna | Descrição |
|---|---|
| id_grupo_bloco | Número ID que identifica a sequencia de relacionamento entre um bloco interno e um usuário, oriunda das configurações salvas no Painel de Controle. |
| id_usuario | Número do ID do usuário relacionado a um bloco interno, oriunda das configurações salvas no Painel de Controle. |

## rel_usuario_marcador

Armazena os atributos de relacionamento entre um marcador e um usuário, oriunda das configurações salvas no Painel de Controle.

| Coluna | Descrição |
|---|---|
| id_marcador | Número ID que identifica a sequencia de relacionamento entre um marcador e um usuário, oriunda das configurações salvas no Painel de Controle. |
| id_usuario | Número do ID do usuário relacionado a um marcador, oriunda das configurações salvas no Painel de Controle. |

## rel_usuario_tipo_prioridade

Associativa entre o usuário, a unidade e o tipo de prioridade concedido

| Coluna | Descrição |
|---|---|
| id_tipo_prioridade | Número ID que identifica o tipo de prioridade. |
| id_unidade | Número ID que identifica a unidade em que o tipo de prioridade foi concedido. |
| id_usuario | Número ID que identifica o usuário ao qual o tipo de prioridade foi concedido. |

## rel_usuario_tipo_proced

Armazena os atributos de relacionado entre uma unidade e um processo, oriunda das configurações salvas no Painel de Controle

| Coluna | Descrição |
|---|---|
| id_tipo_procedimento | Número do ID de um procedimento (processo) relacionado a um usuário, oriunda das configurações salvas no Painel de Controle. |
| id_unidade | Número do ID de uma unidade relacionado a um usuário, oriunda das configurações salvas no Painel de Controle. |
| id_usuario | Número do ID de um usuário que se relacionado a uma unidade e um processo, oriunda das configurações salvas no Painel de Controle. |

## rel_usuario_usuario_unidade

Armazena os atributos de relacionado de usuário atribuído relacionado a um usuário, oriunda das configurações salvas no Painel de Controle.

| Coluna | Descrição |
|---|---|
| id_unidade | Número do ID de uma unidade relacionado a um usuário, oriunda das configurações salvas no Painel de Controle. |
| id_usuario | Número do ID de um usuário atribuído relacionado a um usuário, oriunda das configurações salvas no Painel de Controle. |
| id_usuario_atribuicao | Número do ID de um usuário atribuído que se relaciona com uma unidade e um usuário, oriunda das configurações salvas no Painel de Controle. |

## replicacao_federacao

Armazena os dados de replicação de configuração registradas no Sei Federação

| Coluna | Descrição |
|---|---|
| id_replicacao_federacao | Número ID que identifica a replicação no Sei Federação |
| dth_cadastro | Data correspondente ao momento do pedido de cadastro da replicação |
| dth_replicacao | Data correspondente ao momento da validação do cadastro da replicação |
| erro | Descrição que identifica o erro na replicação |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão no Sei Federação |
| id_protocolo_federacao | Número ID que identifica o número do processo ou documento compartilhado no Sei Federação. |
| sin_ativo | Variável categórica que indica se a replicação está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo de replicação:<br><br><ul><li>1 = Acessos</li><li>2 = Sinalização de Atenção</li><li>3 = Sinalização de Publicação</li><li>4 = Sinalização de envio</li><li>5 = Sinalização de Cancelamento</li></ul> |
| tentativa | Número inteiro que identifica a sequência da tentativa |

## retorno_programado

Armazena as informações referentes ao retorno programado

| Coluna | Descrição |
|---|---|
| id_retorno_programado | Número ID que identifica o Retorno Programado. |
| dta_programada | Data programada para o Retorno Programado. |
| dth_alteracao | Data e hora caso ocorra alteração do Retorno Programado. |
| id_atividade_envio | Número ID que identifica a atividade de envio do Retorno Programado. |
| id_atividade_retorno | Número ID que identifica a atividade de retorno efetivo do Retorno Programado, quando ele já tenha retornado. |
| id_protocolo | Número do ID de protocolo marcado com retorno programado |
| id_unidade_envio | Número ID que identifica a unidade de envio do processo com Retorno Programado. |
| id_unidade_retorno | Id da unidade que recebeu o processo com marcação de retorno programado |
| id_usuario | Número ID que identifica o usuário que realizou o envio do processo com Retorno Programado. |

## revisao_avaliacao

Registra as revisões realizadas sobre uma avaliação documental

| Coluna | Descrição |
|---|---|
| id_revisao_avaliacao | Número ID que identifica a revisão de avaliação. |
| dth_revisao | Data/hora da revisão de avaliação. |
| id_avaliacao_documental | Número ID que identifica a avaliação documental revisada. |
| id_unidade | Número ID que identifica a unidade que realizou a revisão. |
| id_usuario | Número ID que identifica o usuário que realizou a revisão. |
| justificativa | Armazena a justificativa da revisão de avaliação. |
| motivo | Armazena o motivo da revisão de avaliação. |
| sin_ativo | Variável categórica que indica se a revisão de avaliação está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sta_revisao_avaliacao | Status multi-valorado que identifica o resultado da revisão de avaliação:<br><br><ul><li>A = Avaliado</li><li>N = Negado</li></ul> |

## secao_documento

Armazena as informações referentes às seções dos documentos criados

| Coluna | Descrição |
|---|---|
| id_secao_documento | Número ID que identifica a seção do documento. |
| conteudo | Armazena o conteúdo textual da seção de documento<br><br>Este campo deverá estar preenchido quando o campo sin_assinatura for igual a 'S'<br>Este campo deverá estar preenchido em HTML quando o campo sin_assinatura for igual a 'S' |
| id_base_conhecimento | Número ID que identifica a base de conhecimento da seção do documento. |
| id_documento | Número ID que identifica o documento. |
| id_secao_modelo | Número ID que identifica a seção modelo. |
| ordem | Número ID que armazena a ordem de apresentação da seção do documento. |
| sin_assinatura | Variável categórica que indica se a seção do documento permite assinatura:<br><br><ul><li>S = Permite assinatura</li><li>N = Não permite assinatura</li></ul><br>Quando esta variável possuir o valor postivo 'S', a variável sin_somente_leitura possuirá apenas o valor igual a 'N' |
| sin_cabecalho | Variável categórica que indica se a seção do documento é de cabeçalho:<br><br><ul><li>S = De cabeçalho</li><li>N = Não é de cabeçalho</li></ul><br>Quando esta variável possuir o valor postivo 'S', a variável sin_rodape possuirá apenas o valor igual a 'N' |
| sin_dinamica | Variável categórica que indica se a seção do documento é dinâmica:<br><br><ul><li>S = Dinâmica</li><li>N = Não dinâmica</li></ul> |
| sin_html | Variável categórica que indica se a seção do documento possui html:<br><br><ul><li>S = Possui html</li><li>N = Não possui html</li></ul> |
| sin_principal | Variável categórica que indica se a seção do documento é principal:<br><br><ul><li>S = Principal</li><li>N = Não principal</li></ul> |
| sin_rodape | Variável categórica que indica se a seção do documento é de rodapé:<br><br><ul><li>S = De rodapé</li><li>N = Não é de rodapé</li></ul><br>Quando esta variável possuir o valor postivo 'S', a variável sin_cabecalho possuirá apenas o valor igual a 'N' |
| sin_somente_leitura | Variável categórica que indica se a seção do documento é apenas para leitura:<br><br><ul><li>S = Apenas para leitura</li><li>N = Não apenas para leitura</li></ul><br>Quando esta variável possuir o valor postivo 'S', a variável sin_assinatura possuirá apenas o valor igual a 'N' |

## secao_imprensa_nacional

Armazena as informações referentes a seção de imprensa nacional

| Coluna | Descrição |
|---|---|
| id_secao_imprensa_nacional | Número ID que identifica a seção da imprensa nacional. |
| descricao | Descrição da seção da imprensa nacional. |
| id_veiculo_imprensa_nacional | Número ID que identifica o veiculo da imprensa nacional. |
| nome | Armazena o nome da seção de imprensa nacional |

## secao_modelo

Armazena as informações referentes às seções dos modelos dos documentos

| Coluna | Descrição |
|---|---|
| id_secao_modelo | Número ID que identifica a seção modelo. |
| conteudo | Armazena o conteúdo textual do modelo de seção<br><br>Este campo obrigatoriamente receberá nulo quando a variável sin_assinatura for igual a 'S'<br>Este campo armazenará o conteúdo no formato HTML quando a variável sin_html for igual a 'S' |
| id_modelo | Número ID que identifica o modelo. |
| nome | Armazena o nome da seção modelo<br><br>Este campo receberá o valor de 'Assinatura' quando a variável sin_assinatura for igual a 'S'<br>Este campo receberá o valor de 'Cabeçalho' quando a variável sin_cabecalho for igual a 'S'<br>Este campo receberá o valor de 'Rodapé' quando a variável sin_rodape for igual a 'S' |
| ordem | Armazena a ordem de apresentação do modelo de seção |
| sin_assinatura | Variável categórica que indica se o modelo de seção permite assinatura:<br><br><ul><li>S = Permite assinatura</li><li>N = Não permite assinatura</li></ul> |
| sin_ativo | Variável categórica que indica se o modelo de seção é ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_cabecalho | Variável categórica que indica se o modelo de seção é de cabeçalho:<br><br><ul><li>S = De cabeçalho</li><li>N = Não de cabeçalho</li></ul> |
| sin_dinamica | Variável categórica que indica se o modelo de seção é dinâmica:<br><br><ul><li>S = Dinâmica</li><li>N = Não dinâmica</li></ul> |
| sin_html | Variável categórica que indica se o modelo de seção possui html:<br><br><ul><li>S = Possui html</li><li>N = Não possui html</li></ul> |
| sin_principal | Variável categórica que indica se o modelo de seção é principal:<br><br><ul><li>S = Principal</li><li>N = Não principal</li></ul> |
| sin_rodape | Variável categórica que indica se o modelo de seção é de rodapé:<br><br><ul><li>S = De rodapé</li><li>N = Não de rodapé</li></ul> |
| sin_somente_leitura | Variável categórica que indica se o modelo de seção é somente para leitura:<br><br><ul><li>S = Somente para leitura</li><li>N = Não somente para leitura</li></ul><br>Este campo receberá o valor igual a 'N' quando o campo sin_assinatura for igual a 'S' |

## seq_acesso

Sequence da tabela acesso

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela acesso |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_acesso_externo

Sequence da tabela acesso_externo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela acesso_externo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_acompanhamento

Sequence da tabela acompanhamento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela acompanhamento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_andamento_instalacao

Sequence da tabela andamento_instalacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela andamento_instalacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_andamento_marcador

Sequence da tabela andamento_marcador

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela andamento_marcador |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_andamento_plano_trabalho

Sequence da tabela andamento_plano_trabalho

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela andamento_plano_trabalho |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_andamento_situacao

Sequence da tabela andamento_situacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela andamento_situacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_anexo

Sequence da tabela anexo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela anexo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_anotacao

Sequence da tabela anotacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela anotacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_arquivo_extensao

Sequence da tabela arquivo_extensao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela arquivo_extensao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_assinante

Sequence da tabela assinante

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela assinante |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_assinatura

Sequence da tabela assinatura

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela assinatura |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_assunto

Sequence da tabela assunto

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela assunto |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_assunto_proxy

Sequence da tabela assunto_proxy

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela assunto_proxy |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_atividade

Sequence da tabela atividade

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela atividade |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_atributo

Sequence da tabela atributo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela atributo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_atributo_andam_plano_trab

Sequence da tabela atributo_andam_plano_trab

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela atributo_andam_plano_trab |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_atributo_andamento

Sequence da tabela atributo_andamento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela atributo_andamento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_atributo_andamento_situaca

Sequence da tabela atributo_andamento_situaca

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela atributo_andamento_situaca |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_atributo_instalacao

Sequence da tabela atributo_instalacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela atributo_instalacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_auditoria_protocolo

Sequence da tabela auditoria_protocolo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela auditoria_protocolo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_avaliacao_documental

Sequence da tabela avaliacao_documental

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela avaliacao_documental |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_aviso

Sequence da tabela aviso

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela aviso |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_base_conhecimento

Sequence da tabela base_conhecimento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela base_conhecimento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_bloco

Sequence da tabela bloco

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela bloco |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_campo_pesquisa

Sequence da tabela campo_pesquisa

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela campo_pesquisa |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_cargo

Sequence da tabela cargo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela cargo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_categoria

Sequence da tabela categoria

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela categoria |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_cidade

Sequence da tabela cidade

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela cidade |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_comentario

Sequence da tabela comentario

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela comentario |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_conjunto_estilos

Sequence da tabela conjunto_estilos

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela conjunto_estilos |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_conjunto_estilos_item

Sequence da tabela conjunto_estilos_item

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela conjunto_estilos_item |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_contato

Sequence da tabela contato

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela contato |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_controle_interno

Sequence da tabela controle_interno

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela controle_interno |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_controle_prazo

Sequence da tabela controle_prazo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela controle_prazo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_controle_unidade

Sequence da tabela controle_unidade

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela controle_unidade |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_documento

Sequence da tabela documento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela documento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_dominio

Sequence da tabela dominio

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela dominio |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_edital_eliminacao

Sequence da tabela edital_eliminacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela edital_eliminacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_edital_eliminacao_conteudo

Sequence da tabela edital_eliminacao_conteudo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela edital_eliminacao_conteudo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_edital_eliminacao_erro

Sequence da tabela edital_eliminacao_erro

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela edital_eliminacao_erro |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_email_grupo_email

Sequence da tabela email_grupo_email

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela email_grupo_email |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_email_sistema

Sequence da tabela email_sistema

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela email_sistema |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_email_unidade

Sequence da tabela email_unidade

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela email_unidade |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_email_utilizado

Sequence da tabela email_utilizado

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela email_utilizado |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_estatisticas

Sequence da tabela estatisticas

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela estatisticas |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_estilo

Sequence da tabela estilo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela estilo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_etapa_trabalho

Sequence da tabela etapa_trabalho

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela etapa_trabalho |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_feed

Sequence da tabela feed

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela feed |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_feriado

Sequence da tabela feriado

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela feriado |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_acompanhamento

Sequence da tabela grupo_acompanhamento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_acompanhamento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_bloco

Sequence da tabela grupo_bloco

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_bloco |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_contato

Sequence da tabela grupo_contato

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_contato |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_email

Sequence da tabela grupo_email

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_email |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_federacao

Sequence da tabela grupo_federacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_federacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_protocolo_modelo

Sequence da tabela grupo_protocolo_modelo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_protocolo_modelo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_serie

Sequence da tabela grupo_serie

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_serie |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_grupo_unidade

Sequence da tabela grupo_unidade

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela grupo_unidade |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_hipotese_legal

Sequence da tabela hipotese_legal

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela hipotese_legal |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_imagem_formato

Sequence da tabela imagem_formato

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela imagem_formato |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_infra_auditoria

Sequence da tabela infra_auditoria

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela infra_auditoria |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_infra_log

Sequence da tabela infra_log

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela infra_log |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_infra_navegador

Sequence da tabela infra_navegador

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela infra_navegador |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_item_etapa

Sequence da tabela item_etapa

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela item_etapa |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_lembrete

Sequence da tabela lembrete

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela lembrete |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_lixeira

Sequence da tabela lixeira

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela lixeira |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_localizador

Sequence da tabela localizador

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela localizador |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_lugar_localizador

Sequence da tabela lugar_localizador

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela lugar_localizador |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_marcador

Sequence da tabela marcador

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela marcador |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_modelo

Sequence da tabela modelo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela modelo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_monitoramento_servico

Sequence da tabela monitoramento_servico

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela monitoramento_servico |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_nivel_acesso_permitido

Sequence da tabela nivel_acesso_permitido

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela nivel_acesso_permitido |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_notificacao

Sequence da tabela notificacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela notificacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_novidade

Sequence da tabela novidade

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela novidade |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_numeracao

Sequence da tabela numeracao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela numeracao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_observacao

Sequence da tabela observacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela observacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_operacao_servico

Sequence da tabela operacao_servico

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela operacao_servico |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_ordenador_despesa

Sequence da tabela ordenador_despesa

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela ordenador_despesa |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_orgao_historico

Sequence da tabela orgao_historico

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela orgao_historico |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_pais

Sequence da tabela pais

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela pais |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_participante

Sequence da tabela participante

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela participante |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_pesquisa

Sequence da tabela pesquisa

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela pesquisa |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_plano_trabalho

Sequence da tabela plano_trabalho

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela plano_trabalho |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_protocolo

Sequence da tabela protocolo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela protocolo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_protocolo_modelo

Sequence da tabela protocolo_modelo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela protocolo_modelo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_publicacao

Sequence da tabela publicacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela publicacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_reabertura_programada

Sequence da tabela reabertura_programada

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela reabertura_programada |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_rel_protocolo_protocolo

Sequence da tabela rel_protocolo_protocolo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela rel_protocolo_protocolo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_rel_unidade_tipo_contato

Sequence da tabela rel_unidade_tipo_contato

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela rel_unidade_tipo_contato |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_retorno_programado

Sequence da tabela retorno_programado

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela retorno_programado |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_revisao_avaliacao

Sequence da tabela revisao_avaliacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela revisao_avaliacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_secao_documento

Sequence da tabela secao_documento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela secao_documento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_secao_imprensa_nacional

Sequence da tabela secao_imprensa_nacional

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela secao_imprensa_nacional |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_secao_modelo

Sequence da tabela secao_modelo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela secao_modelo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_serie

Sequence da tabela serie

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela serie |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_serie_publicacao

Sequence da tabela serie_publicacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela serie_publicacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_serie_restricao

Sequence da tabela serie_restricao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela serie_restricao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_servico

Sequence da tabela servico

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela servico |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_situacao

Sequence da tabela situacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela situacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tabela_assuntos

Sequence da tabela tabela_assuntos

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tabela_assuntos |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tarefa

Sequence da tabela tarefa

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tarefa |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tarja_assinatura

Sequence da tabela tarja_assinatura

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tarja_assinatura |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_termo_uso

Sequence da tabela termo_uso

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela termo_uso |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_texto_padrao_interno

Sequence da tabela texto_padrao_interno

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela texto_padrao_interno |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_conferencia

Sequence da tabela tipo_conferencia

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_conferencia |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_contato

Sequence da tabela tipo_contato

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_contato |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_formulario

Sequence da tabela tipo_formulario

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_formulario |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_localizador

Sequence da tabela tipo_localizador

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_localizador |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_prioridade

Sequence da tabela tipo_prioridade

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_prioridade |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_proced_restricao

Sequence da tabela tipo_proced_restricao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_proced_restricao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_procedimento

Sequence da tabela tipo_procedimento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_procedimento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tipo_suporte

Sequence da tabela tipo_suporte

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tipo_suporte |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_titulo

Sequence da tabela titulo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela titulo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_tratamento

Sequence da tabela tratamento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela tratamento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_uf

Sequence da tabela uf

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela uf |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_unidade_historico

Sequence da tabela unidade_historico

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela unidade_historico |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_unidade_publicacao

Sequence da tabela unidade_publicacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela unidade_publicacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_upload

Sequence da tabela upload

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela upload |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_veiculo_imprensa_nacional

Sequence da tabela veiculo_imprensa_nacional

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela veiculo_imprensa_nacional |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_veiculo_publicacao

Sequence da tabela veiculo_publicacao

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela veiculo_publicacao |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_versao_secao_documento

Sequence da tabela versao_secao_documento

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela versao_secao_documento |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## seq_vocativo

Sequence da tabela vocativo

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o sequencial da tabela vocativo |
| campo | Armazena a variável da tabela em que a sequence é aplicada |

## serie

Administração dos Tipos de Documento

| Coluna | Descrição |
|---|---|
| id_serie | Número ID que identifica o Tipo de Documento |
| descricao | Armazena a descrição textual da série |
| id_grupo_serie | Número identificador que faz referência para a tabela grupo_serie sobre o Grupo de Tipo de Documento associado. |
| id_modelo | Número ID que identifica o modelo do Tipo de Documento. |
| id_modelo_edoc | Número ID que identifica o Tipo de Documento do modelo edoc. |
| id_tipo_formulario | Número ID que identifica o tipo de formulário usado no Tipo de Documento. |
| nome | Armazena o nome do Tipo de Documento |
| sin_assinatura_publicacao | Variável categórica que indica se o Tipo de Documento possui assinatura de publicação:<br><br><ul><li>S = Possui assinatura de publicação</li><li>N = Não possui assinatura de publicação</li></ul> |
| sin_ativo | Variável categórica que indica se o Tipo de Documento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_destinatario | Variável categórica que indica se o Tipo de Documento possui destinatário:<br><br><ul><li>S = Possui destinatário</li><li>N = Não possui destinatário</li></ul> |
| sin_interessado | Variável categórica que indica se o Tipo de Documento possui interessado:<br><br><ul><li>S = Possui interessado</li><li>N = Não possui interessado</li></ul> |
| sin_interno | Variável categórica que indica se o Tipo de Documento é interna:<br><br><ul><li>S = Interna</li><li>N = Não interna</li></ul> |
| sin_usuario_externo | Variável categórica que indica se é permitida a inclusão de documento deste tipo por usuário externo:<br><br><ul><li>S = Permitida</li><li>N = Não permitida</li></ul> |
| sin_valor_monetario | Variável categórica que indica se o tipo de documento (série) admite valor monetário:<br><br><ul><li>S = Admite valor monetário</li><li>N = Não admite valor monetário</li></ul> |
| sta_aplicabilidade | Status multi-valorado que identifica o Tipo de aplicabilidade do Tipo de Documento:<br><br><ul><li>E = Externo</li><li>I = Interno</li><li>T = Interno e Externo</li><li>F = Formulário</li></ul> |
| sta_numeracao | Status multi-valorado que identifica o Tipo de numeração do Tipo de Documento:<br><br><ul><li>1 = Sequencial Unidade</li><li>2 = Sequencial Órgão</li><li>3 = Sequencial Anual Unidade</li><li>4 = Sequencial Anual Órgão</li><li>I = Informada</li><li>S = Sem Numeração</li></ul> |

## serie_escolha

Armazena os Tipos de Documentos já utilizados por cada Unidade

| Coluna | Descrição |
|---|---|
| id_serie | Número ID que identifica o Tipo de Documento de uso restrito por Unidades específicas. |
| id_unidade | Número ID que identifica a unidade que pode usar o Tipo de Documento. |

## serie_publicacao

Associativa entre o tipo de documento e o veículo de publicação

| Coluna | Descrição |
|---|---|
| id_serie_publicacao | Número ID que identifica o Tipo de Documento de publicação. |
| id_orgao | Número ID que identifica o órgão do Tipo de Documento de publicação. |
| id_serie | Número ID que identifica o Tipo de Documento. |

## serie_restricao

Armazena os Tipos de Documentos com Restrição de Uso para determinadas Unidades parametrizados no Tipo de Documento pela Administração

| Coluna | Descrição |
|---|---|
| id_serie_restricao | Número ID que identifica a restrição de Tipo de Documento. |
| id_orgao | Número ID que identifica o órgão relacionado à restrição de uso do Tipo de Documento. |
| id_serie | Número ID que identifica o Tipo de Documento com restrição de uso. |
| id_unidade | Número ID que identifica da unidade relacionada à restrição de uso do Tipo de Documento. |

## servico

Administração dos serviços de integração do SEI

| Coluna | Descrição |
|---|---|
| id_servico | Número ID que identifica o serviço. |
| chave_acesso | Chave de acesso que libera a execução do serviço |
| crc | Armazena o códido CRC quando o serviço é acesso por meio de uma chave de acesso. OBS: A verificação cíclica de redundância (do inglês, CRC - Cyclic Redundancy Check) é um método de detecção de erros normalmente usada em redes digitais e dispositivos de armazenamento para detectar mudança acidental em cadeias de dados. |
| descricao | Armazena a descrição textual do serviço |
| id_usuario | Número ID que identifica o usuário (nesse contexo, geralmente o usuário é o cadastro de um sistema) |
| identificacao | Armazena a identificação textual do serviço |
| servidor | Armazena os servidores que consomem o serviço |
| sin_ativo | Variável categórica que indica se o serviço está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_chave_acesso | Variável categórica que indica se o uso de autenticação por chave de acesso está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_link_externo | Variável categórica que indica se o serviço possui link externo:<br><br><ul><li>S = Possui link externo</li><li>N = Não possui link externo</li></ul> |
| sin_servidor | Variável categórica que indica se o uso de servidores está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## sinalizacao_federacao

Armazena os dados de ação de sinalização no Sei Federação

| Coluna | Descrição |
|---|---|
| dth_sinalizacao | Data correspondente ao momento da aplicação da sinalização |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão no Sei Federação |
| id_protocolo_federacao | Número ID que identifica o número do processo ou documento compartilhado no Sei Federação. |
| id_unidade | Número ID que identifica a Unidade Interna do órgão no Sei Federação |
| sta_sinalizacao | Status multi-valorado que identifica o Tipo de sinalização:<br><br><ul><li>0 = Nenhuma</li><li>1 = Atenção</li><li>2 = Publicação</li><li>4 = envio</li><li>8 = Cancelamento</li></ul> |

## situacao

Armazena as parametrizações pela Administração dos Pontos de Controles a serem utilizados pelas Unidades indicadas na marcação de Situações dos Processos

| Coluna | Descrição |
|---|---|
| id_situacao | Número ID que identifica a situação (Ponto de Controle). |
| descricao | Armazena a descrição textual da situação (Ponto de Controle) |
| nome | Armazena o nome da situação (Ponto de Controle) |
| sin_ativo | Variável categórica que indica se a situação (Ponto de Controle) está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## solicitacao_ouvidoria

Registra o atendimento de solicitações da ouvidoria vinculadas a um processo

| Coluna | Descrição |
|---|---|
| id_atividade_atendimento | Número ID que identifica a atividade de atendimento da solicitação de ouvidoria. |
| id_documento | Número ID que identifica o documento de resposta da solicitação de ouvidoria. |
| id_procedimento | Número ID que identifica o processo da solicitação de ouvidoria. |
| id_unidade_atendimento | Número ID que identifica a unidade responsável pelo atendimento da solicitação de ouvidoria. |
| idx_solicitacao | Registro idx de indexação de informações e facilitação da pesquisa da tabela solicitacao_ouvidoria. |
| observacao | Armazena a observação registrada sobre a solicitação de ouvidoria. |
| sin_anonimo | Variável categórica que indica se a solicitação de ouvidoria é anônima:<br><br><ul><li>S = Anônima</li><li>N = Não anônima</li></ul> |
| sin_bloqueio | Variável categórica que indica se a solicitação de ouvidoria está bloqueada:<br><br><ul><li>S = Bloqueada</li><li>N = Não bloqueada</li></ul> |
| sin_manual | Variável categórica que indica se a solicitação de ouvidoria foi cadastrada manualmente:<br><br><ul><li>S = Cadastrada manualmente</li><li>N = Não cadastrada manualmente</li></ul> |
| sin_sigilo | Variável categórica que indica se a solicitação de ouvidoria é sigilosa:<br><br><ul><li>S = Sigilosa</li><li>N = Não sigilosa</li></ul> |
| sta_atendimento | Status multi-valorado que identifica a situação do atendimento da solicitação de ouvidoria:<br><br>S = Sim<br>N = Não<br>P = Parcial<br>- = Não informado. |

## tabela_assuntos

Administração das tabela de assuntos

| Coluna | Descrição |
|---|---|
| id_tabela_assuntos | Número id que ordena e identifica as tabelas de assuntos cadastradas |
| descricao | Detalhamento da Tabela Assunto |
| nome | Nome da Tabela assuntos |
| sin_atual | Variável categórica que indica se a tabela de assunto é a tabela atualmente em uso - Sim:<br><br><ul><li>S = A tabela atualmente em uso - Sim</li><li>N = Não a tabela atualmente em uso - Sim</li></ul> |

## tarefa

Administração dos tipos de Tarefas que são lançados nos Andamentos dos Processos

| Coluna | Descrição |
|---|---|
| id_tarefa | Número ID que identifica a tarefa. |
| id_tarefa_modulo | Identificação do módulo quando a tarefa é gerada por um módulo do SEI a parte. |
| nome | Armazena o nome da tarefa |
| sin_consulta_processual | Variável categórica que indica se a tarefa é exibida na consulta processual:<br><br><ul><li>S = Exibida na consulta processual</li><li>N = Não exibida na consulta processual</li></ul> |
| sin_fechar_andamentos_abertos | Variável categórica que indica se a tarefa fecha os andamentos abertos:<br><br><ul><li>S = Fecha os andamentos abertos</li><li>N = Não fecha os andamentos abertos</li></ul> |
| sin_historico_completo | Variável categórica que indica se a tarefa possui histórico complementar:<br><br><ul><li>S = Possui histórico complementar</li><li>N = Não possui histórico complementar</li></ul> |
| sin_historico_resumido | Variável categórica que indica se a tarefa possui histórico resumido:<br><br><ul><li>S = Possui histórico resumido</li><li>N = Não possui histórico resumido</li></ul><br>Esta variável estará preenchida com o valor igual a 'S' apenas se a variável sin_historico_completo for igual a 'S' |
| sin_lancar_andamento_fechado | Variável categórica que indica se a tarefa lança andamento fechado:<br><br><ul><li>S = Lança andamento fechado</li><li>N = Não lança andamento fechado</li></ul> |
| sin_permite_processo_fechado | Variável categórica que indica se a tarefa permite processo fechado:<br><br><ul><li>S = Permite processo fechado</li><li>N = Não permite processo fechado</li></ul> |

## tarefa_instalacao

Administração das tarefas de instalação no Sei Federação

| Coluna | Descrição |
|---|---|
| id_tarefa_instalacao | Número ID que identifica a tarefa associada à instalação |
| nome | Descrição da tarefa de instalação |

## tarefa_plano_trabalho

Administração das tarefas que podem ser associadas a um andamento de plano de trabalho

| Coluna | Descrição |
|---|---|
| id_tarefa_plano_trabalho | Número ID que identifica a tarefa do plano de trabalho. |
| nome | Armazena o nome da tarefa do plano de trabalho. |

## tarja_assinatura

Administração das Tarjas para Assinatura

| Coluna | Descrição |
|---|---|
| id_tarja_assinatura | Número ID que identifica a tarja da assinatura. |
| logo | Armazena a o logo no formato alfanumérico da tarja da assinatura Este campo não terá valor quando o campo sta_tarja_assinatura for igual a 'V' |
| sin_ativo | Variável categórica que indica se a tarja da assinatura está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sta_tarja_assinatura | Status multi-valorado que identifica o Tipo de forma de autenticação:<br><br><ul><li>C = Assinuatura Certificado digital</li><li>S = Assinatura Senha</li><li>A = Autenticação certificado digital</li><li>H = Autenticação senha</li><li>V = Instruções validação</li></ul> |
| texto | Armazena a descrição textual da tarja da assinatura |

## termo_uso

Administração dos termos de uso apresentados aos usuários do sistema

| Coluna | Descrição |
|---|---|
| id_termo_uso | Número ID que identifica o termo de uso. |
| conteudo | Armazena o conteúdo do termo de uso. |
| descricao | Armazena a descrição do termo de uso. |
| dth_final | Data/hora final de vigência do termo de uso. |
| dth_inicial | Data/hora inicial de vigência do termo de uso. |
| id_unidade | Número ID que identifica a unidade do usuário que aceitou o termo de uso. |
| id_usuario | Número ID que identifica o usuário que aceitou o termo de uso. |
| identificacao | Armazena a identificação do termo de uso. |
| sin_bloqueado | Variável categórica que indica se o termo de uso está bloqueado:<br><br><ul><li>S = Bloqueado</li><li>N = Não bloqueado</li></ul> |
| sin_liberado | Variável categórica que indica se o termo de uso está liberado:<br><br><ul><li>S = Liberado</li><li>N = Não liberado</li></ul> |

## texto_padrao_interno

Armazena as parametrizações pelas Unidades dos Textos Padrão

| Coluna | Descrição |
|---|---|
| id_texto_padrao_interno | Número ID que identifica o texto padrão interno. |
| conteudo | Armazena o conteúdo textual do texto padrão interno |
| descricao | Armazena a descrição textual do texto padrão interno |
| id_conjunto_estilos | Número ID que identifica o conjunto de estilos do texto padrão interno. |
| id_unidade | Número ID que identifica a unidade do texto padrão interno. |
| nome | Armazena o nome do texto padrão interno. |

## tipo_conferencia

Administração dos Tipos de Conferência

| Coluna | Descrição |
|---|---|
| id_tipo_conferencia | Número ID que identifica o tipo de conferência. |
| descricao | Armazena a descrição textual do tipo de conferência utilizada em documentos externos digitalizados. |
| sin_ativo | Variável categórica que indica se o tipo de conferencia está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## tipo_contato

Administração dos Tipos de Contatos

| Coluna | Descrição |
|---|---|
| id_tipo_contato | Número ID que identifica o tipo de contato. |
| descricao | Armazena a descrição textual do tipo de contato. |
| nome | Armazena o nome do tipo de contato |
| sin_ativo | Variável categórica que indica se tipo de contato está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_sistema | Variável categórica que indica se tipo de contato é de sistema:<br><br><ul><li>S = De sistema</li><li>N = Não é de sistema</li></ul><br>Os tipos de usuários de sistema são 'Usuários ANATEL', 'Sistemas', 'Unidades Anatel', 'Usuários Externos Anatel' e 'Órgãos do Sistema' |
| sta_acesso | Status multi-valorado que identifica o Tipo de acesso:<br><br><ul><li>C = Consulta Completa</li><li>R = Consulta Resumida</li><li>A = Alteração</li><li>N = Nenhum</li></ul> |

## tipo_formulario

Administração dos Tipos de Formulários

| Coluna | Descrição |
|---|---|
| id_tipo_formulario | Número ID que identifica o tipo de formuário. |
| descricao | Armazena a descrição do tipo de formulário |
| nome | Armazena o nome do tipo de formulário |
| sin_ativo | Variável categórica que indica se tipo de formulário está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## tipo_localizador

Armazena as parametrizações pela Unidade de Arquivamento dos Tipos de Localizadores físicos para sua adequada localização e identificação

| Coluna | Descrição |
|---|---|
| id_tipo_localizador | Número ID que identifica o tipo de localizador. |
| descricao | Armazena a descrição do tipo de localizador |
| id_unidade | Número ID que identifica a unidade do tipo de localizador. |
| nome | Armazena o nome do tipo de localizador. |
| sigla | Armazena a sigla do tipo localizador. |
| sin_ativo | Variável categórica que indica se o tipo de localizador está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## tipo_prioridade

Administração dos tipos de prioridade de tramitação de processos

| Coluna | Descrição |
|---|---|
| id_tipo_prioridade | Número ID que identifica o tipo de prioridade. |
| descricao | Armazena a descrição do tipo de prioridade. |
| nome | Armazena o nome do tipo de prioridade. |
| sin_ativo | Variável categórica que indica se o tipo de prioridade está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## tipo_proced_restricao

Tabela auxiliar da administração de Tipo de Processo que relaciona as unidades onde os processos podem ser abertos

| Coluna | Descrição |
|---|---|
| id_tipo_proced_restricao | Número ID que identifica o tipo do procedimento de restrição. |
| id_orgao | Número ID que identifica o órgão da unidade |
| id_tipo_procedimento | Número ID que identifica o tipo do processo |
| id_unidade | Número ID que identifica a unidade onde o respectivo tipo de processo pode ser aberto |

## tipo_procedimento

Administração dos Tipos de Processos

| Coluna | Descrição |
|---|---|
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |
| descricao | Armazena a descrição do tipo de processo |
| id_hipotese_legal_sugestao | Número ID que identifica a hipótese legal de sugestão do tipo de processo. |
| id_plano_trabalho | Número ID que identifica o plano de trabalho padrão do tipo de procedimento. |
| nome | Armazena o nome do tipo de processo. |
| sin_ativo | Variável categórica que indica se o tipo de processo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_individual | Variável categórica que indica se o tipo de processo é individual:<br><br><ul><li>S = Individual</li><li>N = Não individual</li></ul> |
| sin_interno | Variável categórica que indica se o processo é interno:<br><br><ul><li>S = Interno</li><li>N = Não interno</li></ul> |
| sin_ouvidoria | Variável categórica que indica se o processo é de ouvidoria:<br><br><ul><li>S = De ouvidoria</li><li>N = Não de ouvidoria</li></ul> |
| sin_ouvidoria_anonimo | Variável categórica que indica se o tipo de procedimento admite solicitação de ouvidoria anônima:<br><br><ul><li>S = Admite solicitação de ouvidoria anônima</li><li>N = Não admite solicitação de ouvidoria anônima</li></ul> |
| sta_grau_sigilo_sugestao | Status multi-valorado que identifica o Tipo de grau de sigilo de sugestão:<br><br><ul><li>U = Ultrasecreto</li><li>S = Secreto</li><li>R = Reservado</li></ul> |
| sta_nivel_acesso_sugestao | Status multi-valorado que identifica o Tipo de nível de acesso de sugestão:<br><br><ul><li>0 = Público</li><li>1 = Restrito</li><li>2 = Sigiloso</li></ul><br>Este campo está recebendo o valor igual a '1' quando o campo id_hipotese_legal_sugestao for igual a 31, 34 ou 42<br>Recebe valor igual a '2' quando a variável id_hipotese_legal_sugestao for igual a 44 |

## tipo_procedimento_escolha

Associativa entre tipo de documento e unidade organizacional

| Coluna | Descrição |
|---|---|
| id_tipo_procedimento | Número ID que identifica o tipo de processo da escolha. |
| id_unidade | Número ID que identifica a unidade do tipo de processo da escolha. |

## tipo_suporte

Armazena as parametrizações pela Unidade de Arquivamento dos Tipos de Suporte meio do documento físico a ser arquivado

| Coluna | Descrição |
|---|---|
| id_tipo_suporte | Número ID que identifica o tipo de suporte. |
| nome | Armazena o nome do tipo de suporte |
| sin_ativo | Variável categórica que indica se o tipo de suporte está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## titulo

Administração dos Títulos para associar a Cargo de Contato

| Coluna | Descrição |
|---|---|
| id_titulo | Número ID que identifica o Título para associar ao Cargo de Contato |
| abreviatura | Abreviação do Título |
| expressao | Nome do Título |
| sin_ativo | Variável categórica que indica se o Título está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## tratamento

Administração dos Pronomes de Tratamento para uso nos Contatos

| Coluna | Descrição |
|---|---|
| id_tratamento | Número ID que identifica o tratamento. |
| expressao | Armazena a descrição textutal da expressão de tratamento |
| sin_ativo | Variável categórica que indica se o tratamento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## uf

Administração das Unidades da Federação para uso nos Contatos

| Coluna | Descrição |
|---|---|
| id_uf | Número ID que identifica a uf |
| codigo_ibge | Identificador único do código de IBGE |
| id_pais | Número ID que identifica o país |
| nome | Armazena o nome uf |
| sigla | Armazena a sigla uf |

## unidade

Administração dos dados complementares do cadastro das Unidades

| Coluna | Descrição |
|---|---|
| id_unidade | Número ID que identifica a unidade. |
| codigo_sei | Identificador único do código do SEI |
| descricao | Descrição da unidade. |
| id_contato | Número ID que identifica o contato (OBS: as unidades são cadastradas como um contato, nesse sentido, elas possuem um número id_contato). |
| id_orgao | Número ID que identifica o órgão. |
| id_origem | Número ID que identifica a origem da unidade |
| id_unidade_federacao | Número ID que identifica a Unidade Interna do órgão no Sei Federação |
| idx_unidade | Registro idx de indexação de informações e facilitação da pesquisa da tabela unidade. Formados pelos campos sigla e descricao. |
| sigla | Armazena a sigla da unidade |
| sin_arquivamento | Variável categórica que indica se a unidade é de arquivamento:<br><br><ul><li>S = De arquivamento</li><li>N = Não de arquivamento</li></ul> |
| sin_ativo | Variável categórica que indica se a unidade está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_envio_processo | Variável categórica que indica se a unidade possui envio de processo:<br><br><ul><li>S = Possui envio de processo</li><li>N = Não possui envio de processo</li></ul> |
| sin_mail_pendencia | Variável categórica que indica se a unidade possui email de pendência:<br><br><ul><li>S = Possui email de pendência</li><li>N = Não possui email de pendência</li></ul> |
| sin_ouvidoria | Variável categórica que indica se a unidade é de ouvidoria:<br><br><ul><li>S = De ouvidoria</li><li>N = Não de ouvidoria</li></ul> |
| sin_protocolo | Variável categórica que indica se é de protocolo:<br><br><ul><li>S = De protocolo</li><li>N = Não de protocolo</li></ul> |

## unidade_federacao

Administração das Unidades Internas dos órgãos no Sei Federação

| Coluna | Descrição |
|---|---|
| id_unidade_federacao | Número ID que identifica a Unidade Interna do órgão no Sei Federação |
| descricao | Descrição que identifica a Unidade no Sei Federação |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão associada à Unidade |
| sigla | Sigla que identifica a Unidade no Sei Federação |

## unidade_historico

Armaneza as modificações ocorridas no registro das unidades

| Coluna | Descrição |
|---|---|
| id_unidade_historico | Número ID que identifica a unidade por ordem de criação. |
| descricao | Descrição da unidade. |
| dta_fim | Data de desativação da unidade |
| dta_inicio | Data de cadastro da unidade |
| id_orgao | Número ID que identifica o órgão. |
| id_unidade | Número ID que identifica a origem da unidade |
| sigla | Armazena a sigla da unidade |

## unidade_publicacao

Associativa entre a unidade organizacional e as publicações

| Coluna | Descrição |
|---|---|
| id_unidade_publicacao | Número ID que identifica a unidade da publicação |
| id_unidade | Número ID que identifica a unidade. |

## usuario

Administração do Cadastro dos usuários

| Coluna | Descrição |
|---|---|
| id_usuario | Número ID que identifica o usuário. |
| dth_politica_privacidade | Data/hora de aceite da política de privacidade pelo usuário. |
| dth_termo_uso | Data/hora de aceite do termo de uso pelo usuário. |
| id_contato | Número ID que identifica o contato do usuário. |
| id_orgao | Número ID que identifica o órgão do usuário. |
| id_origem | Número ID que identifica a origem do usuário |
| id_usuario_federacao | Número ID que identifica o usuário do órgão associado no Sei Federação |
| idx_usuario | Registro idx de indexação de informações e facilitação da pesquisa da tabela usuário. Formado pelos campos sigla e nome. |
| nome | Armazena o nome do usuário |
| nome_registro_civil | Armazena o nome civil do usuário |
| nome_social | Armazena o nome social do usuário |
| senha | Armazena o hash da senha do usuário Este campo não terá valor quando o campo sta_tipo for igual a '0' e '1' |
| sigla | Armazena a sigla do usuário |
| sin_ativo | Variável categórica que indica se o usuário está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_gov_br | Variável categórica que indica se o usuário está vinculado à conta gov.br:<br><br><ul><li>S = Vinculado à conta gov.br</li><li>N = Não vinculado à conta gov.br</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo de usuário:<br><br><ul><li>0 = Usuário Interno oriundo do SIP</li><li>1 = Usuário de Sistema Integrado</li><li>2 = Usuário Externo com Cadastro Pendente de Liberação</li><li>3 = Usuário Externo com Cadastro Liberado</li></ul> |

## usuario_configuracao

Armazena as configurações de preferências pessoais do usuário

| Coluna | Descrição |
|---|---|
| botoes_controle | Armazena a configuração dos botões de controle exibidos para o usuário. |
| botoes_documento | Armazena a configuração dos botões de documento exibidos para o usuário. |
| botoes_processo | Armazena a configuração dos botões de processo exibidos para o usuário. |
| detalhe_controle | Armazena o detalhamento da configuração de controle do usuário. |
| dth_cadastro | Data/hora de cadastro da configuração do usuário. |
| id_usuario | Número ID que identifica o usuário. |
| pagina_inicial | Armazena a página inicial configurada pelo usuário. |
| sin_filtrar_botoes | Variável categórica que indica se o usuário optou por filtrar os botões exibidos:<br><br><ul><li>S = Optou por filtrar os botões exibidos</li><li>N = Não optou por filtrar os botões exibidos</li></ul> |
| sta_tipo_controle | Status multi-valorado que identifica o tipo de controle configurado pelo usuário:<br><br>R = Resumida<br>D = Detalhada. |

## usuario_federacao

Administração dos usuários do órgão associado no Sei Federação

| Coluna | Descrição |
|---|---|
| id_usuario_federacao | Número ID que identifica o usuário do órgão associado no Sei Federação |
| id_instalacao_federacao | Número ID que identifica a instalação do órgão associada ao Usuário |
| nome | Nome que identifica o Usuário no Sei Federação |
| sigla | Sigla que identifica o Usuário no Sei Federação |

## usuario_login

Registra as tentativas de login do usuário, usadas no controle de bloqueio por tentativas malsucedidas

| Coluna | Descrição |
|---|---|
| dth_tentativa | Data/hora da última tentativa de login do usuário. |
| http_client_ip | Armazena o endereço IP informado no cabeçalho HTTP_CLIENT_IP da tentativa de login. |
| http_x_forwarded_for | Armazena o endereço IP informado no cabeçalho HTTP_X_FORWARDED_FOR da tentativa de login. |
| id_usuario | Número ID que identifica o usuário. |
| remote_addr | Armazena o endereço IP de origem (REMOTE_ADDR) da tentativa de login. |
| tentativas | Armazena a quantidade de tentativas de login malsucedidas do usuário. |
| user_agent | Armazena o user agent do navegador utilizado na tentativa de login. |

## veiculo_imprensa_nacional

Administração dos veículos da imprensa nacional

| Coluna | Descrição |
|---|---|
| id_veiculo_imprensa_nacional | Número ID que identifica o veiculo da imprensa nacional. |
| descricao | Armazena a descrição textual do veículo de imprensa nacional |
| sigla | Armazena a sigla do veiculo da imprensa nacional |

## veiculo_publicacao

Administração dos veículos oficiais de publicação

| Coluna | Descrição |
|---|---|
| id_veiculo_publicacao | Número ID que identifica o veiculo de publicação. |
| descricao | Armazena a descrição textual do veículo de publicação |
| nome | Armazena o nome do veiculo de publicação |
| sin_ativo | Variável categórica que indica se o veiculo de publicação está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_exibir_pesquisa_interna | Variável categórica que indica se o veículo de publicação exibe pesquisa interna:<br><br><ul><li>S = Exibe pesquisa interna</li><li>N = Não exibe pesquisa interna</li></ul> |
| sin_fonte_feriados | Variável categórica que indica se veiculo de publicação atua em feriados:<br><br><ul><li>S = Atua em feriados</li><li>N = Não atua em feriados</li></ul> |
| sin_permite_extraordinaria | Variável categórica que indica se veiculo de publicação permite publicação extraordinária:<br><br><ul><li>S = Permite publicação extraordinária</li><li>N = Não permite publicação extraordinária</li></ul> |
| sta_tipo | Status multi-valorado que identifica o Tipo:<br><br><ul><li>I = Interno</li><li>E = Externo</li></ul> |
| web_service | Armazena os dados de webservice do veículo de publicação |

## versao_secao_documento

Armazena as Versões de cada Seção dos Documentos produzidos

| Coluna | Descrição |
|---|---|
| id_versao_secao_documento | Número ID que identifica a versão da seção do documento. |
| conteudo | Armazena o conteúdo da versão da seção do documento |
| dth_atualizacao | Data/hora da atualização da versão da seção do documento |
| id_secao_documento | Número ID que identifica a seção do documento. |
| id_unidade | Número ID que identifica a unidade onde foi criada a versão. |
| id_usuario | Número ID que identifica o usuário que criou a versão do documento. |
| sin_ultima | Variável categórica que indica se é a última versão criada:<br><br><ul><li>S = A última versão criada</li><li>N = Não a última versão criada</li></ul> |
| versao | Armazena o número da versão da seção do documento |

## vocativo

Administração dos Vocativos para uso nos Contatos

| Coluna | Descrição |
|---|---|
| id_vocativo | Número ID que identifica o vocativo. |
| expressao | Armazena o texto da expressão de tratamento para o vocativo usado nos Contatos |
| sin_ativo | Variável categórica que indica se o vocativo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
