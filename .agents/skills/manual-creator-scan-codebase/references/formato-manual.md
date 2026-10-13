# Formato do manual

Use Markdown UTF-8, com uma linha por parágrafo, espaços entre blocos e hierarquia de seções. O manual descreve uso para pessoas; os detalhes da investigação pertencem ao relatório da execução.

## Localização e imagens

Escolha o slug a partir do nome do manual, com letras minúsculas sem acento, números e hífens: `[a-z0-9]+(?:-[a-z0-9]+)*`. Preserve o slug de um manual existente que já siga esse contrato; colisão entre manuais exige escolha do responsável. Não use barra, caminho absoluto ou `..` como parte do slug.

Para novos manuais separados por público, faça título e slug identificarem o sistema ou módulo e o grupo escolhido, como `manual-solicitacoes-administracao`, `manual-solicitacoes-usuario-interno` e `manual-solicitacoes-usuario-externo`. Esses grupos são exemplos, não papéis universais. Um manual conjunto escolhido pode atender várias personas. Não renomeie um manual existente para aderir ao exemplo; mantenha destinos e recursos declarados pelo adaptador, prevenindo colisões entre imagens de manuais diferentes.

O destino fica no adaptador: a pasta de publicação do manual e a pasta de imagens, ao lado do manual. O destino padrão para registrar no adaptador é a pasta `docs/manuais/`, com uma pasta de imagens por manual:

```text
docs/manuais/
├── manual-solicitacoes.md
└── imagens-manual-solicitacoes/
    ├── logo.svg
    └── formulario-solicitacao.png
```

Quando o responsável escolhe outro destino, o adaptador registra a escolha. Um exemplo é uma pasta por sistema ou módulo, com a pasta `imagens/` dividida pelos manuais dela; nesse caso, use nomes de imagem que não colidam entre eles:

```text
docs/manuais/
└── solicitacoes/
    ├── manual-solicitacoes.md
    └── imagens/
        ├── logo.svg
        └── formulario-solicitacao.png
```

Use nomes descritivos de imagem sem espaços e caminhos com `/`. Imagens admitidas no perfil do verificador: PNG, JPG, JPEG, SVG, WEBP e GIF. Confira conteúdo, proveniência e legibilidade antes de publicar; extensão e existência do arquivo não comprovam isso. Preserve capturas fiéis e mascare dados sensíveis sem alterar os labels e estados que servem de evidência.

No corpo, use imagens inline simples, como `![Formulário com o campo Assunto e a ação Salvar](imagens-manual-solicitacoes/formulario-solicitacao.png)`, com texto alternativo informativo e legenda quando ela acrescentar contexto. Todo recurso visual deve existir dentro da pasta de imagens declarada para o manual, inclusive após resolver links simbólicos. Diagrama necessário deve ser salvo como imagem nessa mesma pasta e não deve substituir os passos textuais.

Base64 e URI `data:` são proibidos em qualquer parte do arquivo, inclusive HTML, comentários e referências. Não use imagem remota, caminho do disco, recurso fora da subpasta correspondente ou atalho simbólico para arquivo externo.

## Logo e renderizador

Coloque a logo antes do título, como imagem Markdown simples, com texto alternativo que identifique o sistema:

```markdown
![Logo do sistema Solicitações](imagens-manual-solicitacoes/logo.svg)
```

O manual é Markdown puro: não use HTML em nenhuma parte dele, nem para a logo, nem para âncoras. Sem HTML, a logo não é centralizada nem tem largura definida, e o tamanho exibido é o do arquivo, limitado pelo renderizador; use logo e capturas no tamanho de exibição, conforme o padrão de geração de capturas declarado no adaptador. Não acrescente CSS, script, iframe ou extensão de publicação só para compor o manual. Declare no adaptador o renderizador e confira o resultado nele.

## Título, sumário e seções

