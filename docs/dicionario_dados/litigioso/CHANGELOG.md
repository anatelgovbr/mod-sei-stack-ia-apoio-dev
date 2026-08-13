# Changelog do Módulo SEI Litigioso

## [2.2.0]

### Adicionado

- **Tabela `md_lit_tp_info_add`**
- **Tabela `seq_md_lit_tp_info_add`**
- **Tabela `md_lit_campos_ad`**
- **Tabela `seq_md_lit_campos_ad`**
- **Tabela `md_lit_campos_ad_sel`**
- **Tabela `seq_md_lit_campos_ad_sel`**
- **Tabela `md_lit_campos_ad_form`**
- **Tabela `seq_md_lit_campos_ad_form`**
- **Tabela `md_lit_rel_opc_camp_mult`**

### Alterado

- **Tabela `md_lit_situacao_lancamento`**
  - **Colunas**
    - **Nova `sin_utilizar_agendamento`**: adicionada como `tipoTextoVariavel(1) NULL` e finalizada como `tipoTextoVariavel(1) NOT NULL`.
    - **Alterada `sin_cancelamento`**: `tipoTextoVariavel(1) NULL` para `tipoTextoVariavel(1) NOT NULL`.
- **Tabela `md_lit_situacao`**
  - **Colunas**
    - **Nova `tp_prazo`**: adicionada como `tipoTextoVariavel(1) NULL`.
- **Tabela `md_lit_processo_situacao`**
  - **Colunas**
    - **Nova `prazo`**: adicionada como `tipoTextoVariavel(30) NULL`.
    - **Nova `tp_prazo`**: adicionada como `tipoTextoVariavel(1) NULL`.
- **Tabela `md_lit_lancamento`**
  - **Colunas**
    - **Nova `prazo_defesa`**: adicionada como `tipoNumero() NULL`.
    - **Nova `tp_prazo_defesa`**: adicionada como `tipoTextoVariavel(1) NULL`.
    - **Nova `prazo_recurso`**: adicionada como `tipoNumero() NULL`.
    - **Nova `tp_prazo_recurso`**: adicionada como `tipoTextoVariavel(1) NULL`.
- **Tabela `md_lit_historic_lancamento`**
  - **Colunas**
    - **Nova `prazo_defesa`**: adicionada como `tipoNumero() NULL`.
    - **Nova `tp_prazo_defesa`**: adicionada como `tipoTextoVariavel(1) NULL`.
    - **Nova `prazo_recurso`**: adicionada como `tipoNumero() NULL`.
    - **Nova `tp_prazo_recurso`**: adicionada como `tipoTextoVariavel(1) NULL`.

## [2.1.0]

### Alterado

- **Tabela `md_lit_lancamento`**
  - **Colunas**
    - **Nova `id_md_lit_sit_dec_def`**: adicionada como `tipoNumero() NULL`.
    - **Nova `dta_decisao_definitiva`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `dta_apresentacao_recurso`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `id_situacao_decisao`**: adicionada como `tipoNumero() NULL`.
    - **Nova `id_situacao_intimacao`**: adicionada como `tipoNumero() NULL`.
    - **Nova `id_situacao_recurso`**: adicionada como `tipoNumero() NULL`.
    - **Nova `num_doc_decisao_multa`**: adicionada como `tipoTextoVariavel(50) NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk7_md_lit_lancamento`**: `id_md_lit_sit_dec_def` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
    - **Nova `fk8_md_lit_lancamento`**: `id_situacao_decisao` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
    - **Nova `fk9_md_lit_lancamento`**: `id_situacao_intimacao` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
    - **Nova `fk10_md_lit_lancamento`**: `id_situacao_recurso` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
  - **Índices**
    - **Novo `fk7_md_lit_lancamento`**: criado sobre `id_md_lit_sit_dec_def`.
    - **Novo `fk8_md_lit_lancamento`**: criado sobre `id_situacao_decisao`.
    - **Novo `fk9_md_lit_lancamento`**: criado sobre `id_situacao_intimacao`.
    - **Novo `fk10_md_lit_lancamento`**: criado sobre `id_situacao_recurso`.
