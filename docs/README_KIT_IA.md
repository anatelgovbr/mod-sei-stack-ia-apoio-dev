# Kit de Apoio por IA — Desenvolvimento de Módulos SEI

Este guia mostra como usar IA neste projeto de forma simples e prática.

## Resumo rápido

- a recomendação padrão do projeto é usar **GitHub Copilot no VS Code**
- o **GitHub Copilot CLI** também funciona; use `/agents` para acessar o SpecKit no terminal
- o **OpenCode** também é suportado
- todas as ferramentas usam o contexto do repositório
- as integrações deste repositório já estão configuradas
- para começar, basta instalar a ferramenta, autenticar sua conta e abrir o projeto
- não é necessário rodar `init` ou reinicializar a stack de IA do repositório
- o fluxo **SpecKit** é opcional
- para tarefas pequenas, o fluxo direto costuma ser suficiente

## Compatibilidade

| Ambiente | O que esperar |
| --- | --- |
| GitHub Copilot no VS Code ou em IDE compatível | Usa o contexto do projeto e pode mostrar os comandos `/speckit.*` |
| GitHub Copilot CLI | Usa o contexto do projeto; para o SpecKit, use `/agents` para selecionar o agent desejado — os comandos `/speckit.*` são exclusivos do VS Code |
| OpenCode | Também usa o contexto do projeto e executa os comandos `/speckit.*` |

## Onde baixar e instalar

Use sempre a documentação oficial das ferramentas.

### GitHub Copilot

- Documentação geral: [GitHub Copilot Docs](https://docs.github.com/en/copilot)
- GitHub Copilot CLI: [Installing GitHub Copilot CLI](https://docs.github.com/en/copilot/how-tos/set-up/install-copilot-cli)
- Extensão do GitHub Copilot para VS Code: [GitHub Copilot](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot)
- Extensão de chat para VS Code: [GitHub Copilot Chat](https://marketplace.visualstudio.com/items?itemName=GitHub.copilot-chat)

### OpenCode

- Documentação oficial: [OpenCode Docs](https://opencode.ai/docs)
- Repositório oficial: [anomalyco/opencode](https://github.com/anomalyco/opencode)

## Como começar com GitHub Copilot

Depois de instalar e autenticar a ferramenta, abra o repositório no editor e use o chat normalmente.

Neste projeto, o Copilot já está configurado para usar o contexto do repositório.

Você não precisa inicializar nada no projeto para começar a usar o Copilot.

Recomendação prática:

- use preferencialmente o **GitHub Copilot no VS Code**
- se você optar pelo **GitHub Copilot CLI**, use `/agents` para invocar o SpecKit — os comandos `/speckit.*` são exclusivos do chat do VS Code
- se o Copilot parecer sem contexto, confirme se as instruções do repositório estão habilitadas na IDE

## Como começar com OpenCode

Depois de instalar o OpenCode e configurar seu provedor, abra o repositório no diretório correto e execute `opencode`.

Neste projeto, o OpenCode já encontra o contexto necessário. Você não precisa rodar `/init` nem preparar o projeto do zero.

## Quando usar SpecKit

O SpecKit é opcional. Use quando a demanda for maior, nova, ambígua ou quando fizer sentido gerar artefatos de trabalho para o time.

Fluxo principal:

1. `/speckit.specify`
2. `/speckit.clarify`
3. `/speckit.plan`
4. `/speckit.tasks`
5. `/speckit.analyze`
6. `/speckit.implement`

Para mudanças pequenas, correções pontuais e investigações simples, normalmente vale mais seguir direto com análise ou implementação sem passar por todas as etapas.

## Como pedir análise ou implementação

Quase sempre vale informar:

- qual é o módulo-alvo
- qual é o problema atual
- qual é o comportamento esperado
- se você quer só análise ou se já pode implementar
- se há impacto em banco, menu, permissão, API, evento ou release
- se existe erro reproduzível, quais são os passos e a mensagem recebida
- se a regra de negócio não estiver em `PRD.md`, escreva a regra no próprio pedido

Se quiser um ponto de partida rápido, use os exemplos de `docs/prompts-exemplo.md`.

## Cuidados importantes

As ferramentas ajudam bastante, mas não substituem leitura crítica do contexto e do diff.

Desconfie imediatamente de mudanças que:

- inventem regra de negócio que não está em `PRD.md`
- não sigam `AGENTS.md`
- ignorem impacto em permissões, scripts ou release
- usem `$_REQUEST`
- ignorem `validarLink()` e `validarPermissao()`
- proponham alteração fora do escopo permitido

Também evite enviar segredos, tokens, senhas ou dados reais em prompts.

## Onde buscar as regras do projeto

Quando surgir dúvida, use a fonte mais próxima do problema:

- regra de negócio: `PRD.md`
- padrão técnico, escopo e validações mínimas: `AGENTS.md`
- desenvolvimento de módulos SEI/SIP: `docs/manual_desenvolvimento_md/`
- exemplos de pedidos: `docs/prompts-exemplo.md`
- fluxo SpecKit: `.specify/memory/constitution.md`

## Referências internas de código

Se quiser estudar exemplos dentro do próprio repositório, estes caminhos são boas referências:

- `fontes/sei/src/main/php/sei/web/modulos/abc/exemplo`
- `fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento`

Atualizado em: 2026-06-02
