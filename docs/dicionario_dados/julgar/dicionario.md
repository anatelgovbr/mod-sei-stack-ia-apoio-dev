# Dicionário de Dados do Módulo SEI Julgar - v3.0.3

## Índice de Tabelas

- [algoritmo](#algoritmo)
- [andamento_sessao](#andamento_sessao)
- [atributo_andamento_sessao](#atributo_andamento_sessao)
- [ausencia_sessao](#ausencia_sessao)
- [autuacao](#autuacao)
- [bloqueio_item_sess_unidade](#bloqueio_item_sess_unidade)
- [colegiado](#colegiado)
- [colegiado_composicao](#colegiado_composicao)
- [colegiado_versao](#colegiado_versao)
- [destaque](#destaque)
- [distribuicao](#distribuicao)
- [eleicao](#eleicao)
- [impedimento](#impedimento)
- [item_sessao_documento](#item_sessao_documento)
- [item_sessao_julgamento](#item_sessao_julgamento)
- [julgamento_parte](#julgamento_parte)
- [motivo_ausencia](#motivo_ausencia)
- [motivo_canc_distribuicao](#motivo_canc_distribuicao)
- [motivo_distribuicao](#motivo_distribuicao)
- [motivo_mesa](#motivo_mesa)
- [opcao_eleicao](#opcao_eleicao)
- [parte_procedimento](#parte_procedimento)
- [pedido_vista](#pedido_vista)
- [presenca_sessao](#presenca_sessao)
- [provimento](#provimento)
- [qualificacao_parte](#qualificacao_parte)
- [rel_autuacao_tipo_materia](#rel_autuacao_tipo_materia)
- [rel_colegiado_usuario](#rel_colegiado_usuario)
- [rel_destaque_usuario](#rel_destaque_usuario)
- [rel_motivo_distr_colegiado](#rel_motivo_distr_colegiado)
- [revisao_item](#revisao_item)
- [seq_algoritmo](#seq_algoritmo)
- [seq_andamento_sessao](#seq_andamento_sessao)
- [seq_atributo_andamento_sessao](#seq_atributo_andamento_sessao)
- [seq_ausencia_sessao](#seq_ausencia_sessao)
- [seq_autuacao](#seq_autuacao)
- [seq_bloqueio_item_sess_unidade](#seq_bloqueio_item_sess_unidade)
- [seq_colegiado](#seq_colegiado)
- [seq_colegiado_composicao](#seq_colegiado_composicao)
- [seq_colegiado_versao](#seq_colegiado_versao)
- [seq_destaque](#seq_destaque)
- [seq_distribuicao](#seq_distribuicao)
- [seq_eleicao](#seq_eleicao)
- [seq_impedimento](#seq_impedimento)
- [seq_item_sessao_documento](#seq_item_sessao_documento)
- [seq_item_sessao_julgamento](#seq_item_sessao_julgamento)
- [seq_julgamento_item](#seq_julgamento_item)
- [seq_julgamento_parte](#seq_julgamento_parte)
- [seq_motivo_ausencia](#seq_motivo_ausencia)
- [seq_motivo_canc_distribuicao](#seq_motivo_canc_distribuicao)
- [seq_motivo_distribuicao](#seq_motivo_distribuicao)
- [seq_motivo_mesa](#seq_motivo_mesa)
- [seq_opcao_eleicao](#seq_opcao_eleicao)
- [seq_parte_procedimento](#seq_parte_procedimento)
- [seq_pedido_vista](#seq_pedido_vista)
- [seq_presenca_sessao](#seq_presenca_sessao)
- [seq_provimento](#seq_provimento)
- [seq_qualificacao_parte](#seq_qualificacao_parte)
- [seq_revisao_item](#seq_revisao_item)
- [seq_sessao_bloco](#seq_sessao_bloco)
- [seq_sessao_julgamento](#seq_sessao_julgamento)
- [seq_sustentacao_oral](#seq_sustentacao_oral)
- [seq_tarefa_sessao](#seq_tarefa_sessao)
- [seq_tipo_materia](#seq_tipo_materia)
- [seq_tipo_sessao](#seq_tipo_sessao)
- [seq_tipo_sessao_bloco](#seq_tipo_sessao_bloco)
- [seq_voto_eleicao](#seq_voto_eleicao)
- [seq_voto_opcao_eleicao](#seq_voto_opcao_eleicao)
- [seq_voto_parte](#seq_voto_parte)
- [sessao_bloco](#sessao_bloco)
- [sessao_julgamento](#sessao_julgamento)
- [sustentacao_oral](#sustentacao_oral)
- [tarefa_sessao](#tarefa_sessao)
- [tipo_materia](#tipo_materia)
- [tipo_membro_colegiado](#tipo_membro_colegiado)
- [tipo_sessao](#tipo_sessao)
- [tipo_sessao_bloco](#tipo_sessao_bloco)
- [voto_eleicao](#voto_eleicao)
- [voto_opcao_eleicao](#voto_opcao_eleicao)
- [voto_parte](#voto_parte)

## algoritmo

Armazena os registros de utilização de algoritmo na distribuição de processos. Caso o algoritmo de distribuição escolhido para o colegiado seja Por peso atribuído ao membro, essa tabela não será alimentada.

| Coluna | Descrição |
|---|---|
| id_algoritmo | Número que identifica o registro de algoritmo utilizado |
| contador | Status multi-valorado que identifica se o membro do colegiado recebeu ou não processo na última rodada de distribuição:<br><br><ul><li>0 = não recebeu distribuição na última rodada</li><li>1 = já recebeu distribuição na última rodada</li></ul><br>Não se aplica à distribuição por peso |
| id_colegiado | Número que identifica os registros de colegiados cadastrados |
| id_origem | Número que varia de acordo com o tipo de algoritmo utilizado pelo colegiado:<br><br><ul><li>Algoritmo Peso = não alimenta esse campo</li><li>Algoritmo Rodada de distribuição = não alimenta esse campo</li><li>Algoritmo Rodada por Tipo de Matéria = id_tipo_materia</li><li>Algoritmo Rodada por Tipo de Processo = id_tipo_procedimento</li></ul> |
| id_usuario | Número que identificao o membro do colegiado |
| sta_algoritmo | Status multi-valorado que identifica o Tipo de Algoritmo de distribuição de processos utilizada por cada Colegiado:<br><br><ul><li>R = Algoritmo de distribuição por rodadas</li><li>T = Algoritmo de distribuição por rodadas por tipo de processo</li><li>M = Algoritmo de distribuição por rodadas por tipo de matéria</li><li>P = Algoritmo de distribuição por peso atribuído ao membro</li></ul> |

## andamento_sessao

Armazena os registros das atividades que são gerados pelo módulo SEI JULGAR no andamento de cada processo

| Coluna | Descrição |
|---|---|
| id_andamento_sessao | Número que identifica o registro no andamento (atividade) gerado no processo |
| dth_execucao | Data e Hora de execução do registro que gerou o andamento do processo |
| id_sessao_julgamento | Número que identifica o registro de sessão de julgamento |
| id_tarefa_sessao | Número que identifica qual foi o tipo de tarefa gerada pela atividade (pautado, retirado de pauta, etc) |
| id_unidade | Número que identifica a unidade do usuário que executou o registro que gerou a tarefa no andamento do processo |
| id_usuario | Número que identifica o usuário que executou o registro que gerou a tarefa no andamento do processo |

## atributo_andamento_sessao

Armazena informações complementares à tabela andamento_sessao. Associativa entre os ids gerados pela tabela andamento_sessao e a descrição de cada item que consta na tabela atributo_andamento_sessao

| Coluna | Descrição |
|---|---|
| id_atributo_andamento_sessao | Número que identifica o registro do atributo do andamento (atividade) gerado no processo |
| chave | Chave que associa a tabela atributo_andamento_sessao com a tabela tarefa_sessao para viabilizar a captura da informação do complemento (atributo) da tarefa |
| id_andamento_sessao | Número que identifica o registro no andamento (atividade) gerado no processo |
| id_origem | Campo que permite filtrar a informação que complementa o atributo |
| valor | Descrição do complemento (atributo) |

## ausencia_sessao

Armazena os registros de ausência em sessões de julgamento

| Coluna | Descrição |
|---|---|
| id_ausencia_sessao | Número que identifica o registro de ausências em sessão de julgamento |
| id_motivo_ausencia | Número que identifica o motivo da ausência do membro do colegiado na sessão de julgamento |
| id_sessao_julgamento | Número que identifica a sessão de julgamento |
| id_usuario | Número que identifica o usuário membro do colegiado que esteve ausente na sessão de julgamento |

## autuacao

Armazena parte das informações relativas à autuação dos processos (as demais informações da autuação estão na tabela parte_procedimento)

| Coluna | Descrição |
|---|---|
| id_autuacao | Número que identifica a autuação do processo, que tem relação também com dados na tabela parte_procedimento |
| descricao | Armazena informações da descrição (assunto) do processo |
| id_procedimento | Número que identifica o processo autuado |
| id_tipo_materia | Número que identifica o tipo de matéria atribuída ao processo autuado |
| idx_autuacao | Permite pesquisa indexada pela autuação |

## bloqueio_item_sess_unidade

Armazena as unidades que estão com restrição de acesso a um determinado processo pela sessão de julgamento

| Coluna | Descrição |
|---|---|
| id_bloqueio_item_sess_unidade | Número que identifica os registros de bloqueios cadastrados |
| id_distribuicao | Número que identifica o registro da distribuição |
| id_documento | Número que identifica o id_documento do documento bloqueado |
| id_unidade | Número que identifica a unidade que teve o acesso bloqueado |
| sta_tipo | Status multi-valorado que identifica o tipo de restrição de acesso aplicada:<br><br><ul><li>D = Restrição de acesso a Documento</li><li>O = Restrição aos demais não membros</li><li>P = Restrição de Unidade</li><li>S = Restrição à secretaria</li><li>X = Restrição aos Observadores Externos</li></ul> |

## colegiado

Parametrização sobre os informações básicas do colegiado (primeiro bloco de informações da parametrização de colegiado)

| Coluna | Descrição |
|---|---|
| id_colegiado | Número que identifica os registros de colegiados cadastrados |
| artigo | Status multi-valorado que define o gênero do substantivo do colegiado (por exemplo: "O" Conselho Diretor da Anatel ou "A" Primeira Turma de Julgamento):<br><br><ul><li>O = gênero masculino</li><li>A = gênero feminino</li></ul> |
| id_tipo_procedimento | Número que identifica o tipo de processo cadastrado como padrão para o colegiado |
| id_unidade_responsavel | Número que identifica a unidade responsável pela distribuição de processos ao colegiado |
| id_usuario_presidente | Número que identifica o usuário cadastrado como presidente do colegiado |
| id_usuario_secretario | Número que identifica o usuário cadastrado como secretário do colegiado |
| nome | Nome atribuído ao colegiado |
| quorum_minimo | Quórum mínimo para aberta das sessões colegiadas |
| sigla | Sigla atribuída ao colegiado |
| sin_ativo | Variável categórica que indica se o registro do colegiado está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |
| sta_algoritmo_distribuicao | Status multi-valorado que identifica o algoritmo de distribuição de processos utilizado pelo colegiado:<br><br><ul><li>R = Algoritmo de distribuição por rodadas</li><li>T = Algoritmo de distribuição por rodadas por tipo de processo</li><li>M = Algoritmo de distribuição por rodadas por tipo de matéria</li><li>P = Algoritmo de distribuição por peso atribuído ao membro</li></ul> |

## colegiado_composicao

Parametrização sobre os membros que compõem cada colegiado

| Coluna | Descrição |
|---|---|
| id_colegiado_composicao | Número que identifica os registros de membros do colegiado |
| id_cargo | Número que identifica o tipo de cargo atribuído ao membro do colegiado |
| id_colegiado_versao | Número que identifica os registros de versão dos colegiados cadastrados, onde é gerado novo id somente quando tenha sido distribuído processo para a antiga composição do colegiado |
| id_tipo_membro_colegiado | Status multi-valorado que identifica o tipo de membro do colegiado:<br><br><ul><li>1 = Titular</li><li>2 = Suplente</li><li>3 = Eventual</li></ul> |
| id_unidade | Número que identifica a unidade atribuída ao membro do colegiado |
| id_usuario | Número que identifica o usuário cadastrado como membro do colegiado |
| ordem | Número que identifica a ordem do membro do colegiado (setinhas verdes) |
| peso | Valor de peso atribuído a cada membro do colegiado |
| sin_habilitado | Variável categórica que indica se o usuário está habilitado a visualizar os processos da Sessão de Julgamento:<br><br><ul><li>S = Habilitado</li><li>N = Não habilitado</li></ul><br>Membros titulares sempre ficam habilitados. Membros Suplentes ou Eventuais podem estar ou não habilitados |
| sin_rodada | Variável categórica de domínio S/N.<br><br>**TODO:** Esta coluna é multivalorada e não foi possível arbitrar o significado de negócio de seus valores baseado apenas no código. Necessária revisão humana! |

## colegiado_versao

Parametrização sobre os informações básicas do colegiado (diferencia-se da tabela colegiado por trazer as informações do histórico)

| Coluna | Descrição |
|---|---|
| id_colegiado_versao | Número que identifica os registros de versão dos colegiados cadastrados, onde é gerado novo id somente quando tenha sido distribuído processo para a antiga composição do colegiado |
| dth_versao | Data e hora da última alteração no registro do colegiado |
| id_colegiado | Número que identifica os registros de colegiados cadastrados |
| id_tipo_procedimento | Número que identifica o tipo de processo cadastrado como padrão para o colegiado |
| id_unidade | Número que identifica a unidade do usuário que cadastrou o colegiado |
| id_unidade_responsavel | Número que identifica a unidade responsável pela distribuição de processos ao colegiado |
| id_usuario | Número que identifica o usuário que cadastrou o colegiado |
| id_usuario_presidente | Número que identifica o usuário cadastrado como presidente do colegiado |
| id_usuario_secretario | Número que identifica o usuário cadastrado como secretário do colegiado |
| nome | Nome atribuído ao colegiado |
| quorum_minimo | Quórum mínimo para aberta das sessões colegiadas |
| sigla | Sigla atribuída ao colegiado |
| sin_editavel | Variável categórica que indica se o registro do colegiado é editável:<br><br><ul><li>S = Permite edição</li><li>N = Não permite edição, ou seja, o SEI gerará uma nova id_colegiado_versao para o colegiado, pois já houve distribuição para essa composição colegiada</li></ul> |
| sin_ultima | Variável categórica que indica se o registro do colegiado é o último:<br><br><ul><li>S = Última versão</li><li>N = Não é a última versão do colegiado</li></ul><br>O SEI só gera uma nova versão do colegiado caso já tenha sido distribuído processo para a antiga composição do colegiado |
| sta_algoritmo_distribuicao | Status multi-valorado que identifica o algoritmo de distribuição de processos utilizado pelo colegiado:<br><br><ul><li>R = Algoritmo de distribuição por rodadas</li><li>T = Algoritmo de distribuição por rodadas por tipo de processo</li><li>M = Algoritmo de distribuição por rodadas por tipo de matéria</li><li>P = Algoritmo de distribuição por peso atribuído ao membro</li></ul> |

## destaque

Armazena informações sobre os destaques cadastrados nos itens da Pauta da Sessão de Julgamento e dos comentários públicos e restritos criados pelos usuários em cada processo

| Coluna | Descrição |
|---|---|
| id_destaque | Número que identifica os registros de destaque ou de comentário cadastrado nos itens em julgamento |
| descricao | Descrição informada pelo usuário ao cadastrar o Destaque ou Comentário Restrito |
| dth_destaque | Data e hora do cadastro do Destaque ou Comentário Restrito |
| id_item_sessao_julgamento | Número que identifica os registros dos itens pautados em sessões de julgamento |
| id_unidade | Número que identifica a unidade do usuário que cadastrou o destaque ou comentário |
| id_usuario | Número que identifica o usuário que cadastrou o destaque ou comentários restritos |
| sin_bloqueado | Variável categórica que indica se o Destaque está bloqueado para edição (para os casos de comentários restritos, o valor será sempre N):<br><br><ul><li>N = Não</li><li>S = Sim (o destaque fica bloqueado após ter sido lido por algum outro usuário)</li></ul> |
| sta_acesso | Status multi-valorado que identifica o tipo de acesso ao destaque:<br><br><ul><li>P = Público</li><li>R = Restrito</li></ul> |
| sta_tipo | Status multi-valorado que identifica o tipo de destaque ou comentários restritos:<br><br><ul><li>A = Acompanhar Relator</li><li>B = Acompanhar Divergência</li><li>C = Comentário</li><li>D = Divergir</li><li>E = Abster</li><li>G = Aguarda Vista</li><li>I = Impedimento/Suspeição</li><li>M = Manifestação Advogado(a)/Parte</li><li>R = Retirar</li><li>S = Sustentação Oral</li><li>T = Comentário Interno</li><li>V = Pedido de Vista</li><li>X = Discordância com o julgamento virtual</li><li>Z = Ressalva</li></ul> |

## distribuicao

Armazena parte das informações relativas à distribuição de processos ao Colegiado (caso na distribuição tenha havido impedimento, as informações do impedimento estarão na tabela impedimento)

| Coluna | Descrição |
|---|---|
| id_distribuicao | Número que identifica os registros de distribuição |
| dth_distribuicao | Armazena as informações de data e hora em que foi realizada a distribuição do processo |
| dth_situacao_atual | Armazena as informações de data e hora da última situação em que houve alteração do campo 'distribuicao' |
| id_colegiado_versao | Número que identifica os registros de versão do colegiado para o qual o processo foi distribuído |
| id_distribuicao_agrupador | Número que identifica o agrupador de distribuição: liga entre si os registros de uma mesma distribuição e suas redistribuições subsequentes. A distribuição original usa o próprio id_distribuicao como agrupador; cada redistribuição herda o mesmo valor da distribuição anterior. |
| id_documento_distribuicao | Número que identifica o documento gerado automaticamente no processo pelo SEI que contém as informações sobre a distribuição do processo |
| id_motivo_canc_distribuicao | Número que identifica o motivo de cancelamento da distribuição |
| id_motivo_prevencao | Número que identifica o motivo da prevenção (caso não seja indicada nenhum hipótese de prevenção o campo fica null) |
| id_procedimento | Número que identifica o processo distribuído |
| id_unidade | Número que identifica a unidade do usuário que realizou a distribuição do processo |
| id_unidade_relator | Número que identifica a unidade do usuário membro do colegiado designado relator do processo |
| id_unidade_relator_acordao | Número que identifica a unidade do usuário membro do colegiado que proferiu o voto condutor da decisão do processo (enquanto não houver decisão o campo fica null) |
| id_usuario | Número que identifica o usuário que realizou a distribuição do processo |
| id_usuario_relator | Número que identifica o usuário membro do colegiado designado relator do processo |
| id_usuario_relator_acordao | Número que identifica o usuário membro do colegiado que proferiu o voto condutor da decisão do processo (enquanto não houver decisão o campo fica null) |
| sin_prevencao | Variável categórica que indica se a distribuição foi realizada por prevenção:<br><br><ul><li>S = Distribuído por Prevenção</li><li>N = Não foi distribuído por Prevenção</li></ul> |
| sta_distribuicao | Status multi-valorado que identifica a distribuição ou a deliberação do processo:<br><br><ul><li>D = Distribuído</li><li>R = Redistribuído</li><li>P = Pautado</li><li>J = Julgado</li><li>V = Processo em pedido de vista</li><li>A = Adiado julgamento</li><li>M = Em Mesa</li><li>E = Para Referendo</li><li>L = Convertido em Diligência</li><li>T = Retirado de Pauta</li><li>X = Cancelado</li></ul> |
| sta_distribuicao_anterior | Status multi-valorado que identifica a distribuição ou a deliberação anterior do processo:<br><br><ul><li>D = Distribuído</li><li>R = Redistribuído</li><li>P = Pautado</li><li>J = Julgado</li><li>V = Processo em pedido de vista</li><li>A = Adiado julgamento</li><li>M = Em Mesa</li><li>E = Para Referendo</li><li>L = Convertido em Diligência</li><li>T = Retirado de Pauta (só quando a retirada de pauta se dá após o início da sessão de julgamento, antes disso o status do processo volta para o anterior)</li><li>X = Cancelado</li></ul> |
| sta_ultimo | Status multi-valorado que identifica a situação da distribuição do processo:<br><br><ul><li>S = Aparece em praticamente todas as situações, exceto nas duas situações citadas abaixo</li><li>I = Aparece quando o processo foi deliberado pelo colegiado</li><li>N = Apareceu apenas quando foi realizada redistribuição de processo que estava convertido em diligência</li></ul> |

## eleicao

Armazena informações de cadastro de Escrutínio Eletrônico

| Coluna | Descrição |
|---|---|
| id_eleicao | Número que identifica o Escrutínio Eletrônico |
| descricao | Descrição opcional do Escrutínio Eletrônico |
| id_item_sessao_julgamento | Número que identifica o processo da sessão associado com o Escrutínio Eletrônico. Ou seja, identifica o item da sessão a ser julgado na votação pelo Escrutínio Eletrônico |
| identificacao | Texto do Escrutínio Eletrônico que será exibido para os membros na hora da votação |
| ordem | Permite alterar a posição do Escrutínio Eletrônico na lista da tela de Escrutínios Eletrônicos do Processo |
| quantidade | Quantidade mínima de votos que cada membro deverá escolher para concluir a votação no Escrutínio Eletrônico. Não pode ser maior que a quantidade de opções de voto associada com o Escrutínio Eletrônico |
| sin_secreta | Variável categórica que indica se o conteúdo dos votos será identificado ao finalizar a votação no Escrutínio Eletrônico:<br><br><ul><li>S = Sim</li><li>N = Não</li></ul> |
| sta_situacao | Status multi-valorado que identifica a situação do Escrutínio Eletrônico:<br><br><ul><li>C = Criado</li><li>L = Liberado para colher votos dos membros do colegiado</li><li>U = Votação concluída e somente presidente e secretaria conseguem ver o resultado</li><li>F = Finalizado com resultado exibido para todos os membros</li><li>A = Anulado</li></ul> |

## impedimento

Armazena informações de processos que foram distribuídos e que houve hipóteses de impedimentos de membros do colegiado

| Coluna | Descrição |
|---|---|
| id_impedimento | Número que identifica os registros de impedimentos |
| id_distribuicao | Número que identifica os registros de distribuição |
| id_motivo_impedimento | Número que identifica o motivo do impedimento (relaciona também com o campo id_motivo_distribuicao da tabela distribuicao para pegar a descrição) |
| id_usuario | Número que identifica o usuário membro do colegiado que foi impedido na distribuição |

## item_sessao_documento

Armazena informações sobre os documentos disponibilizados para os itens da sessão de julgamento

| Coluna | Descrição |
|---|---|
| id_item_sessao_documento | Número que identifica os registros dos documentos disponibilizados para cada item da sessão de julgamento |
| id_documento | Número SEI do documento disponibilizado para o item da sessão de julgamento |
| id_item_sessao_julgamento | Número que identifica o item de registro do processo na sessão de julgamento (não é o número da ordem do processo na pauta, é o id sequencial do registro) |
| id_unidade | Número que identifica a área do usuário membro do colegiado que disponibilizou o documento para o item da sessão de julgamento (não é o id do usuário que disponbilizou) |
| id_usuario | Número que identifica o usuário membro do colegiado que disponibilizou o documento para o item da sessão de julgamento (não é o id do usuário que disponbilizou) |

## item_sessao_julgamento

Armazena informações sobre a estrutura/composição da pauta das sessões colegiadas

| Coluna | Descrição |
|---|---|
| id_item_sessao_julgamento | Número que identifica os registros dos itens pautados em sessões de julgamento |
| dispositivo | Campo texto que contém o dispositivo de julgamento do item da sessão que constará na Ata e na Certidão de Julgamento |
| dth_inclusao | Data e Hora em que o processo foi incluído em pauta |
| id_distribuicao | Número que identifica o registro da distribuição |
| id_documento | Número que identifica o documento vinculado ao item da sessão de julgamento. |
| id_documento_julgamento | Número que identifica o id_protocolo da certidão de julgamento gerada no item da pauta após a sessão ser finalizada |
| id_motivo_mesa | Número que identifica o motivo de o processo ter sido pautado em mesa |
| id_sessao_bloco | Identifica em qual bloco de sessão o processo foi inserido (Pauta, Referendo, etc). |
| id_sessao_julgamento | Número que identifica o registro de sessão de julgamento |
| id_unidade_sessao | Número que identifica a unidade do membro do colegiado pautou o processo |
| id_usuario_presidente | Indica o Usuário SEI que presidia a sessão no momento que foi gerado o dispositivo do item. É utilizado na alteração de dispositivo com sessão encerrada para não perder a informação de quem era o presidente no momento do julgamento do item. |
| id_usuario_sessao | Número que identifica qual membro do colegiado pautou o processo |
| ordem | Ordem do processo na pauta, dentre os processos pautados pelo mesmo membro do colegiado (por exemplo: mesmo que o processo seja o item 10 da pauta, a ordem do processo dentro da pauta daquele Conselheiro pode ser a 3) |
| sin_manual | Variável categórica que indica se o dispositivo de julgamento foi convertido para manual:<br><br><ul><li>S = Convertido para Manual</li><li>N = Gerado automaticamente</li></ul> |
| sta_situacao | Status multi-valorado que identifica a situação do processo durante a sessão de julgamento:<br><br><ul><li>N = Normal (Item em Pauta - Pauta, Mesa ou Referendo)</li><li>J = Julgado</li><li>M = Em Julgamento</li><li>D = Diligência</li><li>A = Adiado</li><li>R = Retirado de pauta</li><li>V = Solicitada Vista</li><li>C = Sessão Cancelada</li><li>I = Somente quando retirado com pauta aberta e existiam destaques</li></ul> |

## julgamento_parte

Armazeza informações sobre os itens em que houve fracionamento da votação

| Coluna | Descrição |
|---|---|
| id_julgamento_parte | Número que identifica os registros de partes do julgamento |
| descricao | Descrição da parte do julgamento fracionada (Integral, etc.) |
| id_item_sessao_julgamento | Número que identifica o item do processo na sessão de julgamento |
| id_usuario_desempate | Armazena o id do usuário que venceu o julgamento por desempate, caso não haja empate este campo é null; |
| ordem | Indica a ordem das frações de julgamento |

## motivo_ausencia

Parametrização dos motivos de ausência dos membros do Colegiado

| Coluna | Descrição |
|---|---|
| id_motivo_ausencia | Número que identifica os registros de ausência em sessão |
| descricao | Descrição do motivo de ausência |
| sin_ativo | Variável categórica que indica se o registro de ausência em sessão está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |

## motivo_canc_distribuicao

Parametrização dos motivos de cancelamento de distribuição a Colegiados

| Coluna | Descrição |
|---|---|
| id_motivo_canc_distribuicao | Número que identifica os registros de motivos de cancelamento de distribuição |
| descricao | Descrição do motivo de cancelamento de distribuição |
| sin_ativo | Variável categórica que indica se o registro de motivos de cancelamento de distribuição está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |

## motivo_distribuicao

Parametrização dos motivos de distribuição de processos ao Colegiado

| Coluna | Descrição |
|---|---|
| id_motivo_distribuicao | Número que identifica os registros de motivos de distribuição |
| descricao | Descrição do motivo de distribuição |
| sin_ativo | Variável categórica que indica se o registro de motivos de distribuição está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |
| sta_tipo | Status multi-valorado que identifica o tipo de motivos de distribuição:<br><br><ul><li>I = Impedimento</li><li>P = Prevenção</li></ul> |

## motivo_mesa

Parametrização dos motivos de pautar o processo em mesa

| Coluna | Descrição |
|---|---|
| id_motivo_mesa | Número que identifica os registros de motivos de mesa |
| descricao | Descrição do motivo de mesa |
| ordem | Ordem definida na parametrização de motivos de mesa |
| sin_ativo | Variável categórica que indica se o registro de motivos de mesa está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |

## opcao_eleicao

Armazena informações de cadastro de opção de voto associada com Escrutínio Eletrônico

| Coluna | Descrição |
|---|---|
| id_opcao_eleicao | Número que identifica a opção de voto associada com o Escrutínio Eletrônico |
| id_eleicao | Número que identifica o Escrutínio Eletrônico associado |
| identificacao | Texto da opção de voto que será exibido para os membros na hora da votação no Escrutínio Eletrônico do Processo |
| ordem | Ordem em que será exibida a opção de voto para escolha no Escrutínio Eletrônico do Processo |

## parte_procedimento

Armazena informações das partes de um processo indicadas pelo usuário ao autuar um processo

| Coluna | Descrição |
|---|---|
| id_parte_procedimento | Número que identifica os registros das partes de um processo indicadas pelo usuário ao autuar um processo |
| id_contato | Número que identifica o contato (interessado) cadastrado pelo usuário ao autuar o processo |
| id_procedimento | Número que identifica o processo que foi segregado em partes para julgamento |
| id_qualificacao_parte | Número que representa o qualificação de contato cadastrado pelo usuário ao autuar o processo |
| id_unidade | Número que representa a unidade do usuário que cadastrou a informação |

## pedido_vista

Armazena os registros de pedidos de vista formulados em processos pautados em sessões de julgamento

| Coluna | Descrição |
|---|---|
| id_pedido_vista | Número que identifica os registros de pedidos de vista formulados por membros do colegiado |
| dth_devolucao | Data e Hora de devolução do processo à Secretaria do Colegiado (ao acionar o botão devolvar à Secretaria) |
| dth_pedido | Data e Hora do lançamento do registro de pedido de vista no módulo |
| id_distribuicao | Número que identifica a distribuição do processo objeto do pedido de vista |
| id_unidade | Número que identifica a unidade do usuário membro do colegiado que solicitou vista do processo |
| id_usuario | Número que identifica o usuário membro do colegiado que solicitou vista do processo |
| sin_pendente | Variável categórica que indica se o processo possui outro pedido de vista pendente (por exemplo: um membro do colegiado solicita vista do processo, apresenta em outra sessão e outro membro do colegiado solicita vista. No registro da primeira vista o campo fica "N", pois não havia nenhum pedido de vista anterior pendente, mas no segundo pedido de vista, o registro fica "S"):<br><br><ul><li>S = Sim</li><li>N = Não</li></ul> |

## presenca_sessao

Armazena informações sobre data e hora do registro de presença e de ausência dos membros do colegiado na sessão de julgamento

| Coluna | Descrição |
|---|---|
| id_presenca_sessao | Número que identifica os registros de presença nas sessões de julgamento |
| dth_entrada | Data e hora do registro de presença do membro do colegiado na sessão de julgamento |
| dth_saida | Data e hora do registro de ausência do membro do colegiado na sessão de julgamento |
| id_sessao_julgamento | Número que identifica os registros de sessão de julgamento |
| id_usuario | Número que identifica o usuário membro do colegiado |
| sta_modalidade | Status multi-valorado da modalidade da presença:<br><br>P = Presencial<br>T = Remoto<br>V = Virtual<br>N = Não informada. |

## provimento

Parametrização dos tipos de provimentos

| Coluna | Descrição |
|---|---|
| id_provimento | Número que identifica os tipos de provimentos |
| conteudo | Descrição do tipo de provimento |
| sin_ativo | Variável categórica que indica se o registro de tipos de provimentos está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |

## qualificacao_parte

Parametrização da qualificação de partes do processo

| Coluna | Descrição |
|---|---|
| id_qualificacao_parte | Número que identifica os tipos de qualificação de partes do processo |
| descricao | Descrição do tipo de qualificação de partes do processo |
| sin_ativo | Variável categórica que indica se o registro de tipos de qualificação de partes do processo está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |

## rel_autuacao_tipo_materia

Relaciona os tipos de matéria com a autuação do processo

| Coluna | Descrição |
|---|---|
| id_autuacao | Número que identifica a autuação do processo na relação entre os tipos de matéria com a autuação do processo |
| id_tipo_materia | Número que identifica o tipo de matéria na relação entre os tipos de matéria com a autuação do processo |
| ordem | Especifica a ordem dos tipos de matéria relacionados com o processo autuado. Se houver mais de um tipo de matéria associado na autuação do processo, somente o primeiro tipo de matéria será considerado na distribuição quando o colegiado utiliza algoritmo de distribuição por tipo de matéria |

## rel_colegiado_usuario

Associativa entre os usuários externos e os observadores cadastrados em cada colegiado

| Coluna | Descrição |
|---|---|
| id_colegiado | Número que identifica os registros de colegiados cadastrados |
| id_usuario | Número que identifica o usuário externo cadastrado como observador do colegiado |

## rel_destaque_usuario

Armazena informações sobre o usuário que criou o registro de destaque ou comentário restrito no processo

| Coluna | Descrição |
|---|---|
| id_destaque | Número que identifica os registros de destaque ou de comentário cadastrado nos itens em julgamento |
| id_usuario | Número que identifica o usuário que cadastrou o destaque ou comentários restritos |

## rel_motivo_distr_colegiado

Identifica em quais colegiados os motivos de distribuição estão cadastrados. Surgiu na versão 1.2.0 do SEI.

| Coluna | Descrição |
|---|---|
| id_colegiado | Número que identifica os registros de colegiados cadastrados |
| id_motivo_distribuicao | Número que identifica o motivo de distribuição |

## revisao_item

Registra revisões de itens de sessão de julgamento.

| Coluna | Descrição |
|---|---|
| id_revisao_item | Número que identifica os registros de revisão de itens de sessão de julgamento |
| dth_revisao | Data e hora da última vez que o usuário clicou sobre o ícone de revisão, quer seja para marcar como revisado ou para desmarcar |
| id_item_sessao_julgamento | Número que identifica os registros dos itens pautados em sessões de julgamento |
| id_unidade | Número que identifica a unidade do usuário que acionou o ícone de revisão de um item pautado |
| id_usuario | Número que identifica o usuário que acionou o ícone de revisão de um item pautado |
| sin_revisado | Variável categórica que indica se o item foi revisado:<br><br><ul><li>S = Sim, foi revisado</li><li>N = Não foi revisado</li></ul> |

## seq_algoritmo

Sequence da tabela algoritmo

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela algoritmo em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela algoritmo. |

## seq_andamento_sessao

Sequence da tabela andamento_sessao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela andamento_sessao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela andamento_sessao. |

## seq_atributo_andamento_sessao

Sequence da tabela atributo_andamento_sessao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela atributo_andamento_sessao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela atributo_andamento_sessao. |

## seq_ausencia_sessao

Sequence da tabela ausencia_sessao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela ausencia_sessao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela ausencia_sessao. |

## seq_autuacao

Sequence da tabela autuacao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela autuacao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela autuacao. |

## seq_bloqueio_item_sess_unidade

Sequence da tabela bloqueio_item_sess_unidade

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela bloqueio_item_sess_unidade em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela bloqueio_item_sess_unidade |

## seq_colegiado

Sequence da tabela colegiado

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela colegiado em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela colegiado. |

## seq_colegiado_composicao

Sequence da tabela colegiado_composicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela colegiado_composicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela colegiado_composicao. |

## seq_colegiado_versao

Sequence da tabela colegiado_versao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela colegiado_versao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela colegiado_versao. |

## seq_destaque

Sequence da tabela destaque

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela destaque em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela destaque. |

## seq_distribuicao

Sequence da tabela distribuicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela distribuicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela distribuicao. |

## seq_eleicao

Sequence da tabela eleicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela eleicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela eleicao. |

## seq_impedimento

Sequence da tabela impedimento

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela impedimento em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela impedimento. |

## seq_item_sessao_documento

Sequence da tabela item_sessao_documento

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela item_sessao_documento em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela item_sessao_documento. |

## seq_item_sessao_julgamento

Sequence da tabela item_sessao_julgamento

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela item_sessao_julgamento em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela item_sessao_julgamento. |

## seq_julgamento_item

Sequence da tabela julgamento_item

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela julgamento_item em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela julgamento_item. |

## seq_julgamento_parte

Sequence da tabela julgamento_parte

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela julgamento_parte em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela julgamento_parte. |

## seq_motivo_ausencia

Sequence da tabela motivo_ausencia

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela motivo_ausencia em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela motivo_ausencia. |

## seq_motivo_canc_distribuicao

Sequence da tabela motivo_canc_distribuicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela motivo_canc_distribuicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela motivo_canc_distribuicao. |

## seq_motivo_distribuicao

Sequence da tabela motivo_distribuicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela motivo_distribuicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela motivo_distribuicao. |

## seq_motivo_mesa

Sequence da tabela motivo_mesa

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela motivo_mesa em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela motivo_mesa. |

## seq_opcao_eleicao

Sequence da tabela opcao_eleicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela opcao_eleicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela opcao_eleicao. |

## seq_parte_procedimento

Sequence da tabela parte_procedimento

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela parte_procedimento em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela parte_procedimento. |

## seq_pedido_vista

Sequence da tabela pedido_vista

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela pedido_vista em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela pedido_vista. |

## seq_presenca_sessao

Sequence da tabela presenca_sessao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela presenca_sessao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela presenca_sessao. |

## seq_provimento

Sequence da tabela provimento

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela provimento em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela provimento. |

## seq_qualificacao_parte

Sequence da tabela qualificacao_parte

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela qualificacao_parte em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela qualificacao_parte. |

## seq_revisao_item

Sequence da tabela revisao_item

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela revisao_item em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela revisao_item. |

## seq_sessao_bloco

Sequence da tabela sessao_bloco

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela sessao_bloco em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela sessao_bloco. |

## seq_sessao_julgamento

Sequence da tabela sessao_julgamento

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela sessao_julgamento em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela sessao_julgamento. |

## seq_sustentacao_oral

Sequence da tabela sustentacao_oral

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela sustentacao_oral em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela sustentacao_oral. |

## seq_tarefa_sessao

Sequence da tabela tarefa_sessao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela tarefa_sessao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela tarefa_sessao. |

## seq_tipo_materia

Sequence da tabela tipo_materia

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela tipo_materia em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela tipo_materia. |

## seq_tipo_sessao

Sequence da tabela tipo_sessao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela tipo_sessao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela tipo_sessao. |

## seq_tipo_sessao_bloco

Sequence da tabela tipo_sessao_bloco

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela tipo_sessao_bloco em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela tipo_sessao_bloco. |

## seq_voto_eleicao

Sequence da tabela voto_eleicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela voto_eleicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela voto_eleicao. |

## seq_voto_opcao_eleicao

Sequence da tabela voto_opcao_eleicao

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela voto_opcao_eleicao em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela voto_opcao_eleicao. |

## seq_voto_parte

Sequence da tabela voto_parte

| Coluna | Descrição |
|---|---|
| campo | Armazena a variável da tabela voto_parte em que a sequence é aplicada. |
| id | Número que identifica o sequencial da tabela voto_parte. |

## sessao_bloco

Armazena os blocos de processos de cada sessão (Pauta, Mesa, Referendo)

| Coluna | Descrição |
|---|---|
| id_sessao_bloco | Número que identifica os registros de blocos de processos de cada sessão |
| descricao | Nome atribuído ao Bloco de Processos (Pauta, Mesa, Referendo) |
| id_sessao_julgamento | Número que identifica o registro de sessão de julgamento |
| ordem | Ordem do bloco na sessão de julgamento |
| sin_agrupar_membro | Variável categórica que indica se o bloco de processos agrupará os itens pautados de acordo com os membros do colegiado:<br><br><ul><li>S = Sim</li><li>N = Não</li></ul> |
| sta_tipo_item | Status multi-valorado que identifica o tipo dos itens do bloco de processo:<br><br><ul><li>1 = Pauta</li><li>2 = Mesa</li><li>3 = Referendo</li></ul> |

## sessao_julgamento

Armazena informações sobre as sessões de julgamento cadastradas

| Coluna | Descrição |
|---|---|
| id_sessao_julgamento | Número que identifica os registros de sessões de julgamento |
| dth_fim | Data e hora prevista para o fim da sessão de julgamento |
| dth_inicio | Data e hora prevista para o início da sessão de julgamento |
| dth_sessao | Data de realização da sessão de julgamento |
| id_colegiado | Número que identifica o colegiado responsável pela sessão de julgamento |
| id_colegiado_versao | Número que identifica o registro de versão do colegiado responsável pela sessão de julgamento |
| id_documento_pauta | Número SEI do documento gerado no processo de forma automática pelo módulo ao clicar no botão Abrir Pauta |
| id_documento_sessao | Número SEI do documento que contém a Ata da Sessão de Julgamento |
| id_procedimento | Número SEI do processo criado para cada sessão de julgamento |
| id_tipo_sessao | Número que identifica o tipo de sessão (Ordinária, Extraordinária, etc) |
| id_usuario_presidente | Número que identifica o usuário presidente da sessão de julgamento |
| link_reuniao | Armazena o link de reunião da sessão. |
| obs_link | Armazena a observação do link da sessão. |
| sta_modalidade_virtual | Status multi-valorado que identifica a modalidade virtual da sessão:<br><br><ul><li>N = Não se aplica</li><li>D = Por Destaques</li><li>I = Voto sem Consulta Externa</li><li>E = Voto com Consulta Externa</li></ul> |
| sta_situacao | Status multi-valorado que identifica a situação da sessão de julgamento:<br><br><ul><li>P = Prevista</li><li>A = Pauta Aberta</li><li>F = Pauta Fechada</li><li>B = Aberta</li><li>E = Encerrada</li><li>S = Suspensa</li><li>X = Cancelada</li><li>Z = Finalizada</li></ul> |

## sustentacao_oral

Armazena os registros de sustentações orais realizadas em processos pautados em sessões de julgamento

| Coluna | Descrição |
|---|---|
| id_sustentacao_oral | Número que identifica os registros de sustentações orais em processos pautados |
| id_contato | Número que identifica o contato ao qual está vinculada a sustentação oral |
| id_item_sessao_julgamento | Número que identifica o item do processo na sessão de julgamento |
| id_qualificacao_parte | Número que representa a qualificação da parte que fez a sustentação oral |

## tarefa_sessao

Armazena os tipos de tarefa que são geradas automaticamente pelo SEI Julgar no andamento do processo referentes à sessão de julgamento. Outras tarefas também são geradas automaticamente pelo SEI Julgar no andamento do processo e podem ser consultadas na tabela tarefa, em que o campo id_tarefa_modulo é igual a TRF4_SESSAO_JULGAMENTO_*

| Coluna | Descrição |
|---|---|
| id_tarefa_sessao | Número que identifica os tipos de tarefas geradas automaticamente pelo módulo no andamento do processo |
| nome | Nome da Tarefa |
| sin_historico_resumido | Variável categórica que indica se a Tarefa deverá aparecer no histórico resumido do item a ser julgado:<br><br><ul><li>S = Sim</li><li>N = Não</li></ul> |

## tipo_materia

Parametrização dos tipos de naturezas de matéria

| Coluna | Descrição |
|---|---|
| id_tipo_materia | Número que identifica os tipos de matéria |
| descricao | Descrição do tipo de matéria |
| sin_ativo | Variável categórica que indica se o registro de tipo de matéria está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |

## tipo_membro_colegiado

Parametrização do tipo de membros de colegiados

| Coluna | Descrição |
|---|---|
| id_tipo_membro_colegiado | Número que identifica os tipos de membros de colegiado |
| nome | Nome do tipo de membro do colegiado |
| sin_ativo | Variável categórica que indica se o tipo de membro está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |

## tipo_sessao

Parametrização do tipo de sessão

| Coluna | Descrição |
|---|---|
| id_tipo_sessao | Número que identifica os tipos de sessão |
| descricao | Descrição do tipo de sessão |
| sin_ativo | Variável categórica que indica se o registro de tipo de sessão está ativo:<br><br><ul><li>S = Ativo</li><li>N = Inativo</li></ul> |
| sin_virtual | Variável categórica que indica se a sessão será virtual:<br><br><ul><li>S = Sim</li><li>N = Não</li></ul> |

## tipo_sessao_bloco

Armazena os blocos de processos padrão de cada tipo de sessão (Pauta, Mesa, Referendo)

| Coluna | Descrição |
|---|---|
| id_tipo_sessao_bloco | Número que identifica os registros de blocos de processos padrão de cada tipo de sessão |
| descricao | Nome atribuído ao Bloco de Processos padrão da sessão (Pauta, Mesa, Referendo) |
| id_tipo_sessao | Número que identifica o tipo de sessão (Ordinária, Extraordinária, etc) |
| ordem | Ordem do bloco no tipo de sessão |
| sin_agrupar_membro | Variável categórica que indica se o bloco de processos agrupará os itens pautados de acordo com os membros do colegiado:<br><br><ul><li>S = Sim</li><li>N = Não</li></ul> |
| sta_tipo_item | Status multi-valorado que identifica o tipo dos itens do bloco de processo:<br><br><ul><li>1 = Pauta</li><li>2 = Mesa</li><li>3 = Referendo</li></ul> |

## voto_eleicao

Armazena informações de voto lançado no Escrutínio Eletrônico associado

| Coluna | Descrição |
|---|---|
| id_voto_eleicao | Número que identifica os registros de votos lançados em Escrutínio Eletrônico |
| dth_voto_eleicao | Data e Hora em que o registro do voto foi lançado |
| id_eleicao | Número que identifica o registro do Escrutínio Eletrônico |
| id_usuario | Número que identifica o usuário membro do colegiado que lançou o voto |
| ordem | Ordem definida pelo usuário no momento em que salvou o voto, caso a votação seja com lista de preferências |

## voto_opcao_eleicao

Armazena informações de relação entre o voto lançado (id_voto_eleicao) e a opção de voto escolhida (id_opcao_eleicao) na votação no Escrutínio Eletrônico associado

| Coluna | Descrição |
|---|---|
| id_voto_opcao_eleicao | Número que identifica os registros de opções de voto escolhidas |
| id_opcao_eleicao | Número que identifica a opção de voto escolhida |
| id_voto_eleicao | Número que identifica o voto lançado no Escrutínio Eletrônico |
| ordem | Ordem definida pelo usuário em cada opção de voto, caso a votação seja com lista de preferências |

## voto_parte

Armazena informações dos votos proferidos em cada item das sessões de julgamento

| Coluna | Descrição |
|---|---|
| id_voto_parte | Número que identifica os registros de votos lançados |
| complemento | Texto do voto, caso ele seja de referendo, diligência ou destaque do tipo comentar |
| dth_voto | Data e hora do lançamento do voto |
| id_julgamento_parte | Número que identifica o registro da parte do julgamento na qual o voto foi lançado |
| id_provimento | Número que identifica o provimento lançado no voto |
| id_sessao_voto | Número que identifica a sessão em que o voto foi lançado |
| id_usuario | Número que identifica o usuário membro do colegiado que lançou o voto |
| id_usuario_lancamento | Número ID que identifica o usuário responsável pelo lançamento do voto. |
| id_voto_parte_associado | Número que identifica o voto anterior associado ao registro |
| ressalva | Texto da ressalva do voto, caso exista |
| sin_ativo | Variável categórica que indica se o voto está ativo:<br><br><ul><li>S = Ativo</li><li>N = Não ativo</li></ul> |
| sin_vencedor | Variável categórica que indica se o voto é o voto vencedor em casos em que houve empate e o presidente teve que proferir voto de desempate:<br><br><ul><li>S = Sim, é o voto vencedor</li><li>N = Não é o voto vencedor</li></ul> |
| sta_voto_parte | Status multi-valorado que identifica o tipo de voto proferido no processo em sessão de julgamento:<br><br><ul><li>A = Acompanha Relator</li><li>B = Acompanha Divergência</li><li>C = Cancelado</li><li>D = Diverge</li><li>G = Aguarda Vista</li><li>I = Impedimento/Suspeição</li><li>J = Discordância com o julgamento virtual</li><li>P = Provimento Disponibilizado</li><li>S = Abstenção</li><li>V = Pedido de Vista</li><li>X = Ausente</li></ul> |
