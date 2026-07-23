# Dicionário de Dados do Módulo Controle de Demandas - v3.0.0

## Índice de Tabelas

- [md_ri_cad_info_add_reg](#md_ri_cad_info_add_reg)
- [md_ri_cad_info_add_val](#md_ri_cad_info_add_val)
- [md_ri_cad_info_add_val_opc](#md_ri_cad_info_add_val_opc)
- [md_ri_cadastro](#md_ri_cadastro)
- [md_ri_classificacao_tema](#md_ri_classificacao_tema)
- [md_ri_crit_cad](#md_ri_crit_cad)
- [md_ri_ctrl_dem_situacao](#md_ri_ctrl_dem_situacao)
- [md_ri_ctrl_demanda](#md_ri_ctrl_demanda)
- [md_ri_gp_param](#md_ri_gp_param)
- [md_ri_gp_param_info_add_campo](#md_ri_gp_param_info_add_campo)
- [md_ri_gp_param_info_add_opcao](#md_ri_gp_param_info_add_opcao)
- [md_ri_gp_param_regra](#md_ri_gp_param_regra)
- [md_ri_gp_param_regra_validacao](#md_ri_gp_param_regra_validacao)
- [md_ri_rel_cad_cidade](#md_ri_rel_cad_cidade)
- [md_ri_rel_cad_classif](#md_ri_rel_cad_classif)
- [md_ri_rel_cad_contato](#md_ri_rel_cad_contato)
- [md_ri_rel_cad_doc](#md_ri_rel_cad_doc)
- [md_ri_rel_cad_local](#md_ri_rel_cad_local)
- [md_ri_rel_cad_localidade](#md_ri_rel_cad_localidade)
- [md_ri_rel_cad_servico](#md_ri_rel_cad_servico)
- [md_ri_rel_cad_tipo_prc](#md_ri_rel_cad_tipo_prc)
- [md_ri_rel_cad_tp_ctrl](#md_ri_rel_cad_tp_ctrl)
- [md_ri_rel_cad_uf](#md_ri_rel_cad_uf)
- [md_ri_rel_cad_unidade](#md_ri_rel_cad_unidade)
- [md_ri_rel_class_tema_subtema](#md_ri_rel_class_tema_subtema)
- [md_ri_rel_crit_cad_cont](#md_ri_rel_crit_cad_cont)
- [md_ri_rel_crit_cad_proc](#md_ri_rel_crit_cad_proc)
- [md_ri_rel_crit_cad_serie](#md_ri_rel_crit_cad_serie)
- [md_ri_rel_crit_cad_unid](#md_ri_rel_crit_cad_unid)
- [md_ri_rel_ctrl_dem_unid](#md_ri_rel_ctrl_dem_unid)
- [md_ri_rel_gp_param_iac_serie](#md_ri_rel_gp_param_iac_serie)
- [md_ri_rel_gp_param_proc](#md_ri_rel_gp_param_proc)
- [md_ri_rel_gp_param_tema](#md_ri_rel_gp_param_tema)
- [md_ri_rel_gp_regra_servico](#md_ri_rel_gp_regra_servico)
- [md_ri_rel_gp_regra_tp_cont](#md_ri_rel_gp_regra_tp_cont)
- [md_ri_rel_gp_regra_tp_proc](#md_ri_rel_gp_regra_tp_proc)
- [md_ri_rel_reit_doc](#md_ri_rel_reit_doc)
- [md_ri_rel_reit_unid](#md_ri_rel_reit_unid)
- [md_ri_rel_tp_ctrl_dmd_cont](#md_ri_rel_tp_ctrl_dmd_cont)
- [md_ri_rel_tp_ctrl_dmd_gestor](#md_ri_rel_tp_ctrl_dmd_gestor)
- [md_ri_rel_tp_ctrl_dmd_proc](#md_ri_rel_tp_ctrl_dmd_proc)
- [md_ri_rel_tp_ctrl_dmd_serie](#md_ri_rel_tp_ctrl_dmd_serie)
- [md_ri_rel_tp_ctrl_dmd_unid](#md_ri_rel_tp_ctrl_dmd_unid)
- [md_ri_resposta](#md_ri_resposta)
- [md_ri_resposta_reiteracao](#md_ri_resposta_reiteracao)
- [md_ri_servico](#md_ri_servico)
- [md_ri_subtema](#md_ri_subtema)
- [md_ri_tipo_controle](#md_ri_tipo_controle)
- [md_ri_tipo_demanda](#md_ri_tipo_demanda)
- [md_ri_tipo_processo](#md_ri_tipo_processo)
- [md_ri_tipo_reiteracao](#md_ri_tipo_reiteracao)
- [md_ri_tipo_resposta](#md_ri_tipo_resposta)
- [md_ri_tp_ctrl_demanda](#md_ri_tp_ctrl_demanda)

## md_ri_cad_info_add_reg

Registra ocorrências das seções de informações adicionais preenchidas em um cadastro.

| Coluna | Descrição |
|---|---|
| id_md_ri_cad_info_add_reg | Número ID que identifica o registro de informações adicionais. |
| chave_registro | Chave lógica que distingue ocorrências da mesma seção no cadastro. |
| dta_operacao | Data/hora da operação que gravou o registro. |
| fieldset | Identificador da seção funcional à qual o registro pertence. |
| id_contato | Número ID que identifica o contato associado à ocorrência, quando aplicável. |
| id_md_ri_cadastro | Número ID que identifica o cadastro de Controle de Demandas. |
| id_md_ri_gp_param | Número ID que identifica o grupo de parametrizações usado pelo registro. |
| id_usuario | Número ID que identifica o usuário responsável pela operação. |

## md_ri_cad_info_add_val

Armazena valores escalares ou de seleção única dos campos de informações adicionais.

| Coluna | Descrição |
|---|---|
| id_md_ri_cad_info_add_val | Número ID que identifica o valor de informação adicional. |
| dta_operacao | Data/hora da operação que gravou o valor. |
| id_md_ri_cad_info_add_reg | Número ID que identifica a ocorrência de informações adicionais. |
| id_md_ri_gp_param_iac | Número ID que identifica o campo configurado no grupo de parametrizações. |
| id_md_ri_gp_param_iao | Número ID que identifica a opção selecionada, quando aplicável. |
| id_usuario | Número ID que identifica o usuário responsável pela operação. |
| valor_texto | Valor textual preenchido no campo. |

## md_ri_cad_info_add_val_opc

Associa uma ocorrência de informações adicionais às múltiplas opções selecionadas em um campo.

| Coluna | Descrição |
|---|---|
| dta_operacao | Data/hora da operação que selecionou a opção. |
| id_md_ri_cad_info_add_reg | Número ID que identifica a ocorrência de informações adicionais. |
| id_md_ri_gp_param_iac | Número ID que identifica o campo configurado. |
| id_md_ri_gp_param_iao | Número ID que identifica a opção selecionada. |
| id_usuario | Número ID que identifica o usuário responsável pela operação. |

## md_ri_cadastro

Armazena o cadastro principal de Controle de Demandas vinculado a um processo SEI.

| Coluna | Descrição |
|---|---|
| id_md_ri_cadastro | Número ID que identifica o cadastro de Controle de Demandas. |
| dta_criacao | Data/hora de criação do cadastro. |
| dta_prazo | Data final legada para resposta da demanda. |
| id_documento | Número ID que identifica o documento principal legado do cadastro. |
| id_md_ri_gp_param | Número ID que identifica o grupo de parametrizações aplicado. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| id_procedimento | Número ID que identifica o processo SEI do cadastro. |
| id_unidade | Número ID que identifica a unidade associada à criação do cadastro. |
| id_usuario | Número ID que identifica o usuário responsável pela criação do cadastro. |
| informacoes_complementares | Informações complementares sobre a demanda. |

## md_ri_classificacao_tema

Administração dos temas usados para classificar demandas.

| Coluna | Descrição |
|---|---|
| id_md_ri_classificacao_tema | Número ID que identifica o tema de classificação. |
| classificacao_tema | Nome do tema de classificação. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda ao qual o tema pertence. |

## md_ri_crit_cad

Armazena o critério legado global para habilitação de cadastros.

| Coluna | Descrição |
|---|---|
| id_md_ri_crit_cad | Número ID que identifica o critério legado de cadastro. |
| data_corte | Data/hora de corte usada para determinar os processos alcançados pelo critério. |

## md_ri_ctrl_dem_situacao

Administração das situações possíveis para controles sobre demandas.

| Coluna | Descrição |
|---|---|
| id_md_ri_ctrl_dem_situacao | Número ID que identifica a situação do controle sobre a demanda. |
| descricao | Descrição da situação. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| nome | Nome da situação. |
| ordem | Número que define a ordem de apresentação da situação. |
| sin_ativo | Variável categórica que indica se a situação está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_conclui_fluxo | Variável categórica que indica se a situação conclui o fluxo da demanda:<br><br><ul><li>S = Conclui o fluxo da demanda</li><li>N = Não conclui o fluxo da demanda</li></ul> |

## md_ri_ctrl_demanda

Armazena cada controle materializado sobre uma demanda cadastrada.

| Coluna | Descrição |
|---|---|
| id_md_ri_ctrl_demanda | Número ID que identifica o controle sobre a demanda. |
| detalhamento | Detalhamento do controle sobre a demanda. |
| dta_final_resposta | Data final prevista para resposta da demanda. |
| dth_atualizacao | Data/hora da última atualização do controle. |
| dth_cadastro | Data/hora de criação do controle. |
| dth_conclusao | Data/hora em que o controle foi concluído. |
| id_documento | Número ID que identifica o documento associado ao controle. |
| id_md_ri_cadastro | Número ID que identifica o cadastro principal. |
| id_md_ri_ctrl_dem_situacao | Número ID que identifica a situação atual. |
| id_md_ri_tipo_demanda | Número ID que identifica o tipo da demanda. |
| id_unid_coord_resposta | Número ID que identifica a unidade coordenadora da resposta. |
| identificacao | Identificação textual da demanda controlada. |
| resumo | Resumo da demanda. |
| sin_ativo | Variável categórica que indica se o controle está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_concluido | Variável categórica que indica se o controle foi concluído:<br><br><ul><li>S = Concluído</li><li>N = Não concluído</li></ul> |

## md_ri_gp_param

Administração dos grupos de parametrizações de um Tipo de Controle de Demanda.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param | Número ID que identifica o grupo de parametrizações. |
| dth_atualizacao | Data/hora da última atualização do grupo. |
| dth_criacao | Data/hora de criação do grupo. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| nome_grupo | Nome do grupo de parametrizações. |
| sin_ativo | Variável categórica que indica se o grupo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_padrao | Variável categórica que indica se o grupo é o grupo padrão:<br><br><ul><li>S = O grupo padrão</li><li>N = Não o grupo padrão</li></ul> |

## md_ri_gp_param_info_add_campo

Administração dos campos de informações adicionais de um grupo de parametrizações.

| Coluna | Descrição |
|---|---|
| ajuda | Texto de ajuda apresentado ao usuário. |
| decimais | Quantidade de casas decimais permitida no campo. |
| fieldset | Identificador da seção funcional em que o campo é exibido:<br><br><ul><li>`INFO_ADICIONAL_CONTROLE_SOBRE_DEMANDA`</li><li>`INFO_ADICIONAL_DEMANDA`</li><li>`INFO_ADICIONAL_DEMANDANTE`</li><li>`INFO_ADICIONAL_DETALHES_GERAIS_DEMANDA`</li><li>`INFO_ADICIONAL_REITERACAO_DEMANDA`</li><li>`INFO_ADICIONAL_RESPOSTA_DEMANDA`</li></ul> |
| id_md_ri_gp_param | Número ID que identifica o grupo de parametrizações. |
| id_md_ri_gp_param_iac | Número ID que identifica o campo de informação adicional. |
| id_md_ri_gp_param_iac_dep | Número ID que identifica outro campo do qual este campo depende. |
| linhas | Quantidade de linhas usada na apresentação de campos de texto grande. |
| mascara | Máscara de entrada configurada para o campo. |
| nome | Identificador interno do campo. |
| ordem | Número que define a ordem de exibição do campo. |
| rotulo | Texto do campo apresentado aos usuários. |
| sin_ativo | Variável categórica que indica se o campo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_doc_externo | Variável categórica que indica se um campo `DOCUMENTO_SEI` aceita documento externo ao processo:<br><br><ul><li>S = Aceita documento externo ao processo</li><li>N = Não aceita documento externo ao processo</li></ul> |
| sin_obrigatorio | Variável categórica que indica se o preenchimento do campo é obrigatório:<br><br><ul><li>S = Obrigatório</li><li>N = Não obrigatório</li></ul> |
| sin_valor_padrao | Variável categórica que indica se o valor é o padrão do campo:<br><br><ul><li>S = Valor padrão do campo</li><li>N = Não é valor padrão do campo</li></ul> |
| sta_tipo | Status multi-valorado que identifica o tipo do campo: `DATA`, `DINHEIRO`, `DOCUMENTO_SEI`, `LISTA`, `NUMERO_DECIMAL`, `NUMERO_INTEIRO`, `OPCOES`, `TEXTO_GRANDE` ou `TEXTO_SIMPLES`. |
| tamanho | Tamanho máximo configurado para o valor do campo. |
| valor_maximo | Limite máximo ou marcador máximo de validação do campo. |
| valor_minimo | Limite mínimo ou marcador mínimo de validação do campo. |

## md_ri_gp_param_info_add_opcao

Administração das opções disponíveis para campos dos tipos lista e opções.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param_iac | Número ID que identifica o campo de informação adicional. |
| id_md_ri_gp_param_iao | Número ID que identifica a opção do campo. |
| ordem | Número que define a ordem de apresentação da opção. |
| rotulo_valor | Texto da opção apresentado ao usuário. |
| sin_ativo | Variável categórica que indica se a opção está disponível:<br><br><ul><li>S = Disponível</li><li>N = Não disponível</li></ul> |
| sin_padrao | Variável categórica que indica se esta é a opção padrão:<br><br><ul><li>S = É a opção padrão</li><li>N = Não é a opção padrão</li></ul> |
| valor | Código interno da opção. |

## md_ri_gp_param_regra

Administração das regras de exibição e obrigatoriedade dos campos padrão de um grupo.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param_regra | Número ID que identifica a regra de parametrização. |
| dth_atualizacao | Data/hora da última atualização da regra. |
| dth_criacao | Data/hora de criação da regra. |
| id_md_ri_gp_param | Número ID que identifica o grupo de parametrizações. |
| nome_campo_sei | Identificador do campo padrão controlado pela regra: `cidades`, `entidadesRelacionadas`, `informacoesComplementares`, `localidade`, `numeroOrgaoDemandante`, `servicos`, `tipoContatoDemandante`, `tipoProcessoOrgaoDemandante` ou `uf`. |
| sin_ativo | Variável categórica que indica se a regra está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_exibir | Variável categórica que indica se o campo deve ser exibido:<br><br><ul><li>S = Deve ser exibido</li><li>N = Não deve ser exibido</li></ul> |
| sin_obrigatorio | Variável categórica que indica se o preenchimento do campo é obrigatório:<br><br><ul><li>S = Obrigatório</li><li>N = Não obrigatório</li></ul> |

## md_ri_gp_param_regra_validacao

Associa regras de parametrização às validações adicionais de demandante.

| Coluna | Descrição |
|---|---|
| codigo_validacao | Código da validação: `DEMANDANTE_CARGO`, `DEMANDANTE_ENDERECO_COMPLETO`, `DEMANDANTE_NATUREZA_PESSOA_JURIDICA` ou `DEMANDANTE_PESSOA_JURIDICA_ASSOCIADA`. |
| id_md_ri_gp_param_regra | Número ID que identifica a regra de parametrização. |

## md_ri_rel_cad_cidade

Associativa legada entre cadastros e cidades.

| Coluna | Descrição |
|---|---|
| id_cidade | Número ID que identifica a cidade. |
| id_md_ri_cadastro | Número ID que identifica o cadastro. |

## md_ri_rel_cad_classif

Associa cadastros a temas e, opcionalmente, subtemas de classificação.

| Coluna | Descrição |
|---|---|
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| id_md_ri_classificacao_tema | Número ID que identifica o tema de classificação. |
| id_md_ri_subtema | Número ID que identifica o subtema, quando selecionado. |

## md_ri_rel_cad_contato

Associa um cadastro aos contatos relacionados à demanda.

| Coluna | Descrição |
|---|---|
| id_contato | Número ID que identifica o contato relacionado. |
| id_md_ri_cadastro | Número ID que identifica o cadastro. |

## md_ri_rel_cad_doc

Associativa entre cadastros de demandas e documentos SEI.

| Coluna | Descrição |
|---|---|
| id_documento | Número ID que identifica o documento SEI. |
| id_md_ri_cadastro | Número ID que identifica o cadastro da demanda. |

## md_ri_rel_cad_local

Armazena as combinações atuais de UF, cidade e local associadas a um cadastro.

| Coluna | Descrição |
|---|---|
| id_md_ri_rel_cad_local | Número ID que identifica o local associado ao cadastro. |
| id_cidade | Número ID que identifica a cidade, quando informada. |
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| id_uf | Número ID que identifica a Unidade Federativa. |
| local | Descrição complementar do local. |

## md_ri_rel_cad_localidade

Associativa legada entre cadastro, cidade e descrição de localidade.

| Coluna | Descrição |
|---|---|
| id_cidade | Número ID que identifica a cidade. |
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| localidade | Descrição legada da localidade. |

## md_ri_rel_cad_servico

Associativa entre cadastros e serviços relacionados à demanda.

| Coluna | Descrição |
|---|---|
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| id_md_ri_servico | Número ID que identifica o serviço. |

## md_ri_rel_cad_tipo_prc

Registra números e tipos de processo no órgão demandante associados ao cadastro.

| Coluna | Descrição |
|---|---|
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| id_md_ri_tipo_processo | Número ID que identifica o tipo de processo no órgão demandante. |
| numero | Número da demanda ou do processo no órgão demandante. |

## md_ri_rel_cad_tp_ctrl

Registra as referências vinculadas a um cadastro.

| Coluna | Descrição |
|---|---|
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| id_md_ri_tipo_controle | Número ID que identifica o tipo da referência. |
| numero | Número da referência. |

## md_ri_rel_cad_uf

Associativa legada entre cadastros e Unidades Federativas.

| Coluna | Descrição |
|---|---|
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| id_uf | Número ID que identifica a Unidade Federativa. |

## md_ri_rel_cad_unidade

Associa o cadastro às unidades responsáveis no modelo original.

| Coluna | Descrição |
|---|---|
| id_md_ri_cadastro | Número ID que identifica o cadastro. |
| id_unidade | Número ID que identifica a unidade responsável. |

## md_ri_rel_class_tema_subtema

Associativa entre temas e subtemas de classificação.

| Coluna | Descrição |
|---|---|
| id_md_ri_classificacao_tema | Número ID que identifica o tema de classificação. |
| id_md_ri_subtema | Número ID que identifica o subtema. |
| sin_ativo | Variável categórica que indica se o vínculo entre tema e subtema está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_ri_rel_crit_cad_cont

Associativa legada entre o critério de cadastro e tipos de contato permitidos.

| Coluna | Descrição |
|---|---|
| id_md_ri_crit_cad | Número ID que identifica o critério legado de cadastro. |
| id_tipo_contato | Número ID que identifica o tipo de contato permitido. |

## md_ri_rel_crit_cad_proc

Associativa legada entre o critério de cadastro e tipos de processo SEI.

| Coluna | Descrição |
|---|---|
| id_md_ri_crit_cad | Número ID que identifica o critério legado de cadastro. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo SEI. |

## md_ri_rel_crit_cad_serie

Associativa legada entre o critério de cadastro e tipos de documento SEI.

| Coluna | Descrição |
|---|---|
| id_md_ri_crit_cad | Número ID que identifica o critério legado de cadastro. |
| id_serie | Número ID que identifica o tipo de documento SEI. |

## md_ri_rel_crit_cad_unid

Associativa legada entre o critério de cadastro e unidades habilitadas.

| Coluna | Descrição |
|---|---|
| id_md_ri_crit_cad | Número ID que identifica o critério legado de cadastro. |
| id_unidade | Número ID que identifica a unidade habilitada. |

## md_ri_rel_ctrl_dem_unid

Associativa entre controles sobre demandas e suas unidades responsáveis.

| Coluna | Descrição |
|---|---|
| id_md_ri_ctrl_demanda | Número ID que identifica o controle sobre a demanda. |
| id_unidade | Número ID que identifica a unidade responsável. |

## md_ri_rel_gp_param_iac_serie

Associa um campo `DOCUMENTO_SEI` aos tipos de documento aceitos.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param_iac | Número ID que identifica o campo de informação adicional. |
| id_serie | Número ID que identifica um tipo de documento SEI aceito. |

## md_ri_rel_gp_param_proc

Associa um grupo de parametrizações aos tipos de processo em que ele se aplica.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param | Número ID que identifica o grupo de parametrizações. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo SEI. |

## md_ri_rel_gp_param_tema

Associa um grupo de parametrizações aos temas permitidos.

| Coluna | Descrição |
|---|---|
| id_md_ri_classificacao_tema | Número ID que identifica o tema de classificação. |
| id_md_ri_gp_param | Número ID que identifica o grupo de parametrizações. |

## md_ri_rel_gp_regra_servico

Associa uma regra de parametrização aos serviços permitidos.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param_regra | Número ID que identifica a regra de parametrização. |
| id_md_ri_servico | Número ID que identifica o serviço permitido. |

## md_ri_rel_gp_regra_tp_cont

Associa regras de parametrização aos tipos de contato permitidos para demandantes ou entidades relacionadas.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param_regra | Número ID que identifica a regra de parametrização. |
| id_tipo_contato | Número ID que identifica o tipo de contato permitido. |

## md_ri_rel_gp_regra_tp_proc

Associa uma regra de parametrização aos tipos de processo do órgão demandante permitidos.

| Coluna | Descrição |
|---|---|
| id_md_ri_gp_param_regra | Número ID que identifica a regra de parametrização. |
| id_md_ri_tipo_processo | Número ID que identifica o tipo de processo no órgão demandante. |

## md_ri_rel_reit_doc

Registra solicitações vinculadas a demandas e materializadas por documentos SEI.

| Coluna | Descrição |
|---|---|
| id_md_ri_rel_reit_doc | Número ID que identifica a solicitação. |
| dta_certa | Data final prevista para resposta da solicitação. |
| dta_operacao | Data/hora de registro da solicitação. |
| id_documento | Número ID que identifica o documento SEI da solicitação. |
| id_md_ri_cadastro | Número ID que identifica o cadastro principal. |
| id_md_ri_ctrl_demanda | Número ID que identifica a demanda à qual a solicitação se refere. |
| id_md_ri_tipo_reiteracao | Número ID que identifica o tipo de solicitação. |
| id_unidade | Número ID que identifica a unidade que registrou a solicitação. |
| id_usuario | Número ID que identifica o usuário que registrou a solicitação. |
| sin_respondida | Variável categórica que indica se a solicitação foi respondida:<br><br><ul><li>S = Respondida</li><li>N = Não respondida</li></ul> |

## md_ri_rel_reit_unid

Associa solicitações às unidades responsáveis por seu atendimento.

| Coluna | Descrição |
|---|---|
| id_md_ri_rel_reit_unid | Número ID que identifica o vínculo da solicitação com a unidade. |
| id_md_ri_rel_reit_doc | Número ID que identifica a solicitação. |
| id_unidade | Número ID que identifica a unidade responsável. |

## md_ri_rel_tp_ctrl_dmd_cont

Associa um Tipo de Controle de Demanda aos tipos de contato permitidos para entidades relacionadas.

| Coluna | Descrição |
|---|---|
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| id_tipo_contato | Número ID que identifica o tipo de contato permitido. |

## md_ri_rel_tp_ctrl_dmd_gestor

Associa um Tipo de Controle de Demanda aos usuários gestores.

| Coluna | Descrição |
|---|---|
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| id_usuario | Número ID que identifica o usuário gestor. |

## md_ri_rel_tp_ctrl_dmd_proc

Associa um Tipo de Controle de Demanda aos tipos de processo SEI alcançados.

| Coluna | Descrição |
|---|---|
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| id_tipo_procedimento | Número ID que identifica o tipo de processo SEI. |

## md_ri_rel_tp_ctrl_dmd_serie

Associa um Tipo de Controle de Demanda aos tipos de documento SEI aceitos.

| Coluna | Descrição |
|---|---|
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| id_serie | Número ID que identifica o tipo de documento SEI. |

## md_ri_rel_tp_ctrl_dmd_unid

Associa um Tipo de Controle de Demanda às unidades habilitadas.

| Coluna | Descrição |
|---|---|
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| id_unidade | Número ID que identifica a unidade habilitada. |

## md_ri_resposta

Registra respostas apresentadas diretamente a demandas.

| Coluna | Descrição |
|---|---|
| id_md_ri_resposta | Número ID que identifica a resposta. |
| dta_insercao | Data/hora de inserção da resposta. |
| id_documento | Número ID que identifica o documento SEI da resposta. |
| id_md_ri_cadastro | Número ID que identifica o cadastro principal. |
| id_md_ri_ctrl_demanda | Número ID que identifica a demanda respondida. |
| id_md_ri_tipo_resposta | Número ID que identifica o tipo de resposta. |
| id_unidade | Número ID que identifica a unidade que registrou a resposta. |
| id_usuario | Número ID que identifica o usuário que registrou a resposta. |

## md_ri_resposta_reiteracao

Registra respostas apresentadas a solicitações de uma demanda.

| Coluna | Descrição |
|---|---|
| id_md_ri_resposta_reiteracao | Número ID que identifica a resposta da solicitação. |
| dta_insercao | Data/hora de inserção da resposta. |
| id_documento | Número ID que identifica o documento SEI da resposta. |
| id_md_ri_cadastro | Número ID que identifica o cadastro principal. |
| id_md_ri_ctrl_demanda | Número ID que identifica a demanda relacionada. |
| id_md_ri_rel_reit_doc | Número ID que identifica a solicitação respondida. |
| id_md_ri_tipo_resposta | Número ID que identifica o tipo de resposta. |
| id_unidade | Número ID que identifica a unidade que registrou a resposta. |
| id_usuario | Número ID que identifica o usuário que registrou a resposta. |

## md_ri_servico

Administração dos serviços que podem ser relacionados às demandas.

| Coluna | Descrição |
|---|---|
| id_md_ri_servico | Número ID que identifica o serviço. |
| nome | Nome do serviço. |
| sin_ativo | Variável categórica que indica se o serviço está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_ri_subtema

Administração dos subtemas usados para classificar demandas.

| Coluna | Descrição |
|---|---|
| id_md_ri_subtema | Número ID que identifica o subtema. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| nome | Nome do subtema. |
| sin_ativo | Variável categórica que indica se o subtema está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_ri_tipo_controle

Administração dos tipos de referência disponíveis para os cadastros.

| Coluna | Descrição |
|---|---|
| id_md_ri_tipo_controle | Número ID que identifica o tipo de referência. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| sin_ativo | Variável categórica que indica se o tipo de referência está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo_controle | Nome do tipo de referência. |

## md_ri_tipo_demanda

Administração dos tipos de demanda de um Tipo de Controle de Demanda.

| Coluna | Descrição |
|---|---|
| id_md_ri_tipo_demanda | Número ID que identifica o tipo de demanda. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| sin_ativo | Variável categórica que indica se o tipo de demanda está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo_demanda | Nome do tipo de demanda. |

## md_ri_tipo_processo

Administração dos tipos de processo usados pelo órgão demandante.

| Coluna | Descrição |
|---|---|
| id_md_ri_tipo_processo | Número ID que identifica o tipo de processo no órgão demandante. |
| sin_ativo | Variável categórica que indica se o tipo de processo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo_processo | Nome do tipo de processo no órgão demandante. |

## md_ri_tipo_reiteracao

Administração dos tipos de solicitação de um Tipo de Controle de Demanda.

| Coluna | Descrição |
|---|---|
| id_md_ri_tipo_reiteracao | Número ID que identifica o tipo de solicitação. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| sin_ativo | Variável categórica que indica se o tipo de solicitação está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo_reiteracao | Nome do tipo de solicitação. |

## md_ri_tipo_resposta

Administração dos tipos de resposta de um Tipo de Controle de Demanda.

| Coluna | Descrição |
|---|---|
| id_md_ri_tipo_resposta | Número ID que identifica o tipo de resposta. |
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| sin_ativo | Variável categórica que indica se o tipo de resposta está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_merito | Variável categórica que indica se o tipo de resposta responde ao mérito:<br><br><ul><li>S = Responde ao mérito</li><li>N = Não responde ao mérito</li></ul> |
| tipo_resposta | Nome do tipo de resposta. |

## md_ri_tp_ctrl_demanda

Armazena a configuração principal de cada Tipo de Controle de Demanda.

| Coluna | Descrição |
|---|---|
| id_md_ri_tp_ctrl_demanda | Número ID que identifica o Tipo de Controle de Demanda. |
| descricao | Descrição do Tipo de Controle de Demanda. |
| dth_atualizacao | Data/hora da última atualização. |
| dth_corte | Data/hora de corte usada para determinar os processos alcançados. |
| dth_criacao | Data/hora de criação. |
| nome | Nome do Tipo de Controle de Demanda. |
| sin_ativo | Variável categórica que indica se o Tipo de Controle de Demanda está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_exibir_pendencia | Variável categórica que indica se o ícone de cadastro pendente deve ser exibido nos processos:<br><br><ul><li>S = Deve ser exibido nos processos</li><li>N = Não deve ser exibido nos processos</li></ul> |
