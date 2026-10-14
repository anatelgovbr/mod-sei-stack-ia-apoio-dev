# Atualização e preservação de conhecimento

A atualização sincroniza o que o código demonstra sobre o uso do sistema e conserva o conhecimento que tem outra origem. O gestor pode ter acrescentado concepção, fundamento jurídico, transcrição de norma, experiência prática, casos de uso, orientação de portal ou texto argumentativo. Código não é autoridade sobre esse mérito. A classificação e a proteção do conhecimento valem para o manual e o adaptador, inclusive legados ou complementados por pessoas; o contrato do adaptador define sua revalidação, e o controle editorial abaixo aplica-se ao texto do manual.

## Delimitar antes de editar

Leia o manual inteiro, o pedido, o adaptador e as fontes relevantes antes de planejar substituições. Registre o estado anterior e identifique público, tarefas e alcance autorizado. Se o público já estiver claro no pedido ou no manual, aproveite essa informação; em dúvida material, entreviste antes de escrever. Preserve nome, destino, URLs, âncoras, imagens, codificação e quebras de linha existentes; conversão de formato, migração ou reorganização geral precisa de alcance explícito.

Classifique afirmações e trechos, não apenas capítulos. Um parágrafo, item ou célula pode misturar um label da tela com uma justificativa normativa ou dica. A mesma palavra aparecer no código e no manual não prova que ambos tratam da mesma afirmação.

| Trecho | Tratamento na atualização |
|---|---|
| Comportamento funcional ligado à interface e à regra ativa | Corrigir a diferença comprovada no alcance, com a cadeia de evidência e a comparação anterior/atual |
| Concepção, norma, contexto, dica, caso de uso ou procedimento externo | Preservar; eventual divergência vai ao relatório com sugestão, sem mudar mérito ou excluir antes de decisão específica |
| Origem ou ligação indeterminada | Preservar e nomear a incerteza; ausência na busca não transforma o trecho em conteúdo incorreto |
| Trecho misto | Corrigir a parte funcional demonstrada; correção meramente redacional necessária segue o controle editorial abaixo, conservando qualificações, fundamento, citações e conhecimento adjacente |

O pedido de atualizar autoriza, no alcance, sincronização funcional comprovada, reavaliação de capturas com avisos necessários e correções editoriais essenciais aprovadas pelo controle abaixo. Restrições explícitas, como conservar uma seção ou somente relatar ilustrações, prevalecem. Para mudar ou excluir mérito protegido, apresente trecho atual, sugestão, motivo e impacto e aguarde decisão explícita do responsável. Autorização já dada para aquela mudança específica vale; aprovação genérica da atualização não substitui essa decisão. Na verificação sem escrita, prepare/revalide primeiro o adaptador como pré-requisito e depois execute somente a análise do manual, sem editar manual ou imagens.

## Comprovar a diferença funcional

Parta do código para o manual: entidades, objetos e dados interessam quando têm representação ou efeito para a persona na tela, tarefa ou regra. Coluna de banco sem uso visível não exige seção no manual. Este fluxo altera documentação, não altera o sistema para fazê-lo concordar com o manual.

Use histórico ou revisões identificadas para comparar apresentação, chamadores, campos, ajuda, mensagens, regras e acesso. Registre versões, arquivos e linhas e o diff relevante fora do manual. Snapshot anterior fornecido pode ser usado como tal, sem inventar commit ou afirmar que a versão está implantada. O manual anterior também é fonte documental da comparação, não prova de implementação passada.

Uma divergência direta, como o label atual de um campo inequivocamente identificado, pode ser corrigida com a fonte corrente mesmo sem histórico. Declare o limite temporal. Para excluir referência a campo ou funcionalidade retirada, demonstre o vínculo anterior e sua remoção no fluxo ativo, ou obtenha confirmação específica. Busca sem resultado, fonte incompleta, configuração desconhecida ou ausência de consumidor visual exige preservar e relatar incerteza, sem converter falta de prova em prova de ausência.

Tela nova da persona pode gerar seção e aviso de captura; campo novo altera o ponto correspondente; campo removido retira somente sua referência funcional comprovada. Preserve a norma ou dica que usa o mesmo nome. Se uma tarefa inteira foi retirada, confira cada afirmação antes de remover sua seção: transfira ou preserve contexto legítimo somente com autorização para essa reorganização, ou proponha o ajuste no relatório.

## Aplicar somente a alteração necessária

Faça edições locais, sem regenerar o manual pelo esqueleto nem aplicar substituição global de um termo. O esqueleto é para criação. Ausência de mudança funcional não justifica reescrita, novo metadado de revisão ou ajuste geral de estilo. Ainda assim, a atualização inclui avisos de capturas necessárias e correções editoriais essenciais no alcance, conforme seus controles próprios; essas origens independem de diferença funcional. Necessidades de ilustração ou publicação fora do alcance ou com restrição expressa de escrita são reportadas.

Preserve conteúdo protegido também dentro da seção afetada. Alterar um label não autoriza trocar justificativa, obrigação, recomendação, prazo, número, responsável ou procedimento externo adjacente. Em material legado fora do perfil do verificador, mantenha a estrutura anterior e relate o limite; conformidade parcial não é licença para conversão silenciosa. Se não houver como executar a alteração de forma localizada com a ferramenta disponível, proponha o trecho e conserve o arquivo.

## Conferir a escrita sem mudar o mérito

