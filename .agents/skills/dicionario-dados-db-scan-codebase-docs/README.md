# dicionario-dados-db-scan-codebase-docs

A skill `dicionario-dados-db-scan-codebase-docs` investiga a codebase, os scripts de banco e qualquer documentação ou material complementar disponível para gerar e manter dicionários de dados. Ela nasceu de [documento conceitual](references/conceitos-e-instrucoes-tecnicas_descricao_tabelas_colunas.md) apoiado na família de normas ISO/IEC de qualidade de dados e metadados (ISO 8000-1, ISO/IEC 25012/25024 e ISO/IEC 11179). O alvo pode ser o sistema, um módulo, uma base de dados corporativa ou um data warehouse. Todo alvo reconhecido precisa de um adaptador registrado.

Adaptador é o arquivo que ensina a skill a localizar, investigar e versionar esse alvo: onde fica a fonte estrutural, qual fonte tem precedência quando houver mais de uma, como a versão é identificada e onde buscar no código. Fica em `adapters/<família>/<caminho-do-adaptador>.md`, listado em `registro-adaptadores.md`, ambos na raiz da skill. Use o prompt "Criar o adaptador" (seção Prompts de Exemplo) para criar e registrar o adaptador.

A skill gera três artefatos de saída: `dicionario_tabelas.md` e `dicionario_colunas.md`, com as descrições semânticas, e `CHANGELOG.md`, com o changelog estrutural. O que não puder ser confirmado nas fontes disponíveis é reportado como lacuna, nunca publicado por suposição.

Crie o adaptador antes do primeiro dicionário, em um pedido só dele. Uma descrição só é tão assertiva quanto a evidência que a sustenta, e é o adaptador que diz onde essa evidência está. Sem ele, o que o agente descobre sobre o alvo existe só dentro da sessão: na vez seguinte, ou ele refaz a varredura dos padrões do zero, ou você repete as convenções na mão.

## Prompts de Exemplo

Os prompts abaixo são pontos de partida reais, não ilustrações genéricas: adapte para o seu caso e envie.

A ordem das seções abaixo é a ordem recomendada de uso, e é o que garante a qualidade esperada do resultado. Crie o adaptador do alvo primeiro, com "Criar o adaptador". Depois, ao criar ou atualizar o dicionário, anexe sempre os materiais complementares que você tiver disponíveis (manuais, prints de tela, dicionário anterior, planilhas etc.). Eles ajudam a confirmar a semântica de tabelas e colunas e tendem a melhorar a qualidade do resultado. Se ainda não tiver prints mas houver um ambiente de teste disponível, gere-os primeiro com "Gerar prints de tela como insumo complementar".

Cite a skill `dicionario-dados-db-scan-codebase-docs` pelo nome no prompt, como nos exemplos abaixo. Não é preciso citar o adaptador do alvo: uma vez criado e registrado, a skill já sabe localizá-lo sozinha. Também não é preciso citar critérios de qualidade ou comandos de verificação internos à skill. O que puder ser descoberto no código, a skill descobre sozinha.

Todo trecho entre `<` e `>` é um parâmetro: substitua pela informação real antes de enviar. Campo marcado como `<se souber>` que você não tiver como preencher: apague a linha inteira, nunca deixe o texto entre `<` e `>` dentro do prompt enviado.

Nenhum prompt precisa ser enviado igual ao template: eles servem a mais de um sistema ou módulo, e você nem sempre terá todos os dados disponíveis no momento. Linha que não se aplica ao seu caso, apague. Mande só o que você realmente tem.

### Criar o adaptador

Use este prompt no primeiro contato com um alvo que a skill ainda não reconhece, seja o sistema, um módulo ou uma base de dados corporativa. Ele cria só o adaptador. Gere o dicionário depois, em um pedido separado, com o prompt "Criar o dicionário de dados" a seguir. Informe as convenções que você já souber, para reduzir as perguntas que a skill precisará fazer. O que você não souber, ela tenta inferir da codebase antes de perguntar.

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o adaptador de <sistema ou módulo>. Investigue a codebase, crie o adaptador completo e registre-o. Não gere o dicionário de dados nem o changelog nesta etapa.

O que eu já sei sobre ele:
- pistas que identificam este sistema ou módulo (nome, caminhos, prefixo de tabela, pasta de documentação, ou o codebase/repositório em si, se for o sistema inteiro): <se souber, ex.: "prefixo pedidos_, models em app/Models/Pedido.php, migrations em database/migrations/">
- fonte estrutural e convenção de versionamento: <scripts de instalação, migrations, schema ou DDL, se souber, ex.: "migrations em migrations/Version20240115120000.php">
- precedência entre fontes, se houver mais de uma fonte estrutural para a mesma informação: <qual prevalece, se souber, ex.: "migration mais recente prevalece sobre o schema.sql legado">
- codificação, camadas e onde buscar no código: <se souber, ex.: "camadas Entity/Repository/Controller">
- títulos e pasta de destino dos dicionários: <se souber, ex.: "docs/dicionario_dados/abc/">
- particularidades ou exceções conhecidas: <se houver, ex.: "módulo tem tabela compartilhada com outro módulo, não duplicar no dicionário">

Trate os itens acima como pista, não como conclusão: confirme cada um contra a codebase e me avise se algum divergir.

