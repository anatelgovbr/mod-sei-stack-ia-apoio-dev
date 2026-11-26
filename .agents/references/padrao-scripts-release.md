# Padrão de código: scripts de instalação/upgrade SEI e SIP

Referência concreta para escrever métodos `instalarv*` nos scripts
`sei_atualizar_versao_modulo_*.php` e `sip_atualizar_versao_modulo_*.php`.

**Antes de escrever qualquer método:** ler os métodos existentes no script-alvo
para identificar padrões já em uso (nomes de variáveis, estilo de log, etc.).

---

## Guards obrigatórios

### Guard 1: Não criar scripts novos se já existem

Consultar `.agents/references/mapa-modulos-scripts.md` antes de qualquer trabalho no módulo.

- Se o lado SEI ou SIP do módulo tiver script no mapa: **nunca criar outro arquivo para esse lado**. Apenas atualizar o script mapeado.
- Se um dos lados estiver marcado como não localizado: verificar fisicamente o diretório correspondente antes de criar o primeiro script desse lado.
- Se o módulo **não** constar no mapa: verificar fisicamente em `sei/scripts/` e `sip/scripts/` antes de concluir que não existem. Nomes podem divergir do padrão convencional (ex.: `md_cgu_eouv_atualizar_modulo.php`).

### Guard 2: Atualizar scripts somente quando houver impacto de release

No lado SEI, a atualização de release é obrigatória quando a mudança introduzir
novo DTO, nova tabela, nova entidade CRUD base ou colunas em DTO existente.

No lado SIP, a atualização é obrigatória somente quando houver impacto real em
recursos, perfis, menus, parâmetros ou versionamento. Atualizar apenas
o lado afetado e sincronizar `getVersao()` em `*Integracao.php` quando aplicável.

Um arquivo PHP novo, por si só, não dispara release. RN, BD, página, integração,
tarefa ou outro PHP sem impacto estrutural ou SIP confirmado não exige alteração
de script.

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

## Script SEI: padrões de DDL

### Objeto obrigatório

```php
$objInfraMetaBD = new InfraMetaBD(BancoSEI::getInstance());
$objInfraMetaBD->setBolValidarIdentificador(true);
```

Com `setBolValidarIdentificador(true)`, a `InfraMetaBD` recusa, antes de executar o SQL e em qualquer banco, nome com mais de 30 caracteres nos métodos `adicionarColuna`, `alterarColuna`, `adicionarChavePrimaria`, `adicionarChaveEstrangeira` e `criarIndice`. O `CREATE TABLE` escrito à mão, com o nome da tabela e das colunas, e o nome passado a `criarSequencialNativa` não passam por essa validação: o DB03 do auditor de banco confere esses nomes.

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

| Método | MySQL | SQL Server | Oracle | PostgreSQL | Uso |
| --- | --- | --- | --- | --- | --- |
| `tipoNumero()` | `integer` | `integer` | `number(*,0)` | `integer` | PK e FK para coluna `integer` |
| `tipoNumeroGrande()` | `bigint` | `bigint` | `number(*,0)` | `bigint` | FK para coluna `bigint`, como `id_protocolo`, `id_procedimento` e `id_documento` |
| `tipoTextoVariavel(n)` | `varchar(n)` | `varchar(n)` | `varchar2(n byte)` | `varchar(n)` | Texto com `n` até 4000 |
| `tipoTextoFixo(n)` | `char(n)` | `char(n)` | `char(n byte)` | `char(n)` | Texto fixo com `n` até 255, como `sin_*` e `sta_*` |
| `tipoTextoGrande()` | `longtext` | `varchar(max)` | `clob` | `text` | Texto acima de 4000 |
| `tipoNumeroDecimal(p,s)` | `numeric(p,s)` | `numeric(p,s)` | `number(p,s)` | `numeric(p,s)` | Valor decimal, como `din_*` |
| `tipoDataHora()` | `datetime` | `datetime` | `date` | `timestamp` | Data e data com hora, como `dta_*` e `dth_*` |

