---
name: sei-historico-versoes-novidades-evolucoes-correcoes
description: cataloga lista com histórico cronológico das versões dos sistemas SEI e SIP (desenvolvidos e mantidos pelo TRF4), na ordem da Versão principal mais recente até a mais antiga, detalhando as Novidades, Evoluções e Correções ocorridas em cada versão distribuída do SEI. A ordem das seções abaixo são da 'Versão Principal' mais recente distribuída do sistema e dentro dela constam subseções das 'Versões de Atualização' identificadas pelo incremento do terceiro dígito do número da versão do SEI.
	- Use quando precisar localizar:
		- Informações sobre as funcionalidades existentes.
		- Informações sobre as Novidades, Evoluções e Correções já realizadas e em qual versão foram implementadas.
		- Para ter uma visão geral e incremental das melhorias.
	- No início de cada seção de 'Versão Principal' pode ter lista com as 'Dependências tecnológicas importantes'.
---

# Versão Principal 5.0.0

**Dependências tecnológicas importantes**:
	- Sistema Operacional Linux
	- Apache 2.4
	- PHP 8.2
	- Solr 9.6.1
	- Funcionamento em bancos de dados: MySQL, SQL Server, Oracle ou PostgreSQL

1. Novo editor web com visual mais moderno e melhor usabilidade:
	a. permite inclusão de comentários em trechos do texto com visibilidade global, somente unidade ou apenas para o usuário que adicionou;
	b. visualização e inclusão de comentários em trechos do documento também por meio da árvore de processo;
	c. melhorias em tabelas com opções para legenda, alinhamento, redimensionamento uniforme de colunas, ordenação de colunas e limpeza de formatação;
	d. conversão automática de números no texto selecionado para links de protocolos (ao clicar no botão de inclusão de link SEI);
	e. mais opções de formatos em listas ordenadas e não ordenadas com possibilidade de combinar as opções desejadas;
	f. inclusão de referências no texto.
2. Interface
	a. novo esquema de cores “Cinza Escuro”;
	b. Controle de Processos agora exibe a opção “Visualização Detalhada” que pode ser configurada pela opção associada “Configurar Detalhe”;
	c. no ícone “Configuração do Sistema” é possível escolher a página inicial (Controle de Processos, Painel de Controle ou Blocos de Assinatura) e também optar por filtrar os botões acessados recentemente;
	d. o acesso ao menu agora é feito por meio de um ícone localizado ao lado do logo do sistema;
	e. possibilidade de arrastar arquivo para upload no cadastro de documento externo.
3. Usuários Externos
	a. autenticação em 2 fatores com código disponibilizado por email;
	b. acesso por meio do gov.br com liberação automática do usuário externo;
	c. assinatura avançada pelo gov.br;
	d. aceite de Termo de Uso e/ou Política de Privacidade da instituição.
4. Ouvidoria
	a. possibilidade de contato anônimo;
	b. indicação de sigilo para os dados do formulário de contato;
	c. sinalização de atendimento parcial para uma solicitação;
	d. possibilidade de envio de anexos pelo cidadão;
	e. sinalização de atendimento registrado pela ouvidoria;
	f. mais opções de filtro no Acompanhamento da Ouvidoria.
5. Na Avaliação Documental a CPAD vou substituída por um conjunto de revisores. A quantidade de revisores é parametrizada permitindo valor maior ou igual a zero (sem revisão). Também foram realizadas diversas melhorias na pesquisa de avaliações e revisões e ajuste no leiaute dos documentos de edital e listagem de eliminação;
6. Adicionado item de menu “Lixeira” onde ficam disponíveis temporariamente os conteúdos de documentos excluídos/cancelados. O próprio usuário que executou a ação poderá fazer o download do conteúdo;
7. A consulta processual externa agora exibe processos públicos e restritos;
8. No cadastro de extensões de arquivos foram adicionadas opções para indicar quais as extensões permitidas para upload por usuários externos e formulário da ouvidoria;
9. Preparação para CNPJ alfanumérico;
10. Atualização do assinador de documentos com certificado digital;
11. SIP
	a. possibilidade de configurar a autenticação utilizando serviços de login único (SSO) como Google, Microsoft e gov.br;
	b. novo parâmetro para sinalizar o uso de código único de 2 fatores para todos os sistemas existentes no SIP;
	c. possibilidade de configurar quais são os navegadores compatíveis exibindo alerta para o usuário (menu Infra/Configuração de Navegadores);
	d. nova funcionalidade para sincronização de perfis permitindo importar facilmente todos os recursos e itens de menu de um perfil para outro. Na operação também é possível informar recursos que devem ser ignorados.

## Versão de Atualização 5.0.1

1. Envios e recebimentos envolvendo o SEI Federação agora são exibidos como itens na árvore do processo.
2. No novo editor, foi adicionado um botão no menu relacionado a tabelas, chamado “Alterar tema da tabela”.
3. Os comentários em trechos de documentos agora são exibidos após a assinatura, e foi adicionado o novo nível de visibilidade “Tramitação” (visível apenas para as unidades por onde o processo passou).
4. Na assinatura por usuário externo, o processo não estava sendo sinalizado com o triângulo na unidade geradora do documento.
5. Agora, na árvore do processo, ao clicar no ícone da caneta de assinatura, serão listadas todas as assinaturas do documento.
6. Foi adicionado o novo parâmetro SEI_PUBLICACAO_RESUMO para controlar a obrigatoriedade do campo “Resumo” no agendamento de publicações. Os valores são: 1 - opcional (valor padrão), 2 - obrigatório pela interface ou 3 - obrigatório pela interface e web services.
7. Correções e melhorias no novo editor (formatação de texto, colagem, tabelas, …).
8. Corrigidas quebras de linha em textos padrão salvos no novo editor e utilizados em emails.
9. Corrigido erro eventual de formatação no texto de comentários em trechos de documento.
10. Não estava permitindo copiar texto ao navegar pelos documentos de um bloco.
11. Reativada a exibição do ícone de novidades na barra superior.
12. Corrigido erro no script de instalação em bases Oracle ao alterar o campo cnpj: `ORA-01439: column to be modified must be empty to change datatype`.
13. Corrigido erro no agendamento removerAquivosNaoUtilizados quando não existem arquivos para exclusão.
14. Corrigida a exibição duplicada do item de menu Infra/Erros do PHP.

## Versão de Atualização 5.0.2

1. A assinatura avançada gov.br, se configurada para usuários internos, agora estará disponível sem a necessidade de realizar o login no sistema pelo gov.br.
2. Corrigida a identificação de login gov.br para usuários externos quando o SEI e SIP executam no mesmo endereço: “Houve um erro ao efetuar login no serviço.”
3. Corrigido erro na assinatura avançada gov.br por usuário externo em documento sigiloso: “Documento não está disponível para assinatura.”
4. Corrigida a pesquisa por parte de números ao utilizar o caractere `*` (asterisco).
5. Corrigido erro de permissão ao reabrir processo com revisão de avaliação documental.
6. Corrigido erro eventual de parâmetro não encontrado quando o parâmetro existe sem valor informado.

## Versão de Atualização 5.0.3

1. Melhorias no novo editor: visualização em modo página, desempenho para documentos muito grandes, formatação de parágrafos, impressão de tabelas e tratamento de conteúdo sinalizado como somente leitura.
2. Adicionada substituição de variáveis na pré-visualização de modelos com o novo editor.
3. Comentários de documentos (ícone da funcionalidade) não assinados agora são visíveis para as unidades com tramitação no processo.
4. Corrigido erro ao abrir pasta contendo documento com credencial para assinatura.
5. Corrigido erro replicando acessos do SEI Federação quando um órgão participante do processo foi desativado na instalação remota.
6. Corrigido erro processando histórico para unidades que tiveram mudança de órgão: `Erro aplicando histórico`.
7. Corrigido erro em alguns dispositivos móveis que não permitia selecionar a visibilidade de comentários em trechos de documento (ícone da funcionalidade).
8. Corrigido erro eventual nas estatísticas quando houve alteração na data/hora do sistema.

## Versão de Atualização 5.0.4

1. Ao listar blocos, a exibição das unidades de disponibilização foi limitada a 5 registros, com opção para exibição completa.
2. Agora, ao incluir um texto padrão pelo editor, as variáveis referenciadas serão substituídas automaticamente durante a edição.
3. Adicionado autocompletar de nomes de variáveis na elaboração de texto padrão e no cadastro de seções de modelos.
4. Adicionado novo parâmetro opcional SEI_CRITERIO_CONTROLE_INTERNO para facilitar o gerenciamento dos critérios pela interface em bases grandes (ver opções por meio do menu Infra > Configuração do Sistema).
5. Aprimoramentos na exibição e no tratamento do Nome Social.
6. Melhorias e correções diversas no novo editor (formatação de tabelas, exibição de referências, salvamento de imagens grandes, etc.).
7. Correção para que não mais ocorra a alteração automática do nível de acesso no cadastro do processo ao incluir documento com nível mais restritivo, continuando ativa a contaminação.
8. Correção no Relatório de Atividade na Unidade, que poderia considerar alguns andamentos fora do período informado.
9. Correção de erro para usuários internos ao assinar com gov.br: `Atributo [Nome] não recebeu valor`.
10. Correção de erro ao alterar estilos: `consulta retornou mais de um registro de CONJUNTO_ESTILOS`.
11. Correção de erro ao consultar processos de Ouvidoria via integração por web services.
12. Adicionado tratamento na atualização de versão para erro eventual criando índice em bases SQL Server: `Object was created with the following SET options off: 'ANSI_NULLS'`.


# Versão Principal 4.1.0

**Dependências tecnológicas importantes**:
	- Sistema Operacional Linux
	- Apache 2.4.6
	- PHP 7.3.12
	- Solr 8.2.0
	- Funcionamento em bancos de dados: MySQL, SQL Server, Oracle ou PostgreSQL

1. Adicionado Plano de Trabalho com sugestão de etapas e itens associados com o tipo de processo;
2. Novo conjunto de funcionalidades para Avaliação Documental;
3. Painel de Controle exibe mais informações com leiaute em cartões e ícone para acesso rápido na barra superior;
4. Reabertura Programada de processos;
5. Possibilidade de sinalizar processos como prioritários (ex.: Idoso, PcD, ...);
6. Nova tela para Consulta Processual externa;
7. No cadastro de documento agora é possível informar um valor monetário (configurável no tipo do documento) e na pesquisa foi adicionado um novo filtro correspondente;
8. Nova funcionalidade para cadastro de avisos no Controle de Processos e no Painel de Controle;
9. Melhorias na acessibilidade com novas teclas de atalho e tela descritiva disponível por meio de ícone na barra superior;
10. Novo relatório para os administradores com os processos que tramitaram pelo SEI Federação;
11. Melhoria no gerenciamento de Grupos de Blocos exibindo um resumo do uso e facilitando a exclusão;
12. Agora ao acessar uma funcionalidade na árvore de processo os demais botões do protocolo permanecem visíveis. Antes os botões sumiam sendo necessário clicar novamente no processo ou documento para escolher outro botão;
13. Em dispositivos móveis foi adicionada navegação por pastas e um ícone flutuante que permite navegar entre a árvore e o detalhe do protocolo selecionado;
14. Adicionado menu para cópia de dados da unidade na árvore de processo (ao clicar na sigla da unidade associada com o documento);
15. Possibilidade de limitar quais órgãos podem pesquisar em determinado órgão (opção “Restringir pesquisa interna aos órgãos informados” no cadastro de Órgão);
16. Aumento no tamanho do texto de marcadores para até 500 caracteres;
17. Aumento no tamanho do nome de tipos de documento para até 100 caracteres;
18. Novo script para remoção de versões de documentos assinados permitindo liberar espaço na base de dados;
19. Novo parâmetro ID_PAIS_BRASIL permitindo parametrizar esse valor em instituições que não utilizam a tabela de países disponibilizada na base padrão;
20. Adicionadas novas opções para o mecanismo de Captcha no SIP/SEI;
21. No SIP: adicionada possibilidade de sinalizar perfis que requerem autenticação em dois fatores;
22. No SIP: permitido cadastramento de pausa na autenticação em dois fatores para os usuários (ex.: perda, roubo ou esquecimento do celular);
23. No SIP: adicionado cadastro manual do código QR para habilitação da autenticação em dois fatores (quando não é possível ler o código QR com a câmera);
24. No SIP: o perfil “Cadastro de Usuários e Unidades” agora também permite controlar bloqueios de usuários e pausas no 2FA;
25. Novas telas alternativas para configuração dos sistemas SEI/SIP (menu Infra/Configuração do Sistema) com descrição dos valores possíveis para os parâmetros.

