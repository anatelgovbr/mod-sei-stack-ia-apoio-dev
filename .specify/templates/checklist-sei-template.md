# Checklist de Validacao Tecnica SEI — [FEATURE]

**Feature**: [FEATURE] | **Data**: [DATE] | **Responsavel**: [AUTOR]

> Este checklist valida aderencia tecnica ao padrão SEI antes de considerar
> a entrega concluida. Deve ser preenchido apos a implementacao e antes do merge.
> Nao confundir com o checklist de qualidade de requisitos gerado por
> `/speckit.checklist` — aquele valida os requisitos; este valida a entrega tecnica.
>
> Fonte de verdade para cada item: `AGENTS.md` (Guardrails Universais e Qualidade Minima),
> `docs/manual_desenvolvimento_md/` e `.agents/references/implementation-gates.md`.

---

## 1. Encoding e Sintaxe

- [ ] Todos os arquivos PHP alterados ou gerados estao **compativeis com a conversao para ISO-8859-1 (Latin-1) via `.gitattributes`** — sem BOM e sem caracteres fora de Latin-1
- [ ] `php -l` executado em todos os arquivos PHP alterados — zero erros de sintaxe
- [ ] Nenhum BOM (Byte Order Mark) nos arquivos PHP

## 2. Permissao e Link Assinado

- [ ] Toda acao PHP tem `validarLink()` no inicio
- [ ] Toda acao PHP tem `validarPermissao()` apos `validarLink()`
- [ ] Links de acao em paginas usam `assinarLink()`
- [ ] Renderizacao condicional de UI usa `verificarPermissao()`
- [ ] Recurso SIP correspondente existe (`md_<inst/mod>_<acao>`)

## 3. Entrada HTTP

- [ ] Nenhum uso de `$_REQUEST` — proibido sem justificativa documentada
- [ ] Entradas HTTP via `PaginaSEI::POST()` ou `PaginaSEI::GET()` com normalizacao de tipo
- [ ] Parametros normalizados com whitelist ou regex antes do uso
- [ ] Saida HTML via `PaginaSEI::tratarHTML()` ou equivalente (sem XSS)

## 4. Transacoes e Consistencia

- [ ] Toda escrita relevante em BD usa `BancoSEI` ou `InfraRN *Controlado`
- [ ] Efeitos colaterais (email, Solr, sistemas externos) ocorrem **apos** o commit, nao dentro da transacao
- [ ] Nenhuma operacao de indexacao (Solr) dentro de transacao critica sem justificativa registrada

## 5. Seguranca

- [ ] Nenhuma concatenacao insegura em SQL (sem parametros ou prepared statements onde aplicavel)
- [ ] Nenhuma concatenacao insegura em HTML, JS ou URLs
- [ ] Stacktrace nao exposto ao usuario final
- [ ] Logs sem PII (dados pessoais) e sem segredos
- [ ] Nenhuma mudanca fora do escopo `modulos/**` sem proposta formal registrada

## 6. Banco de Dados e Release

- [ ] DDL usa tipos portaveis (MySQL, PostgreSQL, Oracle, SQL Server)
- [ ] Sequences criadas com `criarSequencialNativa` (sem `AUTO_INCREMENT` direto)
- [ ] Nomes de tabelas, colunas, indices e sequences respeitam limite de 30 chars (ideal: 26)
- [ ] Script de instalacao/upgrade SEI criado ou atualizado (se houver mudanca em BD)
- [ ] Script de instalacao/upgrade SIP criado ou atualizado (se houver mudanca em recursos/menus/perfis)
- [ ] `getVersao()` em `*Integracao.php` sincronizado com os scripts SEI e SIP
- [ ] Nenhum script duplicado — verificado em `.agents/references/mapa-modulos-scripts.md`

## 7. Assets e Estrutura de Modulo

- [ ] Arquivos CSS: se `css/` ja tem arquivos, editou o existente — nao criou novo
- [ ] Arquivos JS: se `js/` ja tem arquivos, editou o existente — nao criou novo
- [ ] Camadas respeitadas: `dto/`, `rn/`, `bd/`, `int/`, paginas na raiz do modulo
- [ ] `ConfiguracaoSEI.php` nao foi editado (apenas referenciado)

## 8. CRUD Generator (quando aplicavel)

