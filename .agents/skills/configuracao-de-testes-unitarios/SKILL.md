---
name: configuracao-de-testes-unitarios
description: >
  Orienta a configuração de testes unitários e de cobertura de um projeto. Faz um diagnóstico
  somente leitura (linguagem principal, gerenciador de pacotes, versão da linguagem, Docker,
  testes existentes e padrão de teste) e entrega um plano próprio para o projeto, com o comando,
  o lugar onde roda e a forma de conferir cada item, incluindo a cobertura sem meta e um teste de
  fumaça no padrão AAA.

  Use quando o pedido for configurar, montar ou ajustar testes unitários ou cobertura, rodar
  testes dentro de contêiner ou descobrir como executar os testes de um projeto, inclusive legado
  sem nenhum teste.

  Não usar para pipeline de integração contínua, meta de cobertura, implementação, correção de
  defeito ou revisão de código.
---

# configuracao-de-testes-unitarios

Oriente quem vai configurar testes unitários: leia o que o projeto já tem e devolva um **plano** feito para ele. A skill termina na entrega do plano. Quem executa é a pessoa, com o agente da sessão, depois de aprovar.

A skill só lê. Os comandos do diagnóstico consultam o ambiente e deixam intactos arquivos, dependências, imagens e contêineres. Meta de cobertura e integração contínua são decisões do desenvolvedor e ficam fora do plano. Os testes que o plano propõe seguem o padrão **AAA**, descrito no fim deste arquivo.

## Passo 1. Diagnóstico

Monte a tabela do **diagnóstico** a partir do próprio projeto. O ambiente é a fonte: manifesto, arquivo de trava de versões (lockfile), configuração e a resposta dos comandos de consulta dizem qual ferramenta o ecossistema usa.

| Eixo | O que levantar | Onde costuma estar a evidência |
|---|---|---|
| Linguagem principal | a linguagem do código que a aplicação executa | manifesto na raiz, linguagem do serviço da aplicação no contêiner, volume de código por extensão nos arquivos versionados (`git ls-files`; sem Git, na árvore de arquivos), ponto de entrada |
| Gerenciador de pacotes | o gerenciador e a variante, ou a ausência dele | manifesto e lockfile; bibliotecas copiadas para dentro do repositório indicam projeto sem gerenciador |
| Versão da linguagem | a exigida pelo projeto e a disponível na máquina | restrição de versão no manifesto, `FROM` do `Dockerfile`, imagem no `compose.yaml`, `--version` do executável |
| Docker | estado (ausente, parado ou ativo) e serviços do próprio projeto | `docker info`, arquivos `compose.yaml`, `docker-compose.yml`, `Dockerfile` ou `.devcontainer`, `docker compose ps` na raiz do projeto |
| Testes existentes | ferramenta, configuração, pasta de testes e medição de cobertura | arquivo de configuração da ferramenta, pastas de teste, scripts do manifesto |
| Padrão de teste | se o projeto tem `AGENTS.md` e se ele já traz a regra AAA ou outro padrão de teste | `AGENTS.md`, na seção de regras de qualidade |

Cuidados do diagnóstico:

- Meça a linguagem principal só no código do projeto. Desconte dependências instaladas, bibliotecas de terceiros copiadas para dentro do repositório e as pastas da stack de agentes, como `.agents/` e `.specify/`, que trazem scripts das próprias skills.
- Consulte versões, extensões e configuração, inclusive dentro de contêiner já em execução. Rodar código do projeto é trabalho dos itens do plano, depois da aprovação.
- Considere só os serviços do projeto: `docker compose ps` na raiz lista o projeto, enquanto `docker ps` lista a máquina inteira.
- Liste serviços com `docker compose config --services`. Sem `--services`, o comando imprime as variáveis já preenchidas, inclusive segredos.
- Arquivos de ambiente e de configuração do gerenciador de pacotes, como `.env`, podem guardar token. Registre que existem e alerte o desenvolvedor, sem exibir o conteúdo.
- Com empate na linguagem principal, pergunte qual parte recebe o plano. Quando o pedido nomeia uma parte, o plano é dela. As demais linguagens entram como observação.

Termina quando cada linha da tabela tem valor e uma evidência que o sustenta, seja arquivo ou comando executado. Eixo sem evidência recebe "não encontrado" com a busca feita.

## Passo 2. Plano

Derive o **plano** do diagnóstico, um item por linha, na ordem de execução:

| # | Ação e comando | Onde roda | Como conferir | Observação |
|---|---|---|---|---|