**Variáveis, Web Services e API de Módulos**:
26. Nos modelos de documento agora é possível referenciar individualmente os dados dos 3 primeiros interessados ou destinatários (ex.: @nome_interessado@, @nome_interessado_2@, @nome_interessado_3@, @cpf_interessado@, @cpf_interessado_2@, @cpf_interessado_3@, ...);
27. Os e-mails da unidade também podem ser referenciados pela ordem de cadastro @email_unidade@, @email_unidade_2@ e @email_unidade_3@;
28. Outras variáveis adicionadas: @email_usuario@, @numero_passaporte_destinatario@, @pais_passaporte_destinatario@, @titulo_destinatario@, @titulo_abreviatura_destinatario@, @funcao_destinatario@, @categoria_destinatario@, @artigo_orgao_minuscula@, @artigo_orgao_maiuscula@, @cnpj_orgao@, @endereco_orgao@, @cep_orgao@, @sigla_uf_orgao@, @hifen_bairro_orgao@, @complemento_endereco_orgao@ e @cidade_orgao@;
29. Ao informar interessados, remetentes e destinatários é possível utilizar os novos atributos IdContato, Cpf e Cnpj;
30. Na geração de documentos foi adicionada possibilidade de informar o conteúdo para seções específicas do documento;
31. Na geração de documento a estrutura Documento contém os novos atributos opcionais DinValor, ConteudoSecoes e IdItemEtapa;
32. A consulta de documentos aceita novo parâmetro SinRetornarBlocos (retorna os blocos que contém o documento na unidade) e na estrutura RetornoConsultaDocumento foram incluídos os novos atributos DinValor e Blocos;
33. Na geração de processo a estrutura Procedimento contém novo atributo IdTipoPrioridade;
34. Na consulta de processos a estrutura RetornoConsultaProcedimento contém o novo atributo TipoPrioridade;
35. No serviço listarTiposProcedimento foi adicionado parâmetro SinIndividual (retorna apenas os tipos de processos sinalizados como únicos no órgão por usuário interessado);
36. Novos serviços/operações: listarTiposPrioridade, concluirBloco, reabrirBloco e devolverBloco;
37. Novos eventos: alterarProcesso, alterarDocumento, validarEliminacaoProcesso, eliminarProcesso, validarEliminacaoDocumento, eliminarDocumento, desativarUsuario, reativarUsuario, validarContato, substituirContato, verificarAcessoTipoContato, montarMenuConsultaProcessual, processarPesquisaRapida, tratarLinkSemAssinatura e processarPaginaInclusaoDocumentoItemEtapa.

## Versão de Atualização 4.1.1

1. Adicionado tratamento para falha dos navegadores Chrome/Edge 116 ao exibir estilos no editor;
2. Corrige erro gerando base de conhecimento (“Seção do documento não permite alteração do seu conteúdo.”);
3. Não estava considerando o campo de valor monetário dos documentos ao duplicar processo;
4. Corrige filtro por sinalizador de valor monetário na tela de tipos de documento;
5. Corrige erro eventual ao assinar documento com Nome Social (“Nome possui tamanho superior a 100 caracteres.”);
6. Corrige erro cadastrando Contato de outro país ao informar novo Estado ou Cidade;
7. Melhoria na pesquisa por assinantes, interessados, remetentes e destinatários quando existem múltiplos registros para a mesma pessoa. Nesta situação o sistema passou a agrupar automaticamente todas as ocorrências para efetuar a busca;
8. Corrige limitação de tamanho em alguns campos da tela Infra/Configuração do Sistema;
9. Adicionado novo script aplicar_controle_interno.php que remonta os acessos aplicando os critérios de controle interno cadastrados. Deve ser utilizado caso ocorra algum erro no cadastro de critérios. Esta operação pode ser demorada e recomenda-se que seja executada em horário com menor uso do sistema. Também é recomendado executar posteriormente o agendamento indexacao_controle_ interno.php para que as alterações tenham reflexo na pesquisa;
10. Corrige erro acessando os web services listarMarcadoresUnidade e listarAndamentosMarcadores (failed to open stream: No such file or directory);
11. Corrige erro eventual no script de atualização de versão (“Consulta retornou mais de um registro de ITEM_MENU”);
12. Corrige erro no relatório de processos do SEI Federação em bases SQL Server;
13. Corrige erro instalando módulos (“Call to undefined method Banco::setBolScript”).

## Versão de Atualização 4.1.2

1. Ao cancelar um documento passou a remover automaticamente da lista exibida no Plano de Trabalho;
2. Adicionadas variáveis de documento valor e valor_extenso para uso com modelos do editor;
3. Adicionada validação para evitar cancelamento de documento com assinatura externa liberada;
4. Corrige erro gerando publicação relacionada para documentos associados com Plano de Trabalho;
5. Na tela de Avaliação Documental não estava carregando assuntos dos documentos do processo para escolha;
6. Agora mostra o campo Nome na Árvore na lista de documentos disponível no acesso externo;
7. Corrige erro eventual no cadastramento de documento externo indicando que o nome do anexo possui acentos;
8. Corrige erro excluindo documento externo com autenticação;
9. Corrige falha na gravação do log para alguns erros gerados por módulos.

## Versão de Atualização 4.1.3

1. Adicionado tratamento para dispositivos móveis na tela de cadastro de Usuários Externos. Alterada também a sinalização para preenchimento do campo Nome Social;
2. Corrige falha nas estatísticas quando os andamentos dos processos possuem a mesma data/hora de execução;
3. Corrige validação de número de processo já existente quando informando o número na geração;
4. Corrige falha na exibição da barra de progresso no upload de arquivos;
5. Corrige erro aplicando histórico de unidade em bases PostgreSQL;
6. Adicionados pontos de extensão na API de módulos para tratamento de Hipóteses Legais;
7. Corrige erro incluindo documento por web services quando informando identificador de arquivo;
8. Corrige limitação de caracteres em alguns campos da tela de configuração do sistema SIP.

## Versão de Atualização 4.1.4

1. Permite cadastramento de feriado associado com o órgão mesmo que ele não possa realizar publicações;
2. Não estava permitindo o cancelamento de documento assinado por usuário externo quando a liberação para assinatura foi concedida sem acesso ao processo;
3. Corrige erro consultando andamento em processo restrito sem acesso (se o parâmetro que permite a consulta estiver ligado);
4. Ao informar hipótese legal, na geração de protocolos por meio de web services, estava obrigando o cadastro de uma sugestão de hipótese no tipo de processo correspondente;
5. Corrige falha na indexação para pesquisa que, em algumas situações, pode gerar erro ou não indexar determinados metadados.

## Versão de Atualização 4.1.5

1. Melhorias no envio de e-mail para tentar evitar a criação do documento na árvore de processo se ocorrer algum erro no servidor de e-mails da instituição;
2. Removida restrição, em processos recebidos pelo SEI Federação, que limitava novo envio para o federação somente para as unidades do órgão que recebeu o processo;
3. Corrige acessibilidade para leitores de tela em campos do tipo caixa/opção de seleção;
4. Corrige erro excluindo documento com cancelamento de liberação para assinatura externa com permissão para inclusão de documentos;
5. Corrige erro na Inspeção Administrativa ao utilizar a opção "Tipos de processos em tramitação por órgão" em bases SQL Server.


# Versão Principal 4.0.0

**Dependências tecnológicas importantes**:
	- Sistema Operacional Linux
	- Apache 2.4.6
	- PHP 7.3.12
	- Solr 8.2.0
	- Funcionamento em bancos de dados: MySQL, SQL Server, Oracle ou PostgreSQL
		- PostgreSQL foi adicionado nesta versão

1. Interface renovada com maior acessibilidade em dispositivos móveis;
2. SEI Federação mecanismo para compartilhamento de processos entre instituições;
3. Painel de Controle para possibilitar uma visão resumida e personalizada;
4. Adicionado filtro por tipo de processo no Controle de Processos com possibilidade de combinação com os outros filtros;
5. Marcadores
	a. Permitido mais de um Marcador em processo;
	b. Incluídas 22 novas opções de cores para marcadores;
	c. Botões para adicionar e remover marcadores no Controle de Processos;
6. Acompanhamento Especial
	a. Permitido mais de um acompanhamento em processo;
	b. Adicionado botão no Controle de Processos para inclusão em lote;
	c. Adicionado botão “Alterar Grupo” na lista de acompanhamentos permitindo alteração em lote;
	d. Adicionada pesquisa por palavras-chave;
	e. Agora aceita também processos sigilosos;
	f. Campo Observação de Acompanhamento Especial foi aumentado para 500 caracteres;
	g. Campo Nome de Grupo de Acompanhamento Especial foi aumentado para 100 caracteres;
7. Blocos
	a. Possibilidade de atribuição para um usuário;
	b. Sinalizações para priorização, revisão e inclusão de comentários;
	c. Inclusão em grupos de blocos;
	d. Adicionado botão “Incluir em Acompanhamento Especial” na tela de listagem de processos de Blocos Internos;
	e. Adicionado botão “Incluir e Disponibilizar” na tela de inclusão de documentos em bloco;
8. Nova funcionalidade para controle de prazos em processos na unidade;
9. Nova funcionalidade para inclusão de comentários em processos e documentos;
10. Filtro Linha Direta permite exibir na árvore de processo apenas os protocolos gerados por unidades que tiveram comunicação direta com a unidade atual (enviaram o processo para ela ou que ela enviou);
11. Documento Externo
	a. Campos separados para “Número” e “Nome na Árvore” (as informações já cadastradas ficaram gravadas no campo Nome na Árvore);
	b. Nova opção “Para arquivamento” disponível para documentos digitalizados;
12. Sigilosos
	a. Acervo Global de Sigilosos disponível para administradores do sistema (também substitui o Inventário de Processos Sigilosos sem Credencial Ativa que era acessado pelo menu Relatórios/Processos Sigilosos);
	b. Adicionadas mais informações no resultado do Acervo de Sigilosos da Unidade (Observações e Acompanhamentos Especiais);
	c. Renovação de Credencial deixa o processo em vermelho para o usuário e reabre se necessário;
	d. No gerenciamento de credenciais do processo agora são listadas todas as credenciais e não somente as que o usuário concedeu;
	e. Agora qualquer usuário com credencial no processo pode cassar a credencial concedida para outro usuário na mesma unidade;
	f. Correção: em algumas situações permitia cancelar documento com credencial de assinatura liberada;
	g. Correção: estava permitindo conceder credencial em unidade sem permissão para receber processos;