- [ ] Contrato JSON salvo em `specs/<feature>/crud-contratos/<tabela>.json`
- [ ] Gerador executado via `generate_from_contrato.py` — nao escrita manual do CRUD base
- [ ] Arquivos gerados reorganizados: `*DTO.php` em `dto/`, `*BD.php` em `bd/`, `*RN.php` em `rn/`, `*INT.php` em `int/`
- [ ] `php -l` nos 6 arquivos gerados — zero erros

## 9. Andamentos (quando aplicavel)

- [ ] `id_tarefa` do modulo usa prefixo `MD_<SIGLA>` (nunca valor < 1000, exceto ID_TAREFA=65)
- [ ] Variaveis de andamento declaradas com `@VAR@`

## 10. Testes e Evidencias

- [ ] Cenario principal testado manualmente
- [ ] Cenarios negativos testados: sem permissao, link invalido, parametros invalidos, sessao expirada
- [ ] Evidencias de teste registradas (PR, README do modulo ou `specs/<feature>/`)
- [ ] Se disponivel: `composer test` / `phpcs` / `phpstan` executados sem falhas criticas

## 11. Validações Técnicas Automatizadas

> Execute as skills de validacao para verificar conformidade tecnica.
> Evidencias geradas em `/tmp/sei-sdd-validacoes/` (nao commitadas).

### Rotas Canonicas

```bash
mkdir -p /tmp/sei-sdd-validacoes/
python3 .agents/skills/sei-verificacao-pagina/audit.py --input <modulo> --format json > /tmp/sei-sdd-validacoes/pagina-seguranca.json
python3 .agents/skills/sei-verificacao-rn/audit.py --input <modulo>/rn --format json > /tmp/sei-sdd-validacoes/rn-transacao.json
python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input <modulo>/dto --format json > /tmp/sei-sdd-validacoes/banco-dados.json
python3 .agents/skills/sei-verificacao-tarefa/audit.py --input <modulo>/scripts --format json > /tmp/sei-sdd-validacoes/tarefa-modulo.json
python3 .agents/skills/sei-verificacao-controladores/audit.py --input <modulo> --format json --output /tmp/sei-sdd-validacoes/

| sei-verificacao-pagina | | [ ] PASS / [ ] WARN / [ ] BLOCK | |
| sei-verificacao-rn | | [ ] PASS / [ ] WARN / [ ] BLOCK | |
| sei-verificacao-banco-dados | | [ ] PASS / [ ] WARN / [ ] BLOCK | |
| sei-verificacao-tarefa | | [ ] PASS / [ ] WARN / [ ] BLOCK | |
| sei-verificacao-controladores | | [ ] PASS / [ ] WARN / [ ] BLOCK | |
| sei-sql-injection-check (opcional) | | [ ] PASS / [ ] WARN / [ ] BLOCK | |
| sei-data-exposure-check (opcional) | | [ ] PASS / [ ] WARN / [ ] BLOCK | |

**Veredito Final**: [ ] PASS — todas as validações OK | [ ] BLOCK — corrija erros antes de prosseguir

---

## Resultado

| Secao | Status | Observacoes |
| ----- | ------ | ----------- |
| 1. Encoding e Sintaxe | [ ] OK / [ ] BLOQUEADO | |
| 2. Permissao e Link Assinado | [ ] OK / [ ] BLOQUEADO | |
| 3. Entrada HTTP | [ ] OK / [ ] BLOQUEADO | |
| 4. Transacoes e Consistencia | [ ] OK / [ ] BLOQUEADO | |
| 5. Seguranca | [ ] OK / [ ] BLOQUEADO | |
| 6. BD e Release | [ ] OK / [ ] BLOQUEADO | |
| 7. Assets e Estrutura | [ ] OK / [ ] BLOQUEADO | |
| 8. CRUD Generator | [ ] OK / [ ] N/A | |
| 9. Andamentos | [ ] OK / [ ] N/A | |
| 10. Testes e Evidencias | [ ] OK / [ ] BLOQUEADO | |
| 11. Validações Automatizadas | [ ] OK / [ ] BLOQUEADO | |

**Entrega liberada para merge?** [ ] Sim — todos os itens aplicaveis OK | [ ] Nao — ver itens BLOQUEADOS acima
