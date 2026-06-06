# Matriz de Vulnerabilidades — Ecossistema SEI

Vetores de ataque especificos do SEI/InfraPHP. Cada entrada tem padrao vulneravel e seguro para deteccao e correcao.

**Gates**: `.agents/references/implementation-gates.md`
**Skills**: `sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-controladores`

---

## V01 — Acao PHP sem validarLink (CSRF)

**Severidade**: BLOQUEANTE | **Gate**: G3 | **Skill**: `sei-verificacao-pagina` P1

Arquivo PHP de acao sem `validarLink()` no inicio — permite URLs forjadas no contexto do usuario.

```php
// VULNERAVEL
$objDTO->setNumId(PaginaSEI::GET('id', 'int'));

// SEGURO
SessaoSEI::getInstance()->validarLink();
SessaoSEI::getInstance()->validarPermissao('md_ri_listar');
$objDTO->setNumId(PaginaSEI::GET('id', 'int'));
```

---

## V02 — Acao PHP sem validarPermissao (Escalada de Privilegio)

**Severidade**: BLOQUEANTE | **Gate**: G3 | **Skill**: `sei-verificacao-pagina` P2

`validarLink()` sem `validarPermissao()` — link valido, qualquer usuario executa.

```php
// VULNERAVEL
SessaoSEI::getInstance()->validarLink();
$objRN->excluirControlado($objDTO); // sem validarPermissao

// SEGURO
SessaoSEI::getInstance()->validarLink();
SessaoSEI::getInstance()->validarPermissao('md_ri_adm_excluir');
$objRN->excluirControlado($objDTO);
```

---

## V03 — Acao AJAX sem autorizacao por acao (Autorizacao Insuficiente)

**Severidade**: BLOQUEANTE | **Skill**: `sei-verificacao-controladores` A1

O controlador global valida link mas nao impoe permissao por acao do modulo.

```php
// VULNERAVEL
case 'md_ri_consultar_cpf':
    $objRN = new MdRiConsultaRN();
    return $objRN->consultarCpf(...);

// SEGURO
case 'md_ri_consultar_cpf':
    SessaoSEI::getInstance()->validarPermissao('md_ri_consultar');
    $objRN = new MdRiConsultaRN();
    return $objRN->consultarCpf(...);
```

---

## V04 — XSS via saida sem escape

**Severidade**: ALTA | **Gate**: G6 | **Skill**: `sei-verificacao-pagina` P7

InfraPHP nao faz escape automatico. Saida sem `PaginaSEI::tratarHTML()` abre XSS.

```php
// VULNERAVEL
echo '<td>' . $objDTO->getStrNome() . '</td>';

// SEGURO
echo '<td>' . PaginaSEI::tratarHTML($objDTO->getStrNome()) . '</td>';
```

---

## V05 — SQL Injection via concatenacao

**Severidade**: BLOQUEANTE | **Gate**: G6

Concatenacao de entrada em SQL customizado dentro de `*BD.php`.

```php
// VULNERAVEL
$strSQL = "SELECT * FROM md_ri_cadastro WHERE str_nome LIKE '%" . $strBusca . "%'";

// SEGURO — normalizar e limitar antes de usar como criterio
$strNome = substr(trim(PaginaSEI::GET('str_nome', 'string')), 0, 100);
$objDTO->adicionarCriterio(array('StrNome'), array(InfraDTO::$OPER_IGUAL), array($strNome));
```

---

## V06 — Uso de $_REQUEST

**Severidade**: ALTA | **Gate**: G5

`$_REQUEST` mescla GET/POST/COOKIE sem distinguir origem. Usar `PaginaSEI::GET/POST` com tipo.

```php
// VULNERAVEL
$numId = $_REQUEST['id'];

// SEGURO
$numId = PaginaSEI::GET('id', 'int');
```

---

## V07 — Efeito colateral dentro de transacao

**Severidade**: ALTA | **Skill**: `sei-verificacao-rn`

Efeitos colaterais (email, Solr, API externa) dentro do bloco transacional — se falharem, desfazem toda a persistencia.

```php
// VULNERAVEL — email dentro da transacao
protected function gerarProcedimentoControlado($arr) {
    $retorno = $this->gerarProcedimentoInterno($arr);
    $rn = new MdRiEmailRN();
    $rn->notificar($retorno); // falha desfaz processo
    return $retorno;
}

// SEGURO — efeito colateral apos persistencia
protected function gerarProcedimentoControlado($arr) {
    $retorno = $this->gerarProcedimentoInterno($arr);
    try {
        (new MdRiEmailRN())->notificar($retorno['email']);
    } catch (Exception $e) { /* nao desfaz processo */ }
    return $retorno['recibo'];
}
```

---

## V08 — Encoding UTF-8 em arquivo PHP

**Severidade**: BLOQUEANTE | **Gate**: G1 | **Skill**: `sei-verificacao-pagina` P10

SEI opera em ISO-8859-1. UTF-8 causa corrupcao silenciosa de strings com acentos.

Deteccao: `file -i arquivo.php` deve indicar `charset=iso-8859-1`.

---

## V09 — Exposicao de stacktrace

**Severidade**: ALTA | **Gate**: G7

Excecao com `getMessage()` ou stack exibido na resposta HTTP expoe paths, classes e queries.

```php
// VULNERAVEL
catch (Exception $e) { echo $e->getTraceAsString(); }

// SEGURO
catch (Exception $e) {
    InfraLog::registrarLog(InfraLog::$TIPO_ERRO, __METHOD__, $e->getMessage());
    throw new InfraException('Erro ao processar operacao.');
}
```

---

## V10 — Log com PII ou segredos

**Severidade**: BLOQUEANTE | **Gate**: G8

PII (CPF, email) ou segredos (tokens, senhas) em logs viola LGPD e cria vetor persistente.

```php
// VULNERAVEL
LogSEI::registrarLog(..., 'Usuario ' . $strCpf . ' token ' . $strToken);

// SEGURO
LogSEI::registrarLog(..., 'Operacao realizada. ID: ' . $numIdInterno);
```

---

## Indice por Severidade

| BLOQUEANTE | ALTA |
|---|---|
| V01 Sem validarLink | V04 XSS sem escape |
| V02 Sem validarPermissao | V06 $_REQUEST |
| V03 AJAX sem autorizacao | V07 Efeito colateral em transacao |
| V05 SQL Injection | V09 Stacktrace exposto |
| V08 Encoding UTF-8 | |
| V10 Log com PII/segredos | |
