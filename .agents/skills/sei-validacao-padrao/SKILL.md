---
name: sei-validacao-padrao
description: Validação padrão do SEI após implementação PHP ou alteração visual de interface, inclusive HTML, CSS, JS e componentes por hook. Abrange `php -l` quando houver PHP, auditores por artefato, análise estática aplicável, smoke e verificação dos esquemas de cores.
---

# Skill: Validação padrão do SEI

## Mínimo obrigatório quando há PHP alterado

Quando houver PHP alterado, rodar `php -l` em todos esses arquivos. Bloqueante se houver erro de sintaxe. Todo PHP novo ou alterado abre com `<?php`; arquivo legado que abre com `<?` recebe a troca da abertura antes do lint, porque com `short_open_tag=Off` o `php -l` trata o arquivo como texto e passa sem analisar. Sem PHP alterado, registre o lint PHP como não aplicável.

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
| Cadastro de tarefa (`TarefaDTO` ou `INSERT INTO tarefa`) | `python3 .agents/skills/sei-verificacao-tarefa/audit.py --input <script de release do módulo> --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |
| Controladores | `python3 .agents/skills/sei-verificacao-controladores/audit.py --input <path> --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |
| PHP de módulo SEI novo ou alterado (reuso do core) | `python3 .agents/skills/sei-direcionador-integracao/audit.py --exit-code` | 0=PASS, 1=WARN, 2=BLOCK |

Acione cada auditor somente quando o artefato correspondente existir no
escopo. Todos falham de forma fechada: entrada inexistente, tipo incompatível,
diretório sem artefato elegível ou parser sem extração retornam `BLOCK` e exit
code 2. `PASS` exige ao menos um artefato analisado; não existe opção para
aceitar cobertura vazia.

## Recomendações (quando disponíveis no projeto ou no módulo)

```bash
composer install   # se existir composer.json
composer test      # phpunit
composer lint      # phpcs
composer stan      # phpstan
```

## Análise estática com PHPStan (quando houver configuração no projeto ou no módulo)

A configuração existente é a de `trf4/julgamento/.ci/phpstan.neon`. Ela exige o pacote privado `trf4/phpstan-infraphp`, que o CI do TRF4 clona com `CI_JOB_TOKEN` (`.gitlab-ci.yml` do módulo), e os fontes do core nos caminhos de `scanDirectories` do `phpstan.neon`.

```bash
cd fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento/.ci
composer install --no-interaction --prefer-dist   # falha sem o pacote privado em ./phpstan-infraphp
vendor/bin/phpstan analyse -c phpstan.neon
```

Sem o pacote ou sem os fontes do core, registrar a análise estática como verificação pendente, nunca como executada.

## Interface visual

Para interface criada ou alterada, inclusive HTML, CSS, JS e componentes por hook sem PHP alterado, aplique `.agents/references/padrao-acessibilidade-cores-sei.md`. Registre a cobertura dos esquemas e das superfícies afetadas separadamente do resultado dos auditores estáticos; sem evidência suficiente, informe a verificação pendente.

## Smoke manual (sempre que mexer em UI/ação)

Cenários mínimos a testar. Para página ou ação PHP criada ou alterada, mantenha os cenários abaixo conforme os gates do artefato. Quando não houver página nem ação PHP criada ou alterada e a mudança for apenas visual, identifique os caminhos de ação, permissão, link, entrada e sessão afetados; quando um cenário não tiver relação com a mudança, registre-o como não aplicável com o motivo.

1. **Cenário principal**: fluxo happy path funciona
2. **Sem permissão**: usuário sem recurso recebe erro de autorização
3. **Link inválido**: em sessão de teste isolada, confirme que o hash adulterado é recusado com mensagem de link ou hash inválido, conforme a versão do SEI; se não houver isolamento, registre o cenário como pendente
4. **Parâmetros inválidos**: tipo/tamanho errado não causa crash
5. **Sessão expirada**: em sessão de teste isolada, confirme o redirecionamento para login; se não houver isolamento, registre o cenário como pendente
6. **Foco, Enter, atalhos e ordenação**: em tela com filtro, formulário, barra de comandos ou grid criado ou alterado, execute a seção "Verificação" de `.agents/references/padrao-interacao-telas-sei.md` no navegador

## PHP 8 e InfraErroPHP (diagnóstico)

- Warnings comuns (ex.: acesso a índice inexistente) podem virar erro.
- Em dev, pode-se configurar tratamento via grupo `InfraErroPHP` no `ConfiguracaoSEI.php` e consultar ocorrências em **Infra > Erros do PHP** (`infra_erro_php`).

## Debug desligado

Debug ligado para depurar não chega à entrega, porque compromete desempenho e segurança. Confira as linhas PHP acrescentadas pelo diff:

```bash
git diff -U0 HEAD -- '*.php' | grep -anE '^\+.*(setBolLigado\(true\)|setBolDebugInfra\(true\)|setBolEcho\(true\)|montarAreaDebug\(\))'
```

Cada linha encontrada sai da entrega ou volta a ficar comentada, como no modelo de página do manual. A exceção é o agendamento que liga o debug para gravar o resultado com `LogSEI`, com `setBolDebugInfra(false)` e `setBolEcho(false)`, no padrão dos agendamentos do módulo.

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

## Dependências de registros do core

Exija evidência do caminho real do core com FK física quando aplicável; invocar o hook isoladamente não comprova alcance nem rollback. Aplicar, com `sei-guardrails-modulo`, a [matriz de proteção](../sei-mod-api-eventos/references/protecao-dependencias-core.md) também a protocolos e dependências funcionais sem FK.
