# Introdução Conceitual

Nesta seção são abordadas boas práticas e conceitos importantes para a criação ou revisão de descrições de tabelas e colunas de banco de dados por meio do processamento principalmente do código-fonte do sistema suportado pelo banco de dados e também por outros documentos, como esquemas do banco, consultas, testes e qualquer outra documentação do sistema.

A orientação central é que uma descrição de alta qualidade não se limita a repetir o nome técnico, o tipo SQL ou a estrutura física do banco. Ela deve permitir que um leitor ou máquina compreenda:

* **o que o dado representa no negócio**;
* **em qual contexto esse significado é válido**;
* **como o dado é representado**;
* **como e quando ele é produzido**;
* **para que pode ser utilizado**;
* **quais interpretações ou utilizações seriam incorretas**.

A sequência consolidada é:

> **necessidade de decisão → necessidade de informação → conceito de negócio → especificação do dado → descrição semântica → contexto de uso → validação contra evidências → avaliação de qualidade**

A ISO 8000-1:2022 relaciona a qualidade dos dados às necessidades de informação geradas pelas decisões organizacionais e orienta o uso de especificações que permitam verificar requisitos sintáticos, semânticos e função negocial. A mesma norma associa dados adequados ao propósito à capacidade de pessoas e sistemas tomarem decisões corretas no momento apropriado.

## Normas de Referência

Este documento foi baseado principalmente sobre as normas abaixo:

* ISO 8000-1:2022 — **Data quality**.
* ISO/IEC 25012:2008 — Software engineering — Software product Quality Requirements and Evaluation (SQuaRE) — **Data quality model**
* ISO/IEC 25024:2015 — **medição das características da ISO/IEC 25012:2008 e definição de dicionário de dados**.
* ISO/IEC 11179-3:2023 — **modelo para registro de metadados**.
* ISO/IEC 11179-4:2004 — **formulação de definições de dados**.

## Qualidade relativa ao uso

A qualidade da descrição deve ser avaliada em relação ao uso esperado do dado. Não existe descrição completa sem contexto suficiente para determinar se o dado é adequado a uma operação ou decisão.

Toda descrição de tabela ou coluna deve indicar, diretamente na definição ou em campos complementares:

1. **qual processo de negócio é suportado**;
2. **qual operação, cálculo, decisão ou obrigação depende do dado**;
3. **qual referência temporal, precisão, granularidade e atualização são relevantes**;
4. **quais usuários, serviços, relatórios, integrações ou sistemas são afetados**;
5. **quais usos são apropriados**;
6. **quais usos ou interpretações são inadequados**;
7. **qual é a consequência provável de uma interpretação incorreta**.

Esses elementos não precisam obrigatoriamente aparecer em uma única frase. É preferível separar a **definição semântica nuclear** do **contexto funcional**, das **regras de representação** e das **limitações de uso**.

## O ponto de partida é a necessidade de informação

Antes de redigir a descrição, deve se esforçar ao máximo a tentar responder com base nas evidências disponíveis:

* Qual pergunta de negócio esta tabela ajuda a responder?
* Qual processo cria, altera ou consulta seus registros?
* O objeto representa uma entidade, um evento, um estado, uma relação, uma classificação ou uma agregação?
* O que exatamente uma linha representa?
* Qual decisão, operação ou cálculo pode ser realizado com esses dados?
* Qual requisito funcional, regulatório ou operacional originou o objeto?
* O dado é fonte oficial, cópia, cache, histórico, integração, estágio intermediário ou resultado derivado?
* O dado representa o estado atual, um evento ocorrido, uma versão histórica, uma vigência ou uma fotografia em determinado momento?
* O que seria interpretado incorretamente caso o significado fosse deduzido apenas pelo nome técnico?

Quando essas respostas não puderem ser obtidas das evidências disponibilizadas, não deve preencher as lacunas com suposições apresentadas como fatos.

## Sintaxe, Semântica e Função Negocial (pragmática)

A descrição deve tratar três perspectivas distintas.

| Perspectiva                     | Pergunta principal                         | Conteúdo esperado                                                                                                    |
| ------------------------------- | ------------------------------------------ | -------------------------------------------------------------------------------------------------------------------- |
| **Sintaxe**                     | Como o dado é representado?                | Tipo lógico, formato, tamanho, escala, unidade, moeda, codificação, domínio, padrão temporal, valores permitidos e restrições. |
| **Semântica**                   | O que o dado significa?                    | Conceito de negócio, entidade ou evento, propriedade representada, critérios de distinção e significado dos valores. |
| **Função Negocial**           | Para que e em quais condições o dado é útil? | Processo suportado, decisão, operação, consumidores, atualidade necessária, limitações e usos inadequados.           |

A ISO 8000-1:2022 distingue explicitamente características sintáticas, semânticas e pragmáticas (função negocial). Também orienta que especificações de dados sejam utilizadas para determinar se os requisitos dessas três perspectivas são atendidos.

### Exemplo

Descrição insuficiente:

> Data do pedido.

Descrição semanticamente melhor:

> Data civil em que o pedido de venda foi confirmado pelo processo comercial.

Complemento sintático:

> Representada no calendário gregoriano no formato `AAAA-MM-DD`.

Complemento pragmático (função negocial):

> Utilizada para classificação do pedido no funil comercial. Não representa a data de faturamento, expedição ou reconhecimento contábil da receita.

## Separação entre definição nuclear e contexto funcional

A definição semântica nuclear deve explicar a natureza essencial do conceito e distingui-lo de conceitos relacionados. O contexto funcional deve explicar produção, utilização e limitações.

Essa separação é especialmente importante porque as regras da ISO/IEC 11179-4:2004 orientam que uma definição:

* seja formulada no singular;
* diga o que o conceito é, e não apenas o que ele não é;
* utilize uma frase ou expressão descritiva;
* evite abreviações não compreensíveis;
* não incorpore a definição completa de outros conceitos;
* apresente o significado essencial;
* seja precisa, concisa, autossuficiente e não circular;
* mantenha terminologia e estrutura lógica consistentes entre conceitos relacionados;
* não misture, dentro da definição nuclear, justificativas, procedimentos ou explicações operacionais. 

**Ressalva sobre a ISO/IEC 11179-4:** tomada ao pé da letra, essa norma pede que o campo "definição" fique livre de raciocínio funcional ou procedural; ela não apoia reunir definição e contexto de uso na mesma frase. O formato de descrição única (uma coluna `Descrição` por tabela ou coluna, sem campos separados) usado neste repositório, que combina definição e contexto de uso numa frase quando o catálogo não permite campos separados, é sustentado pela prática de mercado (Dataedo, OvalEdge, Collate), não pela ISO 11179-4 isoladamente. Quando o catálogo permitir campos separados, prefira sempre a separação descrita abaixo: ela é o que a norma efetivamente recomenda.

Portanto, para uma coluna como `vl_receita`, o resultado recomendado não é uma frase excessivamente longa contendo significado, fórmula, procedimento, dono, finalidade e histórico.

Use componentes separados:

**Definição semântica nuclear**

> Valor monetário da receita reconhecida para o item de faturamento.

**Regra de derivação**

> Calculado pelo valor bruto menos descontos comerciais, cancelamentos e devoluções reconhecidos até o fechamento contábil.

**Contexto funcional**

