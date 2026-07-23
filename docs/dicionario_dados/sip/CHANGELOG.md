# Changelog do SIP

## [3.2.0]

### Adicionado

- **Tabela `login_sso`**
- **Tabela `rel_sistema_servico_sso`**
- **Tabela `servico_sso`**
- **Tabela `usuario_login`**
- **Tabela `infra_navegador_verificacao`**
- **Tabela `assinatura_sso`**

### Alterado

- **Tabela `infra_erro_php`**
  - **Colunas**
    - **Nova `quantidade`**: `tipoNumeroGrande() NULL`.
- **Tabela `infra_auditoria`**
  - **Colunas**
    - **Alterada `recurso`**: finalizada como `tipoTextoVariavel(100) NOT NULL`.
- **Tabela `infra_regra_auditoria_recurso`**
  - **Colunas**
    - **Alterada `recurso`**: finalizada como `tipoTextoVariavel(100) NOT NULL`.
- **Tabela `login`**
  - **Colunas**
    - **Nova `id_login_sso`**: `tipoTextoVariavel(26) NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_login_login_sso`**: `id_login_sso` → `login_sso.id_login_sso`.
- **Tabela `sistema`**
  - **Colunas**
    - **Nova `alias`**: `tipoTextoVariavel(4000) NULL`.
    - **Nova `sin_autenticacao_padrao`**: finalizada como `tipoTextoFixo(1) NOT NULL`.
    - **Nova `sin_permissao`**: finalizada como `tipoTextoFixo(1) NOT NULL`.
    - **Nova `sta_confiabilidade_interno`**: `tipoTextoFixo(1) NULL`.
- **Tabela `codigo_acesso`**
  - **Colunas**
    - **Nova `identificacao`**: finalizada como `tipoTextoVariavel(50) NOT NULL`.
    - **Nova `sin_unico`**: finalizada como `tipoTextoFixo(1) NOT NULL`.
  - **Índices**
    - **Novo `i02_codigo_acesso`**: sobre (`id_usuario`, `id_sistema`, `sin_unico`).
- **Tabela `dispositivo_acesso`**
  - **Índices**
    - **Alterado `i01_dispositivo_acesso`**: de (`dth_acesso`) para (`id_codigo_acesso`, `dth_acesso`).
    - **Alterado `i02_dispositivo_acesso`**: de (`dth_liberacao`) para (`id_codigo_acesso`, `dth_liberacao`).

### Excluído

- **Tabela `dtproperties`** (somente no MySQL, se existente)
- **Tabela `infra_captcha_tentativa`**

## [3.1.0]

### Adicionado

- **Tabela `infra_erro_php`**
- **Tabela `grupo_perfil`**
- **Tabela `rel_grupo_perfil_perfil`**
- **Tabela `infra_captcha`**
- **Tabela `infra_captcha_tentativa`**

### Alterado

- **Tabela `recurso`**
  - **Colunas**
    - **Alterada `nome`**: finalizada como `tipoTextoVariavel(100) NOT NULL`.
- **Tabela `perfil`**
  - **Colunas**
    - **Nova `sin_2_fatores`**: finalizada como `tipoTextoFixo(1) NOT NULL`.
- **Tabela `usuario`**
  - **Colunas**
    - **Nova `dth_pausa_2fa`**: `tipoDataHora() NULL`.
  - **Índices**
    - **Novo `i07_usuario`**: sobre (`sin_bloqueado`).
    - **Novo `i08_usuario`**: sobre (`dth_pausa_2fa`).
- **Tabela `usuario_historico`**
  - **Colunas**
    - **Nova `dth_pausa_2fa`**: `tipoDataHora() NULL`.

### Excluído

- **Tabela `seq_usuario_historico`** (somente no MySQL e no SQL Server)

## [3.0.0]

### Adicionado

- **Tabela `codigo_acesso`**
- **Tabela `usuario_historico`**
- **Tabela `codigo_bloqueio`**
- **Tabela `dispositivo_acesso`**
- **Tabela `email_sistema`**
- **Tabela `seq_usuario_historico`** (somente no MySQL e no SQL Server)

### Alterado

- **Tabela `infra_agendamento_tarefa`**
  - **Colunas**
    - **Alterada `periodicidade_complemento`**: finalizada como `tipoTextoVariavel(200) NULL`.
