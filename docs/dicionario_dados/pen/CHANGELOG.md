# Changelog do Módulo Integração Tramita GOV.BR

## [3.7.0]

### Adicionado

- **Tabela `md_pen_uni_restr`**
- **Tabela `md_pen_seq_uni_restr`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_bloco_processo`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)

### Alterado

- **Tabela `md_pen_bloco_processo`** (renomeada de `md_pen_expedir_lote`)
  - **Colunas**
    - **Nova `dth_atualizado`**
    - **Nova `dth_envio`**
    - **Nova `id_protocolo`**
    - **Nova `id_bloco`**
    - **Nova `sequencia`**
    - **Nova `id_andamento`**
    - **Nova `id_atividade_expedicao`**
    - **Nova `tentativas`**
    - **Alterada `id_repositorio_destino`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `str_repositorio_destino`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `id_repositorio_origem`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `id_unidade_origem`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `id_unidade_destino`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `str_unidade_destino`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `id_usuario`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `id_unidade`**: nulidade: `NOT NULL` para `NULL`.
    - **Alterada `id_bloco_processo`**: renomeada de `id_lote`.
  - **Chaves estrangeiras**
    - **Nova `fk_md_pen_bloco_proc_procedi`**: `id_protocolo` → `protocolo.id_protocolo`.
    - **Nova `fk_md_pen_bloco_processo_bl`**: `id_bloco` → `md_pen_bloco.id`.
- **Tabela `md_pen_bloco`**
  - **Colunas**
    - **Nova `ordem`**
- **Tabela `md_pen_envio_comp_digitais`**
  - **Colunas**
    - **Alterada `str_estrutura`**: tipo: texto longo para texto variável de 255 caracteres; nulidade: `NOT NULL` para `NULL`.
    - **Alterada `str_unidade_pen`**: tipo: texto longo para texto variável de 255 caracteres.

### Excluído

- **Tabela `md_pen_bloco_protocolo`**
- **Tabela `md_pen_rel_expedir_lote`**
- **Tabela `md_pen_seq_bloco_protocolo`** (somente MySQL e SQL Server; materialização de sequencial nativo)
- **Tabela `md_pen_seq_expedir_lote`** (somente MySQL e SQL Server; materialização de sequencial nativo)

## [3.6.0]

### Adicionado

- **Tabela `md_pen_bloco`**
- **Tabela `md_pen_bloco_protocolo`**
- **Tabela `md_pen_envio_comp_digitais`**
- **Tabela `md_pen_seq_bloco`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_bloco_protocolo`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_envio_comp_digitais`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)

## [3.5.0]

### Adicionado

- **Tabela `md_pen_orgao_externo`**
- **Tabela `md_pen_map_tipo_processo`**
- **Tabela `md_pen_seq_orgao_externo`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_map_tp_procedimento`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)

## [3.4.0]

### Alterado

- **Tabela `md_pen_unidade`**
  - **Colunas**
    - **Nova `sigla_unidade_rh`**
    - **Nova `nome_unidade_rh`**

## [3.3.0]

### Alterado

- **Tabela `md_pen_tramite`**
  - **Colunas**
    - **Alterada `ticket_envio_componentes`**: tipo: texto longo para texto variável de 10 caracteres.
- **Tabela `md_pen_rel_expedir_lote`**
  - **Colunas**
    - **Nova `tentativas`**
- **Tabela `md_pen_componente_digital`**
  - **Chaves primárias**
    - **Alterada `pk_md_pen_componente_digital`**: recriada sobre (`numero_registro`, `id_procedimento`, `id_documento`, `id_tramite`, `ordem_documento`, `ordem`).

## [3.2.0]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Nova `id_anexo_imutavel`**
    - **Nova `tarja_legada`**

## [3.1.0]

### Adicionado

- **Tabela `md_pen_expedir_lote`**
- **Tabela `md_pen_rel_expedir_lote`**
- **Tabela `md_pen_seq_expedir_lote`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)