> Utilizado em apurações contábeis e relatórios financeiros. Não deve ser utilizado como previsão comercial.

**Representação**

> Expresso na moeda indicada por `cd_moeda`, com duas casas decimais e arredondamento contábil.

## O dicionário como parte da arquitetura de dados

O dicionário deve tratar cada tabela e coluna como um item identificável e governável, e não como texto solto.

A ISO/IEC 25024:2015 define um dicionário de dados como uma coleção de informações sobre dados que pode incluir nome, descrição, criador, proprietário, proveniência, traduções e utilização. Ela também considera o próprio dicionário uma entidade que pode ser submetida a medidas de qualidade. 

A ISO/IEC 11179-3:2023 estrutura um registro por meio de recursos de:

* identificação;
* designação e definição;
* registro;
* classificação;
* mapeamento entre itens.

Essa estrutura está relacionada com a compreensão comum, reutilização, harmonização e compartilhamento dos dados entre sistemas e organizações.

Isso significa:

* não criar definições independentes para conceitos equivalentes sem verificar relações;
* reutilizar os mesmos termos para o mesmo conceito;
* diferenciar termos parecidos que representam conceitos diferentes;
* identificar sinônimos e nomes técnicos alternativos;
* relacionar códigos aos respectivos significados;
* registrar quando um conceito é equivalente, derivado, substituído ou apenas semelhante a outro.

## Proveniência, exatidão e completude

Uma descrição deve ser sustentada por evidências rastreáveis. É importante apontar em documento separado as evidências do porquê que concluiu que determinado objeto possui determinado significado.

São evidências típicas:

* definição DDL;
* restrições `CHECK`, `UNIQUE`, `NOT NULL` e chaves;
* migrações;
* mapeamentos ORM;
* classes de domínio;
* validações;
* serviços de aplicação;
* casos de uso;
* eventos de domínio;
* consultas SQL;
* relatórios;
* APIs;
* telas;
* testes;
* documentação funcional;
* glossários;
* comentários no código.

Uma descrição de alta qualidade deve distinguir:

* **fato confirmado**: afirmação direta em fonte adequada, sem contradição;
* **conclusão corroborada**: dois tipos independentes de evidência convergem;
* **inferência provável**: leitura plausível sem confirmação;
* **não determinado**: busca aplicável concluída sem resultado;
* **conflito estrutural**: estados físicos incompatíveis entre fontes;
* **conflito semântico**: significados incompatíveis entre fontes.

A ISO/IEC 25012:2008 aplica o modelo de qualidade a dados estruturados utilizados por pessoas e sistemas e permite utilizar suas características para requisitos, medidas e avaliações. A ISO/IEC 25024:2015 complementa esse modelo com medidas para exatidão, completude, consistência, credibilidade, atualidade, compreensibilidade, rastreabilidade e outras características.

## Características aplicadas à descrição do dicionário

Nem todas as características precisam aparecer literalmente em cada descrição. Elas funcionam como critérios para verificar se o significado documentado é suficiente.

### Perspectiva inerente

Relacionada ao próprio conteúdo, significado e representação do dado.

| Característica    | Aplicação à descrição                                                                                                                                            |
| ----------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Exatidão**      | A definição deve representar o conceito correto e distingui-lo de conceitos semelhantes.                                                                         |
| **Completude**    | A descrição deve incluir os aspectos necessários para interpretar corretamente o objeto, especialmente granularidade, escopo, temporalidade e semântica do nulo. |
| **Consistência**  | Termos, regras, unidades e relações devem ser compatíveis com outras descrições e com o código.                                                                  |
| **Credibilidade** | A conclusão deve estar sustentada por fontes identificáveis e, quando disponível, por uma fonte oficial ou autoridade negocial.                                  |
| **Atualidade**    | A descrição deve corresponder à versão vigente do esquema e das regras e esclarecer a atualidade do próprio dado.                                                |

### Perspectiva inerente e dependente do sistema

| Característica         | Aplicação à descrição                                                                                       |
| ---------------------- | ----------------------------------------------------------------------------------------------------------- |
| **Precisão**           | Declarar escala, unidade, arredondamento, granularidade temporal ou espacial e nível de detalhe relevante.  |
| **Rastreabilidade**    | Identificar origem, derivações, transformações e relação com outros objetos.                                |
| **Compreensibilidade** | Empregar linguagem de negócio, evitar tautologias e explicar termos técnicos ou códigos.                    |
| **Conformidade**       | Indicar normas, políticas, domínios ou convenções aplicáveis quando forem relevantes ao significado.        |
| **Confidencialidade**  | Indicar restrições ou natureza sensível quando isso afetar a utilização e interpretação do dado.            |
| **Acessibilidade**     | Explicar restrições de acesso quando o dado parecer ausente ou indisponível para determinados consumidores. |
| **Eficiência**         | Registrar limitações de latência, volume ou processamento somente quando forem relevantes ao uso negocial.  |

### Perspectiva predominantemente dependente do sistema

| Característica       | Aplicação à descrição                                                                                           |
| -------------------- | --------------------------------------------------------------------------------------------------------------- |
| **Disponibilidade**  | Informar janelas, atrasos ou indisponibilidades quando afetarem a adequação do dado ao uso.                     |
| **Portabilidade**    | Explicar formatos ou dependências proprietárias quando o significado puder ser perdido na transferência.        |
| **Recuperabilidade** | Registrar possibilidade de reprocessamento ou reconstrução somente quando isso fizer parte da função do objeto. |

Para descrições de negócio, as características normalmente prioritárias são:

> **exatidão, completude, consistência, credibilidade, atualidade, precisão, rastreabilidade e compreensibilidade.**

As demais devem ser incluídas quando alterarem a interpretação, a confiança ou a possibilidade de uso.

## Modelo Recomendado para Descrição de Tabelas

A descrição de uma tabela deve possuir, no mínimo, quatro componentes:

1. **conceito ou função negocial**;
2. **granularidade da linha**;
3. **escopo e temporalidade**;
4. **finalidade e limitações**.

### Conteúdo que deve ser determinado

| Elemento               | Pergunta a responder                                                       |
| ---------------------- | -------------------------------------------------------------------------- |
| **Conceito central**   | Qual entidade, evento, estado ou resultado é representado, ou qual relação N:N entre entidades é associada? |
| **Granularidade**      | O que exatamente uma linha representa?                                     |
| **Evento de criação**  | Qual fato faz o registro surgir?                                           |
| **Escopo de inclusão** | Quais ocorrências fazem parte da tabela?                                   |
| **Escopo de exclusão** | Quais ocorrências semelhantes não fazem parte?                             |
| **Semântica temporal** | Estado atual, histórico, evento, vigência, fotografia ou agregação?        |
| **Identificação**      | Qual chave identifica a ocorrência? A chave é técnica ou negocial?         |
| **Origem**             | A tabela é fonte oficial, réplica, estágio, cache, histórico ou derivação? |
| **Processo suportado** | Qual processo cria, altera ou consome os dados?                            |
| **Finalidade**         | Quais operações, decisões, indicadores ou integrações dependem da tabela?  |
| **Limitações**         | Para quais usos a tabela não é apropriada?                                 |

## Classificação da tabela antes da descrição

É necessário classificar o objeto antes de redigir o texto.