- **Tabela `md_lit_historic_lancamento`**
  - **Colunas**
    - **Nova `id_md_lit_sit_dec_def`**: adicionada como `tipoNumero() NULL`.
    - **Nova `dta_decisao_definitiva`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `dta_apresentacao_recurso`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `id_situacao_decisao`**: adicionada como `tipoNumero() NULL`.
    - **Nova `id_situacao_intimacao`**: adicionada como `tipoNumero() NULL`.
    - **Nova `id_situacao_recurso`**: adicionada como `tipoNumero() NULL`.
    - **Nova `num_doc_decisao_multa`**: adicionada como `tipoTextoVariavel(50) NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk8_md_lit_historic_lancamento`**: `id_md_lit_sit_dec_def` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
    - **Nova `fk9_md_lit_historic_lanc`**: `id_situacao_decisao` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
    - **Nova `fk10_md_lit_historic_lanc`**: `id_situacao_intimacao` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
    - **Nova `fk11_md_lit_hist_lancamento`**: `id_situacao_recurso` → `md_lit_processo_situacao.id_md_lit_processo_situacao`.
  - **Índices**
    - **Novo `fk8_md_lit_historic_lancamento`**: criado sobre `id_md_lit_sit_dec_def`.
    - **Novo `fk9_md_lit_historic_lanc`**: criado sobre `id_situacao_decisao`.
    - **Novo `fk10_md_lit_historic_lanc`**: criado sobre `id_situacao_intimacao`.
    - **Novo `fk11_md_lit_hist_lancamento`**: criado sobre `id_situacao_recurso`.

## [1.10.0]

### Alterado

- **Tabela `md_lit_lancamento`**
  - **Colunas**
    - **Nova `dta_decurso_prazo_recurso`**: adicionada como `tipoDataHora() NULL`.
- **Tabela `md_lit_dado_interessado`**
  - **Colunas**
    - **Nova `cpf`**: adicionada como `tipoNumeroGrande() NULL`.
    - **Nova `cnpj`**: adicionada como `tipoNumeroGrande() NULL`.
- **Tabela `md_lit_especie_decisao`**
  - **Colunas**
    - **Alterada `sin_valor`**: renomeada de `sin_ressarcimento_valor`.
- **Tabela `md_lit_decisao`**
  - **Colunas**
    - **Alterada `valor`**: renomeada de `valor_ressarcimento`.

## [1.7.0]

### Alterado

- **Tabela `md_lit_integracao`**
  - **Colunas**
    - **Nova `tipo_cliente_ws`**: adicionada como `tipoTextoFixo(4) NULL`.
    - **Nova `versao_soap`**: adicionada como `tipoTextoFixo(5) NULL`.
- **Tabela `md_lit_servico_integracao`**
  - **Colunas**
    - **Nova `tipo_cliente_ws`**: adicionada como `tipoTextoFixo(4) NULL`.
    - **Nova `versao_soap`**: adicionada como `tipoTextoFixo(5) NULL`.
- **Tabela `md_lit_situacao_lancam_int`**
  - **Colunas**
    - **Nova `tipo_cliente_ws`**: adicionada como `tipoTextoFixo(4) NULL`.
    - **Nova `versao_soap`**: adicionada como `tipoTextoFixo(5) NULL`.

## [1.6.0]

### Alterado

- **Tabela `md_lit_situacao`**
  - **Colunas**
    - **Nova `sin_obrigatoria`**: adicionada como `tipoTextoFixo(1) NULL`.
    - **Nova `sin_alegacoes`**: adicionada como `tipoTextoFixo(1) NULL`.

## [1.5.0]

### Alterado