## [2.1.7]

### Alterado

- **Tabela `md_pen_rel_hipotese_legal`**
  - **Índices**
    - **Novo `ak1_rel_hipotese_legal`**: único, sobre (`id_hipotese_legal`, `id_hipotese_legal_pen`, `tipo`).

## [2.1.0]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Nova `ordem_documento_referenciado`**

## [2.0.0-beta1]

### Alterado

- **Tabela `md_pen_parametro`**
  - **Colunas**
    - **Alterada `valor`**: nulidade: `NOT NULL` para `NULL`; recriada via coluna auxiliar `valor_novo`.

### Excluído

- **Tabela `md_pen_especie_documental`**
  - **Colunas**
    - **Excluída `descricao`**
- **Tabela `md_pen_rel_doc_map_enviado`**
  - **Colunas**
    - **Excluída `sin_padrao`**
  - **Índices**
    - **Excluído `ak1_rel_doc_map_enviado`**
- **Tabela `md_pen_rel_doc_map_recebido`**
  - **Colunas**
    - **Excluída `sin_padrao`**
  - **Índices**
    - **Excluído `ak1_rel_doc_map_recebido`**

## [1.5.0]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Nova `id_procedimento_anexado`**
    - **Nova `protocolo_procedimento_anexado`**
    - **Nova `ordem_documento_anexado`**

## [1.4.1]

### Alterado

- **Tabela `md_pen_recibo_tramite`**
  - **Colunas**
    - **Alterada `hash_assinatura`**: tamanho: 345 para 1000.
- **Tabela `md_pen_recibo_tramite_enviado`**
  - **Colunas**
    - **Alterada `hash_assinatura`**: tamanho: 345 para 1000.
- **Tabela `md_pen_recibo_tramite_recebido`**
  - **Colunas**
    - **Alterada `hash_assinatura`**: tamanho: 345 para 1000.
  - **Chaves primárias**
    - **Alterada `pk_md_pen_recibo_tramite_receb`**: composição: (`numero_registro`, `id_tramite`, `hash_assinatura`) para (`numero_registro`, `id_tramite`); identificador legado: `pk_md_pen_recibo_tramite_recebido` para `pk_md_pen_recibo_tramite_receb`, quando presente.
  - **Chaves estrangeiras**
    - **Alterada `fk_md_pen_recibo_receb_tram`**: composição mantida sobre (`numero_registro`, `id_tramite`) referenciando `md_pen_tramite` (`numero_registro`, `id_tramite`); identificador legado: `fk_md_pen_recibo_tramite_recebido_md_pen_tramite` para `fk_md_pen_recibo_receb_tram`, quando presente.
- **Tabela `md_pen_tramite_recibo_envio`**
  - **Colunas**
    - **Alterada `hash_assinatura`**: tamanho: 345 para 1000.

### Excluído

- **Tabela `md_pen_recibo_tramite`**
  - **Índices**
    - **Excluído `(numero_registro)`**
    - **Excluído `(id_tramite)`**
- **Tabela `md_pen_recibo_tramite_enviado`**
  - **Índices**
    - **Excluído `(numero_registro)`**
    - **Excluído `(id_tramite)`**
- **Tabela `md_pen_recibo_tramite_recebido`**
  - **Índices**
    - **Excluído `(numero_registro)`**
    - **Excluído `(id_tramite)`**
    - **Excluído `(hash_assinatura)`**
- **Tabela `md_pen_tramite_recibo_envio`**
  - **Índices**
    - **Excluído `(numero_registro)`**
    - **Excluído `(id_tramite)`**

## [1.4.0]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Nova `ordem_documento`**: tipo: número inteiro; nulidade: `NOT NULL`.
  - **Chaves primárias**
    - **Alterada `pk_md_pen_componente_digital`**: recriada sobre (`numero_registro`, `id_procedimento`, `id_documento`, `id_tramite`, `ordem`).
