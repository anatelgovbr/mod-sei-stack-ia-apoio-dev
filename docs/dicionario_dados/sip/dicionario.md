# Dicionário de Dados do SIP - v3.2.4

## Índice de Tabelas

- [administrador_sistema](#administrador_sistema)
- [assinatura_sso](#assinatura_sso)
- [codigo_acesso](#codigo_acesso)
- [codigo_bloqueio](#codigo_bloqueio)
- [coordenador_perfil](#coordenador_perfil)
- [coordenador_unidade](#coordenador_unidade)
- [dispositivo_acesso](#dispositivo_acesso)
- [email_sistema](#email_sistema)
- [grupo_perfil](#grupo_perfil)
- [hierarquia](#hierarquia)
- [infra_agendamento_tarefa](#infra_agendamento_tarefa)
- [infra_auditoria](#infra_auditoria)
- [infra_captcha](#infra_captcha)
- [infra_erro_php](#infra_erro_php)
- [infra_log](#infra_log)
- [infra_navegador_verificacao](#infra_navegador_verificacao)
- [infra_parametro](#infra_parametro)
- [infra_regra_auditoria](#infra_regra_auditoria)
- [infra_regra_auditoria_recurso](#infra_regra_auditoria_recurso)
- [infra_sequencia](#infra_sequencia)
- [item_menu](#item_menu)
- [login](#login)
- [login_sso](#login_sso)
- [menu](#menu)
- [orgao](#orgao)
- [perfil](#perfil)
- [permissao](#permissao)
- [recurso](#recurso)
- [recurso_vinculado](#recurso_vinculado)
- [regra_auditoria](#regra_auditoria)
- [rel_grupo_perfil_perfil](#rel_grupo_perfil_perfil)
- [rel_hierarquia_unidade](#rel_hierarquia_unidade)
- [rel_orgao_autenticacao](#rel_orgao_autenticacao)
- [rel_perfil_item_menu](#rel_perfil_item_menu)
- [rel_perfil_recurso](#rel_perfil_recurso)
- [rel_regra_auditoria_recurso](#rel_regra_auditoria_recurso)
- [rel_sistema_servico_sso](#rel_sistema_servico_sso)
- [seq_infra_auditoria](#seq_infra_auditoria)
- [seq_infra_log](#seq_infra_log)
- [servico_sso](#servico_sso)
- [servidor_autenticacao](#servidor_autenticacao)
- [sistema](#sistema)
- [tipo_permissao](#tipo_permissao)
- [unidade](#unidade)
- [usuario](#usuario)
- [usuario_historico](#usuario_historico)
- [usuario_login](#usuario_login)

## administrador_sistema

Administração dos usuários que são administradores de cada sistema controlado pelo SIP para possuirem privilégios amplos sobre o sistema no âmbito do SIP

| Coluna | Descrição |
|---|---|
| id_sistema | Identificador do sistema controlado pelo SIP |
| id_usuario | Identificador do usuário indicado como administrador do sistema |

## assinatura_sso

Registra as etapas, conteúdos e eventuais erros das assinaturas avançadas realizadas por meio de autenticação SSO.

| Coluna | Descrição |
|---|---|
| id_assinatura_sso | Número ID que identifica o registro de assinatura SSO. |
| code_servico | Código de autorização retornado pelo serviço de assinatura e trocado por token de acesso. |
| dth_assinatura_sso | Data/hora registrada para a assinatura SSO. |
| hash_conteudo | Hash SHA-256 do conteúdo enviado para a operação criptográfica de assinatura. |
| id_login_sso | Número ID que identifica a autenticação SSO à qual a assinatura pertence. |
| identificador_conteudo | Identificador do conteúdo recebido do sistema e usado na devolução da assinatura. |
| sta_assinatura_sso | Status multi-valorado da assinatura SSO<br><br><ul><li>I = Iniciada</li><li>D = Dados obtidos</li><li>C = Código recebido</li><li>T = Token recebido</li><li>A = Assinada</li><li>E = Erro</li><li>F = Finalizada.</li></ul> |
| sta_erro | Status multi-valorado que identifica a etapa em que ocorreu erro na assinatura<br><br><ul><li>1 = Iniciar assinatura</li><li>2 = Obter dados</li><li>3 = Cadastrar dados</li><li>4 = Receber código</li><li>5 = Receber token</li><li>6 = Receber assinatura</li><li>7 = Enviar assinatura</li><li>8 = Buscar login</li><li>9 = Verificar permissão.</li></ul> |
| token_sistema | Token recebido do sistema integrado e usado para obter os conteúdos a assinar. |

## codigo_acesso

Armazena as informações de bloqueios no login

| Coluna | Descrição |
|---|---|
| id_codigo_acesso | Número ID que identifica os registros de código de acesso |
| chave_ativacao | Hash com a chave de ativação para Habilitação de Autenticação em 2 Fatores |
| chave_desativacao | Hash com a chave de desativação para desabilitação da Autenticação em 2 Fatores |
| chave_geracao | Identificação da chave do código de acesso da Habilitação de Autenticação em 2 Fatores |
| dth_acesso | Data de registro do Último Acesso do Usuário de sistema com a Autenticação em 2 Fatores |
| dth_ativacao | Data de registro da execução da chave de ativação enviada ao e-mail para Habilitação da Autenticação em 2 Fatores |
| dth_desativacao | Data de registro da execução da chave de desativação enviada ao e-mail para desabilitação de Autenticação em 2 Fatores |
| dth_envio_ativacao | Data de registro do envio ao e-mail pessoal do usuário da chave de ativação para Habilitação de Autenticação em 2 Fatores |
| dth_envio_desativacao | Data de registro do envio ao e-mail pessoal do usuário da chave de desativação da Habilitação de Autenticação em 2 Fatores |
| dth_geracao | Data de registro da geração da chave de acesso para Habilitação de Autenticação em 2 Fatores |
| email | Identificação do e-mail do usuário inserido na Habilitação de Autenticação em 2 Fatores |
| id_sistema | Identificador do sistema que foi habilitada a Autenticação em 2 Fatores |
| id_usuario | Identificador do usuário do sistema no registro da Habilitação de Autenticação em 2 Fatores |
| id_usuario_desativacao | Identificador do usuário do sistema que realizou a operação de desativação da Habilitação de Autenticação em 2 Fatores. Null se o usuário não foi desativado. |
| identificacao | Identificação do emissor exibida no aplicativo autenticador para o cadastro TOTP. |
| sin_ativo | Variável categórica que indica se a Autenticação em 2 Fatores está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_unico | Variável categórica que indica se a autenticação em dois fatores é única no SIP ou específica do sistema:<br><br><ul><li>S = Única no SIP</li><li>N = Específica do sistema</li></ul> |

## codigo_bloqueio

Armazena as informações de uso da Habilitação de Autenticação em 2 Fatores

| Coluna | Descrição |
|---|---|
| id_codigo_bloqueio | Número ID que identifica os registros de código de bloqueio |
| chave_bloqueio | Hash com a chave de bloqueio do acesso |
| dth_bloqueio | Data de registro da execução da chave de bloqueio |
| dth_envio | Data de registro do envio da chave de bloqueio |
| id_codigo_acesso | Número ID que identifica os registros de código de acesso para Habilitação de Autenticação em 2 Fatores |
| sin_ativo | Variável categórica que indica se o bloqueio está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## coordenador_perfil

Administração dos usuários que são Coordenadores de Perfil no SIP

| Coluna | Descrição |
|---|---|
| id_perfil | Identificador único do perfil |
| id_sistema | Identificador do sistema |
| id_usuario | Identificador do usuário do sistema |

## coordenador_unidade

Administração dos usuários que são Coordenadores de Unidade no SIP

| Coluna | Descrição |
|---|---|
| id_sistema | Identificador do sistema |
| id_unidade | Identificador da unidade |
| id_usuario | Identificador do usuário do sistema |

## dispositivo_acesso

Armazena as informações dos dispositivos dispensados da Autenticação em 2 Fatores

| Coluna | Descrição |
|---|---|
| id_dispositivo_acesso | Número ID que identifica os registros de acesso do dispositivo |
| chave_acesso | Hash com a chave de acesso |
| chave_dispositivo | Hash com a chave do dispositivo |
| dth_acesso | Data de registro do acesso do dispositivo |
| dth_liberacao | Data de registro da liberação do acesso do dispositivode da autenticação em 2 fatores |
| id_codigo_acesso | Número ID que identifica os registros de código de acesso |
| ip_acesso | Identificação do IP do dispositivo utilizado no acesso |
| sin_ativo | Variável categórica que indica se a liberação de acesso do dispositivo está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| user_agent | Identifica a aplicação, sistema operacional, fornecedor, e/ou versão do agente utilizado pelo usuário para acessar o sistema |

## email_sistema

Administração dos E-mails do Sistema

| Coluna | Descrição |
|---|---|
| id_email_sistema | Número ID que identifica os e-mails do sistema registrados |
| assunto | Identificação do assunto padronizado do e-mail |
| conteudo | Identificação do conteúdo padronizado do e-mail |
| de | Identificação do e-mail remetente |
| descricao | Descrição padronizada mais detalhada do conteúdo do e-mail |
| id_email_sistema_modulo | Número ID que identifica os e-mails registrados relacionados ao módulo |
| para | Identificação do destinatário do e-mail |
| sin_ativo | Variável categórica que indica se o e-mail do sistema está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## grupo_perfil

Cadastra agrupamentos de perfis pertencentes a um sistema.

| Coluna | Descrição |
|---|---|
| id_grupo_perfil | Número ID que identifica o grupo de perfis. |
| id_sistema | Número ID que identifica o sistema ao qual o grupo pertence. |
| nome | Nome do grupo de perfis, único por sistema entre registros ativos. |
| sin_ativo | Variável categórica que indica se o grupo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## hierarquia

Administração da lista de hierarquias de unidades com sua Data Inicial e Data Final, onde somente pode haver uma hierarquia por vez em uso por cada sistema controlado pelo SIP

| Coluna | Descrição |
|---|---|
| id_hierarquia | Identificador único para a hierarquia |
| descricao | Texto descritivo da hierarquia |
| dta_fim | Data final para a vigência da hierarquia |
| dta_inicio | Data de início para a vigência da hierarquia |
| nome | Nome da Hierarquia |
| sin_ativo | Variável categórica que indica se a hierarquia está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## infra_agendamento_tarefa

Administração dos agendamentos de tarefas do SIP

| Coluna | Descrição |
|---|---|
| id_infra_agendamento_tarefa | Identificador único do agendamento de tarefa para a infra |
| comando | Comando textual do agendamento de tarefa para a infra |
| descricao | Descrição do agendamento de tarefa para a infra |
| dth_ultima_conclusao | Data de última conclusão do agendamento da tarefa |
| dth_ultima_execucao | Data de última execução do agendamento da tarefa |
| email_erro | Armazena o email para envio em caso de erro |
| parametro | Armazena o parâmentro do agendamento de tarefa |
| periodicidade_complemento | Define a periodicidade complementar de execução do agendamento da tarefa para a infra |
| sin_ativo | Variável categórica que indica se o registro de infra do agendamento de tarefa está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_sucesso | Variável categórica que indica se o agendamento de tarefa da infra foi executado com sucesso:<br><br><ul><li>S = Executado com sucesso</li><li>N = Não executado com sucesso</li></ul> |
| sta_periodicidade_execucao | Status multi-valorado que identifica o tipo de periodicidade de execução:<br><br><ul><li>N = Minuto</li><li>D = Hora</li><li>S = Dia da Semana</li><li>M = Dia do Mês</li><li>A = Dia do Ano</li></ul> |

## infra_auditoria

Registros dos logs de auditoria das operações do SIP

| Coluna | Descrição |
|---|---|
| id_infra_auditoria | Identificador único referente ao registro armazenado na auditoria |
| descricao_unidade | Descrição textual da unidade referente ao registro armazenado na auditoria |
| dth_acesso | Armazena a data e o horário referente ao registro armazenado na auditoria |
| id_orgao_unidade | Identificador único do órgão da unidade referente ao registro armazenado na auditoria |
| id_orgao_usuario | Identificador do órgão do usuário referente ao registro armazenado na auditoria |
| id_orgao_usuario_emulador | Identificador do órgão do usuário emulado referente ao registro armazenado na auditoria |
| id_unidade | Identificador da unidade referente ao registro armazenado na auditoria |
| id_usuario | Identificador do usuário referente ao registro armazenado na auditoria |
| id_usuario_emulador | Identificador único do usuário emulado referente ao registro armazenado na auditoria |
| ip | Armazena o IP de acesso referente ao registro armazenado na auditoria |
| nome_usuario | Nome do usuário referente ao registro armazenado na auditoria |
| nome_usuario_emulador | Nome do usuário emulado referente ao registro armazenado na auditoria |
| operacao | Texto da operação referente ao registro armazenado na auditoria |
| recurso | Definição textual do recurso referente ao registro armazenado na auditoria |
| requisicao | Texto da requisição referente ao registro armazenado na auditoria |
| servidor | Servidor de acesso referente ao registro armazenado na auditoria |
| sigla_orgao_unidade | Sigla do órgão da unidade referente ao registro armazenado na auditoria |
| sigla_orgao_usuario | Sigla do órgão do usuário referente ao registro armazenado na auditoria |
| sigla_orgao_usuario_emulador | Sigla do órgão do usuário emulado referente ao registro armazenado na auditoria |
| sigla_unidade | Sigla da unidade referente ao registro armazenado na auditoria |
| sigla_usuario | Sigla do usuário referente ao registro armazenado na auditoria |
| sigla_usuario_emulador | Sigla do usuário emulado referente ao registro armazenado na auditoria |
| user_agent | User agent referente ao registro armazenado na auditoria |

## infra_captcha

Agrega, por identificação e dia, as quantidades de validações corretas e incorretas de CAPTCHA.

| Coluna | Descrição |
|---|---|
| acertos | Quantidade de resoluções corretas do CAPTCHA. |
| ano | Ano da data em que as validações foram contabilizadas. |
| dia | Dia da data em que as validações foram contabilizadas. |
| erros | Quantidade de resoluções incorretas do CAPTCHA. |
| identificacao | Identificação atribuída ao CAPTCHA ou ao seu contexto de uso. |
| mes | Mês da data em que as validações foram contabilizadas. |

## infra_erro_php

Registra ou contabiliza categorias tratadas de erros e warnings PHP ocorridos na infraestrutura.

| Coluna | Descrição |
|---|---|
| id_infra_erro_php | Número ID que identifica o erro PHP pelo hash da categoria, arquivo e linha. |
| arquivo | Caminho do arquivo PHP em que ocorreu o erro. |
| dth_cadastro | Data/hora do primeiro cadastro do registro de erro. |
| erro | Mensagem do erro PHP. |
| linha | Número da linha do arquivo em que ocorreu o erro. |
| quantidade | Quantidade contabilizada de ocorrências do mesmo erro. |
| sta_tipo | Status multi-valorado que identifica a categoria tratada do erro PHP<br><br><ul><li>1 = Posição de array não definida</li><li>2 = Variável não definida</li><li>3 = Propriedade não definida</li><li>4 = Leitura de propriedade em não objeto</li><li>5 = Índice em não array</li><li>6 = Conversão de array para string</li><li>7 = Recurso usado como índice</li><li>8 = Conversão de offset de string</li><li>9 = Offset de string não inicializado</li><li>10 = Offset inválido em string</li><li>11 = Argumento não passado por referência</li><li>12 = Valor não numérico.</li></ul> |

## infra_log

Registros dos logs de Erro, Aviso, Informação e Debug das operações do SIP

| Coluna | Descrição |
|---|---|
| id_infra_log | Identificador do log de acesso |
| dth_log | Armazena a data e a hora do log de acesso |
| ip | Armazena o IP do log de acesso |
| sta_tipo | Status multi-valorado que identifica o tipo de execução do log armazenado<br><br><ul><li>D = Debug</li><li>A = Aviso</li><li>I = Informação</li><li>E = Erro</li></ul> |
| texto_log | Texto do log de Erro, Aviso, Informação e Debug das operações do SEI |

## infra_navegador_verificacao

Configura quais navegadores e faixas de versão são considerados compatíveis para acesso.

| Coluna | Descrição |
|---|---|
| operador_maior | Operador aplicado à versão detectada contra o limite máximo. |
| operador_menor | Operador aplicado à versão detectada contra o limite mínimo. |
| sin_compativel | Variável categórica que indica se o navegador é compatível:<br><br><ul><li>S = Compatível</li><li>N = Não compatível</li></ul> |
| sin_verificar | Variável categórica que indica se os limites de versão devem ser verificados:<br><br><ul><li>S = Devem ser verificados</li><li>N = Não devem ser verificados</li></ul> |
| tipo_navegador | Tipo de navegador comparado com a identificação obtida do agente do usuário. |
| versao_maior | Versão usada como limite máximo da faixa de compatibilidade. |
| versao_menor | Versão usada como limite mínimo da faixa de compatibilidade. |

## infra_parametro

Administração dos parâmetros do SIP

| Coluna | Descrição |
|---|---|
| nome | Armazena o nome do parâmetro para a tabela de infra_parametro |
| valor | Armazena o valor do parâmetro para a tabela de infra_parametro |

## infra_regra_auditoria

Associativa controlada pela aplicação da regra_auditoria exclusivamente do SIP

| Coluna | Descrição |
|---|---|
| id_infra_regra_auditoria | Identificador da infra da regra de auditoria |
| descricao | Descrição textual da informação de infra da regra de auditoria |
| sin_ativo | Variável categórica que indica se a regra de auditoria está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## infra_regra_auditoria_recurso

Associativa com a tabela infra_regra_auditoria

| Coluna | Descrição |
|---|---|
| id_infra_regra_auditoria | Identificador que referencia a tabela infra_regra_auditoria |
| recurso | Campo textual que referencia a tabela de recurso |

## infra_sequencia

Armazena a sequencia de informações para cada tabela de infra do Sistema

| Coluna | Descrição |
|---|---|
| nome_tabela | Armazena o nome da tabela |
| num_atual | Armazena o valor do número atual da sequência para aquela tabela |
| num_maximo | Armazena o valor do número máximo da sequência para aquela tabela |
| qtd_incremento | Armazena o valor da quantidade de incrementos para aquela tabela |

## item_menu

Armazena as informações pertinentes aos Itens de Menus do sistema

| Coluna | Descrição |
|---|---|
| id_item_menu | Identificador único para o item de menu associado ao menu |
| descricao | Armazena o valor da descrição textual para o item de menu |
| icone | Armazena o valor do ícone associado ao item de menu |
| id_item_menu_pai | Identificador único para o item de menu pai. Este campo, quando preenchido, determina um auto-relacionamento nesta mesma tabela. O valor armazenado neste campo, deverá corresponder, quando preenchido, ao campo id_item_menu do menu pai deste menu |
| id_menu | Identificador referenciado para a tabela de menu |
| id_menu_pai | Identificador referenciado para a tabela de menu |
| id_recurso | Identificador referenciado para a tabela de recurso |
| id_sistema | Identificador referenciado para a tabela de sistema |
| rotulo | Armazena o valor do rótulo para o item de menu |
| sequencia | Armazena o valor numérico da sequência do item de menu |
| sin_ativo | Variável categórica que indica se o item de menu está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_nova_janela | Variável categórica que indica se o item está associado a uma nova janela:<br><br><ul><li>S = Associado a uma nova janela</li><li>N = Não associado a uma nova janela</li></ul> |

## login

Cadastro das informações de Login do sistema

| Coluna | Descrição |
|---|---|
| id_login | Identificador alfanumérico do login (armazena o hash do login) |
| dth_login | Armazena a data e a hora de cadastro do login |
| hash_agente | Armazena o hash do agente |
| hash_interno | Armazena o hash interno do login |
| hash_usuario | Armazena o hash do usuário |
| http_client_ip | Identifica o endereço IP ou nome DNS do cliente que fez a chamada. |
| http_x_forwarded_for | Identificação do endereço IP de origem de um cliente que se conecta a um servidor da Web por meio de um proxy HTTP ou balanceador de carga. |
| id_codigo_acesso | Número ID que identifica os registros de código de acesso |
| id_dispositivo_acesso | Número ID que identifica os registros de acesso do dispositivo |
| id_login_sso | Número ID que identifica a autenticação SSO que originou o login no sistema. |
| id_sistema | Identificador do sistema |
| id_usuario | Identificador do usuário do sistema |
| id_usuario_emulador | Identificador do emulador de usuário |
| remote_addr | Identifica o endereço IP do host remoto que fez a solicitação |
| sta_login | Status multi-valorado que identifica a situação do registro de login:<br><br><ul><li>C = Cadastrado</li><li>V = Validado</li><li>R = Removido</li></ul> |
| user_agent | Identifica a aplicação, sistema operacional, fornecedor e/ou versão do agente utilizado pelo usuário para acessar o sistema |

## login_sso

Registra autenticações SSO, seus dados de identidade, origem, destinos, estado, situação e erros.

| Coluna | Descrição |
|---|---|
| id_login_sso | Número ID que identifica a autenticação SSO. |
| cpf | Número do CPF retornado pelo serviço SSO para identificação do usuário. |
| destino_login | Endereço de retorno após a autenticação SSO. |
| destino_logout | Endereço de retorno após o encerramento da autenticação SSO. |
| dth_login_sso | Data/hora registrada para a autenticação SSO. |
| email | E-mail retornado pelo serviço SSO. |
| http_client_ip | Endereço do cliente informado no cabeçalho HTTP_CLIENT_IP. |
| http_x_forwarded_for | Endereço de origem informado no cabeçalho HTTP_X_FORWARDED_FOR. |
| id_servico_sso | Número ID que identifica o serviço SSO utilizado. |
| id_sistema | Número ID que identifica o sistema no qual a autenticação será usada. |
| nome | Nome retornado pelo serviço SSO. |
| nome_social | Nome social retornado pelo serviço SSO. |
| origem | Endereço de origem da solicitação de autenticação. |
| remote_addr | Endereço remoto capturado no início da autenticação. |
| sin_2_fatores | Variável categórica que indica se o método de autenticação em dois fatores foi informado:<br><br><ul><li>S = Informado</li><li>N = Não informado</li></ul> |
| sin_certificado_digital | Variável categórica que indica se o método de certificado digital foi informado:<br><br><ul><li>S = Informado</li><li>N = Não informado</li></ul> |
| sta_erro | Status multi-valorado que identifica a etapa de erro no fluxo SSO<br><br><ul><li>1 = Alias do sistema ausente</li><li>2 = Alias de login ausente</li><li>3 = Alias de logout ausente</li><li>4 = Falha ao iniciar autenticação</li><li>5 = Tipo de acesso inválido</li><li>6 = Erro após autenticação</li><li>7 = Erro desconhecido ao iniciar</li><li>8 = Erro ao obter dados</li><li>9 = Erro desconhecido ao processar</li><li>10 = Erro ao obter confiabilidade</li><li>11 = Confiabilidade desconhecida</li><li>12 = Credenciais inválidas</li><li>13 = Erro de logout</li><li>14 = State não identificado</li><li>15 = Code verifier não identificado</li><li>16 = Início sem ID de login</li><li>17 = Processamento sem ID de login</li><li>18 = Login já validado</li><li>19 = Início de login sem dados.</li></ul> |
| sta_login_sso | Status multi-valorado da autenticação SSO<br><br><ul><li>I = Iniciada</li><li>L = Logada</li><li>V = Validada</li><li>E = Erro</li><li>O = Logout.</li></ul> |
| sta_nivel_confiabilidade | Status multi-valorado do nível de confiabilidade da conta gov.br<br><br><ul><li>O = Ouro</li><li>P = Prata</li><li>B = Bronze.</li></ul> |
| sta_tipo_acesso | Status multi-valorado do tipo de acesso<br><br><ul><li>I = Interno</li><li>E = Externo</li><li>A = Assinatura.</li></ul> |
| state | Valor do fluxo OIDC usado para correlacionar o retorno com a autenticação iniciada. |
| telefone | Telefone retornado pelo serviço SSO. |
| user_agent | Agente do usuário que iniciou a autenticação. |

## menu

Cadastro de Menus do Sistema

| Coluna | Descrição |
|---|---|
| id_menu | Identificador único do menu |
| descricao | Armazena a descrição textual do menu |
| id_sistema | Identificador referenciado do sistema |
| nome | Armazena o nome do menu |
| sin_ativo | Variável categórica que indica se o menu está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## orgao

Cadastro de Órgaos no sistema

| Coluna | Descrição |
|---|---|
| id_orgao | Identificador único do órgão |
| descricao | Armazena a descrição textual do órgão |
| ordem | Número ordena os registros de sistema |
| sigla | Armazena a sigla do ógão |
| sin_ativo | Variável categórica que indica se o órgão está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_autenticar | Variável categórica que indica se há necessidade de autenticação:<br><br><ul><li>S = Há necessidade de autenticação</li><li>N = Não há necessidade de autenticação</li></ul> |

## perfil

Cadastro de parâmetros para perfil de acesso no sistema

| Coluna | Descrição |
|---|---|
| id_perfil | Identificador único do perfil |
| descricao | Armazena a descrição textual do perfil |
| id_sistema | Identificador referenciado do sistema |
| nome | Armazena o nome do perfil |
| sin_2_fatores | Variável categórica que indica se as permissões do perfil exigem autenticação em dois fatores:<br><br><ul><li>S = Exigem autenticação em dois fatores</li><li>N = Não exigem autenticação em dois fatores</li></ul> |
| sin_ativo | Variável categórica que indica se o perfil está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_coordenado | Variável categórica que indica se o perfil é coordenado:<br><br><ul><li>S = Coordenado</li><li>N = Não coordenado</li></ul> |

## permissao

Administração da concessão de permissão aos usuários de acordo com o sistema controlado pelo SIP, perfil, tipo de permissão e unidade

| Coluna | Descrição |
|---|---|
| dta_fim | Data fim para a vigência da permissão |
| dta_inicio | Data de início para a vigência da permissão |
| id_perfil | Identificador único do perfil |
| id_sistema | Identificador referenciado do sistema |
| id_tipo_permissao | Identificador referenciado para o tipo de permissão concedida para o usuário |
| id_unidade | Identificador referenciado da unidade |
| id_usuario | Identificador referenciado do usuário do sistema |
| sin_subunidades | Variável categórica que indica se existe permissão para subunidades:<br><br><ul><li>S = Existe permissão para subunidades</li><li>N = Não existe permissão para subunidades</li></ul> |

## recurso

Cadastro dos recursos de funcionalidades do sistema

| Coluna | Descrição |
|---|---|
| id_recurso | Identificador único do recurso |
| caminho | Armazena o caminho de acesso para o recurso |
| descricao | Armazena a descrição textual do recurso |
| id_sistema | Identificador referenciado para o sistema |
| nome | Armazena o nome do recurso |
| sin_ativo | Variável categórica que indica se o recurso está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## recurso_vinculado

Armazena os Recursos vinculados aos sistemas

| Coluna | Descrição |
|---|---|
| id_recurso_vinculado | Identificador referenciado para o recurso vinculado |
| id_recurso | Identificador referenciado para o recurso |
| id_sistema | Identificador referenciado para o sistema |
| id_sistema_vinculado | Identificador referenciado para o sistema vinculado |
| tipo_vinculo | Status multi-valorado que identifica o tipo de vinculação do recurso |

## regra_auditoria

Administração das regras de auditoria de cada sistema controlado pelo SIP, inclusive do próprio SIP

| Coluna | Descrição |
|---|---|
| id_regra_auditoria | Identificador único que armazena o número da regra de auditoria |
| descricao | Armazena a descrição textual da regra de auditoria |
| id_sistema | Identificador referenciado para o sistema |
| sin_ativo | Variável categórica que indica se a regra de auditoria está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## rel_grupo_perfil_perfil

Associa perfis a grupos de perfis dentro do mesmo sistema.

| Coluna | Descrição |
|---|---|
| id_grupo_perfil | Número ID que identifica o grupo ao qual o perfil é associado. |
| id_perfil | Número ID que identifica o perfil associado ao grupo. |
| id_sistema | Número ID que identifica o sistema que delimita a associação. |

## rel_hierarquia_unidade

Associativa entre a unidade e a hierarquização da mesma

| Coluna | Descrição |
|---|---|
| dta_fim | Data fim da configuração de hierarquia para a unidade |
| dta_inicio | Data de início da configuração de hierarquia para a unidade |
| id_hierarquia | Identificador referenciado para a hierarquia |
| id_hierarquia_pai | Identificador referenciado para a hierarquia da unidade |
| id_unidade | Identificador referenciado para a unidade |
| id_unidade_pai | Identificador referenciado para a unidade pai na hierarquia |
| sin_ativo | Variável categórica que indica se a hierarquia da unidade está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |

## rel_orgao_autenticacao

Associativa de autenticação entre o Órgão e o servidor autenticado

| Coluna | Descrição |
|---|---|
| id_orgao | Identificador referenciado do órgão |
| id_servidor_autenticacao | Identificador referenciado do servidor autenticado |
| sequencia | Armazena o valor da sequência para o órgão autenticado |

## rel_perfil_item_menu

Associativa do recuros do item de menu com o sistema de acordo com o perfil para mesmo

| Coluna | Descrição |
|---|---|
| id_item_menu | Identificador referenciado para o item de menu |
| id_menu | Identificador referenciado para o menu |
| id_perfil | Identificador referenciado para o perfil |
| id_recurso | Identificador referenciado para o recurso |
| id_sistema | Identificador referenciado para o sistema |

## rel_perfil_recurso

Associativa entre o recurso, o sistema e o perfil

| Coluna | Descrição |
|---|---|
| id_perfil | Identificador referenciado para o perfil |
| id_recurso | Identificador referenciado para o recurso |
| id_sistema | Identificador referenciado para o sistema |

## rel_regra_auditoria_recurso

Associativa entre regra_auditoria e recurso com o sistema controlado pelo SIP correspondente

| Coluna | Descrição |
|---|---|
| id_recurso | Identificador referenciado para o recurso |
| id_regra_auditoria | Identificador referenciado para a regra de auditoria |
| id_sistema | Identificador referenciado para o sistema |

## rel_sistema_servico_sso

Associa serviços SSO a sistemas, separando os vínculos de acesso interno e externo e sua ordem de exibição.

| Coluna | Descrição |
|---|---|
| id_servico_sso | Número ID que identifica o serviço SSO disponibilizado ao sistema. |
| id_sistema | Número ID que identifica o sistema que disponibiliza o serviço SSO. |
| ordem | Número que define a ordem do serviço SSO na lista daquele tipo de acesso. |
| sta_tipo_acesso | Status multi-valorado do tipo de acesso disponibilizado<br><br><ul><li>I = Interno</li><li>E = Externo.</li></ul> |

## seq_infra_auditoria

Sequence da tabela infra_auditoria

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela em que a sequence é aplicada |
| id | Número que identifica o sequencial da tabela infra_auditoria |

## seq_infra_log

Sequence da tabela infra_log

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela em que a sequence é aplicada |
| id | Número que identifica o sequencial da tabela infra_log |

## servico_sso

Configura provedores SSO/OIDC usados em autenticações e, para gov.br, em assinaturas avançadas.

| Coluna | Descrição |
|---|---|
| id_servico_sso | Número ID que identifica o serviço SSO. |
| campo_sso | Nome do atributo retornado pelo provedor usado para identificar o usuário. |
| campo_usuario | Campo local do usuário comparado com o atributo do SSO<br><br><ul><li>Cpf = CPF</li><li>Email = e-mail.</li></ul> |
| client_id | Identificador do SIP perante o provedor SSO. |
| client_id_assinatura | Identificador do SIP no serviço de assinatura avançada gov.br. |
| client_secret | Credencial secreta do SIP perante o provedor SSO. |
| client_secret_assinatura | Credencial secreta do SIP no serviço de assinatura avançada. |
| identificacao | Nome-chave usado para localizar e selecionar o provedor SSO. |
| logo | Imagem codificada em Base64 exibida no botão do serviço. |
| scope | Escopo de dados solicitado ao provedor SSO. |
| sin_ativo | Variável categórica que indica se o serviço está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sta_servico_sso | Status multi-valorado que classifica o serviço SSO<br><br><ul><li>G = Gov.br</li><li>O = Outro.</li></ul> |
| titulo | Texto usado como título do link ou botão de acesso ao SSO. |
| url_api_assinatura | Endereço-base da API de certificado e assinatura. |
| url_api_conta | Endereço da API gov.br usada para consultar a confiabilidade da conta. |
| url_authorize | Endereço do endpoint de autorização do provedor SSO. |
| url_base | Endereço-base do provedor SSO/OIDC. |
| url_base_assinatura | Endereço-base OAuth do serviço de assinatura avançada. |
| url_issuer | Identificador do emissor de identidade do provedor SSO. |
| url_logout | Endereço do endpoint de logout do provedor SSO. |
| url_token | Endereço do endpoint de token do provedor SSO. |

## servidor_autenticacao

Armazena as informações dos servidores autenticados no sistema

| Coluna | Descrição |
|---|---|
| id_servidor_autenticacao | Identificador único que armazena o servidor de autenticação |
| atributo_filtro_pesquisa | Armazena o atributo do filtro de pesquisa para o servidor de autenticação |
| atributo_retorno_pesquisa | Armazena o atributo de retorno de pesquisa para o servidor de autenticação |
| contexto_pesquisa | Armazena o contexto da pesquisa para o servidor de autenticação |
| endereco | Armazena o endereço do servidor de autenticação |
| nome | Armazena o nome do servidor de autenticação |
| porta | Armazena o valor numérico da porta do servidor de autenticação |
| senha_pesquisa | Armazena a senha de pesquisa para o servidor de autenticação |
| sta_tipo | Status multi-valorado que identifica o tipo de autenticação do servidor:<br><br><ul><li>LDAP = OpenLDAP</li><li>AD = Active Directory</li></ul> |
| sufixo | Armazena o sufixo do servidor de autenticação |
| usuario_pesquisa | Armazena o usuário de pesquisa para o servidor de autenticação |
| versao | Armazena o valor numérico da versão do servidor de autenticação |

## sistema

Administração sas informações dos sistemas

| Coluna | Descrição |
|---|---|
| id_sistema | Identificador único do sistema |
| alias | Lista de domínios adicionais autorizados como destinos de login e logout SSO. |
| chave_acesso | Hash com a chave de acesso |
| crc | CRC: cyclic redundancy checksum. Esta função pode ser usada para validar a integridade dos dados |
| descricao | Armazena a descrição textual do sistema |
| esquema_login | Esquema de cores usado no menu de login |
| id_hierarquia | Identificador referenciado da hierarquia |
| id_orgao | Identificador referenciado do órgão |
| logo | Armazena o código alfanumérico do logo do sistema |
| pagina_inicial | Armazena o endereço para página inicial do sistema |
| servicos_liberados | Identificação dos serviços liberados no respectivo sistema |
| sigla | Armazena a sigla do sistema |
| sin_ativo | Variável categórica que indica se o sistema está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_autenticacao_padrao | Variável categórica que indica se usuário e senha devem ser oferecidos no login:<br><br><ul><li>S = Devem ser oferecidos no login</li><li>N = Não devem ser oferecidos no login</li></ul> |
| sin_permissao | Variável categórica que indica se o login exige alguma permissão no sistema:<br><br><ul><li>S = Exige alguma permissão no sistema</li><li>N = Não exige alguma permissão no sistema</li></ul> |
| sta_2_fatores | Status multi-valorado que identifica o uso da autenticação em 2 fatores:<br><br><ul><li>I = Indisponível</li><li>P = Opcional</li><li>O = Obrigatória</li></ul> |
| sta_confiabilidade_interno | Status multi-valorado do nível mínimo de confiabilidade gov.br para acesso interno<br><br><ul><li>O = Ouro</li><li>P = Prata</li><li>B = Bronze.</li></ul> |
| web_service | Armazena o endereço do webservice do sistema |

## tipo_permissao

Administração dos Tipos de Permissão

| Coluna | Descrição |
|---|---|
| id_tipo_permissao | Identitificador único do tipo de permissão |
| descricao | Armazena a descrição textual do tipo de permissão |

## unidade

Cadastro de unidade organizacional no sistema

| Coluna | Descrição |
|---|---|
| id_unidade | Identificador único da unidade |
| descricao | Armazena a descrição textual da unidade |
| id_orgao | Identificador referenciado do órgão |
| id_origem | Identificador que armazena a identificação da unidade na origem, geralmente no sistema de recursos humanos do órgão |
| sigla | Armazena a sigla da unidade |
| sin_ativo | Variável categórica que indica se a unidade está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| sin_global | Variável categórica que indica se a unidade é global:<br><br><ul><li>S = Global</li><li>N = Não global</li></ul> |

## usuario

Cadastro de usuários no sistema

| Coluna | Descrição |
|---|---|
| id_usuario | Identificador único do usuário |
| cpf | Identifica o número do CPF do usuário |
| dth_pausa_2fa | Data/hora final até a qual a autenticação em dois fatores fica pausada para o usuário. |
| email | Identifica o e-mail do usuário |
| id_orgao | Identificador referenciado do órgão |
| id_origem | Identificador que armazena o número de origem do usuário |
| nome | Armazena o nome do usuário |
| nome_registro_civil | Identifica onome do registro civil do usuário |
| nome_social | Identifica o o nome social do usuário |
| sigla | Armazena a sigla do usuário |
| sin_ativo | Variável categórica que indica se o usuário está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_bloqueado | Variável categórica que indica se o usuário está bloqueado:<br><br><ul><li>S = Bloqueado</li><li>N = Não bloqueado</li></ul> |

## usuario_historico

Armazena o histórico de bloqueio, desbloqueio, pausa e remoção da pausa de autenticação em dois fatores dos usuários.

| Coluna | Descrição |
|---|---|
| id_usuario_historico | Número ID que identifica os do histórico do usuário |
| dth_operacao | Data de registro da operação |
| dth_pausa_2fa | Data/hora final da pausa da autenticação em dois fatores registrada no histórico. |
| id_codigo_acesso | Número ID que identifica os registros de código de acesso no registro da Habilitação de Autenticação em 2 Fatores |
| id_usuario | Identificador do usuário do sistema que realizou a operação no SIP |
| id_usuario_operacao | Identificador do usuário do sistema que teve o acesso alterado no SIP |
| motivo | Descrição do motivo inserido para a realização da operação |
| sta_operacao | Status multi-valorado que identifica a operação realizada no SIP<br><br><ul><li>B = Bloqueio</li><li>D = Desbloqueio</li><li>P = Pausa da autenticação em dois fatores</li><li>R = Remoção da pausa.</li></ul> |

## usuario_login

Mantém a contagem e os metadados da última tentativa de login por senha de cada usuário.

| Coluna | Descrição |
|---|---|
| dth_tentativa | Data/hora da última tentativa de login registrada. |
| http_client_ip | Último endereço do cliente informado no cabeçalho HTTP_CLIENT_IP. |
| http_x_forwarded_for | Último endereço de origem informado no cabeçalho HTTP_X_FORWARDED_FOR. |
| id_usuario | Número ID que identifica o usuário cuja contagem de tentativas é controlada. |
| remote_addr | Último endereço remoto registrado na tentativa de login. |
| tentativas | Número de tentativas acumuladas desde o último reinício da contagem. |
| user_agent | Agente do usuário da última tentativa registrada. |
