# Formato dos dicionários de dados

Especificação extraída dos dicionários existentes (`docs/dicionario_dados/sei/dicionario.md`,
`docs/dicionario_dados/sip/dicionario.md`, `docs/dicionario_dados/litigioso/dicionario.md`) e da
atualização do dicionário SEI para a versão 5.0. Seguir à risca — não introduzir variação de estilo
entre dicionários.

## Onde o arquivo vive

- Um dicionário por módulo, em pasta própria: `docs/dicionario_dados/<modulo>/dicionario.md`.
  Pasta própria mesmo quando o módulo tem só 1 arquivo hoje — decisão deliberada do desenvolvedor
  para já prever módulos que precisem de mais de um arquivo no futuro (ex.: `litigioso/` tem
  `dicionario.md` + `dicionario-completo.md`).
- `docs/dicionario_dados/` é versionado e autorizado para escrita pelo `AGENTS.md`; `specs/` está
  no `.gitignore` (ver `README.md` e `.gitignore` na raiz — não confiar de cabeça, conferir se o
  projeto ainda segue essa convenção).
- Variante "original"/histórica de um módulo (ex.: espelha 1:1 uma planilha-fonte que não reflete
  mais o schema atual) vai para `specs/<nome-descritivo>.md`, fora do `docs/` publicado — é
  material de referência local, não o dicionário corrente.
- Changelog de uma atualização (diff entre versão antiga e nova) também vai para `specs/`, nunca
  dentro do próprio dicionário — ver seção "Changelog de atualização" abaixo.

## Encoding

Esses `.md` são UTF-8 puro. `.gitattributes` só força `working-tree-encoding=iso-8859-1` para
`*.php` — não se aplica aqui. `Edit`/`Write` podem ser usados normalmente, sem risco de corromper
acentos (diferente do que vale para PHP, ver `AGENTS.md`).

## Estrutura do documento

```text
# Dicionário de Dados do Módulo <Nome do módulo, conforme Integracao::getNome()> - v<versão>

ou, para o núcleo do sistema (não é módulo):

# Dicionário de Dados do SEI - v<versão>
# Dicionário de Dados do SIP - v<versão>

## Índice de Tabelas

- [tabela_a](#tabela_a)
- [tabela_b](#tabela_b)
...

## tabela_a

<frase descritiva>

| Coluna | Descrição |
|---|---|
| ... | ... |

## tabela_b
...
```

Sem seção `## Tabelas` envolvendo as tabelas — cada tabela é uma seção `##` própria, direto após o
índice. Regra única, sem exceção por alvo.

Regras:

- **Sem linha de origem/fonte e sem parágrafo de metodologia.** Nada de `> Fonte:`, "Gerado a
  partir de...", "Conferido contra...". O título vai direto para `## Índice de Tabelas`.
- **Sem seção de metodologia, divergências ou recomendações.** O documento é só descrição +
  dicionário. Nada de nota técnica, crítica ou hedge tipo "não confirmado, validar com
  desenvolvedor". Ressalva sobre lacuna de evidência vai na resposta ao desenvolvedor, nunca no
  `.md`.
- **Índice em ordem alfabética estrita**, sem exceção, e batendo 1:1 com as seções `## tabela`
  (mesmo conjunto, mesma ordem).
