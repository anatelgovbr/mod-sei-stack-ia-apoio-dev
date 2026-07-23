# Dicionário de Dados do Módulo SEI IA - v1.5.0

## Índice de Tabelas

- [md_ia_adm_cfg_assi_ia_usu](#md_ia_adm_cfg_assi_ia_usu)
- [md_ia_adm_class_aut_tp](#md_ia_adm_class_aut_tp)
- [md_ia_adm_config_assist_ia](#md_ia_adm_config_assist_ia)
- [md_ia_adm_config_similar](#md_ia_adm_config_similar)
- [md_ia_adm_doc_relev](#md_ia_adm_doc_relev)
- [md_ia_adm_ext_permitida](#md_ia_adm_ext_permitida)
- [md_ia_adm_integ_funcion](#md_ia_adm_integ_funcion)
- [md_ia_adm_integracao](#md_ia_adm_integracao)
- [md_ia_adm_meta_ods](#md_ia_adm_meta_ods)
- [md_ia_adm_metadado](#md_ia_adm_metadado)
- [md_ia_adm_objetivo_ods](#md_ia_adm_objetivo_ods)
- [md_ia_adm_ods_onu](#md_ia_adm_ods_onu)
- [md_ia_adm_perc_relev_met](#md_ia_adm_perc_relev_met)
- [md_ia_adm_pesq_doc](#md_ia_adm_pesq_doc)
- [md_ia_adm_seg_doc_relev](#md_ia_adm_seg_doc_relev)
- [md_ia_adm_tp_doc_pesq](#md_ia_adm_tp_doc_pesq)
- [md_ia_adm_unidade_alerta](#md_ia_adm_unidade_alerta)
- [md_ia_adm_url_integracao](#md_ia_adm_url_integracao)
- [md_ia_class_meta_ods](#md_ia_class_meta_ods)
- [md_ia_doc_index_canc](#md_ia_doc_index_canc)
- [md_ia_doc_indexaveis](#md_ia_doc_indexaveis)
- [md_ia_galeria_prompts](#md_ia_galeria_prompts)
- [md_ia_grupo_galeria_prompt](#md_ia_grupo_galeria_prompt)
- [md_ia_grupo_prompts_fav](#md_ia_grupo_prompts_fav)
- [md_ia_hist_class](#md_ia_hist_class)
- [md_ia_interacao_arq_avulso](#md_ia_interacao_arq_avulso)
- [md_ia_interacao_chat](#md_ia_interacao_chat)
- [md_ia_ods_onu_nsa](#md_ia_ods_onu_nsa)
- [md_ia_proc_index_canc](#md_ia_proc_index_canc)
- [md_ia_proc_indexaveis](#md_ia_proc_indexaveis)
- [md_ia_prompts_favoritos](#md_ia_prompts_favoritos)
- [md_ia_topico_chat](#md_ia_topico_chat)

## md_ia_adm_cfg_assi_ia_usu

Associa a configuração do Assistente IA aos usuários que recebem limite diário maior de tokens.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_cfg_assi_ia_usu | Número ID que identifica a associação. |
| id_md_ia_adm_conf_assist_ia | Número ID que identifica a configuração do Assistente IA associada. |
| id_usuario | Número ID que identifica o usuário autorizado a consumir o limite maior. |

## md_ia_adm_class_aut_tp

Associa metas ODS a tipos de processo usados na classificação automática.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_class_aut_tp | Número ID que identifica a associação de classificação automática. |
| id_md_ia_adm_meta_ods | Número ID que identifica a meta ODS configurada para classificação automática. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo relacionado à meta. |

## md_ia_adm_config_assist_ia

Armazena a configuração geral do Assistente IA, seus limites, instruções e funcionalidades opcionais.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_conf_assist_ia | Número ID que identifica a configuração do Assistente IA. |
| limite_geral_tokens | Limite diário geral por usuário, expresso em milhões de tokens. |
| limite_maior_usuarios_tokens | Limite diário maior, em milhões de tokens, aplicável aos usuários selecionados. |
| orientacoes_gerais | Armazena o texto exibido nas orientações gerais do Assistente IA. |
| sin_buscar_web | Variável categórica que indica se a busca na web deve ser ativada:<br><br><ul><li>S = Deve ser ativada</li><li>N = Não deve ser ativada</li></ul> |
| sin_exibir_funcionalidade | Variável categórica que indica se o Assistente IA deve ser exibido:<br><br><ul><li>S = Deve ser exibido</li><li>N = Não deve ser exibido</li></ul> |
| sin_refletir | Variável categórica que indica se a função de reflexão do modelo deve ser ativada:<br><br><ul><li>S = Deve ser ativada</li><li>N = Não deve ser ativada</li></ul> |
| system_prompt | Armazena as instruções internas mínimas de comportamento enviadas ao modelo de linguagem. |

## md_ia_adm_config_similar

Armazena os parâmetros da funcionalidade de recomendação de processos similares.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_config_similar | Número ID que identifica a configuração de similaridade. |
| dth_alteracao | Data/hora da última alteração dos parâmetros de relevância. |
| orientacoes_gerais | Armazena as orientações exibidas na seção de processos similares. |
| perc_relev_cont_doc | Percentual de relevância atribuído ao conteúdo dos documentos. |
| perc_relev_metadados | Percentual de relevância atribuído aos metadados. |
| qtd_process_listagem | Quantidade de processos similares apresentada ao usuário. |
| sin_exibir_funcionalidade | Variável categórica que indica se a funcionalidade de processos similares deve ser exibida:<br><br><ul><li>S = Deve ser exibida</li><li>N = Não deve ser exibida</li></ul> |

## md_ia_adm_doc_relev

Registra tipos de documento considerados relevantes para processos similares e outras funcionalidades do SEI IA.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_doc_relev | Número ID que identifica a configuração de documento relevante. |
| aplicabilidade | Status multi-valorado que identifica o tipo de aplicabilidade:<br><br><ul><li>I = Interno</li><li>E = Externo</li></ul> |
| dth_alteracao | Data/hora da última alteração do registro. |
| id_serie | Número ID que identifica o tipo de documento relevante. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo específico; quando nulo, a configuração abrange todos os tipos. |
| sin_ativo | Variável categórica que indica se a configuração está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## md_ia_adm_ext_permitida

Armazena as regras de aceitação, tratamento e entrega das extensões de arquivo utilizadas pelo Assistente IA.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_ext_permitida | Número ID que identifica a regra da extensão. |
| desc_tratamento_avulso | Armazena a descrição do tratamento aplicado ao arquivo avulso. |
| desc_tratamento_protocolo | Armazena a descrição do tratamento aplicado quando a extensão é citada como protocolo de documento. |
| extensao | Armazena a extensão do arquivo, sem ponto. |
| forma_entrega_arquivo | Status multi-valorado que identifica a forma de entrega na citação de protocolo:<br><br><ul><li>0 = Feed do Solr</li><li>1 = Download do arquivo</li><li>2 = Feed do Solr e download do arquivo</li><li>3 = Citação não permitida como protocolo de documento</li></ul> |
| limite_considerar | Identificador do limite técnico adicional a considerar no tamanho máximo do arquivo. |
| sin_ativo | Variável categórica que indica se a regra está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_conteudo_vetorizavel | Variável categórica que indica se o conteúdo da extensão pode ser vetorizado:<br><br><ul><li>S = Pode ser vetorizado</li><li>N = Não pode ser vetorizado</li></ul> |
| sin_permitida_avulso | Variável categórica que indica se a extensão é aceita como arquivo avulso:<br><br><ul><li>S = Aceita como arquivo avulso</li><li>N = Não aceita como arquivo avulso</li></ul> |
| sin_permitida_protocolo | Variável categórica que indica se a extensão é aceita como protocolo de documento:<br><br><ul><li>S = Aceita como protocolo de documento</li><li>N = Não aceita como protocolo de documento</li></ul> |
| tamanho_maximo_permitido | Tamanho máximo permitido para arquivo avulso, em MB. |

## md_ia_adm_integ_funcion

Cataloga as funcionalidades atendidas pelas integrações do módulo.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_integ_funcion | Número ID que identifica a funcionalidade de integração. |
| nome | Armazena o nome da funcionalidade atendida. |

## md_ia_adm_integracao

Armazena o mapeamento e os parâmetros de autenticação e comunicação das integrações externas.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_integracao | Número ID que identifica a integração. |
| formato_resposta | Status multi-valorado que identifica o formato da resposta:<br><br><ul><li>1 = JSON</li><li>2 = XML</li></ul> |
| id_md_ia_adm_integ_funcion | Número ID que identifica a funcionalidade atendida pela integração. |
| metodo_autenticacao | Status multi-valorado que identifica o método de autenticação:<br><br><ul><li>1 = Sem autenticação</li><li>2 = Token no cabeçalho</li><li>3 = Token no corpo</li></ul> |
| metodo_requisicao | Status multi-valorado que identifica o método HTTP utilizado:<br><br><ul><li>1 = POST</li><li>2 = GET</li></ul> |
| nome | Armazena o nome da integração. |
| operacao_wsdl | Armazena a operação SOAP ou a URL-base do endpoint da integração. |
| sin_ativo | Variável categórica que indica se a integração está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| tipo_integracao | Status multi-valorado que identifica o tipo de integração:<br><br><ul><li>SI = Sem integração</li><li>RE = REST</li><li>SO = SOAP</li></ul> |
| token_autenticacao | Armazena o token utilizado pela integração quando o método de autenticação o exige. |
| url_wsdl | Armazena a URL da definição WSDL para integração SOAP. |
| versao_soap | Versão do protocolo SOAP utilizada pela integração. |

## md_ia_adm_meta_ods

Armazena as metas pertencentes a cada Objetivo de Desenvolvimento Sustentável.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_meta_ods | Número ID que identifica a meta ODS. |
| descricao_meta | Armazena a descrição da meta. |
| id_md_ia_adm_objetivo_ods | Número ID que identifica o objetivo ao qual a meta pertence. |
| identificacao_meta | Armazena o código textual da meta. |
| ordem | Número de ordem da meta dentro do objetivo. |
| sin_forte_relacao | Variável categórica que indica se a meta tem forte relação configurada:<br><br><ul><li>S = Tem forte relação configurada</li><li>N = Não tem forte relação configurada</li></ul> |

## md_ia_adm_metadado

Cataloga os tipos de metadado usados na ponderação da similaridade de processos.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_metadado | Número ID que identifica o tipo de metadado. |
| metadado | Armazena o nome do tipo de metadado. |

## md_ia_adm_objetivo_ods

Armazena os Objetivos de Desenvolvimento Sustentável apresentados pelo módulo.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_objetivo_ods | Número ID que identifica o objetivo. |
| descricao_ods | Armazena a descrição do objetivo. |
| icone_ods | Armazena o nome do arquivo de ícone usado para representar o objetivo. |
| id_md_ia_adm_ods_onu | Número ID que identifica a configuração geral de ODS à qual o objetivo pertence. |
| nome_ods | Armazena o nome do objetivo. |

## md_ia_adm_ods_onu

Armazena a configuração geral da funcionalidade de classificação por ODS.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_ods_onu | Número ID que identifica a configuração de ODS. |
| orientacoes_gerais | Armazena as orientações exibidas na funcionalidade de ODS. |
| sin_classificacao_externo | Variável categórica que indica se usuários externos podem classificar ODS:<br><br><ul><li>S = Podem classificar ODS</li><li>N = Não podem classificar ODS</li></ul> |
| sin_exibir_avaliacao | Variável categórica que indica se a avaliação especializada por racional deve ser exibida:<br><br><ul><li>S = Deve ser exibida</li><li>N = Não deve ser exibida</li></ul> |
| sin_exibir_funcionalidade | Variável categórica que indica se a funcionalidade de ODS deve ser exibida:<br><br><ul><li>S = Deve ser exibida</li><li>N = Não deve ser exibida</li></ul> |

## md_ia_adm_perc_relev_met

Armazena o percentual de relevância de cada metadado na configuração de similaridade.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_perc_relev_met | Número ID que identifica a ponderação do metadado. |
| dth_alteracao | Data/hora da última alteração do percentual. |
| id_md_ia_adm_config_similar | Número ID que identifica a configuração de similaridade. |
| id_md_ia_adm_metadado | Número ID que identifica o metadado ponderado. |
| percentual_relevancia | Percentual de participação do metadado na relevância dos metadados. |

## md_ia_adm_pesq_doc

Armazena a configuração geral da funcionalidade de pesquisa de documentos.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_pesq_doc | Número ID que identifica a configuração da pesquisa de documentos. |
| nome_secao | Armazena o nome da seção exibida ao usuário para a funcionalidade. |
| orientacoes_gerais | Armazena as orientações exibidas na seção de pesquisa de documentos. |
| qtd_process_listagem | Quantidade de documentos apresentada na lista de resultados. |
| sin_exibir_funcionalidade | Variável categórica que indica se a pesquisa de documentos deve ser exibida:<br><br><ul><li>S = Deve ser exibida</li><li>N = Não deve ser exibida</li></ul> |

## md_ia_adm_seg_doc_relev

Armazena segmentos e respectivos pesos dentro de um tipo de documento relevante.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_seg_doc_relev | Número ID que identifica a configuração do segmento. |
| id_md_ia_adm_doc_relev | Número ID que identifica o documento relevante ao qual o segmento pertence. |
| percentual_relevancia | Percentual de relevância atribuído ao segmento do documento. |
| segmento_documento | Armazena o nome ou a expressão usada para localizar o segmento no documento. |

## md_ia_adm_tp_doc_pesq

Associa a configuração da pesquisa aos tipos de documento definidos como alvos.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_tp_doc_pesq | Número ID que identifica a associação do tipo de documento. |
| dth_alteracao | Data/hora da última alteração da associação. |
| id_md_ia_adm_pesq_doc | Número ID que identifica a configuração da pesquisa de documentos. |
| id_serie | Número ID que identifica o tipo de documento alvo da pesquisa. |
| sin_ativo | Variável categórica que indica se o tipo de documento está ativo como alvo:<br><br><ul><li>S = Ativo como alvo</li><li>N = Não ativo como alvo</li></ul> |

## md_ia_adm_unidade_alerta

Associa unidades à configuração de ODS para apresentação de alerta de pendência de classificação.

| Coluna | Descrição |
|---|---|
| id_md_ia_adm_unidade_alerta | Número ID que identifica a associação da unidade de alerta. |
| dth_alteracao | Data/hora da última alteração da associação. |
| id_md_ia_adm_ods_onu | Número ID que identifica a configuração de ODS. |
| id_unidade | Número ID que identifica a unidade que receberá o alerta de pendência. |

## md_ia_adm_url_integracao

Armazena os caminhos de endpoint utilizados por cada integração do módulo.

| Coluna | Descrição |
|---|---|
| id_adm_url_integracao | Número ID que identifica o endpoint configurado. |
| id_md_ia_adm_integracao | Número ID que identifica a integração à qual o endpoint pertence. |
| label | Armazena o rótulo funcional do endpoint. |
| referencia | Armazena a chave interna usada pelo código para localizar o endpoint. |
| url | Armazena o caminho ou complemento de URL do endpoint. |

## md_ia_class_meta_ods

Registra a classificação ou sugestão vigente de uma meta ODS para um processo.

| Coluna | Descrição |
|---|---|
| id_md_ia_class_meta_ods | Número ID que identifica a classificação da meta. |
| dth_cadastro | Data/hora do registro da classificação ou sugestão. |
| id_md_ia_adm_meta_ods | Número ID que identifica a meta ODS classificada. |
| id_procedimento | Número ID que identifica o processo classificado. |
| id_unidade | Número ID que identifica a unidade associada à classificação. |
| id_usuario | Número ID que identifica o usuário ou usuário de sistema responsável pelo registro. |
| racional | Armazena a justificativa da classificação ou sugestão. |
| sin_sugestao_aceita | Variável categórica que indica, quando preenchida, se a sugestão foi aceita:<br><br><ul><li>S = Aceita</li><li>N = Não aceita</li></ul> |
| sta_tipo_usuario | Status multi-valorado que identifica a origem da classificação:<br><br><ul><li>A = Agendamento</li><li>E = Usuário Externo</li><li>I = Inteligência Artificial</li><li>U = Usuário Padrão</li></ul> |

## md_ia_doc_index_canc

Registra documentos pendentes de remoção da indexação externa.

| Coluna | Descrição |
|---|---|
| id_documento | Número ID que identifica o documento pendente de cancelamento da indexação. |

## md_ia_doc_indexaveis

Controla os documentos elegíveis para indexação e vetorização pelo Servidor de Soluções de IA.

| Coluna | Descrição |
|---|---|
| dth_alteracao | Data/hora da inclusão ou da última alteração que reiniciou o processamento. |
| dth_indexacao | Data/hora em que o documento foi marcado como indexado. |
| dth_vetorizacao | Data/hora em que o documento foi marcado como vetorizado. |
| hash | Armazena o hash de controle usado para detectar mudanças nos dados relevantes do documento. |
| id_documento | Número ID que identifica o documento. |
| sin_indexado | Variável categórica que indica se o documento já foi indexado:<br><br><ul><li>S = Indexado</li><li>N = Não indexado</li></ul> |
| sin_processo_aberto | Variável categórica que indica se o documento pertence a processo aberto:<br><br><ul><li>S = Pertence a processo aberto</li><li>N = Não pertence a processo aberto</li></ul> |
| sin_vetorizado | Variável categórica que indica se o documento já foi vetorizado:<br><br><ul><li>S = Vetorizado</li><li>N = Não vetorizado</li></ul> |

## md_ia_galeria_prompts

Armazena prompts publicados na galeria compartilhada do Assistente IA.

| Coluna | Descrição |
|---|---|
| id_md_ia_galeria_prompts | Número ID que identifica o prompt publicado. |
| descricao | Armazena a descrição do prompt apresentada na galeria. |
| dth_alteracao | Data/hora da publicação ou última alteração. |
| id_md_ia_grupo_galeria_prompt | Número ID que identifica o grupo temático da galeria. |
| id_unidade | Número ID que identifica a unidade do publicador. |
| id_usuario | Número ID que identifica o usuário publicador. |
| prompt | Armazena o texto integral do prompt publicado. |
| sin_ativo | Variável categórica que indica se o prompt está ativo na galeria:<br><br><ul><li>S = Ativo na galeria</li><li>N = Não ativo na galeria</li></ul> |

## md_ia_grupo_galeria_prompt

Cataloga os grupos temáticos usados para organizar a galeria de prompts.

| Coluna | Descrição |
|---|---|
| id_md_ia_grupo_galeria_prompt | Número ID que identifica o grupo da galeria. |
| nome_grupo | Armazena o nome do grupo temático. |

## md_ia_grupo_prompts_fav

Armazena grupos pessoais de prompts favoritos, vinculados ao usuário e à unidade.

| Coluna | Descrição |
|---|---|
| id_md_ia_grupo_prompts_fav | Número ID que identifica o grupo de favoritos. |
| id_unidade | Número ID que identifica a unidade em que o grupo foi criado. |
| id_usuario | Número ID que identifica o proprietário do grupo. |
| nome_grupo | Armazena o nome atribuído ao grupo de favoritos. |

## md_ia_hist_class

Registra o histórico das inclusões, exclusões, confirmações, recusas e alterações de classificações ODS.

| Coluna | Descrição |
|---|---|
| id_md_ia_hist_class | Número ID que identifica o evento histórico. |
| dth_cadastro | Data/hora em que o evento histórico foi registrado. |
| id_md_ia_adm_meta_ods | Número ID que identifica a meta ODS afetada. |
| id_md_ia_hist_class_sugest | Número ID que referencia o registro histórico da sugestão confirmada, recusada ou sobrescrita. |
| id_procedimento | Número ID que identifica o processo classificado. |
| id_unidade | Número ID que identifica a unidade associada ao evento. |
| id_usuario | Número ID que identifica o usuário ou usuário de sistema responsável pelo evento. |
| operacao | Status multi-valorado que identifica a operação registrada:<br><br><ul><li>I = Adicionado</li><li>D = Excluído</li><li>C = Sugestão Confirmada</li><li>N = Sugestão Não Confirmada</li><li>S = Sobrescrita de sugestão da IA</li><li>U = Atualização</li></ul> |
| racional | Armazena a justificativa associada ao evento histórico. |
| sin_sugestao_aceita | Variável categórica que indica, quando preenchida, se a sugestão foi aceita:<br><br><ul><li>S = Aceita</li><li>N = Não aceita</li></ul> |
| sta_tipo_usuario | Status multi-valorado que identifica a origem da classificação:<br><br><ul><li>A = Agendamento</li><li>E = Usuário Externo</li><li>I = Inteligência Artificial</li><li>U = Usuário Padrão</li></ul> |

## md_ia_interacao_arq_avulso

Registra os arquivos avulsos enviados em uma interação do Assistente IA.

| Coluna | Descrição |
|---|---|
| id_md_ia_interacao_arq_avulso | Número ID que identifica o arquivo avulso. |
| dth_inclusao | Data/hora em que o upload foi registrado. |
| id_md_ia_interacao_chat | Número ID que identifica a interação à qual o arquivo pertence. |
| nome_original | Armazena o nome original do arquivo enviado. |
| nome_temporario | Armazena o nome temporário usado para guardar o arquivo no servidor. |

## md_ia_interacao_chat

Registra as perguntas, respostas e metadados técnicos das interações com o Assistente IA.

| Coluna | Descrição |
|---|---|
| id_md_ia_interacao_chat | Número ID que identifica a interação. |
| dth_cadastro | Data/hora em que a pergunta foi registrada. |
| feedback | Avaliação numérica em estrelas atribuída à resposta. |
| id_md_ia_topico_chat | Número ID que identifica o tópico da conversa. |
| id_message | Identificador da mensagem devolvido pelo serviço de IA. |
| input_prompt | Armazena a representação JSON do contexto e dos dados enviados para processamento. |
| pergunta | Armazena o texto da pergunta do usuário. |
| resposta | Armazena o conteúdo da resposta recebida do serviço de IA. |
| status_requisicao | Código HTTP ou código de retorno da requisição ao serviço de IA. |
| tempo_execucao | Tempo medido para execução da chamada ao serviço de IA. |
| total_tokens | Total de tokens informado nos metadados de uso da resposta. |

## md_ia_ods_onu_nsa

Registra processos marcados como não aplicáveis à classificação ODS.

| Coluna | Descrição |
|---|---|
| dth_cadastro | Data/hora em que o processo foi marcado como não aplicável. |
| id_procedimento | Número ID que identifica o processo marcado como não aplicável. |
| id_unidade | Número ID que identifica a unidade responsável pela marcação. |
| id_usuario | Número ID que identifica o usuário responsável pela marcação. |

## md_ia_proc_index_canc

Registra processos pendentes de remoção da indexação externa.

| Coluna | Descrição |
|---|---|
| id_procedimento | Número ID que identifica o processo pendente de cancelamento da indexação. |

## md_ia_proc_indexaveis

Controla os processos elegíveis para indexação e os respectivos estados de processamento.

| Coluna | Descrição |
|---|---|
| dth_alteracao | Data/hora da inclusão ou da última alteração que reiniciou o processamento. |
| dth_indexacao | Data/hora em que o processo foi marcado como indexado. |
| dth_vetorizacao | Data/hora em que o processo foi marcado como vetorizado. |
| hash | Armazena o hash de controle usado para detectar alterações nos dados relevantes do processo. |
| id_procedimento | Número ID que identifica o processo. |
| sin_indexado | Variável categórica que indica se o processo já foi indexado:<br><br><ul><li>S = Indexado</li><li>N = Não indexado</li></ul> |
| sin_processo_aberto | Variável categórica que indica se o processo está aberto:<br><br><ul><li>S = Aberto</li><li>N = Não aberto</li></ul> |
| sin_vetorizado | Variável categórica que indica se o processo já foi vetorizado:<br><br><ul><li>S = Vetorizado</li><li>N = Não vetorizado</li></ul> |

## md_ia_prompts_favoritos

Armazena prompts salvos como favoritos dentro dos grupos pessoais do usuário.

| Coluna | Descrição |
|---|---|
| id_md_ia_prompts_favoritos | Número ID que identifica o prompt favorito. |
| descricao_prompt | Armazena a descrição atribuída ao prompt favorito. |
| dth_alteracao | Data/hora do cadastro ou última alteração do favorito. |
| id_md_ia_grupo_prompts_fav | Número ID que identifica o grupo pessoal ao qual o favorito pertence. |
| prompt | Armazena o texto integral do prompt favorito. |

## md_ia_topico_chat

Armazena os tópicos de conversa do Assistente IA por usuário e unidade.

| Coluna | Descrição |
|---|---|
| id_md_ia_topico_chat | Número ID que identifica o tópico de conversa. |
| dth_cadastro | Data/hora em que o tópico foi criado. |
| id_unidade | Número ID que identifica a unidade em que o tópico foi criado. |
| id_usuario | Número ID que identifica o proprietário do tópico. |
| nome | Armazena o nome do tópico. |
| sin_ativo | Variável categórica que indica se o tópico está disponível ou arquivado:<br><br><ul><li>S = Disponível</li><li>N = Arquivado</li></ul> |
