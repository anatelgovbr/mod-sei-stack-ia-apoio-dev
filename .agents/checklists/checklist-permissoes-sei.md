# Checklist de Permissoes SEI

Checklist operacional para revisar autenticacao, autorizacao, link assinado e
recursos SIP em modulos SEI.

## Fontes de verdade

- `.agents/references/gates-de-implementacao.md` - `G3`, `G4`, `G8`, `G9`, `D1`
- `.agents/security/matriz-vulnerabilidades-sei.md` - `V01`, `V02`, `V03`
- `.agents/checklists/checklist-seguranca.md` - secoes `1.1`, `1.2`, `1.4`, `1.6`
- `.agents/skills/sei-verificacao-pagina/SKILL.md`
- `.agents/skills/sei-verificacao-controladores/SKILL.md`

## Quando usar

- paginas `*_lista.php`, `*_cadastro.php`
- handlers de salvar, excluir, desativar e reativar
- `*Integracao.php` com AJAX ou WebServices
- revisao de recursos SIP e menus internos

## Checklist operacional

| # | Item | Origem | Severidade |
|---|---|---|---|
| 1 | A pagina inicia com `validarLink()` | `V01`, `G3`, `P1` | BLOQUEANTE |
| 2 | A pagina inicia com `validarPermissao()` ou `validarAuditarPermissao()` apos `validarLink()` | `V02`, `G3`, `P2` | BLOQUEANTE |
| 3 | Toda acao de escrita usa link assinado com `assinarLink()` | `G4`, `P4` | BLOQUEANTE |
| 4 | UI condicional usa `verificarPermissao()` para esconder acoes nao autorizadas | `P7` | ALTA |
| 5 | `processarControladorAjax*()` e `processarControladorWebServices()` validam permissao especifica por acao ou servico | `V03`, `G8`, `A2`, `A5`, `CI4` | BLOQUEANTE |
| 6 | `tratarLinkSemAssinatura()` usa regra restritiva e nao abre rota arbitraria | `G8`, `A3`, `CI1` | BLOQUEANTE |
| 7 | Fluxos de escrita nao dependem apenas da tela; a camada executora mantem validacao de permissao quando aplicavel | nota `P2`, `L3` | ALTA |
| 8 | Recurso SIP correspondente existe e o nome segue `md_<sigla>_<acao>` | `D1` | BLOQUEANTE |
| 9 | Escrita via GET esta ausente ou fortemente justificada; preferir POST assinado | `G9`, `P10` | ALTA |

## Evidencias que costumam aparecer

- pagina com `validarLink()` mas sem `validarPermissao()`
- pagina com permissao comentada
- handler `*_salvar.php` validando apenas link
- RN de escrita com `validarAuditarPermissao()` comentado ou ausente
- dispatch de AJAX fazendo apenas `switch` sem checagem de permissao por caso
