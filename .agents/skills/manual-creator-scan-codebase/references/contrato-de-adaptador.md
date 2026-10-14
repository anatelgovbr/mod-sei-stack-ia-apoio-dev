# Contrato de adaptador

O adaptador traduz as convenções comprovadas do repositório para a investigação do manual. Ele localiza evidências; não cria regras de negócio nem substitui a entrevista. Os caminhos que declara são relativos à raiz do repositório de uso, salvo insumos locais expressamente indicados.

## Entrevista e seleção

Identifique o caso de uso pela tabela do `../SKILL.md`. Extraia respostas já fornecidas, abra o adaptador e os materiais existentes e investigue pistas antes de perguntar somente o que continuar materialmente indeterminado:

- Preparar somente o adaptador: sistema ou módulo, versão ou revisão, logo, idioma da interface, idioma de redação dos futuros manuais, contexto do sistema e de quem o usa e materiais focalizados nas convenções e no contexto. Investigue personas e tarefas como características do sistema, sem exigir escolha de cada futuro manual.
- Criar manual: público-alvo e seus objetivos, materiais complementares e intenção ou alcance ainda indeterminados. Recupere versão, logo, idiomas, contexto e convenções do adaptador; prepare-o quando faltar.
- Atualizar manual: arquivo existente, público-alvo, materiais complementares e intenção ou alcance ainda indeterminados. Aproveite público e tarefas já claros no manual e revalide as escolhas e convenções do adaptador.
- Verificar sem escrita: arquivo, alvo e alcance da comparação; aproveite público e materiais existentes e pergunte apenas por dúvida que altere a análise. Prepare ou atualize primeiro o adaptador necessário, sem alterar manual e imagens; depois faça somente a análise do manual.

Materiais podem ser arquivos locais, anexos ou links da Internet, tratados pela política de investigação do `../SKILL.md`. Nomeie sua finalidade: convenções e contexto do adaptador, conteúdo do manual, captura ou evidência complementar. Ambiente autorizado e fontes dinâmicas são perguntas somente quando necessários para resolver lacuna concreta; a coleta de prints permanece manual.

O idioma da interface determina os literais e a resolução das traduções do sistema. O idioma de redação determina as explicações dos manuais; não deduza um do outro. Preserve a escolha explícita atual ou já registrada; sem informação anterior suficiente, pergunte pelo idioma de redação. Registre ambos nos grupos existentes e recupere-os na criação ou atualização posterior. Outra língua de redação prevalece sobre o padrão de português brasileiro, preservando os demais critérios de clareza e os literais e citações.

Compare nome, caminhos e componentes do alvo com o reconhecimento dos adaptadores em `../registro-adaptadores.md`. Um candidato único e comprovado pode ser selecionado; candidatos concorrentes exigem inspeção discriminante e, se necessário, escolha do responsável. Sem candidato, crie o adaptador por entrevista e scan de descoberta antes de criar, atualizar ou verificar o manual. Se uma restrição explícita proibir qualquer escrita, inclusive no adaptador e no registro, e impedir satisfazer esse pré-requisito, reporte o impedimento sem avançar à verificação do manual.

Inspecione a cadeia de uma tarefa representativa de cada convenção distinta relevante, incluindo apresentação e regra chamada, para provar que os pontos de leitura são adequados. Confira profundamente como rastrear caminhos visíveis, telas, textos, labels, campos, ajudas, críticas, mensagens, regras, navegação, estados e personas. A descoberta demonstra os métodos e suas variantes; a varredura completa das tarefas do manual vem depois do adaptador. Use `rg --files` para localizar candidatos e `rg -n` para referências quando disponíveis; confirme o conteúdo com a codificação encontrada. Não trate falta de resultado em UTF-8 como ausência de texto em código de outra codificação.

## Grupos obrigatórios

Preencha cada grupo com evidência identificada ou resposta da entrevista; para leitor/renderizador, aplique a política interna abaixo. Declare `não aplicável` com motivo quando a capacidade não existir. Um item desconhecido que afete escopo, permissões, interpretação de tela ou publicação é pendência, salvo leitor/renderizador sem indicação, resolvido pela referência básica. Na preparação exclusiva, definir destinatários, slug e alcance de cada futuro manual é etapa posterior, não falta do contrato: registre as convenções de publicação e identificação, sem inventar esses arquivos.

