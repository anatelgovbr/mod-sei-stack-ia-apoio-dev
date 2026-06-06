# Padrão de código: scripts de instalação/upgrade SEI e SIP

Referência concreta para escrever métodos `instalarv*` nos scripts
`sei_atualizar_versao_modulo_*.php` e `sip_atualizar_versao_modulo_*.php`.

**Antes de escrever qualquer método:** ler os métodos existentes no script-alvo
para identificar padrões já em uso (nomes de variáveis, estilo de log, etc.).

---

## Guards obrigatórios

### Guard 1 — Não criar scripts novos se já existem

Consultar `.agents/references/mapa-modulos-scripts.md` antes de qualquer trabalho no módulo.

- Se o módulo constar no mapa: **nunca criar novos arquivos de script**. Apenas atualizar os scripts mapeados.
- Se o módulo **não** constar no mapa: verificar fisicamente em `sei/scripts/` e `sip/scripts/` antes de concluir que não existem. Nomes podem divergir do padrão convencional (ex.: `md_cgu_eouv_atualizar_modulo.php`).

### Guard 2 — Qualquer arquivo novo exige atualização de script

Qualquer novo arquivo `.php` adicionado a `modulos/<nome>/` em módulo com scripts mapeados **exige** atualização dos scripts de instalação nesta mesma entrega.

Exceções aceitas:
- Edição de arquivo existente sem criação de nova tabela ou recurso SIP.
- Arquivos de asset (`.css`, `.js`) sem ação nova vinculada.

---

## Estrutura geral de um método instalarv*

```php
protected function instalarv<XYZ>()
{
    $nmVersao = '<X.Y.Z>';
    $this->logar('EXECUTANDO A INSTALAÇÃO/ATUALIZAÇÃO DA VERSÃO '. $nmVersao .' DO ' . $this->nomeDesteModulo . ' NA BASE DO SEI'); // ou SIP

    // ... DDL, recursos, etc.

    $this->atualizarNumeroVersao($nmVersao);
}
```

O método `atualizarNumeroVersao` **sempre** é a última chamada.

---

## Script SEI — padrões de DDL

### Objeto obrigatório

```php
$objInfraMetaBD = new InfraMetaBD(BancoSEI::getInstance());
```

### Criar tabela

```php
$this->logar('CRIANDO A TABELA md_xx_entidade');
BancoSEI::getInstance()->executarSql('CREATE TABLE md_xx_entidade (
    id_md_xx_entidade ' . $objInfraMetaBD->tipoNumero() . ' NOT NULL,
    str_campo        ' . $objInfraMetaBD->tipoTextoVariavel(100) . ' NOT NULL,
    num_campo        ' . $objInfraMetaBD->tipoNumero() . ' NULL,
    din_campo        ' . $objInfraMetaBD->tipoNumeroDecimal(15,2) . ' NULL,
    dta_campo        ' . $objInfraMetaBD->tipoDataHora() . ' NULL,
    sin_ativo        ' . $objInfraMetaBD->tipoTextoFixo(1) . ' NOT NULL )');
```

Métodos de tipo disponíveis em `InfraMetaBD`:

| Método | Tipo SQL equivalente |
|--------|---------------------|
| `tipoNumero()` | `integer` / `number` |
| `tipoTextoVariavel(n)` | `varchar(n)` |
| `tipoTextoFixo(n)` | `char(n)` |
| `tipoNumeroDecimal(p,s)` | `numeric(p,s)` |
| `tipoDataHora()` | `datetime` / `timestamp` |

### Mapeamento do contrato JSON para InfraMetaBD

| Tipo no contrato | Método InfraMetaBD | Observação |
|---|---|---|
| `int`, `integer` | `tipoNumero()` | PKs e FKs |
| `varchar(N)` | `tipoTextoVariavel(N)` | N = tamanho declarado no contrato |
| `char(1)` | `tipoTextoFixo(1)` | Usado em `sin_ativo` e flags |
| `datetime` | `tipoDataHora()` | Data e hora |
| `numeric` | `tipoNumeroDecimal(p,s)` | Usar precisão e escala do contrato |

### Chave primária simples