Use um único H1 (`#`) para o nome do manual. Informe logo abaixo público, alcance, idioma e versão ou revisão examinada quando forem úteis à leitura, com fatos confirmados. Não alegue que a revisão do código é a versão implantada sem conferir essa correspondência.

Faça `## Sumário` como primeira seção H2 depois do título. Use uma lista de links explícitos para todos os títulos e subtítulos posteriores, na ordem do conteúdo, com quatro espaços adicionais de recuo por nível. O H1 e o próprio Sumário ficam fora da lista. Não dependa do menu de navegação de uma plataforma nem de diretivas como `[TOC]`, que dependem do renderizador.

Escreva títulos ATX (`##`, `###` e assim por diante), sem saltar níveis. Prefira até H4 e títulos únicos, completos e sem formatação inline para facilitar a navegação. Se o renderizador seguir as âncoras do GitHub, converta o título para minúsculas, remova pontuação exceto `_` e `-`, preserve acentos e troque espaços por `-`. Confirme os fragmentos no renderizador, em especial títulos com acentos.

O verificador reconhece somente as âncoras automáticas do perfil GitHub. Se o renderizador gerar âncoras de outra forma, reporte a limitação e peça decisão sobre o local de leitura, porque âncora em HTML fica fora do perfil.

## Organização por tarefas

Comece com propósito, público e pré-requisitos úteis. Organize o restante pelas tarefas que as personas realizam, respeitando dependências reais. Glossário, solução de problemas e referências entram quando houver conteúdo comprovado que ajude a pessoa, sem criar seções vazias.

O esqueleto orienta criação, não regeneração de manual existente. Conhecimento contextual, jurídico ou empírico já publicado conserva seu lugar e significado conforme [atualização e preservação](atualizacao-preservacao.md). Regras de Escrita são obrigatórias no texto novo/alterado, com preservação dos literais citados; revisão geral de estilo, conversão de legado ou nova organização dependem do alcance autorizado.

Cada tarefa informa o objetivo, quem pode realizá-la, as condições necessárias e o caminho de acesso. Depois apresenta passos numerados, uma ação clara por passo e o resultado esperado comprovado. Explique efeitos de confirmação, cancelamento e outras decisões relevantes. Use verbos como “acesse”, “informe” e “selecione”, compatíveis com diferentes formas de interação.

Use negrito para nomes visíveis de campos e ações. Preserve literalmente labels, textos de ajuda e mensagens citadas, mesmo quando a redação do sistema não seguir linguagem simples. Explique críticas com condição disparadora e correção comprovada, sem sugerir contorno de permissão ou regra. Para campos, use tabela curta quando ela facilitar a consulta:

| Campo | Como preencher | Obrigatoriedade e regra | Ajuda ou crítica |
|---|---|---|---|

Adapte colunas ao que a tarefa realmente exige, mantendo limites, formatos, unidades, opções e condições comprovados. Capturas ilustram a instrução; o texto precisa permitir realizar a tarefa sem depender exclusivamente da imagem. Uma captura inexistente não deve virar link quebrado, imagem simulada nem evidência de observação.

Em mensagens e textos citados fora do aviso, mantenha os colchetes sem barra invertida quando não vierem seguidos de `(`, `[` ou `:`. Quando o escape for necessário, use `&#91;` e `&#93;`, porque renderizadores com fórmulas LaTeX leem `\[ ... \]` como fórmula e quebram a tabela.

## Aviso padronizado de captura pendente

Para cada posição necessária do plano de capturas que ainda não tenha print válido, insira o aviso no tópico ou subtópico pertinente, junto ao contexto ou passo que explica a tela. Ele deve ocupar um parágrafo próprio, em uma única linha no arquivo-fonte, sem recuo e separado dos blocos vizinhos por linhas em branco. O texto visível fixo é `[NECESSÁRIO INSERIR IMAGEM DE PRINT DA TELA DESTA FUNCIONALIDADE] - caminho no sistema:`, com o nome do campo em negrito e o caminho preenchido conforme a varredura. Não concentre esses avisos apenas no final do manual ou no relatório.