| Grupo | Conteúdo obrigatório |
|---|---|
| Reconhecimento e alcance | Nome oficial, pistas de inclusão e exclusão, sistema ou módulo, fronteiras e componentes compartilhados |
| Versão e variante | Fontes de versão ou revisão, configuração e recursos habilitados, idioma da interface e como conferir a correspondência com o material fornecido |
| Leitura da codebase | Raízes, extensões, codificação por fonte, exclusões comprovadas e ferramentas disponíveis; não excluir dependência que forneça comportamento no alcance sem rastrear sua contribuição |
| Pontes de evidência | Como conectar entidades ou objetos, contratos, rotas, menus, componentes, campos, serviços, regras, permissões e testes; identificadores e estratégias concretas de busca; como comprovar o caminho visível de acesso à tela sem confundi-lo com rota ou arquivo técnico |
| Interface e textos | Onde localizar labels, botões, opções, críticas, mensagens, ajudas, ícones acessíveis, traduções, interpolação, textos vindos de banco ou serviço e estados condicionais; como rastrear menus, abas, ações, modais e variantes por persona para orientar os prints |
| Personas e acesso | Objetivos, tarefas, familiaridade relevante, termos de negócio, papéis ou perfis de acesso relacionados e fonte da relação; incertezas que exijam entrevista |
| Publicação e recursos | Idioma de redação dos manuais e fonte da escolha; pastas e convenções de identificação dos manuais e imagens, com slug concreto quando houver manual selecionado; manual anterior, logo e outras imagens aprovadas, fonte e tratamento de dados sensíveis; renderizador, apresentação do aviso Markdown, comportamento de âncoras, padrão de geração das capturas e coleta manual pelo responsável |
| Validação e limites | Checks locais, observação de interface disponível e autorizada, caminhos para evidência complementar, lacunas e condições de bloqueio; data ou revisão da última conferência |

O adaptador declara a pasta de publicação e a pasta de imagens dos manuais. Ao criá-lo, registre o destino padrão de [formato-manual.md](formato-manual.md), salvo outra escolha do responsável; mudança de destino se faz no adaptador, não na skill. Se não existir versão de produto, identifique a revisão examinada e as alterações locais incluídas, em vez de fabricar uma versão. Código-fonte disponível não prova qual versão está implantada.

Na amostra de descoberta, demonstre como localizar a tela e comprovar seu caminho pelos nomes visíveis, com persona e condição de acesso. Se houver somente rota técnica ou trecho de navegação indeterminado, registre esse limite. O adaptador define o método e remete ao aviso de [formato-manual.md](formato-manual.md); o plano de posições para todas as capturas só nasce na varredura funcional posterior. Preparar somente o adaptador não autoriza escrever o manual nem inserir avisos nele.

## Leitor e renderizador

Adote GitLab e GitHub como referências básicas internas para o Markdown de manuais criados ou atualizados, usando a sintaxe comum de arquivos `.md` em repositórios. Esse padrão dispensa informar, escolher ou confirmar leitor/renderizador na entrevista; a falta dessa indicação satisfaz essa parte do grupo Publicação e recursos e não bloqueia o adaptador nem a escrita. Não anuncie o padrão na conversa nem acrescente metadados sobre ele ao manual, pois essa decisão interna não exige participação do usuário.

Uma indicação específica no pedido ou prompt prevalece sobre a referência básica e sobre uma indicação anterior do adaptador. Sem nova indicação, preserve o leitor específico já comprovado no adaptador ou nos materiais do alvo. Na ausência de ambos, aplique a referência básica automaticamente. Registre a referência interna ou a indicação específica no grupo Publicação e recursos, sem novos campos obrigatórios, na preparação prévia do adaptador, inclusive antes de verificar um manual. O manual e suas imagens permanecem intocados na verificação.

