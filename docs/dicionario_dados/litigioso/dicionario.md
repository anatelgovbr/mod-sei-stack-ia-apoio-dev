# Dicionário de Dados do Módulo SEI Litigioso - v2.5.3

## Índice de Tabelas

- [md_lit_adm_modalidad_outor](#md_lit_adm_modalidad_outor)
- [md_lit_adm_tipo_outor](#md_lit_adm_tipo_outor)
- [md_lit_assoc_disp_normat (legado)](#md_lit_assoc_disp_normat-legado)
- [md_lit_campo_integracao](#md_lit_campo_integracao)
- [md_lit_campos_ad](#md_lit_campos_ad)
- [md_lit_campos_ad_form](#md_lit_campos_ad_form)
- [md_lit_campos_ad_sel](#md_lit_campos_ad_sel)
- [md_lit_cancela_lancamento](#md_lit_cancela_lancamento)
- [md_lit_conduta](#md_lit_conduta)
- [md_lit_controle](#md_lit_controle)
- [md_lit_dado_interessado](#md_lit_dado_interessado)
- [md_lit_decisao](#md_lit_decisao)
- [md_lit_disp_normat](#md_lit_disp_normat)
- [md_lit_especie_decisao](#md_lit_especie_decisao)
- [md_lit_fase](#md_lit_fase)
- [md_lit_funcionalidade](#md_lit_funcionalidade)
- [md_lit_historic_lancamento](#md_lit_historic_lancamento)
- [md_lit_integracao](#md_lit_integracao)
- [md_lit_lancamento](#md_lit_lancamento)
- [md_lit_mapea_param_entrada](#md_lit_mapea_param_entrada)
- [md_lit_mapea_param_saida](#md_lit_mapea_param_saida)
- [md_lit_mapea_param_valor](#md_lit_mapea_param_valor)
- [md_lit_motivo](#md_lit_motivo)
- [md_lit_nome_funcional](#md_lit_nome_funcional)
- [md_lit_numero_interessado](#md_lit_numero_interessado)
- [md_lit_obrigacao](#md_lit_obrigacao)
- [md_lit_param_interessado](#md_lit_param_interessado)
- [md_lit_processo_situacao](#md_lit_processo_situacao)
- [md_lit_reinciden_anteceden](#md_lit_reinciden_anteceden)
- [md_lit_rel_controle_motivo](#md_lit_rel_controle_motivo)
- [md_lit_rel_decis_lancament](#md_lit_rel_decis_lancament)
- [md_lit_rel_decisao_uf](#md_lit_rel_decisao_uf)
- [md_lit_rel_dis_nor_con_ctr](#md_lit_rel_dis_nor_con_ctr)
- [md_lit_rel_disp_norm_conduta](#md_lit_rel_disp_norm_conduta)
- [md_lit_rel_disp_norm_revogado](#md_lit_rel_disp_norm_revogado)
- [md_lit_rel_disp_norm_tipo_ctrl](#md_lit_rel_disp_norm_tipo_ctrl)
- [md_lit_rel_esp_decisao_obr](#md_lit_rel_esp_decisao_obr)
- [md_lit_rel_num_inter_modali](#md_lit_rel_num_inter_modali)
- [md_lit_rel_num_inter_servico](#md_lit_rel_num_inter_servico)
- [md_lit_rel_num_inter_tp_outor](#md_lit_rel_num_inter_tp_outor)
- [md_lit_rel_opc_camp_mult](#md_lit_rel_opc_camp_mult)
- [md_lit_rel_protoco_protoco](#md_lit_rel_protoco_protoco)
- [md_lit_rel_sit_serie](#md_lit_rel_sit_serie)
- [md_lit_rel_tipo_ctrl_tipo_dec](#md_lit_rel_tipo_ctrl_tipo_dec)
- [md_lit_rel_tp_control_moti](#md_lit_rel_tp_control_moti)
- [md_lit_rel_tp_controle_proced](#md_lit_rel_tp_controle_proced)
- [md_lit_rel_tp_controle_unid](#md_lit_rel_tp_controle_unid)
- [md_lit_rel_tp_controle_usu](#md_lit_rel_tp_controle_usu)
- [md_lit_rel_tp_ctrl_proc_sobres](#md_lit_rel_tp_ctrl_proc_sobres)
- [md_lit_rel_tp_dec_rein_ante](#md_lit_rel_tp_dec_rein_ante)
- [md_lit_rel_tp_especie_dec](#md_lit_rel_tp_especie_dec)
- [md_lit_servico](#md_lit_servico)
- [md_lit_servico_integracao](#md_lit_servico_integracao)
- [md_lit_situacao](#md_lit_situacao)
- [md_lit_situacao_lancam_int](#md_lit_situacao_lancam_int)
- [md_lit_situacao_lancamento](#md_lit_situacao_lancamento)
- [md_lit_tipo_controle](#md_lit_tipo_controle)
- [md_lit_tipo_decisao](#md_lit_tipo_decisao)
- [md_lit_tp_info_add](#md_lit_tp_info_add)

## md_lit_adm_modalidad_outor

Armazena as modalidades de outorga cadastradas para classificação do serviço/número do interessado.

| Coluna | Descrição |
|---|---|
| id_md_lit_adm_modalidad_outor | Número ID que identifica a Modalidade de Outorga. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_adm_tipo_outor

Armazena os tipos de outorga cadastrados para classificação do serviço/número do interessado (conceito que substituiu, em versão anterior do módulo, o que era denominado 'Abrangência').

| Coluna | Descrição |
|---|---|
| id_md_lit_adm_tipo_outor | Número ID que identifica o Tipo de Outorga. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_assoc_disp_normat (legado)

Tabela associativa entre o Dispositivo Normativo e o Tipo de Controle Litigioso, definindo quais dispositivos normativos estão disponíveis para vinculação em cada tipo de controle.

**Observação:** Os dados da tabela foram migrados para a tabela `md_lit_rel_disp_norm_tipo_ctrl`, porém não foi removida do banco de dados.

| Coluna | Descrição |
|---|---|
| id_md_lit_assoc_disp_normat | Número ID que identifica a associação entre Dispositivo Normativo e Tipo de Controle Litigioso. |
| id_md_lit_disp_normat | Número ID que identifica o Dispositivo Normativo associado, faz referência à tabela `md_lit_disp_normat`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso associado, faz referência à tabela `md_lit_tipo_controle`. |

## md_lit_campo_integracao

Armazena os campos de integração disponíveis para uma Funcionalidade, utilizados no mapeamento de parâmetros de entrada e saída das Integrações.

| Coluna | Descrição |
|---|---|
| id_md_lit_campo_integracao | Número ID que identifica o Campo de Integração. |
| id_md_lit_funcionalidade | Número ID que identifica a Funcionalidade, faz referência à tabela `md_lit_funcionalidade`. |
| nome_campo | Nome do campo de parametrização da integração. |
| sta_parametro | Status multi-valorado que identifica o parâmetro de mapeamento do Campo de Integração:<br><br><ul><li>E = Entrada</li><li>S = Saída</li> |

## md_lit_campos_ad

Cadastro dos Campos Adicionais do formulário dinâmico de Informações Adicionais, com tipo de dado, tamanho, obrigatoriedade e ordem de exibição, associados a um Tipo de Informação Adicional.

| Coluna | Descrição |
|---|---|
| id_md_lit_campos_ad | Número ID que identifica o Campo Adicional. |
| ajuda | Texto de ajuda exibido ao usuário para o preenchimento do campo. |
| id_md_lit_campos_ad_sel | Número ID que identifica a opção de Campo Adicional da qual este Campo Adicional depende, faz referência à tabela `md_lit_campos_ad_sel`. |
| id_md_lit_tp_info_add | Número ID que identifica o Tipo de Informação Adicional, faz referência à tabela `md_lit_tp_info_add`. |
| nome | Nome do registro. |
| ordem | Número que define a ordem de apresentação do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_doc_externo | Variável categórica que indica se o Campo Adicional é do tipo Documento SEI:<br><br><ul><li>S = Do tipo Documento SEI</li><li>N = Não do tipo Documento SEI</li></ul> |
| sin_obrigatorio | Variável categórica que indica se o preenchimento é obrigatório:<br><br><ul><li>S = Obrigatório</li><li>N = Não obrigatório</li></ul> |
| tamanho | Tamanho (quantidade de caracteres) permitido para o campo. |
| tipo | Tipo do campo adicional (ex.: texto, data, lista, múltipla seleção, documento SEI), conforme cadastrado na Administração de Informações Adicionais. |
| valor_maximo | Valor máximo permitido para preenchimento do campo. |
| valor_minimo | Valor mínimo permitido para preenchimento do campo. |

## md_lit_campos_ad_form

Armazena o valor preenchido de um Campo Adicional em um processo (procedimento) específico.

| Coluna | Descrição |
|---|---|
| id_md_lit_campos_ad_form | Número ID que identifica o preenchimento de Campo Adicional. |
| dth_inclusao | Data/hora de inclusão do registro. |
| id_md_lit_campos_ad | Número ID que identifica o Campo Adicional, faz referência à tabela `md_lit_campos_ad`. |
| id_procedimento | Número ID que identifica o processo (procedimento), faz referência à tabela `procedimento`, do núcleo do SEI. |
| id_usuario | Número ID que identifica o usuário, faz referência à tabela `usuario`, do núcleo do SEI. |
| num_linha | Número da linha, usado para ordenar múltiplas ocorrências do mesmo Campo Adicional em um formulário. |
| valor | Valor preenchido pelo usuário para o Campo Adicional, no processo (procedimento) informado. |

## md_lit_campos_ad_sel

Cadastro das opções de seleção de um Campo Adicional do tipo lista/múltipla escolha.

| Coluna | Descrição |
|---|---|
| id_md_lit_campos_ad_sel | Número ID que identifica a opção de Campo Adicional. |
| id_md_lit_campos_ad | Número ID que identifica o Campo Adicional ao qual esta opção de seleção pertence, faz referência à tabela `md_lit_campos_ad`. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_cancela_lancamento

Armazena o registro de cancelamento de um Lançamento de crédito, incluindo o motivo e a justificativa do cancelamento.

| Coluna | Descrição |
|---|---|
| id_md_lit_cancela_lancamento | Número ID que identifica o cancelamento de Lançamento de crédito. |
| id_md_lit_lancamento | Número ID que identifica o Lançamento de crédito, faz referência à tabela `md_lit_lancamento`. |
| justificativa | Texto de justificativa informado pelo usuário. |
| motivo_cancelamento | Motivo do cancelamento do Lançamento. |

## md_lit_conduta

Armazena as condutas que podem ser vinculadas a um dispositivo normativo, utilizadas para descrever a infração imputada no controle litigioso.

| Coluna | Descrição |
|---|---|
| id_md_lit_conduta | Número ID que identifica a Conduta. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_controle

Armazena o registro do controle litigioso instaurado, vinculando o processo (procedimento) e o documento de instauração à respectiva unidade de cadastro e ao Tipo de Controle Litigioso.

| Coluna | Descrição |
|---|---|
| id_md_lit_controle | Número ID que identifica o Controle (processo). |
| dta_instauracao | Data de instauração do Controle (processo). |
| id_documento | Número ID que identifica o documento, faz referência à tabela `documento`, do núcleo do SEI. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| id_procedimento | Número ID que identifica o processo (procedimento), faz referência à tabela `procedimento`, do núcleo do SEI. |

## md_lit_dado_interessado

Armazena os dados do interessado (contato) vinculados a um controle litigioso, incluindo CPF/CNPJ e indicação de se o interessado é o outorgado do serviço/objeto do processo.

| Coluna | Descrição |
|---|---|
| id_md_lit_dado_interessado | Número ID que identifica o Dado do Interessado. |
| cnpj | Número do CNPJ do interessado, quando pessoa jurídica. |
| cpf | Número do CPF do interessado, quando pessoa física. |
| id_contato | Número ID que identifica o contato, faz referência à tabela `contato`, do núcleo do SEI. |
| id_md_lit_controle | Número ID que identifica o Controle (processo), faz referência à tabela `md_lit_controle`. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_outorgado | Variável categórica que indica se o interessado é o outorgado do serviço:<br><br><ul><li>S = O outorgado do serviço</li><li>N = Não o outorgado do serviço</li></ul> |

## md_lit_decisao

Armazena as decisões proferidas em uma Situação (do tipo Decisória) de um processo, vinculando o Tipo de Decisão, a Espécie de Decisão, a Obrigação aplicada, o valor da multa e demais dados da decisão.

| Coluna | Descrição |
|---|---|
| id_md_lit_decisao | Número ID que identifica a Decisão. |
| dth_inclusao | Data/hora de inclusão do registro. |
| id_md_lit_especie_decisao | Número ID que identifica a Espécie de Decisão, faz referência à tabela `md_lit_especie_decisao`. |
| id_md_lit_obrigacao | Número ID que identifica a Obrigação, faz referência à tabela `md_lit_obrigacao`. |
| id_md_lit_processo_situacao | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_md_lit_rel_dis_nor_con_ctr | Número ID que identifica a infração (Dispositivo Normativo/Conduta/Controle), faz referência à tabela `md_lit_rel_dis_nor_con_ctr`. |
| id_md_lit_tipo_decisao | Número ID que identifica o Tipo de Decisão, faz referência à tabela `md_lit_tipo_decisao`. |
| id_unidade | Número ID que identifica a unidade responsável pelo registro da Decisão, faz referência à tabela `unidade`, do núcleo do SEI. |
| id_usuario | Número ID que identifica o usuário responsável pelo registro da Decisão, faz referência à tabela `usuario`, do núcleo do SEI. |
| multa | Valor da multa indicada na Decisão. |
| prazo | Prazo (em dias) associado ao registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_cadastro_parcial | Variável categórica que indica se a Decisão foi salva com cadastro parcial/incompleto:<br><br><ul><li>S = Salva com cadastro parcial/incompleto</li><li>N = Não salva com cadastro parcial/incompleto</li></ul> |
| sin_ultima_decisao | Variável categórica que indica se este é o registro da última Decisão do Processo/Situação:<br><br><ul><li>S = O registro da última Decisão do Processo/Situação</li><li>N = Não o registro da última Decisão do Processo/Situação</li></ul> |
| sta_localidade | Status multi-valorado que identifica a abrangência territorial da Decisão:<br><br><ul><li>N = Nacional</li><li>U = Por UF, associada via `md_lit_rel_decisao_uf`</li></ul> |
| valor | Valor monetário indicado na Decisão (aplicável conforme a Espécie de Decisão). |
| valor_multa_sem_integracao | Valor da multa indicado manualmente, sem uso de integração com o sistema de arrecadação. |

## md_lit_disp_normat

Armazena os dispositivos normativos (normas e respectivos artigos/incisos/dispositivos) cadastrados para vinculação da infração normativa ocorrida no processo.

| Coluna | Descrição |
|---|---|
| id_md_lit_disp_normat | Número ID que identifica o Dispositivo Normativo. |
| descricao | Descrição textual do registro. |
| dispositivo | Identificação do dispositivo (artigo, inciso etc.) dentro da norma. |
| norma | Nome/identificação da norma do Dispositivo Normativo (ex.: nome da lei ou regulamento). |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_revogado | Variável categórica que indica se o Dispositivo Normativo está revogado:<br><br><ul><li>S = Revogado</li><li>N = Não revogado</li></ul> |
| url | Endereço (URL) de referência do Dispositivo Normativo. |

## md_lit_especie_decisao

Armazena as espécies de decisão vinculadas a um Tipo de Decisão, que definem o comportamento da decisão no cadastro (por exemplo, se enseja gestão de multa, indicação de prazo, indicação de obrigações ou indicação de valor).

| Coluna | Descrição |
|---|---|
| id_md_lit_especie_decisao | Número ID que identifica a Espécie de Decisão. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_rd_gestao_multa | Variável categórica que indica se a Espécie de Decisão participa da Gestão de Multa:<br><br><ul><li>S = Participa da Gestão de Multa</li><li>N = Não participa da Gestão de Multa</li></ul> |
| sin_rd_indicacao_obrigacoes | Variável categórica que indica se a Espécie de Decisão indica obrigações:<br><br><ul><li>S = Indica obrigações</li><li>N = Não indica obrigações</li></ul> |
| sin_rd_indicacao_prazo | Variável categórica que indica se a Espécie de Decisão indica prazo:<br><br><ul><li>S = Indica prazo</li><li>N = Não indica prazo</li></ul> |
| sin_valor | Variável categórica que indica se a Espécie de Decisão exige indicação de valor:<br><br><ul><li>S = Exige indicação de valor</li><li>N = Não exige indicação de valor</li></ul> |
| sta_tipo_indicacao_multa | Status multi-valorado que identifica o tipo de indicação de multa da Espécie de Decisão:<br><br><ul><li>1 = Integração</li><li>2 = Indicação de Valor</li></ul> |

## md_lit_fase

Armazena as fases parametrizadas para um tipo de controle litigioso (por exemplo, Instauração, Instrução, Decisória, Recursal, Trânsito em Julgado). Cada Situação do processo pertence a uma Fase.

| Coluna | Descrição |
|---|---|
| id_md_lit_fase | Número ID que identifica a Fase do Tipo de Controle Litigioso. |
| descricao | Descrição textual do registro. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso ao qual a Fase pertence, faz referência à tabela `md_lit_tipo_controle`. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_funcionalidade

Armazena as funcionalidades de integração disponibilizadas pelo módulo (por exemplo, consulta de lançamento, dados complementares do interessado), utilizadas para vincular Integrações e Campos de Integração.

| Coluna | Descrição |
|---|---|
| id_md_lit_funcionalidade | Número ID que identifica a Funcionalidade. |
| nome | Nome do registro. |

## md_lit_historic_lancamento

Armazena o histórico de alterações de um Lançamento de crédito, preservando o estado dos dados do lançamento a cada atualização (por exemplo, a cada retorno da integração com o sistema de arrecadação).

| Coluna | Descrição |
|---|---|
| id_md_lit_historic_lancamento | Número ID que identifica o histórico de Lançamento de crédito. |
| codigo_receita | Código de receita utilizado na integração com o sistema de arrecadação. |
| dta_apresentacao_recurso | Data de apresentação do recurso. |
| dta_constituicao_definitiva | Data da constituição definitiva do crédito. |
| dta_decisao | Data da Decisão registrada no Lançamento. |
| dta_decisao_definitiva | Data em que a Decisão se tornou definitiva. |
| dta_intimacao | Data da intimação registrada no Lançamento. |
| dta_intimacao_definitiva | Data em que a intimação se tornou definitiva. |
| dta_prazo_defesa | Data-limite do prazo de defesa do Lançamento. |
| dta_ultimo_pagamento | Data do último pagamento registrado para o Lançamento. |
| dta_vencimento | Data de vencimento do Lançamento de crédito. |
| dth_inclusao | Data/hora de inclusão do registro. |
| id_md_lit_integracao | Número ID que identifica a Integração, faz referência à tabela `md_lit_integracao`. |
| id_md_lit_lancamento | Número ID que identifica o Lançamento de crédito, faz referência à tabela `md_lit_lancamento`. |
| id_md_lit_numero_interessado | Número ID que identifica o Número do Interessado, faz referência à tabela `md_lit_numero_interessado`. |
| id_md_lit_sit_dec_def | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_md_lit_situacao_lancamento | Número ID que identifica a Situação de Lançamento, faz referência à tabela `md_lit_situacao_lancamento`. |
| id_procedimento | Número ID que identifica o processo (procedimento), faz referência à tabela `procedimento`, do núcleo do SEI. |
| id_situacao_decisao | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_situacao_intimacao | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_situacao_recurso | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_unidade | Número ID que identifica a unidade, faz referência à tabela `unidade`, do núcleo do SEI. |
| id_usuario | Número ID que identifica o usuário, faz referência à tabela `usuario`, do núcleo do SEI. |
| justificativa | Texto de justificativa informado pelo usuário. |
| link_boleto | Endereço (URL) do boleto de cobrança do Lançamento. |
| num_doc_decisao_multa | Número do documento SEI da decisão que aplicou a multa. |
| numero_interessado | Número do interessado associado ao Lançamento (ex.: número de outorga/Fistel), copiado no momento do lançamento. |
| prazo_defesa | Prazo (em dias) para apresentação de defesa. |
| prazo_recurso | Prazo (em dias) para apresentação de recurso. |
| sequencial | Número sequencial do Lançamento. |
| sin_constituicao_definitiva | Variável categórica que indica se houve constituição definitiva do crédito:<br><br><ul><li>S = Houve constituição definitiva do crédito</li><li>N = Não houve constituição definitiva do crédito</li></ul> |
| sin_renuncia_recorrer | Variável categórica que indica se houve renúncia ao direito de recorrer:<br><br><ul><li>S = Houve renúncia ao direito de recorrer</li><li>N = Não houve renúncia ao direito de recorrer</li></ul> |
| sin_suspenso | Variável categórica que indica se o Lançamento está suspenso:<br><br><ul><li>S = Suspenso</li><li>N = Não suspenso</li></ul> |
| tipo_lancamento | Tipo do lançamento de crédito. |
| tp_prazo_defesa | Indica se o prazo de defesa é contado em dias úteis ou em dias corridos. |
| tp_prazo_recurso | Indica se o prazo de recurso é contado em dias úteis ou em dias corridos. |
| vlr_desconto | Valor de desconto aplicado ao Lançamento. |
| vlr_lancamento | Valor do Lançamento de crédito. |
| vlr_pago | Valor pago referente ao Lançamento. |
| vlr_saldo_devedor | Saldo devedor remanescente do Lançamento. |

## md_lit_integracao

Armazena as integrações (webservices) cadastradas para automatizar a gestão e cobrança de multas com o sistema de arrecadação, associadas a uma Funcionalidade.

| Coluna | Descrição |
|---|---|
| id_md_lit_integracao | Número ID que identifica a Integração. |
| endereco_wsdl | Endereço (URL) do WSDL do webservice de integração. |
| id_md_lit_funcionalidade | Número ID que identifica a Funcionalidade, faz referência à tabela `md_lit_funcionalidade`. |
| nome | Nome do registro. |
| operaca_wsdl | Nome da operação do webservice de integração invocada. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_vincular_lancamento | Variável categórica que indica se a Integração deve vincular Lançamentos de crédito:<br><br><ul><li>S = Deve vincular Lançamentos de crédito</li><li>N = Não deve vincular Lançamentos de crédito</li></ul> |
| tipo_cliente_ws | Indica o tipo de cliente SOAP utilizado pela Integração. |
| versao_soap | Indica a versão do protocolo SOAP utilizada pela Integração. |

## md_lit_lancamento

Armazena os lançamentos de crédito (cobranças de multa) gerados a partir de uma decisão, incluindo valores, prazos, datas de intimação/vencimento/pagamento e, quando houver integração, os dados de retorno do sistema de arrecadação.

| Coluna | Descrição |
|---|---|
| id_md_lit_lancamento | Número ID que identifica o Lançamento de crédito. |
| codigo_receita | Código de receita utilizado na integração com o sistema de arrecadação. |
| dta_apresentacao_recurso | Data de apresentação do recurso. |
| dta_constituicao_definitiva | Data da constituição definitiva do crédito. |
| dta_decisao | Data da Decisão registrada no Lançamento. |
| dta_decisao_definitiva | Data em que a Decisão se tornou definitiva. |
| dta_decurso_prazo_recurso | Data do decurso do prazo de recurso. |
| dta_intimacao | Data da intimação registrada no Lançamento. |
| dta_intimacao_definitiva | Data em que a intimação se tornou definitiva. |
| dta_prazo_defesa | Data-limite do prazo de defesa do Lançamento. |
| dta_ultimo_pagamento | Data do último pagamento registrado para o Lançamento. |
| dta_vencimento | Data de vencimento do Lançamento de crédito. |
| dth_inclusao | Data/hora de inclusão do registro. |
| id_md_lit_integracao | Número ID que identifica a Integração, faz referência à tabela `md_lit_integracao`. |
| id_md_lit_numero_interessado | Número ID que identifica o Número do Interessado, faz referência à tabela `md_lit_numero_interessado`. |
| id_md_lit_sit_dec_def | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_md_lit_situacao_lancamento | Número ID que identifica a Situação de Lançamento, faz referência à tabela `md_lit_situacao_lancamento`. |
| id_procedimento | Número ID que identifica o processo (procedimento), faz referência à tabela `procedimento`, do núcleo do SEI. |
| id_situacao_decisao | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_situacao_intimacao | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_situacao_recurso | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação), faz referência à tabela `md_lit_processo_situacao`. |
| id_unidade | Número ID que identifica a unidade, faz referência à tabela `unidade`, do núcleo do SEI. |
| id_usuario | Número ID que identifica o usuário, faz referência à tabela `usuario`, do núcleo do SEI. |
| justificativa | Texto de justificativa informado pelo usuário. |
| link_boleto | Endereço (URL) do boleto de cobrança do Lançamento. |
| num_doc_decisao_multa | Número do documento SEI da decisão que aplicou a multa. |
| numero_interessado | Número do interessado associado ao Lançamento (ex.: número de outorga/Fistel), copiado no momento do lançamento. |
| prazo_defesa | Prazo (em dias) para apresentação de defesa. |
| prazo_recurso | Prazo (em dias) para apresentação de recurso. |
| sequencial | Número sequencial do Lançamento. |
| sin_constituicao_definitiva | Variável categórica que indica se houve constituição definitiva do crédito:<br><br><ul><li>S = Houve constituição definitiva do crédito</li><li>N = Não houve constituição definitiva do crédito</li></ul> |
| sin_renuncia_recorrer | Variável categórica que indica se houve renúncia ao direito de recorrer:<br><br><ul><li>S = Houve renúncia ao direito de recorrer</li><li>N = Não houve renúncia ao direito de recorrer</li></ul> |
| sin_suspenso | Variável categórica que indica se o Lançamento está suspenso:<br><br><ul><li>S = Suspenso</li><li>N = Não suspenso</li></ul> |
| tipo_lancamento | Tipo do lançamento de crédito. |
| tp_prazo_defesa | Indica se o prazo de defesa é contado em dias úteis ou em dias corridos. |
| tp_prazo_recurso | Indica se o prazo de recurso é contado em dias úteis ou em dias corridos. |
| vlr_desconto | Valor de desconto aplicado ao Lançamento. |
| vlr_lancamento | Valor do Lançamento de crédito. |
| vlr_pago | Valor pago referente ao Lançamento. |
| vlr_saldo_devedor | Saldo devedor remanescente do Lançamento. |

## md_lit_mapea_param_entrada

Armazena o mapeamento dos parâmetros de entrada (campos enviados) de uma Integração, relacionando o Nome Funcional do módulo com o campo correspondente no webservice externo.

| Coluna | Descrição |
|---|---|
| id_md_lit_mapea_param_entrada | Número ID que identifica o mapeamento de parâmetro de entrada. |
| campo | Nome do campo mapeado no parâmetro de entrada/saída da integração. |
| chave_unica | Variável categórica que indica se o campo/mapeamento funciona como chave única de identificação na integração (S) ou não (N). |
| id_md_lit_campo_integracao | Número ID que identifica o Campo de Integração, faz referência à tabela `md_lit_campo_integracao`. |
| id_md_lit_integracao | Número ID que identifica a Integração, faz referência à tabela `md_lit_integracao`. |
| id_md_lit_nome_funcional | Número ID que identifica o Nome Funcional, faz referência à tabela `md_lit_nome_funcional`. |

## md_lit_mapea_param_saida

Armazena o mapeamento dos parâmetros de saída (campos de retorno) de uma Integração, relacionando o Nome Funcional do módulo com o campo correspondente no webservice externo.

| Coluna | Descrição |
|---|---|
| id_md_lit_mapea_param_saida | Número ID que identifica o mapeamento de parâmetro de saída. |
| campo | Nome do campo mapeado no parâmetro de entrada/saída da integração. |
| chave_unica | Variável categórica que indica se o campo/mapeamento funciona como chave única de identificação na integração (S) ou não (N). |
| id_md_lit_campo_integracao | Número ID que identifica o Campo de Integração, faz referência à tabela `md_lit_campo_integracao`. |
| id_md_lit_integracao | Número ID que identifica a Integração, faz referência à tabela `md_lit_integracao`. |
| id_md_lit_nome_funcional | Número ID que identifica o Nome Funcional, faz referência à tabela `md_lit_nome_funcional`. |

## md_lit_mapea_param_valor

Armazena o valor padrão (default) de um parâmetro de entrada mapeado, por Tipo de Controle Litigioso, utilizado quando não houver valor informado a ser enviado na integração.

| Coluna | Descrição |
|---|---|
| id_md_lit_mapea_param_valor | Número ID que identifica o valor padrão de parâmetro de entrada. |
| id_md_lit_mapea_param_entrada | Número ID que identifica o mapeamento de parâmetro de entrada, faz referência à tabela `md_lit_mapea_param_entrada`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| valor_default | Valor padrão do parâmetro de entrada para o Tipo de Controle Litigioso. |

## md_lit_motivo

Armazena os motivos de instauração que podem ser associados a um Tipo de Controle Litigioso e, quando associados, tornam-se de indicação obrigatória nos processos daquele tipo de controle.

| Coluna | Descrição |
|---|---|
| id_md_lit_motivo | Número ID que identifica o Motivo de Instauração. |
| descricao | Descrição textual do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_nome_funcional

Armazena os nomes funcionais (rótulos de campo) internos do módulo, utilizados na parametrização de Dados do Interessado e no mapeamento de parâmetros de integração.

| Coluna | Descrição |
|---|---|
| id_md_lit_nome_funcional | Número ID que identifica o Nome Funcional. |
| nome | Nome do registro. |

## md_lit_numero_interessado

Armazena os números de complemento do interessado (por exemplo, números de serviços/outorgas) vinculados a um Dado do Interessado.

| Coluna | Descrição |
|---|---|
| id_md_lit_numero_interessado | Número ID que identifica o Número do Interessado. |
| id_md_lit_dado_interessado | Número ID que identifica o Dado do Interessado, faz referência à tabela `md_lit_dado_interessado`. |
| numero | Número (por exemplo, número de outorga/Fistel) que identifica o interessado. |

## md_lit_obrigacao

Armazena as obrigações que podem ser aplicadas em decorrência de uma decisão, associadas a uma ou mais Espécies de Decisão.

| Coluna | Descrição |
|---|---|
| id_md_lit_obrigacao | Número ID que identifica a Obrigação. |
| descricao | Descrição textual do registro. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_param_interessado

Armazena a parametrização, por Tipo de Controle Litigioso, de quais Dados do Interessado (Nomes Funcionais) devem ser exibidos e/ou são de preenchimento obrigatório no cadastro do processo, incluindo rótulo, tamanho e texto de ajuda do campo.

| Coluna | Descrição |
|---|---|
| id_md_lit_param_interessado | Número ID que identifica a parametrização de campo do Dado do Interessado. |
| descricao_ajuda | Texto de ajuda exibido ao usuário para o preenchimento do campo. |
| id_md_lit_nome_funcional | Número ID que identifica o Nome Funcional, faz referência à tabela `md_lit_nome_funcional`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| label_campo | Rótulo exibido para o campo do Dado do Interessado na tela de cadastro do processo. |
| sin_campo_mapeado | Variável categórica que indica se o campo está mapeado por integração:<br><br><ul><li>S = Mapeado por integração</li><li>N = Não mapeado por integração</li></ul> |
| sin_exibe | Variável categórica que indica se o campo do Dado do Interessado é exibido na tela do processo, para o Tipo de Controle Litigioso:<br><br><ul><li>S = Exibido</li><li>N = Não exibido</li></ul> |
| sin_obrigatorio | Variável categórica que indica se o preenchimento é obrigatório:<br><br><ul><li>S = Obrigatório</li><li>N = Não obrigatório</li></ul> |
| tamanho | Tamanho (quantidade de caracteres) permitido para o campo. |

## md_lit_processo_situacao

Armazena cada movimentação (marcação de Situação) registrada em um processo/procedimento sob controle litigioso, incluindo as datas que compõem os prazos de prescrição intercorrente e quinquenal e os dados de depósito extrajudicial.

| Coluna | Descrição |
|---|---|
| id_md_lit_processo_situacao | Número ID que identifica o andamento do processo em uma Situação (Processo/Situação). |
| deposito_extrajudicial | Variável categórica que indica se houve depósito extrajudicial (S) ou não (N). |
| dta_data | Data de referência do andamento (Processo/Situação). |
| dta_deposito_extrajudicial | Data do depósito extrajudicial. |
| dta_intecorrente | Data de referência para a contagem da prescrição intercorrente do processo. |
| dta_quinquenal | Data de referência para a contagem da prescrição quinquenal do processo. |
| dth_inclusao | Data/hora de inclusão do registro. |
| id_documento | Número ID que identifica o documento, faz referência à tabela `documento`, do núcleo do SEI. |
| id_md_lit_situacao | Número ID que identifica a Situação, faz referência à tabela `md_lit_situacao`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| id_procedimento | Número ID que identifica o processo (procedimento), faz referência à tabela `procedimento`, do núcleo do SEI. |
| id_unidade | Número ID que identifica a unidade, faz referência à tabela `unidade`, do núcleo do SEI. |
| id_usuario | Número ID que identifica o usuário, faz referência à tabela `usuario`, do núcleo do SEI. |
| prazo | Prazo (em dias) associado ao registro. |
| sin_altera_prescricao | Variável categórica que indica se a Situação altera a contagem do prazo de prescrição:<br><br><ul><li>S = Altera a contagem do prazo de prescrição</li><li>N = Não altera a contagem do prazo de prescrição</li></ul> |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tp_prazo | Indica se o prazo informado é contado em dias úteis ou em dias corridos. |
| valor_deposito_extrajudicial | Valor do depósito extrajudicial. |

## md_lit_reinciden_anteceden

Armazena as parametrizações gerais de Reincidência Específica e de Antecedente (prazo considerado e orientação de preenchimento), utilizadas nos botões correspondentes do cadastro das decisões das Situações do processo.

| Coluna | Descrição |
|---|---|
| id_md_lit_reinciden_anteceden | Número ID que identifica a parametrização de Reincidência/Antecedente. |
| orientacao | Texto de orientação sobre a regra de Reincidência/Antecedente, exibido ao usuário. |
| prazo | Prazo (em dias) associado ao registro. |
| tipo | Status multi-valorado que identifica o tipo de parametrização:<br><br><ul><li>R = Reincidência Específica</li><li>A = Antecedente</li></ul> |
| tp_regra_reincidencia | Status multi-valorado que identifica a regra de contagem de Reincidência/Antecedente:<br><br><ul><li>1 = Mesma Conduta</li><li>2 = Mesmo Dispositivo Normativo</li><li>3 = Mesmo Dispositivo Normativo e Conduta</li></ul> |

## md_lit_rel_controle_motivo

Tabela associativa entre o Controle Litigioso e o Motivo de Instauração, registrando os motivos indicados na instauração de um processo.

| Coluna | Descrição |
|---|---|
| id_md_lit_controle | Número ID que identifica o Controle (processo), faz referência à tabela `md_lit_controle`. |
| id_md_lit_motivo | Número ID que identifica o Motivo de Instauração, faz referência à tabela `md_lit_motivo`. |

## md_lit_rel_decis_lancament

Tabela associativa entre a Decisão e o Lançamento de crédito, vinculando cada decisão ao(s) lançamento(s) de multa dela decorrente(s).

| Coluna | Descrição |
|---|---|
| id_md_lit_decisao | Número ID que identifica a Decisão, faz referência à tabela `md_lit_decisao`. |
| id_md_lit_lancamento | Número ID que identifica o Lançamento de crédito, faz referência à tabela `md_lit_lancamento`. |

## md_lit_rel_decisao_uf

Associa uma Decisão à(s) UF(s) às quais ela se aplica.

| Coluna | Descrição |
|---|---|
| id_md_lit_decisao | Número ID que identifica a Decisão, faz referência à tabela `md_lit_decisao`. |
| id_uf | Número ID que identifica a UF, faz referência à tabela `uf`, do núcleo do SEI. |

## md_lit_rel_dis_nor_con_ctr

Armazena o vínculo entre o Dispositivo Normativo, a Conduta e o Controle Litigioso, representando a infração normativa imputada no processo, incluindo a data (ou período) em que a infração ocorreu.

| Coluna | Descrição |
|---|---|
| id_md_lit_rel_dis_nor_con_ctr | Número ID que identifica a infração (Dispositivo Normativo/Conduta/Controle). |
| dta_infracao | Data em que a infração ocorreu (quando pontual). |
| dta_infracao_periodo_final | Data final do período em que a infração ocorreu (quando a infração se estende por um período). |
| dta_infracao_periodo_inicial | Data inicial do período em que a infração ocorreu (quando a infração se estende por um período). |
| id_md_lit_conduta | Número ID que identifica a Conduta, faz referência à tabela `md_lit_conduta`. |
| id_md_lit_controle | Número ID que identifica o Controle (processo), faz referência à tabela `md_lit_controle`. |
| id_md_lit_disp_normat | Número ID que identifica o Dispositivo Normativo, faz referência à tabela `md_lit_disp_normat`. |
| sta_infracao_data | Status multi-valorado que identifica a data da infração registrada:<br><br><ul><li>E = Infração com data específica</li><li>P = Infração por período</li></ul> |

## md_lit_rel_disp_norm_conduta

Tabela associativa entre o Dispositivo Normativo e a Conduta, definindo quais condutas estão disponíveis para vinculação a cada dispositivo normativo.

| Coluna | Descrição |
|---|---|
| id_md_lit_conduta | Número ID que identifica a Conduta, faz referência à tabela `md_lit_conduta`. |
| id_md_lit_disp_normat | Número ID que identifica o Dispositivo Normativo, faz referência à tabela `md_lit_disp_normat`. |

## md_lit_rel_disp_norm_revogado

Tabela associativa que registra a revogação de um Dispositivo Normativo por outro, vinculando o dispositivo normativo revogado ao dispositivo normativo que o revogou.

| Coluna | Descrição |
|---|---|
| id_md_lit_disp_normat | Número ID que identifica o Dispositivo Normativo, faz referência à tabela `md_lit_disp_normat`. |
| id_md_lit_disp_normat_revogado | Número ID que identifica o Dispositivo Normativo, faz referência à tabela `md_lit_disp_normat`. |

## md_lit_rel_disp_norm_tipo_ctrl

Tabela associativa entre o Dispositivo Normativo e o Tipo de Controle Litigioso, definindo quais dispositivos normativos estão disponíveis para vinculação em cada tipo de controle.

| Coluna | Descrição |
|---|---|
| id_md_lit_disp_normat | Número ID que identifica o Dispositivo Normativo, faz referência à tabela `md_lit_disp_normat`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |

## md_lit_rel_esp_decisao_obr

Tabela associativa entre a Espécie de Decisão e a Obrigação, definindo quais obrigações estão disponíveis para indicação em cada espécie de decisão.

| Coluna | Descrição |
|---|---|
| id_md_lit_especie_decisao | Número ID que identifica a Espécie de Decisão associada, faz referência à tabela `md_lit_especie_decisao`. |
| id_md_lit_obrigacao | Número ID que identifica a Obrigação associada, faz referência à tabela `md_lit_obrigacao`. |

## md_lit_rel_num_inter_modali

Tabela associativa entre o Número do Interessado e a Modalidade de Outorga.

| Coluna | Descrição |
|---|---|
| id_md_lit_adm_modalidad_outor | Número ID que identifica a Modalidade de Outorga, faz referência à tabela `md_lit_adm_modalidad_outor`. |
| id_md_lit_numero_interessado | Número ID que identifica o Número do Interessado, faz referência à tabela `md_lit_numero_interessado`. |

## md_lit_rel_num_inter_servico

Tabela associativa entre o Número do Interessado e o Serviço Outorgado.

| Coluna | Descrição |
|---|---|
| id_md_lit_numero_interessado | Número ID que identifica o Número do Interessado, faz referência à tabela `md_lit_numero_interessado`. |
| id_md_lit_servico | Número ID que identifica o Serviço outorgado, faz referência à tabela `md_lit_servico`. |

## md_lit_rel_num_inter_tp_outor

Tabela associativa entre o Número do Interessado e o Tipo de Outorga.

| Coluna | Descrição |
|---|---|
| id_md_lit_adm_tipo_outor | Número ID que identifica o Tipo de Outorga, faz referência à tabela `md_lit_adm_tipo_outor`. |
| id_md_lit_numero_interessado | Número ID que identifica o Número do Interessado, faz referência à tabela `md_lit_numero_interessado`. |

## md_lit_rel_opc_camp_mult

Associa a(s) opção(ões) de seleção múltipla efetivamente escolhida(s) em um preenchimento de Campo Adicional do tipo Múltipla Seleção.

| Coluna | Descrição |
|---|---|
| id_md_lit_campos_ad_form | Número ID que identifica o preenchimento de Campo Adicional, faz referência à tabela `md_lit_campos_ad_form`. |
| id_md_lit_campos_ad_sel | Número ID que identifica a opção de Campo Adicional, faz referência à tabela `md_lit_campos_ad_sel`. |

## md_lit_rel_protoco_protoco

Tabela associativa entre dois protocolos (processos/documentos) do SEI, utilizada para registrar o vínculo de sobrestamento de um processo em razão de outro, no âmbito de um Controle Litigioso.

| Coluna | Descrição |
|---|---|
| id_md_lit_rel_protoco_protoco | Número ID que identifica a relação de sobrestamento entre protocolos. |
| dta_sobrestamento | Data do sobrestamento (suspensão) registrado entre os dois protocolos. |
| id_documento | Número ID que identifica o documento, faz referência à tabela `documento`, do núcleo do SEI. |
| id_md_lit_controle | Número ID que identifica o Controle (processo), faz referência à tabela `md_lit_controle`. |
| id_protocolo_1 | Número ID do primeiro protocolo (processo/documento) da relação de sobrestamento, faz referência à tabela `protocolo`, do núcleo do SEI. |
| id_protocolo_2 | Número ID do segundo protocolo (processo/documento) da relação de sobrestamento, faz referência à tabela `protocolo`, do núcleo do SEI. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_rel_sit_serie

Tabela associativa entre a Situação e a Série (tipo de documento do SEI), definindo os tipos de documento sugeridos/vinculados a uma situação do processo.

| Coluna | Descrição |
|---|---|
| id_md_lit_situacao | Número ID que identifica a Situação, faz referência à tabela `md_lit_situacao`. |
| id_serie | Número ID que identifica a série (tipo de documento), faz referência à tabela `serie`, do núcleo do SEI. |

## md_lit_rel_tipo_ctrl_tipo_dec

Tabela associativa entre o Tipo de Decisão, o Tipo de Controle Litigioso e a Espécie de Decisão, definindo quais combinações de tipo/espécie de decisão estão disponíveis em cada tipo de controle.

| Coluna | Descrição |
|---|---|
| id_md_lit_especie_decisao | Número ID que identifica a Espécie de Decisão, faz referência à tabela `md_lit_especie_decisao`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| id_md_lit_tipo_decisao | Número ID que identifica o Tipo de Decisão, faz referência à tabela `md_lit_tipo_decisao`. |

## md_lit_rel_tp_control_moti

Tabela associativa entre o Tipo de Controle Litigioso e o Motivo de Instauração, definindo quais motivos estão disponíveis para indicação em cada tipo de controle.

| Coluna | Descrição |
|---|---|
| id_md_lit_motivo | Número ID que identifica o Motivo de Instauração, faz referência à tabela `md_lit_motivo`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |

## md_lit_rel_tp_controle_proced

Tabela associativa entre o Tipo de Controle Litigioso e o Tipo de Processo do SEI, definindo em quais tipos de processo o tipo de controle litigioso pode ser instaurado.

| Coluna | Descrição |
|---|---|
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| id_tipo_procedimento | Número ID que identifica o tipo de procedimento, faz referência à tabela `tipo_procedimento`, do núcleo do SEI. |

## md_lit_rel_tp_controle_unid

Tabela associativa entre o Tipo de Controle Litigioso e a Unidade organizacional, definindo quais unidades têm acesso de administração ao tipo de controle.

| Coluna | Descrição |
|---|---|
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| id_unidade | Número ID que identifica a unidade, faz referência à tabela `unidade`, do núcleo do SEI. |

## md_lit_rel_tp_controle_usu

Tabela associativa entre o Tipo de Controle Litigioso e o Usuário, definindo quais usuários têm acesso de administração ao tipo de controle.

| Coluna | Descrição |
|---|---|
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| id_usuario | Número ID que identifica o usuário, faz referência à tabela `usuario`, do núcleo do SEI. |

## md_lit_rel_tp_ctrl_proc_sobres

Tabela associativa entre o Tipo de Controle Litigioso e o Tipo de Processo do SEI, definindo em quais tipos de processo pode ser registrado o sobrestamento vinculado ao tipo de controle.

| Coluna | Descrição |
|---|---|
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| id_tipo_procedimento | Número ID que identifica o tipo de procedimento, faz referência à tabela `tipo_procedimento`, do núcleo do SEI. |

## md_lit_rel_tp_dec_rein_ante

Tabela associativa entre o Tipo de Decisão e a parametrização de Reincidência/Antecedente, definindo em quais tipos de decisão a reincidência/antecedente parametrizada pode ser utilizada.

| Coluna | Descrição |
|---|---|
| id_md_lit_reinciden_anteceden | Número ID que identifica a parametrização de Reincidência/Antecedente, faz referência à tabela `md_lit_reinciden_anteceden`. |
| id_md_lit_tipo_decisao | Número ID que identifica o Tipo de Decisão, faz referência à tabela `md_lit_tipo_decisao`. |

## md_lit_rel_tp_especie_dec

Tabela associativa entre o Tipo de Decisão e a Espécie de Decisão, definindo quais espécies de decisão estão disponíveis para cada tipo de decisão.

| Coluna | Descrição |
|---|---|
| id_md_lit_especie_decisao | Número ID que identifica a Espécie de Decisão, faz referência à tabela `md_lit_especie_decisao`. |
| id_md_lit_tipo_decisao | Número ID que identifica o Tipo de Decisão, faz referência à tabela `md_lit_tipo_decisao`. |

## md_lit_servico

Armazena os serviços outorgados pelo órgão, cadastrados manualmente ou via integração, que são objeto do controle litigioso.

| Coluna | Descrição |
|---|---|
| id_md_lit_servico | Número ID que identifica o Serviço outorgado. |
| codigo | Código que identifica o registro. |
| descricao | Descrição textual do registro. |
| id_md_lit_servico_integracao | Número ID que identifica a integração de Serviço, faz referência à tabela `md_lit_servico_integracao`. |
| sigla | Sigla que identifica o registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_ativo_integracao | Variável categórica que indica se a integração/mapeamento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_origem | Status multi-valorado que identifica a origem do registro:<br><br><ul><li>M = Manual</li><li>I = Integração</li></ul> |

## md_lit_servico_integracao

Armazena as configurações de integração (webservice) utilizadas para importar/atualizar automaticamente os Serviços Outorgados a partir de um sistema externo.

| Coluna | Descrição |
|---|---|
| id_md_lit_servico_integracao | Número ID que identifica a integração de Serviço. |
| chave_unica | Variável categórica que indica se o campo/mapeamento funciona como chave única de identificação na integração (S) ou não (N) |
| endereco_wsdl | Endereço (URL) do WSDL do webservice de integração. |
| mapeamento_codigo | Nome do campo de retorno do webservice mapeado para o código do Serviço. |
| mapeamento_descricao | Nome do campo de retorno do webservice mapeado para a descrição do Serviço/Situação. |
| mapeamento_sigla | Nome do campo de retorno do webservice mapeado para a sigla do Serviço. |
| mapeamento_situacao | Nome do campo de retorno do webservice mapeado para a situação do Serviço. |
| nome_integracao | Nome da integração de Serviço. |
| operacao_wsdl | Nome da operação do webservice de integração invocada. |
| tipo_cliente_ws | Indica o tipo de cliente SOAP utilizado pela integração de Serviço. |
| versao_soap | Indica a versão do protocolo SOAP utilizada pela integração de Serviço. |

## md_lit_situacao

Armazena as situações parametrizadas para um tipo de controle litigioso, associadas a uma Fase, que compõem o fluxo processual utilizado para marcar a movimentação do processo/procedimento no módulo (por exemplo, Instauração, Apresentação de Defesa, Formalização da Decisão, Trânsito em Julgado).

| Coluna | Descrição |
|---|---|
| id_md_lit_situacao | Número ID que identifica a Situação. |
| id_md_lit_fase | Número ID que identifica a Fase do Tipo de Controle Litigioso, faz referência à tabela `md_lit_fase`. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso, faz referência à tabela `md_lit_tipo_controle`. |
| nome | Nome do registro. |
| ordem | Número que define a ordem de apresentação do registro. |
| prazo | Prazo (em dias) associado ao registro. |
| sin_alegacoes | Variável categórica que indica se a Situação é de alegações finais:<br><br><ul><li>S = De alegações finais</li><li>N = Não de alegações finais</li></ul> |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_conclusiva | Variável categórica que indica se a Situação é conclusiva para o processo:<br><br><ul><li>S = Conclusiva para o processo</li><li>N = Não conclusiva para o processo</li></ul> |
| sin_decisoria | Variável categórica que indica se a Situação é decisória, ou seja, admite o registro de Decisões:<br><br><ul><li>S = Decisória, ou seja, admite o registro de Decisões</li><li>N = Não decisória, ou seja, admite o registro de Decisões</li></ul> |
| sin_defesa | Variável categórica que indica se a Situação é de apresentação de defesa:<br><br><ul><li>S = De apresentação de defesa</li><li>N = Não de apresentação de defesa</li></ul> |
| sin_instauracao | Variável categórica que indica se a Situação é de instauração do processo:<br><br><ul><li>S = De instauração do processo</li><li>N = Não de instauração do processo</li></ul> |
| sin_intimacao | Variável categórica que indica se a Situação é de intimação:<br><br><ul><li>S = De intimação</li><li>N = Não de intimação</li></ul> |
| sin_obrigatoria | Variável categórica que indica se a Situação é obrigatória:<br><br><ul><li>S = Obrigatória</li><li>N = Não obrigatória</li></ul> |
| sin_opcional | Variável categórica que indica se a Situação é opcional no fluxo do processo:<br><br><ul><li>S = Opcional no fluxo do processo</li><li>N = Não opcional no fluxo do processo</li></ul> |
| sin_recursal | Variável categórica que indica se a Situação é de fase recursal:<br><br><ul><li>S = De fase recursal</li><li>N = Não de fase recursal</li></ul> |
| tp_prazo | Indica se o prazo informado é contado em dias úteis ou em dias corridos. |

## md_lit_situacao_lancam_int

Armazena as configurações de integração (webservice) utilizadas para consultar a situação de um lançamento de crédito junto ao sistema de arrecadação.

| Coluna | Descrição |
|---|---|
| id_md_lit_situacao_lancam_int | Número ID que identifica a integração de Situação de Lançamento. |
| chave_unica | Variável categórica que indica se o campo/mapeamento funciona como chave única de identificação na integração (S) ou não (N) |
| endereco_wsdl | Endereço (URL) do WSDL do webservice de integração. |
| mapeamento_codigo | Nome do campo de retorno do webservice mapeado para o código da Situação de Lançamento. |
| mapeamento_descricao | Nome do campo de retorno do webservice mapeado para a descrição da Situação de Lançamento. |
| nome_integracao | Nome da integração de Situação de Lançamento. |
| operacao_wsdl | Nome da operação do webservice de integração invocada. |
| tipo_cliente_ws | Indica o tipo de cliente SOAP utilizado pela integração de Situação de Lançamento. |
| versao_soap | Indica a versão do protocolo SOAP utilizada pela integração de Situação de Lançamento. |

## md_lit_situacao_lancamento

Armazena as situações do lançamento de crédito, associando-as à cor de apresentação do texto na seção de Gestão de Multa e, quando houver integração por webservice com o sistema de arrecadação, à respectiva Situação de Lançamento de Integração.

| Coluna | Descrição |
|---|---|
| id_md_lit_situacao_lancamento | Número ID que identifica a Situação de Lançamento. |
| codigo | Código que identifica o registro. |
| cor_situacao | Cor utilizada para exibir a Situação de Lançamento na seção de Gestão de Multa. |
| id_md_lit_situacao_lancam_int | Número ID que identifica a integração de Situação de Lançamento, faz referência à tabela `md_lit_situacao_lancam_int`. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_ativo_integracao | Variável categórica que indica se a integração/mapeamento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_cancelamento | Variável categórica que indica se a Situação de Lançamento permite cancelamento:<br><br><ul><li>S = Permite cancelamento</li><li>N = Não permite cancelamento</li></ul> |
| sin_utilizar_agendamento | Variável categórica que indica se a Situação de Lançamento é utilizada no agendamento automático:<br><br><ul><li>S = Utilizada no agendamento automático</li><li>N = Não utilizada no agendamento automático</li></ul> |
| sta_origem | Status multi-valorado que identifica a origem do registro:<br><br><ul><li>M = Manual</li><li>I = Integração</li></ul> |

## md_lit_tipo_controle

Armazena os tipos de controle litigioso cadastrados pelo órgão (por exemplo, PADO, PAF, Sanção Contratual, Sanção de Licitação, Ressarcimento a Consumidores). É a tabela principal de parametrização do módulo: cada tipo de controle litigioso é independente e possui suas próprias Fases, Situações, Dispositivos Normativos e Tipos de Decisão associados.

| Coluna | Descrição |
|---|---|
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso. |
| descricao | Descrição textual do registro. |
| dta_corte | Data de corte a partir da qual o Tipo de Controle Litigioso passou a valer/ser aplicado. |
| sigla | Sigla que identifica o registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_param_modal_compl_interes | Variável categórica que indica se o Tipo de Controle Litigioso parametriza Modalidade como campo complementar do Interessado:<br><br><ul><li>S = Parametriza Modalidade como campo complementar do Interessado</li><li>N = Não parametriza Modalidade como campo complementar do Interessado</li></ul> |

## md_lit_tipo_decisao

Armazena os tipos de decisão que podem ser proferidos nas situações do tipo Decisória parametrizadas no controle litigioso.

| Coluna | Descrição |
|---|---|
| id_md_lit_tipo_decisao | Número ID que identifica o Tipo de Decisão. |
| descricao | Descrição textual do registro. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_lit_tp_info_add

Cadastro dos Tipos de Informação Adicional, utilizados para agrupar os Campos Adicionais de um Tipo de Controle Litigioso.

| Coluna | Descrição |
|---|---|
| id_md_lit_tp_info_add | Número ID que identifica o Tipo de Informação Adicional. |
| descricao | Descrição textual do registro. |
| id_md_lit_tipo_controle | Número ID que identifica o Tipo de Controle Litigioso ao qual o Tipo de Informação Adicional pertence, faz referência à tabela `md_lit_tipo_controle`. |
| nome | Nome do registro. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
