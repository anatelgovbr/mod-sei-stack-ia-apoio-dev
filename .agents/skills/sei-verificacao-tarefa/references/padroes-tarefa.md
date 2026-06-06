# Padrões de IDs de Tarefa — Manual TRF4

Baseado em `sei_modulos_manual_dev_3_consideracoes_previas.md` —
Seção "Atribuição de Tarefa (andamento)".

---

## K1 — ID >= 1000

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias / Tarefa Módulo

IDs de tarefa de módulo (`id_tarefa_modulo`) devem ser **>= 1000**.
Valores menores são reservados para tarefas core do SEI.

**Conforme:**
```php
'id_tarefa_modulo' => 1001,
```

**Não conforme:**
```php
'id_tarefa_modulo' => 999,  // ERRO — reservado para SEI
```

---

## K2 — ID < 1000 reservado

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias

IDs menores que 1000 são exclusivamente do core do SEI.
Qualquer definição de tarefa de módulo com ID < 1000 deve ser tratada
como erro (exceto o caso especial do ID=65).

**Lista de IDs core reservados (amostra):**
- 1-64: Reservados core
- 65: Livre para módulo (com restrição)
- 66-999: Reservados core

---

## K3 — Prefixo MD_<INST/PROJ> em maiúsculas

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias / nomenclatura de recursos

O nome da tarefa deve usar prefixo `MD_<INST/PROJ>_` em **maiúsculas**,
seguido do nome descritivo em maiúsculas separado por `_`.

**Conforme:**
```php
'nome' => 'MD_RI_RESTAURANTE_CADASTRAR',
```

**Não conforme:**
```php
'nome' => 'Md_Ri_Restaurante_Cadastrar',  // minúsculas
'nome' => 'md_ri_restaurante_cadastrar',   // tudo minúsculas
```

---

## K4 — Máximo 50 caracteres

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias

O atributo `nome` da tarefa (`id_tarefa_modulo`) tem limite de **50 caracteres**.

**Conforme:**
```php
'nome' => 'MD_RI_RESTAURANTE_CADASTRAR',  // 26 chars
```

**Não conforme:**
```php
'nome' => 'MD_RI_RESTaurante_CADASTRAR_ALGO_MUITOMAIOR',  // > 50 chars
```

---

## K5 — Tabela de tarefas com definição

**Severidade:** Aviso
**Base:** Manual SEI MD §Considerações Prévias

Cada tarefa de módulo deve estar definida em uma tabela de controle
`md_<sigla>_tarefa` com os campos `id_tarefa_modulo`, `nome` e `descricao`.

**Estrutura esperada:**
```sql
CREATE TABLE md_ri_tarefa (
    id_tarefa_modulo INTEGER PRIMARY KEY,
    nome VARCHAR(50) NOT NULL,
    descricao VARCHAR(200)
);
```

---

## K6 — ID não conflita no módulo

**Severidade:** Aviso
**Base:** Manual SEI MD §Considerações Prévias

IDs de tarefa devem ser únicos dentro do módulo. Duplicidade causa
sobreposição de comportamento.

**Conforme:**
```php
// IDs únicos
1001 => 'MD_RI_RESTAURANTE_CADASTRAR',
1002 => 'MD_RI_RESTAURANTE_ALTERAR',
```

**Não conforme:**
```php
// ID duplicado
1001 => 'MD_RI_RESTAURANTE_CADASTRAR',
1001 => 'MD_RI_RESTAURANTE_ALTERAR',  // CONFLITO
```

---

## K7 — ID=65 com atributo DESCRICAO

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias — Exceção de ID

O ID=65 é a **única exceção** ao rule K1 (ID < 1000) e serve para
andamentos de texto livre. Deve ser usado **exclusivamente** com
um atributo `descricao` que explique seu propósito.

**Conforme:**
```php
65 => array(
    'id_tarefa_modulo' => 65,
    'nome' => 'MD_RI_ANDAMENTO_LIVRE',
    'descricao' => 'Andamentos livres para observacoes diversas'
),
```

**Não conforme:**
```php
// ID=65 para andamento especifico (nao livre)
65 => array(
    'id_tarefa_modulo' => 65,
    'nome' => 'MD_RI_CONFIRMAR_RECEBIMENTO',
    // falta descricao de livre
),
```

---

## Matriz de severidade

| ID | Regra | Sev |
|----|-------|-----|
| K1 | ID >= 1000 | **Erro** |
| K2 | ID < 1000 reservado | **Erro** |
| K3 | Prefixo MD_ em maiúsculas | **Erro** |
| K4 | Máximo 50 caracteres | **Erro** |
| K5 | Tabela de tarefas com definição | **Aviso** |
| K6 | ID único no módulo | **Aviso** |
| K7 | ID=65 com DESCRICAO | **Erro** |