- `tipoNumero()` e `tipoNumeroGrande()` não recebem parâmetro.
- `tipoTextoVariavel(n)` vai até 4000: o Oracle recusa `varchar2` maior (ORA-00910) e o SQL Server recusa acima de 8000.
- `tipoTextoFixo(n)` vai até 255: o MySQL recusa `char` maior e o Oracle recusa acima de 2000.
- Gravar em coluna `tipoTextoGrande()` no Oracle exige bind: ver `.agents/references/padrao-modelagem-dados.md`, seção "Bind de campos CLOB em `executarSql`".

### Mapeamento do contrato JSON para InfraMetaBD

| Tipo no contrato | Método InfraMetaBD | Observação |
|---|---|---|
| `int`, `integer` | `tipoNumero()` | PKs e FKs; o tipo da FK segue a coluna referenciada (seção "Chave estrangeira") |
| `varchar(N)` | `tipoTextoVariavel(N)` | N = tamanho declarado no contrato |
| `char(1)` | `tipoTextoFixo(1)` | Usado em `sin_ativo` e flags |
| `date` | `tipoDataHora()` | `InfraMetaBD` não tem tipo de data pura; a coluna `dta_*` guarda data e hora e o atributo `Dta` do DTO trata só a data |
| `timestamp` | `tipoDataHora()` | Data e hora (coluna `dth_*`) |
| `datetime` | `tipoDataHora()` | Data e hora; proprietário MySQL, preferir `date` ou `timestamp` |
| `numeric` | `tipoNumeroDecimal(p,s)` | Usar `precisao` e `escala` do contrato (chaves opcionais da coluna) |

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

### Sequence / auto-incremento

Toda tabela funcional com PK gerada por sequence `seq_<tabela>` deve configurar o
DTO com `InfraDTO::$TIPO_PK_NATIVA`. O InfraPHP resolve o nome padrao por
`getStrNomeSequenciaNativa()` (`seq_` + `getStrNomeTabela()`).
Tabelas N:N com PK composta **não usam sequence**.

Nao usar `InfraDTO::$TIPO_PK_SEQUENCIAL` para sequences `seq_<tabela>`: esse tipo
consulta `infra_sequencia` usando o nome da tabela (`<tabela>`), sem prefixo `seq_`.

```php
$this->logar('CRIANDO A SEQUENCE seq_md_xx_entidade');
BancoSEI::getInstance()->criarSequencialNativa('seq_md_xx_entidade', 1);
```

`criarSequencialNativa($strSequencia, $numInicial, $bolNumerosGrandes = false)` cria a sequence nos quatro bancos: tabela com `AUTO_INCREMENT` no MySQL, tabela com `identity` no SQL Server e `CREATE SEQUENCE` no Oracle e no PostgreSQL. Com o terceiro parâmetro `true`, o id da tabela de sequence fica `bigint` no MySQL e no SQL Server; use `true` quando a PK da tabela for `tipoNumeroGrande()`. Em script que já ramifica por banco para criar sequence, a sequence nova também usa `criarSequencialNativa()`.

### Remover sequence

A sequence é tabela no MySQL e no SQL Server e sequence real no Oracle e no PostgreSQL, e cada banco recusa o comando do outro tipo:

```php
$this->logar('REMOVENDO A SEQUENCE seq_md_xx_entidade');
if (BancoSEI::getInstance() instanceof InfraMySql || BancoSEI::getInstance() instanceof InfraSqlServer) {
    BancoSEI::getInstance()->executarSql('drop table seq_md_xx_entidade');
} else {
    BancoSEI::getInstance()->executarSql('drop sequence seq_md_xx_entidade');
}
```

Quando a remoção pode rodar em base onde a sequence já não existe, consultar antes com este helper local do script:

```php
private function existeSequencia(string $strSequencia): bool
{
    $objBanco = BancoSEI::getInstance();
    if ($objBanco instanceof InfraOracle) {
        $strSql = "select sequence_name from all_sequences where lower(sequence_owner) = '" . strtolower($objBanco->getUsuario()) . "' and lower(sequence_name) = '" . $strSequencia . "'";
        return count($objBanco->consultarSql($strSql)) > 0;
    }
    if ($objBanco instanceof InfraPostgreSql) {
        return count($objBanco->consultarSql("select sequence_name from information_schema.sequences where sequence_name = '" . $strSequencia . "'")) > 0;
    }
    return count((new InfraMetaBD($objBanco))->obterTabelas($strSequencia)) > 0;
}
```