| Tipo provável                         | Granularidade que deve ser investigada                            |
| ------------------------------------- | ----------------------------------------------------------------- |
| **Entidade ou cadastro mestre**       | Uma linha por pessoa, produto, contrato, conta ou outra entidade. |
| **Transação ou evento**               | Uma linha por ocorrência negocial.                                |
| **Item de transação**                 | Uma linha por item pertencente a uma transação.                   |
| **Histórico de versões**              | Uma linha por versão da entidade ou alteração registrada.         |
| **Vigência**                          | Uma linha por entidade e intervalo de validade.                   |
| **Snapshot**                          | Uma linha por entidade e instante ou período de referência.       |
| **Associação N:N**                    | Uma linha por combinação ou ocorrência da relação muitos-para-muitos entre uma ocorrência da entidade A e uma ocorrência da entidade B; a relação pode possuir atributos próprios. |
| **Domínio ou referência**             | Uma linha por código ou valor permitido.                          |
| **Agregação**                         | Uma linha por combinação de dimensões e período.                  |
| **Staging**                           | Uma linha por registro recebido da origem, antes da consolidação. |
| **Auditoria ou log**                  | Uma linha por ação, alteração, execução ou evento técnico.        |
| **Fila ou controle de processamento** | Uma linha por unidade de trabalho ou mensagem.                    |

A classificação não deve ser deduzida apenas do prefixo do nome. Ela deve ser confirmada por chaves, operações de escrita, relacionamentos, consultas e regras de ciclo de vida.

### Escolha do verbo inicial

O verbo inicial deve refletir a classificação semântica da tabela. Use **"Associa"** exclusivamente quando a tabela resolver uma relação muitos-para-muitos (N:N) entre duas entidades e cada linha representar uma combinação ou ocorrência dessa relação. Nesse caso, nomeie os dois participantes no formato **"Associa [entidade A] a [entidade B]"**.

Use **"Representa"** nos demais tipos de tabela, incluindo entidades, transações, eventos, itens, históricos, vigências, snapshots, domínios, agregações, staging, auditoria, filas e controles técnicos.

A existência de duas chaves estrangeiras, de vários relacionamentos ou de uma tabela intermediária não determina, por si só, o uso de "Associa". Relações 1:N e tabelas cuja finalidade principal seja representar uma entidade, evento, item, histórico ou resultado devem iniciar com **"Representa"**. Se a relação N:N possuir atributos próprios, ela continua sendo descrita como associação, e esses atributos devem ser explicados separadamente nas colunas.

### Fórmula Recomendada para Tabela

O primeiro termo é a variável de decisão: escolha "Representa" ou "Associa" conforme a seção anterior. Quando for "Associa", preencha o termo seguinte no formato "[entidade A] a [entidade B]"; nos demais casos, preencha com a entidade, evento, relação ou resultado de negócio representado.

> **[Representa ou Associa]** **[entidade, evento, relação ou resultado de negócio]**, com uma linha para cada **[granularidade]**. O registro é criado ou passa a integrar o conjunto quando **[evento ou critério]**. Inclui **[escopo]** e exclui **[exclusões relevantes]**. Mantém **[estado atual, histórico, vigência, fotografia ou agregação]** referente a **[momento ou período]**. É produzido a partir de **[origem]** e utilizado por **[processos, operações ou decisões]**. Não deve ser interpretado ou utilizado como **[limitações]**.

Todas as frases e todos os componentes da fórmula são obrigatórios; nenhuma frase é opcional. A granularidade nunca deve ser omitida de uma tabela de negócio. Termo indeterminado não é preenchido por suposição: vira lacuna registrada, e a descrição não é publicada até se resolver.

### Como redigir a descrição de tabela

#### Declarar a granularidade

A granularidade muda conforme o tipo de tabela, nunca é um valor fixo: numa entidade mestre é uma linha por entidade; numa associação N:N é uma linha por combinação da relação; num item de transação é uma linha por item; num histórico é uma linha por versão; numa agregação é uma linha por combinação de dimensões e período. Não infira pelo nome ou prefixo da tabela; confirme pela chave primária, pelas chaves únicas e pelas operações de escrita.

Ruim:

> Tabela de pedidos.

Melhor:

> Representa pedidos de venda, com uma linha para cada combinação de pedido e empresa emissora.

#### Declarar o evento de criação

O evento de criação é o fato de negócio que faz a linha nascer, não o momento técnico do `INSERT`. Situações comuns: confirmação de uma contratação, aprovação de uma solicitação, recebimento de um lote de integração externa. Quando o evento técnico e o evento de negócio coincidem de fato (por exemplo, uma tabela de log criada no exato instante da ação registrada), diga isso explicitamente em vez de simplesmente omitir a frase.

Ruim:

> Registros de pedidos.

Melhor:

> O registro passa a integrar a tabela quando a contratação é aceita pelo sistema de vendas.

#### Declarar o escopo de inclusão e exclusão

Declare tanto o que entra quanto o que fica de fora, principalmente quando existem objetos parecidos que não pertencem à tabela: rascunhos, simulações, cotações, registros técnicos, dados de teste. A ausência de exclusão explícita costuma ser lida como "tudo que existe no domínio está aqui", o que quase nunca é verdade e é a causa mais comum de alguém consultar a tabela errada.

Ruim:

> Contém os pedidos do sistema.

Melhor:

> Inclui pedidos posteriormente cancelados, desde que tenham sido confirmados, e exclui cotações, simulações e carrinhos não concluídos.

#### Declarar a semântica temporal

Diga se a tabela mantém o estado atual (uma linha por entidade, sobrescrita a cada mudança), um evento (uma linha por ocorrência, imutável), um histórico (uma linha por versão), uma vigência (uma linha por intervalo de validade) ou uma fotografia/agregação (uma linha por período). Essa escolha muda completamente como um consumidor deve interpretar múltiplas linhas para a mesma entidade: presumir "estado atual" quando na verdade é "histórico" faz alguém somar ou comparar linhas que não deveriam ser comparadas.

Ruim:

> Situação do pedido.

Melhor:

> Mantém o estado mais recente do pedido; alterações históricas de estado são registradas em `vendas.pedido_status_historico`.

#### Declarar a origem

Diga se a tabela é a fonte oficial do dado, uma cópia, um cache, uma integração externa ou um resultado derivado de outras tabelas. Isso importa porque duas tabelas podem parecer redundantes à primeira vista, mas uma é a fonte da verdade e a outra é apenas uma projeção ou réplica dela; usar a projeção como se fosse a fonte gera decisão errada quando as duas divergem.

Ruim:

> Dados vindos do sistema comercial.

Melhor:

> É produzida a partir da confirmação da contratação pelo sistema comercial.

#### Declarar o processo suportado

Nomeie o processo, a operação ou a decisão de negócio real que consome a tabela; "usada pelo sistema" não identifica nada porque continuaria verdadeiro para qualquer tabela do banco. Se vários processos dependem dela, cite os principais; se apenas um processo específico e pouco frequente depende dela, diga isso também, porque afeta o quão crítica a tabela realmente é.

Ruim:

> Usada pelo sistema de vendas.

Melhor:

> Utilizada por faturamento, atendimento, logística e análise de conversão.

#### Declarar limitações

