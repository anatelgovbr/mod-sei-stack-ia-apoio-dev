# Padrões de Transação em InfraRN — Manual TRF4

Baseado em `sei_modulos_manual_dev_4_infraphp.md` — Seção "InfraRN (2ª Camada)".

---

## T1 — Sufixo correto por operação

**Severidade:** Erro
**Base:** Manual SEI MD §InfraRN — Mecanismo de Controle de Transação

A classe `InfraRN` implementa controle automático de conexão e transação.
Métodos que fazem **escrita** devem usar o sufixo `Controlado`.
Métodos que fazem apenas **leitura** devem usar o sufixo `Conectado`.

| Tipo | Suffix | Abre | Uso |
|------|--------|------|-----|
| Write | `Controlado` | Conexão + Transação | insert, update, delete |
| Read | `Conectado` | Conexão apenas | select, count |

**Conforme:**
```php
protected function cadastrarControlado($objDTO) {
    // transação aberta automaticamente
}

protected function consultarConectado($objDTO) {
    // apenas conexão, sem transação
}
```

**Não conforme:**
```php
// Operation de escrita com Conectado — transação não aberta
protected function cadastrarConectado($objDTO) {
    // ERRO: conexão sem transação para operação de escrita
}
```

---

## T2 — inicializarObjInfraIBanco()

**Severidade:** Erro
**Base:** Manual SEI MD §InfraRN

A classe RN **deve** implementar o método `inicializarObjInfraIBanco()`
retornando `BancoSEI::getInstance()`. Sem isso, o controle de transação
não funciona.

**Conforme:**
```php
class MdRiRestauranteRN extends InfraRN {

    protected function inicializarObjInfraIBanco() {
        return BancoSEI::getInstance();
    }
}
```

**Não conforme:**
```php
// Falta o método — controle de transação失效
class MdRiRestauranteRN extends InfraRN {
    // sem inicializarObjInfraIBanco()
}
```

---

## T3 — Sem encadeamento Controlado→Controlado

**Severidade:** Erro
**Base:** Manual SEI MD §InfraRN — Transações

Métodos `Controlado` não devem chamar outros métodos `Controlado`
da mesma classe. O aninhamento de transações pode causar inconsistências
em caso de erro.

**Conforme:**
```php
protected function cadastrarControlado($objDTO) {
    // Lógica de negócio
    // Chama método da BD, não de outra RN
    $this->getObjInfraIBanco()->...
}
```

**Não conforme:**
```php
protected function cadastrarControlado($objDTO) {
    $this->processarAlgumaCoisaControlado(); // ANINHAMENTO — perigoso
}
```

**Regra prática:** RN chama BD (diretamente), não chama outro RN.
RN de outras classes pode ser chamada desde que em transação pai.

---

## T4 — Sem fecharConexao() explícito

**Severidade:** Aviso
**Base:** Manual SEI MD §InfraRN

O framework gerencia automaticamente abertura e fechamento de conexões.
Fechar conexão manualmente pode quebrar o controle transacional.

**Conforme:** (sem nenhuma chamada a fechar conexão)
```php
protected function cadastrarControlado($objDTO) {
    try {
        // operações...
    } catch (Exception $e) {
        throw new InfraException("Erro", $e);
    }
    // conexão fecha automaticamente ao fim do método
}
```

**Não conforme:**
```php
protected function cadastrarControlado($objDTO) {
    $this->getObjInfraIBanco()->fecharConexao(); // DISPARIDADE
}
```

---

## T5 — RN não chama BD de outra classe

**Severidade:** Erro
**Base:** Manual SEI MD §Arquitetura em Camadas

RN se comunica apenas com sua própria BD. Uma BD não pode chamar
outra BD. Para acessar lógica de outra entidade, a RN deve chamar
a RN correspondente (que por sua vez chama sua própria BD).

**Conforme:**
```php
class MdRiRestauranteRN extends InfraRN {

    protected function cadastrarControlado($objDTO) {
        // acessa apenas MdRiRestauranteBD
        $objBD = new MdRiRestauranteBD($this->getObjInfraIBanco());
        $objBD->cadastrar($objDTO);
    }
}
```

**Não conforme:**
```php
class MdRiRestauranteRN extends InfraRN {

    protected function cadastrarControlado($objDTO) {
        // acessa BD de outra entidade
        $objBD = new MdRiCardapioBD($this->getObjInfraIBanco()); // ERRO
    }
}
```

---

## T6 — try/catch com InfraException

**Severidade:** Erro
**Base:** Manual SEI MD §InfraException

Métodos RN devem tratar exceções com `try/catch` lançando `InfraException`.
Isso garante que erros sejam capturados e a transação properly cancelada.

**Conforme:**
```php
protected function cadastrarControlado($objDTO) {
    try {
        // lógica...
    } catch (Exception $e) {
        throw new InfraException("Erro ao cadastrar restaurante.", $e);
    }
}
```

**Não conforme:**
```php
protected function cadastrarControlado($objDTO) {
    // sem try/catch — exceção propagada sem contexto
}
```

---

## Matriz de severidade

| ID | Regra | Sev |
|----|-------|-----|
| T1 | Sufixo correto | **Erro** |
| T2 | inicializarObjInfraIBanco() | **Erro** |
| T3 | Sem encadeamento Controlado→Controlado | **Erro** |
| T4 | Sem fecharConexao() explícito | **Aviso** |
| T5 | RN não chama BD de outra classe | **Erro** |
| T6 | try/catch com InfraException | **Erro** |