# <Funcionalidade>

<Propósito em uma a três frases: o que esta funcionalidade faz e para quem.>

Fora do escopo: <item> (<onde é tratado>); <item> (<onde é tratado>).

Regras de negócio: [regras-de-negocio.md](../regras-de-negocio.md).

<!-- Um arquivo por funcionalidade, na pasta requisitos-funcionais/ do módulo. Uma seção por operação, como Listar, Cadastrar e alterar, Excluir, ou por etapa de um fluxo, como Aplicar o modelo. Mudar um requisito de seção não troca o ID. -->

## <Operação ou etapa>

### RF-<SIGLA>-<NNN>: <Título curto com verbo no infinitivo>

<Enunciado EARS com um único "deve". Escolha uma forma:
"O sistema deve <resposta>." |
"Enquanto <estado>, o sistema deve <resposta>." |
"Quando <gatilho>, o sistema deve <resposta>." |
"Onde <funcionalidade estiver habilitada>, o sistema deve <resposta>." |
"Se <situação indesejada>, então o sistema deve <resposta>." |
"Enquanto <estado>, quando <gatilho>, o sistema deve <resposta>.">

<!-- Obrigatório quando a verificação é teste manual: um cenário por caso da lista de cobertura de docs/requisitos-ancorados/README.md, logo abaixo da Verificação, com um subitem por passo. Estilo declarativo: comportamento, sem cliques nem nomes de campo. Caso indesejado que está em outro requisito: cite esse requisito no campo Verificação. -->

- Verificação: <teste automatizado | teste manual | inspeção> - <referência ou cenário>
- Cenário: RF-<SIGLA>-<NNN>.C1 <nome do caso>
  - Dado <estado inicial>
  - Quando <evento>
  - Então <resultado observável>
