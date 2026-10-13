# Processo de varredura funcional

O objeto de investigação é a tarefa humana. Entidades e objetos dão significado e relações ao fluxo; a interface mostra como a pessoa o encontra e opera; regras e permissões definem quando a operação é permitida e qual resultado produz. Estrutura de banco isolada e nomes de classes não bastam para escrever um procedimento.

## Inventário e alcance

Depois de conferir o adaptador, inventarie tarefas, pontos de entrada, telas, componentes compartilhados e condições de acesso no alcance acordado. Relacione cada item a pelo menos uma persona. Identifique telas de lista, pesquisa, detalhe, formulário, confirmação, modal, relatório, exportação e estados vazio, carregando, sucesso e falha, quando existirem. Registre explicitamente elementos fora do alcance e ausências comprovadas.

Leia o caminho efetivamente ativo para a versão, idioma e configuração escolhidos. Não publique código comentado, cópia antiga, componente sem chamador ou recurso desabilitado como funcionalidade disponível. Se uma biblioteca ou componente externo fornecer o comportamento relevante, rastreie sua chamada e sua versão; não conclua ausência porque sua pasta foi excluída da busca inicial.

## Cadeia de evidência

Para cada tarefa, percorra a cadeia nos dois sentidos, sem presumir nomes de camadas:

1. Localize a entrada usada pela pessoa, como menu, rota ou comando, e a condição de acesso.
2. Leia a tela ou componente, seu controlador e os eventos que enviam ou recebem dados. Conecte cada label ao identificador do campo e ao objeto, contrato ou projeção correspondente.
3. Siga o manipulador chamado até regras, validações, permissões e operações de leitura ou escrita. Leia a rotina relevante inteira, seus auxiliares e os consumidores do resultado.
4. Relacione entidades e objetos às suas funções de negócio, relações, estados e transições. Confirme se o campo é entrada, cálculo, identificação, filtro ou mera apresentação.
5. Volte à interface para conferir transformação, mensagem, resultado visível e caminhos de correção. Consulte testes e documentação para corroborar cenários, sem usar fixture como prova de configuração implantada.

Uma associação exige ligação demonstrada, como rota chamada, binding de campo, chave de tradução usada, parâmetro enviado ou consumidor do retorno. Mesmo nome ou texto parecido em outra tela não comprova vínculo. Registre `arquivo:linha` em cada salto; identifique a revisão para que números de linha não pareçam estáveis após mudanças.

## Tudo o que aparece para a pessoa

| Grupo | O que mapear e conferir |
|---|---|
| Acesso e navegação | Menus, títulos, abas, breadcrumbs, links, atalhos, ícones e nomes acessíveis; entrada disponível por persona |
| Campos e opções | Label literal, ajuda, placeholder, tipo funcional, formato, unidade, tamanho, obrigatoriedade, padrão, valores permitidos e preenchimento condicional |
| Ações e decisões | Botões, opções de seleção, confirmações, pré-condições, autorização real, efeitos, cancelamento e reversibilidade |
| Críticas e mensagens | Validação no cliente e no servidor, erro de negócio, aviso, sucesso, condição disparadora e ação comprovada de correção |
| Resultados e estados | Listas, filtros, ordenação, paginação, situação do objeto, transições, processamento assíncrono, downloads, relatórios e estados sem dados |
| Conteúdo dinâmico | Traduções, plurais, interpolação, conteúdo configurado em banco ou serviço, flags, permissões e variações por dispositivo ou implantação |

Para cada texto, registre a forma literal, o local de exibição e a condição em que aparece. Um asterisco ou atributo `required` não resolve sozinho a regra de preenchimento; compare com a validação efetiva. Uma mensagem deve estar ligada à condição que a dispara antes de orientar a solução.

Resolva chaves de tradução no idioma e contexto declarados. Se o texto vier de template ou interpolação, preserve a parte fixa e explique a variável sem fabricar um valor real. Se vier de configuração, banco, serviço ou ambiente inacessível, declare a lacuna e peça somente a fonte que possa resolvê-la. Não invente rótulos, valores de domínio nem o texto de uma crítica a partir do identificador técnico.

O conjunto visível precisa aparecer na matriz. No manual, apresente cada elemento no lugar útil da tarefa, em tabela de campos, orientação de navegação ou solução de problemas, sem transcrever o código inteiro. Um elemento secundário pode ser agrupado com motivo registrado; uma mensagem que impeça concluir a tarefa exige explicação própria.

## Autoridade por afirmação

| Afirmação | Fonte necessária |
|---|---|
| Nome visível e localização | Implementação de apresentação com chamada comprovada, tradução resolvida ou observação da variante correta |
| Significado, condição e efeito | Regra efetivamente chamada, produtor do dado e consumidor; documentação funcional e entrevista corroboram o propósito |
| Quem pode operar | Controle de autorização e configuração aplicável; ocultação de interface é conferência adicional |
| Valor dinâmico e configuração corrente | Fonte configurada ou observação autorizada correspondente à versão, persona e idioma |
| Sequência e resultado observado | Navegação autorizada ou teste aplicável, distinguindo expectativa do código de observação no sistema |

