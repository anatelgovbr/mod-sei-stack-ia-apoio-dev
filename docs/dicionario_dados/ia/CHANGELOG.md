# Changelog do Módulo SEI IA

## [1.5.0]

### Adicionado

- **Tabela `md_ia_adm_ext_permitida`**
- **Tabela `md_ia_interacao_arq_avulso`**
- **Tabela `md_ia_interacao_chat_event`**

### Alterado

- **Tabela `md_ia_doc_indexaveis`**
  - **Índices**
    - **Novo `i01_md_ia_doc_indexaveis`**: sobre `sin_indexado`, `id_documento`.
    - **Novo `i02_md_ia_doc_indexaveis`**: sobre `sin_vetorizado`, `id_documento`.
- **Tabela `md_ia_proc_indexaveis`**
  - **Índices**
    - **Novo `i01_md_ia_proc_indexaveis`**: sobre `sin_indexado`, `id_procedimento`.

## [1.4.0]

### Alterado

- **Tabela `md_ia_doc_indexaveis`**
  - **Colunas**
    - **Nova `dth_vetorizacao`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `hash`**: adicionada como `tipoTextoVariavel(32) NULL`.
    - **Nova `sin_processo_aberto`**: adicionada como `tipoTextoVariavel(1) NULL`.
    - **Nova `sin_vetorizado`**: adicionada como `tipoTextoVariavel(1) NULL` e alterada para `tipoTextoVariavel(1) NOT NULL` após preenchimento dos registros existentes com `N`.
- **Tabela `md_ia_proc_indexaveis`**
  - **Colunas**
    - **Nova `dth_vetorizacao`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `sin_processo_aberto`**: adicionada como `tipoTextoVariavel(1) NULL`.
    - **Nova `sin_vetorizado`**: adicionada como `tipoTextoVariavel(1) NULL` e alterada para `tipoTextoVariavel(1) NOT NULL` após preenchimento dos registros existentes com `N`.

## [1.3.0]

### Adicionado

- **Tabela `md_ia_ods_onu_nsa`**

## [1.2.0]

### Alterado

- **Tabela `md_ia_prompts_favoritos`**
  - **Colunas**
    - **Nova `prompt`**: adicionada como `tipoTextoGrande() NULL`.

### Excluído

- **Tabela `md_ia_prompts_favoritos`**
  - **Colunas**
    - **Excluída `id_md_ia_interacao_chat`**
  - **Chaves estrangeiras**
    - **Excluída `fk1_md_ia_prompts_favoritos`**: sobre `id_md_ia_interacao_chat`.
  - **Índices**
    - **Excluído `fk1_md_ia_prompts_favoritos`**: sobre `id_md_ia_interacao_chat`.

## [1.1.0]

### Adicionado

- **Tabela `md_ia_adm_class_aut_tp`**
- **Tabela `md_ia_adm_url_integracao`**
- **Tabela `md_ia_doc_index_canc`**
- **Tabela `md_ia_doc_indexaveis`**
- **Tabela `md_ia_galeria_prompts`**
- **Tabela `md_ia_grupo_galeria_prompt`**
- **Tabela `md_ia_proc_index_canc`**
- **Tabela `md_ia_proc_indexaveis`**

### Alterado

- **Tabela `md_ia_adm_config_assist_ia`**
  - **Colunas**
    - **Nova `sin_buscar_web`**: adicionada como `tipoTextoVariavel(1) NULL`.
    - **Nova `sin_refletir`**: adicionada como `tipoTextoVariavel(1) NULL`.
- **Tabela `md_ia_adm_doc_relev`**
  - **Chaves estrangeiras**
    - **Nova `fk2_md_ia_adm_doc_relev`**: em `id_tipo_procedimento`, referenciando `tipo_procedimento.id_tipo_procedimento`.
