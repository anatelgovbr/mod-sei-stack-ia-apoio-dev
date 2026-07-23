# Changelog do Módulo SEI Correios

## [2.7.0]

### Alterado

- **Tabela `md_cor_adm_parametro_ar`**
  - **Colunas**
    - **Nova `sin_niv_ace_doc_princ_ar`**: texto variável de 1 caractere, `DEFAULT 'S'`, `NOT NULL`.
    - **Nova `nivel_acesso_ar`**: texto fixo de 1 caractere, nula.
    - **Nova `id_hipotese_legal_ar`**: numérica, nula.
  - **Chaves estrangeiras**
    - **Nova `md_cor_p_ar_hip_leg_fk`**: `id_hipotese_legal_ar` referencia `hipotese_legal.id_hipotese_legal`.

## [2.5.0]

### Adicionado

- **Tabela `md_cor_adm_integr_tokens`**

## [2.3.0]

### Adicionado

- **Tabela `md_cor_adm_integracao`**

### Alterado

- **Tabela `md_cor_contrato`**
  - **Colunas**
    - **Alterada `id_md_cor_diretoria`**: de `NOT NULL` para nula; tipo numérico mantido.
    - **Alterada `numero_contrato`**: de texto fixo de 50 caracteres para texto variável de até 50 caracteres; manteve `NOT NULL`.
    - **Alterada `numero_contrato_correio`**: de texto fixo de 50 caracteres para texto variável de até 50 caracteres; manteve `NOT NULL`.
    - **Alterada `numero_cartao_postagem`**: de texto fixo de 50 caracteres para texto variável de até 50 caracteres; manteve `NOT NULL`.
- **Tabela `md_cor_expedicao_solicitad`**
  - **Colunas**
    - **Nova `id_pre_postagem`**: texto variável de até 100 caracteres, nula.

### Excluído

- **Tabela `md_cor_contrato`**
  - **Colunas**
    - **Excluída `url_webservice`**
    - **Excluída `codigo_administrativo`**
    - **Excluída `usuario`**
    - **Excluída `senha`**
    - **Excluída `numero_ano_contrato`**
- **Tabela `md_cor_parametro_rastreio`**

## [2.2.0]

### Alterado

- **Tabela `md_cor_servico_postal`**
  - **Colunas**
    - **Nova `sin_anexar_midia`**: texto fixo de 1 caractere; criada nula, preenchida com `N` e alterada para `NOT NULL`.

## [2.1.0]

### Alterado

- **Tabela `md_cor_adm_parametro_ar`**
  - **Colunas**
    - **Nova `dias_exp_ret_ar`**: texto variável de até 6 caracteres.
- **Tabela `md_cor_expedicao_solicitad`**
  - **Colunas**
    - **Nova `sin_devolvido`**: texto fixo de 1 caractere, nula; registros existentes preenchidos com `N`.
    - **Nova `justificativa_devolucao`**: texto variável de até 250 caracteres, nula.
- **Tabela `md_cor_lista_status`**
  - **Colunas**
    - **Nova `sta_rastreio_modulo`**: texto variável de 1 caractere, nula.

### Excluído

- **Tabela `md_cor_expedicao_solicitad`**
  - **Colunas**
    - **Excluída `observacao`**
- **Tabela `md_cor_lista_status`**
  - **Colunas**
    - **Excluída `nome_imagem`**

## [1.0.0]

### Adicionado

- **Tabela `md_cor_adm_par_ar_infrigen`**
- **Tabela `md_cor_adm_parametro_ar`**
- **Tabela `md_cor_ar_cobranca`**
- **Tabela `md_cor_contato`**
- **Tabela `md_cor_contrato`**
- **Tabela `md_cor_diretoria`**
- **Tabela `md_cor_expedicao_andamento`**
- **Tabela `md_cor_expedicao_formato`**
- **Tabela `md_cor_expedicao_solicitad`**
- **Tabela `md_cor_extensao_midia`**
- **Tabela `md_cor_justificativa`**
- **Tabela `md_cor_lista_status`**
- **Tabela `md_cor_map_unid_servico`**
- **Tabela `md_cor_map_unidade_exp`**
- **Tabela `md_cor_objeto`**
- **Tabela `md_cor_parametro_rastreio`**
- **Tabela `md_cor_plp`**
- **Tabela `md_cor_retorno_ar`**
- **Tabela `md_cor_retorno_ar_doc`**
- **Tabela `md_cor_serie_exp`**
- **Tabela `md_cor_servico_postal`**
- **Tabela `md_cor_status_process`**
- **Tabela `md_cor_substatus_process`**
- **Tabela `md_cor_tipo_correspondenc`**
- **Tabela `md_cor_tipo_objeto`**
- **Tabela `md_cor_unidade_exp`**
- **Tabela `rel_contato_justificativa`**