13. Usuário Externo
	a. No Controle de Acessos Externos adicionadas as opções Ver válidos e Ver expirados;
	b. Incluído Nome Social no formulário de cadastro;
	c. Formulário de cadastro disponível também no idioma inglês;
	d. Agora é possível informar uma data de validade na Liberação para Assinatura Externa;
	e. Na lista de acessos externos liberados foi adicionada uma coluna para indicar a data/hora de visualização pelo usuário externo;
	f. Possibilidade de inclusão de documentos por usuário externo (ver parâmetro SEI_HABILITAR_ACESSO_EXTERNO_INCLUSAO_DOCUMENTO). Os tipos de documento disponíveis para escolha na liberação do Acesso Externo são os sinalizados com a opção “Permitida inclusão por usuário externo”;
14. Pesquisa
	a. Agora é possível recuperar processos filtrando por dados existentes nos documentos (ex.: todos os processos onde um usuário assinou um documento);
	b. Salvamento de critérios de pesquisa;
	c. Campos separados para pesquisa por “Número” ou “Nome na Árvore”;
	d. Adicionado filtro por “Data de Inclusão no SEI” ou “Data do Processo/Documento”;
	e. Agora também é possível informar o número do documento ou do processo no campo "Texto para Pesquisa" (antes só localizava o protocolo pelo campo Nº SEI);
	f. Vai marcar em azul no resultado os processos/documentos já acessados durante a sessão atual do usuário;
15. Contatos
	a. Novos campos no cadastro (nome social, categoria, função, título, telefone residencial e cônjuge);
	b. Novos campos para filtro categoria (categoria e cargo);
	c. Relatórios em formato CSV com escolha de campos para geração;
	d. Melhorias na geração de etiquetas;
	e. No resultado da pesquisa foi adicionada informação indicando se o contato representa um órgão do sistema, unidade do sistema, usuário interno, usuário externo ou usuário externo pendente;
	f. Somente usuários com permissão para alterar Usuários Externos poderão modificar os valores informados nos campos de contato que são replicados do formulário de cadastro de usuário externo (endereço, CPF, RG, ...);
16. Ouvidoria
	a. Incluído Nome Social no formulário;
	b. Agora quando houver uma correção de encaminhamento será enviado um e-mail para o solicitante (ver em e-mails do sistema “Correção de encaminhamento de Ouvidoria”);
17. Adicionado tratamento para “Nome Social” no SIP/SEI (cadastros usuários, contatos, formulário de Ouvidoria, formulário de Usuários Externos, variáveis do editor,...). O nome social, se preenchido, será utilizado em todas as telas do sistema. Apenas na assinatura de documentos constará referência ao nome civil por meio do texto “registrado(a) civilmente como”;
18. Agora é possível configurar o sistema para remover as sinalizações do processo (ícones de atenção e publicação) somente se for acessado pelo usuário para o qual ele está atribuído na unidade (ver parâ-metro SEI_SINALIZACAO_PROCESSO);
19. Marcação em azul para protocolos lidos na árvore de processo;
20. A unidade geradora agora aparece para todos os protocolos da árvore em um elemento destacado;
21. Adicionado botão para gerar PDF em documentos internos;
22. O botão “Cancelar Documento” não será exibido se ainda for possível excluir ou alterar o conteúdo do documento;
23. O botão “Incluir Documento” agora aparece também nas ações do documento;
24. Na tela de envio de processo foi adicionado o campo “Órgão das Unidades” para restringir a pesquisa das unidades destinatárias;
25. No SEI adicionado histórico para siglas/descrições das unidades com reflexo nas consultas de andamentos, publicações e pesquisas;
26. Na lista de Unidades adicionado filtro por Sinalização (Protocolo, Arquivamento, Ouvidoria, ...);
27. Na lista de Tipos de Processo adicionados filtros por Assunto, Sinalização (Exclusivo da Ouvidoria, Interno do Sistema, ...) e Nível de Acesso;
28. Na lista de Tipos de Documento adicionados filtros por Assunto, Tipo de Numeração e Sinalização (Permite Interessados, Permite Destinatários, Interno do Sistema, ...);
29. No cadastro de extensões de arquivos permitidas é possível restringir o uso da extensão apenas pela interface do sistema ou por serviços;
30. Quando houver suspeita de XSS no conteúdo de um documento o sistema passará a exibi-lo no formato PDF. E quando o usuário colar algum conteúdo suspeito o sistema exibirá uma comparação das versões informando, se possível, o trecho do documento com problema;
31. No SIP/SEI adicionada possibilidade de uso de autenticação em 2 fatores (2FA);
32. No SIP/SEI adicionada exibição do último acesso após logar e também consulta dos últimos acessos (clicando no link após o login ou no ícone do usuário na barra superior);
33. No SIP/SEI adicionado tratamento para evitar salvamento de senha pelo navegador;
34. Melhorias no editor do SEI para tratamento de espaços em branco ao colar textos (botões “Colar” e “Colar como texto sem formatação”). Para documentos com estilo de fonte mono espaçada, como o SIAFI, utilizar a colagem sem formatação (CTRL + Shift + V);
35. Na lista de modelos de documentos foi adicionada ação para possibilitar a visualização prévia sem a necessidade de criar um documento;
36. “Modelos Favoritos” mudou para “Favoritos” e permite também a inclusão de processos;
37. Agora os administradores podem cancelar arquivamentos (é necessário que o administrador possua o perfil de arquivamento na unidade);
38. Campo Cargo/Função da Assinatura foi aumentado para 200 caracteres;
39. Campo Descrição de Órgão foi aumentado para 250 caracteres;
40. As assinaturas das unidades agora são agrupadas por órgão;
41. Na árvore de processo agora é possível navegar entre protocolos usando seta acima e seta abaixo;
42. Pesquisa de Auditoria:
	a. Adicionada lupa para auxílio no preenchimento do campo Recurso;
	b. Escolha dos campos de retorno;
	c. Escolha do número de registros por página;
	d. Possibilidade de exportação do resultado para planilha;
	e. Adicionada seção “Complemento” na qual o sistema tenta recuperar automaticamente os registros referenciados usando os identificadores internos auditados (ex.: busca o número do processo/documento referenciado);
43. Novas variáveis no editor: telefone_comercial_unidade, telefone_residencial_destinatario, telefone_comercial_destinatario, telefone_residencial_interessado, telefone_comercial_interessado, titulo_destinatario, titulo_interessado, titulo_abreviatura_destinatario, titulo_abreviatura_interessado, funcao_destinatario, funcao_interessado, categoria_destinatario e categoria_interessado;
44. Alterações nos Web Services e API de módulos do SEI
	a. gerarProcedimento
		- adicionados DataControlePrazo, DiasControlePrazo e SinDiasUteisControlePrazo;
	b. incluirDocumento
		- adicionados NomeArvore e SinArquivamento;
	c. listarExtensoesPermitidas
		- considera as opções “interface” e “serviços” sinalizadas no cadastro da extensão;
	d. listarCidades
		- se listando todas as cidades de um estado retornará primeiro a capital;
	e. listarCargos
		- adicionados ExpressaoTitulo e AbreviaturaTitulo;
	f. atualizarContatos e listarContatos
		- removido TelefoneFixo;
		- adicionados NomeSocial, TelefoneComercial, TelefoneResidencial, Conjuge, Funcao, Titulo, AbreviaturaTitulo, ExpressaoTitulo, IdCategoria e NomeCategoria;
	g. consultarDocumento
		- adicionado NomeArvore;
	h. consultarBloco
		- adicionados SinPrioridade, SinRevisao e UsuarioAtribuicao;
		- novo valor “B” para StaEstado indicando "Recebido" e sinalizado quando o bloco não é da unidade mas foi disponibilizado para ela;
	i. Novos Eventos
		- confirmarAtualizacaoConteudoDocumento;
		- confirmarPublicacao;
		- listarUnidadesEnvioProcesso;
		- montarIconeSistema;
		- obterDiretorioIconesMenu;
		- desativarTipoContato;
		- excluirTipoContato;
		- reativarTipoContato;
		- desativarArquivoExtensao;
		- excluirArquivoExtensao;
		- reativarArquivoExtensao;
	j. Novas Operações
		- definirControlePrazo;
		- bloquearDocumento;
		- registrarOuvidoria;
		- listarTiposProcedimentoOuvidoria.
45. No cadastro de usuário do SIP e no Web Service replicarUsuario foram adicionados campos para Cpf, NomeSocial e Email;
46. O SEI/SIP agora podem ser executados também com bases de dados PostgreSQL (além de MySQL, SQL Server e Oracle).

## Versão de Atualização 4.0.1

1. Ativação da funcionalidade Filtro Linha Direta que permite exibir na árvore de processo apenas os protocolos gerados por unidades que tiveram comunicação direta com a unidade atual (enviaram o processo para ela ou que ela enviou);
2. Agora ao pesquisar por número de processo de outra instalação do SEI Federação vai posicionar no órgão correspondente na árvore de processo;
3. Alterada geração de PDFs para comprimir o conteúdo quando algum elemento não couber na página (antes estava cortando);
4. Melhorias diversas na interface incluindo alteração na abertura de várias janelas para evitar bloqueador de pop-ups;
5. Correção no script de atualização do SIP ao configurar o ícone no item de menu “Estatísticas” do SEI. Para as instituições que já instalaram e onde o ícone ainda não é exibido basta atualizar o cadastro do item de menu: no SIP Menus/Montar, selecionar o menu “Principal” do SEI, localizar o item “Estatísticas” e no cadastro informar no campo “Ícone” o valor “estatisticas.svg” (sem acento);
6. Corrige exibição de comentários de processo em unidades sem acesso ao processo;
7. Corrige alteração de Assinatura de Unidade que, em algumas situações, não exibia a lista de unidades para modificação;
8. Corrige erro gerando gráficos de Pontos de Controle;
9. Corrige link do ícone de ajuda na tela de pesquisa de publicações;
10. Corrige web service consultarDocumento que poderia apresentar erro na integração com algumas aplicações.

## Versão de Atualização 4.0.2

1. Na lista de blocos foram adicionados ícones ao lado das unidades de disponibilização para indicar quais já devolveram e quais estão aguardando devolução;
2. Algumas pesquisas por palavras (Cargos de Assinatura, Tipos de Processo, Tipos de Documentos, Órgãos, Usuários e Unidades) não estavam funcionando no SEI dependendo das configurações do banco de dados;
3. Corrige erro na inclusão de documento por usuário externo com hipótese legal e/ou grau de sigilo obrigatórios;
4. Corrige erro aplicando histórico de unidades que poderia acontecer em algumas situações;
5. Corrige ocorrências de erro processando dados no formulário ao efetuar login;
6. Corrige erro na ativação da autenticação em 2 fatores que poderia acontecer dependendo das configurações do banco de dados;
7. Adicionados novos métodos na API de módulos: montarBotaoLoginExterno, montarBotaoAssinaturaInterno, montarBotaoAssinaturaExterno, verificarLoginExt erno e prepararAssinaturaDocumento.

## Versão de Atualização 4.0.3

