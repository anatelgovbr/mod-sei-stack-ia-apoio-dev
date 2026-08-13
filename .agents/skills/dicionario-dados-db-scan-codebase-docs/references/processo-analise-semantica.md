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

1. **Direta, obrigatória:** identificador físico, nome lógico, acessores, constantes, rótulos e variantes do adaptador nas camadas mais relevantes.
2. **Indireta:** chamadores, assinaturas, aliases, junções, filtros e validações.
3. **Vizinhança:** valores isolados, objetos relacionados, outro lado do alvo, testes, massas e documentação próxima.

Não interrompa uma rodada na primeira ocorrência. Scaffolding, repetição do nome físico e existência de valor sem significado contam como ausência de resultado.

## Autoridade por dimensão

| Dimensão | Fonte principal | Conferência |
|---|---|---|
| Estrutura física | Fonte estrutural vigente | Definição de dados e bloco de versão |
| Escrita e cálculo | Regra e operação de escrita | Validação, testes e consumidores |
| Significado e terminologia | Documentação funcional e interface | Regra, integração, consulta e tela |
| Domínio e representação negocial | Regra, integração e documentação | Estrutura, validação, interface e testes |
| Uso e impacto | Regra, consulta, relatório e interface | Escritores e consumidores |

Fonte forte em uma dimensão não resolve outra: nulidade não prova significado; rótulo não prova preenchimento.

## Confiança

| Nível | Condição | Uso |
|---|---|---|
| Fato confirmado | Afirmação direta em fonte adequada, sem contradição | Preencher o termo correspondente |
| Conclusão corroborada | Dois tipos independentes convergem | Preencher o termo correspondente |
| Inferência provável | Leitura plausível sem confirmação | Não publicar; ampliar busca |
| Não determinado | Busca aplicável concluída sem resultado | Registrar lacuna |
| Conflito estrutural | Estados físicos incompatíveis | Aplicar conflito estrutural |
| Conflito semântico | Significados incompatíveis | Aplicar conflito semântico |

Uma descrição só pode ser publicada quando todos os termos da fórmula estiverem confirmados ou corroborados. Registre confiança no relatório, não nos dicionários ou no `CHANGELOG.md`.

## Conflitos

**Estrutural:** bloqueie somente os objetos e fatos dependentes da divergência; não derive estado, `CHANGELOG.md` ou A8 escolhendo uma fonte. Continue nos objetos não afetados e reporte fontes, estados possíveis, impacto e decisão necessária.

**Semântico:** calcule o conteúdo comum e use-o apenas nos termos comprovados. Qualquer termo controvertido impede publicar a descrição, sem bloquear a estrutura nem outros objetos. Reporte leituras, conteúdo comum, lacuna e decisão necessária.

## Lacunas e fonte remota

Termo não resolvido após as rodadas é lacuna. Não publique descrição parcial; preserve texto anterior somente se continuar comprovado e já obedecer à fórmula. Agregue resultados negativos equivalentes, mas nomeie evidências positivas, conflitos e lacunas que alterem uma descrição.

Se uma fonte remota específica puder resolver a lacuna, aplique a política de execução do `SKILL.md`: identifique objeto, fonte e escopo e aguarde autorização explícita. Sem autorização ou resultado suficiente, reporte a lacuna e prossiga com os demais objetos.
