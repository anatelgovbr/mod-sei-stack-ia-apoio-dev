# Changelog do Módulo SEI IA

## [1.5.0]

### Adicionado

- **Tabela `md_ia_interacao_arq_avulso`**
- **Tabela `md_ia_adm_ext_permitida`**

### Alterado

- **Tabela `md_ia_doc_indexaveis`**
  - **Índices**
    - **Novo `i01_md_ia_doc_indexaveis`**: adicionado sobre as colunas `sin_indexado` e `id_documento`.
    - **Novo `i02_md_ia_doc_indexaveis`**: adicionado sobre as colunas `sin_vetorizado` e `id_documento`.
- **Tabela `md_ia_proc_indexaveis`**
  - **Índices**
    - **Novo `i01_md_ia_proc_indexaveis`**: adicionado sobre as colunas `sin_indexado` e `id_procedimento`.

## [1.4.0]

### Alterado

- **Tabela `md_ia_proc_indexaveis`**
  - **Colunas**
    - **Nova `sin_processo_aberto`**: adicionada como texto variável de 1 caractere, aceitando valor nulo.
    - **Nova `sin_vetorizado`**: adicionada como texto variável de 1 caractere, preenchida com `N` e finalizada como `NOT NULL`.
    - **Nova `dth_vetorizacao`**: adicionada como data/hora, aceitando valor nulo.
- **Tabela `md_ia_doc_indexaveis`**
  - **Colunas**
    - **Nova `sin_processo_aberto`**: adicionada como texto variável de 1 caractere, aceitando valor nulo.
    - **Nova `sin_vetorizado`**: adicionada como texto variável de 1 caractere, preenchida com `N` e finalizada como `NOT NULL`.
    - **Nova `dth_vetorizacao`**: adicionada como data/hora, aceitando valor nulo.
    - **Nova `hash`**: adicionada como texto variável de 32 caracteres, aceitando valor nulo.

## [1.3.0]

### Adicionado

- **Tabela `md_ia_ods_onu_nsa`**

## [1.2.0]

### Alterado

- **Tabela `md_ia_prompts_favoritos`**
  - **Colunas**
    - **Nova `prompt`**: adicionada como texto grande, aceitando valor nulo, e preenchida a partir de `md_ia_interacao_chat.pergunta`.

### Excluído

- **Tabela `md_ia_prompts_favoritos`**
  - **Colunas**
    - **Excluída `id_md_ia_interacao_chat`**: excluída após a migração para `prompt`.
  - **Chaves estrangeiras**
    - **Excluída `fk1_md_ia_prompts_favoritos`**: excluída.
  - **Índices**
    - **Excluído `fk1_md_ia_prompts_favoritos`**: excluído.

## [1.1.0]

### Adicionado

- **Tabela `md_ia_grupo_galeria_prompt`**
- **Tabela `md_ia_galeria_prompts`**
- **Tabela `md_ia_proc_indexaveis`**
- **Tabela `md_ia_proc_index_canc`**
- **Tabela `md_ia_adm_url_integracao`**
- **Tabela `md_ia_doc_indexaveis`**
- **Tabela `md_ia_doc_index_canc`**
- **Tabela `md_ia_adm_class_aut_tp`**

### Alterado

- **Tabela `md_ia_class_meta_ods`**
  - **Colunas**
    - **Alterada `racional`**: alterada de texto variável de 1.000 para 4.000 caracteres, aceitando valor nulo.
    - **Nova `sta_tipo_usuario`**: adicionada como texto variável de 1 caractere, preenchida durante a migração e finalizada como `NOT NULL`.
    - **Nova `id_procedimento`**: adicionada como número grande, preenchida durante a migração e finalizada como `NOT NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk5_md_ia_class_meta_ods`**: adicionada na coluna `id_procedimento`, referenciando `procedimento.id_procedimento`.
  - **Índices**
    - **Novo `fk5_md_ia_class_meta_ods`**: adicionado sobre a coluna `id_procedimento`.
    - **Novo `uq_meta_usuario_procedimento`**: índice único adicionado sobre as colunas `id_md_ia_adm_meta_ods` e `id_procedimento`.
