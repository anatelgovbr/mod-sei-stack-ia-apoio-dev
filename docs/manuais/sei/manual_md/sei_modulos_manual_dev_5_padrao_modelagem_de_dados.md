# 5. Padrão de Modelagem de Dados

## Regras Gerais

Regras de nomenclatura aplicáveis a todos os elementos (tabelas, colunas, índices, etc) do modelo de dados:

- usar somente letras, números e o caractere sublinhado;

- limitar o tamanho de **nome de tabelas e colunas** ao **máximo de 26 caracteres**;

- tendo em vista que tabelas que controlam sequencial de autoincremento de tabelas funcionais recebem automaticamente o prefixo `seq` e que elementos como índices e FKs também recebem prefixos próprios (por exemplo, i01 e fk), essa limitação de 26 caracteres reserva 4 caracteres para uso dos mencionados prefixos, o que evita cair no limitador cabal de 30 caracteres em bancos Oracle para qualquer nome de elemento de banco e de nomenclatura de colunas em DTO.
- utilizar apenas letras minúsculas;
- palavras internas devem ser separadas pelo caractere sublinhado;
- suprimir as preposições;
- utilizar apenas palavras no singular.
- todas as tabelas e colunas devem possuir uma descrição negocial no campo de metadado `comment`, informando sua finalidade funcional; se for coluna de status multi-valorado deve informar também suas opções e finalidades (Ex.: P=Processo, G=Doc. Gerado, E=Doc. Externo).

Em script de instalação/atualização é importante conhecer cada função disponível no `/infra/InfraBD.php`.

## Tabelas

- Não utilizar verbos para designar nomes de tabelas, priorizar o uso de substantivos e adicionar o prefixo `MD_<instituição/módulo>`:
  - `md_abc_pedido`
  - `md_abc_item`
  - `md_abc_nota_fiscal`

- A identificação deve tentar representar a entidade de forma clara dentro do limite de 26 caracteres, podendo utilizar de abreviações, desde que essas abreviações façam sentido:
  - `md_ri_tipo_controle_de_demanda` -> `md_ri_tp_ctrl_demanda`

- Para tabelas que implementam relacionamentos (n x n) utilizar o prefixo `MD_<instituição/módulo>`_rel seguido dos nomes das tabelas envolvidas (sem o prefixo `MD_<instituição/módulo>`) e separados por sublinhado:

  - `md_abc_rel_pedido_item`
- Se o relacionamento expressar um **conceito forte do sistema**, então o nome desse conceito pode ser utilizado:
  - `md_abc_administrador_sistema` (e não `md_abc_rel_usuario_sistema`)
- Tabelas que representam **conjuntos de valores relacionados** a uma determinada entidade, devem conter um prefixo **indicativo do tipo do conjunto** seguido do nome da entidade:
  - `md_abc_tipo_pedido`

## Colunas

- Para **chaves primárias sequenciais** utilizar o prefixo id seguido do nome da tabela:
  - `id_md_abc_pedido`
- Para **chaves primárias que fazem uso de chaves estrangeiras**, manter a nomenclatura da chave estrangeira igual à da chave primária de origem:
  - `id_md_abc_tabela_a`
  - `id_md_abc_tabela_b`

- **Prefixos recomendados**:
   \- sin_: campo sinalizador que aceita apenas os valores S ou N
   \- sta_: *status multi-valorado. Exemplo: P=Processo, G=Documento Gerado, E=Documento Externo
   \- dta_: data
   \- dth: data/hora
   \- din_: dinheiro

- Para **exclusão lógica** utilizar o nome de campo:
   \- sin_ativo

## Tipos de Dados

Quanto ao tipo de dado usado na representação, aconselha-se, para maior portabilidade, a escolha de um dos tipos principais definidos pelo padrão SQL-99 (ou SQL3):

