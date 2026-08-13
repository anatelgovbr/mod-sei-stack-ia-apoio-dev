# Changelog do Módulo SEI Julgar

## [3.0.0]

### Alterado

- **Tabela `voto_parte`**
  - **Colunas**
    - **Nova `id_usuario_lancamento`**: adicionada como `tipoNumero() NULL`.
    - **Nova `sin_ativo`**: adicionada como `tipoTextoFixo(1) NULL`, preenchida com `S` e finalizada como `tipoTextoFixo(1) NOT NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_usuario_lancam_voto_parte`**: `id_usuario_lancamento` → `usuario.id_usuario`.
  - **Índices**
    - **Novo `fk_usuario_lancam_voto_parte`**: criado sobre `id_usuario_lancamento`.
- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Nova `sta_modalidade_virtual`**: adicionada como `tipoTextoFixo(1) NULL`, preenchida com `N` ou `D` conforme o tipo de sessão e finalizada como `tipoTextoFixo(1) NOT NULL`.

## [2.1.0]

### Alterado

- **Tabela `presenca_sessao`**
  - **Colunas**
    - **Nova `sta_modalidade`**: adicionada como `tipoTextoFixo(1) NULL`, preenchida com `N` e finalizada como `tipoTextoFixo(1) NOT NULL`.
- **Tabela `bloqueio_item_sess_unidade`**
  - **Colunas**
    - **Alterada `id_unidade`**: `tipoNumero() NOT NULL` para `tipoNumero() NULL`.
- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Nova `link_reuniao`**: adicionada como `tipoTextoVariavel(1000) NULL`.
    - **Nova `obs_link`**: adicionada como `tipoTextoVariavel(4000) NULL`.
- **Tabela `voto_parte`**
  - **Colunas**
    - **Alterada `ressalva`**: `tipoTextoVariavel(1000) NULL` para `tipoTextoGrande() NULL`.

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
    - **Nova `id_tipo_sessao`**: adicionada como `tipoNumero() NULL` e preenchida conforme `sta_tipo`.
  - **Chaves estrangeiras**
    - **Nova `fk_sessao_julg_tipo_sessao`**: `id_tipo_sessao` → `tipo_sessao.id_tipo_sessao`.
  - **Índices**
    - **Novo `fk_sessao_julg_tipo_sessao`**: criado sobre `id_tipo_sessao`.
- **Tabela `item_sessao_julgamento`**
  - **Colunas**
    - **Nova `id_sessao_bloco`**: adicionada como `tipoNumero() NULL`, preenchida na carga e finalizada como `tipoNumero() NOT NULL`.

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
    - **Nova `idx_autuacao`**: adicionada como `tipoTextoVariavel(4000) NULL`.
- **Tabela `sessao_julgamento`**
  - **Colunas**
    - **Nova `id_documento_pauta`**: adicionada como `tipoNumeroGrande() NULL`.
  - **Chaves estrangeiras**
    - **Nova `fk_sessao_julgamento_doc_pauta`**: `id_documento_pauta` → `documento.id_documento`.
  - **Índices**
    - **Novo `fk_sessao_julgamento_doc_pauta`**: criado sobre `id_documento_pauta`.
- **Tabela `atributo_andamento_sessao`**
  - **Colunas**
    - **Alterada `valor`**: `tipoTextoVariavel(250) NULL` para `tipoTextoVariavel(4000) NULL`.
- **Tabela `provimento`**
  - **Colunas**
    - **Nova `sin_ativo`**: adicionada como `tipoTextoFixo(1) NULL`, preenchida com `S` e finalizada como `tipoTextoFixo(1) NOT NULL`.

## [1.3.0]

### Adicionado

- **Tabela `seq_bloqueio_item_sess_unidade`**
- **Tabela `seq_revisao_item`**
- **Tabela `bloqueio_item_sess_unidade`**
- **Tabela `revisao_item`**

### Alterado

- **Tabela `colegiado`**
  - **Colunas**
    - **Nova `artigo`**: adicionada como `tipoTextoFixo(1) NULL`.
- **Tabela `destaque`**
  - **Colunas**
    - **Alterada `descricao`**: `tipoTextoVariavel(4000) NOT NULL` para `tipoTextoGrande() NULL`.
- **Tabela `andamento_sessao`**
  - **Colunas**
    - **Alterada `id_unidade`**: `tipoNumero() NULL` para `tipoNumero() NOT NULL`.
  - **Índices**
    - **Novo `fk_andamento_sessao_unidade`**: recriado sobre `id_unidade` nos SGBDs aplicáveis.

### Excluído

- **Tabela `andamento_sessao`**
  - **Índices**
    - **Excluído `fk_andamento_sessao_unidade`**: removido antes da alteração da coluna, quando encontrado.
    - **Excluído `if_andamento_sessao_unidade`**: removido antes da alteração da coluna, quando encontrado.

## [1.2.0]

### Adicionado

- **Tabela `rel_motivo_distr_colegiado`**

### Alterado

- **Tabela `colegiado_composicao`**
  - **Colunas**
    - **Nova `sin_habilitado`**: adicionada como `char(1) NULL`, preenchida com `N` ou `S` e finalizada como `char(1) NOT NULL`.
- **Tabela `julgamento_parte`**
  - **Colunas**
    - **Nova `ordem`**: adicionada como `int NULL`, preenchida na carga e finalizada como `int NOT NULL`.
    - **Alterada `descricao`**: `tipoTextoVariavel(100) NOT NULL` para `tipoTextoVariavel(4000) NOT NULL`.
- **Tabela `autuacao`**
  - **Colunas**
    - **Alterada `descricao`**: `tipoTextoVariavel(1000) NULL` para `tipoTextoVariavel(2000) NULL`.

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
    - **Nova `sta_acesso`**: adicionada como `tipoTextoFixo(1) NULL`, preenchida a partir de `sta_tipo` e finalizada como `tipoTextoFixo(1) NOT NULL`.
    - **Alterada `descricao`**: `tipoTextoVariavel(4000) NOT NULL` para `tipoTextoVariavel(4000) NULL`.
    - **Alterada `sta_tipo`**: `tipoTextoFixo(1) NOT NULL` para `tipoTextoFixo(1) NULL`.

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

### Alterado

- **Tabela `seq_tarefa`**
  - **Propriedades da tabela**
    - **Alterada `sequência nativa`**: recriada no MySQL com valor inicial calculado a partir do maior identificador de tarefa; quando não há tarefa, inicia em `1`, quando o maior identificador é até `1000`, inicia em `1001`, e nos demais casos inicia no maior identificador acrescido de `1`.