1. A tela de pesquisa recebeu melhorias na exibição em dispositivos móveis e agora posiciona automaticamente no início dos resultados;
2. Adicionada possibilidade de cancelar documentos gerados do tipo E-mail;
3. A visualização e alteração de anotações agora exibem o usuário e a data/hora do registro;
4. Adicionados na tela de controle de Numeração de tipos de documento filtros por tipo de documento, órgão e unidade;
5. Estava permitindo enviar processo com acesso externo liberado para inclusão de documentos sem manter aberto na unidade (impedindo o usuário externo de subir documentos). Também passou a considerar apenas os acessos externos não expirados para bloqueio da conclusão na unidade;
6. Alteração para permitir o uso de endereços de e-mail com novos domínios;
7. Corrige erro no editor usando o Chrome que não permitia selecionar células mescladas em tabelas e colar imagens com CTRL+V;
8. Corrige erro aplicando histórico de unidades que poderia acontecer em algumas situações;
9. Corrige erro de acesso negado ao tentar salvar modificações na configuração do Histórico;
10. Corrige erro carregando lista de contatos ao criar novo Grupo de Contatos.

## Versão de Atualização 4.0.4

1. Agora também é possível excluir retornos programados que já foram cumpridos;
2. Adicionada no SIP a possibilidade de cancelar os dispositivos liberados do uso de 2FA (acessar o link "Autenticação em dois fatores" no login e clicar no botão “Cancelar Dispositivos Liberados”);
3. Corrige erro ao visualizar histórico de processo quando a informação Grau de Sigilo é removida;
4. Corrige perda de formatação ao colar conteúdo no editor usando Chrome;
5. Não estava permitindo alterar metadados de processos quando o tipo continha restrição configurada para órgãos e/ou unidades;
6. Corrige erro no script de instalação: “Órgão do usuário não informado.”.

## Versão de Atualização 4.0.5

1. Adicionado campo “Nome na Árvore” também para documentos internos (editor web, e-mail, formulários, ...);
2. Ao gerar arquivo PDF de documento foi adicionado rodapé nas páginas igual ao da geração de PDF de processo;
3. Corrige erro exibindo painel de controle ao selecionar “Ver Minha Seleção” em grupos de blocos e posteriormente desmarcar a exibição de grupos de blocos na configuração do painel;
4. Corrige pesquisa quando utilizando a opção “Com Tramitação na Unidade” para processos/documentos públicos.

## Versão de Atualização 4.0.6

1. Na árvore de processo agora também é exibido o texto da especificação associado com os processos relacionados;
2. Alterada forma de escolha do texto padrão na geração de documento permitindo filtrar por partes do nome;
3. Melhorias na acessibilidade na indicação de qual campo da tela possui o foco;
4. Adicionada barra de rolagem na tela de novidades do sistema;
5. Corrige registro de e-mail na árvore mesmo após exibir mensagem informando que o tamanho dos anexos excedeu o limite configurado;
6. Corrige acessibilidade nos links “+” e “-” das telas de escolha de tipos de processo e documento;
7. Corrige erro visualizando andamentos de processo em alguns dispositivos móveis;
8. Corrige erros eventuais ao gerar PDF de processo/documento;
9. Não estava permitindo alterar o campo Resumo em agendamentos de publicações de veículos internos.

## Versão de Atualização 4.0.7

1. A tela de Conferência de Autenticidade de Documentos recebeu melhorias na exibição em dispositivos móveis;
2. Novo parâmetro opcional SEI_FEDERACAO_NOME_TIPO_PROCESSO (menu Infra/Parâmetros), se configurado com o valor “1” (um) então, ao receber processo pelo SEI Federação, o sistema tentará localizar um tipo de processo que tenha o mesmo nome e que aceite o nível de acesso recebido (caso não encontre utilizará o tipo padrão);
3. Corrige processamento do botão Imprimir, existente em algumas telas, que considerava todo o conteúdo exibido e não apenas os itens selecionados da tabela;
4. Disponibilizado novo web service e novo método na API de módulos chamado “registrarAnotacao” para registro de anotação em processo;
5. Corrige exibição do ícone de menu do sistema SIP em dispositivos móveis;
6. Corrige Estatísticas da Unidade e Desempenho de Processos em bases Oracle com cache configurada para a sequence SEQ_ATIVIDADE.

## Versão de Atualização 4.0.8

1. No SEI Federação agora é possível enviar novamente o processo para órgãos que já possuem acesso. Se o processo estiver concluído na unidade destino, será reaberto automaticamente. Também ficará em vermelho em todas as unidades do órgão destinatário em que estiver aberto;
2. Alteradas as telas de envio de e-mail, geração de PDF e geração de ZIP com a inclusão de lupa para seleção dos documentos (com filtros por número de protocolo, tipo de documento e unidade geradora);
3. Novo captcha mais seguro e acessível nas telas de login, validação de documentos, ouvidoria e usuários externos;
4. Foram adicionadas no Controle de Processos as sinalizações para usuários com acessibilidade ativada: Já acessado, Não recebido e Sigiloso;
5. Melhorias em várias telas no esquema preto alto contraste;
6. Passou a exibir na pesquisa os documentos que tenham sido publicados, mesmo que estejam em processos restritos aos quais o usuário não têm acesso. Antes não mostrava, causando inconsistência entre o número de registros informado e os realmente exibidos. Não há prejuízo, já que todas as informações exibidas são públicas;
7. Corrige exclusão do ícone de alteração (triângulo amarelo) em processos do SEI Federação no Acompanhamento Especial;
8. Corrige exibição indevida do ícone do SEI Federação no Controle de Processos após tentativa de envio.

## Versão de Atualização 4.0.9

1. No SIP os links para ativação/desativação do 2FA e para bloqueio de usuário agora exibem uma tela com um botão para confirmar a operação. Evitando execução indevida pelo usuário ou por mecanismos de varredura de conteúdo;
2. A geração de PDF/ZIP pela árvore do processo agora considera todos os documentos com acesso na unidade. Antes, por exemplo, documentos de outras unidades disponibilizados em bloco de assinatura e que ainda não estavam assinados não eram incluídos;
3. Melhorias na exibição da tela de Pesquisa de Publicações em dispositivos móveis;
4. Corrige realce do texto digitado nas telas de escolha de tipos de processo e documento no esquema preto alto contraste;
5. Corrige visualização de autenticações em documentos externos no esquema preto alto contraste;
6. Corrige processamento do botão Imprimir nas estatísticas da Unidade e da Ouvidoria.

## Versão de Atualização 4.0.10

1. Corrige fechamento automático da janela de assinatura quando assinando por meio da navegação de documentos do bloco;
2. Melhoria no desempenho da visualização de documentos contendo milhares de links para outros documentos;
3. Melhoria na acessibilidade do editor com a inclusão dos nomes dos grupos de botões e das seções do documento para os leitores de tela;
4. Corrige envio de processo pelo SEI Federação quando a instalação destino possui Hipótese Legal configurada como obrigatória para o tipo de processo;
5. Corrige erro consultando processo do SEI Federação que possui processos anexados gerados por outras unidades;
6. Corrige tela de alteração de processo que estava permitindo a escolha de tipos sinalizados como Internos do Sistema;
7. Corrige colagem no editor quando o texto contém estilo para controle automático da numeração de parágrafos;
8. Adicionado tratamento na pesquisa nos campos Número e Nome na Árvore para considerar apenas as letras e números informados (evitando a consulta por partículas quando informados caracteres como ponto, hífen, barra, ...);
9. Novo parâmetro opcional SEI_DATA_CORTE_SINALIZADOR_PARA_ARQUIVAMENTO (formato da data dd/mm/aaaa). Os documentos externos protocolados antes da data escolhida poderão ser arquivados, mesmo que não contenham a marcação "Para arquivamento" sinalizada na tela de cadastro. Esse parâmetro não aceita data futura;
10. Corrige erro, em algumas situações, ao listar protocolos de blocos em bases SQL Server.

## Versão de Atualização 4.0.11

1. O botão para inclusão de nova tabela no editor passou a criar a tabela centralizada e com bordas finas;
2. Melhoria na funcionalidade “Limpar Formatação” de tabelas no editor que agora deixa a tabela centralizada e com bordas finas (item disponível no menu exibido ao clicar com o botão direito sobre a tabela);
3. Melhorias na aplicação de estilos em células de tabelas do editor para evitar perda de outras formatações;
4. Corrige funcionalidade do botão “Remover Formatação” do editor que, em algumas situações, não removia todos os estilos do conteúdo selecionado prejudicando nova formatação do texto;
5. Adicionados novos atalhos no editor CTRL+SHIFT+L (inserir um link para processo ou documento) e CTRL+SHIFT+X (inserir texto padrão);
6. Corrige exibição de campos na tela de Pesquisa quando selecionada opção “Processos” com o sinalizador “Considerar Documentos” desmarcado (nesta situação exibia campos que não eram considerados na busca);
7. Corrige erro ao imprimir etiquetas de localizadores e contatos;
8. Corrige erro, em algumas situações, ao indexar os metadados de protocolos.

## Versão de Atualização 4.0.12

1. Adicionado tratamento para falha dos navegadores Chrome/Edge 116 ao exibir estilos no editor;
2. Corrige erro eventual ao assinar documento com Nome Social (“Nome possui tamanho superior a 100 caracteres.”);
3. Corrige erro cadastrando Contato de outro país ao informar novo Estado ou Cidade;
4. Melhoria na pesquisa por assinantes, interessados, remetentes e destinatários quando existem múltiplos registros para a mesma pessoa. Nesta situação o sistema passou a agrupar automaticamente todas as ocorrências para efetuar a busca;
5. Adicionado novo script aplicar_controle_interno.php que remonta os acessos aplicando os critérios de controle interno cadastrados. Deve ser utilizado caso ocorra algum erro no cadastro de critérios. Esta operação pode ser demorada e recomenda-se que seja executada em horário com menor uso do sistema. Também é recomendado executar posteriormente o agendamento indexacao_controle_ interno.php para que as alterações tenham reflexo na pesquisa;
6. Corrige erro acessando os web services listarMarcadoresUnidade e listarAndamentosMarcadores (failed to open stream: No such file or directory);
7. Adicionado tratamento no script de atualização quando ocorrer erro processando andamentos de marcadores (ao alterar a coluna andamento_marcador.sta_operacao para not null).


# Versão Principal 3.1.0

**Dependências tecnológicas importantes**:
	- Sistema Operacional Linux
	- Apache 2.4.6
	- PHP 5.6.5
	- Solr 6.1.0
	- Funcionamento em bancos de dados: MySQL, SQL Server ou Oracle

1. Novo componente para assinatura com Certificado Digital;
2. Na pesquisa foram adicionadas opções para busca em processos ou documentos;
3. Adicionada opção Estrangeiro no formulário de usuários externos. Neste caso são apresentados os campos Número do Passaporte e País de Emissão no lugar de CPF, RG e Órgão Expedidor;
4. O parâmetro SEI_HABILITAR_NUMERO_PROCESSO_INFORMADO agora permite também a alteração do número de processo e da data de autuação (serão lançados andamentos para registro das alterações);
5. Agora também será lançado um andamento quando houver alteração no tipo do processo;
6. Adicionada possibilidade de utilização de links prontos para a tela de pesquisa de publicações permitindo que a tela seja aberta com alguns filtros já aplicados (ver seção Pesquisa de Publicações no documento de instalação);
7. Melhoria nos índices do banco de dados e na pesquisa rápida por número de protocolo;
8. Evolução da API de módulos com novos eventos e operações para tratamento de publicações;
9. Correção: Estatísticas estavam considerando a data dos documentos e não a data de inclusão no sistema;
10. Correção: em algumas situações estava permitindo cancelar documento com credencial de assinatura liberada.

## Versão de Atualização 3.1.1

