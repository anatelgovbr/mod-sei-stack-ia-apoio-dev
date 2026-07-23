# Changelog do Módulo Integração Tramita GOV.BR

## [3.7.0]

### Adicionado

- **Tabela `md_pen_uni_restr`**

### Alterado

- **Tabela `md_pen_bloco_processo`** (tabela `md_pen_expedir_lote` renomeada para este nome nesta versão)
  - **Colunas**
    - **Nova `dth_atualizado`**
    - **Nova `dth_envio`**
    - **Nova `id_protocolo`**
    - **Nova `id_bloco`**
    - **Nova `sequencia`**
    - **Nova `id_andamento`**
    - **Nova `id_atividade_expedicao`**
    - **Nova `tentativas`**
    - **Alterada `id_repositorio_destino`**
    - **Alterada `str_repositorio_destino`**
    - **Alterada `id_repositorio_origem`**
    - **Alterada `id_unidade_origem`**
    - **Alterada `id_unidade_destino`**
    - **Alterada `str_unidade_destino`**
    - **Alterada `id_usuario`**
    - **Alterada `id_unidade`**
    - **Alterada `id_lote` para `id_bloco_processo`**
  - **Chaves estrangeiras**
    - **Nova `fk_md_pen_bloco_proc_procedi`**: `id_protocolo` → `protocolo.id_protocolo`.
    - **Nova `fk_md_pen_bloco_processo_bl`**: `id_bloco` → `md_pen_bloco.id`.
- **Tabela `md_pen_bloco`**
  - **Colunas**
    - **Nova `ordem`**
- **Tabela `md_pen_envio_comp_digitais`**
  - **Colunas**
    - **Alterada `str_estrutura` (via coluna auxiliar `str_estrutura_novo`)**
    - **Alterada `str_unidade_pen` (via coluna auxiliar `str_unidade_pen_novo`)**

### Excluído

- **Tabela `md_pen_bloco_protocolo`** (criada na 3.6.0, removida nesta versão).
- **Tabela `md_pen_rel_expedir_lote`** (removida junto com a tabela `md_pen_expedir_lote` que a referenciava).

## [3.6.0]

### Adicionado

- **Tabela `md_pen_bloco`**
- **Tabela `md_pen_bloco_protocolo`** (removida na 3.7.0)
- **Tabela `md_pen_envio_comp_digitais`**

## [3.5.0]

### Adicionado

- **Tabela `md_pen_orgao_externo`**
- **Tabela `md_pen_map_tipo_processo`**

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
    - **Alterada `ticket_envio_componentes`** (recriada via coluna auxiliar `ticket_envio_componentes_temp`).
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

## [3.1.22]

### Alterado

- **Tabela `md_pen_rel_expedir_lote`** (renomeada a partir de `md_pen_rel_expedir_lote_procedimento`)

## [3.1.0]

### Adicionado

- **Tabela `md_pen_expedir_lote`** (renomeada para `md_pen_bloco_processo` na versão 3.7.0)
- **Tabela `md_pen_rel_expedir_lote`** (removida na versão 3.7.0)

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
    - **Alterada `valor`** (recriada via coluna auxiliar `valor_novo`).

### Excluído

- **Tabela `md_pen_especie_documental`**
  - **Colunas**
    - **Excluída `descricao`** (não mais necessária a partir desta versão).
- **Tabela `md_pen_rel_doc_map_enviado`**
  - **Colunas**
    - **Excluída `sin_padrao`** (tabela recriada nesta faixa de versão via tabela temporária `md_pen_rel_doc_map_enviado_tmp`).
- **Tabela `md_pen_rel_doc_map_recebido`**
  - **Colunas**
    - **Excluída `sin_padrao`** (tabela recriada nesta faixa de versão via tabela temporária `md_pen_rel_doc_map_recebido_tm`).

## [1.5.0]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Nova `id_procedimento_anexado`**
    - **Nova `protocolo_procedimento_anexado`**
    - **Nova `ordem_documento_anexado`**

## [1.4.2]

### Alterado

- **Tabela `md_pen_recibo_tramite_recebido`**
  - **Chaves primárias**
    - **Alterada `pk_md_pen_recibo_tramite_receb`**: recriada sobre (`numero_registro`, `id_tramite`).

## [1.4.1]

### Alterado

- **Tabela `md_pen_recibo_tramite`**
  - **Colunas**
    - **Alterada `hash_assinatura`**
- **Tabela `md_pen_recibo_tramite_enviado`**
  - **Colunas**
    - **Alterada `hash_assinatura`**
