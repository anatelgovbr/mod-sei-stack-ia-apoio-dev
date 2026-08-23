# Padrões de IDs de Tarefa, Manual TRF4

Baseado em `sei_modulos_manual_dev_3_consideracoes_previas.md`,
Seção "Atribuição de Tarefa (andamento)".

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

IDs menores que 1000 são exclusivamente do core do SEI.
Qualquer definição de tarefa de módulo com ID < 1000 deve ser tratada
como erro (exceto o caso especial do ID=65).

**Lista de IDs core reservados (amostra):**
- 1-64: Reservados core
- 65: Livre para módulo (com restrição)
- 66-999: Reservados core

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

## K7 - ID=65 com atributo DESCRICAO

**Severidade:** Erro
**Base:** Manual SEI MD §Considerações Prévias, Exceção de ID

O ID=65 é a **única exceção** à regra K1 (ID < 1000) e serve para
andamentos de texto livre. Deve ser usado **exclusivamente** com
o atributo `DESCRICAO` que explica seu propósito.

**Conforme:**
```php
[
    'id_tarefa' => 65,
    'id_tarefa_modulo' => 'MD_RI_ANDAMENTO_LIVRE',
    'atributos' => ['DESCRICAO' => 'Andamentos livres para observacoes diversas']
],
```

**Não conforme:**
```php
// ID=65 para andamento especifico (nao livre)
[
    'id_tarefa' => 65,
    'id_tarefa_modulo' => 'MD_RI_CONFIRMAR_RECEBIMENTO'
],
```

---

## Matriz de severidade

| ID | Regra | Sev |
|----|-------|-----|
| K1 | `id_tarefa` >= 1000 | **Erro** |
| K2 | `id_tarefa` < 1000 reservado | **Erro** |
| K3 | Prefixo de `id_tarefa_modulo` | **Erro** |
| K4 | `id_tarefa_modulo` com até 50 caracteres | **Erro** |
| K6 | Unicidade dos dois identificadores | **Erro** |
| K7 | ID=65 com DESCRICAO | **Erro** |
