# Dicionário de Dados do Módulo Integração Tramita GOV.BR - v4.0.3

## Índice de Tabelas

- [md_pen_bloco](#md_pen_bloco)
- [md_pen_bloco_processo](#md_pen_bloco_processo)
- [md_pen_componente_digital](#md_pen_componente_digital)
- [md_pen_envio_comp_digitais](#md_pen_envio_comp_digitais)
- [md_pen_especie_documental](#md_pen_especie_documental)
- [md_pen_hipotese_legal](#md_pen_hipotese_legal)
- [md_pen_map_tipo_processo](#md_pen_map_tipo_processo)
- [md_pen_orgao_externo](#md_pen_orgao_externo)
- [md_pen_parametro](#md_pen_parametro)
- [md_pen_procedimento_andamento](#md_pen_procedimento_andamento)
- [md_pen_processo_eletronico](#md_pen_processo_eletronico)
- [md_pen_protocolo](#md_pen_protocolo)
- [md_pen_recibo_tramite](#md_pen_recibo_tramite)
- [md_pen_recibo_tramite_enviado](#md_pen_recibo_tramite_enviado)
- [md_pen_recibo_tramite_hash](#md_pen_recibo_tramite_hash)
- [md_pen_recibo_tramite_recebido](#md_pen_recibo_tramite_recebido)
- [md_pen_rel_doc_map_enviado](#md_pen_rel_doc_map_enviado)
- [md_pen_rel_doc_map_recebido](#md_pen_rel_doc_map_recebido)
- [md_pen_rel_hipotese_legal](#md_pen_rel_hipotese_legal)
- [md_pen_rel_processo_apensado](#md_pen_rel_processo_apensado)
- [md_pen_rel_tarefa_operacao](#md_pen_rel_tarefa_operacao)
- [md_pen_tramite](#md_pen_tramite)
- [md_pen_tramite_pendente](#md_pen_tramite_pendente)
- [md_pen_tramite_processado](#md_pen_tramite_processado)
- [md_pen_uni_restr](#md_pen_uni_restr)
- [md_pen_unidade](#md_pen_unidade)

## md_pen_bloco

Armazena os blocos usados para trâmite conjunto de múltiplos processos eletrônicos entre unidades.

| Coluna | Descrição |
|---|---|
| descricao | Armazena a descrição do bloco. |
| id | Número ID que identifica o bloco. |
| id_unidade | Número ID que identifica a unidade que criou o bloco. |
| id_usuario | Número ID que identifica o usuário que criou o bloco. |
| idx_bloco | Registro idx de indexação de informações e facilitação da pesquisa do bloco. |
| ordem | Armazena a ordem de exibição do bloco. |
| sta_estado | Status multi-valorado que identifica o estado do bloco:<br><br>A = Aberto<br>D = Aguardando Processamento<br>C = Concluído<br>P = Concluído Parcialmente<br>R = Retornado. |
| sta_tipo | Status multi-valorado que identifica o tipo do bloco:<br><br>I = Interno. |

## md_pen_bloco_processo

Associa processos do SEI aos blocos de trâmite do PEN, controlando o envio em lote pelo barramento.

| Coluna | Descrição |
|---|---|
| dth_atualizado | Data/hora da última atualização do registro. |
| dth_envio | Data/hora do envio do processo no bloco. |
| dth_registro | Data/hora de registro do processo no bloco. |
| id_andamento | Número ID que identifica o andamento do PEN associado ao envio do processo no bloco. |
| id_atividade_expedicao | Número ID que identifica a atividade de expedição associada ao processo no bloco. |
| id_bloco | Número ID que identifica o bloco ao qual o processo pertence, faz referência à tabela `md_pen_bloco`. |
| id_bloco_processo | Número ID que identifica a associação entre o processo e o bloco. |
| id_protocolo | Número ID que identifica o protocolo do processo associado ao bloco. |
| id_repositorio_destino | Número ID que identifica o repositório de destino do processo no barramento do PEN. |
| id_repositorio_origem | Número ID que identifica o repositório de origem do processo no barramento do PEN. |
| id_unidade | Número ID que identifica a unidade associada ao processo no bloco. |
| id_unidade_destino | Número ID que identifica a unidade de destino do processo no barramento do PEN. |
| id_unidade_origem | Número ID que identifica a unidade de origem do processo no barramento do PEN. |
| id_usuario | Número ID que identifica o usuário que incluiu o processo no bloco. |
| sequencia | Armazena a sequência do processo dentro do bloco. |
| str_repositorio_destino | Armazena o nome do repositório de destino do processo no barramento do PEN. |
| str_unidade_destino | Armazena o nome da unidade de destino do processo no barramento do PEN. |
| tentativas | Armazena a quantidade de tentativas de envio do processo no bloco. |

## md_pen_componente_digital

Armazena os componentes digitais (documentos e anexos) recebidos ou expedidos em um trâmite do PEN.

| Coluna | Descrição |
|---|---|
| algoritmo_hash | Armazena o algoritmo utilizado no cálculo do hash do componente digital. |
| codigo_especie | Número ID que identifica a espécie documental do componente digital no barramento do PEN, faz referência à tabela `md_pen_especie_documental`. |
| dados_complementares | Armazena dados complementares do componente digital. |
| hash_conteudo | Armazena o hash do conteúdo do componente digital. |
| id_anexo | Número ID que identifica o anexo do componente digital. |
| id_anexo_imutavel | Número ID que identifica o anexo de forma imutável, preservado mesmo após reordenação do componente digital. |
| id_documento | Número ID que identifica o documento associado ao componente digital. |
| id_procedimento | Número ID que identifica o processo associado ao componente digital. |
| id_procedimento_anexado | Número ID que identifica o processo anexado associado ao componente digital. |
| id_tramite | Número ID que identifica o trâmite associado ao componente digital, faz referência à tabela `md_pen_tramite`. |
| mime_type | Armazena o tipo MIME do componente digital. |
| nome | Armazena o nome do componente digital. |
| nome_especie_produtor | Armazena o nome da espécie documental informado pelo produtor do componente digital. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado ao componente digital. |
| ordem | Armazena a ordem do componente digital no processo. |
| ordem_documento | Armazena a ordem de exibição do documento associado ao componente digital. |
| ordem_documento_anexado | Armazena a ordem de exibição do documento no processo anexado. |
| ordem_documento_referenciado | Armazena a ordem de registro do documento referenciado, apresentado como documento anexado na árvore do processo. |
| protocolo | Armazena o número de protocolo do documento associado ao componente digital. |
| protocolo_procedimento_anexado | Armazena o número de protocolo do processo anexado associado ao componente digital. |
| sin_enviar | Variável categórica que indica se o componente digital deve ser enviado:<br><br><ul><li>S = Deve ser enviado</li><li>N = Não deve ser enviado</li></ul> |
| tamanho | Armazena o tamanho do componente digital. |
| tarja_legada | Armazena a tarja de acesso legada associada ao componente digital. |
| tipo_conteudo | Status que identifica o tipo de conteúdo do componente digital. |

## md_pen_envio_comp_digitais

Armazena as restrições de estrutura organizacional e unidade que impedem o envio de componentes digitais pelo PEN.

| Coluna | Descrição |
|---|---|
| id_comp_digitais | Número ID que identifica a restrição de envio de componentes digitais. |
| id_estrutura | Número ID que identifica a estrutura organizacional restringida no envio de componentes digitais. |
| id_unidade_pen | Número ID que identifica a unidade do PEN restringida no envio de componentes digitais. |
| str_estrutura | Armazena o nome da estrutura organizacional restringida no envio de componentes digitais. |
| str_unidade_pen | Armazena o nome da unidade do PEN restringida no envio de componentes digitais. |

## md_pen_especie_documental

Armazena as espécies documentais do vocabulário do barramento do PEN.

| Coluna | Descrição |
|---|---|
| id_especie | Número ID que identifica a espécie documental do barramento do PEN. |
| nome_especie | Armazena o nome da espécie documental do barramento do PEN. |

## md_pen_hipotese_legal

Armazena as hipóteses legais do barramento do PEN utilizadas no mapeamento de nível de acesso dos processos trocados.

| Coluna | Descrição |
|---|---|
| id_hipotese_legal | Número ID que identifica a hipótese legal do barramento do PEN. |
| identificacao | Armazena a identificação da hipótese legal no barramento do PEN. |
| nome | Armazena o nome da hipótese legal do barramento do PEN. |
| sin_ativo | Variável categórica que indica se a hipótese legal está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## md_pen_map_tipo_processo

Mapeia o tipo de processo local ao tipo de processo equivalente de outro órgão no barramento do PEN.

| Coluna | Descrição |
|---|---|
| dth_criacao | Data/hora de criação do mapeamento de tipo de processo. |
| id | Número ID que identifica o mapeamento de tipo de processo. |
| id_map_orgao | Número ID que identifica o mapeamento de órgão externo associado, faz referência à tabela `md_pen_orgao_externo`. |
| id_tipo_processo_destino | Número ID que identifica o tipo de processo de destino no barramento do PEN. |
| id_tipo_processo_origem | Número ID que identifica o tipo de processo de origem no barramento do PEN. |
| id_unidade | Número ID que identifica a unidade associada ao mapeamento de tipo de processo. |
| nome_tipo_processo | Armazena o nome do tipo de processo no barramento do PEN. |
| sin_ativo | Variável categórica que indica se o mapeamento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## md_pen_orgao_externo

Armazena o mapeamento entre a estrutura organizacional local e a de outro órgão participante do barramento do PEN.

| Coluna | Descrição |
|---|---|
| dth_criacao | Data/hora de criação do mapeamento de órgão externo. |
| id | Número ID que identifica o mapeamento de órgão externo. |
| id_estrutura_origem | Número ID que identifica a estrutura organizacional de origem no barramento do PEN. |
| id_orgao_destino | Número ID que identifica o órgão de destino no barramento do PEN. |
| id_orgao_origem | Número ID que identifica o órgão de origem no barramento do PEN. |
| id_unidade | Número ID que identifica a unidade associada ao mapeamento de órgão externo. |
| sin_ativo | Variável categórica que indica se o mapeamento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| str_estrutura_origem | Armazena o nome da estrutura organizacional de origem no barramento do PEN. |
| str_orgao_destino | Armazena o nome do órgão de destino no barramento do PEN. |
| str_orgao_origem | Armazena o nome do órgão de origem no barramento do PEN. |

## md_pen_parametro

Armazena os parâmetros de configuração do módulo PEN.

| Coluna | Descrição |
|---|---|
| descricao | Armazena a descrição do parâmetro de configuração do módulo PEN. |
| nome | Armazena o nome do parâmetro de configuração do módulo PEN. |
| sequencia | Armazena a sequência de exibição do parâmetro. |
| valor | Armazena o valor do parâmetro de configuração do módulo PEN. |

## md_pen_procedimento_andamento

Registra o andamento do processamento de um trâmite do PEN sobre um processo.

| Coluna | Descrição |
|---|---|
| data | Armazena a data do andamento do trâmite. |
| hash | Armazena o hash do andamento do trâmite. |
| id_andamento | Número ID que identifica o andamento do processo associado ao trâmite. |
| id_procedimento | Número ID que identifica o processo associado ao andamento do trâmite. |
| id_tarefa | Número ID que identifica a tarefa associada ao andamento do trâmite. |
| id_tramite | Número ID que identifica o trâmite associado ao andamento, faz referência à tabela `md_pen_tramite`. |
| mensagem | Armazena a mensagem do andamento do trâmite. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado ao andamento. |
| situacao | Status multi-valorado que identifica a situação do andamento do trâmite:<br><br><ul><li>S = Concluído</li><li>N = Falhou</li></ul> |

## md_pen_processo_eletronico

Armazena o processo eletrônico do SEI vinculado a um registro do barramento do PEN.

| Coluna | Descrição |
|---|---|
| id_procedimento | Número ID que identifica o processo do SEI associado ao registro do barramento do PEN. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN. |
| sta_tipo_protocolo | Status multi-valorado que identifica o tipo de protocolo do processo eletrônico:<br><br><ul><li>P = Processo</li><li>D = Documento avulso</li></ul> |

## md_pen_protocolo

Armazena informações complementares do PEN sobre o protocolo do SEI.

| Coluna | Descrição |
|---|---|
| id_protocolo | Número ID que identifica o protocolo do SEI. |
| sin_obteve_recusa | Variável categórica que indica se o protocolo obteve recusa de recebimento pelo PEN:<br><br><ul><li>S = Obteve recusa de recebimento pelo PEN</li><li>N = Não obteve recusa de recebimento pelo PEN</li></ul> |

## md_pen_recibo_tramite

Armazena o recibo do trâmite de um processo pelo PEN.

| Coluna | Descrição |
|---|---|
| cadeia_certificado | Armazena a cadeia do certificado digital do recibo do trâmite. |
| dth_recebimento | Data/hora de recebimento do recibo do trâmite. |
| hash_assinatura | Armazena o hash da assinatura do recibo do trâmite. |
| id_tramite | Número ID que identifica o trâmite associado ao recibo, faz referência à tabela `md_pen_tramite`. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado ao recibo. |

## md_pen_recibo_tramite_enviado

Armazena o recibo do trâmite enviado de um processo pelo PEN.

| Coluna | Descrição |
|---|---|
| cadeia_certificado | Armazena a cadeia do certificado digital do recibo do trâmite enviado. |
| dth_recebimento | Data/hora de recebimento do recibo do trâmite enviado. |
| hash_assinatura | Armazena o hash da assinatura do recibo do trâmite enviado. |
| id_tramite | Número ID que identifica o trâmite associado ao recibo enviado, faz referência à tabela `md_pen_tramite`. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado ao recibo enviado. |

## md_pen_recibo_tramite_hash

Armazena o hash de cada componente digital vinculado a um recibo de trâmite do PEN.

| Coluna | Descrição |
|---|---|
| hash_componente_digital  | Armazena o hash do componente digital associado ao recibo. |
| id_tramite | Número ID que identifica o trâmite associado ao recibo, faz referência à tabela `md_pen_tramite`. |
| id_tramite_hash | Número ID que identifica o registro de hash do recibo do trâmite. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado ao recibo. |
| tipo_recibo | Status multi-valorado que identifica o tipo de recibo do trâmite:<br><br><ul><li>1 = Recibo de envio</li><li>2 = Recibo de recebimento enviado</li><li>3 = Recibo de recebimento recebido</li></ul> |

## md_pen_recibo_tramite_recebido

Armazena o recibo do trâmite recebido de um processo pelo PEN.

| Coluna | Descrição |
|---|---|
| cadeia_certificado | Armazena a cadeia do certificado digital do recibo do trâmite recebido. |
| dth_recebimento | Data/hora de recebimento do recibo do trâmite recebido. |
| hash_assinatura | Armazena o hash da assinatura do recibo do trâmite recebido. |
| id_tramite | Número ID que identifica o trâmite associado ao recibo recebido, faz referência à tabela `md_pen_tramite`. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado ao recibo recebido. |

## md_pen_rel_doc_map_enviado

Mapeia a espécie documental do barramento do PEN ao tipo de documento local usado na expedição.

| Coluna | Descrição |
|---|---|
| codigo_especie | Número ID que identifica a espécie documental do barramento do PEN mapeada, faz referência à tabela `md_pen_especie_documental`. |
| id_mapeamento | Número ID que identifica o mapeamento entre espécie documental do PEN e tipo de documento do SEI usado na expedição. |
| id_serie | Número ID que identifica o tipo de documento do SEI mapeado para expedição. |

## md_pen_rel_doc_map_recebido

Mapeia a espécie documental do barramento do PEN ao tipo de documento local usado no recebimento.

| Coluna | Descrição |
|---|---|
| codigo_especie | Número ID que identifica a espécie documental do barramento do PEN mapeada, faz referência à tabela `md_pen_especie_documental`. |
| id_mapeamento | Número ID que identifica o mapeamento entre espécie documental do PEN e tipo de documento do SEI usado no recebimento. |
| id_serie | Número ID que identifica o tipo de documento do SEI mapeado para recebimento. |

## md_pen_rel_hipotese_legal

Associa a hipótese legal do barramento do PEN à hipótese legal equivalente do SEI.

| Coluna | Descrição |
|---|---|
| id_hipotese_legal | Número ID que identifica a hipótese legal do SEI associada ao mapeamento. |
| id_hipotese_legal_pen | Número ID que identifica a hipótese legal do barramento do PEN associada ao mapeamento, faz referência à tabela `md_pen_hipotese_legal`. |
| id_mapeamento | Número ID que identifica o mapeamento entre a hipótese legal do PEN e a hipótese legal do SEI. |
| sin_ativo | Variável categórica que indica se o mapeamento está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| tipo | Status multi-valorado que identifica o tipo do mapeamento de hipótese legal:<br><br><ul><li>E = Enviado</li><li>R = Recebido</li></ul> |

## md_pen_rel_processo_apensado

Registra o processo apensado a um processo eletrônico recebido pelo PEN.

| Coluna | Descrição |
|---|---|
| id_procedimento_apensado | Número ID que identifica o processo apensado ao processo recebido pelo PEN. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado à apensação. |
| protocolo | Armazena o número de protocolo do processo apensado. |

## md_pen_rel_tarefa_operacao

Associa a tarefa do SEI à operação equivalente do barramento do PEN.

| Coluna | Descrição |
|---|---|
| codigo_operacao | Armazena o código da operação do barramento do PEN associada à tarefa. |
| id_tarefa | Número ID que identifica a tarefa do SEI associada à operação do PEN. |

## md_pen_tramite

Armazena os trâmites de envio e recebimento de processos eletrônicos pelo PEN.

| Coluna | Descrição |
|---|---|
| dth_registro | Data/hora de registro do trâmite. |
| id_andamento | Número ID que identifica o andamento associado ao trâmite. |
| id_estrutura_destino | Número ID que identifica a estrutura organizacional de destino do trâmite no barramento do PEN. |
| id_estrutura_origem | Número ID que identifica a estrutura organizacional de origem do trâmite no barramento do PEN. |
| id_repositorio_destino | Número ID que identifica o repositório de destino do trâmite no barramento do PEN. |
| id_repositorio_origem | Número ID que identifica o repositório de origem do trâmite no barramento do PEN. |
| id_tramite | Número ID que identifica o trâmite. |
| id_unidade | Número ID que identifica a unidade associada ao trâmite. |
| id_usuario | Número ID que identifica o usuário associado ao trâmite. |
| numero_registro | Armazena o número de registro do processo no barramento do PEN associado ao trâmite. |
| sta_tipo_tramite | Status multi-valorado que identifica o tipo do trâmite:<br><br><ul><li>E = Envio</li><li>R = Recebimento</li></ul> |
| ticket_envio_componentes | Armazena o ticket de controle do envio dos componentes digitais do trâmite. |

## md_pen_tramite_pendente

Registra os trâmites do PEN pendentes de processamento.

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica o registro de trâmite pendente. |
| id_atividade_expedicao | Número ID que identifica a atividade de expedição associada ao trâmite pendente. |
| numero_tramite | Número ID que identifica o trâmite pendente de processamento, faz referência à tabela `md_pen_tramite`. |

## md_pen_tramite_processado

Controla o processamento de cada trâmite do PEN, evitando reprocessamento.

| Coluna | Descrição |
|---|---|
| dth_ultimo_processamento | Data/hora do último processamento do trâmite. |
| id_tramite | Número ID que identifica o trâmite processado, faz referência à tabela `md_pen_tramite`. |
| numero_tentativas | Armazena a quantidade de tentativas de processamento do trâmite. |
| sin_recebimento_concluido | Variável categórica que indica se o recebimento do trâmite foi concluído:<br><br><ul><li>S = Concluído</li><li>N = Não concluído</li></ul> |
| tipo_tramite_processo | Status multi-valorado que identifica o tipo de processamento do trâmite:<br><br><ul><li>RP = Processo</li><li>RR = Recibo</li></ul> |

## md_pen_uni_restr

Armazena as restrições de unidade e recursos humanos utilizadas na configuração do PEN por unidade.

| Coluna | Descrição |
|---|---|
| id | Número ID que identifica a restrição de unidade do PEN. |
| id_unidade | Número ID que identifica a unidade restringida no PEN. |
| id_unidade_restricao | Número ID que identifica a unidade de restrição vinculada à unidade do PEN. |
| id_unidade_rh | Número ID que identifica a unidade de RH da unidade restringida no PEN. |
| id_unidade_rh_restricao | Número ID que identifica a unidade de RH da unidade de restrição vinculada. |
| nome_unidade_restricao | Armazena o nome da unidade de restrição vinculada à unidade do PEN. |
| nome_unidade_rh_restricao | Armazena o nome da unidade de RH da unidade de restrição vinculada. |

## md_pen_unidade

Armazena as configurações da unidade específicas do módulo PEN.

| Coluna | Descrição |
|---|---|
| id_unidade | Número ID que identifica a unidade configurada no módulo PEN. |
| id_unidade_rh | Número ID que identifica a unidade de RH associada à unidade do PEN. |
| nome_unidade_rh | Armazena o nome da unidade de RH associada à unidade do PEN. |
| sigla_unidade_rh | Armazena a sigla da unidade de RH associada à unidade do PEN. |
