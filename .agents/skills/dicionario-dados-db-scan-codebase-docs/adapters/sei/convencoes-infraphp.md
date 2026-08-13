# Convenções da família InfraPHP

Aplique este arquivo somente com `sei.md`, `sip.md`, `julgar.md` ou `modulos/padrao.md`. Ele traduz construções técnicas de InfraPHP para a análise de dados; o contrato, o alcance e as decisões do alvo ficam no adaptador selecionado.

## Codificação

- Código PHP e scripts de release destes alvos são lidos como ISO-8859-1. Para preservar texto de evidência, use `iconv -f ISO-8859-1 -t UTF-8` ou uma leitura com `encoding='latin-1'`.
- Markdown do repositório é UTF-8, salvo exceção verificada e declarada pelo adaptador ou overlay do alvo.
- Em `.wsdl`, `.json` e `.html`, respeite a declaração do próprio arquivo quando existir; sem declaração, valide a codificação antes da leitura.
- Use busca binária segura, como `grep -a`, em PHP InfraPHP. Bytes altos podem fazer uma busca textual comum omitir resultados.

## Linguagem e persistência

Estes alvos usam PHP sobre InfraPHP. Estado persistido é modelado por `InfraDTO` e acessado por RN e BD; scripts de release usam `BancoSEI`, `BancoSip` ou outro `InfraIBanco`.

## APIs estruturais

Considere efeito estrutural o SQL DDL executado por `BancoSEI`, `BancoSip` ou outro `InfraIBanco`, e as operações equivalentes de `InfraMetaBD` ou do banco.

| Efeito | Construções reais |
|---|---|
| Tabela | `CREATE TABLE`, `DROP TABLE` via `executarSql` |
| Coluna | `adicionarColuna`, `alterarColuna`, `excluirColuna`, `ALTER TABLE` |
| Chave primária | `adicionarChavePrimaria`, `excluirChavePrimaria` |
| Chave estrangeira | `adicionarChaveEstrangeira`, `excluirChaveEstrangeira` |
| Índice | `criarIndice`, `excluirIndice`, `CREATE INDEX`, `DROP INDEX` |
| Sequencial nativo | `criarSequencialNativa` em `BancoSEI`, `BancoSip` ou outro banco InfraPHP |
| Inspeção | `obterTabelas`, `obterColunasTabela`, `obterIndices`, `obterConstraints` |

`INSERT`, `UPDATE` e `DELETE` alteram dados, não a estrutura. Uma chamada de inspeção também não altera estrutura; use-a apenas para entender condições que controlam um DDL.

Tabela cujo nome é `seq_<algo>` ou contém o segmento `_seq_` (por exemplo `seq_serie`, `md_pen_seq_bloco`) é o controle sequencial técnico produzido por `criarSequencialNativa` para emular sequência nativa em banco sem suporte próprio; não tem significado de negócio. Ignore-a na criação e na atualização do dicionário: não crie entrada em `dicionario_tabelas.md`, `dicionario_colunas.md` nem no índice de nenhum alvo desta família. `infra_sequencia`, a tabela de controle central do próprio InfraPHP, não é abrangida por esta exclusão.

Esta exclusão vale somente para `dicionario_tabelas.md`, `dicionario_colunas.md` e o índice. `CHANGELOG.md` continua registrando toda mudança estrutural sobre tabela `seq_<algo>` normalmente, como registra para qualquer outra tabela: ele é o histórico estrutural do alvo, não o dicionário de negócio, e esta regra não autoriza omitir, remover nem retroagir sobre entradas já publicadas nele.

## Tipos

Traduza o retorno destas APIs para o tipo físico produzido pelo banco selecionado:

| API InfraPHP | Família de tipo |
|---|---|
| `tipoNumero` | número inteiro |
| `tipoNumeroGrande` | número inteiro de maior capacidade |
| `tipoTextoFixo` | texto de tamanho fixo |
| `tipoTextoVariavel` | texto de tamanho variável |
| `tipoTextoGrande` | texto longo |
| `tipoDataHora` | data e hora |

Preserve tamanho, nulidade e valor padrão declarados na chamada ou no SQL. Literal como `char(1)`, `bigint` ou `varchar(255)` continua sendo evidência estrutural direta.

## Classes de banco

