# Requisitos dos módulos

Esta pasta guarda, para cada módulo, as regras de negócio, os requisitos funcionais e os requisitos técnicos que valem hoje. Esses documentos continuam valendo depois da entrega e mudam na mesma entrega do código, no modelo que o desenvolvimento guiado por especificação chama de spec-anchored.

O código continua sendo a fonte do comportamento executável. Os requisitos descrevem o comportamento que o código deve ter e serve de contexto para pessoas e agentes antes de mudar o módulo.

## Estrutura dos documentos

| Arquivo | O que guarda | Template |
|---|---|---|
| `<modulo>/README.md` | Propósito, índice das regras de negócio, lista dos arquivos de requisitos funcionais e glossário do módulo | [TEMPLATE-README.md](TEMPLATE-README.md) |
| `<modulo>/regras-de-negocio.md` | Regras de negócio (`RN`) do módulo, agrupadas por assunto | [TEMPLATE-regras-de-negocio.md](TEMPLATE-regras-de-negocio.md) |
| `<modulo>/requisitos-funcionais/<funcionalidade>.md` | Requisitos funcionais (`RF`) de uma funcionalidade do módulo, em seções por operação ou etapa; cada funcionalidade tem o seu arquivo na pasta `requisitos-funcionais/` | [TEMPLATE-requisitos-funcionais.md](TEMPLATE-requisitos-funcionais.md) |
| `<modulo>/requisitos-tecnicos.md` | Requisitos técnicos do módulo (`RT`): os limites que a solução respeita e o grau de qualidade que ela precisa atingir. | [TEMPLATE-requisitos-tecnicos.md](TEMPLATE-requisitos-tecnicos.md) |
| `docs/architecture/adr/<modulo>/` | O porquê de cada decisão arquitetural do módulo; as decisões do SEI inteiro ficam em `docs/architecture/adr/sei/`; a ADR aceita não é editada | [ADR-TEMPLATE.md](../architecture/ADR-TEMPLATE.md) |

Todo módulo tem essa estrutura: o `README.md`, o `regras-de-negocio.md`, a pasta `requisitos-funcionais/`, com um arquivo por funcionalidade, e o `requisitos-tecnicos.md`. Cada arquivo ou pasta tem o nome do template que o gera, sem o prefixo `TEMPLATE-`. Arquivo ou seção sem conteúdo traz "Nenhuma definição.".

A pasta `<modulo>` tem o mesmo nome da pasta do módulo em `docs/dicionario_dados/` e em `docs/architecture/adr/`. Funcionalidade é um serviço do módulo que o usuário reconhece pelo nome, como "associação de documento modelo", "geração com documento modelo" ou "pesquisa de protocolos". As regras de negócio não seguem as funcionalidades, porque uma regra pode valer para várias delas; elas ficam agrupadas por assunto, como "Associação" ou "Documento modelo". O arquivo de cada funcionalidade em `requisitos-funcionais/` separa os requisitos em seções por operação, como listar, cadastrar e alterar ou excluir, ou por etapa de um fluxo, como aplicar o modelo.

## Papel de cada documento

Cada documento responde a uma pergunta diferente, é lido por pessoas diferentes e muda por motivos diferentes. Por isso cada um fica no seu lugar.

| Documento | Pergunta que responde | Principais leitores | Quando muda |
|---|---|---|---|
| `regras-de-negocio.md` | Quais regras de negócio o módulo deve cumprir? | Área de negócio e responsáveis pelo comportamento do módulo | A norma, a política ou a decisão de negócio muda |
| `requisitos-funcionais/<funcionalidade>.md` | O que o sistema faz em cada operação e como isso é verificado? | Desenvolvimento e testes | O comportamento de uma operação muda |
| `requisitos-tecnicos.md` | Quais limites a solução respeita e qual nível de qualidade ela deve atingir? | Desenvolvimento e arquitetura | Uma decisão técnica ou uma ADR muda |
| `docs/architecture/adr/<modulo>/` | Por que uma decisão de arquitetura foi tomada? | Responsáveis pela arquitetura | Nunca: a ADR aceita não é editada, e uma ADR nova a substitui |

### Por que a regra de negócio não fica no arquivo funcional

Uma regra de negócio costuma valer para várias operações e até para várias funcionalidades. No APT, a RN-APT-002 (documento modelo válido) vale no cadastro da associação e na geração do documento, que estão em arquivos funcionais diferentes. Se a regra ficasse dentro de um deles, o outro repetiria o texto, e cada mudança da regra precisaria ser feita em dois lugares, com risco de um ficar diferente do outro.