1. Corrige exibição do caractere apóstrofo em campos do tipo auto completar;
2. Corrige erro ao pesquisar processo que teve o número alterado (ver documentação do parâmetro SEI_HABILITAR_NUMERO_PROCESSO_INFORMADO). A pesquisa só funcionava pelo número antigo mas o processo era retornado com o número novo. Para ajustar registros anteriores basta acessar o cadastro do processo e pressionar o botão salvar;
3. Estava permitindo agendar publicação em veículos não liberados para o tipo de documento;
4. No Web Service listarContatos e na respectiva operação da API de módulos a pesquisa por Sigla e Nome agora também permite a busca por partículas (LIKE). Neste caso é necessário informar o caractere de filtro “%”;
5. Adicionado método para envio de e-mail em processo na API de módulos e Web Services;
6. Corrige erro no script de atualização do banco de dados para a versão 3.1.0: “VERSAO INSTALADA 3.0.X NAO ENCONTRADA NO CONJUNTO DE VERSOES”.

## Versão de Atualização 3.1.2

1. Na árvore de processo ao clicar no ícone de Acompanhamento Especial, localizado ao lado do número do processo, e alterando o texto do acompanhamento exibia indefinidamente o ícone de aguarde após o salvamento;
2. A funcionalidade para alteração do número do processo estava permitindo alterar também números gerados automaticamente (ver documentação do parâmetro SEI_HABILITAR_NUMERO_PROCESSO_INFORMADO). Após aplicar esta atualização somente números informados manualmente em novos processos poderão ser alterados. Em processos antigos não será mais possível a alteração;
3. Correção no tratamento de alguns caracteres especiais em Texto Padrão que poderiam provocar erro no editor;
4. Melhoria no Controle de Acessos Externos dos usuários externos onde processos com muitos documentos tornavam lento o carregamento da tela;
5. Corrige ordenação ao incluir documento na árvore quando os últimos itens são documentos movidos ou processos desanexados (o novo documento não ficava posicionado no final da árvore);
6. Correção no Web Service de inclusão de documento que em algumas situações estava permitindo a inclusão por unidade que não teve tramitação no processo;
7. No SIP passa a mostrar em laranja permissões que estejam sinalizadas com a opção “Estender permissão às subunidades”;
8. No SIP ao pesquisar permissões administradas ocorria eventualmente perda do filtro pelo campo Perfil;
9. No SIP na tela de montagem de hierarquia estava permitindo a inclusão de unidades desativadas.

## Versão de Atualização 3.1.3

1. Adicionada opção na pesquisa do Acervo de Sigilosos da Unidade para exibir apenas os processos em tramitação na unidade;
2. O parâmetro SEI_HABILITAR_NUMERO_PROCESSO_INFORMADO agora aceita também o valor “3” indicando que qualquer unidade pode gerar processos informando o número e a data de autuação, mas a alteração destes dados fica restrita apenas para unidades de protocolo;
3. Ao responder formulários da ouvidoria estava montando o email do remetente de forma fixa com o formato: [sigla órgão] <naoresponder@[sigla órgão].[parâmetro SEI_SUFIXO_EMAIL]>
	- Agora usará o valor cadastrado no campo “Remetente” do email do sistema “Contato com Ouvidoria” (menu Administração/E-mails do Sistema);
4. Foi realizada uma otimização no script de banco da versão 3.1.0 reduzindo o tempo de processamento. Para instituições com bases de dados muito grandes e que ainda não instalaram a versão 3.1.0 é recomendado aplicar esta atualização sobre os fontes antes de rodar os scripts de banco.

## Versão de Atualização 3.1.4

1. Corrige erro na alteração de processo que estava permitindo informar um interessado duplicado para tipos de processos sinalizados como “único no órgão por usuário interessado”;
2. Adicionada paginação de registros na lista de controle de numerações de documentos;
3. Corrige erro de conexão nos scripts de atualização de sequências do SEI e SIP;
4. Alterações em validações de links externos para maior compatibilidade com módulos.

## Versão de Atualização 3.1.5

1. Corrige validação de e-mails para aceitar domínios com apenas uma letra;
2. Corrige erro ao tentar alterar dados do DOU em publicações já disponibilizadas;
3. Corrige bloqueio na geração de processo com número informado na API de módulos.

## Versão de Atualização 3.1.6

1. Adicionadas novas variáveis no editor @nome_usuario@ e @cargo_usuario@ referentes ao usuário logado;
2. Web Services e API: adicionados nos retornos das consultas de processo e documento os campos NivelAcessoGlobal e NivelAcessoLocal;
3. Alteração na desativação de Contato para remover de grupos somente após o processamento da operação pelos módulos instalados;
4. Corrige erro ao disparar a indexação de critérios de controle interno em bases SQL Server;
5. Corrige erro ao atualizar versões de módulos indicando que as versões não são compatíveis.

## Versão de Atualização 3.1.7

1. Corrige erro na geração de PDF contendo documentos do Office;
2. Corrige web service consultarDocumento que poderia apresentar erro na integração com algumas aplicações;
3. Corrige alinhamento de alguns campos da interface nas versões mais novas do navegador Chrome.


# Versão Principal 3.0.0

**Dependências tecnológicas importantes**:
	- Sistema Operacional Linux
	- Apache 2.4.6
	- PHP 5.6.5
	- Solr 6.1.0
	- Funcionamento em bancos de dados: MySQL, SQL Server ou Oracle
	- Nesta versão foi disponibilizada API e Manual para desenvolvimento de Módulos integrados ao SEI para agregar novas funcionalidade sem alterar o código do sistema

