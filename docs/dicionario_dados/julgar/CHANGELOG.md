# Changelog do Módulo SEI Julgar

## [3.0.0]

### Alterado

- **Tabela `voto_parte`**
  - **Colunas**
    - **Nova `id_usuario_lancamento`**: adicionada como número, aceitando valor nulo.
    - **Nova `sin_ativo`**: adicionada como texto fixo de 1 caractere, preenchida com `S` e finalizada como `NOT NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_usuario_lancam_voto_parte`**
- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Nova `sta_modalidade_virtual`**: adicionada como texto fixo de 1 caractere, preenchida e finalizada como `NOT NULL`.

## [2.1.0]

### Alterado

- **Tabela `presenca_sessao`**
  - **Colunas**
    - **Nova `sta_modalidade`**: adicionada como texto fixo de 1 caractere, preenchida com `N` e finalizada como `NOT NULL`.
- **Tabela `bloqueio_item_sess_unidade`**
  - **Colunas**
    - **Alterada `id_unidade`**: `NOT NULL` para `NULL`.
- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Nova `link_reuniao`**: adicionada como texto variável de 1000 caracteres, aceitando valor nulo.
    - **Nova `obs_link`**: adicionada como texto variável de 4000 caracteres, aceitando valor nulo.
- **Tabela `voto_parte`**
  - **Colunas**
    - **Alterada `ressalva`**: texto variável de 1000 caracteres, aceitando valor nulo, para texto grande, aceitando valor nulo.

## [2.0.0]

### Adicionado

- **Tabela `seq_tipo_sessao`**
- **Tabela `seq_sessao_bloco`**
- **Tabela `seq_tipo_sessao_bloco`**
- **Tabela `tipo_sessao`**
- **Tabela `sessao_bloco`**
- **Tabela `tipo_sessao_bloco`**

### Alterado

- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Nova `id_tipo_sessao`**: adicionada como número, aceitando valor nulo.
  - **Chaves estrangeiras**
    - **Nova `fk_sessao_julg_tipo_sessao`**
- **Tabela `item_sessao_julgamento`**
  - **Colunas**
    - **Nova `id_sessao_bloco`**: adicionada como número, aceitando valor nulo, preenchida na carga e finalizada como `NOT NULL`.

### Excluído

- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Excluída `sta_tipo`**
- **Tabela `item_sessao_julgamento`**
  - **Colunas**
    - **Excluída `sta_item_sessao_julgamento`**

## [1.4.0]

### Adicionado

- **Tabela `seq_eleicao`**
- **Tabela `seq_opcao_eleicao`**
- **Tabela `seq_voto_eleicao`**
- **Tabela `seq_voto_opcao_eleicao`**
- **Tabela `rel_autuacao_tipo_materia`**
- **Tabela `eleicao`**
- **Tabela `opcao_eleicao`**
- **Tabela `voto_eleicao`**
- **Tabela `voto_opcao_eleicao`**

### Alterado

- **Tabela `autuacao`**
  - **Colunas**
    - **Nova `idx_autuacao`**: adicionada como texto variável de 4000 caracteres, aceitando valor nulo.
- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Nova `id_documento_pauta`**: adicionada como número grande, aceitando valor nulo.
  - **Chaves estrangeiras**
    - **Nova `fk_sessao_julgamento_doc_pauta`**
- **Tabela `atributo_andamento_sessao`**
  - **Colunas**
    - **Alterada `valor`**: texto variável de 250 caracteres, aceitando valor nulo, para texto variável de 4000 caracteres, aceitando valor nulo.
- **Tabela `provimento`**
  - **Colunas**
    - **Nova `sin_ativo`**: adicionada como texto fixo de 1 caractere, preenchida com `S` e finalizada como `NOT NULL`.

## [1.3.0]

### Adicionado

- **Tabela `seq_bloqueio_item_sess_unidade`**
- **Tabela `seq_revisao_item`**
- **Tabela `bloqueio_item_sess_unidade`**
- **Tabela `revisao_item`**

### Alterado

- **Tabela `colegiado`**
  - **Colunas**
    - **Nova `artigo`**: adicionada como texto fixo de 1 caractere, aceitando valor nulo.
- **Tabela `destaque`**
  - **Colunas**
    - **Alterada `descricao`**: texto variável de 4000 caracteres, aceitando valor nulo, para texto grande, aceitando valor nulo.
- **Tabela `andamento_sessao`**
  - **Colunas**
    - **Alterada `id_unidade`**: `NULL` para `NOT NULL`.

## [1.2.0]

### Adicionado

- **Tabela `rel_motivo_distr_colegiado`**

### Alterado

- **Tabela `colegiado_composicao`**
  - **Colunas**
    - **Nova `sin_habilitado`**: adicionada como texto fixo de 1 caractere, preenchida na carga e finalizada como `NOT NULL`.
