# mod-sei-stack-ia-apoio-dev

Repositório de apoio com a stack de IA usada no desenvolvimento de módulos SEI.

Aqui ficam concentrados os artefatos que dão suporte ao uso de agentes, prompts, skills e fluxo SDD com SpecKit. Este repositório não contém o código-fonte da aplicação; ele existe para organizar e evoluir a camada de apoio ao trabalho com IA.

## Estrutura do repositório

```text
mod-sei-stack-ia-apoio-dev/
├── .agents/        # Skills, referências, memória operacional e apoio de segurança
├── .github/        # Integrações, agents e prompts do GitHub Copilot
├── .opencode/      # Configuração do OpenCode
├── .specify/       # Scripts, templates e fluxo SDD com SpecKit
├── docs/           # Documentação complementar e exemplos de prompt
├── specs/          # Artefatos locais do SpecKit
├── AGENTS.md       # Diretrizes centrais do repositório
└── README.md       # Este arquivo
```

## Stack de IA

Para ferramenta de IA, recomendamos a extensão do **GitHub Copilot no VS Code**, porque hoje esse é o caminho mais simples para aproveitar o contexto do projeto no dia a dia.

Ao mesmo tempo, a stack de IA deste repositório é agnóstica. Você pode trabalhar com outra ferramenta, desde que ela consiga ler corretamente o contexto do repositório.

Essa stack se apoia principalmente em:

- `AGENTS.md`, com diretrizes, guardrails, escopo de escrita e regras de decisão
- `.agents/skills/`, com as skills compartilhadas do projeto
- fluxo SDD com SpecKit, já versionado e pronto para uso no próprio repositório

Neste repositório, não é necessário instalar nada do SpecKit para começar. A estrutura necessária já está presente, então basta usar o fluxo quando fizer sentido para a demanda.

Em outras palavras: aqui o SpecKit já faz parte da estrutura do projeto. O desenvolvedor não precisa preparar nem configurar esse framework antes de usar.

Se você optar por uma ferramenta não convencional ao projeto, confirme antes se ela consegue ler [`.agents/skills/`](.agents/skills/) e seguir as instruções de [`AGENTS.md`](AGENTS.md).

### Estrutura da stack

- [`AGENTS.md`](AGENTS.md) — diretrizes centrais para agentes, prompts e uso da stack
- [`.agents/`](.agents/) — skills, referências, memória operacional e apoio de segurança
- [`.github/`](.github/) — integrações, agents e prompts do GitHub Copilot
- [`.opencode/`](.opencode/) — configuração do OpenCode
- [`.specify/`](.specify/) — scripts, templates e configuração do fluxo SDD com SpecKit

Pensando na manutenção da stack, o repositório foi organizado para manter o SpecKit como base do fluxo, enquanto as integrações por ferramenta apenas expõem essa base no runtime correspondente.

Na prática:

- o fluxo padrão vive em `.agents/skills/speckit/`
- `.github/` e `.opencode/` funcionam como adapters leves por ferramenta
- `AGENTS.md` e `.agents/references/` definem o contexto e os guardrails de uso

### Estrutura da pasta `.agents/`

```text
.agents/
├── decisions/                 # ADRs e registros de decisões arquiteturais
├── memory/                    # Memória operacional compartilhada entre sessões
├── references/                # Guias, padrões, gates e mapas de apoio
├── security/                  # Checklists e referências de revisão de segurança
└── skills/                    # Skills reutilizáveis por domínio, fluxo ou validação
```

Resumo de uso:

- `decisions/` concentra decisões mais duradouras, quando uma escolha técnica precisa ficar documentada.
- `memory/` guarda memória operacional curta e reutilizável, como o `runbook.md`.
- `references/` reúne o material base consultado pelas skills, como padrões de codificação, roteamento e gates.
- `security/` concentra apoio para revisão de segurança e análise de riscos.
- `skills/` contém as skills do projeto, incluindo fluxos do SpecKit, guardrails do SEI e verificações especializadas.

## Como começar

1. Tenha uma ferramenta de IA disponível, preferencialmente a extensão do GitHub Copilot no VS Code.
2. Abra este repositório na ferramenta escolhida.
3. Use os recursos da stack conforme a demanda, consultando `AGENTS.md`, `.agents/skills/` e, quando fizer sentido, o fluxo SDD com SpecKit.

Você não precisa rodar `init`, instalar o SpecKit nem fazer configuração adicional para começar. Se a ferramenta não fizer parte da stack usual do projeto, confirme antes que ela consegue ler `.agents/skills/`.

## Quando usar SpecKit

Use o SpecKit quando a demanda for maior, nova, ambígua ou quando fizer sentido estruturar o raciocínio antes de implementar. Neste repositório, ele apoia o fluxo SDD, ajudando a especificar, esclarecer, planejar, decompor e implementar uma entrega com mais contexto.

Fluxo principal:

1. `/speckit.specify`
2. `/speckit.clarify`
3. `/speckit.plan`
4. `/speckit.tasks`
5. `/speckit.analyze`
6. `/speckit.implement`

Os arquivos em `specs/` são locais e descartáveis. Eles não fazem parte dos artefatos versionados do time.

## Arquivos locais opcionais

Os arquivos abaixo são locais por desenvolvedor e não precisam ser versionados:

- `.specify/init-options.json`
- `.specify/integration.json`

A ausência desses arquivos não impede o uso normal do SpecKit neste repositório.

## Atualizações da stack

Ferramentas como `specify`, `OpenCode` e `GitHub Copilot` são atualizadas localmente por cada desenvolvedor em sua própria máquina.

Essas atualizações locais não atualizam automaticamente os arquivos versionados do repositório. Qualquer mudança em arquivos da stack de IA e do SpecKit do projeto deve ser feita manualmente, com parcimônia e revisão do desenvolvedor.

Quando houver necessidade de atualizar o framework do SpecKit dentro do projeto, o ponto de partida deve ser sempre o fluxo padrão em `.agents/skills/speckit/`.
