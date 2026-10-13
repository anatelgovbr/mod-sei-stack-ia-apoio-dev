# SEI

Este é o repositório de código do SEI na Anatel. Aqui vivem o código-fonte, as configurações de ambiente, os módulos desenvolvidos pela equipe, a stack de inteligência artificial do projeto e o [manual de desenvolvimento de módulos SEI](docs/manuais/sei/manual_md/).

---

## Sumário

- [Para quem é este documento](#para-quem-é-este-documento)
- [O que é o SEI](#o-que-é-o-sei)
- [Stack de IA](#stack-de-ia)
- [Módulos](#módulos)
  - [Introdução](#introdução)
  - [O que é o InfraPHP](#o-que-é-o-infraphp)
  - [Lista de módulos](#lista-de-módulos)
- [Ambiente de Desenvolvimento](#ambiente-de-desenvolvimento)
  - [Introdução](#introdução)
  - [Pré-requisitos](#pré-requisitos)
  - [Estrutura de diretórios](#estrutura-de-diretórios)
  - [Ambiente local](#ambiente-local)
- [Referências](#referências)

---

## Para quem é este documento

Este repositório é usado por pessoas de perfis variados: desenvolvedores, analistas de sistemas, gestores e outros profissionais que interagem com o SEI ou com a stack de IA do projeto. Este README foi escrito para que qualquer pessoa que entre no projeto pela primeira vez consiga entender o que existe aqui, para que serve e como usar.

Se você é desenvolvedor, encontrará aqui as instruções técnicas de ambiente e os ponteiros para os padrões de codificação do projeto. Se você não é desenvolvedor, a seção [Stack de IA](#stack-de-ia) mostra onde está a documentação da camada de inteligência artificial, escrita em linguagem acessível.

---

## O que é o SEI

O **SEI** (Sistema Eletrônico de Informações) é um sistema de gestão de processos e documentos eletrônicos desenvolvido pelo Tribunal Regional Federal da 4ª Região. O TRF4 criou o SEI e o disponibilizou como software público para outros órgãos federais, que podem adaptá-lo às suas necessidades. A Anatel adotou o SEI junto a milhares de outros órgãos públicos brasileiros. É por ele que tramitam (circulam e são processados) os processos administrativos da agência em formato digital.

O **SIP** (Sistema de Permissões) é o painel administrativo do SEI. Enquanto o SEI cuida dos processos e documentos, o SIP cuida de quem pode acessar o quê: gerencia usuários, perfis de acesso e permissões. Na prática, os dois sistemas funcionam juntos; as configurações feitas no SIP refletem diretamente no que cada usuário consegue fazer dentro do SEI.

Neste repositório vivem as **adaptações e módulos** do SEI desenvolvidos pela equipe da Anatel: funcionalidades adicionais, integrações com outros sistemas e configurações específicas da agência.

---

## Stack de IA

Este repositório traz uma camada de inteligência artificial integrada ao código: agentes, skills e o fluxo SDD com SpecKit. Ela funciona com GitHub Copilot, OpenCode e Claude Code, e o contexto do projeto viaja junto com o repositório.

Toda a documentação da stack está em [`docs/stack_ai/README.md`](docs/stack_ai/README.md): o que é a stack, o que são agentes e skills, quais ferramentas de IA funcionam aqui, como usar o SpecKit, quais skills existem, prompts prontos e como manter tudo atualizado.

Regras de código, limites de escrita e padrões deste projeto ficam no [`AGENTS.md`](AGENTS.md).

---

## Módulos

### Introdução

Os módulos são extensões desenvolvidas pela Anatel que adicionam funcionalidades ao SEI padrão. Cada módulo tem seu próprio ciclo de desenvolvimento, versionamento (controle de histórico de alterações do código) e documentação.

Todos os módulos seguem a mesma estrutura interna definida pelo InfraPHP, o framework PHP do projeto, explicado na seção a seguir.

### O que é o InfraPHP

**InfraPHP** é o framework interno desenvolvido em PHP (linguagem de programação usada para construir o SEI e seus módulos) que estrutura todos os módulos. Um framework é um conjunto de regras e ferramentas que padronizam como o código é organizado, evitando que cada desenvolvedor resolva o mesmo problema de um jeito diferente.

O InfraPHP define quatro camadas que todo módulo deve seguir:

| Sigla | Camada | O que faz |
|---|---|---|
| **DTO** | Data Transfer Object | Representa os dados de uma entidade, como os campos de um formulário |
| **RN** | Regra de Negócio | Contém a lógica da operação: validações, cálculos e coordenação entre os demais componentes |
| **BD** | Banco de Dados | Contém as instruções de leitura e escrita no banco de dados |
| **INT** | Interface | Ponto de entrada do módulo no SEI: menus, ações e eventos |

Quando um agente ou skill menciona "DTO", "RN" ou "BD", está se referindo a essas camadas. Cada funcionalidade do sistema passa por todas elas.

### Lista de módulos

| Módulo | Descrição | Documentação / Pasta |
|---|---|---|
| `ia` | Integração com o Servidor de Soluções de IA da Anatel | [README](fontes/sei/src/main/php/sei/web/modulos/ia/README.md) |
| `utilidades` | Distribuição e acompanhamento de carga horária por desempenho | [README](fontes/sei/src/main/php/sei/web/modulos/utilidades/README.md) |
| `apoio-plano-trabalho` (APT) | Associação de documentos modelo aos itens de etapa dos planos de trabalho | [README](fontes/sei/src/main/php/sei/web/modulos/apoio-plano-trabalho/README.md) |
| `controle-de-demandas` | Controle de demandas externas e internas | [README](fontes/sei/src/main/php/sei/web/modulos/relacionamento-institucional/README.md) |
| `litigioso` | Controle de processos litigiosos, sanções e decisões | [README](fontes/sei/src/main/php/sei/web/modulos/litigioso/README.md) |
| `peticionamento` | Peticionamento e intimação eletrônicos para usuários externos | [README](fontes/sei/src/main/php/sei/web/modulos/peticionamento/README.md) |
| `pesquisa` | Pesquisa pública de processos e documentos | [README](fontes/sei/src/main/php/sei/web/modulos/pesquisa/README.md) |
| `correios` | Expedição postal via integração com os Correios | [README](fontes/sei/src/main/php/sei/web/modulos/correios/README.md) |
| `ws_complementar` | Web service (integração via API) complementar do SEI | [README](fontes/sei/src/main/php/sei/web/modulos/ws_complementar/README.md) |
| `mod-sei-estatisticas` | Coleta e envio de estatísticas ao PEN (Processo Eletrônico Nacional) | [README](fontes/sei/src/main/php/sei/web/modulos/mod-sei-estatisticas/README.md) |
| `centraliza-modulos` | Centralização de módulos e cadastro de instalações externas | [centraliza-modulos/](fontes/sei/src/main/php/sei/web/modulos/centraliza-modulos/) |
| `pen` | Envio e recebimento de processos e documentos pelo Tramita GOV.BR | [pen/](fontes/sei/src/main/php/sei/web/modulos/pen/) |
| `cgu/mod-sei-eouv` | Integração SEI/FalaBR para importação de manifestações e recursos | [cgu/mod-sei-eouv/](fontes/sei/src/main/php/sei/web/modulos/cgu/mod-sei-eouv/) |
| `trf4/julgamento` | SEI Julgar, gestão de colegiados e sessões de julgamento | [trf4/julgamento/](fontes/sei/src/main/php/sei/web/modulos/trf4/julgamento/) |
| `wssei` | Serviços REST do SEI | [wssei/](fontes/sei/src/main/php/sei/web/modulos/wssei/) |

Cada README de módulo contém: requisitos de versão do SEI, procedimentos de instalação, orientações de negócio e instruções de configuração pós-instalação.

O módulo `controle-de-demandas` está armazenado na pasta `relacionamento-institucional/` por compatibilidade com a organização atual do repositório.

---

## Ambiente de Desenvolvimento

> Se você não é desenvolvedor e não precisa rodar o SEI localmente, pode pular esta seção.

### Introdução

O ambiente de desenvolvimento roda via Docker. O **Docker** é uma ferramenta que empacota o SEI, o banco de dados e os serviços de apoio em contêineres isolados (ambientes independentes que funcionam como "mini-computadores" dentro do seu computador). O **Docker Compose** é um complemento que permite iniciar todos esses contêineres juntos com um único comando, sem precisar instalar PHP, banco de dados ou outros serviços manualmente.

### Pré-requisitos

| Componente | O que é | Observação |
|---|---|---|
| [Git](https://git-scm.com) | Ferramenta de controle de versão de código | Usado para baixar (clonar) e versionar o repositório |
| [Docker](https://www.docker.com) + Docker Compose | Ferramenta que cria ambientes isolados de execução | Garante que o projeto funcione igual em qualquer máquina |

### Estrutura de diretórios

```text
SEI/
├── .agents/       # Configurações dos agentes de IA: skills, regras e referências
├── .claude/       # Integração com o Claude Code
├── .github/       # Integração com o GitHub Copilot
├── .opencode/     # Integração com o OpenCode
├── .specify/      # SpecKit: scripts de execução do fluxo SDD (templates usados apenas no setup inicial)
├── docs/          # Documentação técnica: manual de desenvolvimento de módulos SEI, exemplos de uso da IA e dicionários de dados
│   ├── dicionario_dados/  # Dicionário de dados por módulo (sei/, sip/, litigioso/, ...)
│   ├── manuais/           # Manuais, uma subpasta por módulo
│   │   ├── apoio-plano-trabalho/  # Manual de uso do módulo Apoio a Plano de Trabalho
│   │   └── sei/                   # Manual de desenvolvimento de módulos SEI nos formatos de origem
│   │       └── manual_md/         # O mesmo manual dividido por capítulo em Markdown
│   └── stack_ai/          # Documentação da stack de IA
├── fontes/sei/
│   ├── ops_sei-docker/  # Ambiente Docker com Makefile (ambiente principal)
│   ├── ops/             # Ambiente Docker Compose com scripts para Windows
│   └── src/main/php/
│       ├── sei/   # Código-fonte SEI: páginas, módulos e scripts de atualização
│       ├── sip/   # Código-fonte SIP: scripts de atualização
│       └── infra/ # InfraPHP
├── specs/         # Documentos gerados pelo SpecKit por funcionalidade (somente locais)
└── AGENTS.md      # Regras do projeto para os agentes de IA (leia antes de contribuir)
```

As pastas que começam com ponto (`.agents`, `.claude`, `.github`, `.opencode`, `.specify`) são pastas de configuração. Elas não contêm código do SEI, mas contêm as instruções e ferramentas que orientam o trabalho dos agentes de IA. Cada uma é explicada em detalhes em [`docs/stack_ai/README.md`](docs/stack_ai/README.md).

### Ambiente local

Após iniciar os contêineres Docker (seguindo o guia de configuração), os seguintes serviços ficam disponíveis no seu navegador:

> **O que é `localhost`?** É o endereço que o computador usa para se referir a si mesmo. Os links abaixo funcionam apenas no computador onde o Docker está rodando e somente enquanto o ambiente estiver ativo. Eles não abrem em celulares nem em outros computadores da rede.

| Serviço | O que é | Endereço | Credenciais |
|---|---|---|---|
| SEI | O sistema principal | http://localhost:8000/sei | `teste` / `teste` |
| SIP | O painel de permissões | http://localhost:8000/sip | `teste` / `teste` |
| Solr | Motor de busca textual (pesquisa de processos e documentos) | http://localhost:8983/solr | - |
| MailCatcher | Servidor de e-mail local para capturar e-mails enviados durante testes | http://localhost:1080 | - |

Para instruções de como subir o ambiente:

- [`fontes/sei/ops_sei-docker/README.md`](fontes/sei/ops_sei-docker/README.md): configuração passo a passo com Makefile **(doc principal)**
- [`fontes/sei/ops/README.md`](fontes/sei/ops/README.md): configuração Docker Compose com scripts para Windows

---

## Referências

| Documento | O que contém |
|---|---|
| [`AGENTS.md`](AGENTS.md) | Regras centrais do projeto para agentes: o que pode ser feito, padrões de código e regras de decisão |
| [`docs/stack_ai/README.md`](docs/stack_ai/README.md) | Documentação da stack de IA: conceitos, ferramentas, SpecKit, skills, prompts e manutenção |
| [`docs/manuais/sei/manual_md/`](docs/manuais/sei/manual_md/) | Manual oficial de desenvolvimento de módulos SEI |
| [`docs/dicionario_dados/`](docs/dicionario_dados/) | Dicionário de dados por módulo (uma pasta por módulo: SEI, SIP, Litigioso, ...) |