- **Tabela `md_ia_hist_class`**
  - **Colunas**
    - **Alterada `racional`**: alterada de texto variável de 1.000 para 4.000 caracteres, aceitando valor nulo.
    - **Nova `sta_tipo_usuario`**: adicionada como texto variável de 1 caractere, preenchida durante a migração e finalizada como `NOT NULL`.
    - **Nova `id_procedimento`**: adicionada como número grande, preenchida durante a migração e finalizada como `NOT NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk6_md_ia_hist_class`**: adicionada na coluna `id_procedimento`, referenciando `procedimento.id_procedimento`.
  - **Índices**
    - **Novo `fk6_md_ia_hist_class`**: adicionado sobre a coluna `id_procedimento`.
- **Tabela `md_ia_adm_config_assist_ia`**
  - **Colunas**
    - **Nova `sin_refletir`**: adicionada como texto variável de 1 caractere, aceitando valor nulo, e preenchida com `N` nos registros existentes.
    - **Nova `sin_buscar_web`**: adicionada como texto variável de 1 caractere, aceitando valor nulo, e preenchida com `N` nos registros existentes.

### Excluído

- **Tabela `md_ia_interacao_chat`**
  - **Colunas**
    - **Excluída `procedimento_citado`**: excluída.
    - **Excluída `link_acesso_procedimento`**: excluída.
- **Tabela `md_ia_adm_config_assist_ia`**
  - **Colunas**
    - **Excluída `llm_ativo`**: excluída.
- **Tabela `md_ia_class_meta_ods`**
  - **Colunas**
    - **Excluída `id_md_ia_classificacao_ods`**: excluída após a migração para `id_procedimento`.
  - **Chaves estrangeiras**
    - **Excluída `fk1_md_ia_class_meta_ods`**: excluída.
  - **Índices**
    - **Excluído `fk1_md_ia_class_meta_ods`**: excluído.
- **Tabela `md_ia_hist_class`**
  - **Colunas**
    - **Excluída `id_md_ia_classificacao_ods`**: excluída após a migração para `id_procedimento`.
  - **Chaves estrangeiras**
    - **Excluída `fk1_md_ia_hist_class`**: excluída.
  - **Índices**
    - **Excluído `fk1_md_ia_hist_class`**: excluído.
- **Tabela `md_ia_classificacao_ods`**

## [1.0.0]

### Adicionado

- **Tabela `md_ia_adm_config_similar`**
- **Tabela `md_ia_adm_metadado`**
- **Tabela `md_ia_adm_perc_relev_met`**
- **Tabela `md_ia_adm_doc_relev`**
- **Tabela `md_ia_adm_seg_doc_relev`**
- **Tabela `md_ia_adm_integ_funcion`**
- **Tabela `md_ia_adm_integracao`**
- **Tabela `md_ia_adm_pesq_doc`**
- **Tabela `md_ia_adm_tp_doc_pesq`**
- **Tabela `md_ia_adm_ods_onu`**
- **Tabela `md_ia_adm_unidade_alerta`**
- **Tabela `md_ia_adm_objetivo_ods`**
- **Tabela `md_ia_adm_meta_ods`**
- **Tabela `md_ia_classificacao_ods`**
- **Tabela `md_ia_class_meta_ods`**
- **Tabela `md_ia_hist_class`**
- **Tabela `md_ia_adm_config_assist_ia`**
- **Tabela `md_ia_adm_cfg_assi_ia_usu`**
- **Tabela `md_ia_topico_chat`**
- **Tabela `md_ia_grupo_prompts_fav`**
- **Tabela `md_ia_interacao_chat`**
- **Tabela `md_ia_prompts_favoritos`**