`InfraMetaBD::obterSequencias()` não serve para essa checagem: no Oracle, ela não acha a sequence quando o usuário do banco está em minúsculas na configuração.

### Ajustar o próximo valor de uma sequence

Depois de gravar registro com id calculado fora da sequence, recriar a sequence com início no último id gravado mais 1. É o procedimento do `ScriptRN::atualizarSequencias()` do core. Quando a PK da tabela é `tipoNumeroGrande()`, leia o último id com `formatarSelecaoDbl` e passe `true` no terceiro parâmetro de `criarSequencialNativa`, como o core faz no grupo de ids `bigint`:

```php
// $numProximo = último id gravado na tabela + 1
// $bolNumerosGrandes = true quando a PK da tabela é tipoNumeroGrande()
$this->logar('AJUSTANDO A SEQUENCE seq_md_xx_entidade');
if (BancoSEI::getInstance() instanceof InfraMySql || BancoSEI::getInstance() instanceof InfraSqlServer) {
    BancoSEI::getInstance()->executarSql('drop table seq_md_xx_entidade');
} else {
    BancoSEI::getInstance()->executarSql('drop sequence seq_md_xx_entidade');
}
BancoSEI::getInstance()->criarSequencialNativa('seq_md_xx_entidade', $numProximo, $bolNumerosGrandes);
if ($numProximo > 1 && BancoSEI::getInstance() instanceof InfraMySql) {
    BancoSEI::getInstance()->executarSql('insert into seq_md_xx_entidade (id, campo) values (' . ($numProximo - 1) . ', \'0\')');
    BancoSEI::getInstance()->executarSql('alter table seq_md_xx_entidade AUTO_INCREMENT = ' . $numProximo);
}
```

Os comandos de ajuste do manual (cap. 3, seção Andamentos) não funcionam nos quatro bancos: no MySQL e no Oracle, a sequence devolve o último id gravado e a próxima inserção colide com ele; no SQL Server, o `DBCC CHECKIDENT` falha pela `executarSql`; no PostgreSQL, o `CREATE SEQUENCE` sem `drop sequence` falha porque a sequence já existe. Scripts de módulo que ajustam com `CREATE SEQUENCE ... START WITH <último id gravado>` têm a mesma colisão no Oracle e no PostgreSQL.

### Chave estrangeira

```php
$objInfraMetaBD->adicionarChaveEstrangeira('fk_md_xx_entidade_pai', 'md_xx_entidade',
    array('id_md_xx_pai'), 'md_xx_pai', array('id_md_xx_pai'));
```

Assinatura: `adicionarChaveEstrangeira(nomeFk, tabelaFilha, colunasFilha[], tabelaPai, colunasPai[], bolCriarIndice = true)`.
Nome e limite da FK: `.agents/references/padrao-modelagem-dados.md`, seções "Naming e limites" e "Chaves e índices (naming)".

A coluna da FK tem o mesmo tipo da coluna referenciada: o MySQL e o SQL Server recusam FK de `integer` para `bigint`, e o Oracle e o PostgreSQL aceitam, então o erro só aparece no órgão que usa um dos dois primeiros. Em coluna de texto, o tamanho também é o mesmo: o SQL Server recusa FK de `varchar(18)` para `varchar(14)`, e os outros três bancos aceitam. No SEI 5.0, `id_protocolo`, `id_procedimento` e `id_documento` são `bigint` e pedem `tipoNumeroGrande()`; `id_usuario`, `id_unidade` e `id_tarefa` são `integer` e pedem `tipoNumero()`; `id_atividade` muda de tipo entre instalações, e o core cria a coluna que a referencia com `obterTipoColunaTabela('atividade', 'id_atividade')`. No Oracle, os dois métodos geram `number(*,0)` e todos esses ids são `number`. Para outra coluna do core, conferir o tipo com `$objInfraMetaBD->obterTipoColunaTabela('<tabela>', '<coluna>')`. O retorno serve como tipo de coluna nova só quando a coluna é numérica, porque vem sem o tamanho.