- **Seções `## tabela` também em ordem alfabética estrita** ao longo de todo o documento — não
  agrupar por funcionalidade dentro do dicionário principal (ver seção "Por que alfabético, não
  por funcionalidade" abaixo).
- Cada seção de tabela:
  1. `## nome_tabela`
  2. Uma frase descritiva em português, sem bullet, curta e factual. Aberturas comuns já usadas:
     "Armazena...", "Administração de/dos...", "Associativa entre... e...", "Registra...",
     "Referencia...".
  3. Linha em branco, depois tabela markdown `| Coluna | Descrição |` / `|---|---|`.

## Ordem das colunas dentro de cada tabela

Regra confirmada por precedente no arquivo (ex.: `documento_conteudo`, que tem apenas
`id_documento` como FK e está **totalmente alfabético**, sem promoção):

- Se existir uma coluna com nome **exatamente igual a** `id_<nome_da_tabela>` (PK própria por
  convenção de nomenclatura), ela vem primeiro; todas as demais colunas em ordem alfabética
  estrita depois dela.
- Se a tabela **não** tiver uma coluna `id_<nome_da_tabela>` — por exemplo, tabelas de extensão
  1:1 cuja chave é uma FK como `id_usuario` (`usuario_login`, `usuario_configuracao`) — **não**
  promover essa FK para o topo. Ordem totalmente alfabética, sem exceção.
- Erro já cometido e corrigido numa atualização real: promover `id_usuario`/`id_procedimento`
  para o topo em tabelas sem `id_<nome_da_tabela>` própria. Conferir sempre com o script de
  validação (subcomando `schema` com `--checar-ordem`, ver `SKILL.md`) antes de considerar pronto.
- Tabelas `seq_*` e `*_idx` não seguem necessariamente esse padrão de PK (`seq_*` costuma ter só
  1-2 colunas técnicas) — o script de validação já exclui essas do check de ordenação.

## Templates de descrição de coluna

Não inventar frase nova por tabela — seguir o padrão já estabelecido por prefixo/sufixo de nome:

| Padrão de nome | Template | Observação |
|---|---|---|
| `id_x` (PK ou FK) | "Número ID que identifica [o/a] x [da/do entidade]." | |
| `sin_x` (`char(1)`, domínio S/N) | "Variável categórica que indica se [afirmação]:" + lista `<ul><li>S = ...</li><li>N = ...</li></ul>` | Mesmo padrão de lista do `sta_x` (ver seção abaixo) — nunca a frase crua terminada em "(S) ou não (N)". |
| `sta_x` (status, sempre multi-valorado) | "Status multi-valorado que identifica..." + lista dos códigos reais | **A palavra "multi-valorado" é obrigatória na frase-resumo, mesmo sem código conhecido.** Nunca inventar os códigos. RN é só uma das camadas de evidência — não parar nela; ver a ordem de prioridade completa (README → DTO → RN → páginas) logo abaixo antes de concluir "sem evidência". |
| `dth_x` / `dta_x` | "Data/hora de..." / "Data de..." | |
| Texto livre (`nome`, `descricao`, `observacao`, etc.) | "Armazena..." | |

### Lista de códigos dentro da célula (`sta_x`, `sin_x` e equivalentes)

Célula de tabela Markdown não renderiza `- item`/`1. item` (vira texto literal com o traço) — por
isso a lista de códigos usa HTML inline, que os renderizadores de tabela do GFM aceitam. Regra
universal, para qualquer dicionário — vale tanto para domínio multi-valorado (`sta_x`) quanto para
domínio binário S/N (`sin_x`):

```text
| sta_x | Status multi-valorado que identifica X:<br><br><ul><li>1 = Descrição do código 1</li><li>2 = Descrição do código 2</li></ul> |
| sin_x | Variável categórica que indica se [afirmação]:<br><br><ul><li>S = Rótulo curto da afirmação</li><li>N = Não + o mesmo rótulo, ou o rótulo oposto quando este for mais natural</li></ul> |
```

- Frase-resumo termina em `:`, seguida de `<br><br>` (não `<br>` simples) antes da lista — é o
  separador entre a frase e o início da lista.
- Cada código vira um `<li>CÓDIGO = Descrição</li>` dentro de um único `<ul>...</ul>`, tudo na
  mesma linha da célula (célula de tabela é uma linha só no `.md` — nunca quebrar `<ul>`/`<li>` em
  múltiplas linhas de arquivo).
- Nota/ressalva que não é código (ex.: "Não se aplica à distribuição por peso") fica **fora** do
  `<ul>`, depois dele, separada por um único `<br>` (não `<br><br>` — só a abertura da lista usa
  dois) — não vira `<li>`. Exemplo real (`julgar`, coluna `contador`):
  `...:<br><br><ul><li>0 = ...</li><li>1 = ...</li></ul><br>Não se aplica à distribuição por peso`
- Frase condicional em prosa (sem formato `código = descrição`) não é lista — mantém só `<br><br>`/
  `<br>` como já era, não force `<ul>` nela.
- Não inventar nem reordenar os códigos — a lista reflete exatamente a evidência encontrada na
  constante de classe (mesma regra de evidência da tabela de templates acima).

Casos especiais:

- `sin_x`: o rótulo de cada item **não repete o sujeito nem a cópula** já citados na frase-resumo —
  extrai só o predicado. Ex.: frase "...indica se o campo está ativo:" → `<li>S = Ativo</li><li>N =
  Não ativo</li>` (não `<li>S = O campo está ativo</li>`). Quando existir antônimo natural e mais
  claro que "Não X" (ex.: Ativo/Inativo), pode usar o antônimo — mas "Não X" nunca está errado e é
  a opção segura quando não houver antônimo óbvio.
- `sin_x` com domínio S/N onde os dois valores **não são afirmação/negação simétrica** (ex.: S = uma
  alternativa, N = outra alternativa igualmente positiva) — não forçar "não" artificial; usar o
  rótulo real de cada lado. Ex.: `<li>S = Endereço do contato associado</li><li>N = Endereço próprio
  do contato</li>`.
- Coluna com prefixo `sin_` mas domínio **não é S/N** (ex.: `I`/`M`, `P`/`C`/`N`) é inconsistência de
  nomenclatura pré-existente — reformatar a célula com a mesma estrutura de lista (`<ul><li>código =
  descrição</li></ul>`), mas não simular um domínio S/N que não existe; a inconsistência de nome em
  si é observação à parte, não bloqueia a formatação da célula.
- Campo sem prefixo `sta_` mas com domínio fechado e códigos explícitos na fonte pode usar o mesmo
  estilo de lista de itens, desde que a evidência esteja no código ou na planilha oficial.
- Campo `id_*` usado semanticamente como enumeração ou classificação não deve receber descrição de
  PK/FK por inferência. Se a fonte o tratar como domínio fechado, seguir a fonte e descrever o uso
  factual.
- Se a planilha oficial contradisser o prefixo do campo, priorizar a semântica comprovada da fonte,
  não o prefixo do nome isoladamente.

**Esta ordem de evidência vale para todo campo sendo documentado durante a varredura da tabela —
frase-resumo, descrição de coluna comum, domínio de `sta_*`/`tipo_*`, tudo.** Não é regra exclusiva
de status multi-valorado; é o método de pesquisa padrão para qualquer nome ou descrição que não
esteja óbvio de cabeça. Ordem de prioridade:

1. README e demais documentos funcionais específicos do módulo.
2. DTO correspondente (`fontes/.../dto/*.php` ou `fontes/.../modulos/<modulo>/dto/*.php`) —
   getters/setters e PHPDoc.
3. RN correspondente (`.../rn/*.php`) — regras de negócio e constantes de domínio.
4. Páginas de cadastro/lista (`.../modulos/<modulo>/*.php` ou `sei/web/*.php`) — labels de campo
   visíveis ao usuário, que costumam ser a fonte do fraseado já usado no dicionário. **Não é só
   fallback de texto**: o significado real de um campo — qualquer campo, não só domínio de
   `sta_*`/`tipo_*` — às vezes só existe como literal no HTML da página (`value="X"` de rádio/
   select, label de `<input>`, às vezes montado em JS), sem nenhuma constante nomeada em RN nem
   PHPDoc no DTO. Achado real no `peticionamento`: `sta_tp_cliente_ws` está documentado sem código
   porque a busca parou em DTO+RN — o valor `'S'` (SOAP) está só no
   `<input type="radio" ... value="S">` da página de cadastro. O mesmo risco vale pra um campo de
   texto livre cujo rótulo de negócio só aparece como `<label>` na página, não em comentário de RN.

**Não concluir "sem evidência" para nenhum campo antes de chegar à camada 4** — vale para domínio
de `sta_*`/`tipo_*`, mas também pra frase-resumo de tabela e descrição de coluna comum. DTO e RN não
terem a informação não é prova de que ela não existe — pode estar só na página. Técnica prática:
`grep -rla "NomeDoAtributo\|getNomeDoAtributo"` na pasta inteira do módulo (não só `dto/`/`rn/`),
incluindo os arquivos `.php` de página e `.js` — pega qualquer camada de uma vez, pra qualquer
campo.

**O nome da pasta `int/` não tem papel fixo entre módulos — conferir antes de assumir.** Em alguns
módulos é a camada de API externa (`Entrada*API`/`Saida*API`); no `peticionamento`, por exemplo, são
classes `extends InfraINT` que só montam fragmento de tela (ex.: `<select>` de hipótese legal) — a
API externa de verdade fica em `ws/` (`*APIWS.php`). Não citar `int/` como evidência de contrato de
API sem antes confirmar o que a classe realmente faz.

**Qualquer descrição encontrada em RN gerada por ferramenta pode ser placeholder nunca preenchido —
não é evidência real, seja de valor de domínio, de coluna comum ou de tabela.** Achado real
(`litigioso`, `md_lit_campo_integracao.sta_parametro`):
`MdLitCampoIntegracaoRN` confirma os valores (`$PARAMETRO_1 = 'A'` etc.), mas o método
`listarValoresParametro()` que deveria descrever cada um retorna literalmente `'Descrição Parametro
1'`, `'Descrição Parametro 2'`, `'Descrição Parametro 3'` — texto de gerador de código (CRUD) nunca
customizado, não descrição de negócio. Antes de usar uma string de descrição encontrada em RN como
evidência, checar se não é um placeholder desse tipo (padrão comum: "Descrição X N", nome genérico
igual ao nome da constante). Se for, tratar como **sem evidência de significado** mesmo com os
valores confirmados — não inventar `A = X`, `B = Y` a partir do placeholder.

**No dicionário, nunca citar RN/constante/gerador de código como justificativa — isso é
metodologia, não descrição de negócio** (mesma regra de "sem parágrafo de metodologia" já vale
aqui). Usar `<br><br>**Observação:** <texto>` dentro da própria célula para sinalizar que a
descrição precisa de verificação — mesmo rótulo em negrito já usado na flag `(legado)` de tabela,
aplicado aqui no nível de coluna. **Só se aplica quando sobrar conteúdo de negócio real e útil para
o leitor** — não basta confirmar que os caracteres literais do código existem (`A`, `B`, `C` sem
descrição nenhuma anexada não é conteúdo de negócio, é só um rótulo vazio; tratar como "não sabemos
os valores", caso `TODO:` abaixo, não como `Observação:`). Uso legítimo é quando a maior parte do
domínio já tem significado descrito e só uma parte pontual fica em aberto — nesse caso a frase-resumo
já é útil por si só, e a `Observação:` sinaliza apenas o resíduo não confirmado.

### Coluna multi-valorada sem nenhuma evidência aproveitável (`TODO:`)

Caso diferente do `**Observação:**` acima — ali sobra conteúdo de negócio real depois da pesquisa
(ainda que incompleto). Aqui a lacuna é maior: depois de esgotar toda a ordem de prioridade de
evidência (README → DTO → RN → páginas), não sobrou frase-resumo aproveitável nenhuma — nem os
códigos com significado atribuído (`sta_x` e equivalentes; confirmar que o caractere existe no
código, sozinho, sem descrição de negócio anexada, **não conta** como frase aproveitável — achado
real: `litigioso`, `md_lit_campo_integracao.sta_parametro`, onde `A`, `B`, `C` são confirmados como
caracteres reais em `MdLitCampoIntegracaoRN`, mas nenhum deles tem significado de negócio descrito,
então é `TODO:`, não `Observação:`) nem a própria afirmação que a coluna testa (`sin_x`). Marcar a
célula com a frase padrão abaixo, em negrito (destaque para revisão manual posterior), separada do
que já existir por `<br><br>`:

```text
| sta_x | Status multi-valorado que identifica X.<br><br>**TODO:** Esta coluna é multivalorada e não foi possível arbitrar o significado de negócio de seus valores baseado apenas no código. Necessária revisão humana! |
| sin_x | Variável categórica que indica se(S) ou não (N).<br><br>**TODO:** Esta coluna é multivalorada e não foi possível arbitrar o significado de negócio de seus valores baseado apenas no código. Necessária revisão humana! |
```

- Frase fixa, não parafrasear: "TODO: Esta coluna é multivalorada e não foi possível arbitrar o
  significado de negócio de seus valores baseado apenas no código. Necessária revisão humana!" — só
  o rótulo `**TODO:**` em negrito, mesmo padrão de `**Observação:**` (que também só negrita o
  rótulo), texto do motivo sem negrito. A frase fala da **coluna**, não da tabela — mesmo repetida em
  várias colunas da mesma tabela, cada uma recebe sua própria marcação.
- **"Significado de negócio", não "valores"**: em `sin_x` os valores (`S`/`N`) já são sempre
  conhecidos por definição de template — nunca estão em dúvida. O que falta é o significado de
  negócio por trás de cada valor (a afirmação/condição que o `S` representa). Escrever "não foi
  possível arbitrar a descrição de seus valores" nesse caso soa contraditório, já que a própria
  frase-resumo mostra `(S) ou não (N)` — por isso a frase fixa fala em "significado de negócio de
  seus valores", não em "valores" isolado, e vale igual para `sta_x` (onde o próprio código, além do
  significado, também está em aberto).
- Não inventar código nem tentar redigir "significado provável" — a frase-resumo (quando existir
  algo, caso `sta_x`) mantém só o que o prefixo do nome já garante (ex.: a palavra "multi-valorado"
  obrigatória, ver tabela de templates acima), sem lista `<ul>`.
- **Critério para escolher `TODO:` vs `**Observação:**`**: sobra descrição de negócio real e útil
  para o leitor, mesmo que incompleta (ex.: maior parte do domínio já descrita, só uma parte pontual
  em aberto) → `**Observação:**`. Não sobra nada de útil (frase vazia/quebrada tipo "indica se(S) ou
  não (N)." sem afirmação nenhuma; coluna `sta_x` cujo código real não foi encontrado em lugar
  nenhum; ou coluna `sta_x` cujo(s) código(s) foram confirmados como caracteres reais mas nenhum tem
  significado de negócio atribuído — conhecer só a letra/número sem descrição não é frase
  aproveitável) → `TODO:`. Vale para `sta_x` e para `sin_x` igualmente — a diferença não é o prefixo
  do nome, é se sobrou algo de negócio escrito para o leitor ou não.
- Para `sin_x` especificamente: antes de concluir "sem frase aproveitável", buscar a afirmação pela
  ordem de evidência normal (README → DTO → RN → páginas) até o fim; achado real (`sei`,
  `rel_secao_modelo_estilo.sin_padrao`): RN não documenta, mas a página `secao_modelo_cadastro.php`
  tem o `<label for="selEstiloPadrao">Estilo Padrão:</label>` que resolve a afirmação ("se o estilo é
  o estilo padrão da seção do modelo") sem precisar de qualquer marcação de lacuna. Só marcar `TODO:`
  depois de esgotar todas as camadas.
- Não usar texto ad hoc tipo "Não foi possível entender a lógica de funcionamento" — a frase padrão
  acima é a única forma aceita de sinalizar essa lacuna, para permitir busca/grep consistente por
  pendências de revisão em qualquer dicionário.

Se a regra de negócio não estiver documentada, perguntar ao desenvolvedor. Não inventar regra de
negócio sem evidência. Descrição conservadora e factual é melhor que uma frase elaborada e não
verificável — mantém o tom enxuto já usado nos arquivos existentes.

Para módulo customizado, o DDL acumulado até a versão-alvo define a estrutura persistida e o DTO é
a conferência obrigatória. Divergência entre ambos bloqueia o trabalho até decisão do
desenvolvedor.

## Flags de status no nome da tabela (`(legado)` / `(removida)`)

Convenção usada no módulo litigioso quando o dicionário precisa registrar uma tabela que existe no
banco mas está fora de uso (`(legado)`) ou que só existe na variante "original"/histórica porque já
foi removida do schema atual (`(removida)`):

- A flag aparece junto ao nome, tanto no `## Índice de Tabelas` quanto no `## nome_tabela`:
  `md_lit_assoc_disp_normat (legado)`, âncora vira `#nome-legado`.
- Usar só quando fizer sentido manter a tabela documentada apesar do status — quando a tabela
  simplesmente não existe mais em nenhuma variante do dicionário, ela é removida do arquivo, não
  flegada (foi o que aconteceu com `velocidade_transferencia` na atualização do SEI 5.0: não há
  variante "completa" do dicionário SEI que precise preservá-la, então foi removida, não flegada).
- **Tabela `(legado)` exige uma linha de observação do motivo**, logo após a frase descritiva e
  antes da tabela markdown, no formato `**Observação:** <texto sem negrito>` (rótulo em negrito,
  texto do motivo não). Buscar evidência real no script de instalação do módulo (migração de dados
  sem drop da tabela antiga é o caso mais comum) antes de escrever. Quando a tabela de destino da
  migração for identificável, citar o nome dela; motivo desconhecido não bloqueia a flag, mas usar
  o texto-padrão em vez de inventar detalhe: "Os dados da tabela foram migrados para a tabela
  `<tabela-destino, se souber>`, porém não foi removida do banco de dados." Exemplo real:
  `md_lit_assoc_disp_normat (legado)` no dicionário litigioso.

## Por que alfabético, não por funcionalidade

Alfabético é a escolha padrão, sem exceção. "Dicionário"
pressupõe busca por nome; `sip` e `litigioso` já seguem esse padrão; muitas tabelas nucleares
(`unidade`, `usuario`, `documento`, `protocolo`, `orgao`...) são compartilhadas por várias
funcionalidades ao mesmo tempo, então agrupar por funcionalidade geraria ambiguidade sobre onde
cada uma entra. Quando uma visão agrupada por funcionalidade é útil (ex.: revisar de uma vez só as
15 tabelas novas do Plano de Trabalho), isso vira o changelog em `specs/`, não uma reestruturação
do dicionário principal.

## Changelog de atualização

Quando uma atualização de dicionário existente adiciona/remove tabelas ou colunas ou altera
descrições, gerar um arquivo separado em
`specs/dicionario-de-dados-<modulo>-atualizacao-<versao>.md` (local, não versionado) — nunca
misturar isso dentro do dicionário publicado. Estrutura:

```text
# Changelog do Dicionário de Dados <Nome>

## Resumo
<tabela com contagem de tabelas/colunas antes e depois>

## [<versão mais recente>]

### Adicionado
#### Tabela **`nome_tabela_nova`**
<descrição e tabela Markdown com todas as colunas criadas>

### Modificado
#### Tabela **`nome_tabela_existente`**
<uma linha por coluna alterada>

### Removido
#### Tabela **`nome_tabela_removida`**
<motivo da remoção ou uma linha por coluna removida>

## [<versão anterior>]
...

## Fontes e limitações
<fontes utilizadas e lacunas de evidência>
```

As versões ficam em ordem decrescente. Este é um relatório detalhado de comparação do dicionário,
usado inclusive para confrontar planilhas históricas: uma tabela por subtópico, identificadores em
código e negrito e uma linha por coluna. Tabela criada exige a enumeração completa das colunas do
`CREATE TABLE`. Esse detalhamento é específico do relatório em `specs/` e não deve ser replicado no
`CHANGELOG.md` histórico permanente, cujo formato simples está definido abaixo.

Gerar esse diff **programaticamente** (parsing dos dois arquivos, não de memória) — ver o
subcomando `comparar_schema.py diff` no `SKILL.md`. Uma contagem feita de cabeça já divergiu do
resultado real numa atualização passada (relatório dizia "19 colunas adicionadas", o recálculo
automático achou 24).

## CHANGELOG.md histórico

Diferente do "Changelog de atualização" acima (relatório avulso de uma única atualização, em
`specs/`, não versionado): este é o histórico **completo e permanente** versionado junto do
dicionário em `docs/dicionario_dados/<alvo>/CHANGELOG.md`.

O procedimento de **localização da fonte estrutural** (onde está o script/DDL de cada versão) é
diferente conforme o padrão de origem do alvo e por isso não está aqui — está na referência própria
de cada skill consumidora (`sei-dicionario-dados-core` para SEI/SIP/Julgar,
`sei-dicionario-dados-modulo` para módulo customizado). O que segue abaixo é só **formato do
arquivo final**, comum aos dois.

Scripts de origem (de qualquer padrão) costumam ser ISO-8859-1: nunca ler com `Read` direto
(corrompe acento para U+FFFD) — usar `iconv -f ISO-8859-1 -t UTF-8 <arquivo>` ou Python com
`encoding='latin-1'`. Como é só leitura (não edição do `.php`), a regra do `AGENTS.md` contra
`Edit`/`Write` em PHP acentuado não se aplica aqui.

Usar o DDL real (`CREATE TABLE`, `ALTER TABLE`, `DROP`, renomes, chaves e índices) como evidência
estrutural. As mensagens `$this->logar('...')` podem esclarecer a operação técnica, mas o changelog
não recebe descrição negocial das tabelas.

### Filtro de escopo

O CHANGELOG.md é sobre mudanças estruturais: tabelas e, em tabelas preexistentes, colunas, chaves
estrangeiras, chaves primárias e índices. Versão cujo método só mexe em recurso/menu/permissão do
SIP, e-mail, agendamento, dados de referência ou código sem tocar schema **não entra** — omitir a
versão inteira, não criar uma entrada vazia.

Critérios para delta determinístico:

- **Incluir** objeto explicitamente criado, alterado, renomeado ou removido no DDL, inclusive quando
  a alteração for condicionada por SGBD e o efeito final continuar determinístico.
- **Incluir** FK/PK/índice implícito apenas quando a API usada pelo script o cria de modo
  determinístico e nominalmente previsível (ex.: `adicionarChaveEstrangeira()` que sempre cria o
  índice homônimo naquele contexto já comprovado).
- **Não incluir** rotinas genéricas de reparo (`fixIndices()`, `processarIndicesChavesEstrangeiras()`
  e equivalentes) quando o script não provar qual objeto efetivamente mudou em cada banco.
- **Não incluir** recriação idempotente do mesmo objeto quando não houver delta líquido de definição.
- **Consolidar** add/copy/drop do mesmo nome lógico na mesma versão como `Alterado`, não como
  adição+exclusão separadas, quando o resultado final é a mesma coluna/FK/PK/índice com nova
  definição.
- **Tratar como alteração** drop/create da mesma tabela ou do mesmo índice quando o nome lógico é
  preservado e o interesse do changelog é o delta final, não o ritual técnico intermediário.
- **Omitir** versões cujo método exista mas fique vazio após remover comentários e whitespace.

### Cabeçalho de versão

Usar somente `## [X.Y.Z]`, sem data. Data de importação do script no repositório não é data de
lançamento da versão — não atribuir uma coisa à outra.

### Formato do arquivo

**Só título + entradas de versão — sem preâmbulo.** Nada de link para Keep a Changelog, nada de
"este projeto adere ao Versionamento Semântico" (o projeto não adere), nada de nota de
metodologia/"reconstruído por engenharia reversa". Essas explicações não vão no arquivo publicado —
se quiser registrar ressalva sobre lacuna de evidência, reportar ao desenvolvedor na resposta, não
escrever no `.md`.

```text
# Changelog do Módulo <Nome>

## [X.Y.Z]

### Adicionado

- **Tabela `nome_tabela_nova`**

### Alterado

- **Tabela `nome_tabela_existente`**
  - **Colunas**
    - **Nova `nome_coluna_nova`**
    - **Alterada `nome_coluna_alterada`**: <definição anterior> para <definição nova>.
  - **Chaves estrangeiras**
    - **Nova `fk_nome`**
  - **Chaves primárias**
    - **Alterada `pk_nome`**
  - **Índices**
    - **Novo `i01_nome`**

### Excluído

- **Tabela `nome_tabela_removida`**
- **Tabela `outra_tabela_existente`**
  - **Colunas**
    - **Excluída `nome_coluna_removida`**
  - **Chaves estrangeiras**
    - **Excluída `fk_nome`**
  - **Índices**
    - **Excluído `i01_nome`**

## [X.Y.Z anterior]
...
```

Ordem decrescente (mais nova primeiro). Usar somente as categorias que tiverem conteúdo, nesta
ordem: `Adicionado`, `Alterado`, `Excluído`.

Regras do formato simples:

- `Adicionado`: listar somente cada tabela nova como bullet principal. Não enumerar suas colunas,
  chaves ou índices e não incluir descrição negocial.
- `Alterado`: agrupar por tabela preexistente e, dentro dela, pelos tópicos `Colunas`, `Chaves
  estrangeiras`, `Chaves primárias` e `Índices`. Cada objeto adicionado ou alterado recebe um bullet
  próprio dentro do tópico correspondente; adição de coluna em tabela existente também entra aqui,
  não em `Adicionado`.
- `Excluído`: tabela removida aparece somente como bullet principal. Em tabela mantida, cada
  coluna, FK, PK ou índice removido fica no respectivo tópico aninhado.
- Usar os tópicos mesmo quando houver um único objeto e omitir tópicos vazios. FK e índice ficam
  separados porque são objetos distintos e podem variar por SGBD.
- Dentro de cada tópico, o tipo da mudança e o identificador ficam em negrito, conforme o exemplo:
  `Nova`/`Alterada`/`Excluída` para colunas e chaves; `Novo`/`Alterado`/`Excluído` para índices. Não
  reunir vários objetos no mesmo bullet.
- Registrar apenas informação técnica comprovada no DDL. Não acrescentar finalidade negocial de
  tabela ou coluna.
- Não expandir chamadas genéricas e idempotentes de reparo, como `fixIndices()`, em dezenas de
  entradas quando o script não comprovar um delta determinístico para cada índice. Registrar
  índices explicitamente criados, alterados ou excluídos pela versão.
