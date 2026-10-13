# Sistema Solicitações, exemplo fictício

Esta codebase pequena serve somente para avaliar a skill. Não representa um sistema da Anatel nem uma aplicação implantada; as rotas e os manipuladores demonstram os vínculos de investigação, sem servidor ou ambiente navegável disponível.

O público é formado pelas personas Solicitante, que registra e consulta solicitações, e Consulta, que apenas consulta. Os perfis de acesso têm esses mesmos nomes neste exemplo, mas a relação é explícita, não uma convenção para outros sistemas.

O alcance contém registrar e consultar solicitações, com interface em português brasileiro. A versão corrente vem de `VERSAO` em `src/sistema.py`. O código é UTF-8 e o campo interno `descricao` conserva seu identificador antigo, mesmo que a interface tenha passado a usar Assunto.

O responsável escolheu leitura em GitHub Flavored Markdown, com o manual em Markdown puro. A logo fictícia aprovada está em `recursos/logo.svg`. O comportamento visual do renderizador ainda deve ser conferido; não existe observação da aplicação nem autorização para procurar ambiente externo.

Os artefatos do manual devem usar o nome `manual-solicitacoes`, com arquivos de imagem na subpasta correspondente. O escopo e o público desta descrição preenchem a entrevista inicial; informe qualquer lacuna que ainda depender de observação.