- **Tabela `login`**
  - **Colunas**
    - **Nova `http_client_ip`**: `tipoTextoVariavel(39) NULL`.
    - **Nova `remote_addr`**: `tipoTextoVariavel(39) NULL`.
    - **Nova `http_x_forwarded_for`**: `tipoTextoVariavel(39) NULL`.
    - **Nova `sta_login`**: `tipoTextoFixo(1) NOT NULL`.
    - **Nova `user_agent`**: `tipoTextoVariavel(500) NOT NULL`.
    - **Nova `id_dispositivo_acesso`**: `tipoTextoVariavel(26) NULL`.
    - **Nova `id_codigo_acesso`**: `tipoTextoVariavel(26) NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_login_dispositivo_acesso`**: `id_dispositivo_acesso` → `dispositivo_acesso.id_dispositivo_acesso`.
    - **Nova `fk_login_codigo_acesso`**: `id_codigo_acesso` → `codigo_acesso.id_codigo_acesso`.
  - **Chaves primárias**
    - **Alterada `pk_login`**: recriada no Oracle sobre (`id_login`, `id_usuario`, `id_sistema`).
  - **Índices**
    - **Novo `i04_login`**: sobre (`id_login`, `id_sistema`, `id_usuario`, `sta_login`).
    - **Novo `i05_login`**: sobre (`id_login`, `id_sistema`, `id_usuario`, `dth_login`).
    - **Alterado `i06_login`**: recriado sobre (`hash_usuario`, `dth_login`, `sta_login`).
    - **Alterado `i07_login`**: recriado sobre (`dth_login`).
- **Tabela `usuario`**
  - **Colunas**
    - **Nova `cpf`**: `tipoNumeroGrande() NULL`.
    - **Nova `nome_registro_civil`**: finalizada como `tipoTextoVariavel(100) NOT NULL`.
    - **Nova `nome_social`**: `tipoTextoVariavel(100) NULL`.
    - **Nova `email`**: `tipoTextoVariavel(100) NULL`.
    - **Nova `sin_bloqueado`**: finalizada como `tipoTextoFixo(1) NOT NULL`.
  - **Índices**
    - **Novo `i03_usuario`**: sobre (`id_origem`).
    - **Novo `i04_usuario`**: sobre (`cpf`).
    - **Novo `i05_usuario`**: sobre (`id_usuario`, `id_orgao`, `id_origem`).
    - **Novo `i06_usuario`**: sobre (`id_usuario`, `id_orgao`, `cpf`).
- **Tabela `sistema`**
  - **Colunas**
    - **Nova `sta_2_fatores`**: finalizada como `tipoTextoFixo(1) NOT NULL`.
    - **Alterada `logo`**: recriada no Oracle como `tipoTextoGrande() NULL`.
    - **Nova `esquema_login`**: `tipoTextoVariavel(50) NULL`.
    - **Nova `servicos_liberados`**: `tipoTextoVariavel(200) NULL`.
    - **Nova `chave_acesso`**: `tipoTextoVariavel(60) NULL`.
    - **Nova `crc`**: `tipoTextoFixo(8) NULL`.
- **Tabela `orgao`**
  - **Colunas**
    - **Alterada `descricao`**: finalizada como `tipoTextoVariavel(250) NOT NULL`.

### Excluído

- **Tabela `login`**
  - **Colunas**
    - **Excluída `sin_validado`**
    - **Excluída `id_contexto`**
    - **Excluída `id_grupo_rede`**
    - **Excluída `dn_usuario`**
  - **Chaves estrangeiras**
    - **Excluída `fk_login_contexto`**
    - **Excluída `fk_login_grupo_rede`**
  - **Índices**
    - **Excluído `i03_login`**
    - **Excluído `fk_login_contexto`**
    - **Excluído `fk_login_grupo_rede`**: somente no SQL Server.
- **Tabela `contexto`**
- **Tabela `rel_grupo_rede_unidade`**
- **Tabela `grupo_rede`**

## [2.1.0]

### Alterado

- **Tabela `orgao`**
  - **Colunas**
    - **Alterada `ordem`**: finalizada no Oracle como `tipoNumero() NOT NULL`.
- **Tabela `infra_log`**
  - **Colunas**
    - **Alterada `sta_tipo`**: finalizada no Oracle como `tipoTextoFixo(1) NOT NULL`.
- **Tabela `item_menu`**
  - **Colunas**
    - **Nova `icone`**: `tipoTextoVariavel(250) NULL`.