Pergunte objetivamente só sobre o que não puder ser inferido nem foi informado acima. Justifique sua resposta.
```

### Criar o dicionário de dados

Use este prompt na primeira vez que for gerar o dicionário de um sistema ou módulo já com adaptador. O material complementar pode ser qualquer formato: esquema de banco em outra ferramenta, dicionário anterior, prints de tela, manuais, vídeos ou transcrições. Cite os materiais que tiver e, se houver mais de um, indique a qual dar atenção especial. A skill sempre confirma tudo contra as fontes estruturais disponíveis (codebase, esquema de banco ou DDL) antes de publicar qualquer descrição, com ou sem material complementar.

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para criar o dicionário de dados e o changelog estrutural de <sistema ou módulo>.

Investigue as fontes estruturais disponíveis (codebase, scripts de instalação, migrations, schemas ou DDLs) para identificar a convenção de versionamento e, quando houver codebase, onde ficam as regras de negócio. Aproveite também qualquer documentação já existente. Não publique como fato uma descrição cuja semântica não esteja suficientemente sustentada pelas evidências encontradas.

Considere como material complementar <se houver: arquivos anexados, esquema em outro formato, dicionário anterior, prints, manuais, vídeos, transcrições>. Dê atenção especial a <o material mais relevante, se houver mais de um>, mas confirme tudo contra a fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, informe explicitamente: as tabelas ou colunas cuja semântica você não conseguiu confirmar nas fontes disponíveis, o que faltou para confirmá-las, e onde algum material complementar divergiu da fonte estrutural e qual fonte você adotou. Justifique sua resposta.
```

### Atualizar o dicionário

Use quando o dicionário já existir e você quiser sincronizá-lo com mudanças estruturais no sistema ou módulo (novas tabelas, colunas ou regras de negócio) ou após uma nova versão. Também serve para corrigir uma descrição anterior, mas só diante de divergência estrutural confirmada ou domínio incompleto confirmado, nunca por ajuste de estilo.

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para atualizar o dicionário de dados de <sistema ou módulo> para o estado mais recente da <codebase ou base>.

Compare o dicionário de dados e o changelog já existentes com a estrutura e as regras de negócio atuais e altere somente o que realmente mudou desde a última atualização, preservando o restante que não teve mudança sem alteração.

Se você souber a versão-alvo, os commits ou as migrations específicas da mudança, indique-os. Caso contrário, identifique o escopo da diferença pela própria codebase.

Considere como material complementar <se houver: arquivos anexados, esquema em outro formato, dicionário anterior, prints, manuais, vídeos, transcrições>. Dê atenção especial a <o material mais relevante, se houver mais de um>, mas confirme tudo contra a fonte estrutural disponível (código, esquema de banco ou DDL) antes de publicar qualquer descrição.

Ao final, liste o que foi alterado e o que foi preservado intencionalmente. Justifique sua resposta.
```

### Revisar a qualidade do dicionário

Use quando quiser avaliar se um dicionário já existente segue os critérios de qualidade e as convenções da própria skill (completude, consistência, terminologia, distinções documentadas), sem alterar nenhum arquivo e independentemente de a codebase ter mudado.

```text
Use a skill `dicionario-dados-db-scan-codebase-docs` para revisar a qualidade e a consistência do dicionário de dados de <sistema ou módulo>, sem alterar nenhum arquivo.

Classifique cada achado como problema de qualidade documental (descrição incompleta, inconsistente, genérica ou fora das convenções da skill) ou como lacuna (elemento sem descrição). Liste claramente qualquer lacuna que impeça considerar a documentação completa. Justifique sua resposta.
```

### Gerar prints de tela como insumo complementar

Use quando, antes de rodar o prompt, já existir um ambiente de teste do alvo disponível (local ou remoto) e uma ferramenta de automação de navegador (Playwright, Selenium etc.) configurada no seu projeto. Os prints gerados aqui podem ser apontados como material complementar no exemplo "Criar o dicionário de dados".

```text
Gere os prints de tela de <sistema ou módulo> para servir de insumo complementar ao
dicionário de dados (skill `dicionario-dados-db-scan-codebase-docs`).

O ambiente de teste de <sistema ou módulo> já está disponível em <endereço ou instrução
para subir o ambiente>. Para autenticar, leia a credencial de <variável de ambiente
ou arquivo local não versionado>. Se não houver, peça a credencial no momento do uso.
Nunca use credencial de produção.

Use <ferramenta de automação de navegador disponível no seu ambiente> para rodar um
script de automação que:

1. Faça login no ambiente de teste.
2. Navegue por todas as telas relevantes de <sistema ou módulo>, criando os dados de
   teste (seeds) necessários para preencher cada tela.
3. Capture um print de cada tela relevante (listagem, formulário vazio, formulário
   preenchido, modal, estado intermediário).
4. Salve os PNGs em <pasta de destino>/<nome-do-alvo>/screenshots/, organizados
   por subpasta.
5. Exporte os seeds/dados de teste usados no passo 2 (SQL de insert ou passo a passo
   reprodutível) em <pasta de destino>/<nome-do-alvo>/seeds/, para reaproveitar
   em futuras implementações sem recriar a massa de teste do zero.

Ao final, liste as telas que não conseguiu capturar e o motivo. Justifique sua resposta.
```
