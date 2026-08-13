# Templates de descrição de tabelas e colunas

Autoridade sobre: fórmulas obrigatórias de redação para descrições de tabelas e colunas nos dicionários de dados. Este arquivo não autoriza preencher lacunas por inferência.

## Regras de uso

- Use obrigatoriamente a fórmula aplicável depois de classificar o objeto e comprovar a granularidade.
- Classifique a coluna antes de redigir, pela evidência disponível, não pelo termo que a fórmula viria a preencher: use a fórmula específica de domínio multivalorado somente quando houver evidência de que o valor é escolhido a partir de um conjunto de alternativas controladas e nomeadas, com significado próprio para cada uma (constraint ou enumeração no banco, tabela de domínio ou referência, validação de código, ou regra de negócio documentada). Valores apenas observados repetidos numa amostra, sem essa evidência, não bastam; nesse caso permanece texto livre e usa a fórmula geral. Confirmada a evidência, use a fórmula específica independentemente do conteúdo representado e da quantidade de valores comprovados, de um em diante: o mesmo tratamento vale para um valor, dois valores ou vinte. Essa fórmula não se aplica quando o termo é preenchido com unidade, moeda, escala ou referência sem enumeração de valores nomeados. Use a fórmula geral para toda coluna sem essa evidência.
- Preserve a redação e a ordem das fórmulas. Elas são a única estrutura permitida. Substitua os termos entre colchetes apenas por conteúdo sustentado pelas evidências.
- Todas as frases e todos os componentes da fórmula selecionada são obrigatórios. Se algum termo estiver indeterminado, não publique a descrição e registre a lacuna.
- Quando um componente comprovadamente não se aplicar, declare essa condição no termo correspondente sem alterar ou omitir a frase da fórmula.
- A granularidade nunca pode ser omitida da descrição de uma tabela.
- Ao preencher os termos da fórmula, ajuste a regência nominal considerando a frase completa, e não concatene os marcadores mecanicamente. Faça as contrações exigidas quando a preposição introduzir um complemento nominal: `Identificador da configuração`, `Identificador do atributo`, `Identificador dos documentos` e `Identificador de processo`. Preserve a forma sem contração quando a construção gramatical exigir, como em `antes de o processo começar`.

## Tabelas

### Fórmula Obrigatória para Tabelas

O primeiro termo é a variável de decisão: use `Representa` ou `Associa`, conforme `principios-qualidade-dados.md`. Use `Associa` exclusivamente quando a tabela resolver uma relação muitos-para-muitos (N:N) entre duas entidades, preenchendo o termo seguinte no formato `[entidade A] a [entidade B]`. Nos demais casos, use `Representa`, preenchendo o termo seguinte com a entidade, evento, relação ou resultado de negócio representado.

> [Representa ou Associa] [entidade, evento, relação ou resultado de negócio], com uma linha para cada [granularidade]. O registro é criado ou passa a integrar o conjunto quando [evento ou critério]. Inclui [escopo] e exclui [exclusões relevantes]. Mantém [estado atual, histórico, vigência, fotografia ou agregação] referente a [momento ou período]. É produzido a partir de [origem] e utilizado por [processos, operações ou decisões]. Não deve ser interpretado ou utilizado como [limitações].

## Colunas

### Fórmula Obrigatória para Colunas

> [Propriedade ou conceito] de [entidade ou evento], correspondente a [significado e critério], determinado em [momento, período ou condição]. É expresso em [unidade, moeda, escala, domínio ou referência] e obtido por [captura, origem ou regra]. O valor nulo significa [semântica da ausência]. É utilizado para [função] e não representa [distinção ou limitação].

### Fórmula Obrigatória para Colunas com Domínio Multivalorado

Use esta variante da fórmula geral quando a classificação da coluna, feita antes da redação conforme Regras de uso, confirmar um domínio controlado por evidência. O conteúdo e a quantidade de valores nunca decidem a estrutura da descrição; a quantidade decide apenas quantos itens a lista final tem.

> [Propriedade ou conceito] de [entidade ou evento], correspondente a [significado e critério], determinado em [momento, período ou condição]. É expresso em um domínio multivalorado de [quantidade] valores fixos, listados a seguir, e obtido por [captura, origem ou regra]. O valor nulo significa [semântica da ausência]. É utilizado para [função] e não representa [distinção ou limitação]. Valores do domínio:
> - <valor_1>: descrição negocial do valor
> - <valor_2>: descrição negocial do valor
> - <valor_3>: descrição negocial do valor

Os três itens mostram a forma da enumeração, não uma cardinalidade fixa. Na descrição publicada, inclua um item para cada valor do domínio completo e comprovado, mesmo quando o domínio tiver um único valor comprovado; domínio incompleto bloqueia a descrição. No termo `[quantidade]`, informe apenas a quantidade de valores comprovados; não repita a enumeração ali, ela vai somente na lista final. Mantenha cada valor como um item independente na lista; não agrupe vários valores num único item para reduzir o tamanho do texto, mesmo quando compartilharem alguma característica. Agrupar prejudica a leitura direta de "valor → significado".