- **Tabela `md_pen_recibo_tramite_recebido`**
  - **Colunas**
    - **Alterada `hash_assinatura`**
  - **Chaves primárias**
    - **Alterada `pk_md_pen_recibo_tramite_receb`**: recriada sobre (`numero_registro`, `id_tramite`).

## [1.4.0]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Alterada `ordem_documento`**
  - **Chaves primárias**
    - **Alterada `pk_md_pen_componente_digital`**: recriada sobre (`numero_registro`, `id_procedimento`, `id_documento`, `id_tramite`, `ordem`).
- **Tabela `md_pen_parametro`**
  - **Colunas**
    - **Nova `sequencia`**
- **Tabela `md_pen_processo_eletronico`**
  - **Colunas**
    - **Alterada `sta_tipo_protocolo`**

## [1.2.1]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Nova `codigo_especie`**
    - **Nova `nome_especie_produtor`**

## [1.1.16]

### Alterado

- **Tabela `md_pen_procedimento_andamento`**
  - **Colunas**
    - **Alterada `numero_registro`**

## [1.1.15]

### Alterado

- **Tabela `md_pen_procedimento_andamento`**
  - **Colunas**
    - **Alterada `numero_registro`**

## [1.1.14]

### Alterado

- **Tabela `md_pen_componente_digital`**
  - **Colunas**
    - **Alterada `nome`**
- **Tabela `md_pen_rel_doc_map_enviado`**
  - **Índices**
    - **Novo `ak1_rel_doc_map_enviado`**: único, sobre `id_serie`.
- **Tabela `md_pen_rel_doc_map_recebido`**
  - **Índices**
    - **Novo `ak1_rel_doc_map_recebido`**: único, sobre `codigo_especie`.

## [1.1.13]

### Alterado

- **Tabela `md_pen_procedimento_andamento`**
  - **Colunas**
    - **Alterada `numero_registro`**

## [1.1.12]

### Alterado

- **Tabela `md_pen_tramite`**
  - **Colunas**
    - **Nova `sta_tipo_tramite`**
- **Tabela `md_pen_procedimento_andamento`**
  - **Colunas**
    - **Nova `numero_registro`**
    - **Alterada `id_procedimento`**

## [1.1.8]

### Alterado

- **Tabela `md_pen_tramite`**
  - **Colunas**
    - **Nova `id_repositorio_origem`**
    - **Nova `id_estrutura_origem`**
    - **Nova `id_repositorio_destino`**
    - **Nova `id_estrutura_destino`**
- **Tabela `md_pen_tramite_processado`**
  - **Chaves primárias**
    - **Alterada `pk_md_pen_tramite_processado`**: recriada sobre (`id_tramite`, `tipo_tramite_processo`).

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

- **Tabela `md_pen_hipotese_legal`**
- **Tabela `md_pen_rel_hipotese_legal`**
- **Tabela `md_pen_parametro`**

## [1.0.0]

### Adicionado

- **Tabela `md_pen_processo_eletronico`**
- **Tabela `md_pen_tramite`**
- **Tabela `md_pen_tramite_pendente`**
- **Tabela `md_pen_procedimento_andamento`**
- **Tabela `md_pen_protocolo`**
- **Tabela `md_pen_recibo_tramite`**
- **Tabela `md_pen_recibo_tramite_enviado`**
- **Tabela `md_pen_recibo_tramite_recebido`**
- **Tabela `md_pen_rel_processo_apensado`**
- **Tabela `md_pen_rel_tarefa_operacao`**
- **Tabela `md_pen_componente_digital`**
- **Tabela `md_pen_unidade`**
- **Tabela `md_pen_tramite_processado`**
- **Tabela `md_pen_rel_doc_map_enviado`**
- **Tabela `md_pen_rel_doc_map_recebido`**
- **Tabela `md_pen_recibo_tramite_hash`**

### Alterado

- **Tabela `md_pen_recibo_tramite`**
  - **Colunas**
    - **Alterada `cadeia_certificado`** (recriada via coluna auxiliar `cadeia_certificado_temp`).
- **Tabela `md_pen_recibo_tramite_enviado`**
  - **Colunas**
    - **Alterada `cadeia_certificado`** (recriada via coluna auxiliar `cadeia_certificado_temp`).

### Excluído

- **Tabela `md_pen_rel_serie_especie`** (criada e removida na mesma versão).
- **Tabela `md_pen_rel_tipo_documento_mapeamento_recebido`** (removida nesta versão).