Quando as colunas da FK são as mesmas da PK da tabela filha, o sexto parâmetro desliga o índice no Oracle, que recusa um segundo índice nas colunas da PK (ORA-01408):

```php
$objInfraMetaBD->adicionarChaveEstrangeira('fk_md_xx_ent_ext_entidade', 'md_xx_entidade_ext',
    array('id_md_xx_entidade'), 'md_xx_entidade', array('id_md_xx_entidade'),
    !(BancoSEI::getInstance() instanceof InfraOracle));
```

### Índice para chave estrangeira

`adicionarChaveEstrangeira()` já cria o índice da FK com o mesmo nome da chave (parâmetro `$bolCriarIndice`, padrão `true`), que é a regra do manual cap. 5 ("índices que representam chaves estrangeiras usam o mesmo nome da chave"). Não chamar `criarIndice` para FK: duplica o índice. `criarIndice` serve só para índice que não representa FK, com o nome da seção "Chaves e índices (naming)" de `.agents/references/padrao-modelagem-dados.md`:

```php
$objInfraMetaBD->criarIndice('md_xx_entidade', 'i01_md_xx_entidade', array('dta_cadastro'));
```

Assinatura: `criarIndice(tabela, nomeIndice, colunas[], unico = false)`. O auditor de banco não enxerga o índice que `adicionarChaveEstrangeira` cria, então o aviso DB09 sobre a FK continua mesmo com a FK criada no script; nesse caso, o aviso é esperado.

### Índice único

Crie o índice único com o quarto parâmetro de `criarIndice` em `true`, com o nome de chave alternativa da seção "Chaves e índices (naming)" de `.agents/references/padrao-modelagem-dados.md`. A `criarIndice` compara só as colunas: quando já existe índice nas mesmas colunas, ela mantém ou renomeia esse índice sem torná-lo único, então exclua antes o índice existente:

```php
$objInfraMetaBD->criarIndice('md_xx_entidade', 'ak_md_xx_entidade_id_externo', array('id_externo'), true);
```

No SQL Server, quando a tabela tem `ANSI_NULLS` ligado, que é o padrão, a `InfraMetaBD` cria o índice filtrado por `is not null` nas colunas, que aceita vários nulos, como os outros três bancos. O `create unique index` escrito à mão recusa o segundo nulo no SQL Server.

### Limites de nomenclatura (cross-SGBD)

Os nomes e limites de tabela, coluna, índice, FK e sequence estão em `.agents/references/padrao-modelagem-dados.md`, seções "Naming e limites" e "Chaves e índices (naming)". O Oracle 11g recusa nome com mais de 30 caracteres (ORA-00972), e MySQL, SQL Server e PostgreSQL aceitam; `setBolValidarIdentificador(true)` (seção "Objeto obrigatório") faz o erro aparecer em qualquer banco nos métodos da `InfraMetaBD` que validam o nome.

### Alterar tabela existente (upgrade incremental)

```php
$this->logar('ADICIONANDO COLUNA num_campo EM md_xx_entidade');
$objInfraMetaBD->adicionarColuna('md_xx_entidade', 'num_campo',
    $objInfraMetaBD->tipoNumero(), 'null');
```

O quarto parâmetro de `adicionarColuna` e de `alterarColuna` é texto que entra no SQL, sempre em minúsculas e sem espaço extra: `'null'` ou `'not null'`. No PostgreSQL, `alterarColuna` compara a opção com `'null'` sem converter maiúsculas, e `'NULL'` gera `set not null`, o contrário do pedido.

### Coluna `NOT NULL` em tabela com dados

Criar a coluna como `'null'`, preencher e depois tornar `'not null'`:

```php
$objInfraMetaBD->adicionarColuna('md_xx_entidade', 'sin_campo', $objInfraMetaBD->tipoTextoFixo(1), 'null');
BancoSEI::getInstance()->executarSql("update md_xx_entidade set sin_campo = 'N'");
$objInfraMetaBD->alterarColuna('md_xx_entidade', 'sin_campo', $objInfraMetaBD->tipoTextoFixo(1), 'not null');
```