Aponte o conceito vizinho com o qual a tabela é mais frequentemente confundida: outro estágio do mesmo processo, outra entidade, previsão versus realizado, estado atual versus histórico. A limitação existe para evitar que alguém use a tabela errada para responder uma pergunta de negócio que ela não responde.

Ruim:

> Tabela de pedidos, cuidado ao usar.

Melhor:

> Não representa, isoladamente, uma nota fiscal emitida, uma entrega concluída ou receita contabilmente reconhecida.

### Exemplo negativo

> Tabela de pedidos do sistema.

Problemas:

* não informa o que uma linha representa;
* não diferencia pedido, item, versão ou evento;
* não informa se há pedidos não confirmados;
* não informa se representa estado atual ou histórico;
* não identifica finalidade ou limitação.

### Exemplo positivo

> Representa pedidos de venda confirmados pelo processo comercial, com uma linha para cada pedido e empresa emissora. O registro passa a integrar a tabela quando a contratação é aceita pelo sistema de vendas. Inclui pedidos posteriormente cancelados, desde que tenham sido confirmados, e exclui cotações, simulações e carrinhos não concluídos. Mantém o estado mais recente do pedido e é utilizado por faturamento, atendimento, logística e análise de conversão. Não representa faturamento concluído nem receita contabilmente reconhecida.

### Exemplo positivo de associação N:N

> Associa usuários a perfis de acesso, com uma linha para cada combinação de usuário e perfil. O registro é criado quando o perfil é atribuído ao usuário e utilizado para determinar os perfis relacionados a cada usuário. Não representa o usuário, o perfil nem o histórico de alterações da atribuição.

Esse exemplo mostra simultaneamente o verbo correto, a granularidade e a distinção entre a relação e as entidades participantes.

## Modelo Recomendado para Descrição de Colunas

A descrição de uma coluna deve responder:

1. **qual propriedade ou conceito é representado**;
2. **de qual entidade ou evento essa propriedade faz parte**;
3. **em qual momento ou condição o valor é válido**;
4. **como o valor deve ser interpretado**;
5. **qual unidade, domínio ou referência é utilizada**;
6. **o que significa a ausência do valor**;
7. **se o valor é capturado, recebido, calculado ou derivado**;
8. **para que é utilizado e quais limitações possui**.

### Domínio multivalorado: quando usar

Um domínio controlado por evidência é sempre qualificado como **multivalorado**, qualquer que seja a quantidade de valores comprovados, a partir de um único valor, e qualquer que seja o conteúdo representado (ex.: um indicador binário como ativo/inativo, um status com múltiplos estados como aberto/em análise/concluído/arquivado, ou um domínio com um único valor comprovado até o momento). Evidência aceitável é constraint ou enumeração no banco, tabela de domínio ou referência, validação de código, ou regra de negócio documentada. Valores apenas observados repetidos numa amostra, sem essa evidência, não bastam para essa classificação; nesse caso a coluna permanece texto livre e usa a fórmula geral.

### Fórmula Recomendada para Coluna

