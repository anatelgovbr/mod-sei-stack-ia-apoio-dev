# Padrões de IDs de Tarefa, Manual TRF4

Baseado em `sei_modulos_manual_dev_3_consideracoes_previas.md`,
Seção "Andamentos".

---

## K1 - ID >= 1000

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias / Tarefa Módulo

O identificador numérico `id_tarefa` deve ser maior ou igual a 1000. Valores
menores são reservados para tarefas do core do SEI, exceto 65.

**Conforme:**
```php
'id_tarefa' => 1001,
```

**Não conforme:**
```php
'id_tarefa' => 999,  // ERRO: reservado para SEI
```

---

## K2 - ID < 1000 reservado

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias

IDs menores que 1000 são exclusivamente do core do SEI. Cadastro de tarefa de módulo com ID < 1000 é erro, inclusive com ID 65: a 65 é tarefa do core que o módulo só lança (K7).

---

## K3 - Prefixo de `id_tarefa_modulo`

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias / nomenclatura de recursos

O identificador textual `id_tarefa_modulo` deve usar o prefixo
`MD_<SIGLA>_` em maiúsculas, seguido do nome descritivo.

**Conforme:**
```php
'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_CADASTRAR',
```

**Não conforme:**
```php
'id_tarefa_modulo' => 'Md_Ri_Restaurante_Cadastrar',
'id_tarefa_modulo' => 'md_ri_restaurante_cadastrar',
```

O valor identifica a tarefa em qualquer instalação, porque o `id_tarefa` muda de uma instalação para outra. Tarefa já instalada mantém o `id_tarefa_modulo`, mesmo fora do padrão, como `TRF4_` em `trf4/julgamento` e `PEN_` no PEN: os lançamentos e as consultas do módulo usam esse valor, e o K3 nessa tarefa é achado preexistente.

---

## K4 - Máximo 50 caracteres

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias

O valor textual de `id_tarefa_modulo` tem limite de **50 caracteres**.

**Conforme:**
```php
'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_CADASTRAR',
```

**Não conforme:**
```php
'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_CADASTRAR_ALGO_MUITO_MAIOR_QUE_LIMITE',
```

---

## K6 - Identificadores únicos no módulo

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias

`id_tarefa` e `id_tarefa_modulo` devem ser únicos em suas respectivas
dimensões. Duplicidade causa sobreposição de comportamento.

**Conforme:**
```php
['id_tarefa' => 1001, 'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_CADASTRAR'],
['id_tarefa' => 1002, 'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_ALTERAR'],
```

**Não conforme:**
```php
['id_tarefa' => 1001, 'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_CADASTRAR'],
['id_tarefa' => 1001, 'id_tarefa_modulo' => 'MD_RI_RESTAURANTE_ALTERAR'],
```

---

## K7 - Tarefa 65: só lançamento, com atributo DESCRICAO

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias, Andamentos

A tarefa 65 é do core: atualização do andamento com texto livre (`TarefaRN::$TI_ATUALIZACAO_ANDAMENTO`). É a única tarefa abaixo de 1000 que o módulo pode lançar, sempre com o atributo `DESCRICAO` preenchido com o texto do andamento. O módulo nunca cadastra a 65; para andamento próprio, cadastra tarefa com `id_tarefa_modulo` (K1, K3).

Na lista de definição `*_tarefa.php` lida pelo auditor, a entrada 65 representa esse lançamento e exige `DESCRICAO` não vazio.

**Conforme:**
```php
$objEntradaLancarAndamentoAPI = new EntradaLancarAndamentoAPI();
$objEntradaLancarAndamentoAPI->setIdProcedimento($dblIdProcedimento);
$objEntradaLancarAndamentoAPI->setIdTarefa(65);

$objAtributoAndamentoAPI = new AtributoAndamentoAPI();
$objAtributoAndamentoAPI->setNome('DESCRICAO');
$objAtributoAndamentoAPI->setValor('Prazo de resposta prorrogado.');
$objEntradaLancarAndamentoAPI->setAtributos([$objAtributoAndamentoAPI]);

(new SeiRN())->lancarAndamento($objEntradaLancarAndamentoAPI);
```

**Não conforme:**
```php
// cadastrar a 65 como tarefa do modulo
$objTarefaDTO->setNumIdTarefa(65);
$objTarefaDTO->setStrIdTarefaModulo('MD_RI_ANDAMENTO_LIVRE');
$objTarefaRN->cadastrar($objTarefaDTO);
```

Lançar a 65 sem o atributo `DESCRICAO` também é não conforme.

---

## K8 - Como obter o `id_tarefa` do modulo

**Severidade:** Erro
**Base:** Manual SEI MD, Considerações Prévias, Andamentos

A parte mais esquecida do procedimento é a atualização da sequência no final.