- **Tabela `julgamento_parte`**
  - **Colunas**
    - **Nova `ordem`**: adicionada como número, aceitando valor nulo, preenchida na carga e finalizada como `NOT NULL`.
    - **Alterada `descricao`**: texto variável de 100 caracteres, `NOT NULL`, para texto variável de 4000 caracteres, `NOT NULL`.
- **Tabela `autuacao`**
  - **Colunas**
    - **Alterada `descricao`**: texto variável de 1000 caracteres, aceitando valor nulo, para texto variável de 2000 caracteres, aceitando valor nulo.

### Excluído

- **Tabela `motivo_distribuicao`**
  - **Colunas**
    - **Excluída `id_colegiado`**
  - **Chaves estrangeiras**
    - **Excluída `fk_motivo_distrib_colegiado`**
  - **Índices**
    - **Excluído `fk_motivo_distrib_colegiado`**

## [1.1.0]

### Adicionado

- **Tabela `seq_autuacao`**
- **Tabela `autuacao`**

### Alterado

- **Tabela `destaque`**
  - **Colunas**
    - **Nova `sta_acesso`**: adicionada como texto fixo de 1 caractere, preenchida a partir de `sta_tipo` e finalizada como `NOT NULL`.
    - **Alterada `descricao`**: `NOT NULL` para `NULL`.
    - **Alterada `sta_tipo`**: `NOT NULL` para `NULL`.

### Excluído

- **Tabela `rel_proced_tipo_materia`**
- **Tabela `item_sessao_julgamento`**
  - **Colunas**
    - **Excluída `provimento`**
- **Tabela `voto_parte`**
  - **Colunas**
    - **Excluída `id_documento`**
  - **Chaves estrangeiras**
    - **Excluída `fk_voto_parte_documento`**
  - **Índices**
    - **Excluído `fk_voto_parte_documento`**

## [1.0.0]

### Adicionado

- **Tabela `algoritmo`**
- **Tabela `andamento_sessao`**
- **Tabela `ausencia_sessao`**
- **Tabela `atributo_andamento_sessao`**
- **Tabela `colegiado`**
- **Tabela `colegiado_composicao`**
- **Tabela `colegiado_versao`**
- **Tabela `destaque`**
- **Tabela `distribuicao`**
- **Tabela `impedimento`**
- **Tabela `item_sessao_documento`**
- **Tabela `item_sessao_julgamento`**
- **Tabela `julgamento_parte`**
- **Tabela `motivo_ausencia`**
- **Tabela `motivo_canc_distribuicao`**
- **Tabela `motivo_distribuicao`**
- **Tabela `motivo_mesa`**
- **Tabela `parte_procedimento`**
- **Tabela `pedido_vista`**
- **Tabela `presenca_sessao`**
- **Tabela `provimento`**
- **Tabela `qualificacao_parte`**
- **Tabela `rel_colegiado_usuario`**
- **Tabela `rel_destaque_usuario`**
- **Tabela `rel_proced_tipo_materia`**
- **Tabela `sessao_julgamento`**
- **Tabela `sustentacao_oral`**
- **Tabela `tarefa_sessao`**
- **Tabela `tipo_materia`**
- **Tabela `tipo_membro_colegiado`**
- **Tabela `voto_parte`**
- **Tabela `seq_algoritmo`**
- **Tabela `seq_andamento_sessao`**
- **Tabela `seq_atributo_andamento_sessao`**
- **Tabela `seq_ausencia_sessao`**
- **Tabela `seq_colegiado`**
- **Tabela `seq_colegiado_composicao`**
- **Tabela `seq_colegiado_versao`**
- **Tabela `seq_destaque`**
- **Tabela `seq_distribuicao`**
- **Tabela `seq_impedimento`**
- **Tabela `seq_item_sessao_documento`**
- **Tabela `seq_item_sessao_julgamento`**
- **Tabela `seq_julgamento_item`**
- **Tabela `seq_julgamento_parte`**
- **Tabela `seq_motivo_ausencia`**
- **Tabela `seq_motivo_canc_distribuicao`**
- **Tabela `seq_motivo_distribuicao`**
- **Tabela `seq_motivo_mesa`**
- **Tabela `seq_parte_procedimento`**
- **Tabela `seq_pedido_vista`**
- **Tabela `seq_presenca_sessao`**
- **Tabela `seq_provimento`**
- **Tabela `seq_qualificacao_parte`**
- **Tabela `seq_sessao_julgamento`**
- **Tabela `seq_sustentacao_oral`**
- **Tabela `seq_tarefa_sessao`**
- **Tabela `seq_tipo_materia`**
- **Tabela `seq_voto_parte`**