Releia integralmente as **Regras de Escrita** do `../SKILL.md` antes de redigir e antes de concluir. Confira todo texto novo ou alterado: idioma de redação escolhido, clareza, frases completas e voz ativa, uma linha por parágrafo, estrutura útil, termos adequados ao público, siglas explicadas quando necessário e ausência de travessão nas explicações novas. Preserve os literais no idioma comprovado da interface.

A conferência verbal por sentença definida no [passo 4 do SKILL.md](../SKILL.md#4-redigir-ou-atualizar) vale também na revisão editorial autorizada, com sentido, condições e literais preservados.

Na atualização, uma correção editorial é essencial quando resolve um problema concreto de compreensão ou precisão para o público, ou um descumprimento das Regras de Escrita que prejudique a leitura; demonstre o problema e por que o ajuste é necessário. Preferência de estilo, troca por sinônimo e uniformização cosmética não bastam. Revisão editorial geral ou além desse limite exige alcance específico; "não solicitei revisão geral" não revoga por si só a correção essencial nativa, mas uma proibição expressa de edição editorial prevalece.

Preserve sentido, fatos, atores, números, prazos, condições, negações, grau de obrigação, exceções e conhecimento contextual, jurídico, empírico ou externo; uma recomendação não vira exigência. Mantenha a precisão dos termos jurídicos ou de negócio. Se simplificar exigir escolher uma interpretação, decidir mérito ou inventar responsável, apenas sugira e aguarde decisão.

Para cada lote de correções editoriais necessárias no manual, execute este controle antes de aplicar e depois de editar:

1. Analise duas vezes cada trecho proposto: primeiro identifique o problema concreto, a regra aplicável e a necessidade; depois confronte original e proposta para verificar equivalência e os elementos protegidos. Registre as duas análises por trecho.
2. Submeta original, proposta, público, alcance e justificativas a um subagente adversarial que não tenha redigido a proposta. Ele deve contestar necessidade e equivalência, inclusive citações e conhecimento protegido. Aplique somente os trechos aprovados, sem pedir decisão adicional para correção meramente redacional que cumpra esse controle.
3. Após editar, confira duas vezes o diff real: primeiro necessidade, localização e alcance de cada alteração; depois equivalência de sentido, citações, mérito, URLs, imagens e âncoras. Preserve os trechos restantes e registre as duas conferências.
4. Submeta original, arquivo resultante e diff ao subagente adversarial para a conferência final das mesmas condições. Corrija alterações inadvertidas e repita as conferências afetadas até obter aprovação; sem aprovação, conserve ou restaure o trecho original e reporte a pendência.

Sem subagente disponível ou sem prova de necessidade e equivalência, conserve o texto editorial e reporte o limite; execute somente a parte funcional ou de ilustração independente. Aprovação adversarial não substitui decisão do responsável sobre mérito. Em verificação sem escrita, recomende ajustes no relatório; nenhuma aprovação editorial autoriza aplicar mudanças nesse modo.

Preserve literalmente citações diretas de normas e de outras fontes, salvo revisão explicitamente solicitada dessas citações. Não corrija sua gramática por uma revisão geral de escrita. Textos de interface citados em atualização funcional passam a reproduzir a fonte corrente comprovada, inclusive sua redação original; explique em linguagem simples sem normalizar o literal da tela.

## Examinar o diff e concluir

Antes de salvar e após editar, confira cada inclusão, alteração e remoção contra a decisão do trecho. Use o diff do versionamento; se o arquivo anterior não estiver versionado, compare com a cópia preservada. Mantenha no relatório um registro conciso:

| Trecho e alteração | Tipo | Evidência ou autorização | Conferência de preservação |
|---|---|---|---|

As origens permitidas são diferença funcional ou de convenção comprovada, escolha explicitamente atualizada, ilustração incluída no alcance da atualização, correção editorial essencial com controle concluído, revisão editorial ou mérito especificamente autorizados e ajuste estrutural derivado da mudança, como o link de uma seção nova no Sumário. Para cada ajuste estrutural, identifique sua causa e preserve as demais entradas. No adaptador, registre também as fontes e escolhas preservadas, conforme seu contrato. Citação de fonte, classe interna e rastro de auditoria ficam fora do teor do manual humano.

Compare os trechos protegidos com o original. Fora dos trechos editoriais aprovados, confira os bytes; nos trechos revisados, examine também necessidade e equivalência de sentido, que um hash não demonstra, com os registros e pareceres do controle acima. Alteração sem origem suficiente deve ser desfeita antes de concluir. Na verificação, examine separadamente o diff da preparação prévia do adaptador e confirme que manual e imagens permanecem idênticos; reporte suas diferenças, propostas e limites sem aplicar mudanças nesses artefatos.

M04 exige a conferência de todas as regras de escrita aplicáveis e preservação dos literais. M08 exige diff justificado e conteúdo protegido intacto ou alterado somente conforme decisão específica. Se faltar confirmação para mérito externo, conserve esse trecho e conclua apenas a parte independente; reporte a pendência sem declarar conformidade integral.

## Base das escolhas

Pesquisa em 12 de outubro de 2026. [Microsoft: estilo e intenção](https://learn.microsoft.com/en-us/contribute/content/style-quick-start) orienta definir leitor e tarefa antes da criação ou atualização. [Divio: explicações](https://docs.divio.com/documentation-system/explanation/) reconhece concepção e contexto como documentação legítima além da referência técnica. [Google: hierarquia editorial](https://developers.google.com/style) prioriza convenções do projeto. A política de preservação e autorização acima traduz o alcance desta skill; não representa parecer sobre validade jurídica de conteúdo legado.
