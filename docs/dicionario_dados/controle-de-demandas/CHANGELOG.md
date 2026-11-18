# Changelog do Módulo SEI Controle de Demandas

## [3.0.0]

### Observações

As tabelas abaixo permanecem no banco na versão 3.0.0, mas são legadas: nenhuma tela do módulo grava nelas, e a migração para a 3.0.0 transfere o conteúdo delas para o modelo novo. A remoção física está prevista para a versão 3.1.0.

- **Tabela `md_ri_crit_cad`**
- **Tabela `md_ri_rel_cad_cidade`**
- **Tabela `md_ri_rel_cad_localidade`**
- **Tabela `md_ri_rel_cad_uf`**
- **Tabela `md_ri_rel_crit_cad_cont`**
- **Tabela `md_ri_rel_crit_cad_proc`**
- **Tabela `md_ri_rel_crit_cad_serie`**
- **Tabela `md_ri_rel_crit_cad_unid`**

Os DTOs abaixo ainda mapeiam as tabelas legadas e continuam no módulo, cada um com as classes de regra de negócio (RN) e de acesso ao banco (BD) correspondentes. Eles precisam sair junto com as tabelas:

- `MdRiCriterioCadastroDTO`: `md_ri_crit_cad`
- `MdRiRelCadastroCidadeDTO`: `md_ri_rel_cad_cidade`
- `MdRiRelCadastroLocalidadeDTO`: `md_ri_rel_cad_localidade`
- `MdRiRelCadastroUfDTO`: `md_ri_rel_cad_uf`
- `MdRiRelCriterioCadastroTipoContatoDTO`: `md_ri_rel_crit_cad_cont`
- `MdRiRelCriterioCadastroTipoProcessoDTO`: `md_ri_rel_crit_cad_proc`
- `MdRiRelCriterioCadastroSerieDTO`: `md_ri_rel_crit_cad_serie`
- `MdRiRelCriterioCadastroUnidadeDTO`: `md_ri_rel_crit_cad_unid`

Leituras que ainda dependem das tabelas legadas:

- `md_ri_rel_crit_cad_cont` ainda é lida na seleção de contatos sem Grupo de Parametrização e na montagem da lista de tipos de contato.
- `md_ri_rel_crit_cad_unid` ainda é lida na seleção e no autocompletar de unidades e impede desativar ou excluir uma unidade vinculada a critério.
- `md_ri_crit_cad`, `md_ri_rel_crit_cad_proc` e `md_ri_rel_crit_cad_serie` só aparecem na gravação de critérios, que nenhuma tela aciona desde a versão 3.0.0.
- `md_ri_rel_cad_uf`, `md_ri_rel_cad_cidade` e `md_ri_rel_cad_localidade` só são lidas para apagar os vínculos antigos quando uma demanda é excluída.

Há ainda o DTO `MdRiRelTipoControleDemandaGrupoParamRegraDTO`, que aponta para a tabela `md_ri_rel_tp_ctrl_dmd_gp_param_regra`. Nenhum script de instalação cria essa tabela, e nenhuma classe usa esse DTO. Ele não corresponde a uma tabela do banco e também deve ser removido na versão 3.1.0.

### Adicionado

- **Tabela `md_ri_cad_info_add_reg`**
- **Tabela `md_ri_cad_info_add_val`**
- **Tabela `md_ri_cad_info_add_val_opc`**
- **Tabela `md_ri_ctrl_dem_situacao`**
- **Tabela `md_ri_ctrl_demanda`**
- **Tabela `md_ri_gp_param`**
- **Tabela `md_ri_gp_param_info_add_campo`**
- **Tabela `md_ri_gp_param_info_add_opcao`**
- **Tabela `md_ri_gp_param_regra`**
- **Tabela `md_ri_gp_param_regra_validacao`**
- **Tabela `md_ri_rel_cad_doc`**
- **Tabela `md_ri_rel_cad_local`**
- **Tabela `md_ri_rel_ctrl_dem_unid`**
- **Tabela `md_ri_rel_gp_param_iac_serie`**
- **Tabela `md_ri_rel_gp_param_proc`**
- **Tabela `md_ri_rel_gp_param_tema`**
- **Tabela `md_ri_rel_gp_regra_servico`**
- **Tabela `md_ri_rel_gp_regra_tp_cont`**
- **Tabela `md_ri_rel_gp_regra_tp_proc`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_cont`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_gestor`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_proc`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_serie`**
- **Tabela `md_ri_rel_tp_ctrl_dmd_unid`**
- **Tabela `md_ri_tipo_demanda`**
- **Tabela `md_ri_tp_ctrl_demanda`**
- **Tabela `seq_md_ri_cad_info_add_reg`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_cad_info_add_val`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_ctrl_demanda`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_ctrl_dem_situacao`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_gp_param`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_gp_param_iac`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_gp_param_iao`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_gp_param_regra`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_rel_cad_local`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_tipo_demanda`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_tp_ctrl_demanda`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)

### Alterado

- **Tabela `md_ri_cadastro`**
  - **Colunas**
    - **Nova `id_md_ri_gp_param`**: adicionada como `tipoNumero() NULL`.
    - **Nova `id_md_ri_tp_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
    - **Alterada `dta_prazo`**: nulidade: `tipoDataHora() NOT NULL` para `tipoDataHora() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_ri_cad_ctrl`**: em `id_md_ri_tp_ctrl_demanda`, referenciando `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
    - **Nova `fk_ri_cad_gp_param`**: em `id_md_ri_gp_param`, referenciando `md_ri_gp_param.id_md_ri_gp_param`.
