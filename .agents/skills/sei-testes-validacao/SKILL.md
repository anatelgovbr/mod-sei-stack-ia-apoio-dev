---
name: sei-testes-validacao
description: Checagens e testes para módulos SEI (lint PHP obrigatório; checks opcionais do módulo). Inclui dicas para capturar warnings do PHP 8 via InfraErroPHP em ambiente de desenvolvimento.
---

# Skill: Testes e validações

## Mínimo obrigatório (sempre)

Rodar `php -l` em todos os arquivos PHP alterados. Bloqueante se houver erro de sintaxe.

```bash
# Exemplo: validar todos os PHP de um módulo
find fontes/sei/src/main/php/sei/web/modulos/<modulo>/ -name "*.php" -exec php -l {} \; 2>&1 | grep -v "No syntax errors"

# Exemplo: validar apenas os arquivos alterados no commit
git diff --name-only HEAD~1 -- '*.php' | xargs -I{} php -l {}
```

Exit code: `0` = PASS, qualquer outro = BLOCK.

## Checks automatizados do módulo (quando aplicáveis)

Executar na seguinte ordem quando os artefatos existirem:

| Artefato alterado | Comando de validação | Exit codes (`--exit-code`) |
|---|---|---|
| Páginas PHP | `python3 .agents/skills/sei-verificacao-pagina/audit.py --input <path> --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |
| Classes RN | `python3 .agents/skills/sei-verificacao-rn/audit.py --input <path> --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |
| DTO/BD/DDL | `python3 .agents/skills/sei-verificacao-banco-dados/audit.py --input <path> --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |
| Scripts de tarefa | `python3 .agents/skills/sei-verificacao-tarefa/audit.py --input <path> --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |
| Controladores | `python3 .agents/skills/sei-verificacao-controladores/audit.py --input <path> --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |

Acione cada auditor somente quando o artefato correspondente existir no
escopo. Todos falham de forma fechada: entrada inexistente, tipo incompatível,
diretório sem artefato elegível ou parser sem extração retornam `BLOCK` e exit
code 2. `PASS` exige ao menos um artefato analisado; não existe opção para
aceitar cobertura vazia.

## Recomendações (quando disponíveis no módulo)

```bash
composer install   # se existir composer.json
composer test      # phpunit
composer lint      # phpcs
composer stan      # phpstan
```

## Smoke manual (sempre que mexer em UI/ação)

Cenários mínimos a testar:

1. **Cenário principal**: fluxo happy path funciona
2. **Sem permissão**: usuário sem recurso recebe erro de autorização
3. **Link inválido**: hash adulterado retorna "Link Inválido"
4. **Parâmetros inválidos**: tipo/tamanho errado não causa crash
5. **Sessão expirada**: redireciona para login

## PHP 8 e InfraErroPHP (diagnóstico)

- Warnings comuns (ex.: acesso a índice inexistente) podem virar erro.
- Em dev, pode-se configurar tratamento via grupo `InfraErroPHP` no `ConfiguracaoSEI.php` e consultar ocorrências em **Infra > Erros do PHP** (`infra_erro_php`).

## Critérios de resultado

| Resultado | Significado | Ação |
|---|---|---|
| PASS (exit 0) | Todos os checks verdes | Prosseguir |
| WARN (exit 1) | Avisos sem bloqueio | Registrar e decidir |
| BLOCK (exit 2) | Erros bloqueantes | Corrigir antes de entregar |

## Saída esperada

Registro do que foi validado (comandos executados + evidência de smoke) no PR ou no README do módulo.

## InfraErroPHP: warnings ignorados e registro de erro

Por padrao o SEI **ignora** os erros `$W_UNDEFINED_ARRAY_KEY`, `$W_UNDEFINED_VARIABLE`, `$W_UNDEFINED_PROPERTY` e equivalentes. Em desenvolvimento isso esconde defeito real de codigo PHP 8.

Para ver esses warnings durante o desenvolvimento, ajustar o grupo `InfraErroPHP` no `ConfiguracaoSEI.php` do ambiente local, nunca no ambiente compartilhado.

Quando o tratamento `InfraErroPHP::$T_REGISTRAR` estiver ativo, o erro e gravado na tabela `infra_erro_php`, consultavel pelo menu correspondente. Conferir essa tabela apos rodar o fluxo e parte do smoke de um modulo novo.