- **Tabela `md_ia_class_meta_ods`**
  - **Colunas**
    - **Nova `id_procedimento`**: adicionada como `tipoNumeroGrande() NULL` e alterada para `tipoNumeroGrande() NOT NULL` após migração dos registros.
    - **Nova `sta_tipo_usuario`**: adicionada como `tipoTextoVariavel(1) NULL` e alterada para `tipoTextoVariavel(1) NOT NULL` após migração dos registros.
    - **Alterada `racional`**: de `tipoTextoVariavel(1000) NULL` para `tipoTextoVariavel(4000) NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk5_md_ia_class_meta_ods`**: em `id_procedimento`, referenciando `procedimento.id_procedimento`.
  - **Restrições**
    - **Nova `uq_meta_usuario_procedimento`**: única sobre `id_md_ia_adm_meta_ods`, `id_procedimento`.
- **Tabela `md_ia_hist_class`**
  - **Colunas**
    - **Nova `id_procedimento`**: adicionada como `tipoNumeroGrande() NULL` e alterada para `tipoNumeroGrande() NOT NULL` após migração dos registros.
    - **Nova `sta_tipo_usuario`**: adicionada como `tipoTextoVariavel(1) NULL` e alterada para `tipoTextoVariavel(1) NOT NULL` após migração dos registros.
    - **Alterada `racional`**: de `tipoTextoVariavel(1000) NULL` para `tipoTextoVariavel(4000) NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk6_md_ia_hist_class`**: em `id_procedimento`, referenciando `procedimento.id_procedimento`.

### Excluído

- **Tabela `md_ia_classificacao_ods`**
- **Tabela `md_ia_adm_config_assist_ia`**
  - **Colunas**
    - **Excluída `llm_ativo`**
- **Tabela `md_ia_class_meta_ods`**
  - **Colunas**
    - **Excluída `id_md_ia_classificacao_ods`**
  - **Chaves estrangeiras**
    - **Excluída `fk1_md_ia_class_meta_ods`**: sobre `id_md_ia_classificacao_ods`.
  - **Índices**
    - **Excluído `fk1_md_ia_class_meta_ods`**: sobre `id_md_ia_classificacao_ods`.
- **Tabela `md_ia_hist_class`**
  - **Colunas**
    - **Excluída `id_md_ia_classificacao_ods`**
  - **Chaves estrangeiras**
    - **Excluída `fk1_md_ia_hist_class`**: sobre `id_md_ia_classificacao_ods`.
  - **Índices**
    - **Excluído `fk1_md_ia_hist_class`**: sobre `id_md_ia_classificacao_ods`.
- **Tabela `md_ia_interacao_chat`**
  - **Colunas**
    - **Excluída `link_acesso_procedimento`**
    - **Excluída `procedimento_citado`**

## [1.0.0]

### Adicionado

- **Tabela `md_ia_adm_cfg_assi_ia_usu`**
- **Tabela `md_ia_adm_config_assist_ia`**
- **Tabela `md_ia_adm_config_similar`**
- **Tabela `md_ia_adm_doc_relev`**
- **Tabela `md_ia_adm_integ_funcion`**
- **Tabela `md_ia_adm_integracao`**
- **Tabela `md_ia_adm_meta_ods`**
- **Tabela `md_ia_adm_metadado`**
- **Tabela `md_ia_adm_objetivo_ods`**
- **Tabela `md_ia_adm_ods_onu`**
- **Tabela `md_ia_adm_perc_relev_met`**
- **Tabela `md_ia_adm_pesq_doc`**
- **Tabela `md_ia_adm_seg_doc_relev`**
- **Tabela `md_ia_adm_tp_doc_pesq`**
- **Tabela `md_ia_adm_unidade_alerta`**
- **Tabela `md_ia_class_meta_ods`**
- **Tabela `md_ia_classificacao_ods`**
- **Tabela `md_ia_grupo_prompts_fav`**
- **Tabela `md_ia_hist_class`**
- **Tabela `md_ia_interacao_chat`**
- **Tabela `md_ia_prompts_favoritos`**
- **Tabela `md_ia_topico_chat`**
