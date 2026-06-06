# GitHub Copilot — Instrucoes

Leia `AGENTS.md` antes de qualquer sugestao — fonte autoritativa do projeto.

Guardrails criticos:
- PHP: encoding ISO-8859-1 obrigatorio; nunca UTF-8
- HTTP: proibido `$_REQUEST` e `$_GET` direto; usar `PaginaSEI::POST/GET`
- Acoes PHP: `validarLink()` + `validarPermissao()` obrigatorios no inicio
- `php -l` em todo arquivo PHP alterado antes de entregar