1. Liberada interface de programação de módulos possibilitando que as instituições desenvolvam novas funcionalidades sem alteração no código do sistema;
2. Adicionados "Marcadores" para uso na tela de Controle de Processos facilitando o gerenciamento pela unidade;
3. Adicionada opções de navegação na visualização de documentos que estão em blocos de assinatura;
4. Adicionado campo para filtro do tipo de processo e documento nas telas de geração de processo e inclusão de documento;
5. Nova funcionalidade para geração dinâmica de formulários com tratamentos para diversos tipos de campos: datas, moedas, números, textos simples, textos com máscaras, múltiplas opções, sinalizadores,...(menu Administração/Tipos de Formulários);
6. Novo perfil "Coordenador do Acervo de Sigilosos" possibilitando a consulta de todos os processos sigilosos na unidade (menu "Relatórios/Acervo de Sigilosos da Unidade"). Por meio deste relatório será possível ativar credencial em processos sem credencial ativa na unidade bem como cancelar as credenciais inativas;
7. Alteração da tela de Pesquisa com adição de novos critérios;
8. Atualização dos arquivos de configuração do mecanismo de pesquisa tornando possível a busca no conteúdo por CPF, CNPJ, datas, etc. Antes a pesquisa considerava cada parte do número informado como itens individuais não retornando corretamente a informação desejada;
9. Nova funcionalidade "Pesquisar no Processo", disponível nas ações do processo ao visualizar a árvore;
10. Agora é possível atribuir e visualizar os Pontos de Controle no Controle de Processos;
11. Adicionadas colunas "Usuário" e "Data/Hora" na tela de lista de Pontos de Controle;
12. Reestruturação da funcionalidade Critérios de Controle Interno com otimização do tempo de aplicação;
13. Na funcionalidade "Ordenar Árvore do Processo" agora é possível mover o último documento diretamente para a primeira posição clicando na seta para baixo. E da mesma forma é possível mover o primeiro documento para a última posição clicando na seta para cima;
14. Adicionado botão "Assinar" no editor web;
15. Nova funcionalidade para comparação de versões dos documentos elaborados com o editor web (disponível na tela de listagem das versões do documento);
16. Em processos sigilosos quando um usuário renunciar as credenciais em um determinado processo isso provocará a anulação das credencias de assinatura não utilizadas que ele tiver naquele processo e unidade. Antes a credencial de assinatura permanecia até que o documento fosse assinado ou que o usuário solicitante cassasse;
17. Agora é possível selecionar no Controle de Processos vários processos sigilosos para execução de operações como atualização de andamento e conclusão;
18. Adicionados botões para Concluir/Reabrir Processo quando visualizando um documento na árvore (não é mais necessário clicar no processo para realizar estas operações);
19. Possibilidade de alterar a anotação em processo clicando diretamente sobre o respectivo ícone no Controle de Processos (não é mais necessário acessar o processo);
20. Adicionada opção para geração de arquivos ZIP no acesso externo de processos;
21. Agora é possível restringir os protocolos que o usuário externo terá acesso na liberação de acesso externo e assinatura externa;
22. Na consulta de acesso externo passam a ser exibidos o número do protocolo, tipo, data de geração e unidade geradora também para protocolos aos quais o destinatário não tem acesso (a visualização do conteúdo estará bloqueada);
23. Aumentado tamanho do campo "Especificação" no cadastro do processo para 100 caracteres;
24. Aumentado tamanho do campo "Nome" no cadastro de textos padrão para 50 caracteres;
25. Agora é possível clicar com o botão direito nos processos do Controle de Processos e solicitar abertura em uma nova janela ou aba;
26. Adicionada funcionalidade "Gerar Circular" que utiliza um documento como base para geração de documentos individuais para cada destinatário. Os novos documentos podem ser adicionados em um bloco de assinatura e enviados para os emails associados com os destinatários. Esta ação estará disponível para o documento na visualização da árvore de processo se o tipo do documento estiver sinalizado para permitir destinatários;
27. Reestruturação da tabela de temporalidade com funcionalidades para criar versões da tabela, cadastrar mapeamentos entre assuntos de diferentes versões e ativação de uma versão sem a necessidade de realizar uma indexação completa de processos e documentos;
28. Nova funcionalidade "Estatísticas de Arquivamento" que permite uma visão completa do acervo de documentos arquivados, desarquivados, recebidos e localizadores utilizados;
29. Liberação do módulo de contatos que possibilita múltiplos cadastros de pessoas físicas e jurídicas dentro do sistema. Para cada Tipo de Contato é possível informar quais unidades podem alterar ou consultar os contatos relacionados. É possível também a criação de Grupos de Contatos da unidade ou institucionais para uso como interessados ou destinatários;
30. Adicionado o editor web na tela de elaboração das Novidades do sistema;
31. Agora é possível definir tamanhos máximos para arquivos externos por extensão cadastrada (menu Administração/Extensões de Arquivos Permitidas);
32. Adicionadas informações de grau de sigilo, hipótese legal e base legal ao passar ou clicar o mouse no ícone de acesso restrito ou sigiloso (chave amarela e vermelha);
33. Agora é possível restringir tipos de processos e documentos a determinados órgãos e/ou unidades;
34. Liberada funcionalidade para "Autenticação de Documentos Externos" (com colaboração do Ministério do Planejamento);
35. Adicionadas versões para as tarjas de assinatura evitando modificação para os documentos já assinados (com colaboração do Ministério do Planejamento);
36. Adicionados os dados de publicação no DJU/DOU no ícone de publicação associado com o documento e no carimbo de publicação ao visualizar o conteúdo. Entretanto ainda não existe integração com estes veículos, os dados são aqueles informados pelo usuário no momento do agendamento no SEI (com colaboração da ANATEL);
37. Correções de vulnerabilidade para ataques de XSS - Cross-Site Scripting (com colaboração do Ministério do Planejamento);
38. Nova variável para geração de NUP "@dv_mod97_base10_executivo_federal_2d@" (contribuição Ministério do Planejamento);
39. Adicionada funcionalidade "Monitoramento de Serviços" que permite identificar as chamadas de Web Services recebidas pelo SEI bem como o tempo médio e individual de execução (menu Administração/Sistemas);
40. Melhorias na geração de estatísticas com diminuição do tempo de processamento;
41. Nova funcionalidade para migração de dados da unidade: acompanhamentos especiais, cargos/funções de assinatura, blocos internos, grupos de contatos, grupos de email, grupos de envio, modelos favoritos e textos padrão (menu Administração/Unidades);
42. Adicionada paginação de registros no Controle de Processos (ver parâmetro SEI_NUM_PAGINACAO_CONTROLE_PROCESSOS);
43. Alterado formato do formulário de contato com a ouvidoria com inclusão do campo opcional "Processos Relacionados (se houver)";
44. Agora é possível inserir um texto HTML personalizado na tela padrão do formulário de ouvidoria (ver parâmetro SEI_MSG_FORMULARIO_OUVIDORIA);
45. Atualização da linguagem PHP utilizada para a versão 5.6;
46. Atualização do mecanismo de pesquisa Solr para a versão 6.1;
47. Atualização da codificação de senhas armazenadas de usuários externos usando o algoritmo bcrypt;
48. Novo atributo opcional do arquivo de configuração PaginaSEI/OrgaoTopoJanela que permite escolher se a descrição exibida no topo da janela será referente a instituição do usuário logado ou a instituição associada com o sistema no SIP;
49. Novo atributo opcional do arquivo de configuração SEI/DigitosDocumento que permite informar a quantidade de dígitos para documentos do SEI (valor padrão 7);
50. Novos atributos opcionais do arquivo de configuração Solr/TempoCommitBasesConhecimento, Solr/TempoCommitPublicacoes, Solr/TempoCommitProtocolos que permitem especificar o tempo máximo que o mecanismo de pesquisa poderá levar para indexar os registros (o valor padrão para bases de conhecimento e publicações é 1 minuto e para processos e documentos 5 minutos);
51. Alterado atributo do arquivo de configuração InfraMail para permitir a configuração de múltiplos servidores de email associados com os domínios dos remetentes. Com isso podem ser evitados erros de spam no recebimento de emails enviados pelo SEI;
52. Novos atributos opcionais dos arquivos de configuração BancoSEI/PesquisaCaseInsensitive e BancoSip/PesquisaCaseInsensitive que, dependendo da configuração do banco de dados, podem melhorar o desempenho em algumas funcionalidades como a pesquisa de interessados;
53. Adicionado campo obrigatório "Formato" no registro de documentos externos com as opções "Natodigital" e "Digitalizado nesta Unidade";
54. Ao cadastrar documento externo se for escolhido um tipo não permitido é mostrado aviso com a lista de extensões permitidas (contribuição ANATEL);
55. Novos parâmetros SEI_TIPO_ASSINATURA_INTERNA e SEI_TIPO_AUTENTICACAO_INTERNA que possibilitam configurar o tipo de assinatura liberada para uso no sistema: somente login/senha, somente certificado digital ou ambas;
56. As opções para pesquisa simples no banco de dados (LIKE) e SQL Server FullTextSearch foram removidas do sistema;
57. Removido suporte para geração/alteração/assinatura de documentos criados com o antigo editor eDoc/Word (a consulta continua ativa). Também foi disponibilizado um script que permite importar os documentos do eDoc/Word para dentro da base de dados do SEI permitindo a desativação completa do componente (ver seção Scripts no documento de instalação);
58. A indexação de processos, documentos, bases de conhecimento e publicações agora podem ser realizadas pela interface ou por meio de scripts no servidor (ver seção Scripts no documento de instalação);
59. Novas variáveis disponíveis para elaboração de modelos: @nome_pessoa_juridica_associada_destinatario@, @cnpj_pessoa_juridica_associada_destinatario@, @cpf_destinatario@, @rg_destinatario@, @orgao_expedidor_rg_destinatario@, @matricula_destinatario@, @matricula_oab_destinatario@, @cnpj_destinatario@, @complemento_endereco_destinatario@, @pais_destinatario@, @email_destinatario@, @sitio_internet_destinatario@, @telefone_destinatario@, @fax_destinatario@, @descricao_documento@, @tipo_processo@, @especificacao_processo@, @observacao_unidade@, @hierarquia_unidade_raiz_sigla@, @hierarquia_unidade_raiz_descricao@, @hierarquia_unidade_superior_sigla@, @hierarquia_unidade_superior_descricao@, @hierarquia_unidade_descricao_quebra_linha@, @hierarquia_unidade_invertida_descricao_quebra_linha@, @link_acesso_externo_processo@;
60. No SIP a tela para cópia de permissões (botão Copiar ao listar Permissões Administradas) agora permite escolher se a unidade destino será informada ou se deverá ser a mesma da permissão original;
61. No SIP agora é possível modificar a ordem de exibição dos órgãos na lista da tela de login (campo Ordem no cadastro do Órgão);
62. Web Services SIP: novos serviços listarPermissao e replicarPermissao;
63. Web Services SEI: novos serviços listarHipotesesLegais, listarTiposConferencia, listarContatos, atualizarContatos, lancarAndamento, listarAndamentos, bloquearProcesso e desbloquearProcesso;
64. Web Services SEI: novos serviços adicionarArquivo e adicionarConteudoArquivo possibilitam particionar o envio de arquivos grandes para uso posterior em documentos externos;
65. Web Services SEI: adicionado no serviço incluirDocumento os atributos IdTipoConferencia e IdHipoteseLegal;
66. Web Services SEI: o serviço incluirDocumento agora aceita que o processo destino seja informado pelo identificador interno (atributo IdProcedimento) ou diretamente pelo número de protocolo (atributo ProtocoloProcedimento);
67. Web Services SEI: adicionado no serviço incluirDocumento o atributo "Campos" referente aos valores de elementos de formulários dinâmicos;
68. Web Services SEI: adicionado parâmetro "SinRetornarCampos" no serviço consultarDocumento;
69. Web Services SEI: no serviço gerarProcedimento foram adicionados os atributos NumeroProtocolo, DataAutuacao e IdHipoteseLegal;
70. Web Services SEI: adicionado atributo "Aplicabilidade" no retorno do serviço listarSeries;
71. CORREÇÃO: apresentava erro na chamada do serviço atribuirProcedimento quando a opção para reabertura do processo era utilizada;
72. CORREÇÃO: na geração de documentos por Web Services não estava validando as configurações "Permite interessados" e "Permite destinatários" do tipo de documento;
73. CORREÇÃO: permitia excluir documento com credencial de assinatura ativa e caso o usuário destinatário da credencial de assinatura renunciasse então processo ficava no Controle de Processos indefinidamente (não era possível renunciar nem concluir);
74. CORREÇÃO: não estava permitindo renunciar credencial na unidade se houvesse documento não assinado e apenas o usuário gerador tivesse credencial além do usuário atual;
75. CORREÇÃO: erro excluindo Tipo de Suporte;
76. CORREÇÃO: dependendo do formato de numeração a pesquisa por número de processos sem informar os zeros a esquerda não estava funcionando;
77. CORREÇÃO: não estava permitindo utilizar o cadastro de feriados internos se nenhum veículo de publicação estivesse cadastrado;
78. CORREÇÃO: em algumas situações não lançava andamento de recebimento do processo na unidade (por exemplo realizando uma atribuição antes de visualizar o processo em vermelho);
79. CORREÇÃO: em algumas situações apresentava erro ao tentar assinar um bloco inteiro de assinatura (clicando na caneta na tela "Blocos de Assinatura");
80. CORREÇÃO: estava permitindo dar ciência em documento gerado não assinado;
81. CORREÇÃO: estava permitindo sobrestar e anexar processos com retorno programado pendente.
82. CORREÇÃO: estava permitindo que unidades de protocolo adicionassem documentos em processos anexados.


# Versão Principal 2.6.0

**Dependências tecnológicas importantes**:
	- Sistema Operacional Linux
	- Apache 2.2.15
	- PHP 5.3.2
	- Solr 4.0.0
	- Funcionamento em bancos de dados: MySQL, SQL Server ou Oracle

