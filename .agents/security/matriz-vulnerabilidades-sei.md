# Matriz de Vulnerabilidades do Ecossistema SEI

Vetores de ataque especificos do SEI/InfraPHP. Cada entrada tem padrao vulneravel e seguro para deteccao e correcao.

Severidade do risco e estado do gate seguem `.agents/references/gates-de-implementacao.md`, regras 5 e 6.

**Gates base**: `.agents/references/gates-de-implementacao.md`
**Checklist operacional**: `.agents/checklists/checklist-seguranca.md`
**Skills**: `sei-verificacao-pagina`, `sei-verificacao-rn`, `sei-verificacao-banco-dados`, `sei-verificacao-controladores`

---

## V01: Acao PHP sem validarLink (CSRF)

**Severidade**: BLOQUEANTE | **Estado confirmado**: `BLOCK` | **Gate**: G3 | **Skill**: `sei-verificacao-pagina` P1

Arquivo PHP de acao sem `validarLink()` no inicio permite URLs forjadas no contexto do usuario.

```php
// VULNERAVEL
$objDTO->setNumId(PaginaSEI::GET('id', 'int'));

// SEGURO
SessaoSEI::getInstance()->validarLink();
SessaoSEI::getInstance()->validarPermissao('md_ri_listar');
$objDTO->setNumId(PaginaSEI::GET('id', 'int'));
```

---

## V02: Acao PHP sem validarPermissao (Escalada de Privilegio)

**Severidade**: BLOQUEANTE | **Estado confirmado**: `BLOCK` | **Gate**: G3 | **Skill**: `sei-verificacao-pagina` P2

`validarLink()` sem `validarPermissao()` deixa o link valido executavel por qualquer usuario.

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

## V03: Acao AJAX sem autorizacao por acao (Autorizacao Insuficiente)

**Severidade**: BLOQUEANTE | **Estado confirmado**: `BLOCK` | **Gate**: G8 | **Skill**: `sei-verificacao-controladores` CI4

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

## V04: XSS via saida sem escape

**Severidade**: ALTA | **Estado confirmado**: `BLOCK` | **Gate**: G7 | **Skill**: `sei-verificacao-pagina` P8/P9

InfraPHP nao faz escape automatico. Saida sem `PaginaSEI::tratarHTML()` abre XSS.
P8 retorna `BLOCK` quando a saida dinamica sem tratamento for confirmada. P9
retorna `BLOCK` somente quando fonte dinamica e sink inseguro forem confirmados;
heuristica inconclusiva retorna `WARN`.

```php
// VULNERAVEL
echo '<td>' . $objDTO->getStrNome() . '</td>';

// SEGURO
echo '<td>' . PaginaSEI::tratarHTML($objDTO->getStrNome()) . '</td>';
```

---

## V05: SQL Injection via concatenacao

**Severidade**: BLOQUEANTE | **Estado confirmado**: `BLOCK` | **Checklist**: B6

Concatenacao de entrada em SQL customizado dentro de `*BD.php`.

```php
// VULNERAVEL
$strSQL = "SELECT * FROM md_ri_cadastro WHERE str_nome LIKE '%" . $strBusca . "%'";

// SEGURO: normalizar e limitar antes de usar como criterio
$strNome = substr(trim(PaginaSEI::GET('str_nome', 'string')), 0, 100);
$objDTO->adicionarCriterio(array('StrNome'), array(InfraDTO::$OPER_IGUAL), array($strNome));
```

---

## V06: Uso de $_REQUEST

**Severidade**: ALTA | **Estado confirmado**: `BLOCK` | **Gate**: G5 | **Skill**: `sei-verificacao-pagina` P5/P6

`$_REQUEST` mescla GET/POST/COOKIE sem distinguir origem. O mesmo gate cobre
`$_GET` e `$_POST` diretos sem normalizacao explicita. Usar
`PaginaSEI::GET/POST` com tipo.

```php
// VULNERAVEL
$numId = $_REQUEST['id'];

// SEGURO
$numId = PaginaSEI::GET('id', 'int');
```

---

## V07: Efeito colateral dentro de transacao

**Severidade**: ALTA | **Estado confirmado**: `BLOCK` | **Gate RN**: T6 | **Skill**: `sei-verificacao-rn`

Efeitos colaterais (email, Solr, API externa) dentro do bloco transacional podem
desfazer toda a persistencia. O metodo `*Controlado` deve conter apenas
persistencia. Efeitos externos ocorrem no wrapper publico somente depois do
retorno de `*Controlado`.

Exemplo vulneravel, exemplo seguro e as tres tecnicas do wrapper estao em `.agents/skills/sei-verificacao-rn/references/padroes-transacao.md`, regra T6, que o `AGENTS.md` nomeia como template.

---

## V08: Encoding incompativel com a conversao Latin-1 em arquivo PHP

**Severidade**: BLOQUEANTE | **Estado confirmado**: `BLOCK` | **Gate**: G1 | **Skill**: revisao de PHP alterado

SEI opera com conversao para ISO-8859-1 no blob final. BOM ou caractere fora de Latin-1
causa corrupcao silenciosa de strings com acentos.

Deteccao: validar ausencia de BOM e ausencia de caracteres fora de Latin-1 no blob final,
considerando a conversao definida em `.gitattributes`. Worktree UTF-8, por si so, nao
caracteriza achado.

---

## V09: Exposicao de stacktrace

**Severidade**: ALTA | **Estado sem gate bloqueante especifico**: `WARN`

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

## V10: Log com PII ou segredos

**Severidade**: BLOQUEANTE para segredos; ALTA para PII | **Estado**: `BLOCK` para segredo confirmado; `WARN` para PII isolada | **Checklist**: L1/L2

PII (CPF, email) ou segredos (tokens, senhas) em logs viola LGPD e cria vetor persistente.

```php
// VULNERAVEL
LogSEI::getInstance()->gravar('Usuario ' . $strCpf . ' token ' . $strToken, InfraLog::$INFORMACAO);

// SEGURO
LogSEI::getInstance()->gravar('Operacao realizada. ID: ' . $numIdInterno, InfraLog::$INFORMACAO);
```

---

## Indice por Severidade

| BLOQUEANTE | ALTA |
|---|---|
| V01 Sem validarLink | V04 XSS sem escape |
| V02 Sem validarPermissao | V06 $_REQUEST |
| V03 AJAX sem autorizacao | V07 Efeito colateral em transacao |
| V05 SQL Injection | V09 Stacktrace exposto |
| V08 Encoding incompativel com Latin-1 | |
| V10 Log com PII/segredos | |
