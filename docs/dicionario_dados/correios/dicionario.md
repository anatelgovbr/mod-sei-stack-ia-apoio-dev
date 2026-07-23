# Dicionário de Dados do Módulo SEI Correios - v2.7.2

## Índice de Tabelas

- [md_cor_adm_integr_tokens](#md_cor_adm_integr_tokens)
- [md_cor_adm_integracao](#md_cor_adm_integracao)
- [md_cor_adm_par_ar_infrigen](#md_cor_adm_par_ar_infrigen)
- [md_cor_adm_parametro_ar](#md_cor_adm_parametro_ar)
- [md_cor_ar_cobranca](#md_cor_ar_cobranca)
- [md_cor_contato](#md_cor_contato)
- [md_cor_contrato](#md_cor_contrato)
- [md_cor_diretoria](#md_cor_diretoria)
- [md_cor_expedicao_andamento](#md_cor_expedicao_andamento)
- [md_cor_expedicao_formato](#md_cor_expedicao_formato)
- [md_cor_expedicao_solicitad](#md_cor_expedicao_solicitad)
- [md_cor_extensao_midia](#md_cor_extensao_midia)
- [md_cor_justificativa](#md_cor_justificativa)
- [md_cor_lista_status](#md_cor_lista_status)
- [md_cor_map_unid_servico](#md_cor_map_unid_servico)
- [md_cor_map_unidade_exp](#md_cor_map_unidade_exp)
- [md_cor_objeto](#md_cor_objeto)
- [md_cor_plp](#md_cor_plp)
- [md_cor_retorno_ar](#md_cor_retorno_ar)
- [md_cor_retorno_ar_doc](#md_cor_retorno_ar_doc)
- [md_cor_serie_exp](#md_cor_serie_exp)
- [md_cor_servico_postal](#md_cor_servico_postal)
- [md_cor_status_process](#md_cor_status_process)
- [md_cor_substatus_process](#md_cor_substatus_process)
- [md_cor_tipo_correspondenc](#md_cor_tipo_correspondenc)
- [md_cor_tipo_objeto](#md_cor_tipo_objeto)
- [md_cor_unidade_exp](#md_cor_unidade_exp)
- [rel_contato_justificativa](#rel_contato_justificativa)

## md_cor_adm_integr_tokens

Armazena credenciais e tokens das integrações dos Correios por contrato.

| Coluna | Descrição |
|---|---|
| id_md_cor_adm_integr_tokens | Número ID que identifica o registro de credenciais e token. |
| data_exp_token | Data/hora de expiração do token. |
| id_md_cor_adm_integracao | Número ID da integração à qual as credenciais pertencem. |
| id_md_cor_contrato | Número ID do contrato ao qual as credenciais pertencem. |
| senha | Armazena a senha do usuário do órgão nos Correios. |
| sin_ativo | Variável categórica que indica se o registro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| token | Armazena o token de autenticação da integração. |
| usuario | Armazena o usuário do órgão nos Correios. |

## md_cor_adm_integracao

Armazena as funcionalidades e os endpoints das APIs dos Correios.

| Coluna | Descrição |
|---|---|
| id_md_cor_adm_integracao | Número ID que identifica a configuração de integração. |
| data_exp_token | Data/hora de expiração do token armazenado na integração. |
| funcionalidade | Código da funcionalidade: 1 gerar token; 2 rastrear objeto; 3 consultar CEP; 4 serviços postais; 5 solicitar etiquetas; 6 pré-postagem nacional; 7 emitir rótulo; 8 baixar rótulo; 9 aviso de recebimento; 10 cancelar pré-postagem. |
| nome | Armazena o nome da funcionalidade integrada. |
| senha | Armazena a senha associada à configuração da integração. |
| sin_ativo | Variável categórica que indica se a integração está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| token | Armazena o token associado à configuração da integração. |
| url_operacao | Armazena o endpoint da operação disponibilizada pelos Correios. |
| usuario | Armazena o usuário associado à configuração da integração. |

## md_cor_adm_par_ar_infrigen

Armazena motivos de devolução de objetos e sua classificação como infringência contratual.

| Coluna | Descrição |
|---|---|
| id_md_cor_param_ar_infrigencia | Número ID que identifica o motivo de devolução. |
| id_md_cor_parametro_ar | Número ID da parametrização de AR à qual o motivo pertence. |
| motivo_infrigencia | Armazena a descrição do motivo de devolução do objeto. |
| sin_ativo | Variável categórica que indica se o motivo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_infrigencia | Variável categórica que indica se o motivo configura infringência contratual:<br><br><ul><li>S = Configura infringência contratual</li><li>N = Não configura infringência contratual</li></ul> |

## md_cor_adm_parametro_ar

Armazena parâmetros para retorno de AR, objetos devolvidos e geração de documentos de cobrança.

| Coluna | Descrição |
|---|---|
| dias_exp_ret_ar | Quantidade máxima de dias para finalizar o fluxo de AR não retornado. |
| id_contato | Número ID do destinatário padrão dos documentos de cobrança. |
| id_hipotese_legal_ar | Número ID da hipótese legal aplicada ao documento AR quando o nível de acesso é predefinido. |
| id_md_cor_parametro_ar | Número ID que identifica a parametrização de AR. |
| id_procedimento_cobranca | Número ID do processo no qual os documentos de cobrança serão gerados. |
| id_serie | Número ID do tipo de documento usado para registrar o retorno do AR. |
| id_serie_cobranca | Número ID do tipo de documento usado nas cobranças de AR pendente. |
| id_serie_devolvido | Número ID do tipo de documento usado quando o objeto é devolvido. |
| id_tipo_conferencia | Número ID do tipo de conferência aplicado ao documento de retorno do AR. |
| id_tipo_conferencia_devolvido | Número ID do tipo de conferência aplicado ao documento de objeto devolvido. |
| id_unidade_cobranca | Número ID da unidade geradora dos documentos de cobrança. |
| modelo_cobranca | Armazena o conteúdo-modelo usado para gerar documentos de cobrança. |
| nivel_acesso_ar | Status multi-valorado que identifica o nível de acesso predefinido para o documento AR:<br><br><ul><li>0 = Público</li><li>1 = Restrito</li><li>2 = Sigiloso</li></ul> |
| nome_arvore | Armazena o número ou complemento exibido na árvore para o documento de retorno do AR. |
| nome_arvore_devolvido | Armazena o número ou complemento exibido na árvore para o documento de objeto devolvido. |
| nu_dias_cobranca_ar | Quantidade de dias durante a qual ainda é possível cobrar um AR não retornado. |
| nu_dias_retorno_ar | Prazo contratual, em dias, para considerar atrasado o retorno do AR. |
| sin_niv_ace_doc_princ_ar | Variável categórica que indica a regra de acesso do AR:<br><br><ul><li>S = Usa o nível do documento principal</li><li>N = Usa o nível predefinido na parametrização</li></ul> |

## md_cor_ar_cobranca

Registra documentos gerados para cobrar pendências de retorno de AR.

| Coluna | Descrição |
|---|---|
| id_md_cor_ar_cobranca | Número ID que identifica o registro de cobrança. |
| dt_md_cor_ar_cobranca | Data/hora de geração ou registro da cobrança. |
| id_documento_cobranca | Número ID do documento de cobrança gerado no SEI. |
| id_md_cor_expedicao_solicitada | Número ID da solicitação de expedição cobrada. |

## md_cor_contato

Registra os dados do destinatário usados em cada solicitação de expedição.

| Coluna | Descrição |
|---|---|
| id_md_cor_contato | Número ID que identifica o registro do destinatário. |
| bairro | Armazena o bairro do endereço utilizado na expedição. |
| cargo_expressao | Armazena a expressão de cargo do destinatário. |
| cep | Armazena o CEP do endereço utilizado na expedição. |
| complemento | Armazena o complemento do endereço utilizado na expedição. |
| endereco | Armazena o endereço utilizado na expedição. |
| id_contato | Número ID do contato original no SEI. |
| id_contato_associado | Número ID do contato associado cujo endereço pode ser utilizado. |
| id_md_cor_expedicao_solicitada | Número ID da solicitação de expedição à qual o destinatário pertence. |
| id_tipo_contato | Número ID do tipo do contato destinatário. |
| id_tipo_contato_associado | Número ID do tipo do contato associado. |
| nome | Armazena o nome do destinatário. |
| nome_cidade | Armazena a cidade do endereço utilizado na expedição. |
| nome_contato_associado | Armazena o nome do contato associado. |
| sigla_uf | Armazena a sigla da UF do endereço utilizado na expedição. |
| sin_ativo | Variável categórica que indica se o registro do destinatário está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_endereco_associado | Variável categórica que indica qual endereço deve ser usado:<br><br><ul><li>S = Endereço do contato associado</li><li>N = Endereço próprio do contato</li></ul> |
| sta_genero | Status multi-valorado que identifica o gênero do contato:<br><br><ul><li>M = Masculino</li><li>F = Feminino</li></ul> |
| sta_natureza | Status multi-valorado que identifica a natureza do contato:<br><br><ul><li>F = Pessoa física</li><li>J = Pessoa jurídica</li></ul> |
| sta_natureza_contato_associado | Status multi-valorado que identifica a natureza do contato associado:<br><br><ul><li>F = Pessoa física</li><li>J = Pessoa jurídica</li></ul> |
| tratamento_expressao | Armazena a expressão de tratamento do destinatário. |

## md_cor_contrato

Armazena contratos do órgão com os Correios.

| Coluna | Descrição |
|---|---|
| id_md_cor_contrato | Número ID que identifica o contrato. |
| id_md_cor_diretoria | Número ID da diretoria regional dos Correios vinculada ao contrato. |
| id_procedimento | Número ID do processo SEI de contratação dos Correios. |
| numero_cartao_postagem | Armazena o número do cartão de postagem do contrato. |
| numero_cnpj | Armazena o CNPJ do órgão correspondente ao contrato. |
| numero_contrato | Armazena o número de identificação do contrato no órgão. |
| numero_contrato_correio | Armazena o código interno dos Correios que identifica o contrato. |
| sin_ativo | Variável categórica que indica se o contrato está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_cor_diretoria

Armazena códigos, descrições e siglas das diretorias regionais dos Correios usadas pelos contratos.

| Coluna | Descrição |
|---|---|
| id_md_cor_diretoria | Número ID que identifica a diretoria. |
| codigo_diretoria | Armazena o código da diretoria nos Correios. |
| descricao_diretoria | Armazena a descrição da diretoria. |
| sigla_diretoria | Armazena a sigla da diretoria. |

## md_cor_expedicao_andamento

Registra eventos de rastreamento de uma solicitação de expedição.

| Coluna | Descrição |
|---|---|
| id_md_cor_expedicao_andamento | Número ID que identifica o evento de rastreamento. |
| categoria_objeto | Armazena a categoria postal do objeto retornada pela API de rastreamento. |
| cidade | Armazena a cidade da unidade do evento de rastreamento. |
| codigo_cep | Armazena o CEP da unidade do evento de rastreamento. |
| data_hora | Data/hora de criação do evento nos Correios. |
| data_ultima_atualizacao | Data/hora em que o módulo consultou e registrou a atualização. |
| descricao | Armazena a descrição do evento de rastreamento. |
| detalhe | Armazena o detalhe complementar do evento. |
| id_md_cor_expedicao_solicitada | Número ID da solicitação de expedição rastreada. |
| local | Armazena o tipo da unidade dos Correios onde ocorreu o evento. |
| nome_objeto | Armazena a descrição do tipo postal do objeto. |
| sigla_objeto | Armazena a sigla do tipo postal do objeto. |
| status | Armazena o tipo do evento retornado pela API dos Correios. |
| tipo | Armazena o código do evento retornado pela API dos Correios. |
| uf | Armazena a UF da unidade do evento de rastreamento. |
| versao_sro_xml | Armazena a versão da resposta do serviço de rastreamento. |

## md_cor_expedicao_formato

Registra o formato de expedição escolhido para cada documento principal ou anexo.

| Coluna | Descrição |
|---|---|
| id_md_cor_expedicao_formato | Número ID que identifica o formato do documento expedido. |
| id_md_cor_expedicao_solicitada | Número ID da solicitação à qual o documento pertence. |
| id_protocolo | Número ID do protocolo ou documento formatado para expedição. |
| justificativa | Armazena a justificativa exigida para impressão colorida. |
| sin_forma_expedicao | Variável categórica que indica o formato de expedição:<br><br><ul><li>I = Impresso</li><li>M = Gravação em mídia</li></ul> |
| sin_impressao | Variável categórica que indica o tipo de impressão:<br><br><ul><li>P = Preto e branco</li><li>C = Colorido</li><li>N = Nenhuma, quando gravado em mídia</li></ul> |

## md_cor_expedicao_solicitad

Registra solicitações de expedição de documentos pelos Correios.

| Coluna | Descrição |
|---|---|
| codigo_rastreamento | Armazena o código de rastreamento atribuído ao objeto. |
| data_expedicao | Data/hora em que a solicitação foi efetivamente expedida. |
| data_solicitacao | Data/hora de criação da solicitação de expedição. |
| id_contato_destinatario | Número ID do contato destinatário da expedição. |
| id_documento_principal | Número ID do documento principal expedido. |
| id_md_cor_expedicao_solicitada | Número ID que identifica a solicitação de expedição. |
| id_md_cor_objeto | Número ID da configuração de embalagem e rótulo usada na expedição. |
| id_md_cor_plp | Número ID da PLP à qual a solicitação foi vinculada. |
| id_md_cor_servico_postal | Número ID do serviço postal selecionado. |
| id_pre_postagem | Armazena o identificador da pré-postagem retornado pela API dos Correios. |
| id_unidade | Número ID da unidade solicitante da expedição. |
| id_usuario_exp_autorizador | Número ID do usuário da unidade expedidora que autorizou a expedição. |
| id_usuario_solicitante | Número ID do usuário que criou a solicitação. |
| justificativa_devolucao | Armazena a justificativa da devolução da solicitação pela unidade expedidora. |
| sin_devolvido | Variável categórica que indica se a solicitação foi devolvida pela unidade expedidora:<br><br><ul><li>S = Devolvida pela unidade expedidora</li><li>N = Não devolvida pela unidade expedidora</li></ul> |
| sin_necessita_ar | Variável categórica que indica se a expedição exige aviso de recebimento:<br><br><ul><li>S = Exige aviso de recebimento</li><li>N = Não exige aviso de recebimento</li></ul> |
| sin_objeto_acessado | Variável categórica que indica se os documentos ou rótulos do objeto já foram acessados para preparação da expedição:<br><br><ul><li>S = Já acessados para preparação da expedição</li><li>N = Não acessados para preparação da expedição</li></ul> |
| sin_recebido | Variável categórica que indica se o AR ou objeto foi recebido:<br><br><ul><li>S = Recebido</li><li>N = Não recebido</li></ul> |
| status_cobranca | Status multi-valorado que identifica a situação da cobrança do AR:<br><br><ul><li>C = Pendente com cobrança</li><li>S = Pendente sem cobrança</li><li>F = Fora do prazo</li><li>P = Cobrado fora do prazo</li><li>E = Extraviado sem cobrança</li><li>O = Extraviado com cobrança</li><li>N = Situação inicial da solicitação, antes de qualquer cobrança ser registrada</li></ul> |

## md_cor_extensao_midia

Associa extensões de arquivo do SEI às extensões permitidas para gravação em mídia.

| Coluna | Descrição |
|---|---|
| id_md_cor_extensao_midia | Número ID que identifica a extensão habilitada pelo módulo. |
| id_arquivo_extensao | Número ID da extensão de arquivo cadastrada no SEI. |
| sin_ativo | Variável categórica que indica se a extensão está habilitada:<br><br><ul><li>S = Habilitada</li><li>N = Não habilitada</li></ul> |

## md_cor_justificativa

Armazena justificativas usadas para marcar destinatários não habilitados para expedição.

| Coluna | Descrição |
|---|---|
| id_md_cor_justificativa | Número ID que identifica a justificativa. |
| nome | Armazena o texto da justificativa. |
| sin_ativo | Variável categórica que indica se a justificativa está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## md_cor_lista_status

Armazena tipos de situações SRO e sua classificação de rastreamento no módulo.

| Coluna | Descrição |
|---|---|
| id_md_cor_lista_status | Número ID que identifica o mapeamento de situação SRO. |
| descricao | Armazena a descrição do evento SRO. |
| sin_ativo | Variável categórica que indica se o status é exibido e utilizado no rastreamento:<br><br><ul><li>S = Exibido e utilizado no rastreamento</li><li>N = Não exibido e utilizado no rastreamento</li></ul> |
| sta_rastreio_modulo | Status multi-valorado que identifica a classificação do evento no módulo:<br><br><ul><li>P = Postado</li><li>T = Em trânsito</li><li>S = Sucesso na entrega</li><li>I = Insucesso na entrega</li><li>W = Evento SRO novo ainda não classificado</li></ul> |
| status | Código numérico do tipo do evento retornado pelo SRO. |
| tipo | Código textual do evento retornado pelo SRO. |

## md_cor_map_unid_servico

Associa unidades solicitantes aos serviços postais que podem utilizar.

| Coluna | Descrição |
|---|---|
| id_md_cor_map_unid_servico | Número ID que identifica o mapeamento. |
| id_md_cor_servico_postal | Número ID do serviço postal disponibilizado à unidade. |
| id_unidade_solicitante | Número ID da unidade solicitante. |
| sin_ativo | Variável categórica que indica se o mapeamento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_cor_map_unidade_exp

Associa unidades expedidoras às unidades autorizadas a solicitar expedições.

| Coluna | Descrição |
|---|---|
| id_unidade_exp | Número ID da unidade expedidora. |
| id_unidade_solicitante | Número ID da unidade solicitante vinculada. |
| sin_ativo | Variável categórica que indica se o vínculo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_cor_objeto

Armazena configurações de embalagem, rótulo e margens de impressão por contrato.

| Coluna | Descrição |
|---|---|
| id_md_cor_objeto | Número ID que identifica a configuração do objeto postal. |
| id_md_cor_contrato | Número ID do contrato ao qual a configuração pertence. |
| id_md_cor_tipo_objeto | Número ID do tipo de embalagem. |
| margem_esquerda_impressao | Margem esquerda do rótulo, em centímetros. |
| margem_superior_impressao | Margem superior do rótulo, em centímetros. |
| sin_ativo | Variável categórica que indica se a configuração está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_objeto_padrao | Variável categórica que indica se esta é a configuração padrão de expedição do contrato:<br><br><ul><li>S = Configuração padrão de expedição do contrato</li><li>N = Não é a configuração padrão de expedição do contrato</li></ul> |
| tipo_rotulo_impressao | Status multi-valorado que identifica o tipo do rótulo:<br><br><ul><li>C = Completo</li><li>R = Resumido</li></ul> |

## md_cor_plp

Registra PLPs, identificadores de pré-listas de pré-postagens geradas pelo módulo.

| Coluna | Descrição |
|---|---|
| id_md_cor_plp | Número ID que identifica a PLP. |
| codigo_plp | Armazena o identificador da PLP ou pré-postagem. |
| data_cadastro | Data/hora de cadastro da PLP. |
| id_unidade_geradora | Número ID da unidade que gerou a PLP. |
| sta_plp | Status multi-valorado que identifica a situação da PLP:<br><br><ul><li>G = Gerada</li><li>P = Possui objeto pendente de entrega</li><li>E = Todos os objetos entregues</li><li>C = Cancelada</li><li>R = Possui retorno de AR pendente</li><li>F = Finalizada</li></ul> |

## md_cor_retorno_ar

Registra lotes ZIP de documentos de retorno de AR processados por usuário e unidade.

| Coluna | Descrição |
|---|---|
| id_md_cor_retorno_ar | Número ID que identifica o lote de retorno de AR. |
| data_cadastro | Data/hora de cadastro do lote. |
| id_unidade | Número ID da unidade que processou o lote. |
| id_usuario | Número ID do usuário que processou o lote. |
| nome_arquivo_zip | Armazena o nome do arquivo ZIP submetido ao processamento. |
| sin_autenticado | Variável categórica que indica se os documentos do lote foram autenticados:<br><br><ul><li>S = Autenticados</li><li>N = Não autenticados</li></ul> |

## md_cor_retorno_ar_doc

Registra cada arquivo PDF de retorno de AR e o resultado de seu processamento.

| Coluna | Descrição |
|---|---|
| id_md_cor_retorno_ar_doc | Número ID que identifica o documento processado no lote. |
| codigo_rastreamento | Armazena o código de rastreamento identificado no AR. |
| data_ar | Data de recebimento efetivo pelo destinatário ou da última tentativa de entrega. |
| data_retorno | Data de entrega efetiva do AR pelos Correios ao órgão. |
| id_documento_ar | Número ID do documento externo de AR gerado no SEI. |
| id_documento_principal | Número ID do documento principal referente à expedição identificada. |
| id_md_cor_param_ar_infrigencia | Número ID do motivo de devolução do objeto, quando aplicável. |
| id_md_cor_retorno_ar | Número ID do lote ao qual o arquivo pertence. |
| id_status_process | Código do resultado de processamento: 1 identificado automaticamente; 2 identificado manualmente; 3 retorno já processado; 4 não processado. |
| id_substatus_process | Código do motivo complementar quando não processado: 1 não identificado; 2 processado anteriormente; 3 processo sobrestado; 4 processo anexado; 5 processo bloqueado; 6 unidade desativada. |
| nome_arquivo_pdf | Armazena o nome do arquivo PDF processado. |
| sin_status | Variável categórica que indica se o registro do arquivo foi salvo:<br><br><ul><li>S = Registro do arquivo salvo</li><li>N = Registro do arquivo não salvo</li></ul> |

## md_cor_serie_exp

Associa tipos de documentos do SEI habilitados para solicitação de expedição.

| Coluna | Descrição |
|---|---|
| id_serie | Número ID do tipo de documento habilitado para expedição. |
| sin_ativo | Variável categórica que indica se o tipo de documento está habilitado:<br><br><ul><li>S = Habilitado</li><li>N = Não habilitado</li></ul> |

## md_cor_servico_postal

Armazena serviços postais disponíveis em cada contrato.

| Coluna | Descrição |
|---|---|
| id_md_cor_servico_postal | Número ID que identifica o serviço postal. |
| codigo_ws_correios | Armazena o código externo do serviço postal usado nas integrações. |
| descricao | Armazena a descrição amigável configurada para o serviço. |
| expedicao_aviso_recebimento | Indica se o serviço será expedido com AR (S) ou sem AR (N). |
| id_md_cor_contrato | Número ID do contrato ao qual o serviço pertence. |
| id_md_cor_tipo_correspondenc | Número ID do tipo de correspondência associado ao serviço. |
| id_ws_correios | Armazena o identificador do serviço no web service dos Correios. |
| nome | Armazena o nome original do serviço postal. |
| sin_anexar_midia | Variável categórica que indica se o serviço permite anexar mídia:<br><br><ul><li>S = Permite anexar mídia</li><li>N = Não permite anexar mídia</li></ul> |
| sin_ativo | Variável categórica que indica se o serviço postal está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_servico_cobrar | Variável categórica que indica se o serviço é à cobrar:<br><br><ul><li>S = À cobrar</li><li>N = Não à cobrar</li></ul> |

## md_cor_status_process

Armazena o domínio principal de resultados do processamento de retorno de AR.

| Coluna | Descrição |
|---|---|
| id_md_cor_status_process | Código que identifica o resultado: 1 identificado automaticamente; 2 identificado manualmente; 3 retorno já processado; 4 não processado. |
| descricao | Armazena a descrição do resultado de processamento. |

## md_cor_substatus_process

Armazena motivos complementares associados aos resultados de processamento de retorno de AR.

| Coluna | Descrição |
|---|---|
| id_md_cor_substatus_process | Código do motivo complementar: 1 não identificado; 2 processado anteriormente; 3 processo sobrestado; 4 processo anexado; 5 processo bloqueado; 6 unidade desativada. |
| descricao | Armazena a descrição do motivo complementar. |
| id_md_cor_status_process | Número ID do resultado principal ao qual o motivo pertence. |

## md_cor_tipo_correspondenc

Armazena tipos de correspondência usados para classificar serviços postais.

| Coluna | Descrição |
|---|---|
| id_md_cor_tipo_correspondenc | Número ID que identifica o tipo de correspondência. |
| nome_imagem_chancela | Armazena o nome da imagem de chancela usada pelo tipo de correspondência. |
| nome_tipo | Armazena o nome do tipo de correspondência. |
| sin_ar | Variável categórica que indica se o tipo de correspondência admite aviso de recebimento:<br><br><ul><li>S = Admite aviso de recebimento</li><li>N = Não admite aviso de recebimento</li></ul> |

## md_cor_tipo_objeto

Armazena o domínio de tipos de embalagem postal.

| Coluna | Descrição |
|---|---|
| id_md_cor_tipo_objeto | Número ID que identifica o tipo de embalagem. |
| codigo_correio | Código do tipo nos Correios: 001 envelope; 002 caixa; 003 cilindro. |
| nome | Armazena o nome do tipo de embalagem. |

## md_cor_unidade_exp

Registra unidades do SEI habilitadas como unidades expedidoras.

| Coluna | Descrição |
|---|---|
| id_unidade | Número ID da unidade expedidora no SEI. |
| sin_ativo | Variável categórica que indica se a unidade expedidora está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## rel_contato_justificativa

Associa contatos não habilitados para expedição às respectivas justificativas.

| Coluna | Descrição |
|---|---|
| id_rel_contato_justificativa | Número ID que identifica a associação. |
| id_contato | Número ID do contato não habilitado para expedição. |
| id_md_cor_justificativa | Número ID da justificativa aplicada ao contato. |