Criar direto com `'not null'` falha no SQL Server, no Oracle e no PostgreSQL quando a tabela tem linhas. Criar com `"DEFAULT 'S' NOT NULL"` funciona, mas no SQL Server deixa uma restrição `DF__...` com nome gerado pelo banco, e depois `excluirColuna` e `alterarColuna` nessa coluna falham.

### Alterar ou excluir coluna com FK ou índice

Excluir antes a FK e o índice da coluna, nesta ordem, e recriar depois quando a coluna continuar:

```php
$objInfraMetaBD->excluirChaveEstrangeira('md_xx_entidade', 'fk_md_xx_entidade_pai');
$objInfraMetaBD->excluirIndice('md_xx_entidade', 'fk_md_xx_entidade_pai');
$objInfraMetaBD->excluirColuna('md_xx_entidade', 'id_md_xx_pai');
```

O MySQL recusa excluir a coluna da FK e o índice da FK enquanto a FK existe. O SQL Server recusa trocar o tipo ou a nulidade, ou excluir, coluna que tem índice. Para coluna só com índice: `excluirIndice`, `alterarColuna` e `criarIndice`.

### Trocar o tipo de coluna com dados

Antes de trocar o tipo, exclua a FK e o índice da coluna, como na seção "Alterar ou excluir coluna com FK ou índice", e recrie os dois no fim, nos quatro bancos.

Enquanto a coluna continua texto, `alterarColuna` troca o tipo com dados nos quatro bancos: `tipoTextoVariavel(n)` e `tipoTextoFixo(n)` entre si, aumento de tamanho, `tipoTextoVariavel(n)` para `tipoTextoGrande()` e troca de nulidade. Reduzir o tamanho abaixo de um valor gravado falha nos quatro bancos (no Oracle, ORA-01441).

De número para texto, o Oracle recusa a troca em coluna com dados (ORA-01439), e o ramo Oracle renomeia, copia e exclui a coluna:

```php
$objInfraMetaBD->excluirIndice('md_xx_entidade', 'i01_md_xx_entidade');
if (BancoSEI::getInstance() instanceof InfraOracle) {
    BancoSEI::getInstance()->executarSql('alter table md_xx_entidade rename column cod_externo to cod_externo_antigo');
    $objInfraMetaBD->adicionarColuna('md_xx_entidade', 'cod_externo', $objInfraMetaBD->tipoTextoVariavel(20), 'null');
    BancoSEI::getInstance()->executarSql('update md_xx_entidade set cod_externo = cod_externo_antigo');
    $objInfraMetaBD->excluirColuna('md_xx_entidade', 'cod_externo_antigo');
} else {
    $objInfraMetaBD->alterarColuna('md_xx_entidade', 'cod_externo', $objInfraMetaBD->tipoTextoVariavel(20), 'null');
}
$objInfraMetaBD->criarIndice('md_xx_entidade', 'i01_md_xx_entidade', array('cod_externo'));
```

O SQL Server não tem `RENAME COLUMN`; por isso a renomeação fica só no ramo Oracle. No Oracle, excluir a coluna renomeada apaga junto a FK e o índice dela, sem erro. De texto para número, o Oracle e o PostgreSQL recusam o `alterarColuna` em coluna com dados, e o exemplo acima não cobre esse caso. Na coluna de FK, o tipo e o tamanho novos são os da coluna referenciada, conforme a seção "Chave estrangeira": o SQL Server recusa recriar a FK quando só a coluna da FK muda de tamanho.

### Checagem de existência antes de DDL

DDL que pode rodar em base onde o objeto já existe, ou já saiu, consulta antes:

| Objeto | Consulta |
| --- | --- |
| Tabela | `count($objInfraMetaBD->obterTabelas('md_xx_entidade')) > 0` |
| Coluna | `count($objInfraMetaBD->obterColunasTabela('md_xx_entidade', 'num_campo')) > 0` |
| Índice | `isset($objInfraMetaBD->obterIndices(null, 'md_xx_entidade')['md_xx_entidade']['i01_md_xx_entidade'])` |
| PK e FK | `$objInfraMetaBD->obterConstraints('md_xx_entidade')`, com `constraint_name` e `constraint_type`; no MySQL, a PK vem com o nome `primary` |
| Sequence | helper `existeSequencia()` da seção "Remover sequence" |