Um fato funcional diretamente sustentado por fonte adequada pode ser documentado. Inferência ainda provável exige ampliar a busca; se não houver prova, mantenha lacuna. Respostas de entrevista definem público, objetivos e escolhas do manual, mas uma regra atribuída ao software precisa ser confrontada com o código ou a configuração correspondente. Conteúdo de concepção, norma, experiência ou fonte externa tem domínio próprio; não deve ser invalidado por ausência na codebase. Em manual existente, siga [atualização e preservação](atualizacao-preservacao.md), inclusive para afirmações misturadas no mesmo trecho.

Quando fontes divergirem, relate as leituras, os caminhos, a variante e o efeito no procedimento. Na criação, suspenda a inclusão dependente da divergência até confirmação adequada. Na atualização, corrija somente a diferença funcional demonstrada no alcance; preserve mérito externo e afirmação indeterminada enquanto reporta a proposta ou incerteza. Remover uma referência exige prova de retirada ou decisão específica, e não apenas busca vazia. A investigação mais ampla não amplia por si só a autorização de edição.

## Matriz técnica e término

Use uma linha por elemento ou regra rastreável; agrupe somente elementos equivalentes que mantenham os respectivos vínculos.

| Tarefa e persona | Entidade ou objeto | Tela e elemento visível | Regra, permissão ou condição | Evidências da cadeia | Seção do manual | Estado e pendência |
|---|---|---|---|---|---|---|

Identifique a origem de cada evidência: código examinado, documentação corroborada, declaração da entrevista ou observação no ambiente. Para observação, registre versão ou revisão, idioma, perfil, configuração relevante e captura ou teste, sem dados sensíveis. Diferencie comprovado no código, observado no ambiente, não aplicável e não determinado.

### Plano de capturas derivado da varredura

Depois de mapear o alcance completo, transforme os vínculos da matriz em posições de ilustração. Considere cada tela funcional distinta e cada estado visual relevante; escolha o print que ajude a persona a localizar elementos, preencher campos, decidir ou reconhecer um resultado. Uma logo não ilustra o uso de uma funcionalidade. Quando uma captura não acrescentar informação útil, justifique a dispensa. Não distribua avisos mecanicamente por título, campo ou mensagem.

| Seção e ponto de inserção | Vínculo com a matriz e finalidade didática | Tela, estado, persona e pré-condições | Caminho visível e evidência | Captura e situação |
|---|---|---|---|---|

Escolha um ponto junto à explicação da tela, depois do contexto ou do passo que a abre e antes de mudar de assunto. Informe quais campos, ajudas, controles ou resultados devem ficar visíveis no recorte. Um print do formulário pode ilustrar campos e ajuda de subtópicos próximos; registre os trechos atendidos e use uma referência clara à seção correspondente quando necessário. Modal, confirmação ou outro estado distinto pede print próprio somente quando ajudar a compreensão e tiver vínculo de apresentação comprovado. Não planeje uma tela de erro a partir de uma mensagem retornada pelo servidor sem rastrear seu consumidor na interface.

Construa o caminho de acesso com os labels literais comprovados de menus, abas e ações, na ordem efetiva, como `Menu > Submenu > Aba > Ação`. A sequência é exemplo de formato, não hierarquia obrigatória. Um menu direto pode ser o caminho completo. Não crie um menu pai pelo nome da entidade nem apresente uma URL, endpoint ou arquivo-fonte como navegação humana. Se o acesso for realmente por endereço direto, documente essa modalidade somente com evidência, sem parâmetros sensíveis. Indique a persona quando ela alterar acesso ou conteúdo.

Rastreie cada parte do caminho até a apresentação ativa, condição de acesso e destino correspondente. Materiais ou entrevista podem complementar navegação não recuperável do código, com origem e confirmação identificadas. Se continuar indeterminada, indique `Navegação não confirmada; tela: <nome comprovado da tela>` no lugar do caminho, descreva no relatório o trecho faltante e mantenha M03 pendente. Não entregue o campo de caminho vazio, um placeholder de template ou uma sequência provável como comprovada.

Classifique cada posição como captura disponível e conferida, captura pendente ou dispensa justificada. Na criação ou atualização dentro do alcance, uma posição pendente recebe o aviso definido em [formato-manual.md](formato-manual.md). A captura será obtida manualmente pelo usuário ou desenvolvedor; o plano orienta a coleta, sem criar imagens ou operar a aplicação. Na verificação sem escrita, confronte plano e manual e reporte seção, ponto, caminho e aviso sugerido para ausências ou incoerências, sem inserir ou corrigir arquivos. Na atualização, relate necessidades fora do alcance sem alterar as seções preservadas.

Encerre a rodada quando inventário, matriz e plano de capturas estiverem conciliados: cada tarefa, objeto e elemento visível no alcance tem destino documentado, agrupamento justificado ou lacuna nomeada, e cada posição de ilustração necessária tem imagem conferida ou aviso de pendência. Informe quantidades e pendências por fluxo; nenhum percentual de cobertura dispensa a conferência de um passo crítico ou comprova legibilidade. Mantenha a matriz, o plano e o rastro técnicos fora do texto humano do manual; os avisos ficam nas posições previstas nele.
