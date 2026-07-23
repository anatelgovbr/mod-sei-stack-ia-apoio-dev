# Changelog do Módulo Controle de Demandas

## [3.0.0]

### Adicionado

- **Tabela `md_ri_tp_ctrl_demanda`**
- **Tabela `md_ri_tipo_demanda`**
- **Tabela `md_ri_gp_param`**
- **Tabela `md_ri_gp_param_info_add_campo`**
- **Tabela `md_ri_gp_param_info_add_opcao`**
- **Tabela `md_ri_rel_gp_param_iac_serie`**
- **Tabela `md_ri_cad_info_add_reg`**
- **Tabela `md_ri_cad_info_add_val`**
- **Tabela `md_ri_cad_info_add_val_opc`**
- **Tabela `md_ri_gp_param_regra`**
- **Tabela `md_ri_gp_param_regra_validacao`**
- **Tabela `md_ri_rel_gp_regra_tp_cont`**
- **Tabela `md_ri_rel_gp_regra_servico`**
- **Tabela `md_ri_rel_gp_regra_tp_proc`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_cont`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_proc`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_serie`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_unid`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_gestor`**
- **Tabela `md_ri_rel_gp_param_proc`**
- **Tabela `md_ri_rel_gp_param_tema`**
- **Tabela `md_ri_rel_cad_local`**
- **Tabela `md_ri_ctrl_dem_situacao`**
- **Tabela `md_ri_ctrl_demanda`**
- **Tabela `md_ri_rel_ctrl_dem_unid`**
- **Tabela `md_ri_rel_cad_doc`**

### Alterado

- **Tabela `md_ri_tipo_controle`**
  - **Chaves estrangeiras**
    - **Nova `fk_ri_tipo_demanda_tp_ctrl`**: `id_md_ri_tp_ctrl_demanda` → `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
  - **Índices**
    - **Novo `fk_ri_tipo_demanda_tp_ctrl`**: adicionado sobre a coluna `id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_cadastro`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**
    - **Nova `id_md_ri_gp_param`**
  - **Chaves estrangeiras**
    - **Nova `fk_ri_cad_ctrl`**: `id_md_ri_tp_ctrl_demanda` → `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
    - **Nova `fk_ri_cad_gp_param`**: `id_md_ri_gp_param` → `md_ri_gp_param.id_md_ri_gp_param`.
  - **Índices**
    - **Novo `fk_ri_cad_ctrl`**: adicionado sobre a coluna `id_md_ri_tp_ctrl_demanda`.
    - **Novo `fk_ri_cad_gp_param`**: adicionado sobre a coluna `id_md_ri_gp_param`.
- **Tabela `md_ri_tipo_reiteracao`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**
  - **Chaves estrangeiras**
    - **Nova `fk_ri_reit_ctrl`**: `id_md_ri_tp_ctrl_demanda` → `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
  - **Índices**
    - **Novo `fk_ri_reit_ctrl`**: adicionado sobre a coluna `id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_tipo_resposta`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**
  - **Chaves estrangeiras**
    - **Nova `fk_ri_resp_ctrl`**: `id_md_ri_tp_ctrl_demanda` → `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
  - **Índices**
    - **Novo `fk_ri_resp_ctrl`**: adicionado sobre a coluna `id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_subtema`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**
  - **Chaves estrangeiras**
    - **Nova `fk_ri_subt_ctrl`**: `id_md_ri_tp_ctrl_demanda` → `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
  - **Índices**
    - **Novo `fk_ri_subt_ctrl`**: adicionado sobre a coluna `id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_classificacao_tema`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**
  - **Chaves estrangeiras**
    - **Nova `fk_ri_cltema_ctrl`**: `id_md_ri_tp_ctrl_demanda` → `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
  - **Índices**
    - **Novo `fk_ri_cltema_ctrl`**: adicionado sobre a coluna `id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_rel_reit_doc`**
  - **Colunas**
    - **Nova `id_md_ri_ctrl_demanda`**
  - **Chaves estrangeiras**
    - **Nova `fk_reit_doc_ctrl_dem`**: `id_md_ri_ctrl_demanda` → `md_ri_ctrl_demanda.id_md_ri_ctrl_demanda`.
  - **Índices**
    - **Novo `i01_md_ri_rel_reit_ctrl_dem`**: adicionado sobre a coluna `id_md_ri_ctrl_demanda`.
- **Tabela `md_ri_resposta`**
  - **Colunas**
    - **Nova `id_md_ri_ctrl_demanda`**
  - **Chaves estrangeiras**
    - **Nova `fk_md_ri_resposta_ctrl_dem`**: `id_md_ri_ctrl_demanda` → `md_ri_ctrl_demanda.id_md_ri_ctrl_demanda`.
  - **Índices**
    - **Novo `i01_md_ri_resposta_ctrl_dem`**: adicionado sobre a coluna `id_md_ri_ctrl_demanda`.
- **Tabela `md_ri_resposta_reiteracao`**
  - **Colunas**
    - **Nova `id_md_ri_ctrl_demanda`**
  - **Chaves estrangeiras**
    - **Nova `fk_md_ri_resp_reit_ctrl_dem`**: `id_md_ri_ctrl_demanda` → `md_ri_ctrl_demanda.id_md_ri_ctrl_demanda`.
  - **Índices**
    - **Novo `i01_md_ri_resp_reit_ctrl_dem`**: adicionado sobre a coluna `id_md_ri_ctrl_demanda`.
- **Tabela `md_ri_rel_cad_classif`**
  - **Colunas**
    - **Alterada `id_md_ri_subtema`**: `tipoNumero() NOT NULL` para `tipoNumero() NULL`.
  - **Índices**
    - **Alterado `i_md_ri_rel_cad_classif_cad`**: renomeado de `fk_md_ri_rel_cad_class_1`, mantido sobre a coluna `id_md_ri_cadastro`.
    - **Novo `uk_md_ri_rel_cad_classif`**: índice único adicionado sobre as colunas `id_md_ri_cadastro`, `id_md_ri_classificacao_tema` e `id_md_ri_subtema`.

### Excluído

- **Tabela `md_ri_rel_cad_classif`**
  - **Chaves primárias**
    - **Excluída `pk_md_ri_rel_cad_classif`**

## [1.0.0]

### Adicionado

- **Tabela `md_ri_crit_cad`**
- **Tabela `md_ri_rel_crit_cad_cont`**
- **Tabela `md_ri_rel_crit_cad_proc`**
- **Tabela `md_ri_rel_crit_cad_serie`**
- **Tabela `md_ri_rel_crit_cad_unid`**
- **Tabela `md_ri_cadastro`**
- **Tabela `md_ri_tipo_processo`**
- **Tabela `md_ri_rel_cad_tipo_prc`**
- **Tabela `md_ri_rel_cad_uf`**
- **Tabela `md_ri_rel_cad_cidade`**
- **Tabela `md_ri_servico`**
- **Tabela `md_ri_rel_cad_servico`**
- **Tabela `md_ri_subtema`**
- **Tabela `md_ri_classificacao_tema`**
- **Tabela `md_ri_rel_class_tema_subtema`**
- **Tabela `md_ri_rel_cad_classif`**
- **Tabela `md_ri_rel_cad_unidade`**
- **Tabela `md_ri_rel_cad_contato`**
- **Tabela `md_ri_tipo_controle`**
- **Tabela `md_ri_rel_cad_tp_ctrl`**
- **Tabela `md_ri_tipo_reiteracao`**
- **Tabela `md_ri_rel_reit_doc`**
- **Tabela `md_ri_rel_reit_unid`**
- **Tabela `md_ri_tipo_resposta`**
- **Tabela `md_ri_resposta`**
- **Tabela `md_ri_resposta_reiteracao`**
- **Tabela `md_ri_rel_cad_localidade`**
