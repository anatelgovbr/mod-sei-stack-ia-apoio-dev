# Processo de análise semântica

Autoridade sobre: coleta, confiança, conflitos, lacunas e expansão da busca local.

O adaptador define raízes e extensões da codebase. Insumos fornecidos são classificados pelo conteúdo e não alteram o status das camadas do adaptador.

## Tipos de evidência

| Tipo | Pode resolver |
|---|---|
| Documentação funcional | Conceito, granularidade e processo |
| Definição estrutural | Estrutura, representação física e versão; não resolve significado sozinha |
| Modelo ou contrato de dados | Nome lógico e relações |
| Regra de negócio e operação de escrita | Domínio, preenchimento, validação e cálculo |
| Integração | Mapeamento externo e nome público |
| Consulta e projeção | Leitura, filtro, agregação e combinação |
| Apresentação e comportamento de tela | Terminologia, ajuda, opções e transformação visível |
| Enumeração e constante | Conjunto fechado de valores |
| Relatório | Granularidade e terminologia de negócio |
| Teste, massa e comentário confirmado pelo código | Cenário, valor válido e intenção verificável |

## Busca progressiva

Indexe os insumos fornecidos, mas sempre execute busca na codebase. Expanda somente os termos da fórmula ainda indeterminados ou conflitantes:

0. **Escritor, obrigatória e primeira:** antes de buscar por nome, localize o objeto que **insere ou atualiza** a tabela, seja procedure, gatilho, rotina de carga ou tela de gravação, e leia-o inteiro, não só o trecho que cita a coluna. Um escritor costuma resolver a maioria das colunas da tabela de uma vez e fixa, para o módulo inteiro, unidade, domínio, momento e regra de derivação. É a leitura de maior rendimento por unidade de esforço e a única que mostra o valor sendo produzido.
1. **Direta:** identificador físico, nome lógico, acessores, constantes, rótulos e variantes do adaptador nas camadas mais relevantes.
2. **Indireta:** chamadores, assinaturas, aliases, junções, filtros e validações.
3. **Vizinhança:** valores isolados, objetos relacionados, outro lado do alvo, testes, massas e documentação próxima.

Não interrompa uma rodada na primeira ocorrência. Scaffolding, repetição do nome físico e existência de valor sem significado contam como ausência de resultado.

**Quem escreve o valor define o significado; quem apenas o exibe sugere.** Rótulo, cabeçalho de relatório e texto de tela são evidência de terminologia, não de conteúdo, e só valem quando a tela em que aparecem referencia a própria tabela. Descartar antes de usar: linha comentada na linguagem do alvo, arquivo em diretório de cópia, backup ou versão anterior, e rótulo colhido de tela que não toca a tabela. Mineração ampla de rótulo sem esses filtros produz associação falsa em volume, e associação falsa publicada é pior do que lacuna marcada.

## Autoridade por dimensão

| Dimensão | Fonte principal | Conferência |
|---|---|---|
| Estrutura física | Fonte estrutural vigente | Definição de dados e bloco de versão |
| Escrita e cálculo | Regra e operação de escrita | Validação, testes e consumidores |
| Significado e terminologia | Documentação funcional e interface | Regra, integração, consulta e tela |
| Significado, sem documentação funcional disponível | Regra e operação de escrita | Interface, integração e consulta |
| Domínio e representação negocial | Regra, integração e documentação | Estrutura, validação, interface e testes |
| Uso e impacto | Regra, consulta, relatório e interface | Escritores e consumidores |

Fonte forte em uma dimensão não resolve outra: nulidade não prova significado; rótulo não prova preenchimento.

Em alvo legado sem documentação funcional recuperável, a autoridade sobre significado desloca-se para a regra e a operação de escrita, e a interface passa a conferência. Registre no relatório quando aplicar essa inversão.

## Confiança

| Nível | Condição | Uso |
|---|---|---|
| Fato confirmado | Afirmação direta em fonte adequada, sem contradição | Preencher o termo correspondente |
| Conclusão corroborada | Dois tipos independentes convergem | Preencher o termo correspondente |
| Inferência provável | Leitura plausível sem confirmação | Não publicar; ampliar busca |
| Não determinado | Busca aplicável concluída sem resultado | Registrar lacuna |
| Conflito estrutural | Estados físicos incompatíveis | Aplicar conflito estrutural |
| Conflito semântico | Significados incompatíveis | Aplicar conflito semântico |

Publique a descrição com cada termo confirmado ou corroborado preenchido e cada termo ainda aberto ocupado pelo marcador de lacuna. Registre confiança no relatório, e mantenha os dicionários e o `CHANGELOG.md` livres dela.

## Conflitos

**Estrutural:** bloqueie somente os objetos e fatos dependentes da divergência, e deixe estado, `CHANGELOG.md` e A8 para depois da decisão humana sobre qual fonte vale. Continue nos objetos não afetados e reporte fontes, estados possíveis, impacto e decisão necessária.

**Semântico:** calcule o conteúdo comum e use-o apenas nos termos comprovados. Qualquer termo controvertido impede publicar a descrição, sem bloquear a estrutura nem outros objetos. Reporte leituras, conteúdo comum, lacuna e decisão necessária.

## Lacunas e fonte remota

Termo não resolvido após as rodadas é lacuna. **Publique a descrição assim mesmo**, com os termos comprovados preenchidos e cada termo aberto ocupado pelo marcador de lacuna de `formato-dicionario-de-dados.md`. Célula vazia deixa de ser resultado aceitável: ela esconde o que falta e faz o trabalho parcial se perder entre execuções, enquanto a descrição marcada preserva o que já se sabe e deixa a pendência localizável por busca de texto e contável por ferramenta.

Preserve texto anterior somente se continuar comprovado e já obedecer à fórmula. Agregue resultados negativos equivalentes, mas nomeie evidências positivas, conflitos e lacunas que alterem uma descrição. No motivo do marcador, escreva o que já foi buscado, para que a retomada não repita a mesma varredura.

Se uma fonte remota específica puder resolver a lacuna, aplique a política de execução do `SKILL.md`: identifique objeto, fonte e escopo e aguarde autorização explícita. Sem autorização ou resultado suficiente, reporte a lacuna e prossiga com os demais objetos.