- **Tabela `md_lit_especie_decisao`**
  - **Colunas**
    - **Nova `sta_tipo_indicacao_multa`**: adicionada como `tipoTextoFixo(1) NULL`.
    - **Nova `sin_ressarcimento_valor`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `md_lit_decisao`**
  - **Colunas**
    - **Nova `valor_ressarcimento`**: adicionada como `tipoNumeroDecimal(19,2) NULL`.
    - **Nova `valor_multa_sem_integracao`**: adicionada como `tipoNumeroDecimal(19,2) NULL`.

## [1.4.0]

### Adicionado

- **Tabela `md_lit_adm_modalidad_outor`**
- **Tabela `seq_md_lit_adm_modalidad_outor`**
- **Tabela `md_lit_adm_tipo_outor`**
- **Tabela `seq_md_lit_adm_tipo_outor`**
- **Tabela `md_lit_rel_num_inter_tp_outor`**

### Alterado

- **Tabela `md_lit_integracao`**
  - **Colunas**
    - **Nova `sin_vincular_lancamento`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `md_lit_rel_num_inter_modali`**
  - **Colunas**
    - **Nova `id_md_lit_adm_modalidad_outor`**: adicionada como `tipoNumero() NOT NULL`.
  - **Chaves estrangeiras**
    - **Alterada `fk2_md_lit_rel_num_inter_moda`**: `id_md_lit_modalidade` → `md_lit_adm_modalidad_outor.id_md_lit_adm_modalidad_outor`.
  - **Chaves primárias**
    - **Alterada `pk1_md_lit_rel_num_inter_moda`**: (`id_md_lit_numero_interessado`, `id_md_lit_modalidade`) para (`id_md_lit_numero_interessado`, `id_md_lit_adm_modalidad_outor`).
  - **Índices**
    - **Alterado `fk2_md_lit_rel_num_inter_moda`**: coluna `id_md_lit_modalidade` para `id_md_lit_adm_modalidad_outor`.
  - **Propriedades da tabela**
    - **Alterada `recriação física`**: excluída e recriada fisicamente com `id_md_lit_adm_modalidad_outor`, nova chave estrangeira para `md_lit_adm_modalidad_outor.id_md_lit_adm_modalidad_outor` e nova chave primária composta por (`id_md_lit_numero_interessado`, `id_md_lit_adm_modalidad_outor`).

### Excluído

- **Tabela `md_lit_rel_num_inter_uf`**
- **Tabela `md_lit_rel_num_inter_cidade`**
- **Tabela `md_lit_rel_servico_modalidade`**
- **Tabela `md_lit_rel_servico_abrangen`**
- **Tabela `md_lit_rel_num_inter_abrang`**
- **Tabela `md_lit_abrangencia`**
- **Tabela `seq_md_lit_abrangencia`**
- **Tabela `md_lit_modalidade`**
- **Tabela `seq_md_lit_modalidade`**
- **Tabela `md_lit_rel_num_inter_modali`**
  - **Colunas**
    - **Excluída `id_md_lit_modalidade`**

## [1.3.0]

### Alterado

- **Tabela `md_lit_reinciden_anteceden`**
  - **Colunas**
    - **Nova `tp_regra_reincidencia`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `md_lit_decisao`**
  - **Colunas**
    - **Nova `sin_ultima_decisao`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `md_lit_historic_lancamento`**
  - **Colunas**
    - **Alterada `justificativa`**: `tipoTextoVariavel(100) NULL` para `tipoTextoVariavel(250) NULL`.
- **Tabela `md_lit_rel_disp_norm_conduta`**
  - **Chaves primárias**
    - **Alterada `pk_md_lit_rel_disp_norm_condut`**: renomeada de `pk_md_lit_rel_disp_norm_conduta` no estado físico compatível.
- **Tabela `md_lit_rel_disp_norm_tipo_ctrl`**
  - **Chaves primárias**
    - **Alterada `pk_md_lit_rel_disp_norm_tp_ctr`**: renomeada de `pk_md_lit_rel_disp_norm_tipo_ctrl` no estado físico compatível.

## [1.2.0]

### Alterado

- **Tabela `md_lit_decisao`**
  - **Colunas**
    - **Nova `sin_cadastro_parcial`**: adicionada como `tipoTextoFixo(1) NULL`.

