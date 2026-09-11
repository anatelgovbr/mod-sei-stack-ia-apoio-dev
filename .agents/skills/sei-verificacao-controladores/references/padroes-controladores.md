# Padroes de Controladores de Integracao — Referencia Resumida

Curado a partir dos contratos do SEI para `*Integracao.php`.
Fonte original: `sei_modulos_manual_dev_9_eventos.md` secoes 1363, 1442 e 1648.

## CI1 — `tratarLinkSemAssinatura()`

Deve usar `preg_match` restritivo sobre a acao recebida.
Nunca aceitar qualquer string sem validacao de formato.

```php
public function tratarLinkSemAssinatura() {
    $strAcao = PaginaSEI::GET('acao', 'string');
    if (!preg_match('/^md_<sigla>_[a-z_]+$/', $strAcao)) {
        throw new InfraException('Acao invalida.');
    }
    // dispatch explicito por acao
}
```

## CI2 — `processarControladorWebServices()`

Dispatch explicito por servico — cada servico mapeado individualmente.
Nunca usar call dinamico ou `eval`.

```php
public function processarControladorWebServices() {
    $strServico = PaginaSEI::GET('servico', 'string');
    switch ($strServico) {
        case 'md_<sigla>_servico_a': $this->servicoA(); break;
        case 'md_<sigla>_servico_b': $this->servicoB(); break;
        default: throw new InfraException('Servico nao reconhecido.');
    }
}
```

## CI3 — `processarControladorAjax()` / `processarControladorAjaxExterno()`

Dispatch explicito por acao — cada case valida permissao especifica antes de executar.
Validacao global no pai nao substitui validacao por acao.

```php
public function processarControladorAjax() {
    $strAcao = PaginaSEI::GET('acao', 'string');
    switch ($strAcao) {
        case 'md_<sigla>_listar':
            SessaoSEI::getInstance()->validarPermissao('md_<sigla>_listar');
            $this->listar();
            break;
        default:
            throw new InfraException('Acao nao reconhecida.');
    }
}
```

## CI4 — Autorizacao por acao/servico sensivel

Cada acao ou servico que altere estado ou retorne dado sensivel deve chamar
`validarPermissao()` especifica antes de executar — nao depender de gate global.

## CI5 — Payload sensivel em retorno

Evitar retornar em AJAX campos sensiveis (senhas, tokens, chaves) mesmo que
o usuario tenha permissao para a acao.

## CI6 - Contrato de entrada e saida de cada controlador

O dispatch de CI2 e CI3 depende de receber o parametro certo, entao o nome do parametro faz parte da regra.

| Metodo | Parametro recebido | Origem |
|---|---|---|
| `processarControlador()` | `$strAcao`, acao recebida na URL | manual 9, processarControlador |
| `processarControladorExterno()` | `$strAcao`, acao recebida na URL | manual 9, processarControladorExterno |
| `processarControladorPublicacoes()` | `$strAcao`, acao recebida na URL | manual 9, processarControladorPublicacoes |
| `processarControladorAjax()` | `$strAcaoAjax`, acao ajax recebida na URL | manual 9, processarControladorAjax |
| `processarControladorAjaxExterno()` | `$strAcaoAjax`, acao ajax recebida na URL | manual 9, processarControladorAjaxExterno |
| `processarControladorWebServices()` | `$strServico`, servico recebido na URL | manual 9, processarControladorWebServices |
| `tratarLinkSemAssinatura()` | `$strLink`, link sem assinatura para redirecionamento automatico | manual 9, tratarLinkSemAssinatura |
| `validarLoginUsuarioExterno()` | `$objUsuarioAPI` com IdUsuario, Sigla, Nome e StaTipo | manual 9, validarLoginUsuarioExterno |

Retornos obrigatorios:

- `tratarLinkSemAssinatura()` devolve `$bolValido`, booleano true ou false. Nao devolve o link tratado.
- `validarLoginUsuarioExterno()` devolve booleano.

## CI7 - URL de referencia do WSDL

O WebService do modulo e publicado em `https://[servidor]/sei/controlador_ws.php?servico=[nome do servico do modulo]`.

O nome do servico na URL e o mesmo valor que `processarControladorWebServices()` recebe em `$strServico`, entao o dispatch de CI2 precisa cobrir exatamente os nomes publicados.