| Tipo | Parâmetro | Significado |
|---|---|---|
| integer | \- | Números inteiros com sinal, o número de bits utilizado na representação é dependente da implementação (geralmente 32 bits). |
| smallint | \- | Números inteiros pequenos com sinal, o número de bits utilizado na representação é dependente da implementação (geralmente 16 bits). |
| numeric | [(*precisão* [,*decimais*])] | Números decimais com precisão fixa. Ao criar uma coluna do tipo numeric é necessário especificar o comprimento total do número e o número de casas decimais. Esse tipo é recomendado para representação de moedas. Muitos bancos de dados possuem um tipo money (não padronizado) que, na maioria das vezes, é um campo numeric com precisão e decimais específicos. |
| decimal | [(*precisão* [,*decimais*])] | Semelhante ao numeric, entretanto deve possuir uma precisão maior permitindo mais casas decimais. |
| float | [(*precisão*)] | Números com precisão única em ponto flutuante. A faixa de valores e a precisão da representação dependem da implementação. |
| double | \- | Números com precisão dupla em ponto flutuante. A faixa de valores e a precisão da representação dependem da implementação, mas é sempre igual ou melhor do que o tipo float. |
| blob | [(*tamanho*)] | Usado para armazenagem de qualquer dado em formato binário. O significado do parâmetro *tamanho* depende da implementação do banco, podendo ser medido em Kb, Mb ou até Gb. |
| char | [(*tamanho*)] | Usado na representação de sequências de caracteres de tamanho fixo. Tenha cuidado com o parâmetro *tamanho* -- para maior portabilidade, evite comprimentos superiores a 1000 caracteres. |
| varchar | (*tamanho*) | Usado na representação de sequências de caracteres de tamanho variável. |
| clob | [(*tamanho*)] | Semelhante ao tipo blob, só que aplicado a caracteres. |
| date | \- | Um valor de data no formato YYYY-MM-DD. A faixa de valores para o ano pode variar de 1 a 9999). |
| time | [(*precisão*)] | Um valor de hora no formato hh:mm:ss.nnn. O parâmetro *precisão* indica as frações de segundo representadas, e é dependente da implementação (geralmente variando entre 0 e 6). |
| timestamp | [(*precisão*)] | Data e hora no formato YYYY-MM-DD hh:mm:ss.nnn. O parâmetro *precisão* indica as frações de segundo representadas, e é dependente da implementação (geralmente variando entre 0 e 6). |
| boolean | \- | Valor lógico booleano (verdadeiro/falso). |

## Chave Primária

Utilizar o prefixo pk seguido do nome da entidade:

- `pk_md_abc_pedido`

## Chave Alternativa

Utilizar o prefixo ak seguido do nome da entidade e do nome do campo ou dos campos que a compõem:

- `ak_md_abc_pedido_codigo`

## Chave Estrangeira

Utilizar o prefixo fk seguido do prefixo `MD_<instituição/módulo>`, do nome da entidade que possui a chave estrangeira **e do nome da entidade à qual a chave faz referência** (sem o prefixo `MD_<instituição/módulo>`):

- `fk_md_abc_item_pedido`

## Índices

Para **índices que não representam chaves estrangeiras** utilizar o prefixo i(01-99)_  seguido do nome da entidade:

- `i01_md_abc_pedido`
- `i02_md_abc_pedido`
...
- `i99_md_abc_pedido`

Para **índices que representam chaves estrangeiras** utilizar o mesmo nome da chave:

- `fk_md_abc_item_pedido`

## Sequências

Utilizar o prefixo seq seguido do nome do objeto ao qual a sequência atende:

`seq_md_abc_pedido`

São utilizadas quando os DTOs possuem o tipo da chave primária nativa. Dependendo do banco de dados utilizado, podem ser tabelas ou sequences.

- MySQL

```sql
create table seq_md_abc_pedido (id int not null primary key AUTO_INCREMENT, campo char(1) null)
```

- SQL Server

```sql
create table seq_md_abc_pedido (id int identity(1,1), campo char(1) null)
```

- Oracle

```sql
CREATE SEQUENCE seq_md_abc_pedido START WITH 1 INCREMENT BY 1 NOCACHE NOCYCLE
```

- PostgreSQL

```sql
CREATE SEQUENCE seq_md_abc_pedido INCREMENT BY 1 START WITH 1
```