- **Ação e comando**: o que fazer e o comando exato. A ferramenta é a que o projeto já usa ou cita; sem isso, a mais adotada no ecossistema, com o motivo da escolha na observação. A versão é a compatível com a versão de linguagem que o projeto exige.
- **Onde roda**: prefira o serviço do projeto que enxerga o código; depois, a máquina com a versão de linguagem compatível. Sem nenhum dos dois, recomende o caminho de menor custo e registre o seguinte, com o custo de cada um.
- **Como conferir**: o resultado observável que prova o item, como a versão respondendo, o arquivo existindo ou o código de saída 0.
- **Observação**: persistência, efeito no versionamento e decisão do desenvolvedor.

O plano cobre o que faltar no projeto, nesta ordem:

1. o gerenciador de pacotes;
2. a ferramenta de teste, como dependência de desenvolvimento;
3. o que a medição de cobertura exige, como extensão ou plugin;
4. a configuração mínima e a pasta de testes;
5. a regra AAA no `AGENTS.md`, conforme a seção "Padrão AAA";
6. um **teste de fumaça**, o "olá, mundo" dos testes, no padrão AAA: roda pela ferramenta de teste e carrega o código do projeto, de modo que erro de sintaxe ou de carregamento aparece na primeira execução;
7. a execução dos testes, conferida por código de saída 0 com pelo menos um teste executado;
8. a execução da cobertura, conferida pelo número na saída, sem meta;
9. o registro do comando de execução como a pessoa o digita, com o prefixo do contêiner quando houver, onde o projeto documenta seus comandos; sem lugar evidente, pergunte onde registrar.

Cite cada arquivo que o plano cria à mão pelo caminho e pelo papel, numa linha; os gerados pela ferramenta, como lockfile e pasta de dependências, entram na observação do item que os gera. O conteúdo é escrito na execução, depois da aprovação. O tópico do item 5 é a exceção e vai palavra por palavra.

O teste de fumaça prova a ferramenta e o carregamento do projeto, e não regra de negócio. Os testes seguintes são escolha do desenvolvedor.

O teste de fumaça se chama `Smoke`, no formato de nome de teste do ecossistema, como `SmokeTest`.

Marque como decisão do desenvolvedor: criar infraestrutura nova, como `Dockerfile` ou serviço no `compose.yaml`, subir, parar ou construir contêiner, baixar imagem, alterar `Dockerfile` ou `compose.yaml` existente e instalar algo no sistema operacional da máquina.

Declare as duas consequências que nenhuma configuração mostra, quando o plano usar contêiner:

- O que se instala num contêiner em execução some quando ele é recriado. Persistir exige alterar o `Dockerfile`.
- Arquivo criado dentro do contêiner pode ficar com dono `root` na máquina. Rode com o usuário do serviço os itens que geram arquivo no repositório.

Quando o projeto já tiver `Dockerfile` ou `compose.yaml`, avalie reaproveitá-los para rodar os testes, como um estágio só de teste no `Dockerfile` ou um serviço só de teste no `compose.yaml`. Antes, confira qual arquivo ou estágio gera a imagem de produção: testes e dependências de teste ficam fora dela.

Termina quando toda lacuna do diagnóstico tem um item ou um motivo declarado, todo item tem como conferir e toda decisão do desenvolvedor está marcada.

## Padrão AAA

Todo teste que o plano propõe segue o padrão AAA, nos termos do tópico abaixo. O item 5 do plano leva o tópico à seção de regras de qualidade do `AGENTS.md` do projeto, como "Qualidade Mínima", palavra por palavra, para que os testes seguintes também o sigam:

```markdown
- Escrever cada teste novo no padrão AAA (Arrange, Act, Assert): preparar o cenário (Arrange), executar uma única ação sobre a unidade testada (Act) e verificar o resultado esperado (Assert), com os três blocos separados e visíveis no código e o nome do teste descrevendo o comportamento verificado.
```

- `AGENTS.md` que já traz o tópico: o item 5 sai do plano.
- `AGENTS.md` sem seção de regras de qualidade: o item 5 pergunta onde inserir o tópico.
- `AGENTS.md` com outro padrão de teste: vale o do projeto. O plano segue esse padrão e registra a diferença como pergunta.
- Projeto sem `AGENTS.md`: o teste de fumaça segue o AAA, e o item 5 sai do plano.

## Saída

Entregue, nesta ordem:

1. o caminho recomendado, em até três frases;
2. a tabela do diagnóstico;
3. o plano;
4. as perguntas em aberto e as observações que mudam uma decisão do desenvolvedor, como outras linguagens e arquivos com credencial, uma linha cada.

A entrega do plano encerra a skill. Quando outra skill aciona esta, o plano volta para ela.