- **Tabela `md_pen_parametro`**
  - **Colunas**
    - **Nova `sequencia`**
- **Tabela `md_pen_processo_eletronico`**
  - **Colunas**
    - **Nova `sta_tipo_protocolo`**: tipo: texto de tamanho variável de 1 caractere; nulidade: `NOT NULL`; valor padrão: `P`.

## [1.2.1]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Nova `codigo_especie`**
    - **Nova `nome_especie_produtor`**

## [1.1.14]

### Adicionado

- **Tabela `md_pen_seq_procedimento_andam`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_hipotese_legal`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_rel_hipotese_legal`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_recibo_tramite_hash`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_rel_doc_map_enviado`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_rel_doc_map_recebid`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `md_pen_seq_tramite_pendente`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Alterada `nome`**: tamanho: 100 para 255.
- **Tabela `md_pen_rel_doc_map_enviado`**
  - **Índices**
    - **Novo `ak1_rel_doc_map_enviado`**: único, sobre `id_serie`.
- **Tabela `md_pen_rel_doc_map_recebido`**
  - **Índices**
    - **Novo `ak1_rel_doc_map_recebido`**: único, sobre `codigo_especie`.

## [1.1.12]

### Alterado

- **Tabela `md_pen_tramite`**
  - **Colunas**
    - **Nova `sta_tipo_tramite`**
- **Tabela `md_pen_procedimento_andamento`**
  - **Colunas**
    - **Nova `numero_registro`**
    - **Alterada `id_procedimento`**: nulidade: `NOT NULL` para `NULL`.

## [1.1.8]

### Alterado

- **Tabela `md_pen_tramite`**
  - **Colunas**
    - **Nova `id_repositorio_origem`**
    - **Nova `id_estrutura_origem`**
    - **Nova `id_repositorio_destino`**
    - **Nova `id_estrutura_destino`**

## [1.1.0]

### Alterado

- **Tabela `md_pen_hipotese_legal`**
  - **Colunas**
    - **Nova `identificacao`**
- **Tabela `md_pen_parametro`**
  - **Colunas**
    - **Nova `descricao`**

## [1.0.1]

### Adicionado

- **Tabela `md_pen_hipotese_legal`** (tabela e sequência legada homônima criada em `infra_sequencia`)
- **Tabela `md_pen_rel_hipotese_legal`** (tabela e sequência legada homônima criada em `infra_sequencia`)
- **Tabela `md_pen_parametro`**

## [1.0.0]

### Adicionado

- **Tabela `md_pen_processo_eletronico`**
- **Tabela `md_pen_tramite`**
- **Tabela `md_pen_especie_documental`**
- **Tabela `md_pen_tramite_pendente`** (tabela e sequência legada homônima criada em `infra_sequencia`)
- **Tabela `md_pen_tramite_recibo_envio`**
- **Tabela `md_pen_procedimento_andamento`** (tabela e sequência legada homônima criada em `infra_sequencia`)
- **Tabela `md_pen_protocolo`**
- **Tabela `md_pen_recibo_tramite`**
- **Tabela `md_pen_recibo_tramite_enviado`**
- **Tabela `md_pen_recibo_tramite_recebido`**
- **Tabela `md_pen_rel_processo_apensado`**
- **Tabela `md_pen_rel_tarefa_operacao`**
- **Tabela `md_pen_rel_tipo_doc_map_rec`**
- **Tabela `md_pen_componente_digital`**
- **Tabela `md_pen_unidade`**
- **Tabela `md_pen_tramite_processado`**
- **Tabela `md_pen_rel_doc_map_enviado`** (tabela e sequência legada homônima criada em `infra_sequencia`)
- **Tabela `md_pen_rel_doc_map_recebido`** (tabela e sequência legada homônima criada em `infra_sequencia`)
- **Tabela `md_pen_recibo_tramite_hash`** (tabela e sequência legada homônima criada em `infra_sequencia`)