### Leitura e gravação de dados no script

Dado que depende de regra de negócio, como a coluna `idx_`, é preenchido ou recomposto pela RN que já monta o dado, com o DTO filtrando só os registros pendentes. A `InfraBD` trata as diferenças entre os bancos, como a divisão de `IN` acima de 1000 itens no Oracle e o limite de 2100 parâmetros do SQL Server. A regra da coluna `idx_` está em `.agents/references/padrao-metodos-crud-infraphp.md`, seção "Coluna derivada para busca textual".

O script roda o código da versão atual do módulo também nos `instalarv*` antigos. No acesso por DTO, use em `ret*` e nos filtros só colunas que já existem naquele `instalarv*`, sem `retTodos()`, e confira que o método da RN chamado também lê só essas colunas.

SQL escrito à mão usa só sintaxe e funções aceitas pelos quatro bancos. Quando precisar de função própria de um banco, ramifique por banco e cubra MySQL, SQL Server, Oracle e PostgreSQL. Data, número e texto entram no SQL por `formatarGravacao<Tipo>` do `BancoSEI`; cada campo selecionado sai por `formatarSelecao<Tipo>`, e o valor lido por `consultarSql` passa por `formatarLeitura<Tipo>`.

---

## Script SIP: padrões de recursos e perfis

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

**Tabelas N:N não têm `desativar`/`reativar`**. Registrar apenas os 6 recursos base.

### Perfil Básico nao e default

- So vincular recursos ao perfil `Básico` quando a spec ou a regra de negócio disser
  explicitamente que a funcionalidade deve ficar acessível a todos os usuários internos.
- Para CRUD administrativo interno, o padrão seguro é registrar recursos apenas no
  perfil administrativo do módulo.

### Regra de auditoria do módulo

O manual exige que os recursos auditáveis façam parte de uma regra de auditoria.
Se o script SIP do módulo já cria ou mantém uma regra existente, anexar os novos
recursos de escrita a essa mesma regra e replicá-la ao final da atualização. Os recursos `_listar`, `_consultar` e `_selecionar` ficam fora da regra, conforme `.agents/references/padrao-auditoria-sip-sei.md`.

Exemplo de passos adicionais:

```php
// 1. localizar ou criar a regra do módulo
// 2. inserir os novos recursos de escrita em rel_regra_auditoria_recurso
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

O `break` fica **no último case**. Todos os anteriores usam fallthrough intencional.

### Campos de versão (ambos os scripts)

```php
private $versaoAtualDesteModulo = '<X.Y.Z>';
private $historicoVersoes = array('1.0.0', ..., '<X.Y.Z>');
```

### Classe de integração do módulo

Além dos scripts SEI e SIP, sincronizar a versão exposta por `getVersao()` na classe
`*Integracao.php` do módulo. O valor deve refletir a mesma versão aplicada nos scripts.

No script do SEI, confira essa sincronia em `atualizarVersaoConectado()`, depois da checagem da versão do framework e antes do teste de permissão de DDL:

```php
$objMdXxIntegracao = new MdXxIntegracao();
if ($objMdXxIntegracao->getVersao() !== $this->versaoAtualDesteModulo) {
    $this->finalizar('VERSÃO ' . $objMdXxIntegracao->getVersao() . ' DA CLASSE MdXxIntegracao DIFERENTE DA VERSÃO ' . $this->versaoAtualDesteModulo . ' DO SCRIPT', true);
}
```

No script que estende `InfraScriptVersao`, `setStrClasseModulo('MdXxIntegracao')` faz essa conferência só com os dois primeiros números da versão: com `1.2.0` em `setStrVersaoAtual()` e `1.2.1` em `getVersao()`, o script passa e grava `1.2.0`. Nessa família, confira à mão que os três números de `getVersao()` são os de `setStrVersaoAtual()`. O script do SIP fica sem essa conferência, conforme a seção "Separação SEI x SIP".

## Separação SEI x SIP

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
