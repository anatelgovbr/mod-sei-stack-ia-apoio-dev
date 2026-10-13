# Atualização e preservação de conhecimento

A atualização sincroniza o que o código demonstra sobre o uso do sistema e conserva o conhecimento que tem outra origem. O gestor pode ter acrescentado concepção, fundamento jurídico, transcrição de norma, experiência prática, casos de uso, orientação de portal ou texto argumentativo. Código não é autoridade sobre esse mérito. Esta regra vale para qualquer manual existente, inclusive legado e manual criado pela própria skill e depois complementado por pessoas.

## Delimitar antes de editar

Leia o manual inteiro, o pedido, o adaptador e as fontes relevantes antes de planejar substituições. Registre o estado anterior e identifique público, tarefas e alcance autorizado. Se o público já estiver claro no pedido ou no manual, aproveite essa informação; em dúvida material, entreviste antes de escrever. Preserve nome, destino, âncoras, imagens, codificação e quebras de linha existentes; conversão de formato, migração ou reorganização geral precisa de alcance explícito.

Classifique afirmações e trechos, não apenas capítulos. Um parágrafo, item ou célula pode misturar um label da tela com uma justificativa normativa ou dica. A mesma palavra aparecer no código e no manual não prova que ambos tratam da mesma afirmação.

| Trecho | Tratamento na atualização |
|---|---|
| Comportamento funcional ligado à interface e à regra ativa | Corrigir a diferença comprovada no alcance, com a cadeia de evidência e a comparação anterior/atual |
| Concepção, norma, contexto, dica, caso de uso ou procedimento externo | Preservar; eventual divergência vai ao relatório com sugestão, sem mudar mérito ou excluir antes de decisão específica |
| Origem ou ligação indeterminada | Preservar e nomear a incerteza; ausência na busca não transforma o trecho em conteúdo incorreto |
| Trecho misto | Alterar somente a parte funcional demonstrada; conservar qualificações, fundamento, citações e conhecimento adjacente |

O pedido de atualizar autoriza a sincronização funcional comprovada no alcance; não autoriza corrigir todo o mérito do manual. Para mudar conteúdo protegido, apresente trecho atual, sugestão, motivo e impacto e aguarde decisão explícita do responsável. Autorização já dada para aquela mudança específica vale; aprovação genérica da atualização não substitui essa decisão.

## Comprovar a diferença funcional

Parta do código para o manual: entidades, objetos e dados interessam quando têm representação ou efeito para a persona na tela, tarefa ou regra. Coluna de banco sem uso visível não exige seção no manual. Este fluxo altera documentação, não altera o sistema para fazê-lo concordar com o manual.

Use histórico ou revisões identificadas para comparar apresentação, chamadores, campos, ajuda, mensagens, regras e acesso. Registre versões, arquivos e linhas e o diff relevante fora do manual. Snapshot anterior fornecido pode ser usado como tal, sem inventar commit ou afirmar que a versão está implantada. O manual anterior também é fonte documental da comparação, não prova de implementação passada.

Uma divergência direta, como o label atual de um campo inequivocamente identificado, pode ser corrigida com a fonte corrente mesmo sem histórico. Declare o limite temporal. Para excluir referência a campo ou funcionalidade retirada, demonstre o vínculo anterior e sua remoção no fluxo ativo, ou obtenha confirmação específica. Busca sem resultado, fonte incompleta, configuração desconhecida ou ausência de consumidor visual exige preservar e relatar incerteza, sem converter falta de prova em prova de ausência.

Tela nova da persona pode gerar seção e aviso de captura; campo novo altera o ponto correspondente; campo removido retira somente sua referência funcional comprovada. Preserve a norma ou dica que usa o mesmo nome. Se uma tarefa inteira foi retirada, confira cada afirmação antes de remover sua seção: transfira ou preserve contexto legítimo somente com autorização para essa reorganização, ou proponha o ajuste no relatório.

## Aplicar somente a alteração necessária