1. Nova versão do mecanismo de assinatura digital compatível com o verificador lançado pelo ITI - Instituto Nacional de Tecnologia da Informação (https://verificador.iti.gov.br/);
2. Nova funcionalidade Pontos de Controle que possibilita definir situações para os processos. O cadastramento das situações e a associação com as unidades pode ser realizado pelo Administrador através do menu Administração/Pontos de Controle. Quando a unidade tiver Pontos de Controle associados aparecerá o botão Gerenciar Ponto de Controle na visualização da árvore de processo; Consultas aos processos sinalizados poderão ser feitas por meio do menu principal no item "Pontos de Controle";
3. Botão Incluir Documento no Controle de Processos permite incluir um documento em vários processos simultaneamente. É possível informar um documento pronto ou um texto padrão e, opcionalmente, também pode ser informado um bloco de assinatura para inclusão dos documentos. Os documentos gerados conterão os assuntos sugeridos para o tipo de documento escolhido e os interessados serão os mesmos do processo (caso o tipo de documento permita interessados);
4. Agora para processos em Acompanhamento Especial será exibido um ícone ao lado do número do processo na árvore;
5. No Acompanhamento Especial passam a ser exibidos os mesmos ícones do Controle de Processos ( , , ,...). Os ícones de aviso serão exibidos também para processos que não passaram pela unidade;
6. Novo parâmetro SEI_ACESSO_FORMULARIO_OUVIDORIA, se estiver ativado então apenas a unidade de ouvidoria poderá visualizar o formulário de contato (independente do nível de acesso do processo). Ao lado do formulário será exibido o ícone indicando o acesso limitado;
7. Adicionada opção "Ativar recursos de acessibilidade" no cadastro de usuário. Esta opção muda o conteúdo da dica exibida pelo sistema ao passar o mouse sobre um processo no Controle de Processos (para uso pelos leitores de tela). Foram realizadas também diversas alterações no código do sistema visando uma melhoria da acessibilidade;
8. Novo menu que agora pode ser acessado também através das teclas de atalho CTRL + ALT + F9 e pode ser navegado com as teclas ←, ↑, →, ↓, ESC e ENTER;
9. Duplicar processo agora permite escolher o Interessado também entre os cadastros temporários e permite também cadastrar automaticamente um nome de interessado inexistente;
10. Unidades de protocolo agora podem cancelar documentos externos inseridos por ela em processos de outras unidades;
11. No cadastro de Usuário Externo alterados os rótulos (Nome -> Nome do Representante, Endereço -> Endereço Residencial);
12. Novas opções na solicitação de Retorno Programado (Data certa, Prazo em dias corridos ou úteis). No caso da escolha em dias úteis, serão desconsiderados sábados, domingos e os feriados cadastrados no SEI ou no sistema de publicação externo (se este estiver configurado como fonte de feriados);
13. Nova funcionalidade "Iniciar Processo Relacionado" que gera um novo processo e relaciona automaticamente. Disponível ao clicar no processo na árvore de processo;
14. Nova funcionalidade "Encaminhar / Reenviar Correspondência Eletrônica" disponível ao clicar em email na árvore de processo;
15. No envio de email adicionada opção "Enviar com cópia oculta", neste caso, o ícone correspondente ao e-mail na árvore de processo ficará com a cor amarela;
16. No envio de email agora aceita colar uma lista de emails usando como separador vírgula "," ou ponto e vírgula ";" (antes aceitava apenas "ponto e vírgula");
17. No editor web adicionadas opções para texto Subscrito e Sobrescrito;
18. Web Services: adicionados parâmetros DiasRetornoProgramado e SinDiasUteisRetornoProgramado nos serviços gerarProcedimento e enviarProcesso;
19. Web Services: adicionado novo serviço consultarBloco;
20. Web Services: adicionado novo serviço cancelarDocumento;
21. Alterado tamanho da descrição das unidades de 100 para até 250 caracteres;
22. No cadastro de Tipos de Processo foi aumentado tamanho do campo Nome para até 100 caracteres;
23. No cadastro de Tipos de Documento adicionado campo "Interno do sistema". Tipos com esta marcação não estarão disponíveis para escolha pelo usuário e somente poderão ser gerados através de Web Services;
24. Adicionado suporte para uso de IPv6;
25. Melhorias diversas no acesso ao banco de dados com diminuição do número de conexões abertas por usuário;
26. CORREÇÃO: unidades configuradas como Protocolo conseguiam gerar PDF/ZIP de processos Restritos de outras unidades;
27. CORREÇÃO: adicionado tratamento para senhas contendo caracteres especiais;
28. CORREÇÃO: em algumas situações apresentava erro ao cadastrar seção em modelo de documento;
29. CORREÇÃO: não deixava concluir o processo na unidade se existisse retorno programado pendente para uma unidade desativada;
30. CORREÇÃO: em algumas situações poderia ocorrer erro ao retirar e após adicionar novamente uma unidade na hierarquia;
31. CORREÇÃO: enviando processo para uma unidade onde ele já se encontrava aberto e atribuído, no Controle de Processos ele era exibido em vermelho mas não era mostrado o usuário de atribuição (após clicar no processo a informação de atribuição voltava a aparecer);
32. CORREÇÃO: ao desativar unidade não estava retirando dos Grupos de Envio;
33. CORREÇÃO: não estava deixando duplicar processos com mais de uma observação de unidade registrada;
34. CORREÇÃO: cancelamento de agendamento de publicação em uma unidade configurada como Protocolo provocava fechamento do processo na unidade;
35. CORREÇÃO: ao alterar a descrição ou liberar uma base de conhecimento estava ocorrendo perda do valor da seção título no respectivo documento;
36. CORREÇÃO: na duplicação de processo se a ordem dos documentos do processo original tivesse sido alterada manualmente isso não era refletido no novo processo (era considerada a ordem original de inserção dos documentos);
37. CORREÇÃO: alterações no mecanismo de indexação para evitar deadlocks no banco de dados quando o SOLR apresentar lentidão;
38. CORREÇÃO: não estava deixando alterar os dados cadastrais de documentos externos com ciência;
39. CORREÇÃO: em algumas situações, nas instalações utilizando banco SQL Server, eram registrados no Log do SEI erros no cálculo da velocidade de transferência de arquivos;


# Versão Principal 2.5.0

**Dependências tecnológicas importantes**:
	- Sistema Operacional Linux
	- Apache 2.2.15
	- PHP 5.3.2
	- Solr 4.0.0
	- Funcionamento em bancos de dados: MySQL, SQL Server ou Oracle

1. No cadastro de órgãos e unidades do SEI foram adicionados os campos “Código SIP” e “Código SEI”. Novas variáveis relacionadas com estes campos foram adicionadas dando mais flexibilidade para formação do número de processo. Uma possibilidade é que várias unidades tenham o mesmo “Código SEI” e assim compartilhem um seqüencial específico dentro do órgão;
2. No cadastro de unidades foi adicionada marcação para indicar unidade de protocolo (pode haver mais de uma no mesmo órgão). Unidades de protocolo podem, por exemplo, inserir e pesquisar documentos em processos de outras unidades (exceto sigilosos). Além disso, vários parâmetros adicionados nesta versão podem ser configurados para aplicação apenas nestas unidades;
3. A formatação do código de assuntos agora pode ser personalizada (ver Roteiro de Instalação, Tabela de Parâmetros SEI, parâmetro SEI_MASCARA_ASSUNTO). Campo “Classificação CJF” foi removido do cadastro de Assuntos;
4. Na tela de geração de processo é possível informar o número do processo e a data de autuação (ver Roteiro de Instalação, Tabela de Parâmetros SEI, parâmetros SEI_HABILITAR_NUMERO_PROCESSO_INFORMADO e SEI_MASCARA_NUMERO_PROCESSO_INFORMADO);
5. Adicionada funcionalidade para “Anexação de Processos”. O processo anexado terá sua tramitação bloqueada e ficará como um documento no processo principal (não aplicável a sigilosos);
6. No editor web adicionado botão “Inserir um link para processo ou documento do SEI!”. Na árvore de processo, ao ler um documento, bastará clicar no link para que o processo ou documento referenciado seja aberto em outra janela;
7. Liberada assinatura para Documentos Externos. A assinatura de externos continua opcional, ou seja, um documento não assinado continuará sendo visto pelas demais unidades. Mas se o documento externo for assinado poderá ficar com a “caneta preta” não sendo mais possível alterar o seu conteúdo (ver Roteiro de Instalação, Tabela de Parâmetros, parâmetro SEI_HABILITAR_ASSINATURA_DOCUMENTO_EXTERNO);
8. Adicionada funcionalidade “Mover Documento para outro Processo” (ver Roteiro de Instalação, Tabela de Parâmetros, parâmetro SEI_HABILITAR_MOVER_DOCUMENTO);
9. Relatório de Desempenho Gerencial, informando, dentre outras coisas, o tempo médio dos tipos de processos por unidade;
10. Na tela de iniciar processo alterado rótulo “Tipo” por “Tipo do Processo”;
11. Alterado rótulo “Série” por “Tipo de Documento” nas telas e itens de menu correspondentes;
12. Nas telas de cadastro e alteração de processo alterado rótulo “Assuntos” por “Classificação por Assuntos”;
13. Adicionada sugestão de classificação por assuntos para os tipos de documento. Adicionado também no cadastro de documento o campo opcional “Classificação por Assuntos” (virá preenchido com as sugestões cadastradas para o tipo do documento);
14. Em adequação a LAI (Lei de Acesso à Informação) adicionada possibilidade de informar o Grau de Sigilo e a Hipótese Legal associada com a restrição de acesso (ver Roteiro de Instalação, Tabela de Parâmetros SEI, parâmetros SEI_HABILITAR_GRAU_SIGILO e SEI_HABILITAR_HIPOTESE_LEGAL). As hipóteses legais podem ser cadastradas no SEI através do menu Administração/Hipóteses Legais;
15. Em adequação a LAI (Lei de Acesso à Informação) foi alterada denominação do nível de acesso “Reservado” para “Restrito”. Nenhuma alteração com relação ao comportamento foi realizada;
16. Liberação de Assinatura Externa passou a informar a Data/Hora de utilização pelo usuário externo. Agora também é possível cancelar o acesso ao processo após a assinatura (se a liberação para assinatura incluía acesso ao processo);
17. Adicionada possibilidade de desativar o envio de emails automáticos do sistema (no SEI menu Administração/E-mails do Sistema);
18. No cadastro de unidades agora é possível indicar mais de uma unidade de arquivamento no mesmo órgão;
19. Na pesquisa de publicações foi adicionado o campo de filtro “Veículo”;
20. Alterado texto do carimbo de publicação do documento para constar as datas de disponibilização e publicação;
21. No cadastro de documentos externos foi adicionado campo “Tipo de Conferência”. Esta informação é lançada no andamento do processo;
22. No campo Interessado/Remetente da pesquisa do SEI passou a mostrar os nomes cadastrados através de serviços como a Ouvidoria;
23. Alterado ícone de relacionamentos do processo;
24. Adicionada funcionalidade para consulta de assinaturas nos documentos. Tela restrita aos administradores permite baixar o conteúdo assinado e os arquivos para validação da assinatura digital;
25. Manual de instalação: vários tópicos foram mais detalhados e outros adicionados. É recomendada a leitura, mesmo que superficial, do manual de instalação (inclusive para instituições que já utilizam plenamente o sistema);
26. Removido suporte ao GSA (Google Search Appliance);
27. Web Services: Padronização do serviço para consulta de cargos/funções de assinatura do usuário no RH. Permite preencher automaticamente a caixa “Cargo/Função” na tela de assinatura (ver documentação de WebServices, item Serviços Acessados em outros Sistemas);
28. Web Services: adicionado campo opcional Especificação na geração de processos;
29. Web Services: no agendamento de publicações em veículos externos o campo DescricaoTipoDocumento mudou para NomeTipoDocumento e o campo DescricaoVeiculoPublicacao mudou para NomeVeiculoPublicacao;
30. CORREÇÃO: na tela de pesquisa, usando Solr, os operadores “e”, “ou” e “não” não estavam funcionando nos campos “Especificação/Descrição” e “Obs. desta Unidade”;
31. CORREÇÃO: tela de “Acompanhamento da Ouvidoria” apresentava erro se a base de dados era SQL Server;
32. CORREÇÃO: impressão de etiquetas de arquivo no Chrome e Firefox apresentava erro;
33. CORREÇÃO: em determinadas situações ao trocar o tipo de processo utilizando o teclado o sistema não realizava a troca;
34. CORREÇÃO: tratamento de caracteres especiais (como “&”) em diversas telas do sistema. Estes caracteres causavam quebra da página no Firefox, Chrome e IE 9 ou superior;
35. CORREÇÃO: em algumas instalações ao digitar ENTER no editor web era exibido o caracter “Â”;
36. CORREÇÃO: adicionado filtro para caracteres ISO-8859-1 em diversas telas do sistema (anotações de processos, acompanhamento especial, anotações de blocos, ...). Eventualmente, ao colar textos nestes campos, caracteres especiais poderiam ser gravados provocando quebra da página no Firefox, Chrome e IE 9 ou superior;
37. CORREÇÃO: nas estatísticas da unidade ao utilizar como final do período um dia no passado alguns processos com tramitação ou conclusão neste último dia poderiam não entrar no cálculo;
38. CORREÇÃO: a pesquisa de publicações não funcionava para órgãos com ID maior que 9.

## Versão de Atualização 2.5.1

1.	No controle de processos o ícone   passa a ser exibido quando um documento externo for incluído ou quando um documento (interno ou externo) for assinado. Antes, ao gerar um documento interno o ícone aparecia, entretanto no acesso ao processo ainda não era possível a visualização do conteúdo;
2.	Na geração de PDF do processo passou a incluir o cabeçalho e rodapé para os documentos gerados;
3.	No cadastro de assuntos o tamanho do campo “Código” foi alterado de 14 para até 50 caracteres;
4.	No cadastro de documentos externos foi adicionado um novo campo “Reabrir processo nas unidades” permitindo reabrir o processo em unidades cuja tramitação já esteja concluída. Este campo está disponível apenas para unidades configuradas como Protocolo e somente para processos de outras unidades (se o processo já tramitou pela unidade de protocolo o campo não irá aparecer). Os processos serão reabertos nas unidades selecionadas ficando no Controle de Processos com a cor vermelha acrescidos do ícone de exclamação;
5.	Ao gerar um processo deixou de atribuir automaticamente para o usuário gerador;
6.	Adicionada a possibilidade de uso de imagens no editor web. Para que o ícone   apareça na barra de ferramentas pelo menos um tipo de imagem deve ser cadastrado através do menu Administração/Editor/Formatos de Imagem Permitidos. Entretanto o uso de imagens em alta resolução, ou formatos com pouca ou nenhuma compressão como o TIFF e o BMP, podem deixar o editor lento. Esta funcionalidade estará disponível para os navegadores Firefox, Chrome e Internet Explorer 8, 9 ou 10;
7.	Adicionado cálculo da taxa de transferência de dados por usuário possibilitando evitar o início automático de downloads para usuários com taxas de transferência baixas (ver Roteiro de Instalação, seção Tabela de Parâmetros SEI, parâmetro SEI_NUM_FATOR_DOWNLOAD_ AUTOMATICO);
8.	Adicionados novos agendamentos no SIP que permitem forçar a replicação de todos os usuários e unidades para o SEI (menu Infra/Agendamentos, itens replicarTodosUsuariosSEI e ReplicarUnidadesHierarquiaSEI). Os usuários cadastrados no SIP serão replicados mesmo que não tenham permissão no sistema SEI (com isso estarão, por exemplo, disponíveis para escolha como interessados e para assinatura de documentos). Com este agendamento ativo bastará que o sistema de RH da instituição chame o Web Service de replicação de usuários do SIP para que os usuários apareçam ou saiam do SEI. Estes novos agendamentos foram criados inicialmente desabilitados (ver Roteiro de Instalação, seção Carga e Sincronização de Usuários e Unidades);
9.	Agora se o SIP estiver configurado para uso com HTTPS então o sistema irá forçar o envio de todas as páginas com este protocolo e não apenas a página de login (ver Roteiro de Instalação, seção HTTPS);
10.	No SEI adicionada opção para configuração do HTTPS. Se ativada então todas as páginas serão enviadas pelo sistema com este protocolo (ver Roteiro de Instalação, seção HTTPS);  
11.	No SIP adicionado novo item de menu “Servidores de Autenticação” permitindo o compartilhamento de servidores entre órgãos da mesma base. Além disso, foram incluídas facilidades para teste da configuração e modificações que possibilitam autenticar mesmo sem realizar uma pesquisa prévia do contexto do usuário. (ver Roteiro de Instalação, seção Integração LDAP/AD);
12.	Adicionado suporte para a extensão “Microsoft Drivers for PHP for SQL Server” (aplicável quando o PHP é instalado em plataforma Windows);
13.	Adicionado filtro de conteúdo para documentos gerados via Web Services. O sistema não deixará gerar documentos internos que contenham as tags: script, iframe, frame, embed, object, param, video, audio, button, input e select. A tag img será permitida apenas para os tipos de imagens liberados para uso no editor web (ver item 6 deste documento);
14.	CORREÇÃO: usuários externos com credencial para assinatura em processo sigiloso recebiam mensagem de acesso negado ao documento no momento da assinatura;
15.	CORREÇÃO: no iPad, dependendo da versão do IOS, alguns links para funcionalidades podiam não funcionar. Além disso, a visualização dos documentos na árvore foi modificada permitindo rolar o conteúdo, evitando desta forma que a visualização do documento quebre para a parte de baixo da tela;
16.	CORREÇÃO: em determinadas situações acontecia erro ao informar o número de protocolo na geração de processo se a base de dados fosse SQL Server;
17.	CORREÇÃO: não estava carregando o corretor ortográfico configurado para o órgão na edição de textos padrão;
18.	CORREÇÃO: ao dar ciência ou alterar dados cadastrais de processo estava reenviando para indexação todos os documentos do processo. Isso poderia deixar estas operações lentas em processos com muitos documentos;
19.	CORREÇÃO: em determinadas situações exibia erro ao montar a árvore de processo se o primeiro item era um processo anexado;
20.	CORREÇÃO: exibia erro na alteração da Descrição no cadastro de Tipo de Conferência;
21.	CORREÇÃO: no desarquivamento estava utilizando o órgão do usuário logado para validação da senha do usuário que estava retirando o documento (provocava erro quando um usuário tentava retirar um documento em uma unidade de arquivo em outro órgão);
22.	CORREÇÃO: alterada ordenação para escolha de localizadores na tela de arquivamento;
23.	CORREÇÃO: ao incluir documento gerado, via Web Services, não estava aplicando automaticamente os estilos no documento (ex.: em alguns tipos de documento o título não ficava centralizado em negrito). Os estilos eram aplicados apenas se o usuário abrisse o documento no editor web;
24.	CORREÇÃO: tempo máximo de execução para a operação de indexação completa estava limitado em 3 minutos (o limite de tempo foi removido);
25.	CORREÇÃO: erro na pesquisa de processos, documentos e publicações se utilizando como mecanismo de indexação o banco de dados puro;
26.	CORREÇÃO: erro ao duplicar processo restrito quando o sistema estava configurado para uso obrigatório do campo hipótese legal;
27.	CORREÇÃO: erro na inserção de links para processos/documentos do SEI utilizando o editor com Internet Explorer (funcionava apenas para o primeiro link, sendo necessário salvar o conteúdo, fechar e abrir o editor para adicionar outros links);
28.	CORREÇÃO: problema na concorrência de chamadas para geração de documentos via Web Services;
29.	CORREÇÃO: na geração de PDFs foi adicionado tratamento para arquivos criptografados. Melhorada também a identificação de erros adicionando, em várias situações, a identificação do arquivo apresentou problema;
30.	CORREÇÃO: em determinadas situações podia calcular errado o Digito Verificador para processos do Executivo Federal;
31.	CORREÇÃO: na tela de assinatura de documento ao clicar no ícone   (Instruções para Configuração da Assinatura Digital) exibia erro de Acesso Negado.
32.	CORREÇÃO: formulário da ouvidoria estava limitando o texto da mensagem em 200 caracteres quando deveria ser 2000.

## Versão de Atualização 2.5.2

1. Diversos aprimoramentos nos mecanismos de segurança do sistema com base em um relatório elaborado para o SEI pelo Gabinete de Segurança Institucional da Presidência da República;
2. Adicionado suporte para a base de dados Oracle, com contribuição do Tribunal Regional Eleitoral do Tocantins;
3. Na assinatura digital adicionado tratamento para certificados digitais da cadeia V4;
4. O sistema passou a bloquear a alteração/exclusão de documentos externos visualizados fora da unidade (mesmo que ainda não tenham tramitado);
5. Não é mais possível liberar a assinatura de documentos externos para todas as unidades (parâmetro SEI_HABILITAR_ASSINATURA_DOCUMENTO_EXTERNO=2). Os únicos valores válidos para configuração passam a ser 0 (nenhuma unidade) ou 1 (somente unidades de protocolo);
6. No cadastro de tipos de documento foi adicionado o campo "Aplicabilidade" permitindo escolher se o tipo deve aparecer para escolha na geração de documentos internos, externos ou ambos. Se o tipo for aplicável para documentos internos então será obrigatório informar o modelo associado;
7. No cadastro de Tipos de Processo adicionado tratamento para o campo "Interno do sistema". Tipos com esta marcação não estarão disponíveis para escolha pelo usuário e somente poderão ser gerados através de Web Services;
8. Adicionada a funcionalidade de Grupos de Envio (da unidade e institucionais) que permite a criação de conjuntos de unidades para posterior escolha no envio de processos;
9. No envio de processos agora também é possível selecionar grupos de envio ou unidades por onde o processo já tramitou;
10.Na tela para conferência de autenticidade de documentos foram adicionadas opções para baixar o conteúdo e também os arquivos de assinatura (p7s) para validação externa;
11. Adicionado no SEI o parâmetro SEI_MAX_TAM_MENSAGEM_OUVIDORIA que permite configurar o número máximo de caracteres da mensagem de texto do formulário de ouvidoria;
12. Editor Web:
	- atualização do componente interno CKEditor versão 4.1 para 4.4;
	- adicionado suporte para o Internet Explorer 11 no Windows 7 e 8;
	- nova tela para inserção de caracteres especiais (botão Ω);
	- atualizado o plugin SCAYT de correção ortográfica corrigindo alguns problemas de desempenho e perda de seleção. Este novo plugin é utilizado automaticamente para o webspellchecker gratuito ou licenciado na versão 3;
	- ao inserir uma nova linha na tabela, os estilos das células novas serão os mesmos usados na linha atual, ou da última linha, caso seja usada a tabulação;
	- ao alterar o estilo de um parágrafo com imagens, a imagem não perde mais as informações de tamanho;
	- inclusão de borda vermelha em torno de objetos não permitidos (após colar e tentar salvar);
	- adicionado tratamento ao copiar/colar entre documentos internos do SEI mantendo a formatação e removendo estilos não permitidos no documento destino.
13. Adicionada funcionalidade para geração de arquivo compactado com os documentos do processo (ZIP);
14. Agora as ações "Enviar Processo" e "Acompanhamento Especial" estão disponíveis também ao clicar em documentos na árvore de processo;
15. Visualizando a árvore de processo ao passar o mouse sobre um processo relacionado agora exibe a sua Especificação (antes exibia o Tipo do Processo);
16. Adicionado campo para pesquisa na tela de seleção de grupos de email;
17. Adicionado o editor web na tela de cadastro de seções de documento. O editor aparecerá se a opção "Conteúdo Inicial HTML" estiver marcada. Para trabalhar diretamente com código HTML clicar no botão "Código-Fonte" disponível no editor;
18. Adicionada opção para desativar seções de um modelo de documento mesmo que já existam documentos utilizando (evitando a necessidade de criação de um novo modelo);
19. No envio de e-mail ao preencher o campo destinatário o sistema agora exibe sugestões dentre os endereços já utilizados pela unidade;
20. Melhorias e ampliação do número de serviços disponibilizados via Web Services (ver arquivo SEI-Web-Services-v2.5.2.doc);
21. Web Services: adicionado suporte para uso de MTOM no envio do conteúdo de documentos, com contribuição da ANATEL (ver arquivo SEI-Web-Services-v2.5.2.doc, seção Estruturas de Dados, Documento);
22. Web Services: alterado serviço gerarBloco, agora se na geração for solicitada também a disponibilização do bloco então será necessário que o serviço também tenha permissão na operação "Disponibilizar Bloco" no SEI;
23. Web Services: alterado serviço gerarProcedimento, agora se na geração for solicitado também o envio do processo para outras unidades então será necessário que o serviço chamador também tenha permissão na operação "Enviar Processo" no SEI;
24. A tela para disparar a indexação manual de processos/documentos/publicações agora passa a ser acessada através do menu (Infra/Indexação);
25. CORREÇÃO: após reindexar todas as publicações os campos Tipo de Documento e Unidade Responsável ficavam vazios na tela de pesquisa de publicações;
26. CORREÇÃO: erro na indexação completa quando o número de processos era menor que 100;
27. CORREÇÃO: em determinadas situações de erro a senha do usuário poderia ser gravada no log de erros do sistema;
28. CORREÇÃO: estava permitindo inserir tipos de processo com nomes repetidos;
29. CORREÇÃO: em alguns tipos de andamento do processo estava montando o texto com uma preposição incorreta, ex.: "Processo atribuído para por xyz";
30. CORREÇÃO: em algumas situações documentos internos do SEI, enviados como anexos de email, eram abertos pelo cliente de email com acentuação incorreta;
31. CORREÇÃO: ao excluir um processo a relação de processos visitados (exibidos em azul no Controle de Processos) era perdida;
32. CORREÇÃO: nas Estatísticas da Unidade ou da Ouvidoria quando o período solicitado era superior a um ano algumas tabelas eram montadas de forma incorreta;
33. CORREÇÃO: Internet Explorer 10 não estava mais deixando os documentos sem acesso com a cor cinza na árvore de processo;
34. CORREÇÃO: Estava permitindo salvar o documento no editor web mesmo se ele estivesse assinado em outra unidade (via bloco de assinatura). Neste caso a assinatura era cancelada sem aviso para o usuário que estava editando o documento;
35. CORREÇÃO: na assinatura de documentos utilizando Firefox com Android passou a exibir o botão "Assinar" pois na digitação da senha o navegador não disponibiliza o ENTER;
36. CORREÇÃO: em determinadas situações, no editor web, se ocorresse um erro ao salvar o documento era exibida apenas uma tela em branco.