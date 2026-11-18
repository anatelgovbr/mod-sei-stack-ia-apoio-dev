# ADR-SEI-005: Testes e2e preparam os dados por seed idempotente

- Status: aceita
- Data: 2026-10-21
- Proprietário: Equipe SEI
- Participantes afetados: desenvolvedores que rodam ou escrevem testes e2e e quem mantém o ambiente local em `ops/`
- Escopo: testes e2e de `tests/e2e`, executados pelo serviço `pw` de `ops/qa/docker-compose.yml` sobre o ambiente local de `ops/sei-docker-localhost`; nenhum ID de `docs/requisitos-ancorados/` afetado
- Substitui: nenhuma
- Substituída por: nenhuma

## Contexto

Os testes e2e rodam no SEI local, em `http://localhost:8000`, e leem o banco do ambiente de desenvolvimento. Alguns testes dependem de dados que esse banco nem sempre tem. O teste do módulo Apoio a Plano de Trabalho (APT), por exemplo, precisa do módulo instalado no SIP e no SEI e de pelo menos um plano de trabalho ativo.

O banco do ambiente local nasce da imagem `processoeletronico/mysql8-sei50`, sem módulos e sem planos de trabalho. Depois de recriar o banco, ou em uma máquina nova, esses testes falham sem defeito no código, porque os dados não existem. Sem um passo de preparação, o resultado da suíte depende do que existe no banco de cada máquina.

O módulo também precisa estar registrado na `ConfiguracaoSEI.php` da máquina, arquivo fora do versionamento que não muda quando o banco é recriado.

O projeto não tem padrão para preparar dados de teste. A escolha vale para todos os testes e2e que vierem depois.

## Critérios da decisão

- A suíte e2e passa em um banco recém-criado a partir da imagem, sem passo manual.
- A suíte e a preparação rodam com um único comando, igual no Windows e no Linux.
- A preparação não apaga nem altera dados que o desenvolvedor já tem no banco local.
- Rodar a preparação de novo não duplica registros.
- Os dados são gravados do mesmo jeito em MySQL, SQL Server, PostgreSQL e Oracle, os bancos que o SEI suporta.
- O custo de memória, disco e tempo cabe na máquina de desenvolvimento, que já divide o Docker entre o SEI, o SonarQube local e o contêiner `qa`.

## Alternativas consideradas e tradeoffs

### Alternativa A: cada teste cria os próprios dados pela tela

Cada teste cadastra o que precisa pelas telas do SEI antes de começar e apaga depois. Dá o maior isolamento entre testes. Rejeitada porque deixa a suíte lenta, já que o login local leva cerca de 25 segundos, faz o teste depender de telas que ele não testa e repete código de cadastro em cada teste.

### Alternativa B: arquivo SQL com os dados

Um script SQL insere os registros direto nas tabelas. É simples de escrever. Rejeitada porque precisa de uma versão por banco suportado e grava identificadores fixos que podem colidir com os gerados pelas sequências do InfraPHP.

### Alternativa C: seed idempotente antes da suíte, no banco do ambiente local

Um serviço `seed`, com a imagem e a configuração do `httpd`, roda antes do pytest, e o serviço `pw` só começa depois que o seed termina sem erro. O seed instala os módulos pelos scripts oficiais de versão e cadastra os registros pelas classes RN do SEI, só quando ainda não existem. Adotada.

## Decisão e justificativa

Os testes e2e obtêm os dados de que precisam por um seed idempotente, `tests/e2e/seed.php`, executado pelo serviço `seed` de `ops/qa/docker-compose.yml` com a imagem e a configuração do `httpd`. O serviço `pw` depende do `seed` e só começa depois que ele termina sem erro, então o comando da suíte também roda o seed. O seed instala os módulos pelos scripts oficiais de versão e cadastra os registros pelas classes RN do SEI. Os registros do seed levam o prefixo `E2E` no nome e só são gravados quando ainda não existem. O seed nunca altera nem apaga dados que ele não criou e não altera a `ConfiguracaoSEI.php`: sem o módulo registrado, o script oficial de versão para e a suíte não roda.

A decisão atende aos critérios:

- O banco recém-criado recebe os dados sem passo manual.
- O comando da suíte, no Windows e no Linux, continua o mesmo e roda o seed antes dos testes.
- O banco do desenvolvedor só ganha registros novos, identificados pelo prefixo.
- A checagem antes de gravar evita registros duplicados.
- As classes RN e as sequências do InfraPHP gravam do mesmo jeito em todos os bancos suportados.

A documentação do Playwright recomenda controlar os dados quando o teste usa banco: "If working with a database then make sure you control the data."

## Consequências

### Favoráveis

- Um banco recriado volta a rodar a suíte e2e completa com um comando.
- Os testes continuam só de leitura e não precisam de código de preparação.
- Os dados de teste ficam identificáveis pelo prefixo no banco local.

### Desfavoráveis

- O banco local do desenvolvedor passa a ter registros de teste ao lado dos dados dele.
- Cada teste novo que depende de dado obriga a atualizar o seed.
- Uma falha no seed impede a suíte de rodar, e o motivo fica no log do serviço `seed`, fora da saída do comando da suíte.
- O seed depende das classes RN do SEI e dos scripts de versão dos módulos e precisa acompanhar mudanças neles.
- Um teste que grava ou altera dados não cabe nesta decisão, porque mudaria os registros do seed para a rodada seguinte.

## Verificação

Em um banco recém-criado a partir da imagem, sem módulos instalados, rodar a suíte e2e duas vezes seguidas. A decisão é aceita quando todos os testes passam nas duas rodadas, a quantidade de registros com o prefixo do seed é a mesma depois da primeira e da segunda rodada e as tabelas tocadas pelo seed mantêm os registros que existiam antes. O resultado fica na descrição da MR que implementa o seed.

## Gatilhos de revisão

- A suíte e2e passa a rodar em pipeline de integração contínua.
- Um teste precisa gravar ou alterar dados.
- O volume de dados do seed deixa de caber na preparação feita pelo serviço `seed` antes da suíte.
- Mudança nas classes RN ou nos scripts de versão usados pelo seed.

## Referências

- Playwright, [Best Practices](https://playwright.dev/docs/best-practices): "If working with a database then make sure you control the data."
- `tests/e2e/`: testes e2e, entre eles `sei/web/modulos/apoio-plano-trabalho/test_associacao_de_documento_modelo.py`.
- `tests/e2e/seed.php`: seed dos testes e2e.
- `ops/qa/docker-compose.yml`: serviço `seed`, que roda o seed, e serviço `pw`, que roda a suíte depois dele.
- `fontes/sei/src/main/php/sip/scripts/sip_atualizar_versao_modulo_apt.php` e `fontes/sei/src/main/php/sei/scripts/sei_atualizar_versao_modulo_apt.php`: scripts oficiais de versão do APT.