As ramificações multi-SGBD podem usar `InfraMySqli`, `InfraPostgreSql`, `InfraOracle` e `InfraSqlServer`. `InfraMySqli` estende `InfraMySql`; confira a classe efetivamente testada pelo script e não troque uma pela outra ao interpretar a condição.

`BancoSEI::getInstance()` e `BancoSip::getInstance()` fornecem o `InfraIBanco` do respectivo lado. Uma ramificação específica só qualifica o resultado por SGBD quando os efeitos finais realmente divergirem.

## Mapeamento de camadas

O adaptador do alvo atribui status e caminhos concretos a cada tipo. Use este mapa técnico para reconhecer os artefatos:

| Tipo de evidência | Artefatos InfraPHP usuais |
|---|---|
| Documentação funcional | `README.md` e outros `.md` do alvo |
| Definição estrutural | scripts PHP de release e DDL literal |
| Modelo ou contrato de dados | `*DTO.php` em `dto/` |
| Regra de negócio | `*RN.php` em `rn/` |
| Contrato de integração | `*Integracao.php`, `api/`, `ws/`, `.wsdl` e `.json` de contrato |
| Consulta e projeção | `*BD.php` em `bd/`, `consultarSql`, aliases e junções |
| Apresentação e interface | páginas PHP, `.html` do alvo e `*INT.php extends InfraINT` em `int/` |
| Comportamento de tela | `.js` e PHP que gera JavaScript |
| Operação de escrita | métodos `*Controlado`, `*Conectado` e escritores em `*RN.php` |
| Enumeração e constante | constantes e propriedades estáticas em RN, DTO, integração e JavaScript |
| Relatório | páginas e exportadores de relatório em `.php` ou `.html` |
| Teste e massa de dados | testes, fixtures PHP e massas `.json` |
| Comentário no código | comentários próximos da implementação verificável em qualquer arquivo aplicável |

O nome da pasta não fixa seu papel. Confirme pelo conteúdo se `int/`, `api/`, `ws/` ou `bd/` implementa o tipo de evidência atribuído pelo adaptador.

## Técnicas de busca

### Ordem de investigação

Ao apurar o significado de uma tabela ou coluna, percorra as camadas nesta ordem, expandindo para a próxima somente nos termos ainda não resolvidos:

1. **DTO** (`dto/`): nome físico, atributo lógico, tipo e comentário; a âncora que conecta as demais camadas.
2. **BD** (`bd/`): como o campo é filtrado, ordenado e unido a outras tabelas; revela relação e uso, não só estrutura.
3. **RN** (`rn/`): quando o campo é preenchido, validado, calculado ou recebe valor padrão; normalmente é onde o significado de negócio mora.
4. **Páginas e `int/`**: rótulo, opção de domínio e texto de ajuda exibidos ao usuário; o vocabulário de negócio efetivamente visível.
5. **JavaScript**: comportamento condicional e validação client-side; pode revelar regra ausente no lado servidor.
6. **Integração** (`*Integracao.php`, `api/`, `ws/`): nomenclatura do contrato externo; cruze com o significado interno, não substitua por ele.
7. **Testes e massas**: valores concretos, úteis para confirmar domínio e status.
8. **Documentação** (`README.md`, manuais): melhor fonte de prosa sobre significado quando existir, mas nunca aceita sem confronto com o código.

Essa ordem prioriza onde procurar primeiro. A autoridade final por dimensão (estrutura, escrita, significado, domínio, uso) continua sendo a de `processo-analise-semantica.md`.

### Chaves de busca

Monte chaves InfraPHP para cada tabela e coluna:

- nome físico, como `id_usuario`;
- atributo DTO em PascalCase, como `IdUsuario`;
- acessores tipados, como `getNumIdUsuario`, `setNumIdUsuario` e `retNumIdUsuario`;
- variantes de prefixo `Num`, `Dbl`, `Str`, `Dth` e `Bol`;
- constantes de RN ou integração comparadas com o atributo;
- aliases SQL, filtros de DTO e nomes de relacionamento declarados no DTO;
- rótulos e valores enviados por página ou JavaScript.
- prefixos físicos `id_`, `sin_`, `dth_` e `sta_` apenas como pistas de identificação, condição, tempo e domínio.

Na busca indireta, localize assinaturas que recebem o atributo e depois seus chamadores. Na busca por consulta, inclua `consultarSql`, `executarSql`, `SELECT`, `JOIN`, `WHERE` e aliases. Use apenas as raízes e extensões declaradas pelo adaptador e exclua dependências vendorizadas, salvo referência direta do código do alvo.