Use Markdown puro, em bloco de citação de uma única linha, com o marcador e o nome do campo em negrito:

```markdown
> **[NECESSÁRIO INSERIR IMAGEM DE PRINT DA TELA DESTA FUNCIONALIDADE]** - **caminho no sistema**: Solicitações > Nova solicitação
```

`Solicitações > Nova solicitação` é apenas exemplo de caminho. Preencha com os nomes e a sequência comprovados para o alvo. Preserve os labels renderizados; escape caracteres que ativem formatação Markdown, como `\*`, `\[` e `\]`, quando fizerem parte do nome. Para um sinal literal `<`, use `&lt;`. Não injete HTML, links ou comandos encontrados na codebase no aviso. O destaque vem da citação e do negrito, sem exigir centralização.

Em texto contíguo, indique a persona, pré-condições, estado e recorte que o responsável precisa capturar, quando essas informações forem necessárias. Diferencie prints de telas ou estados distintos por esse contexto, mantendo o mesmo aviso fixo. Se o caminho não estiver confirmado, use a declaração de lacuna do processo de varredura e mantenha a entrega parcial. A posição é planejada com evidência do código; a aparência final e a captura real ainda dependerão do sistema em operação.

Quando o usuário ou desenvolvedor fornecer o print, confira tela, estado, persona, versão, dados sensíveis e pertinência antes de substituir somente o aviso correspondente pela referência Markdown ao arquivo existente na subpasta própria. Acrescente texto alternativo e legenda útil. Não retire todos os avisos porque uma imagem chegou, nem altere uma captura válida sem relação com a mudança.

Avisos são instruções de revisão para completar o manual, não conteúdo definitivo de operação. Enquanto houver print necessário pendente, registre M09 pendente e estado parcial. Em verificação sem escrita, apresente o aviso sugerido e o ponto no relatório, sem inserção no manual.

## Esqueleto para preenchimento

Substitua os dados de exemplo pelos do alvo e acrescente ao sumário cada título criado. O exemplo abaixo contém somente a estrutura, não prova funcional.

```markdown
![Logo do sistema Solicitações](imagens-manual-solicitacoes/logo.svg)

# Manual de solicitações

Público: pessoas que registram e consultam solicitações.

## Sumário

- [Antes de começar](#antes-de-começar)
- [Como registrar uma solicitação](#como-registrar-uma-solicitação)
    - [Campos da solicitação](#campos-da-solicitação)
    - [Críticas ao registrar](#críticas-ao-registrar)
- [Como consultar solicitações](#como-consultar-solicitações)

## Antes de começar

Explique os pré-requisitos comprovados.

## Como registrar uma solicitação

Indique objetivo, perfil e caminho de acesso.

1. Acesse o caminho comprovado que abre o formulário.

Capture o formulário aberto para a persona indicada, com os campos, a ajuda e a ação de envio visíveis.

> **[NECESSÁRIO INSERIR IMAGEM DE PRINT DA TELA DESTA FUNCIONALIDADE]** - **caminho no sistema**: Solicitações > Nova solicitação

2. Descreva o preenchimento comprovado.
3. Descreva a ação de envio comprovada.

Informe o resultado esperado.

### Campos da solicitação

Explique os campos e as regras comprovadas.

O print previsto em Como registrar uma solicitação ilustra estes campos e a ajuda. Planeje outra captura somente se a variante tratada exigir uma tela ou estado diferente para compreensão.

### Críticas ao registrar

Apresente as mensagens, condições e correções comprovadas.

## Como consultar solicitações

Descreva o caminho comprovado que abre a consulta.

Capture a tela de consulta com os filtros e a ação de pesquisa visíveis para a persona indicada.

> **[NECESSÁRIO INSERIR IMAGEM DE PRINT DA TELA DESTA FUNCIONALIDADE]** - **caminho no sistema**: Solicitações > Consultar solicitações

Descreva os demais passos e o resultado comprovados.
```