1. Obter o próximo id por `BancoSEI::getInstance()->getValorSequencia('seq_tarefa')`. Por esse caminho, o passo 2 não se aplica, e o passo 5 só se aplica quando o passo 4 troca o valor por 1000. No SEI 5.0 recém-instalado, o primeiro valor é 1001 nos quatro bancos.
2. Se a inserção for feita sem essa chamada, calcular por `select max(id_tarefa)+1 from tarefa`.
3. Se o valor obtido for maior ou igual a 1000, utilizar esse valor.
4. Se for menor que 1000, utilizar 1000, porque ids abaixo de 1000 são reservados do core.
5. Depois de inserir com id calculado, recriar `seq_tarefa` com início no último id gravado mais 1, pelo trecho de `.agents/references/padrao-scripts-release.md`, seção "Ajustar o próximo valor de uma sequence". Os comandos de ajuste do manual, capítulo 3, seção Andamentos, não funcionam nos quatro bancos; a mesma seção mostra o que acontece em cada um.

**Não conforme:** inserir com id calculado e não atualizar `seq_tarefa`. A próxima inserção que usar a sequência colide com o id já gravado.

**Verificação automática:** no cadastro por `TarefaDTO` ou `INSERT INTO tarefa`, o auditor aceita sem realinhamento o id vindo de `getValorSequencia('seq_tarefa')`, direto ou por variável cuja última atribuição antes do uso é essa chamada. Id fixo ou calculado passa quando o arquivo recria `seq_tarefa` por `criarSequencialNativa('seq_tarefa', ...)` ou por `ScriptRN::atualizarSequencias()`. Com ajuste por SQL próprio (`CREATE SEQUENCE`, `ALTER`, `INSERT INTO seq_tarefa`, `DBCC CHECKIDENT` ou `setval`), o auditor dá aviso, porque não lê o valor que o SQL grava: confira na revisão que a sequence começa no último id gravado mais 1 nos quatro bancos. Sem nenhum desses ajustes, dá erro. A ordem entre cálculo, realinhamento e cadastro fica para a revisão.

---

## K9 - Variáveis e sinalizadores do andamento

**Severidade:** Erro
**Base:** Manual SEI MD, Considerações Prévias, Andamentos

### Variáveis no texto do andamento

O texto da tarefa pode conter variáveis, como `@SALA@`, e o valor de cada uma é informado por **atributos** (`AtributoAndamentoAPI`) no momento de lançar o andamento.

Algumas variáveis são **reservadas do sistema**, como `DOCUMENTO`, `PROCESSO`, `USUARIO` e `UNIDADE`. O módulo pode utilizá-las, desde que informe o `Valor` e o `IdOrigem` que cada uma espera. Não redefinir o significado de uma variável reservada. A tabela completa está no manual, capítulo 3, seção Andamentos: `docs/manuais/sei/manual_md/sei_modulos_manual_dev_3_consideracoes_previas.md`.

### Sinalizadores da tabela `tarefa`

Todos aceitam `S` ou `N`.

| Coluna | O que controla | Como escolher |
|---|---|---|
| `sin_historico_resumido` | Se o andamento aparece no histórico resumido | |
| `sin_historico_completo` | Se o andamento aparece no histórico completo | |
| `sin_lancar_andamento_fechado` | `N` lança o andamento aberto, em amarelo, como última atividade da unidade; `S` lança já concluído | Andamento aberto em processo concluído na unidade gera o erro "Processo X não possui andamento aberto na unidade Y" |
| `sin_permite_processo_fechado` | `S` permite lançar em processo concluído na unidade, e o andamento aberto passa a ser lançado concluído | Antes de usar `S`, verificar se o fluxo deveria reabrir o processo: andamento concluído em processo concluído não aparece para ninguém da unidade |
| `sin_fechar_andamentos_abertos` | `S` conclui os andamentos abertos da unidade, e só o novo fica em amarelo | Usar `S` quando o processo estiver aberto na unidade no momento do lançamento |

Definir os cinco explicitamente ao cadastrar a tarefa do módulo. `TarefaRN::cadastrar` recusa sinalizador vazio ou inválido; `TarefaBD::cadastrar` e `INSERT INTO tarefa` gravam sem essa validação.

**Verificação automática:** no cadastro por `TarefaDTO` ou `INSERT INTO tarefa`, o auditor confere que os cinco estão presentes e que o valor literal é `S` ou `N`. A escolha de cada valor fica para a revisão.

---

## Matriz de severidade

| ID | Regra | Sev |
|----|-------|-----|
| K1 | `id_tarefa` >= 1000 | **Erro** |
| K2 | `id_tarefa` < 1000 reservado | **Erro** |
| K3 | Prefixo de `id_tarefa_modulo` | **Erro** |
| K4 | `id_tarefa_modulo` com até 50 caracteres | **Erro** |
| K6 | Unicidade dos dois identificadores | **Erro** |
| K7 | Tarefa 65 só no lançamento, com DESCRICAO | **Erro** |
| K8 | Id da tarefa por `seq_tarefa` ou com realinhamento | **Erro**; aviso com ajuste por SQL próprio |
| K9 | Cinco sinalizadores explícitos, com `S` ou `N` | **Erro** |