Faça edições locais, sem regenerar o manual pelo esqueleto nem aplicar substituição global de um termo. O esqueleto é para criação. Ausência de mudança funcional não justifica reescrita, novo metadado de revisão, ajuste geral de estilo ou inclusão de avisos em trechos não autorizados. Necessidades de ilustração ou publicação fora do alcance são reportadas.

Preserve conteúdo protegido também dentro da seção afetada. Alterar um label não autoriza trocar justificativa, obrigação, recomendação, prazo, número, responsável ou procedimento externo adjacente. Em material legado fora do perfil do verificador, mantenha a estrutura anterior e relate o limite; conformidade parcial não é licença para conversão silenciosa. Se não houver como executar a alteração de forma localizada com a ferramenta disponível, proponha o trecho e conserve o arquivo.

## Conferir a escrita sem mudar o mérito

Releia integralmente as **Regras de Escrita** do `../SKILL.md` antes de redigir e antes de concluir. Confira todo texto novo ou alterado: português brasileiro, clareza, frases completas e voz ativa, uma linha por parágrafo, estrutura útil, termos adequados ao público, siglas explicadas quando necessário e ausência de travessão nas explicações novas.

A conferência verbal por sentença definida no [passo 4 do SKILL.md](../SKILL.md#4-redigir-ou-atualizar) vale também na revisão editorial autorizada, com sentido, condições e literais preservados.

Revisão editorial de conteúdo prévio protegido exige pedido ou autorização para esse alcance. Preserve sentido, fatos, atores, números, prazos, condições, negações, grau de obrigação e exceções; uma recomendação não vira exigência. Mantenha a voz do autor compatível com a finalidade e a precisão dos termos jurídicos ou de negócio. Se simplificar exigir decidir mérito, apenas sugira e aguarde decisão.

Preserve literalmente citações diretas de normas e de outras fontes, salvo revisão explicitamente solicitada dessas citações. Não corrija sua gramática por uma revisão geral de escrita. Textos de interface citados em atualização funcional passam a reproduzir a fonte corrente comprovada, inclusive sua redação original; explique em linguagem simples sem normalizar o literal da tela.

## Examinar o diff e concluir

Antes de salvar e após editar, confira cada inclusão, alteração e remoção contra a decisão do trecho. Use o diff do versionamento; se o arquivo anterior não estiver versionado, compare com a cópia preservada. Mantenha no relatório um registro conciso:

| Trecho e alteração | Tipo | Evidência ou autorização | Conferência de preservação |
|---|---|---|---|

As origens permitidas são diferença funcional comprovada, revisão editorial ou mérito especificamente autorizados e ajuste estrutural derivado da mudança, como o link de uma seção nova no Sumário. Para cada ajuste estrutural, identifique sua causa e preserve as demais entradas. Citação de fonte, classe interna e rastro de auditoria ficam fora do teor do manual humano.

Compare os trechos protegidos com o original. Sem revisão autorizada, confira os bytes; com revisão editorial, examine também a equivalência de sentido, que um hash não demonstra. Alteração sem origem suficiente deve ser desfeita antes de concluir. Em verificação sem escrita, execute a classificação e reporte diferenças, propostas e limites sem aplicar nenhuma mudança, inclusive no adaptador e no registro.

M04 exige a conferência de todas as regras de escrita aplicáveis e preservação dos literais. M08 exige diff justificado e conteúdo protegido intacto ou alterado somente conforme decisão específica. Se faltar confirmação para mérito externo, conserve esse trecho e conclua apenas a parte independente; reporte a pendência sem declarar conformidade integral.

## Base das escolhas

Pesquisa em 12 de outubro de 2026. [Microsoft: estilo e intenção](https://learn.microsoft.com/en-us/contribute/content/style-quick-start) orienta definir leitor e tarefa antes da criação ou atualização. [Divio: explicações](https://docs.divio.com/documentation-system/explanation/) reconhece concepção e contexto como documentação legítima além da referência técnica. [Google: hierarquia editorial](https://developers.google.com/style) prioriza convenções do projeto. A política de preservação e autorização acima traduz o alcance desta skill; não representa parecer sobre validade jurídica de conteúdo legado.