```php
$objInfraMetaBD->adicionarChavePrimaria('md_xx_entidade', 'pk_md_xx_entidade',
    array('id_md_xx_entidade'));
```

### Chave primária composta (N:N)

```php
$objInfraMetaBD->adicionarChavePrimaria('md_xx_rel_a_b', 'pk_md_xx_rel_a_b',
    array('id_md_xx_a', 'id_md_xx_b'));
```

### Sequence / auto-incremento (multi-SGBD obrigatório)

Toda tabela funcional com PK gerada por sequence `seq_<tabela>` deve configurar o
DTO com `InfraDTO::$TIPO_PK_NATIVA`. O InfraPHP resolve o nome padrao por
`getStrNomeSequenciaNativa()` (`seq_` + `getStrNomeTabela()`).
Tabelas N:N com PK composta **não usam sequence**.

Nao usar `InfraDTO::$TIPO_PK_SEQUENCIAL` para sequences `seq_<tabela>`: esse tipo
consulta `infra_sequencia` usando o nome da tabela (`<tabela>`), sem prefixo `seq_`.

```php
$this->logar('CRIANDO A SEQUENCE seq_md_xx_entidade');
if (BancoSEI::getInstance() instanceof InfraMySql) {
    BancoSEI::getInstance()->executarSql('create table seq_md_xx_entidade (id bigint not null primary key AUTO_INCREMENT, campo char(1) null) AUTO_INCREMENT = 1');
} else if (BancoSEI::getInstance() instanceof InfraSqlServer) {
    BancoSEI::getInstance()->executarSql('create table seq_md_xx_entidade (id bigint identity(1,1), campo char(1) null)');
} else if (BancoSEI::getInstance() instanceof InfraOracle || BancoSEI::getInstance() instanceof InfraPostgreSql) {
    BancoSEI::getInstance()->criarSequencialNativa('seq_md_xx_entidade', 1);
}
```

### Chave estrangeira

```php
$objInfraMetaBD->adicionarChaveEstrangeira('fk_md_xx_rel_entpai', 'md_xx_entidade',
    array('id_md_xx_pai'), 'md_xx_pai', array('id_md_xx_pai'));
```

Assinatura: `adicionarChaveEstrangeira(nomeFk, tabelaFilha, colunasFilha[], tabelaPai, colunasPai[])`.
Nome da FK deve respeitar o limite de **30 caracteres**.

### Limites de nomenclatura (cross-SGBD)

- **Nomes de tabelas**: recomenda-se ≤ 26 caracteres para compatibilidade cross-SGBD
  (MySQL, PostgreSQL, Oracle, SQL Server). Oracle tem limite prático de 30 bytes,
  mas reservas do sistema podem reduzir o efetivo.
- **Nomes de FK**: limite absoluto de 30 caracteres (cross-SGBD).
- **Sequências**: `seq_` + nome da tabela ≤ 30 caracteres.

### Alterar tabela existente (upgrade incremental)

```php
$this->logar('ADICIONANDO COLUNA num_campo EM md_xx_entidade');
$objInfraMetaBD->adicionarColuna('md_xx_entidade', 'num_campo',
    $objInfraMetaBD->tipoNumero(), true); // true = nullable
```

---

## Script SIP — padrões de recursos e perfis

### Boilerplate obrigatório no início do método

```php
$objSistemaRN = new SistemaRN();
$objPerfilRN  = new PerfilRN();

$objSistemaDTO = new SistemaDTO();
$objSistemaDTO->retNumIdSistema();
$objSistemaDTO->setStrSigla('SEI');
$objSistemaDTO = $objSistemaRN->consultar($objSistemaDTO);
if ($objSistemaDTO == null) {
    throw new InfraException('Sistema SEI não encontrado.');
}
$numIdSistemaSei = $objSistemaDTO->getNumIdSistema();

$objPerfilDTO = new PerfilDTO();
$objPerfilDTO->retNumIdPerfil();
$objPerfilDTO->setNumIdSistema($numIdSistemaSei);
$objPerfilDTO->setStrNome('Administrador');
$objPerfilDTO = $objPerfilRN->consultar($objPerfilDTO);
if ($objPerfilDTO == null) {
    throw new InfraException('Perfil Administrador do sistema SEI não encontrado.');
}
$numIdPerfilSeiAdministrador = $objPerfilDTO->getNumIdPerfil();
```