- **Tabela `md_ri_classificacao_tema`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_ri_cltema_ctrl`**: em `id_md_ri_tp_ctrl_demanda`, referenciando `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_rel_cad_classif`**
  - **Colunas**
    - **Alterada `id_md_ri_subtema`**: nulidade: `tipoNumero() NOT NULL` para `tipoNumero() NULL`.
  - **Índices**
    - **Novo `i_md_ri_rel_cad_classif_cad`**: sobre `id_md_ri_cadastro`.
    - **Novo `uk_md_ri_rel_cad_classif`**: único, sobre `id_md_ri_cadastro`, `id_md_ri_classificacao_tema`, `id_md_ri_subtema`.
- **Tabela `md_ri_rel_reit_doc`**
  - **Colunas**
    - **Nova `id_md_ri_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
    - **Nova `sin_prazo_resposta`**: adicionada como `tipoTextoFixo(1) DEFAULT 'S' NOT NULL`.
    - **Alterada `dta_certa`**: nulidade: `tipoDataHora() NOT NULL` para `tipoDataHora() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_reit_doc_ctrl_dem`**: em `id_md_ri_ctrl_demanda`, referenciando `md_ri_ctrl_demanda.id_md_ri_ctrl_demanda`.
  - **Índices**
    - **Novo `i01_md_ri_rel_reit_ctrl_dem`**: sobre `id_md_ri_ctrl_demanda`.
- **Tabela `md_ri_resposta`**
  - **Colunas**
    - **Nova `id_md_ri_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_md_ri_resposta_ctrl_dem`**: em `id_md_ri_ctrl_demanda`, referenciando `md_ri_ctrl_demanda.id_md_ri_ctrl_demanda`.
  - **Índices**
    - **Novo `i01_md_ri_resposta_ctrl_dem`**: sobre `id_md_ri_ctrl_demanda`.
- **Tabela `md_ri_resposta_reiteracao`**
  - **Colunas**
    - **Nova `id_md_ri_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_md_ri_resp_reit_ctrl_dem`**: em `id_md_ri_ctrl_demanda`, referenciando `md_ri_ctrl_demanda.id_md_ri_ctrl_demanda`.
  - **Índices**
    - **Novo `i01_md_ri_resp_reit_ctrl_dem`**: sobre `id_md_ri_ctrl_demanda`.
- **Tabela `md_ri_subtema`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_ri_subt_ctrl`**: em `id_md_ri_tp_ctrl_demanda`, referenciando `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_tipo_controle`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_ri_tipo_demanda_tp_ctrl`**: em `id_md_ri_tp_ctrl_demanda`, referenciando `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_tipo_reiteracao`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_ri_reit_ctrl`**: em `id_md_ri_tp_ctrl_demanda`, referenciando `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.
- **Tabela `md_ri_tipo_resposta`**
  - **Colunas**
    - **Nova `id_md_ri_tp_ctrl_demanda`**: adicionada como `tipoNumero() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_ri_resp_ctrl`**: em `id_md_ri_tp_ctrl_demanda`, referenciando `md_ri_tp_ctrl_demanda.id_md_ri_tp_ctrl_demanda`.

### Excluído

- **Tabela `md_ri_rel_cad_classif`**
  - **Chaves primárias**
    - **Excluída `pk_md_ri_rel_cad_classif`**

## [1.0.0]

### Adicionado

- **Tabela `md_ri_cadastro`**
- **Tabela `md_ri_classificacao_tema`**
- **Tabela `md_ri_crit_cad`**
- **Tabela `md_ri_rel_cad_cidade`**
- **Tabela `md_ri_rel_cad_classif`**
- **Tabela `md_ri_rel_cad_contato`**
- **Tabela `md_ri_rel_cad_localidade`**
- **Tabela `md_ri_rel_cad_servico`**
- **Tabela `md_ri_rel_cad_tipo_prc`**
- **Tabela `md_ri_rel_cad_tp_ctrl`**
- **Tabela `md_ri_rel_cad_uf`**
- **Tabela `md_ri_rel_cad_unidade`**
- **Tabela `md_ri_rel_class_tema_subtema`**
- **Tabela `md_ri_rel_crit_cad_cont`**
- **Tabela `md_ri_rel_crit_cad_proc`**
- **Tabela `md_ri_rel_crit_cad_serie`**
- **Tabela `md_ri_rel_crit_cad_unid`**
- **Tabela `md_ri_rel_reit_doc`**
- **Tabela `md_ri_rel_reit_unid`**
- **Tabela `md_ri_resposta`**
- **Tabela `md_ri_resposta_reiteracao`**
- **Tabela `md_ri_servico`**
- **Tabela `md_ri_subtema`**
- **Tabela `md_ri_tipo_controle`**
- **Tabela `md_ri_tipo_processo`**
- **Tabela `md_ri_tipo_reiteracao`**
- **Tabela `md_ri_tipo_resposta`**
- **Tabela `seq_md_ri_cadastro`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_classificacao_tema`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_rel_reit_doc`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_rel_reit_unid`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_resposta`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_resposta_reiteracao`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_servico`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_subtema`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_tipo_controle`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_tipo_processo`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_tipo_reiteracao`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
- **Tabela `seq_md_ri_tipo_resposta`** (sequencial nativo: tabela no MySQL/SQL Server; sequência no PostgreSQL/Oracle)
