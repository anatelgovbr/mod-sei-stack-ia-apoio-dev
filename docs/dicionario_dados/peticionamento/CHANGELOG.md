# Changelog do Módulo SEI Peticionamento e Intimação Eletrônicos

## [4.6.0]

### Adicionado

- **Tabela `md_pet_adm_pro_repres_whit`**

### Alterado

- **Tabela `md_pet_vinculo`**
  - **Colunas**
    - **Alterada `id_procedimento`**: recriada no PostgreSQL como `tipoNumeroGrande() NULL`, com cópia dos dados da coluna anterior.

### Excluído

- **Tabela `md_pet_rel_cont_sit_rf`** (se existente)

## [4.3.0]

### Adicionado

- **Tabela `md_pet_prz_tac_rel_tp_proc`**

### Alterado

- **Tabela `md_pet_adm_integracao`**
  - **Colunas**
    - **Alterada `endereco_wsdl`**: recriada no Oracle e no PostgreSQL como `tipoTextoVariavel(250) NULL`, com cópia dos dados da coluna anterior; nos demais SGBDs, alterada para a mesma definição.
- **Tabela `md_pet_int_prazo_tacita`**
  - **Colunas**
    - **Nova `sta_tipo_prazo`**: adicionada como `tipoTextoFixo(1) NOT NULL`, após preenchimento dos registros existentes com `G`.
- **Tabela `md_pet_tipo_processo`**
  - **Colunas**
    - **Nova `sin_doc_formulario`**: adicionada como `tipoTextoFixo(1) NULL`, com preenchimento dos registros existentes com `N`.
    - **Nova `id_tipo_formulario`**: adicionada como `tipoNumero(1) NULL`.
- **Tabela `md_pet_vinculo`**
  - **Colunas**
    - **Nova `dth_ultima_consulta_rfb`**: adicionada como `tipoDataHora() NULL`.
- **Tabela `md_pet_int_rel_dest`**
  - **Colunas**
    - **Nova `dta_prazo_tacito`**: adicionada como `tipoDataHora() NULL`.
- **Tabela `md_pet_adm_integ_param`**
  - **Colunas**
    - **Alterada `nome_campo`**: recriada no PostgreSQL de `tipoTextoVariavel(500) NULL` para `tipoTextoVariavel(250) NULL`, com cópia dos dados da coluna anterior.
- **Tabela `md_pet_adm_vinc_tp_proced`**
  - **Colunas**
    - **Alterada `sin_na_usuario_externo`**: recriada no PostgreSQL de `tipoTextoFixo(1) NULL` para `tipoTextoVariavel(250) NULL`, com cópia dos dados da coluna anterior.
    - **Alterada `sin_na_padrao`**: recriada no PostgreSQL de `tipoTextoFixo(1) NULL` para `tipoTextoVariavel(250) NULL`, com cópia dos dados da coluna anterior.

### Excluído

- **Tabela `md_pet_fila_consulta_rf`**

## [4.2.0]

### Alterado

- **Tabela `md_pet_tp_processo_orientacoes`**
  - **Colunas**
    - **Nova `sin_ativo_menu_ext`**: adicionada como `tipoTextoFixo(1) NOT NULL`, após preenchimento dos registros existentes com `S`.

## [4.1.0]

### Adicionado

- **Tabela `md_pet_adm_nivel_aces_doc`**
- **Tabela `md_pet_fila_consulta_rf`**
- **Tabela `md_pet_rel_cont_sit_rf`**

### Alterado

- **Tabela `md_pet_adm_integracao`**
  - **Colunas**
    - **Nova `cod_receita_suspensao_auto`**: adicionada como `tipoTextoVariavel(30) NULL`.
    - **Alterada `endereco_wsdl`**: de `tipoTextoVariavel(100) NULL` para `tipoTextoVariavel(250) NULL`.
- **Tabela `md_pet_vinculo`**
  - **Colunas**
    - **Alterada `id_procedimento`**: de `tipoNumeroGrande() NOT NULL` para `tipoNumeroGrande() NULL`.
- **Tabela `md_pet_criterio`**
  - **Colunas**
    - **Nova `sin_intercorrente_sigiloso`**: adicionada como `tipoTextoFixo(1) NOT NULL`, após preenchimento dos registros existentes com `S`.

### Excluído

- **Tabela `md_pet_int_prot_disponivel`**
  - **Chaves estrangeiras**
    - **Excluída `fk1_md_pet_int_prot_disponivel`**: sobre `id_protocolo`.
  - **Índices**
    - **Excluído `fk1_md_pet_int_prot_disponivel`**
