# Dicionário de Dados do Módulo SEI Peticionamento, Intimação e Procuração - v4.6.3

## Índice de Tabelas

- [md_pet_acesso_externo](#md_pet_acesso_externo)
- [md_pet_adm_integ_funcion](#md_pet_adm_integ_funcion)
- [md_pet_adm_integ_param](#md_pet_adm_integ_param)
- [md_pet_adm_integracao](#md_pet_adm_integracao)
- [md_pet_adm_nivel_aces_doc](#md_pet_adm_nivel_aces_doc)
- [md_pet_adm_pro_repres_whit](#md_pet_adm_pro_repres_whit)
- [md_pet_adm_tipo_poder](#md_pet_adm_tipo_poder)
- [md_pet_adm_vinc_rel_serie](#md_pet_adm_vinc_rel_serie)
- [md_pet_adm_vinc_tp_proced](#md_pet_adm_vinc_tp_proced)
- [md_pet_criterio](#md_pet_criterio)
- [md_pet_ext_arquivo_perm](#md_pet_ext_arquivo_perm)
- [md_pet_hipotese_legal](#md_pet_hipotese_legal)
- [md_pet_indisp_doc](#md_pet_indisp_doc)
- [md_pet_indisponibilidade](#md_pet_indisponibilidade)
- [md_pet_int_aceite](#md_pet_int_aceite)
- [md_pet_int_dest_resposta](#md_pet_int_dest_resposta)
- [md_pet_int_prazo_tacita](#md_pet_int_prazo_tacita)
- [md_pet_int_prot_disponivel](#md_pet_int_prot_disponivel)
- [md_pet_int_protocolo](#md_pet_int_protocolo)
- [md_pet_int_rel_dest](#md_pet_int_rel_dest)
- [md_pet_int_rel_intim_resp](#md_pet_int_rel_intim_resp)
- [md_pet_int_rel_resp_doc](#md_pet_int_rel_resp_doc)
- [md_pet_int_rel_tipo_resp](#md_pet_int_rel_tipo_resp)
- [md_pet_int_rel_tpo_res_des](#md_pet_int_rel_tpo_res_des)
- [md_pet_int_serie](#md_pet_int_serie)
- [md_pet_int_tipo_intimacao](#md_pet_int_tipo_intimacao)
- [md_pet_int_tipo_resp](#md_pet_int_tipo_resp)
- [md_pet_int_tp_int_orient](#md_pet_int_tp_int_orient)
- [md_pet_intimacao](#md_pet_intimacao)
- [md_pet_prz_tac_rel_tp_proc](#md_pet_prz_tac_rel_tp_proc)
- [md_pet_rel_int_dest_extern](#md_pet_rel_int_dest_extern)
- [md_pet_rel_recibo_docanexo](#md_pet_rel_recibo_docanexo)
- [md_pet_rel_recibo_protoc](#md_pet_rel_recibo_protoc)
- [md_pet_rel_tp_ctx_contato](#md_pet_rel_tp_ctx_contato)
- [md_pet_rel_tp_proc_serie](#md_pet_rel_tp_proc_serie)
- [md_pet_rel_tp_processo_unid](#md_pet_rel_tp_processo_unid)
- [md_pet_rel_vincrep_protoc](#md_pet_rel_vincrep_protoc)
- [md_pet_rel_vincrep_tipo_poder](#md_pet_rel_vincrep_tipo_poder)
- [md_pet_tamanho_arquivo](#md_pet_tamanho_arquivo)
- [md_pet_tipo_processo](#md_pet_tipo_processo)
- [md_pet_tp_processo_orientacoes](#md_pet_tp_processo_orientacoes)
- [md_pet_usu_externo_menu](#md_pet_usu_externo_menu)
- [md_pet_vinculo](#md_pet_vinculo)
- [md_pet_vinculo_documento](#md_pet_vinculo_documento)
- [md_pet_vinculo_represent](#md_pet_vinculo_represent)

## md_pet_acesso_externo

Registra as funcionalidades do módulo associadas a cada acesso externo.

| Coluna | Descrição |
|---|---|
| id_acesso_externo | Número ID que identifica o acesso externo. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_intimacao | Variável categórica que indica se o acesso foi concedido para intimação eletrônica:<br><br><ul><li>S = Concedido para intimação eletrônica</li><li>N = Não concedido para intimação eletrônica</li></ul> |
| sin_proc_intercorrente | Variável categórica que indica se o acesso foi concedido para peticionamento intercorrente:<br><br><ul><li>S = Concedido para peticionamento intercorrente</li><li>N = Não concedido para peticionamento intercorrente</li></ul> |
| sin_proc_novo | Variável categórica que indica se o acesso foi concedido para peticionamento de processo novo:<br><br><ul><li>S = Concedido para peticionamento de processo novo</li><li>N = Não concedido para peticionamento de processo novo</li></ul> |
| sin_vinculo | Variável categórica que indica se o acesso está relacionado a uma vinculação:<br><br><ul><li>S = Relacionado a uma vinculação</li><li>N = Não relacionado a uma vinculação</li></ul> |

## md_pet_adm_integ_funcion

Armazena as funcionalidades atendidas pelas integrações externas do módulo.

| Coluna | Descrição |
|---|---|
| id_md_pet_adm_integ_funcion | Número ID que identifica a funcionalidade de integração. |
| nome | Armazena o nome da funcionalidade de integração. |

## md_pet_adm_integ_param

Armazena o mapeamento de parâmetros de entrada e saída das integrações externas.

| Coluna | Descrição |
|---|---|
| id_md_pet_adm_integ_param | Número ID que identifica o parâmetro de integração. |
| id_md_pet_adm_integracao | Número ID que identifica a integração relacionada. |
| nome | Armazena o nome funcional do parâmetro. |
| nome_campo | Armazena o nome do campo correspondente no serviço externo. |
| tp_parametro | Status multi-valorado que identifica o tipo do parâmetro:<br><br><ul><li>E = Entrada</li><li>P = Saída</li></ul> |
| valor_padrao | Armazena o valor padrão do parâmetro. |

## md_pet_adm_integracao

Armazena as configurações das integrações externas usadas pelo módulo.

| Coluna | Descrição |
|---|---|
| id_md_pet_adm_integracao | Número ID que identifica a integração. |
| cod_receita_suspensao_auto | Armazena o código da Receita Federal usado na suspensão automática. |
| endereco_wsdl | Armazena o endereço do serviço externo. |
| id_md_pet_adm_integ_funcion | Número ID que identifica a funcionalidade atendida pela integração. |
| nome | Armazena o nome da integração. |
| nu_versao | Armazena o número da versão do serviço SOAP. |
| operacao_wsdl | Armazena a operação executada no serviço externo. |
| sin_ativo | Variável categórica que indica se a integração está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_cache | Variável categórica que indica se a integração utiliza cache:<br><br><ul><li>S = Utiliza cache</li><li>N = Não utiliza cache</li></ul> |
| sin_comp_lougradouro | Variável categórica que indica se o complemento compõe o logradouro retornado:<br><br><ul><li>S = Compõe o logradouro retornado</li><li>N = Não compõe o logradouro retornado</li></ul> |
| sin_nu_lougradouro | Variável categórica que indica se o número compõe o logradouro retornado:<br><br><ul><li>S = Compõe o logradouro retornado</li><li>N = Não compõe o logradouro retornado</li></ul> |
| sin_tp_lougradouro | Variável categórica que indica se o tipo compõe o logradouro retornado:<br><br><ul><li>S = Compõe o logradouro retornado</li><li>N = Não compõe o logradouro retornado</li></ul> |
| sta_tp_cliente_ws | Status multi-valorado que identifica o tipo de cliente do serviço externo:<br><br>S = SOAP. |
| sta_utilizar_ws | Status multi-valorado que identifica se a configuração utiliza serviço externo:<br><br>N = Sem Integração<br>S = Com Integração. |

## md_pet_adm_nivel_aces_doc

Armazena as regras que impõem nível de acesso a tipos de documento do peticionamento.

| Coluna | Descrição |
|---|---|
| id_md_pet_adm_nivel_aces_doc | Número ID que identifica a regra de nível de acesso. |
| id_md_pet_hipodese_legal | Número ID que identifica a hipótese legal relacionada. |
| ids_tipos_documento | Armazena os IDs dos tipos de documento abrangidos pela regra. |
| sta_nivel_acesso | Status multi-valorado que identifica o nível de acesso imposto aos documentos:<br><br>P = Público<br>R = Restrito. |
| sta_tipo_peticionamento | Status multi-valorado que identifica a modalidade de peticionamento abrangida pela regra:<br><br>N = Processo Novo<br>I = Intercorrente/Resposta. |

## md_pet_adm_pro_repres_whit

Registra os processos de representação autorizados para tratamento excepcional pelo módulo.

| Coluna | Descrição |
|---|---|
| id_md_pet_adm_pro_repres_whit | Número ID que identifica a autorização do processo de representação. |
| id_procedimento | Número ID que identifica o processo de representação autorizado. |

## md_pet_adm_tipo_poder

Armazena os tipos de poder que podem ser atribuídos aos representantes.

| Coluna | Descrição |
|---|---|
| data_cadastro | Data/hora de cadastro do tipo de poder. |
| id_md_pet_tipo_poder | Número ID que identifica o tipo de poder. |
| nome | Armazena o nome do tipo de poder. |
| sin_ativo | Variável categórica que indica se o tipo de poder está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_sistema | Status multi-valorado que identifica a origem sistêmica do tipo de poder:<br><br>I = Registro padrão do sistema. |

## md_pet_adm_vinc_rel_serie

Associa tipos de documento às configurações dos processos de representação.

| Coluna | Descrição |
|---|---|
| id_md_pet_adm_vinc_rel_ser | Número ID que identifica a associação entre configuração e tipo de documento. |
| id_md_pet_adm_vinc_tp_proced | Número ID que identifica a configuração do processo de representação. |
| id_serie | Número ID que identifica o tipo de documento. |
| sin_obrigatorio | Variável categórica que indica se o documento é obrigatório:<br><br><ul><li>S = Obrigatório</li><li>N = Não obrigatório</li></ul> |

## md_pet_adm_vinc_tp_proced

Armazena as configurações dos tipos de processo usados nas vinculações de representação.

| Coluna | Descrição |
|---|---|
| id_md_pet_adm_vinc_tp_proced | Número ID que identifica a configuração do processo de representação. |
| especificacao | Armazena o modelo textual usado na especificação do processo. |
| id_hipotese_legal | Número ID que identifica a hipótese legal relacionada. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |
| id_unidade | Número ID que identifica a unidade responsável. |
| orientacoes | Armazena as orientações apresentadas no fluxo de vinculação. |
| sin_ativo | Variável categórica que indica se a configuração está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_na_padrao | Variável categórica que indica se há nível de acesso padrão:<br><br><ul><li>S = Há nível de acesso padrão</li><li>N = Não há nível de acesso padrão</li></ul> |
| sin_na_usuario_externo | Variável categórica que indica se o usuário externo pode definir o nível de acesso:<br><br><ul><li>S = Pode definir o nível de acesso</li><li>N = Não pode definir o nível de acesso</li></ul> |
| sta_nivel_acesso | Status multi-valorado que identifica o nível de acesso configurado para o processo:<br><br>0 = Público<br>1 = Restrito. |
| tipo_vinculo | Status multi-valorado que identifica o tipo de vinculação:<br><br><ul><li>F = Pessoa física</li><li>J = Pessoa jurídica</li></ul> |

## md_pet_criterio

Armazena os critérios de nível de acesso para peticionamento intercorrente.

| Coluna | Descrição |
|---|---|
| id_md_pet_criterio | Número ID que identifica o critério. |
| id_hipotese_legal | Número ID que identifica a hipótese legal relacionada. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |
| sin_ativo | Variável categórica que indica se o critério está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_criterio_padrao | Variável categórica que indica se o critério é padrão:<br><br><ul><li>S = Padrão</li><li>N = Não padrão</li></ul> |
| sin_intercorrente_sigiloso | Variável categórica que indica se o critério contempla processo sigiloso:<br><br><ul><li>S = Contempla processo sigiloso</li><li>N = Não contempla processo sigiloso</li></ul> |
| sta_nivel_acesso | Status multi-valorado que identifica como o nível de acesso será definido:<br><br>1 = Usuário Externo indica diretamente<br>2 = Padrão pré definido. |
| sta_tipo_nivel_acesso | Status multi-valorado que identifica o tipo de nível de acesso predefinido:<br><br>P = Público<br>I = Restrito. |

## md_pet_ext_arquivo_perm

Armazena as extensões de arquivo permitidas nos peticionamentos.

| Coluna | Descrição |
|---|---|
| id_md_pet_ext_arquivo_perm | Número ID que identifica a permissão de extensão de arquivo. |
| id_arquivo_extensao | Número ID que identifica a extensão de arquivo. |
| sin_ativo | Variável categórica que indica se a extensão está permitida:<br><br><ul><li>S = Permitida</li><li>N = Não permitida</li></ul> |
| sin_principal | Variável categórica que indica se a extensão pode ser usada no documento principal:<br><br><ul><li>S = Pode ser usada no documento principal</li><li>N = Não pode ser usada no documento principal</li></ul> |

## md_pet_hipotese_legal

Referencia as hipóteses legais permitidas nas configurações do módulo.

| Coluna | Descrição |
|---|---|
| id_md_pet_hipotese_legal | Número ID que identifica a hipótese legal permitida. |

## md_pet_indisp_doc

Registra documentos e acessos externos relacionados a períodos de indisponibilidade.

| Coluna | Descrição |
|---|---|
| id_md_pet_indisp_doc | Número ID que identifica o documento de indisponibilidade. |
| dth_inclusao | Data/hora de inclusão do documento. |
| id_acesso_externo | Número ID que identifica o acesso externo relacionado. |
| id_documento | Número ID que identifica o documento relacionado. |
| id_md_pet_indisponibilidade | Número ID que identifica a indisponibilidade relacionada. |
| id_unidade | Número ID que identifica a unidade responsável. |
| id_usuario | Número ID que identifica o usuário responsável. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_pet_indisponibilidade

Registra períodos de indisponibilidade e sua repercussão nos prazos do módulo.

| Coluna | Descrição |
|---|---|
| id_md_pet_indisponibilidade | Número ID que identifica a indisponibilidade. |
| dth_fim | Data/hora de término da indisponibilidade. |
| dth_inicio | Data/hora de início da indisponibilidade. |
| resumo_indisponibilidade | Armazena o resumo da indisponibilidade. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_prorrogacao | Variável categórica que indica se a indisponibilidade gera prorrogação de prazo:<br><br><ul><li>S = Gera prorrogação de prazo</li><li>N = Não gera prorrogação de prazo</li></ul> |

## md_pet_int_aceite

Registra o cumprimento da intimação por consulta direta ou decurso de prazo.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_aceite | Número ID que identifica o aceite da intimação. |
| data | Data/hora do cumprimento da intimação. |
| data_consulta_direta | Data/hora da consulta direta à intimação. |
| id_documento_certidao | Número ID que identifica a certidão de cumprimento. |
| id_md_pet_int_rel_dest | Número ID que identifica o destinatário da intimação. |
| id_usuario | Número ID que identifica o usuário associado ao cumprimento. |
| ip | Armazena o endereço IP associado ao cumprimento. |
| tipo_aceite | Status multi-valorado que identifica o tipo de aceite:<br><br><ul><li>A = Automático por decurso de prazo</li><li>U = Realizado pelo usuário externo</li></ul> |

## md_pet_int_dest_resposta

Registra as respostas apresentadas pelos destinatários das intimações.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_dest_resposta | Número ID que identifica a resposta do destinatário. |
| data | Data/hora de apresentação da resposta. |
| id_md_pet_int_rel_dest | Número ID que identifica o destinatário da intimação. |
| id_md_pet_int_rel_tipo_resp | Número ID que identifica o tipo de resposta utilizado. |
| id_usuario | Número ID que identifica o usuário responsável pela resposta. |
| ip | Armazena o endereço IP associado à resposta. |

## md_pet_int_prazo_tacita

Armazena os prazos para cumprimento tácito das intimações.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_prazo_tacita | Número ID que identifica a configuração de prazo tácito. |
| num_prazo | Armazena a quantidade de dias do prazo tácito. |
| sta_tipo_prazo | Status multi-valorado que identifica o tipo de aplicação do prazo tácito:<br><br>G = Geral<br>E = Específico/Customizado. |

## md_pet_int_prot_disponivel

Associa às intimações os protocolos disponibilizados aos destinatários.

| Coluna | Descrição |
|---|---|
| id_md_pet_intimacao | Número ID que identifica a intimação. |
| id_protocolo | Número ID que identifica o protocolo disponibilizado. |

## md_pet_int_protocolo

Registra os protocolos que compõem cada intimação eletrônica.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_protocolo | Número ID que identifica a associação entre intimação e protocolo. |
| id_md_pet_intimacao | Número ID que identifica a intimação. |
| id_protocolo | Número ID que identifica o protocolo relacionado. |
| sin_principal | Variável categórica que indica se o protocolo é o documento principal da intimação:<br><br><ul><li>S = O documento principal da intimação</li><li>N = Não o documento principal da intimação</li></ul> |

## md_pet_int_rel_dest

Registra os destinatários e a situação individual de cada intimação.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_rel_dest | Número ID que identifica o destinatário da intimação. |
| data_cadastro | Data/hora de inclusão do destinatário. |
| dta_prazo_tacito | Data/hora limite para cumprimento tácito. |
| id_contato | Número ID que identifica o contato destinatário. |
| id_md_pet_intimacao | Número ID que identifica a intimação. |
| id_unidade | Número ID que identifica a unidade expedidora. |
| sin_ativo | Variável categórica que indica se o destinatário está ativo na intimação:<br><br><ul><li>S = Ativo na intimação</li><li>N = Não ativo na intimação</li></ul> |
| sin_pessoa_juridica | Variável categórica que indica se o destinatário é pessoa jurídica:<br><br><ul><li>S = Pessoa jurídica</li><li>N = Não pessoa jurídica</li></ul> |
| sta_situacao_intimacao | Status multi-valorado que identifica a situação da intimação para o destinatário:<br><br>1 = Pendente<br>2 = Cumprida por Decurso do Prazo Tácito<br>3 = Cumprida por Consulta Direta<br>4 = Respondida<br>5 = Pendente de Resposta com Prazo Externo Vencido. |

## md_pet_int_rel_intim_resp

Associa os tipos de resposta permitidos a cada tipo de intimação.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_tipo_intimacao | Número ID que identifica o tipo de intimação. |
| id_md_pet_int_tipo_resp | Número ID que identifica o tipo de resposta. |
| sin_ativo | Variável categórica que indica se a associação está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## md_pet_int_rel_resp_doc

Associa documentos protocolizados às respostas de intimação.

| Coluna | Descrição |
|---|---|
| id_documento | Número ID que identifica o documento da resposta. |
| id_md_pet_int_dest_resposta | Número ID que identifica a resposta do destinatário. |
| id_md_pet_int_resp_documento | Número ID que identifica a associação entre resposta e documento. |

## md_pet_int_rel_tipo_resp

Registra os tipos de resposta disponibilizados em cada intimação.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_rel_tipo_resp | Número ID que identifica a associação entre intimação e tipo de resposta. |
| id_md_pet_int_tipo_resp | Número ID que identifica o tipo de resposta. |
| id_md_pet_intimacao | Número ID que identifica a intimação. |
| sin_ativo | Variável categórica que indica se o tipo de resposta está disponível:<br><br><ul><li>S = Disponível</li><li>N = Não disponível</li></ul> |

## md_pet_int_rel_tpo_res_des

Registra os prazos dos tipos de resposta para cada destinatário da intimação.

| Coluna | Descrição |
|---|---|
| data_limite | Data/hora limite original para apresentação da resposta. |
| data_prorrogada | Data/hora limite após prorrogação. |
| id_md_pet_int_rel_dest | Número ID que identifica o destinatário da intimação. |
| id_md_pet_int_rel_tipo_res_des | Número ID que identifica a associação entre destinatário e tipo de resposta. |
| id_md_pet_int_rel_tipo_resp | Número ID que identifica o tipo de resposta disponibilizado. |

## md_pet_int_serie

Referencia os tipos de documento habilitados para gerar intimações eletrônicas.

| Coluna | Descrição |
|---|---|
| id_serie | Número ID que identifica o tipo de documento habilitado. |

## md_pet_int_tipo_intimacao

Armazena os tipos de intimação eletrônica disponíveis no módulo.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_tipo_intimacao | Número ID que identifica o tipo de intimação. |
| nome | Armazena o nome do tipo de intimação. |
| sin_ativo | Variável categórica que indica se o tipo de intimação está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo_resposta_aceita | Status multi-valorado que identifica o tipo de resposta aceita:<br><br><ul><li>F = Facultativa</li><li>E = Exigida</li><li>S = Sem resposta</li></ul> |

## md_pet_int_tipo_resp

Armazena os tipos de resposta e seus prazos externos.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_tipo_resp | Número ID que identifica o tipo de resposta. |
| nome | Armazena o nome do tipo de resposta. |
| sin_ativo | Variável categórica que indica se o tipo de resposta está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo_dia | Status multi-valorado que identifica o tipo de contagem:<br><br><ul><li>C = Dias corridos</li><li>U = Dias úteis</li></ul> |
| tipo_prazo_externo | Status multi-valorado que identifica a unidade usada no prazo externo:<br><br><ul><li>D = Dia</li><li>M = Mês</li><li>A = Ano</li></ul> |
| tipo_resposta_aceita | Status multi-valorado que identifica o tipo de resposta:<br><br><ul><li>E = Exigida</li><li>F = Facultativa</li></ul> |
| valor_prazo_externo | Armazena a quantidade correspondente ao prazo externo. |

## md_pet_int_tp_int_orient

Armazena orientações sobre a escolha do tipo de destinatário da intimação.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_tp_int_orient | Número ID que identifica a orientação. |
| id_conjunto_estilos | Número ID que identifica o conjunto de estilos aplicado. |
| orientacoes_tp_destinatario | Armazena o conteúdo das orientações sobre o destinatário. |

## md_pet_intimacao

Registra as intimações eletrônicas e sua política de acesso ao processo.

| Coluna | Descrição |
|---|---|
| id_md_pet_intimacao | Número ID que identifica a intimação. |
| id_md_pet_int_tipo_intimacao | Número ID que identifica o tipo de intimação. |
| sin_tipo_acesso_processo | Variável categórica que indica o tipo de acesso concedido ao processo:<br><br><ul><li>I = Integral</li><li>P = Parcial</li></ul> |

## md_pet_prz_tac_rel_tp_proc

Associa prazos tácitos específicos aos tipos de processo abrangidos.

| Coluna | Descrição |
|---|---|
| id_md_pet_int_prazo_tacita | Número ID que identifica a configuração de prazo tácito. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |

## md_pet_rel_int_dest_extern

Associa os destinatários das intimações aos acessos externos concedidos.

| Coluna | Descrição |
|---|---|
| id_acesso_externo | Número ID que identifica o acesso externo. |
| id_md_pet_int_rel_dest | Número ID que identifica o destinatário da intimação. |

## md_pet_rel_recibo_docanexo

Registra os documentos e anexos apresentados em cada recibo eletrônico.

| Coluna | Descrição |
|---|---|
| id_md_pet_rel_recibo_docanexo | Número ID que identifica o item do recibo. |
| classificacao_documento | Status multi-valorado que identifica a função do documento no peticionamento:<br><br><ul><li>P = Principal</li><li>E = Essencial</li><li>C = Complementar</li><li>V = Vinculação</li></ul> |
| formato_documento | Status multi-valorado que identifica o formato do documento:<br><br><ul><li>D = Digitalizado</li><li>N = Nato-digital</li></ul> |
| id_anexo | Número ID que identifica o anexo relacionado. |
| id_documento | Número ID que identifica o documento relacionado. |
| id_md_pet_rel_recibo_protoc | Número ID que identifica o recibo eletrônico. |

## md_pet_rel_recibo_protoc

Registra os recibos eletrônicos emitidos pelos fluxos do módulo.

| Coluna | Descrição |
|---|---|
| id_md_pet_rel_recibo_protoc | Número ID que identifica o recibo eletrônico. |
| data_hora_recebimento_final | Data/hora de conclusão do protocolo. |
| id_documento | Número ID que identifica o documento associado ao recibo. |
| id_protocolo | Número ID que identifica o protocolo principal. |
| id_protocolo_relacionado | Número ID que identifica o protocolo relacionado. |
| id_usuario | Número ID que identifica o usuário responsável. |
| ip_usuario | Armazena o endereço IP do usuário. |
| sin_ativo | Variável categórica que indica se o recibo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_tipo_peticionamento | Status multi-valorado que identifica o tipo de peticionamento do recibo:<br><br>N = Processo Novo<br>I = Intercorrente<br>R = Resposta a Intimação<br>V = Responsável Legal - Inicial<br>A = Responsável Legal - Alteração<br>C = Atualização de Atos Constitutivos<br>P = Procuração Eletrônica - Emissão<br>G = Procuração Eletrônica - Revogação<br>U = Procuração Eletrônica - Renúncia. |
| txt_doc_principal_intimacao | Armazena a identificação textual do documento principal da intimação. |

## md_pet_rel_tp_ctx_contato

Configura os tipos de contato permitidos na indicação de interessados.

| Coluna | Descrição |
|---|---|
| id_md_pet_rel_tp_ctx_contato | Número ID que identifica a configuração do tipo de contato. |
| id_tipo_contato | Número ID que identifica o tipo de contato. |
| sin_cadastro_interessado | Variável categórica que indica se o tipo pode ser usado no cadastro de interessado:<br><br><ul><li>S = Pode ser usado no cadastro de interessado</li><li>N = Não pode ser usado no cadastro de interessado</li></ul> |
| sin_selecao_interessado | Variável categórica que indica se o tipo pode ser usado na seleção de interessado:<br><br><ul><li>S = Pode ser usado na seleção de interessado</li><li>N = Não pode ser usado na seleção de interessado</li></ul> |

## md_pet_rel_tp_proc_serie

Associa documentos essenciais e complementares aos tipos de processo configurados.

| Coluna | Descrição |
|---|---|
| id_md_pet_rel_tipo_proc | Número ID que identifica a associação entre tipo de processo e documento. |
| id_md_pet_tipo_processo | Número ID que identifica a configuração do tipo de processo. |
| id_serie | Número ID que identifica o tipo de documento. |
| sta_tp_doc | Status multi-valorado que identifica a classificação do documento no peticionamento:<br><br>C = Complementar<br>E = Essencial. |

## md_pet_rel_tp_processo_unid

Associa unidades aos tipos de processo disponibilizados para peticionamento.

| Coluna | Descrição |
|---|---|
| id_md_pet_tipo_processo | Número ID que identifica a configuração do tipo de processo. |
| id_unidade | Número ID que identifica a unidade destinatária. |
| sta_tp_unidade | Status multi-valorado que identifica a forma de seleção da unidade:<br><br>U = Unidade Única<br>M = Múltiplas Unidades. |

## md_pet_rel_vincrep_protoc

Associa representações aos processos ou protocolos por elas abrangidos.

| Coluna | Descrição |
|---|---|
| id_md_pet_vinculo_represent | Número ID que identifica a representação. |
| id_protocolo | Número ID que identifica o processo ou protocolo abrangido. |

## md_pet_rel_vincrep_tipo_poder

Associa os poderes concedidos a cada representante.

| Coluna | Descrição |
|---|---|
| id_md_pet_tipo_poder | Número ID que identifica o tipo de poder. |
| id_md_pet_vinculo_represent | Número ID que identifica a representação. |

## md_pet_tamanho_arquivo

Armazena os limites de tamanho dos documentos enviados no peticionamento.

| Coluna | Descrição |
|---|---|
| id_md_pet_tamanho_arquivo | Número ID que identifica a configuração de tamanho de arquivo. |
| sin_ativo | Variável categórica que indica se a configuração está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| valor_doc_complementar | Armazena o limite definido para documento complementar. |
| valor_doc_principal | Armazena o limite definido para documento principal. |

## md_pet_tipo_processo

Armazena as configurações dos tipos de processo disponibilizados ao usuário externo.

| Coluna | Descrição |
|---|---|
| id_md_pet_tipo_processo | Número ID que identifica a configuração do tipo de processo. |
| id_hipotese_legal | Número ID que identifica a hipótese legal relacionada. |
| id_serie | Número ID que identifica o tipo do documento principal. |
| id_tipo_formulario | Número ID que identifica o formulário associado. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo. |
| orientacoes | Armazena as orientações apresentadas ao usuário externo. |
| sin_ativo | Variável categórica que indica se o tipo de processo está disponível:<br><br><ul><li>S = Disponível</li><li>N = Não disponível</li></ul> |
| sin_doc_externo | Variável categórica que indica se documento externo é permitido:<br><br><ul><li>S = Permitido</li><li>N = Não permitido</li></ul> |
| sin_doc_formulario | Variável categórica que indica se documento formulário é permitido:<br><br><ul><li>S = Permitido</li><li>N = Não permitido</li></ul> |
| sin_doc_gerado | Variável categórica que indica se documento gerado é permitido:<br><br><ul><li>S = Permitido</li><li>N = Não permitido</li></ul> |
| sin_ii_indic_direta_contato | Variável categórica que indica se interessado pode ser indicado diretamente por contato:<br><br><ul><li>S = Pode ser indicado diretamente por contato</li><li>N = Não pode ser indicado diretamente por contato</li></ul> |
| sin_ii_indic_direta_cpf_cnpj | Variável categórica que indica se interessado pode ser indicado diretamente por CPF ou CNPJ:<br><br><ul><li>S = Pode ser indicado diretamente por CPF ou CNPJ</li><li>N = Não pode ser indicado diretamente por CPF ou CNPJ</li></ul> |
| sin_ii_indicacao_direta | Variável categórica que indica se a indicação direta de interessado é permitida:<br><br><ul><li>S = Permitida</li><li>N = Não permitida</li></ul> |
| sin_ii_proprio_usuario_externo | Variável categórica que indica se o próprio usuário externo pode ser interessado:<br><br><ul><li>S = Pode ser interessado</li><li>N = Não pode ser interessado</li></ul> |
| sin_na_padrao | Variável categórica que indica se há nível de acesso padrão:<br><br><ul><li>S = Há nível de acesso padrão</li><li>N = Não há nível de acesso padrão</li></ul> |
| sin_na_usuario_externo | Variável categórica que indica se o usuário externo pode definir o nível de acesso:<br><br><ul><li>S = Pode definir o nível de acesso</li><li>N = Não pode definir o nível de acesso</li></ul> |
| sta_nivel_acesso | Status multi-valorado que identifica o nível de acesso configurado para o processo:<br><br>0 = Público<br>1 = Restrito. |

## md_pet_tp_processo_orientacoes

Armazena orientações gerais para o peticionamento de processo novo.

| Coluna | Descrição |
|---|---|
| id_conjunto_estilos | Número ID que identifica o conjunto de estilos aplicado. |
| id_md_pet_tp_proc_orientacoes | Número ID que identifica a orientação geral. |
| orientacoes_gerais | Armazena o conteúdo das orientações gerais. |
| sin_ativo_menu_ext | Variável categórica que indica se as orientações aparecem no menu externo:<br><br><ul><li>S = Aparecem no menu externo</li><li>N = Não aparecem no menu externo</li></ul> |

## md_pet_usu_externo_menu

Armazena itens adicionais do menu do usuário externo.

| Coluna | Descrição |
|---|---|
| id_md_pet_usu_externo_menu | Número ID que identifica o item de menu. |
| conteudo_html | Armazena o conteúdo HTML do item de menu. |
| id_conjunto_estilos | Número ID que identifica o conjunto de estilos aplicado. |
| nome | Armazena o nome exibido no menu. |
| sin_ativo | Variável categórica que indica se o item está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo | Status multi-valorado que identifica o tipo do item:<br><br><ul><li>E = Endereço externo</li><li>H = Conteúdo HTML</li></ul> |
| url | Armazena o endereço do item de menu. |

## md_pet_vinculo

Registra a entidade representada e o processo administrativo de sua vinculação.

| Coluna | Descrição |
|---|---|
| id_md_pet_vinculo | Número ID que identifica a vinculação. |
| dth_ultima_consulta_rfb | Data/hora da última consulta cadastral à Receita Federal. |
| id_contato | Número ID que identifica o contato representado. |
| id_procedimento | Número ID que identifica o processo administrativo da vinculação. |
| sin_validado | Variável categórica que indica se a vinculação foi validada:<br><br><ul><li>S = Validada</li><li>N = Não validada</li></ul> |
| sin_web_service | Variável categórica que indica se a vinculação utiliza serviço externo:<br><br><ul><li>S = Utiliza serviço externo</li><li>N = Não utiliza serviço externo</li></ul> |
| tp_vinculo | Status multi-valorado que identifica o tipo de vinculação:<br><br><ul><li>F = Pessoa física</li><li>J = Pessoa jurídica</li></ul> |

## md_pet_vinculo_documento

Registra os documentos produzidos ou relacionados às vinculações de representação.

| Coluna | Descrição |
|---|---|
| id_md_pet_vinculo_documento | Número ID que identifica o documento da vinculação. |
| data_cadastro | Data/hora de cadastro do documento na vinculação. |
| id_documento | Número ID que identifica o documento relacionado. |
| id_md_pet_vinculo_represent | Número ID que identifica a representação relacionada. |
| tipo_documento | Status multi-valorado que identifica o tipo do documento relacionado à vinculação:<br><br><ul><li>A = Atos</li><li>P = Principal</li><li>R = Recibo</li><li>E = Procuração Especial</li><li>N = Procuração</li><li>S = Suspensão</li><li>T = Restabelecimento</li><li>D = Diligência de Suspensão</li><li>I = Diligência de Restabelecimento</li></ul> |

## md_pet_vinculo_represent

Registra os representantes, a vigência, a abrangência e a situação de cada representação.

| Coluna | Descrição |
|---|---|
| id_md_pet_vinculo_represent | Número ID que identifica a representação. |
| data_cadastro | Data/hora de início da representação. |
| data_encerramento | Data/hora de encerramento da representação. |
| data_limite | Data/hora limite da representação. |
| id_contato | Número ID que identifica o contato outorgado. |
| id_contato_outorg | Número ID que identifica o contato outorgante. |
| id_md_pet_vinculo | Número ID que identifica a vinculação representada. |
| motivo | Armazena o motivo relacionado à situação da representação. |
| sta_abrangencia | Status multi-valorado que identifica a abrangência da representação:<br><br>Q = Qualquer Processo em Nome do Outorgante<br>E = Processos Específicos. |
| sta_estado | Status multi-valorado que identifica a situação da representação:<br><br>A = Ativa<br>S = Suspensa<br>R = Revogada<br>C = Renunciada<br>V = Vencida<br>T = Substituída<br>I = Inativa. |
| tipo_representante | Status multi-valorado que identifica o tipo do representante vinculado:<br><br><ul><li>L = Responsável Legal</li><li>E = Procurador Especial</li><li>C = Procurador</li><li>S = Procurador Simples</li><li>U = Autorrepresentação</li></ul> |
