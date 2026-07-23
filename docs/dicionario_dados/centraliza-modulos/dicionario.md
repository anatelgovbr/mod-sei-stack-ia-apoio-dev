# Dicionário de Dados do Módulo SEI Centraliza Módulos - v1.0.0

## Índice de Tabelas

- [md_central_mds_dist](#md_central_mds_dist)
- [md_central_mds_instal](#md_central_mds_instal)
- [md_central_mds_mantido](#md_central_mds_mantido)
- [md_central_mds_white_url](#md_central_mds_white_url)

## md_central_mds_dist

Registra a versão de cada módulo mantido instalada em cada órgão externo e a data/hora da última atualização.

| Coluna | Descrição |
|---|---|
| id_md_central_mds_dist | Número ID que identifica o registro de módulo distribuído. |
| dth_atualizacao | Data/hora da última atualização da versão do módulo na instalação externa. |
| id_md_central_mds_instal | Número ID que identifica a instalação do órgão externo associada ao módulo distribuído. |
| id_md_central_mds_mantido | Número ID que identifica o módulo mantido associado ao registro distribuído. |
| versao_modulo | Armazena a versão do módulo instalada no órgão externo. |

## md_central_mds_instal

Armazena o cadastro e as credenciais das instalações SEI de órgãos externos que interagem com os serviços do módulo.

| Coluna | Descrição |
|---|---|
| id_md_central_mds_instal | Número ID que identifica a instalação do órgão externo. |
| cadastro | Data/hora de cadastro ou renovação da credencial da instalação. |
| chave_acesso | Armazena o hash da chave de acesso utilizada para autenticar a instalação. |
| email_administrador | Armazena o endereço de e-mail do administrador da instalação. |
| ip | Armazena o endereço IP da instalação que solicitou a chave de acesso. |
| sigla_orgao | Armazena a sigla do órgão responsável pela instalação. |
| sin_ativo | Variável categórica que indica se a instalação do órgão externo está ativa:<br><br><ul><li>S = Ativa</li><li>N = Não ativa</li></ul> |
| tipo_banco_dados | Armazena o tipo de banco de dados utilizado pela instalação do SEI. |
| url | Armazena a URL da instalação do SEI. |
| versao_sei | Armazena a versão do SEI utilizada pela instalação. |

## md_central_mds_mantido

Armazena os módulos SEI mantidos pela Anatel e seus repositórios de distribuição.

| Coluna | Descrição |
|---|---|
| id_md_central_mds_mantido | Número ID que identifica o módulo mantido pela Anatel. |
| modulo | Armazena o nome da classe de integração do módulo. |
| nome | Armazena o nome de apresentação do módulo. |
| repositorio | Armazena o nome do repositório do módulo no GitHub. |
| url_repositorio | Armazena a URL completa do repositório do módulo no GitHub da Anatel. |

## md_central_mds_white_url

Armazena os domínios permitidos na validação das URLs de instalações que solicitam chave de acesso.

| Coluna | Descrição |
|---|---|
| id_md_central_mds_white_url | Número ID que identifica o domínio permitido. |
| url | Armazena o domínio permitido usado para autorizar a URL da instalação na solicitação de chave de acesso. |