- **Tabela `md_pet_vinculo_represent`**
  - **Colunas**
    - **Excluída `sin_ativo`**

## [4.0.2]

### Alterado

- **Tabela `md_pet_tipo_processo`**
  - **Colunas**
    - **Alterada `orientacoes`**: de `tipoTextoVariavel(500) NOT NULL` para `tipoTextoVariavel(1000) NOT NULL`.

## [3.3.0]

### Alterado

- **Tabela `md_pet_adm_integ_param`**
  - **Colunas**
    - **Alterada `nome_campo`**: de `tipoTextoVariavel(50) NULL` para `tipoTextoVariavel(500) NULL`.

## [3.1.0]

### Adicionado

- **Tabela `md_pet_adm_tipo_poder`**
- **Tabela `md_pet_rel_vincrep_tipo_poder`**
- **Tabela `md_pet_rel_vincrep_protoc`**

### Alterado

- **Tabela `md_pet_vinculo_represent`**
  - **Colunas**
    - **Nova `sta_abrangencia`**: adicionada como `tipoTextoFixo(1) NULL`.
    - **Nova `data_limite`**: adicionada como `tipoDataHora() NULL`.
- **Tabela `md_pet_adm_vinc_tp_proced`**
  - **Colunas**
    - **Nova `especificacao`**: adicionada como `tipoTextoVariavel(100) NULL`.
    - **Nova `tipo_vinculo`**: adicionada como `tipoTextoFixo(1) NULL`.
    - **Alterada `sin_na_usuario_externo`**: de `tipoTextoFixo(1) NOT NULL` para `tipoTextoFixo(1) NULL`.
    - **Alterada `sin_na_padrao`**: de `tipoTextoFixo(1) NOT NULL` para `tipoTextoFixo(1) NULL`.
    - **Alterada `sin_ativo`**: de `tipoTextoFixo(1) NOT NULL` para `tipoTextoFixo(1) NULL`.
- **Tabela `md_pet_adm_integracao`**
  - **Colunas**
    - **Nova `sta_tp_cliente_ws`**: adicionada como `tipoTextoFixo(1) NULL`.
    - **Nova `nu_versao`**: adicionada como `tipoNumeroDecimal(2, 1) NULL`.
    - **Nova `sin_tp_lougradouro`**: adicionada como `tipoTextoFixo(1) NULL`.
    - **Nova `sin_nu_lougradouro`**: adicionada como `tipoTextoFixo(1) NULL`.
    - **Nova `sin_comp_lougradouro`**: adicionada como `tipoTextoFixo(1) NULL`.

## [3.0.0]

### Adicionado

- **Tabela `md_pet_adm_integ_funcion`**
- **Tabela `md_pet_adm_integracao`**
- **Tabela `md_pet_adm_integ_param`**
- **Tabela `md_pet_adm_vinc_tp_proced`**
- **Tabela `md_pet_adm_vinc_rel_serie`**
- **Tabela `md_pet_vinculo`**
- **Tabela `md_pet_vinculo_represent`**
- **Tabela `md_pet_vinculo_documento`**
- **Tabela `md_pet_int_tp_int_orient`**
- **Tabela `md_pet_rel_int_dest_extern`**

### Alterado

- **Tabela `md_pet_acesso_externo`**
  - **Colunas**
    - **Nova `sin_vinculo`**: adicionada como `tipoTextoFixo(1) NOT NULL`, após preenchimento dos valores nulos com `N`.
- **Tabela `md_pet_int_aceite`**
  - **Colunas**
    - **Nova `id_usuario`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_md_pet_int_aceite_doc3`**: em `id_usuario`, referenciando `usuario.id_usuario`.
  - **Índices**
    - **Novo `fk_md_pet_int_aceite_doc3`**
- **Tabela `md_pet_int_dest_resposta`**
  - **Colunas**
    - **Nova `id_usuario`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk3_md_pet_int_dest_resp_usu`**: em `id_usuario`, referenciando `usuario.id_usuario`.
  - **Índices**
    - **Novo `fk3_md_pet_int_dest_resp_usu`**

### Excluído

- **Tabela `md_pet_int_rel_dest`**
  - **Colunas**
    - **Excluída `id_acesso_externo`**
  - **Chaves estrangeiras**
    - **Excluída `fk3_md_pet_int_rel_dest`**: sobre `id_acesso_externo` no MySQL, SQL Server e Oracle.
  - **Índices**
    - **Excluído `fk3_md_pet_int_rel_dest`**: sobre o índice `fk3_md_pet_int_rel_dest` no MySQL e SQL Server.

## [2.0.2]

### Adicionado

