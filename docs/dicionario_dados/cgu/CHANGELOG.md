# Changelog do Módulo de Integração entre o sistema SEI e o FalaBR

## [4.1.0]

### Alterado

- **Tabela `md_eouv_depara_importacao`**
  - **Colunas**
    - **Nova `sin_ativo`**: adicionada como `tipoTextoFixo(1) NULL` e finalizada como `tipoTextoFixo(1) NOT NULL`.

### Excluído

- **Tabela `md_eouv_parametros`**
  - **Colunas**
    - **Excluída `de_tipo`**
- **Tabela `md_eouv_rel_import`**
  - **Colunas**
    - **Excluída `tip_manifestacao`**
- **Tabela `md_eouv_rel_import_det`**
  - **Colunas**
    - **Excluída `dth_importacao`**
    - **Excluída `dth_prazo_atendimento`**

## [4.0.2]

### Alterado

- **Tabela `md_eouv_parametros`**
  - **Colunas**
    - **Alterada `de_valor_parametro`**: tipo: `tipoTextoVariavel(455)` para `tipoTextoGrande()`.

## [4.0.0]

### Alterado

- **Tabela `md_eouv_parametros`**
  - **Colunas**
    - **Nova `de_tipo`**: adicionada como `tipoTextoVariavel(10) NULL` e finalizada como `tipoTextoVariavel(10) NOT NULL`.
- **Tabela `md_eouv_rel_import`**
  - **Colunas**
    - **Nova `tip_manifestacao`**: adicionada como `tipoTextoFixo(2) NULL` e finalizada como `tipoTextoFixo(2) NOT NULL`.
- **Tabela `md_eouv_rel_import_det`**
  - **Colunas**
    - **Nova `dth_prazo_atendimento`**: adicionada como `tipoDataHora() NULL`.
    - **Nova `tip_manifestacao`**: adicionada como `tipoTextoFixo(2) NULL` e finalizada como `tipoTextoFixo(2) NOT NULL`.

## [3.0.0]

### Adicionado

- **Tabela `md_eouv_parametros`**

## [2.0.5]

### Adicionado

- **Tabela `md_eouv_depara_importacao`**
- **Tabela `md_eouv_rel_import`**
- **Tabela `md_eouv_rel_import_det`**
- **Tabela `seq_md_eouv_rel_import`**