Classifique a coluna antes de redigir, conforme [Domínio multivalorado: quando usar](#domínio-multivalorado-quando-usar). Use a fórmula de domínio multivalorado quando essa classificação confirmar um domínio controlado por evidência; use a fórmula geral nos demais casos, inclusive quando o termo é preenchido com unidade, moeda, escala ou referência sem enumeração de valores nomeados.

**Geral**

> **[Propriedade ou conceito]** de **[entidade ou evento]**, correspondente a **[significado e critério]**, determinado em **[momento, período ou condição]**. É expresso em **[unidade, moeda, escala, domínio ou referência]** e obtido por **[captura, origem ou regra]**. O valor nulo significa **[semântica da ausência]**. É utilizado para **[função]** e não representa **[distinção ou limitação]**.

**Domínio multivalorado**

> **[Propriedade ou conceito]** de **[entidade ou evento]**, correspondente a **[significado e critério]**, determinado em **[momento, período ou condição]**. É expresso em um domínio multivalorado de **[quantidade]** valores fixos, listados a seguir, e obtido por **[captura, origem ou regra]**. O valor nulo significa **[semântica da ausência]**. É utilizado para **[função]** e não representa **[distinção ou limitação]**. Valores do domínio:
> - <valor_1>: descrição negocial do valor
> - <valor_2>: descrição negocial do valor
> - <valor_3>: descrição negocial do valor

Os três itens acima mostram a forma da enumeração, não uma cardinalidade fixa: a descrição publicada inclui um item para cada valor do domínio completo e comprovado, mesmo quando o domínio tiver um único valor comprovado, e domínio incompleto bloqueia a descrição. No termo **[quantidade]**, informe apenas a quantidade de valores comprovados; não repita a enumeração ali, ela vai somente na lista final. Mantenha cada valor como um item independente na lista final: não agrupe vários valores dentro de um único item só para reduzir o tamanho do texto, mesmo quando compartilharem alguma característica; agrupar prejudica a leitura direta de "valor → significado", que é o propósito da lista.

### Regência nominal e contrações

Ao preencher os termos da fórmula, ajuste a regência nominal considerando a frase completa, e não concatene os marcadores mecanicamente. Faça as contrações exigidas quando a preposição introduzir um complemento nominal: `Identificador da configuração`, `Identificador do atributo`, `Identificador dos documentos` e `Identificador de processo`. Preserve a forma sem contração quando a construção gramatical exigir, como em `antes de o processo começar`.

Quando o catálogo possui campos separados, prefira:

* definição semântica;
* regra de derivação;
* representação;
* semântica do nulo;
* contexto de uso;
* limitações.

### Como redigir a definição de negócio

#### Começar pelo conceito e não pelo mecanismo

Ruim:

> Campo que guarda o status.

Melhor:

> Estado do pedido no fluxo de atendimento comercial.

#### Identificar a entidade ou o evento

Ruim:

> Valor total.

Melhor:

> Valor monetário total previsto para o pedido de venda confirmado.

#### Declarar a referência temporal

Ruim:

> Saldo atual.

Melhor:

> Saldo das obrigações financeiras abertas da conta ao término do último processamento diário concluído.

#### Diferenciar conceitos relacionados

Ruim:

> Data de cancelamento.

Melhor:

> Data civil em que o cancelamento foi confirmado pelo processo comercial, distinta da data em que a solicitação de cancelamento foi recebida.

#### Informar unidade e escala

Ruim:

> Peso do produto.

Melhor:

> Massa líquida de uma unidade comercial do produto, expressa em quilogramas com três casas decimais.

#### Explicar a ausência

Ruim:

> Pode ser nulo.

Melhor:

> O valor nulo indica que o pedido ainda não foi faturado.

#### Separar significado de cálculo

Definição:

> Valor monetário líquido do item de pedido.

Derivação:

> Calculado pela quantidade multiplicada pelo preço unitário, menos o desconto concedido ao item.

#### Declarar a função negocial

Diga qual decisão, cálculo, filtro ou apresentação depende do valor da coluna; "usado pelo sistema" não identifica nada, porque continuaria verdadeiro para qualquer coluna do banco. Se a coluna alimenta mais de um processo, cite os principais; se ela existe só por compatibilidade e não é mais usada ativamente, diga isso também, porque muda a limitação que vem em seguida na fórmula.

Ruim:

> Usado pelo sistema.

Melhor:

> Utilizado para classificar o pedido no funil comercial e liberar a separação logística.

#### Declarar limitações

> Representa a previsão comercial do valor do pedido e não a receita reconhecida contabilmente.

## Regras específicas para tipos comuns de coluna

### Identificadores

A descrição deve informar:

* qual objeto é identificado;
* se o identificador é técnico ou negocial;
* o escopo de unicidade;
* se é imutável;
* se pode ser reutilizado;
* se é atribuído internamente ou recebido de fonte externa.

Exemplo:

> Identificador técnico imutável atribuído ao pedido pelo sistema comercial. É único em todo o ambiente e não corresponde ao número apresentado ao cliente.

### Chaves estrangeiras

Não descreva apenas como “código da tabela X”.

> Identificador do cliente responsável pela contratação do pedido, utilizado para relacionar o pedido ao cadastro corporativo de clientes.

A função da entidade relacionada deve ser explicitada: cliente contratante, beneficiário, pagador, aprovador, destinatário etc.

### Datas e horários

A descrição deve distinguir:

* data do evento;
* início ou término de vigência;
* data de referência;
* instante de criação técnica;
* instante de atualização;
* instante de integração;
* data informada pelo usuário;
* data calculada;
* fuso horário e precisão relevantes.

### Valores monetários

A descrição deve esclarecer:

* objeto econômico;
* valor bruto, líquido, previsto, realizado ou reconhecido;
* moeda;
* tributos, descontos, frete e encargos incluídos ou excluídos;
* momento de valorização;
* regra de arredondamento;
* conversão cambial, quando existente.

### Quantidades e medidas

Informar:

* o que está sendo contado ou medido;
* unidade;
* população ou universo;
* granularidade;
* período;
* limites;
* regra de arredondamento.

### Indicadores booleanos

Evitar:

> Indica se está ativo.

Preferir, explicando o significado de cada valor:

> Indica se o contrato pode ser utilizado para novas operações na data de referência. O valor nulo indica que a condição ainda não foi avaliada.

Publique o significado de `true` e `false` na lista da fórmula de domínio multivalorado, não em prosa dentro da frase de uso: um indicador binário com evidência de domínio controlado é multivalorado com dois valores (ver [Domínio multivalorado: quando usar](#domínio-multivalorado-quando-usar)).

### Códigos e enumerações

Informar:

* conceito classificado;
* domínio ou lista controlada;
* significado de cada código;
* responsável pelo domínio;
* condição de uso;
* códigos depreciados ou reservados.

Não usar somente:

> Código do status.

### Valores derivados

Informar:

* significado negocial do resultado;
* fórmula ou regra;
* entradas utilizadas;
* granularidade do cálculo;
* momento de cálculo;
* tratamento de nulos;
* arredondamentos;
* filtros e exclusões;
* possibilidade de recálculo.

### Colunas de auditoria

Diferenciar:

* autor da operação negocial;
* usuário autenticado;
* serviço técnico;
* processo em lote;
* instante do evento de negócio;
* instante de persistência;
* instante da última alteração.

## Exemplo completo de descrições

### Tabela `vendas.pedido`

**Definição semântica e granularidade**

> Representa um pedido de venda confirmado por uma empresa emissora, com uma linha para cada combinação de pedido e empresa.

**Escopo e temporalidade**

> O registro é criado quando o sistema comercial aceita a contratação. Inclui pedidos posteriormente cancelados e exclui cotações, simulações e carrinhos não concluídos. Mantém o estado mais recente do pedido; alterações históricas de estado são registradas em `vendas.pedido_status_historico`.

**Função negocial**

> Suporta faturamento, atendimento ao cliente, separação logística, acompanhamento comercial e análise de conversão.

**Limitações**

> Não representa, isoladamente, uma nota fiscal emitida, uma entrega concluída ou receita contabilmente reconhecida.

### Coluna `id_pedido`

> Identificador técnico imutável atribuído ao pedido pelo sistema comercial no momento da confirmação. É único em todo o ambiente e não deve ser reutilizado. Não corresponde ao número de pedido apresentado ao cliente.

### Coluna `nr_pedido`

> Número negocial utilizado para identificar o pedido em comunicações com o cliente. É único dentro da empresa emissora e deve ser interpretado em conjunto com `id_empresa`.

### Coluna `dh_confirmacao`

> Instante em que a contratação é aceita definitivamente pelo processo comercial. É armazenado em UTC e apresentado no fuso horário da empresa emissora. Não representa o instante de criação inicial do carrinho nem a data de faturamento.

### Coluna `vl_total_previsto`

> Valor monetário total previsto para o pedido confirmado, incluindo os valores líquidos dos itens, frete e encargos comerciais aplicáveis. Não incorpora devoluções, retenções ou ajustes reconhecidos após o faturamento. É expresso na moeda indicada por `cd_moeda`.

### Coluna `cd_status`

> Código que representa o estado mais recente do pedido no fluxo comercial, conforme o domínio controlado `status_pedido`. O código expressa a situação operacional do pedido e não a situação da nota fiscal ou da entrega.

### Coluna `dh_cancelamento`

> Instante em que o cancelamento do pedido foi confirmado pelo processo comercial. O valor nulo indica que nenhum cancelamento confirmado foi registrado. Não representa o instante da solicitação inicial de cancelamento.

### Coluna `id_cliente_contratante`

> Identificador do cliente que assumiu a contratação comercial do pedido. Relaciona o pedido ao cadastro corporativo de clientes. Não identifica necessariamente o destinatário da entrega ou o responsável pelo pagamento.


---


# Instruções para Descrição de Tabelas e Colunas de Banco de Dados com Alta Qualidade Negocial

As instruções seguintes devem ser utilizadas como comportamento obrigatório **de uma IA agêntica** responsável por analisar código-fonte e documentação PARA gerar ou revisar descrições de Tabelas e Colunas para um dicionário de dados. Elas consolidam as orientações de qualidade relativas ao uso, especificação semântica, função negocial, registro de metadados, formulação de definições e avaliação de qualidade.

## 1. Missão

Analise cada tabela e coluna para produzir descrições que permitam a uma pessoa ou sistema compreender:

* o conceito de negócio representado;
* a classificação da tabela e o verbo inicial correspondente: **"Associa"** para uma associação N:N e **"Representa"** para os demais tipos;
* a granularidade;
* o contexto em que o significado é válido;
* a origem e a forma de produção do valor;
* a referência temporal;
* a representação relevante;
* a função negocial;
* as limitações;
* o grau de certeza da conclusão.

Não produza apenas documentação técnica do esquema. Transforme as evidências técnicas em significado de negócio, sem inventar informações não sustentadas.

## 2. Princípios obrigatórios

1. **Baseie toda afirmação em evidência identificável.**

2. **Não deduza o significado somente pelo nome da tabela ou coluna.**

3. **Não trate tipo SQL, tamanho ou nulabilidade como definição de negócio.**

4. **Determine primeiro o conceito e depois redija a descrição.**

5. **Separe definição semântica, representação, derivação, utilização e limitação.**

6. **Não misture conceitos diferentes em uma única definição.**

7. **Utilize um termo de negócio de forma consistente em todo o dicionário.**

8. **Diferencie estado atual, evento, histórico, vigência, snapshot e agregação.**

9. **Informe explicitamente a granularidade de toda tabela de negócio.**

10. **Informe o significado do valor nulo sempre que a coluna for anulável e a ausência possuir significado negocial.**

11. **Não apresente inferência como fato confirmado.**

12. **Preserve conflitos e incertezas; não os esconda por meio de uma descrição artificialmente conclusiva.**

13. **Inicie a descrição com "Associa" somente quando a tabela representar uma relação N:N entre entidades e cada linha corresponder a uma combinação ou ocorrência dessa relação. Nos demais casos, inicie com "Representa". A existência de chaves estrangeiras, isoladamente, não basta para classificar a tabela como associação N:N.**

## 3. Fontes de evidência

Investigue as fontes abaixo. Nenhuma fonte isolada deve ser considerada automaticamente suficiente para determinar toda a semântica.

### 3.1 Estrutura física

Examine:

* DDL;
* esquema atual;
* migrações;
* chaves primárias;
* chaves estrangeiras;
* índices únicos;
* restrições `CHECK`;
* obrigatoriedade;
* valores padrão;
* tipos e escalas;
* comentários do banco;
* triggers;
* views;
* procedures;
* funções.

Use essa fonte principalmente para confirmar sintaxe, cardinalidade, integridade e regras formalizadas.

### 3.2 Modelo de domínio e persistência

Examine:

* entidades;
* objetos de valor;
* classes ORM;
* mapeamentos;
* conversores;
* enums;
* agregados;
* eventos de domínio;
* nomes de propriedades;
* relacionamentos;
* anotações de validação.

Use essa fonte para identificar entidades, propriedades, papéis e vocabulário empregado pela aplicação.

### 3.3 Regras e casos de uso

Examine:

* serviços;
* comandos;
* casos de uso;
* handlers;
* validadores;
* políticas;
* máquinas de estado;
* fluxos de aprovação;
* regras de cálculo;
* regras de transição;
* eventos publicados.

Use essa fonte para entender quando o dado é criado, alterado e utilizado.

### 3.4 Escrita e leitura dos dados

Localize:

* operações `INSERT`;
* operações `UPDATE`;
* exclusões;
* assignments;
* transformações;
* consultas;
* filtros;
* agrupamentos;
* joins;
* ordenações;
* condições;
* consumidores.

Para cada tabela, identifique os principais escritores e leitores. Para cada coluna, identifique onde o valor é atribuído, transformado, validado e consumido.

### 3.5 Interfaces e documentos

Examine:

* contratos de API;
* schemas de mensagens;
* eventos;
* interfaces gráficas;
* rótulos;
* relatórios;
* indicadores;
* manuais;
* requisitos;
* histórias de usuário;
* documentação regulatória;
* glossários.

Use essa fonte para identificar terminologia conhecida pelos usuários e finalidade negocial.

### 3.6 Testes

Examine:

* testes unitários;
* testes de integração;
* fixtures;
* cenários de aceitação;
* dados de exemplo;
* casos de erro;
* limites;
* transições;
* tratamento de nulos.

Os testes são evidências importantes para regras condicionais, exceções e significados de códigos.

## 4. Prioridade e conflito entre evidências

A lista abaixo é um heurístico genérico de força de evidência, útil apenas quando não houver conflito direto entre dimensões diferentes do significado. Ela não substitui a autoridade por dimensão explicada logo a seguir, que é o critério real de desempate quando duas fontes de dimensões diferentes divergem:

1. restrições executáveis e comportamento vigente;
2. regras do domínio e serviços ativos;
3. testes que confirmam o comportamento;
4. contratos de API e eventos vigentes;
5. documentação funcional atualizada;
6. relatórios e consultas de consumidores;
7. comentários;
8. convenções de nomenclatura.

A estrutura física possui alta autoridade para representação e restrições, mas não necessariamente para significado negocial.

A documentação funcional pode possuir alta autoridade semântica, mas pode estar desatualizada em relação ao código.

Não existe uma única fonte "mais forte" para toda dimensão do significado: a autoridade é por dimensão. Estrutura física tem como fonte principal a definição de dados vigente; escrita e cálculo, a regra e a operação de escrita; significado e terminologia, a documentação funcional e a interface; domínio e representação negocial, a regra, a integração e a documentação; uso e impacto, a regra, a consulta, o relatório e a interface. Fonte forte em uma dimensão não resolve outra: nulidade não prova significado, e rótulo não prova preenchimento.

Quando as fontes divergirem:

* não escolha silenciosamente uma versão;
* identifique o conflito;
* indique as fontes conflitantes;
* use como descrição aprovada apenas o conteúdo suficientemente corroborado;
* marque o restante para validação.

## 5. Processo obrigatório para analisar uma tabela

### Etapa 1 — Identificar o tipo do objeto

Classifique a tabela como:

* entidade;
* transação;
* evento;
* item;
* histórico;
* vigência;
* snapshot;
* associação N:N;
* domínio;
* agregação;
* staging;
* auditoria;
* fila;
* controle técnico;
* outro tipo comprovado.

Classifique a tabela como **associação N:N** somente quando uma linha corresponder à relação entre uma ocorrência da entidade A e uma ocorrência da entidade B. Confirme essa classificação por chaves estrangeiras, chaves primárias ou únicas, cardinalidade, operações de escrita, consultas e documentação. A existência de chaves estrangeiras, isoladamente, não autoriza o uso de **"Associa"**. A classificação **associação N:N** determina **"Associa"**; as demais classificações determinam **"Representa"**.

### Etapa 2 — Determinar a granularidade

Formule internamente:

> Uma linha representa exatamente __________.

Para uma associação N:N, complete a frase com uma combinação ou ocorrência da relação entre uma ocorrência de **[entidade A]** e uma ocorrência de **[entidade B]**. Para os demais tipos, complete com a unidade efetivamente representada: entidade, evento, item, versão, vigência, snapshot, agregado, registro de auditoria ou unidade de processamento.

Valide a resposta utilizando:

* chave primária;
* chaves únicas;
* relacionamentos;
* código de criação;
* consultas;
* agrupamentos;
* documentação.

Não aprove uma descrição de tabela de negócio sem granularidade determinada.

### Etapa 3 — Identificar o ciclo de vida

Determine:

* qual evento cria a linha;
* quais eventos a alteram;
* se a linha pode ser excluída;
* se existe exclusão lógica;
* se são mantidas versões;
* quando o registro deixa de ser válido;
* se existe encerramento, cancelamento ou expiração;
* se o registro representa o último estado ou todos os estados.

### Etapa 4 — Determinar o escopo

Identifique:

* ocorrências incluídas;
* ocorrências excluídas;
* filtros implícitos;
* condições de ingresso;
* condições de permanência;
* registros técnicos;
* dados incompletos;
* dados rejeitados;
* registros de teste, quando aplicável.

### Etapa 5 — Determinar a temporalidade

Classifique como:

* estado atual;
* evento;
* histórico de alterações;
* vigência;
* snapshot;
* período contábil;
* acumulado;
* série temporal;
* resultado sem referência temporal.

Identifique a data ou coluna que define a referência.

### Etapa 6 — Determinar a proveniência

Informe se o objeto é:

* fonte oficial;
* cópia;
* réplica;
* cache;
* integração;
* consolidação;
* staging;
* resultado derivado;
* materialização;
* histórico;
* dado manual;
* dado recebido externamente.

### Etapa 7 — Determinar a função negocial

Localize os processos, operações e consumidores que dependem da tabela.

Não use expressões vagas como:

* “utilizada pelo sistema”;
* “serve para consultas”;
* “usada nos processos”;
* “contém dados importantes”.

Nomeie o processo ou finalidade identificável.

### Etapa 8 — Determinar limitações

Procure situações em que a tabela possa ser confundida com:

* outro estágio do processo;
* outra entidade;
* outra data de referência;
* dado oficial versus derivado;
* previsão versus realizado;
* valor operacional versus contábil;
* estado atual versus histórico;
* pedido versus item;
* cliente versus destinatário;
* criação técnica versus evento de negócio.

Inclua a distinção quando houver risco razoável de interpretação incorreta.

## 6. Construção da descrição da tabela

Produza internamente os seguintes componentes:

```text
tabela:
  classificacao:
  verbo_inicial:
  conceito_negocial:
  granularidade:
  evento_de_criacao:
  escopo_inclusao:
  escopo_exclusao:
  semantica_temporal:
  origem_e_proveniencia:
  processos_suportados:
  usos_apropriados:
  usos_inadequados:
  evidencias:
  conflitos:
  confianca:
```

Em seguida, gere a descrição textual.

### Modelo textual

Use a fórmula obrigatória e a regra de escolha entre "Representa" e "Associa" já apresentadas em [Fórmula Recomendada para Tabela](#fórmula-recomendada-para-tabela), na Introdução Conceitual.

Não force todos os componentes em um único parágrafo quando isso prejudicar clareza. Utilize uma definição principal e complementos.

## 7. Processo obrigatório para analisar uma coluna

### Etapa 1 — Identificar o conceito

Determine:

* qual propriedade é representada;
* de qual entidade, evento ou relação ela faz parte;
* se é identificador, medida, classificação, indicador, data, texto, referência ou resultado;
* qual termo de negócio melhor designa o conceito.

### Etapa 2 — Rastrear a produção do valor

Localize:

* atribuição inicial;
* origem externa;
* valor padrão;
* transformação;
* fórmula;
* lookup;
* agregação;
* conversão;
* trigger;
* sincronização;
* atualização posterior.

Classifique o valor como:

* capturado;
* recebido;
* copiado;
* calculado;
* agregado;
* inferido;
* gerado;
* atribuído manualmente;
* controlado pelo banco.

### Etapa 3 — Determinar a referência temporal

Para datas, valores, estados, saldos e classificações, determine:

* em qual momento o valor é válido;
* se é valor atual ou histórico;
* se representa ocorrência, vigência, captura ou processamento;
* se pode ser alterado retroativamente;
* qual fuso horário é aplicado;
* qual precisão temporal existe.

### Etapa 4 — Determinar domínio e representação

Identifique:

* tipo lógico;
* formato;
* unidade;
* moeda;
* precisão;
* escala;
* arredondamento;
* conjunto de valores;
* domínio controlado;
* significado dos códigos;
* dependência de outra coluna.

Não copie o tipo SQL para a descrição de negócio, exceto quando a representação influenciar a interpretação.

### Etapa 5 — Determinar nulabilidade semântica

Quando a coluna aceitar nulo, procure determinar se significa:

* desconhecido;
* não informado;
* não aplicável;
* ainda não ocorrido;
* não calculado;
* indisponível na origem;
* protegido;
* removido;
* erro;
* condição não avaliada.

Não escreva apenas “campo opcional” ou “pode ser nulo”.

### Etapa 6 — Determinar uso e limitação

Identifique:

* condições e decisões que consultam a coluna;
* cálculos em que participa;
* filtros;
* agrupamentos;
* indicadores;
* apresentações;
* integrações;
* possíveis interpretações incorretas.

## 8. Construção da descrição da coluna

Produza internamente:

```text
coluna:
  dominio_multivalorado:
  conceito_negocial:
  entidade_ou_evento:
  definicao_semantica:
  referencia_temporal:
  origem:
  derivacao:
  dominio_e_unidade:
  semantica_do_nulo:
  funcao_negocial:
  limitacoes:
  evidencias:
  conflitos:
  confianca:
```

### Modelo textual

Use as fórmulas obrigatórias e a regra de uso do domínio multivalorado já apresentadas em [Domínio multivalorado: quando usar](#domínio-multivalorado-quando-usar) e [Fórmula Recomendada para Coluna](#fórmula-recomendada-para-coluna), na Introdução Conceitual.

Gere preferencialmente os seguintes campos separados:

### Definição semântica

> **[Propriedade ou conceito]** de **[entidade ou evento]** que representa **[significado essencial e critério de distinção]**.

### Representação

> Expresso em **[unidade, moeda, escala, formato ou domínio]**.

### Origem ou derivação

> Obtido por **[origem, captura, fórmula ou transformação]**.

### Semântica do nulo

> O valor nulo indica **[significado]**.

### Contexto funcional

> Utilizado para **[processo, operação, cálculo ou decisão]**.

### Limitação

> Não representa **[conceito semelhante ou uso inadequado]**.

Quando for necessário retornar uma única descrição, combine esses componentes em uma sequência clara, sem transformar o texto em uma especificação excessivamente longa.

## 9. Regras obrigatórias de redação

1. Formule a definição no singular.

2. Diga o que o conceito é.

3. Use uma frase descritiva completa ou uma expressão nominal suficientemente clara.

4. Comece pelo significado, e não pelo nome físico.

5. Identifique a entidade ou evento a que a propriedade pertence.

6. Utilize linguagem de negócio compreensível.

7. Expanda abreviações não universalmente compreendidas.

8. Não repita o nome da coluna como definição.

9. Não utilize “campo que contém”, “campo que guarda”, “tabela que armazena” como núcleo da descrição.

10. Não descreva exclusivamente o mecanismo de persistência.

11. Não use termos subjetivos como “correto”, “válido”, “normal” ou “adequado” sem informar o critério.

12. Evite “atual”, “último”, “vigente”, “total” e “saldo” sem referência temporal ou escopo.

13. Não use definição negativa como única explicação.

14. Não crie definição circular.

15. Não incorpore longas definições de outros conceitos; relacione-os por referência.

16. Use a mesma estrutura lógica para colunas relacionadas.

17. Diferencie sinônimos técnicos de equivalência semântica real.

18. Mantenha definição semântica separada da fórmula e do procedimento.

19. Inclua exemplos somente quando ajudarem a eliminar ambiguidade.

20. Inclua limitações quando houver risco relevante de interpretação incorreta.

## 10. Conteúdo proibido ou insuficiente

Considere inadequadas descrições como:

> Código do cliente.

> Nome do cliente.

> Data do cadastro.

> Valor total.

> Status do registro.

> Campo utilizado pelo sistema.

> Tabela de dados de pedido.

> Guarda informações do produto.

> Indica se está ativo.

Essas descrições devem ser revisadas porque não identificam suficientemente:

* papel da entidade;
* evento;
* granularidade;
* escopo;
* referência temporal;
* unidade;
* origem;
* domínio;
* significado do nulo;
* finalidade;
* distinção entre conceitos.

## 11. Tratamento de incerteza

Classifique cada conclusão em um dos seis níveis abaixo.

### Fato confirmado

Use quando o significado é uma afirmação direta em fonte adequada, sem contradição.

### Conclusão corroborada

Use quando dois tipos independentes de evidência convergem para o mesmo significado.

### Inferência provável

Use quando a leitura é plausível mas não confirmada. Não escreva uma definição conclusiva: amplie a busca antes de publicar.

### Não determinado

Use quando a busca aplicável já foi concluída e não produziu resultado. Registre como lacuna; não invente o termo.

### Conflito estrutural

Use quando os estados físicos encontrados em diferentes fontes são incompatíveis entre si.

### Conflito semântico

Use quando os significados encontrados em diferentes fontes são incompatíveis entre si.

Uma descrição só pode ser publicada quando todos os termos da fórmula estiverem em fato confirmado ou conclusão corroborada. Para inferência provável, não determinado ou qualquer conflito, apresente a hipótese ou os estados possíveis separadamente, registre quais evidências faltam e utilize "não determinado pelas evidências analisadas" quando necessário.

Não use expressões vagas como "aparentemente" dentro de uma descrição aprovada. Mantenha a incerteza em campo próprio.

## 12. Tratamento de conflitos

Quando código, documentação e banco divergirem:

```text
conflito:
  objeto:
  fonte_1:
  interpretacao_1:
  fonte_2:
  interpretacao_2:
  impacto_na_descricao:
  informacao_que_precisa_ser_validada:
```

Não resolva um conflito semanticamente relevante com base apenas na fonte mais recente sem verificar se ela representa o comportamento efetivamente utilizado.

## 13. Regras para revisão de descrições existentes

Ao revisar uma descrição:

1. preserve o conteúdo comprovadamente correto;
2. remova tautologias;
3. substitua linguagem técnica por conceito de negócio quando possível;
4. acrescente granularidade ausente;
5. acrescente referência temporal;
6. esclareça origem e derivação;
7. esclareça semântica do nulo;
8. acrescente domínio, unidade ou moeda relevante;
9. diferencie conceitos semelhantes;
10. acrescente finalidade e limitações;
11. verifique consistência terminológica com outras descrições;
12. marque conteúdo não confirmado;
13. não aumente o tamanho sem aumentar a precisão ou a utilidade.

## 14. Validação final da descrição de tabela

A descrição somente deve ser considerada satisfatória quando permitir responder:

* O verbo inicial está compatível com a classificação: **"Associa"** para uma associação N:N e **"Representa"** para os demais tipos?
* Se começa com **"Associa"**, a descrição identifica as duas entidades participantes e deixa claro que uma linha representa uma combinação ou ocorrência da relação?
* Se começa com **"Representa"**, a descrição identifica o objeto efetivamente representado?
* O que uma linha representa?
* Qual evento cria a linha?
* Qual é o escopo de inclusão e exclusão?
* A tabela representa estado, evento, vigência, histórico, snapshot ou agregação?
* Qual é a referência temporal?
* Qual é a origem?
* Qual processo depende dela?
* Para quais usos é apropriada?
* Com qual outro conceito poderia ser confundida?
* A descrição está sustentada por evidências?
* Há informação inferida apresentada indevidamente como fato?

## 15. Validação final da descrição de coluna

A descrição somente deve ser considerada satisfatória quando permitir responder:

* Qual propriedade ou conceito é representado?
* De qual entidade ou evento?
* Em qual momento o valor é válido?
* Qual é a unidade, moeda, formato ou domínio relevante?
* Como o valor é obtido?
* O valor é capturado ou derivado?
* O que significa nulo?
* Qual processo, cálculo ou decisão utiliza o valor?
* Qual conceito semelhante não deve ser confundido com ele?
* A descrição é autossuficiente?
* A descrição repete apenas o nome?
* A afirmação está apoiada em evidências?

## 16. Formato recomendado de saída

O dicionário de dados é entregue em dois arquivos Markdown versionados, mantidos juntos e descrevendo o mesmo conjunto de tabelas na mesma versão, mais um `CHANGELOG.md` de estrutura física. Não produza bloco YAML, JSON ou qualquer representação paralela: o formato publicável é sempre a tabela Markdown abaixo.

`dicionario_tabelas.md` contém uma linha por tabela, com exatamente um `H1` e uma única tabela Markdown, ordenada pelo identificador físico:

```text
# Vendas - v1.0.0

| Tabela | Descrição |
|---|---|
| vendas.pedido | Representa pedidos de venda confirmados por uma empresa emissora, com uma linha para cada pedido e empresa emissora. O registro passa a integrar a tabela quando a contratação é aceita pelo sistema de vendas. Inclui pedidos posteriormente cancelados, desde que tenham sido confirmados, e exclui cotações, simulações e carrinhos não concluídos. Mantém o estado mais recente do pedido e é utilizado por faturamento, atendimento, logística e análise de conversão. Não representa faturamento concluído nem receita contabilmente reconhecida. |
| seguranca.usuario_perfil | Associa usuários a perfis de acesso, com uma linha para cada combinação de usuário e perfil. O registro é criado quando o perfil é atribuído ao usuário e utilizado para determinar os perfis relacionados a cada usuário. Não representa o usuário, o perfil nem o histórico de alterações da atribuição. |
```

`dicionario_colunas.md` contém um índice de tabelas seguido de uma seção por tabela, cada seção com a mesma descrição da tabela (textualmente igual à de `dicionario_tabelas.md`) e uma tabela de colunas:

```text
# Vendas - v1.0.0

## Índice de Tabelas

- [vendas.pedido](#vendaspedido)

## vendas.pedido

Representa pedidos de venda confirmados por uma empresa emissora, com uma linha para cada pedido e empresa emissora. [... mesma descrição de dicionario_tabelas.md ...]

| Tabela | Coluna | Descrição |
|---|---|---|
| vendas.pedido | id_pedido | Identificador técnico imutável atribuído ao pedido pelo sistema comercial no momento da confirmação. É único em todo o ambiente e não deve ser reutilizado. Não corresponde ao número de pedido apresentado ao cliente. |
| vendas.pedido | dh_cancelamento | Instante em que o cancelamento do pedido foi confirmado pelo processo comercial. O valor nulo indica que nenhum cancelamento confirmado foi registrado. Não representa o instante da solicitação inicial de cancelamento. |
```

`CHANGELOG.md` registra somente fatos de estrutura física por versão, nunca significado ou finalidade de negócio:

```text
# Vendas - Changelog

## [1.0.0]

### Adicionado

- **Tabela `vendas.pedido`**
```

Evidências, confiança e lacunas de cada objeto não vão nos três arquivos acima: são reportadas ao desenvolvedor na resposta da varredura ou atualização, no formato:

```text
| Objeto | Afirmação | Confiança | Evidências | Limitação |
|---|---|---|---|---|
| vendas.pedido | tabela de pedidos confirmados | Conclusão corroborada | DDL (chave primária id_empresa+id_pedido); serviço ConfirmarPedido; teste de cancelamento posterior | nenhuma |
```

## 17. Regra final de qualidade

A descrição final deve permitir que um consumidor compreenda corretamente o dado **sem precisar ler o código que originou a descrição**, mas toda afirmação relevante deve poder ser rastreada até esse código ou até outra evidência confiável.

Não considere uma descrição de alta qualidade apenas porque ela é extensa. Considere-a de alta qualidade quando for:

> **semanticamente correta, suficientemente completa, consistente, rastreável, compreensível, contextualizada para o negócio e explícita quanto às suas limitações.**