## [1.1.0]

### Adicionado

- **Tabela `md_lit_rel_decisao_uf`**

### Alterado

- **Tabela `md_lit_rel_dis_nor_con_ctr`**
  - **Colunas**
    - **Alterada `dta_infracao`**: `tipoDataHora() NOT NULL` para `tipoDataHora() NULL`.
    - **Nova `dta_infracao_periodo_inicial`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `dta_infracao_periodo_final`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `sta_infracao_data`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `md_lit_decisao`**
  - **Colunas**
    - **Nova `sta_localidade`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `md_lit_rel_tipo_ctrl_tipo_dec`**
  - **Colunas**
    - **Nova `id_md_lit_especie_decisao`**: adicionada como `tipoNumero() NULL`, preenchida e finalizada como `tipoNumero() NOT NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_rel_tipo_ctrl_tipo_dec_03`**: `id_md_lit_especie_decisao` → `md_lit_especie_decisao.id_md_lit_especie_decisao`.
  - **Chaves primárias**
    - **Alterada `pk_md_lit_rel_tipo_ctrl_tipo`**: substitui `pk_lit_rel_tipo_ctrl_tipo_dec1`; (`id_md_lit_tipo_controle`, `id_md_lit_tipo_decisao`) para (`id_md_lit_tipo_decisao`, `id_md_lit_tipo_controle`, `id_md_lit_especie_decisao`).
  - **Índices**
    - **Novo `fk_rel_tipo_ctrl_tipo_dec_03`**: criado sobre `id_md_lit_especie_decisao`.

## [1.0.0]

### Adicionado

- **Tabela `md_lit_reinciden_anteceden`**
- **Tabela `seq_md_lit_reinciden_anteceden`**
- **Tabela `md_lit_rel_tp_dec_rein_ante`**
- **Tabela `md_lit_motivo`**
- **Tabela `seq_md_lit_motivo`**
- **Tabela `md_lit_rel_tp_control_moti`**
- **Tabela `md_lit_rel_controle_motivo`**

## [0.0.4]

### Adicionado

- **Tabela `md_lit_tipo_decisao`**
- **Tabela `seq_md_lit_tipo_decisao`**
- **Tabela `md_lit_especie_decisao`**
- **Tabela `seq_md_lit_especie_decisao`**
- **Tabela `md_lit_rel_tp_especie_dec`**
- **Tabela `md_lit_obrigacao`**
- **Tabela `seq_md_lit_obrigacao`**
- **Tabela `md_lit_rel_esp_decisao_obr`**
- **Tabela `md_lit_rel_tipo_ctrl_tipo_dec`**
- **Tabela `md_lit_controle`**
- **Tabela `seq_md_lit_controle`**
- **Tabela `md_lit_rel_dis_nor_con_ctr`**
- **Tabela `seq_md_lit_rel_dis_nor_con_ctr`**
- **Tabela `md_lit_rel_protoco_protoco`**
- **Tabela `seq_md_lit_rel_protoco_protoco`**
- **Tabela `md_lit_modalidade`**
- **Tabela `seq_md_lit_modalidade`**
- **Tabela `md_lit_abrangencia`**
- **Tabela `seq_md_lit_abrangencia`**
- **Tabela `md_lit_servico_integracao`**
- **Tabela `seq_md_lit_servico_integracao`**
- **Tabela `md_lit_servico`**
- **Tabela `seq_md_lit_servico`**
- **Tabela `md_lit_rel_servico_abrangen`**
- **Tabela `md_lit_rel_servico_modalidade`**
- **Tabela `md_lit_dado_interessado`**
- **Tabela `seq_md_lit_dado_interessado`**
- **Tabela `md_lit_nome_funcional`**
- **Tabela `seq_md_lit_nome_funcional`**
- **Tabela `md_lit_param_interessado`**
- **Tabela `seq_md_lit_param_interessado`**
- **Tabela `md_lit_funcionalidade`**
- **Tabela `seq_md_lit_funcionalidade`**
- **Tabela `md_lit_integracao`**
- **Tabela `seq_md_lit_integracao`**
- **Tabela `md_lit_mapea_param_saida`**
- **Tabela `seq_md_lit_mapea_param_saida`**
- **Tabela `md_lit_mapea_param_entrada`**
- **Tabela `seq_md_lit_mapea_param_entrada`**
- **Tabela `md_lit_numero_interessado`**
- **Tabela `seq_md_lit_numero_interessado`**
- **Tabela `md_lit_rel_num_inter_modali`**
- **Tabela `md_lit_rel_num_inter_abrang`**
- **Tabela `md_lit_rel_num_inter_servico`**
- **Tabela `md_lit_rel_num_inter_cidade`**
- **Tabela `md_lit_rel_num_inter_uf`**
- **Tabela `md_lit_campo_integracao`**
- **Tabela `md_lit_mapea_param_valor`**
- **Tabela `seq_md_lit_mapea_param_valor`**
- **Tabela `md_lit_processo_situacao`**
- **Tabela `seq_md_lit_processo_situacao`**
- **Tabela `md_lit_decisao`**
- **Tabela `seq_md_lit_decisao`**
- **Tabela `md_lit_situacao_lancam_int`**
- **Tabela `seq_md_lit_situacao_lancam_int`**
- **Tabela `md_lit_situacao_lancamento`**
- **Tabela `seq_md_lit_situacao_lancamento`**
- **Tabela `md_lit_lancamento`**
- **Tabela `seq_md_lit_lancamento`**
- **Tabela `md_lit_historic_lancamento`**
- **Tabela `seq_md_lit_historic_lancamento`**
- **Tabela `md_lit_cancela_lancamento`**
- **Tabela `seq_md_lit_cancela_lancamento`**
- **Tabela `md_lit_rel_decis_lancament`**
- **Tabela `md_lit_rel_disp_norm_revogado`**