## Vocabulário de negócio

Estes termos são legados na estrutura física do SEI, mas o vocabulário de negócio usado por usuário, manual e documentação funcional é outro. Ao redigir prosa (descrição de tabela, descrição de coluna e demais textos livres do dicionário), traduza os termos abaixo; nunca altere o identificador físico correspondente.

| Termo físico/legado (prosa) | Termo de negócio a usar na prosa |
|---|---|
| procedimento | processo |
| tipo de procedimento | tipo de processo |
| série | tipo de documento |

- Aplique a tradução somente em prosa; identificador físico preserva a forma definida em "Identificadores e âncoras", inclusive quando citado entre crases dentro de uma frase. Ajuste artigo, adjetivo e pronome da frase para manter a concordância correta em português com o termo de negócio substituído; não é necessária uma regra mecânica passo a passo para isso.
- Não aplique a tradução de `série` quando o termo não se referir à classificação do tipo de documento do SEI (por exemplo, série histórica ou série temporal).
- CHANGELOG.md relata efeito estrutural sobre o identificador físico; não aplique esta tradução a ele.

## Identificadores e âncoras

- Tabela, coluna e objeto técnico usam o identificador físico não vazio e em uma única linha, exatamente como emitido pela fonte estrutural. O padrão não qualificado desta família é `[a-z][a-z0-9_]*`; qualificação por esquema separa componentes por ponto. Caixa, qualificação ou citação fora desse padrão exigem declaração no adaptador ou overlay e validação manual.
- A identificação usual é `id_{tabela}`; chave composta pode não ter identificador próprio. `seq_*` e `*_idx` são objetos técnicos.
- Atributos DTO removem sublinhados e usam PascalCase; o prefixo do acessor indica o tipo lógico, não integra o nome físico.
- Escape `|` como `\|` somente na representação Markdown; ele continua sendo parte do identificador físico para comparação.
- Para a âncora, converta o identificador para minúsculas, remova caracteres que não sejam letras, números, sublinhado, hífen ou espaço e substitua cada espaço por `-`. Em colisões, preserve a primeira âncora e acrescente `-1`, `-2` e assim por diante, na ordem das seções.

## Versionamento comum

A versão-alvo desta família aceita três componentes numéricos. Publique-a como `vM.m.p` nos dicionários e como `M.m.p` no relatório e entre colchetes no `CHANGELOG.md`. Use `^v[0-9]+\.[0-9]+\.[0-9]+$` no `formato` e `^[0-9]+\.[0-9]+\.[0-9]+$` no `changelog`. A ordem histórica vem da fonte estrutural declarada pelo adaptador, nunca de comparação textual. Um overlay pode ampliar esta gramática (por exemplo, sufixo de pré-release) declarando a exceção explicitamente.

### Adaptadores baseados em `setArrVersoes`

Aplicável a SEI, SIP e Julgar, salvo exceção declarada pelo adaptador.

- Âncora de versão: entrada de `setArrVersoes` mais o método apontado.
- Assinatura de bloco: `public function versao_M_m_p($strVersaoAtual)` em SEI e SIP; Julgar declara a própria assinatura no adaptador.
- Baseline e alcance: inspecione o mapa completo a cada execução. Só reconheça baseline quando o primeiro caminho executável comprovar a instalação integral do esquema; caso contrário, limite atualização e verificação aos blocos comprovados e bloqueie criação ou reconstrução integral.
- Bloqueios: criação ou reconstrução integral sem baseline comprovado bloqueia; versão-alvo ausente ou divergente bloqueia escrita e validações dependentes da versão, com verificação parcial permitida no alcance comprovado, fontes reportadas e sem escolha de precedência.

## Relatório de atualização

- Nome: `dicionario-de-dados-<slug-do-destino>-atualizacao-<versao-sem-prefixo-v>.md`.
- Título: `Alterações — <titulo comum do dicionario> (atualização para <versao-sem-prefixo-v>)`.
- `<slug-do-destino>` é o nome exato da pasta de publicação declarada pelo adaptador. Preserve eventual sufixo da versão-alvo ao remover somente o prefixo de apresentação `v`.
- Destino: `specs/`, quando a skill exigir o relatório.