Em arquivo próprio, a regra é escrita uma vez. Cada requisito funcional descreve só o que a operação faz quando a regra é cumprida ou violada. O [Business Rules Manifesto](https://www.businessrulesgroup.org/brmanifesto.htm) defende esse modelo no artigo 2, "Separate From Processes, Not Contained In Them": "Rules apply across processes and procedures. There should be one cohesive body of rules, enforced consistently across all relevant areas of business activity."

### Por que o requisito técnico fica separado

O requisito funcional diz o que o sistema faz. O requisito técnico diz dentro de quais limites e quão bem o sistema faz. Por exemplo, a RT-APT-004 (proteger o conteúdo do documento modelo) vale para todas as operações do APT e não é o comportamento de nenhuma delas.

O requisito técnico também muda por outros motivos: uma ADR, uma nova versão do SEI ou uma decisão sobre a arquitetura, muitas vezes sem mudar o que o usuário vê. Separado, ele é o único documento do módulo ligado às ADRs. O [manual do IREB](https://isqi.org/media/82/71/8c/1744288379/cpre_foundationlevel_handbook_EN_v1.2.pdf) trata requisito funcional, requisito de qualidade e restrição como tipos diferentes de requisito.

### Por que os requisitos funcionais ficam em pasta

Os requisitos funcionais crescem com o número de funcionalidades do módulo. Cada funcionalidade tem o seu arquivo, e uma mudança mexe só no arquivo da funcionalidade que muda. O [template de SRS de Karl Wiegers](https://research.cs.queensu.ca/home/emads/teaching/slides/srs_template_sep14.pdf) organiza os requisitos funcionais da mesma forma, "by system features, the major services provided by the product". As regras de negócio e os requisitos técnicos valem para o módulo todo e continuam pequenos, então ficam em arquivo único.

### Por que o README do módulo

O README é a porta de entrada. Ele mostra o propósito do módulo, a lista das regras de negócio, a lista dos arquivos funcionais e o glossário. O glossário define o vocabulário uma vez, e as regras e os requisitos usam os mesmos termos.

### Exemplo: o mesmo assunto em cada documento

No APT, o documento modelo válido aparece assim:

| Documento | O que diz |
|---|---|
| RN-APT-002, em `regras-de-negocio.md` | O que torna um documento válido como modelo: existir, ser de editor interno, não ser sigiloso, não estar cancelado e a unidade do usuário ter acesso a ele. |
| RF-APT-009, em `requisitos-funcionais/associacao-de-documento-modelo.md` | No cadastro da associação, o sistema recusa o protocolo que não corresponde a documento modelo válido e informa o motivo. |
| RF-APT-017, em `requisitos-funcionais/geracao-com-documento-modelo.md` | Na geração, se o documento modelo não é válido para a unidade do usuário, o documento é gerado sem o conteúdo do modelo. |
| RT-APT-004, em `requisitos-tecnicos.md` | O módulo omite o texto do documento modelo das mensagens, das respostas da tela e dos registros de log. |

A fonte de cada elemento do formato está na seção "Fontes do formato".

## Classificação dos requisitos

Faça estas perguntas, em ordem, para cada enunciado:

1. O enunciado descreve um resultado, um comportamento ou uma interação de uma função do sistema? Se sim, é requisito funcional e vai para o arquivo da funcionalidade em `requisitos-funcionais/`.
2. O enunciado continuaria necessário com um computador infinitamente rápido, sem custo e sem falhas? Se não, é requisito técnico.
3. O enunciado descreve grau de desempenho, disponibilidade, tolerância a falha, segurança, rastreabilidade, integridade ou usabilidade? É requisito técnico, mesmo quando o usuário percebe.
4. O enunciado limita a solução com tecnologia, norma técnica, convenção ou interface publicada? É requisito técnico.

Regras que acompanham as perguntas:

- Cada enunciado fica em um lugar só. Quando um requisito induz outro do outro lado, cada um fica no seu arquivo, e o requisito técnico cita o requisito funcional relacionado no enunciado, entre parênteses.
- Requisito técnico que vale para o SEI inteiro não se repete nos requisitos do módulo. Exemplos: encoding, validação de link e permissão, padrão transacional, auditoria SIP, disponibilidade.
- Justificativa e alternativas de decisão arquitetural ficam na ADR. O requisito cita o número da ADR e não copia o conteúdo.
- Valores de parâmetro, limites e contratos fixados por uma decisão ficam nos requisitos técnicos, não na ADR.

Um requisito técnico só entra no `requisitos-tecnicos.md` quando passa nos três testes:

1. Foi decidido: mudar o requisito exige decisão de alguém além de quem desenvolve, como área de negócio, norma, ADR ou decisão registrada. Valor que o desenvolvedor pode trocar sem pedir aprovação, como o tamanho de uma página de resultado, é detalhe de implementação.
2. É do módulo: regra que vale para todos os módulos, como encoding, permissão ou versionamento, não se repete.
3. Limita ou mede a solução: descrição de como o código ou o banco estão hoje, dívida técnica e instrução de instalação ou de configuração não limitam nem medem a solução.

| Enunciado | Destino |
|---|---|
| "Somente usuário com o perfil Gestor pode cancelar o registro." | `regras-de-negocio.md`, como regra, e o arquivo da funcionalidade em `requisitos-funcionais/`, como requisito de recusa |
| "Quando o usuário arquivar o processo, o sistema deve lançar andamento com data, usuário e unidade." | Arquivo da funcionalidade em `requisitos-funcionais/`, porque a unidade consulta o andamento no processo |
| "A consulta responde em até 3 segundos para 95% das chamadas." | `requisitos-tecnicos.md`, porque fala do grau de desempenho |
| "O registro de auditoria não pode ser alterado nem excluído." | `requisitos-tecnicos.md`, porque é um limite de segurança |
| "Toda ação de página valida link assinado e permissão." | Nenhum arquivo do módulo, porque a regra vale para o SEI inteiro |
| "Usar processo Python persistente acessado por socket Unix." | ADR, porque é escolha entre alternativas de arquitetura |

## Identificadores

| Elemento | Formato | Exemplo |
|---|---|---|
| Requisito funcional | `RF-<SIGLA>-<NNN>` | `RF-PET-012` |
| Regra de negócio | `RN-<SIGLA>-<NNN>` | `RN-PET-003` |
| Requisito técnico | `RT-<SIGLA>-<NNN>` | `RT-PET-004` |
| Cenário de um requisito funcional | `RF-<SIGLA>-<NNN>.C<n>` | `RF-PET-012.C2` |
| ADR | `ADR-<SIGLA>-<NNN>`, numerada por módulo; a decisão do SEI inteiro usa a sigla `SEI` | `ADR-PESQ-001` |

- `<SIGLA>` é a sigla do módulo usada nos recursos SIP (`md_<sigla>_`), em maiúsculas.
- O número é sequencial por módulo e por prefixo. ID novo usa o número seguinte ao maior já usado, inclusive os de requisitos retirados, que ficam no histórico do Git.
- Nenhum ID é renumerado ou reutilizado. Requisito que muda de tipo, como de funcional para técnico, sai do arquivo antigo e entra no novo com ID novo; a descrição da MR registra os dois IDs.
- Requisito retirado sai do arquivo, e a descrição da MR registra o ID retirado e o motivo.
- Não há campo de estado por requisito. O que está no arquivo está vigente.
- A regra de negócio usa o prefixo `RN`, o mesmo que a equipe usa nos documentos dos módulos, como `[RN16]` em comentários do litigioso. Com a sigla e o hífen, o ID não se confunde com as classes `*RN.php`.

## Formato dos requisitos

A regra de negócio é uma frase declarativa, em linguagem de negócio, sem nome técnico como nome de permissão, de tabela ou de classe. Ela entra em `regras-de-negocio.md` quando vale para dois ou mais requisitos ou vem de norma; regra usada por um requisito só fica no enunciado desse requisito. O README do módulo lista o ID e o título de cada regra, agrupados pelo mesmo assunto, e muda junto com `regras-de-negocio.md`. Quando um requisito funcional usa um termo definido por uma regra, a entrada do glossário cita a regra, como "Documento modelo válido: documento modelo que cumpre as condições da RN-APT-002". Assim o leitor chega à regra a partir do requisito.

O requisito funcional usa a notação EARS, com um único "deve" por enunciado:

| Padrão | Forma |
|---|---|
| Sempre válido | O `<sistema>` deve `<resposta>`. |
| Estado | Enquanto `<estado>`, o `<sistema>` deve `<resposta>`. |
| Evento | Quando `<gatilho>`, o `<sistema>` deve `<resposta>`. |
| Funcionalidade opcional | Onde `<funcionalidade estiver habilitada>`, o `<sistema>` deve `<resposta>`. |
| Comportamento indesejado | Se `<situação indesejada>`, então o `<sistema>` deve `<resposta>`. |
| Combinação | Enquanto `<estado>`, quando `<gatilho>`, o `<sistema>` deve `<resposta>`. |

Cada requisito tem o campo Verificação (teste automatizado, teste manual ou inspeção). Todo requisito verificado por teste manual tem cenários Dado/Quando/Então em estilo declarativo. O cenário descreve o comportamento em linguagem de negócio, com três a cinco passos, e não descreve cliques, campos ou telas. Cada cenário é um item da lista do requisito, logo abaixo da Verificação, com o ID e o nome, e cada passo é um subitem com as palavras-chave `Dado`, `Quando`, `Então` e `E`. A lista mantém um passo por linha, porque o Markdown junta em um parágrafo só as linhas seguidas que não são lista.

Para conferir se os cenários de um requisito estão completos, verifique:

1. O caso desejado.
2. O par indesejado: o que acontece quando a condição do requisito falha.
3. Um cenário para cada classe de entrada que muda o resultado, como cada motivo de recusa.
4. Os limites: o valor no limite e o valor logo acima dele.
5. Os estados do objeto que mudam o resultado, como ativo, inativo, cancelado, excluído ou sigiloso.
6. O usuário com e sem a permissão da operação.

Caso já coberto por regra que vale para o SEI inteiro, por requisito técnico ou por questão em aberto não ganha cenário. Caso de uma regra de negócio já coberto por cenário de outro requisito não se repete; o requisito ganha cenário só para o que muda no seu contexto. Requisito sem cenário de caso indesejado precisa estar em um destes casos: o caso indesejado é outro requisito, citado no campo Verificação, como "caso indesejado em RF-APT-020"; ou não existe falha possível, como em uma ordenação.

O requisito técnico tem título, enunciado com um único "deve" e dois campos: Categoria e Critério de aceitação. O critério diz o resultado observável que prova o requisito e, entre parênteses, como conferir: teste automatizado, teste manual ou leitura do código. Ele faz para o requisito técnico o papel que os cenários fazem para o requisito funcional. Ele pode ser um limite, como "O módulo deve exigir o SEI na versão 5.0.3 ou superior", ou um grau de qualidade, como "O módulo deve copiar o modelo no máximo uma vez para cada documento gerado". Quando fala de grau, o enunciado traz número ou limite, como "no máximo uma vez" ou "até 3 segundos". Os requisitos ficam em ordem de ID. A categoria segue o Volere, que guarda o tipo do requisito como atributo. Arquivo sem requisito técnico traz "Nenhuma definição.".

A categoria vem desta lista:

| Categoria | Para quê | Base |
|---|---|---|
| Compatibilidade (Compatibility) | Versões e ambiente que o módulo exige, como a versão mínima do SEI | [Q42, ISO/IEC 25010:2023](https://quality.arc42.org/standards/iso-25010), característica Compatibility |
| Integração (Integration) | Como o módulo usa o SEI ou outro sistema, como o índice do Solr | ISO/IEC 25010:2023, subcaracterística Interoperability, de Compatibility; [IREB](https://isqi.org/media/82/71/8c/1744288379/cpre_foundationlevel_handbook_EN_v1.2.pdf), seção Interfaces do modelo de especificação |
| Confiabilidade (Reliability) | O que acontece quando algo falha ou se repete | ISO/IEC 25010:2023, característica Reliability |
| Segurança (Security) | O que não pode ser exposto, alterado ou forjado | ISO/IEC 25010:2023, característica Security |
| Rastreabilidade (Accountability) | O que fica registrado em log ou em auditoria | ISO/IEC 25010:2023, subcaracterísticas Accountability, de Security, e Analysability, de Maintainability |
| Manutenção (Maintainability) | Nomes e convenções que não podem mudar | ISO/IEC 25010:2023, característica Maintainability; [arc42, seção 2](https://docs.arc42.org/section-2/), "conventions" |
| Organização (Organizational constraints) | Como o módulo é publicado ou mantido | [arc42, seção 2](https://docs.arc42.org/section-2/), "organizational and political constraints"; [IREB](https://isqi.org/media/82/71/8c/1744288379/cpre_foundationlevel_handbook_EN_v1.2.pdf), restrições |

Regras de redação do enunciado, para requisito funcional e técnico:

- O sujeito é quem responde pelo requisito, em geral "O sistema" ou "O módulo", e o verbo fica na voz ativa.
- A frase fica na forma positiva: "deve omitir o texto" no lugar de "não deve exibir o texto".
- Cada frase tem uma ideia só, sem ponto e vírgula. Duas ideias viram dois requisitos.
- "Cada" substitui "todos", "toda" e "100%".
- O enunciado não descreve implementação, como a ordem interna das chamadas ou a forma de uma checagem, salvo quando a decisão técnica é o próprio requisito.

Requisito técnico que vem de uma ADR cita o número dela no fim do enunciado, entre parênteses, como "(ADR-APT-001)". O porquê de cada requisito fica na ADR ou na descrição da MR que o criou, e nunca é explicado pela leitura do código.

## Ciclo de uma mudança

1. Quem propõe a mudança avalia se ela é decisão arquitetural. As regras de registro estão em `docs/architecture/adr/README.md`.
2. Quando a mudança exige ADR, a ADR nasce `proposta` antes da implementação e cita os IDs `RT` afetados ou a criar. O requisito técnico não muda enquanto a ADR estiver `proposta`.
3. Quando a mudança não exige ADR, os requisitos técnicos mudam na mesma MR, e o motivo fica na descrição da MR.
4. Mudança que contraria uma ADR aceita citada em um requisito técnico exige ADR nova, que substitui a anterior.
5. Na MR que entrega o código, os arquivos do módulo passam a descrever o novo estado. A ADR aceita entra na mesma MR, e o requisito passa a citar a ADR nova no lugar da substituída.
6. A descrição da MR lista cada ID adicionado, alterado ou retirado, com o motivo em uma frase. O commit de merge do GitLab aponta para a MR.
7. A revisão bloqueia a MR que muda comportamento ou requisito técnico descritos sem atualizar os requisitos, ou que contraria requisito ou ADR aceita. Requisito que cita ADR `descontinuada` é defeito.

A adoção é incremental. Quando um módulo entra no padrão, cada mudança documenta só a parte que toca, e o módulo não é documentado inteiro de uma vez. Cada requisito precisa vir de uma fonte real, como norma, área demandante, documento do módulo, decisão registrada ou o comportamento de uma versão já entregue, mesmo que a fonte não fique escrita no documento. Requisito escrito a partir da leitura do código descreve a implementação, e não o que o módulo deve fazer.

## Conteúdo fora dos requisitos

| Conteúdo | Destino |
|---|---|
| Plano de tarefas e checklist de implementação | Planejamento da mudança, fora desta pasta |
| Histórias de usuário como estrutura do documento | Planejamento da mudança, fora desta pasta |
| Questões em aberto | Planejamento da mudança que tratar a questão |
| Desenho do mecanismo, com nomes de classe ou método | Código ou documentação própria do módulo, fora dos requisitos |
| Modelo físico de dados | `docs/dicionario_dados/<modulo>/` |
| Estado atual do código ou do banco, como parâmetro com valor fixo, coluna sem uso ou tamanho de página | Código e `docs/dicionario_dados/<modulo>/` |
| Dívida técnica e código a remover | Comentário `TODO:` no código ou planejamento da mudança que vai tratar |
| Instrução de instalação, configuração e operação, como nomes de parâmetros a preencher | README de instalação do módulo |
| Convenção que vale para todos os módulos, como versionamento e release | Não se repete nos requisitos do módulo |
| Histórico, autoria e datas de cada mudança | Git e descrição da MR |
| Prioridade e estimativa | Backlog da equipe |
| Gates técnicos, como `php -l` | Ferramentas de validação, fora desta pasta |
| Instruções para agente de IA | Stack de IA, fora desta pasta |

## Fontes do formato

Cada elemento do formato tem uma fonte reconhecida. Os trechos abaixo foram conferidos nas fontes originais.

| Elemento | Fonte | O que a fonte diz |
|---|---|---|
| Requisitos que continuam valendo depois da entrega | [Böckeler, martinfowler.com](https://martinfowler.com/articles/exploring-gen-ai/sdd-3-tools.html) | "Spec-anchored: The spec is kept even after the task is complete, to continue using it for evolution and maintenance of the respective feature." |
| Requisitos do módulo separados da proposta de mudança | [OpenSpec, conceitos](https://github.com/Fission-AI/OpenSpec/blob/main/docs/concepts.md) | "Specs describe current behavior" e "Changes propose modifications (as deltas)" |
| Requisitos separados do documento de decisão | [Python, PEP 1](https://peps.python.org/pep-0001/) | "Once resolution is reached, a PEP is considered a historical document rather than a living specification. Formal documentation of the expected behavior should be maintained elsewhere" |
| ADR guarda o porquê de uma decisão de arquitetura | [Michael Nygard, Documenting Architecture Decisions](https://www.cognitect.com/blog/2011/11/15/documenting-architecture-decisions) | "We will keep a collection of records for "architecturally significant" decisions: those that affect the structure, non-functional characteristics, dependencies, interfaces, or construction techniques." |
| ADR sem desenho detalhado | [Microsoft, Azure Well-Architected Framework, ADR](https://learn.microsoft.com/en-us/azure/well-architected/architect-role/architecture-decision-record) | "Avoid making decision records design guides." |
| Desenho detalhado fora da ADR | [Olaf Zimmermann, ADR Mistakes](https://ozimmer.ch/practices/2026/09/12/ADRMistakes.html) | "detailed design specifications deserve their own place in the documentation" |
| Requisito funcional separado do técnico | [IREB, manual CPRE Foundation Level](https://isqi.org/media/82/71/8c/1744288379/cpre_foundationlevel_handbook_EN_v1.2.pdf) | "Quality requirements pertain to quality concerns that are not covered by functional requirements" |
| Regras de negócio em arquivo próprio | [Business Rules Manifesto](https://www.businessrulesgroup.org/brmanifesto.htm), artigo 2 | "Rules apply across processes and procedures. There should be one cohesive body of rules" |
| Cada enunciado em um lugar só | [INCOSE, Guide to Writing Requirements v4](http://web.archive.org/web/20240919131806id_/https://www.incose.org/docs/default-source/working-groups/requirements-wg/guidetowritingrequirements/incose_rwg_gtwr_v4_summary_sheet.pdf), R30 | "Express each need and requirement once and only once." |
| Um único "deve" por requisito | INCOSE, Guide to Writing Requirements v4, C5 | "The need or requirement statement should state a single capability, characteristic, constraint, or quality factor." |
| Requisito sem descrição de implementação | INCOSE, Guide to Writing Requirements v4, R31 | "Avoid stating implementation in a need statement or requirement statement unless there is rationale for constraining the design." |
| Sujeito na voz ativa | INCOSE, Guide to Writing Requirements v4, R2 | "Use the active voice in the need or requirement statement with the responsible entity clearly identified as the subject of the sentence." |
| Forma positiva | INCOSE, Guide to Writing Requirements v4, R16 | "Avoid the use of "not."" |
| Uma ideia por frase | INCOSE, Guide to Writing Requirements v4, R18 | "Write a single sentence that contains a single thought conditioned and qualified by relevant sub-clauses." |
| "Cada" no lugar de "todos" | INCOSE, Guide to Writing Requirements v4, R32 | "Use "each" instead of "all", "any", or "both" when universal quantification is intended." |
| Glossário do módulo | INCOSE, Guide to Writing Requirements v4, R4 | "Define all terms used within the need statement and requirement statement within an associated glossary and/or data dictionary." |
| Notação EARS e comportamento indesejado | [Alistair Mavin, EARS](https://alistairmavin.com/ears/) | "Unwanted behaviour requirements are used to specify the required system response to undesired situations and are denoted by the keywords If and Then." |
| Requisitos funcionais por funcionalidade | [Karl Wiegers, template de SRS](https://research.cs.queensu.ca/home/emads/teaching/slides/srs_template_sep14.pdf) | "organizing the functional requirements for the product by system features, the major services provided by the product" |
| Critério de aceitação e métrica no enunciado | [Volere, Atomic Requirements](https://www.volere.org/wp-content/uploads/2018/12/06-Atomic-Requirements.pdf), Fit Criterion | "A measurement of the requirement such that it is possible to non-subjectively test whether the solution fits the original requirement." |
| Critério de aceitação separado do método | INCOSE, Guide to Writing Requirements v4, atributos A6 e A8 | "A6 - System Verification or System Validation Success Criteria" e "A8 - System Verification or System Validation Method" |
| Categoria do requisito técnico | INCOSE, Guide to Writing Requirements v4, R29 | "Classify needs and requirements according to the aspects of the problem or system it addresses." |
| Nomes das categorias do requisito técnico | [Q42, ISO/IEC 25010:2023](https://quality.arc42.org/standards/iso-25010); [arc42, seção 2](https://docs.arc42.org/section-2/) | ISO/IEC 25010:2023: "Compatibility", "Reliability", "Security" e "Maintainability", com as subcaracterísticas "Interoperability", "Accountability" e "Analysability". arc42: "technical constraints, organizational and political constraints and conventions" |
| Restrição como tipo de requisito técnico | [IREB](https://isqi.org/media/82/71/8c/1744288379/cpre_foundationlevel_handbook_EN_v1.2.pdf) | "Constraints are requirements that limit the solution space beyond what is necessary to meet the given functional requirements and quality requirements." |
| Tipo do requisito como atributo | Volere, Atomic Requirements, Requirement Type | "The type of the requirement as defined in the Volere requirements template." |
| ID único para cada requisito | Volere, Atomic Requirements, Requirement Number | "The only purpose of this identifier is as an identifier for this requirement." |
| Cenário declarativo | [Cucumber, Writing better Gherkin](https://cucumber.io/docs/bdd/better-gherkin/) | "Your scenarios should describe the intended behaviour of the system, not the implementation." |
| Palavras-chave dos cenários em português | [Cucumber, gherkin-languages.json](https://raw.githubusercontent.com/cucumber/gherkin/main/gherkin-languages.json) | Português: "Cenário", "Dado", "Quando", "Então" e "E" |
| Lista de cobertura dos cenários | [SWEBOK V4](https://ieeecs-media.computer.org/media/education/swebok/swebok-v4.pdf), p. 1-14 | "combining ATDD or BDD with appropriate functional test coverage criteria, such as Domain Testing, Boundary Value Analysis and Pairwise Testing (see the Software Testing KA), can reduce the likelihood of requirements incompleteness." |
| Requisito sem campo de justificativa | [Spec Kit, spec-template.md](https://github.com/github/spec-kit/blob/main/templates/spec-template.md) e [OpenSpec, template de spec](https://github.com/Fission-AI/OpenSpec/blob/main/schemas/spec-driven/templates/spec.md) | Os dois modelos têm só o enunciado, como "System MUST [specific capability]", ou o enunciado e os cenários ("### Requirement:" e "#### Scenario:"), sem campo de justificativa |

### Adaptações do projeto

Estes pontos são escolhas do projeto, sem fonte externa que os prescreva:

- Os requisitos do módulo são divididos por tipo de conteúdo em três arquivos e uma pasta. O IREB, o Wiegers e o Volere descrevem um documento único com seções.
- Nenhum documento de requisitos tem campo de origem ou de justificativa, nem a regra de negócio. O INCOSE (atributos A1 Rationale e A3 Trace to Source) e o Volere (Rationale e Originator) recomendam guardar a fonte e o porquê junto do requisito. Aqui o porquê fica na ADR e na descrição da MR, rastreável pelo Git, como nos modelos do Spec Kit e do OpenSpec.
- O item 6 da lista de cobertura, usuário com e sem permissão, vem do controle de acesso do SEI.
- O teste de entrada do requisito técnico parte das definições de restrição do IREB e do arc42 e acrescenta os critérios do projeto.
- O caso indesejado é citado por ID quando está em outro requisito, porque cada requisito tem um único "deve" e o caso indesejado pode ficar em outra seção.
- A lista de categorias do requisito técnico é do projeto. Ela junta características e subcaracterísticas da ISO/IEC 25010:2023 com os tipos de restrição do arc42, e os nomes em português são tradução do projeto. Integração e Rastreabilidade são subcaracterísticas na ISO e viraram categorias porque aparecem muito nos módulos do SEI.
- A pasta do módulo tem o nome da pasta do dicionário de dados e da pasta de ADR, e cada arquivo tem o nome do template que o gera.
- O ID traz o tipo do requisito e a sigla do módulo, o que o Volere desaconselha: "Do not include hybrid meanings (like the status, or the importance or whatever) in this number". O prefixo ajuda a leitura; por isso, requisito que muda de tipo ganha ID novo.