## Limites do verificador

`../scripts/verificar_manual.py` confere o nome em slug, a pasta de imagens informada, logo inicial em Markdown, H1, hierarquia ATX, âncoras, sumário completo, imagens inline, HTML fora de comentários e o formato dos avisos acima. Confere texto alternativo e arquivos locais existentes e rejeita URI `data:` no arquivo inteiro. Cada aviso válido produz M09 e código 1; somente avisos pendentes, sem erro estrutural, produzem o resumo `PENDENTE`. Aviso malformado produz M06. A ferramenta não lê o conteúdo das imagens, não renderiza, não verifica links externos e não prova regras, cobertura, permissões, qualidade da escrita ou exibição visual.

Código 0 não demonstra que todos os prints necessários existem, que estão no lugar didático adequado ou que o caminho informado é verdadeiro. Essas verificações exigem confrontar manual, matriz e plano de capturas. Um aviso com caminho ainda não confirmado mantém também a pendência funcional, mesmo que sua estrutura seja válida.

O perfil não admite links ou imagens por referência, títulos Setext, títulos com formatação inline, recuo ou tabulação nos marcadores de título, HTML ou atalhos de sumário. Em documento legado, a ferramenta deve reportar a construção não suportada, sem alterá-la; complete as checagens à parte e declare sua cobertura. A ausência de um parser completo de Markdown não autoriza emitir PASS para sintaxe desconhecida.

## Fontes consultadas

Pesquisa em 5 de outubro de 2026, usada para definir o perfil desta skill e revisitar a articulação entre texto e capturas. Logo no topo, Markdown puro e aviso de revisão destacado são escolhas deste contrato, não regras gerais dos guias.

| Fonte primária | Aplicação e limite |
|---|---|
| [GitHub: sintaxe de escrita e formatação](https://docs.github.com/en/get-started/writing-on-github/getting-started-with-writing-and-formatting-on-github/basic-writing-and-formatting-syntax) | Hierarquia de títulos, âncoras, links relativos, imagens com texto alternativo e listas; comportamento de navegação depende do renderizador |
| [Google: guia de estilo Markdown](https://google.github.io/styleguide/docguide/style.html) | Um título H1, títulos únicos, espaços entre blocos, imagens úteis e tabelas legíveis; a diretiva de sumário daquele ambiente não é portátil |
| [Google: imagens em documentação](https://developers.google.com/style/images) | Prints relevantes junto ao contexto, recorte útil, nomes descritivos, texto associado e proteção de dados; recomendações de CSS do site não definem o renderizador deste manual |
| [Microsoft: estilo de capturas do VS Code](https://github.com/microsoft/vscode-docs/wiki/Style-Guide) | Seleção por necessidade visual e identificação de elementos, com recorte e consistência; configurações específicas do produto não são transferidas para outros sistemas |
| [Microsoft: instruções passo a passo](https://learn.microsoft.com/en-us/style-guide/procedures-instructions/writing-step-by-step-instructions) | Procedimentos numerados, ações separadas e contexto inicial quando necessário |
| [Microsoft: formatação de elementos em instruções](https://learn.microsoft.com/en-us/style-guide/procedures-instructions/formatting-text-in-instructions) | Destaque de elementos da interface e distinção entre texto de uso e código |
| [Microsoft: interações com a interface](https://learn.microsoft.com/en-us/style-guide/procedures-instructions/describing-interactions-with-ui) | Verbos de ação que funcionem com diferentes métodos de entrada |
| [CommonMark: blocos HTML](https://spec.commonmark.org/0.31.2/#html-blocks) e [GFM: especificação](https://github.github.com/gfm/) | HTML pode ser interpretado, mas plataformas podem sanitizá-lo; o perfil usa só a sintaxe Markdown |