Confira formato e âncoras conforme [formato-manual.md](formato-manual.md#título-sumário-e-seções). Referência de compatibilidade não comprova leitura visual: registre no relatório o ambiente realmente observado e os limites da verificação. Isso permite informar pendências concretas sem transformar o padrão interno em pergunta ou confirmação ao usuário.

## Personas e permissões

Persona representa um grupo de pessoas com objetivos e necessidades de leitura. Papel ou perfil representa uma condição de acesso implementada. Registre a relação entre ambos, sem equipará-los: uma persona pode ter mais de um perfil, e um perfil pode atender várias personas.

| Persona ou público | Objetivo e tarefas | Conhecimento relevante | Perfil e restrições | Fonte e confirmação |
|---|---|---|---|---|

Use grupos de público conhecidos no sistema ou informados pelo responsável. A inferência de um nome de perfil é pista para a entrevista, não persona confirmada. Não invente idade, profissão, experiência ou permissão. Um público único é suficiente quando comprovado; mantenha a tabela mesmo nesse caso. Regras de autorização vêm da implementação e da configuração efetiva, e não apenas de um botão oculto.

## Criação e composição

Crie `adapters/<slug_do_alvo>.md` dentro da skill instalada. Use slug com letras minúsculas sem acento, números e hífens, sem separadores de caminho. Preencha o esqueleto abaixo com conteúdo concreto antes de registrar o alvo.

```markdown
# Adaptador: <nome oficial do alvo>

## Reconhecimento e alcance

## Versão e variante

## Leitura da codebase

## Pontes de evidência

## Interface e textos

## Personas e acesso

## Publicação e recursos

## Validação e limites
```

Somente extraia uma base compartilhada quando duas adaptações reais demonstrarem as mesmas convenções. O adaptador declara o caminho da base e cada exceção; grupos não preenchidos nem herdados explicitamente continuam faltantes. Não crie antecipadamente famílias de frameworks e não copie para um alvo adaptadores feitos para outra codebase.

Registre o nome, o link para o arquivo e as pistas de reconhecimento e alcance na tabela de `../registro-adaptadores.md` apenas após completar o contrato. O comportamento de entrevista, varredura, formato e verificação permanece nas referências gerais.

O adaptador registra convenções do alvo e escolhas vigentes, não o estado de uma execução. Registre no relatório o que a rodada criou, verificou ou deixou pendente; não copie para o adaptador frases como "esta etapa não cria manual" ou o limite de escrita do caso acionado. Ao reutilizá-lo em outro caso de uso, confira a coerência das escolhas atuais e identifique explicitamente qualquer informação histórica por data ou revisão, preservando conhecimento protegido. Uma escolha posterior de público ou publicação não pode coexistir com afirmação corrente de que essa escolha ainda está indeterminada.

## Revalidação e atualização

A cada execução, abra o adaptador e confira reconhecimento, alcance, fontes correntes de versão ou revisão, caminhos, codificações, pontos de leitura da interface, traduções e perfis contra a parte da codebase afeta ao alvo. Registre a conferência e os resultados no relatório. Atualidade depende das convenções e fontes comprovadas, não somente da data ou versão histórica anotada. Se houver divergência, ajuste o adaptador antes de criar, atualizar ou verificar o manual; na verificação, esses ajustes pertencem à fase prévia, sem escrita no manual e nas imagens. Sem adaptador completo e atual, a execução do manual fica bloqueada.

Classifique cada afirmação afetada do adaptador: convenção técnica ou funcional comprovada, escolha de entrevista, conhecimento contextual, jurídico, empírico ou externo e origem indeterminada. Corrija somente diferenças comprovadas de convenção ou funcionamento e escolhas expressamente atualizadas; preserve conhecimento de outras fontes e incertezas, inclusive dentro de um trecho misto. Ausência no código não autoriza excluir esse conhecimento. Mudança ou exclusão de mérito exige proposta e decisão específica. Registre o antes/depois, a origem de cada ajuste e a preservação do restante no relatório; use a classificação de [atualização e preservação](atualizacao-preservacao.md). A autorização editorial necessária do manual não se estende automaticamente ao adaptador.

Uma mudança funcional com as mesmas convenções não exige reconstruir o adaptador: confirme sua validade e siga a cadeia afetada, inclusive chamadores, textos, permissões, configurações e testes. Se a diferença não puder ser delimitada pelo histórico, compare todo o alcance do manual com as fontes atuais e reporte esse alcance maior de conferência. Isso não autoriza reescrever conteúdo ainda correto.
