# Princípios de qualidade do dicionário de dados

Autoridade sobre: conteúdo publicável das descrições e critérios A1 a A10.

## Regra de publicação

Uma descrição deve permitir que alguém entenda o conceito sem abrir o código. Estrutura física pertence à fonte estrutural e ao `CHANGELOG.md`; significado e uso pertencem aos dicionários.

Use integralmente a fórmula obrigatória aplicável. Preencha todos os termos com evidência; termo indeterminado impede publicar a descrição. Quando algo comprovadamente não se aplicar, declare essa condição no termo correspondente sem alterar a fórmula.

## Redação

- Formule no singular e no afirmativo.
- Defina o conceito; não traduza apenas o identificador nem use o termo definido como sua própria definição.
- Faça a frase funcionar sem depender do nome da coluna ao lado.
- Expanda siglas na primeira ocorrência e use o mesmo termo para o mesmo conceito.
- Distinga conceitos vizinhos e termos diferentes apresentados pela interface; divergência gera conflito, não um terceiro termo.
- Descreva chave estrangeira pela entidade e pelo papel referenciado, não pelo nome físico da tabela.
- Não use classe, método, arquivo, caminho, framework ou norma como significado de negócio.
- Não use `atual`, `último`, `vigente`, `total` ou `saldo` sem referência temporal ou escopo.
- Não use termos subjetivos como `correto`, `válido`, `normal` ou `adequado` sem informar o critério que os torna verdadeiros.
- Não publique afirmação genérica que continuaria verdadeira ao trocar o alvo.

## Tabelas

Antes de redigir, determine por evidência:

- conceito e granularidade exata de uma linha;
- evento ou critério de criação e ciclo de vida;
- escopos de inclusão e exclusão;
- estado temporal e momento ou período de referência;
- origem, processos suportados, usos e limitações.

Use a fórmula associativa somente quando a tabela resolver uma relação muitos-para-muitos (N:N) entre duas entidades e uma linha representar uma combinação ou ocorrência comprovada dessa relação; nos demais casos, incluindo relação 1:N e tabela cuja finalidade principal for representar uma entidade, evento, item, histórico ou resultado, use a fórmula geral. A existência isolada de chaves estrangeiras não prova associação N:N; confirme por cardinalidade, chaves e operações de escrita. Uma relação N:N com atributos próprios continua sendo associação; descreva esses atributos nas colunas. Prefixo ou nome não prova classificação. Granularidade também é obrigatória para objeto técnico.

## Colunas

Determine propriedade, entidade ou evento, critério, referência temporal, representação, origem, uso, limitação e semântica da ausência.

- Identificador: informe o objeto e a natureza técnica ou negocial.
- Chave estrangeira: informe entidade e papel na relação.
- Data e hora: informe evento ou período; acrescente fuso e precisão quando relevantes.
- Valor monetário ou medida: informe objeto, unidade, momento, escala e arredondamento aplicáveis.
- Valor derivado: informe resultado, regra, entradas e momento do cálculo.
- Domínio: publique somente o conjunto completo, com significado de cada valor.
- Valor nulo: informe a semântica comprovada ou a impossibilidade comprovada; `opcional` e `pode ser nulo` não são significados.

## Critérios de aceitação

Em verificação, avalie `dicionario_tabelas.md` e `dicionario_colunas.md` inteiros; descrição fora da fórmula obrigatória bloqueia a entrega do artefato avaliado. Em atualização, avalie os dois arquivos inteiros para o relatório de A1 a A10, mas bloqueie a entrega apenas por descrição do escopo solicitado ou por divergência estrutural confirmada (A8) ou domínio incompleto confirmado (A2); descrição preexistente fora desse alcance é registrada como lacuna no relatório, sem bloquear a entrega nem ser reescrita.

| Número | Medida | Aceite |
|---|---|---|
| A1 | Tabelas com granularidade determinada | 100% |
| A2 | Domínios fechados completos, com valores e significados | 100%; incompletude bloqueia a descrição |
| A3 | Descrições tautológicas ou genéricas | 0 |
| A4 | Afirmações sem evidência suficiente | 0 publicadas; lacunas reportadas |
| A5 | Conflitos decididos silenciosamente | 0 |
| A6 | Termos divergentes para o mesmo conceito | 0 |
| A7 | Implementação ou norma mencionada nos dicionários | 0 |
| A8 | Estrutura acumulada divergente dos dicionários | 0 |
| A9 | Erros de forma automatizados ou manuais | 0 |
| A10 | Significado ou finalidade de negócio no `CHANGELOG.md` | 0 |

A1 a A7 e A10 exigem leitura. A8 exige comparar, no alcance comprovado pelo adaptador, a estrutura acumulada com os dicionários; história anterior a esse alcance não integra a medida. A9 combina o verificador com os checks manuais de forma. Registre A1 a A10 no relatório, nunca nos artefatos publicados.