- **Tabela `md_pet_indisp_doc`** (somente se ausente)

### Excluído

- **Tabela `md_pet_indisp_anexo`** (se existente)
- **Tabela `md_pet_rel_recibo_protoc`**
  - **Colunas**
    - **Excluída `nome_tipo_intimacao`**: se existente.
    - **Excluída `nome_tipo_resposta`**: se existente.
- **Tabela `md_pet_usu_ext_processo`** (se existente)

## [2.0.0]

### Adicionado

- **Tabela `md_pet_int_prazo_tacita`**
- **Tabela `md_pet_int_tipo_intimacao`**
- **Tabela `md_pet_int_tipo_resp`**
- **Tabela `md_pet_int_rel_intim_resp`**
- **Tabela `md_pet_int_serie`**
- **Tabela `md_pet_acesso_externo`**
- **Tabela `md_pet_intimacao`**
- **Tabela `md_pet_int_rel_tipo_resp`**
- **Tabela `md_pet_int_rel_dest`**
- **Tabela `md_pet_int_protocolo`**
- **Tabela `md_pet_int_prot_disponivel`**
- **Tabela `md_pet_int_dest_resposta`**
- **Tabela `md_pet_int_rel_resp_doc`**
- **Tabela `md_pet_int_aceite`**
- **Tabela `md_pet_int_rel_tpo_res_des`**

### Alterado

- **Tabela `md_pet_rel_recibo_protoc`**
  - **Colunas**
    - **Nova `txt_doc_principal_intimacao`**: adicionada como `tipoTextoVariavel(250) NULL`.

## [1.1.0]

### Adicionado

- **Tabela `md_pet_criterio`**

### Alterado

- **Tabela `md_pet_rel_recibo_protoc`**
  - **Colunas**
    - **Nova `id_protocolo_relacionado`**: adicionada como `tipoNumeroGrande() NULL` somente quando ausente em instalações legadas; a coluna já integra o `CREATE TABLE` da versão 0.0.2.
    - **Nova `id_documento`**: adicionada como `tipoNumeroGrande() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk5_md_pet_rel_recibo_protoc`**: em `id_protocolo_relacionado`, referenciando `protocolo.id_protocolo`, somente no reparo condicional.
    - **Nova `fk6_md_pet_rel_recibo_protoc`**: em `id_documento`, referenciando `documento.id_documento`.
  - **Índices**
    - **Novo `fk5_md_pet_rel_recibo_protoc`**: somente no reparo condicional.
    - **Novo `fk6_md_pet_rel_recibo_protoc`**

## [1.0.4]

### Alterado

- **Tabela `md_pet_rel_tp_ctx_contato`**
  - **Colunas**
    - **Nova `id_tipo_contato`**: adicionada como `tipoNumero() NOT NULL`, com cópia dos dados de `id_tipo_contexto_contato`, somente quando ausente.

### Excluído

- **Tabela `md_pet_rel_tp_ctx_contato`**
  - **Colunas**
    - **Excluída `id_tipo_contexto_contato`**: removida após a cópia dos dados, na mesma migração condicional.

## [1.0.0]

### Adicionado

- **Tabela `md_pet_hipotese_legal`**
- **Tabela `md_pet_rel_tp_processo_unid`**
- **Tabela `md_pet_rel_tp_proc_serie`** (recriada em substituição a `md_pet_rel_tp_processo_serie`, com nova chave primária simples e inclusão de identificador sequencial e classificação do tipo de documento)

### Excluído

- **Tabela `md_pet_tipo_processo`**
  - **Colunas**
    - **Excluída `id_unidade`**
  - **Chaves estrangeiras**
    - **Excluída `fk_pet_tp_proc_unidade_02`**: sobre `id_unidade`.
  - **Índices**
    - **Excluído `fk_pet_tp_proc_unidade_02`**
- **Tabela `md_pet_rel_tp_processo_serie`**

## [0.0.2]

### Adicionado

- **Tabela `md_pet_usu_externo_menu`**
- **Tabela `md_pet_rel_tp_ctx_contato`**
- **Tabela `md_pet_rel_recibo_protoc`**
- **Tabela `md_pet_rel_recibo_docanexo`**

## [0.0.1]

### Adicionado

- **Tabela `md_pet_tipo_processo`**
- **Tabela `md_pet_rel_tp_processo_serie`**
- **Tabela `md_pet_tp_processo_orientacoes`**
- **Tabela `md_pet_ext_arquivo_perm`**
- **Tabela `md_pet_tamanho_arquivo`**
- **Tabela `md_pet_indisponibilidade`**
- **Tabela `md_pet_indisp_doc`**