Para obter o perfil **Básico** (quando recursos precisam ser acessíveis a todos):

```php
$objPerfilDTO = new PerfilDTO();
$objPerfilDTO->retNumIdPerfil();
$objPerfilDTO->setNumIdSistema($numIdSistemaSei);
$objPerfilDTO->setStrNome('Básico');
$objPerfilDTO = $objPerfilRN->consultar($objPerfilDTO);
if ($objPerfilDTO == null) {
    throw new InfraException('Perfil Básico do sistema SEI não encontrado.');
}
$numIdPerfilSeiBasico = $objPerfilDTO->getNumIdPerfil();
```

### Registrar recursos por entidade

```php
// Recursos sempre presentes
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_cadastrar');
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_alterar');
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_consultar');
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_listar');
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_excluir');
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_selecionar');

// Apenas quando a entidade tem sin_ativo
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_desativar');
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilSeiAdministrador, 'md_xx_entidade_reativar');
```

**Tabelas N:N não têm `desativar`/`reativar`** — registrar apenas os 6 recursos base.

### Perfil Básico nao e default

- So vincular recursos ao perfil `Básico` quando a spec ou a regra de negócio disser
  explicitamente que a funcionalidade deve ficar acessível a todos os usuários internos.
- Para CRUD administrativo interno, o padrão seguro é registrar recursos apenas no
  perfil administrativo do módulo.

### Regra de auditoria do módulo

O manual exige que os recursos auditáveis façam parte de uma regra de auditoria.
Se o script SIP do módulo já cria ou mantém uma regra existente, anexar os novos
recursos a essa mesma regra e replicá-la ao final da atualização.

Exemplo de passos adicionais:

```php
// 1. localizar ou criar a regra do módulo
// 2. inserir os novos recursos em rel_regra_auditoria_recurso
// 3. chamar replicarRegraAuditoria(...)
```

---

## Atualização do switch e metadados

### No switch (ambos os scripts)

```php
case '<versaoAnterior>':
    $this->instalarv<XYZ>();
    break;  // break migra do case anterior para este
```

O `break` fica **no último case** — todos os anteriores usam fallthrough intencional.

### Campos de versão (ambos os scripts)

```php
private $versaoAtualDesteModulo = '<X.Y.Z>';
private $historicoVersoes = array('1.0.0', ..., '<X.Y.Z>');
```

### Classe de integração do módulo

Além dos scripts SEI e SIP, sincronizar a versão exposta por `getVersao()` na classe
`*Integracao.php` do módulo. O valor deve refletir a mesma versão aplicada nos scripts.

## Separacao SEI x SIP

Scripts SIP (`fontes/sei/src/main/php/sip/scripts/*`) devem tratar apenas recursos,
menus, perfis, permissoes, auditoria e parametros no banco SIP.

Nao adicionar validacoes de `*Integracao.php`, `ConfiguracaoSEI.php`,
`ConfiguracaoSIP.php['SIP']['Modulos']` ou `class_exists(<Modulo>Integracao)` em
scripts SIP, salvo se houver evidencia explicita no proprio contexto SIP do modulo.

---

## Regras de bump de versão

| Tipo de mudança | Bump recomendado | Exemplo |
|---|---|---|
| Nova entidade (tabela + recursos SIP) | minor (`x.Y.0`) | 2.0.0 → 2.1.0 |
| Ajuste de coluna, índice, dado inicial | patch (`x.y.Z`) | 2.0.0 → 2.0.1 |
| Remoção de tabela ou recurso | major (`X.0.0`) | 2.0.0 → 3.0.0 |

Para remocao ou mudanca destrutiva: delegar para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release`, conforme o lado afetado.

Quando os scripts nao existem, **nao** tentar gerar o boilerplate completo inline. Delegar para `sei-gerador-scripts-release` e/ou `sip-gerador-scripts-release` com:

- Skill `sei-gerador-scripts-release` para blocos incrementais de release SEI

- Skill `sip-gerador-scripts-release` para blocos incrementais de release SIP