### Alterado

- **Tabela `md_lit_situacao`**
  - **Colunas**
    - **Nova `sin_decisoria`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `md_lit_tipo_controle`**
  - **Colunas**
    - **Nova `sin_param_modal_compl_interes`**: adicionada como `tipoTextoVariavel(1) NULL`.
- **Tabela `md_lit_mapea_param_entrada`**
  - **Colunas**
    - **Nova `id_md_lit_campo_integracao`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk3_md_lit_mapea_param_entrada`**: `id_md_lit_campo_integracao` → `md_lit_campo_integracao.id_md_lit_campo_integracao`.
- **Tabela `md_lit_mapea_param_saida`**
  - **Colunas**
    - **Nova `id_md_lit_campo_integracao`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk3_md_lit_mapea_param_saida`**: `id_md_lit_campo_integracao` → `md_lit_campo_integracao.id_md_lit_campo_integracao`.

## [0.0.3]

### Adicionado

- **Tabela `md_lit_conduta`**
- **Tabela `seq_md_lit_conduta`**
- **Tabela `md_lit_disp_normat`**
- **Tabela `seq_md_lit_disp_normat`**
- **Tabela `md_lit_rel_disp_norm_conduta`**
- **Tabela `md_lit_rel_disp_norm_tipo_ctrl`**
- **Tabela `md_lit_assoc_disp_normat`**
- **Tabela `seq_md_lit_assoc_disp_normat`**

## [0.0.2]

### Adicionado

- **Tabela `md_lit_tipo_controle`**
- **Tabela `seq_md_lit_tipo_controle`**
- **Tabela `md_lit_fase`**
- **Tabela `seq_md_lit_fase`**
- **Tabela `md_lit_rel_tp_controle_usu`**
- **Tabela `md_lit_rel_tp_controle_unid`**
- **Tabela `md_lit_rel_tp_controle_proced`**
- **Tabela `md_lit_rel_tp_ctrl_proc_sobres`**
- **Tabela `md_lit_situacao`**
- **Tabela `seq_md_lit_situacao`**
- **Tabela `md_lit_rel_sit_serie`**
