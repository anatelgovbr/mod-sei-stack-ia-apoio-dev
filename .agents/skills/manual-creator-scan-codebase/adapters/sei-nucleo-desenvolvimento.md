# Adaptador: Núcleo do SEI para desenvolvimento de módulos

Caminhos relativos à raiz do repositório SEI da Anatel. `<php>` abrevia `fontes/sei/src/main/php` e `<web>` abrevia `<php>/sei/web`. Última conferência: 2026-10-08, árvore de trabalho do branch `adr_spec_docs_stack_ia` sobre a revisão `3f3fdf1f4a`.

## Reconhecimento e alcance

- Nome oficial: `Sistema Eletrônico de Informações` (`<web>/PaginaSEIExterna.php:34` e título da barra em `<web>/PaginaSEI.php:53`). Sigla: SEI.
- Alvo: o núcleo do SEI do ponto de vista de quem desenvolve módulos, isto é, os contratos que o núcleo oferece aos módulos e os padrões que os módulos seguem.
- Alcance: os temas do manual oficial de desenvolvimento de módulos, na ordem do índice `docs/manuais/sei/manual_md/sei_modulos_manual_dev_0_indice.md`: introdução, criação e ativação, considerações prévias, InfraPHP, modelagem de dados, codificação PHP, gerador de código, classes da API, eventos e operações.
- Pistas de inclusão: classe abstrata `<web>/SeiIntegracao.php`, carga dos módulos em `<web>/SEI.php`, trecho de despacho para módulos nos controladores `<web>/controlador*.php` e `<web>/publicacoes/controlador_publicacoes.php`, classes da API em `<web>/api/`, operações em `<web>/rn/SeiRN.php`, InfraPHP em `<php>/infra/infra_php/`, `<php>/sip/web/ScriptSip.php` e os scripts de atualização do núcleo `<php>/sei/scripts/atualizar_versao_sei.php`, `<php>/sip/scripts/atualizar_versao_sip.php` e `<php>/sip/scripts/atualizar_recursos_sei.php`.
- Pistas de exclusão: o código próprio de cada módulo em `<web>/modulos/<modulo>/`, que tem adaptador próprio quando houver manual de uso (por exemplo, `adapters/sei-modulo-apt.md`); o editor em `<web>/editor/`; e os manuais de uso do núcleo para quem opera o sistema, que ficam fora deste alvo.
- Componentes compartilhados: InfraPHP (`<php>/infra/`) e SIP (`<php>/sip/`), lidos quando o tema depende deles, como permissões, recursos, perfis e scripts de versão de módulo.
- Exemplos de implementação: gabaritos `<web>/modulos/abc/exemplo/` (referência mínima) e `<web>/modulos/trf4/julgamento/` (referência robusta). Um evento real implementado aparece em `<web>/modulos/apoio-plano-trabalho/MdAptIntegracao.php:169` (`gerarDocumento`).

## Versão e variante

- Versão do núcleo no código: `SEI_VERSAO = '5.0.5'` e `SEI_RC = ''` (`<web>/SEI.php:14-15`). InfraPHP: `VERSAO_INFRA = '3.1.8'` (`<php>/infra/infra_php/Infra.php:26`).
- Manual oficial disponível: `SEI-Modulos-v5.0` (título em `docs/manuais/sei/SEI-Modulos-v5.0.md:1`), sem indicação de revisão 5.0.x no texto. Ao documentar ou conferir um tema, compare o manual com o código da versão 5.0.5 e registre como divergência o que um descreve e o outro não tem.
- Carga e ativação de módulos: chave `Modulos` do `ConfiguracaoSEI.php`, lida em `<web>/SEI.php:55-71`. O núcleo encerra com mensagem quando falta a classe de integração (`<web>/SEI.php:62-64`) ou quando `getNome`, `getVersao` ou `getInstituicao` voltam vazios (`<web>/SEI.php:75-85`), e dispara o evento `inicializar` com a versão do núcleo (`<web>/SEI.php:87`).
- Idioma: português brasileiro. Identificadores, assinaturas e mensagens são literais no PHP; não há arquivos de tradução.
- Código-fonte não prova a versão implantada. A versão em produção é pergunta ao responsável.

## Leitura da codebase

- Raízes: `<web>` sem `modulos/` e sem `editor/`, `<web>/api/`, `<web>/rn/`, `<web>/publicacoes/`, `<php>/infra/infra_php/`, `<php>/sip/web/`, `<php>/sei/scripts/`, `<php>/sip/scripts/`, `docs/manuais/sei/` e `docs/manuais/sei/manual_md/`.
- Extensões: `.php`, `.js` e `.md`.
- Codificação: o PHP do núcleo, da InfraPHP e do SIP fica em ISO-8859-1 com CRLF na árvore de trabalho (regra `*.php text working-tree-encoding=iso-8859-1` em `.gitattributes:2`). Parte dos scripts antigos abre com `<?`, como `<php>/sip/scripts/atualizar_recursos_sei.php:1`. Os capítulos do manual oficial estão em UTF-8 com CRLF.
- Leitura: `iconv -f latin1 -t utf-8 <arquivo> | tr -d '\r' | cat -n`. Busca: `grep -a` sempre, porque sem `-a` o `grep` desta máquina (ugrep) trata o PHP Latin-1 como binário e devolve vazio. `rg` não está instalado.
- Exclusões comprovadas: `<web>/modulos/` (código de módulos) e `<web>/editor/` (editor de documentos).
- Ferramentas: `grep -a`, `iconv`, `file`, `git`, `python3` e `php -l`.

## Pontes de evidência

- Evento para disparo no núcleo: cada evento é um método público de `SeiIntegracao` com implementação padrão vazia (`<web>/SeiIntegracao.php`), e o núcleo o dispara por `executar('<evento>', ...)` (`SeiIntegracao::executar`, `<web>/SeiIntegracao.php:147`). Busca do ponto de disparo: `grep -arn "executar('<evento>'" <web> --include=*.php | grep -v /modulos/`. Leia o trecho do disparo para saber os parâmetros, o momento da chamada e o uso do retorno.
- Controladores de módulo: `processarControlador`, `processarControladorAjax`, `processarControladorExterno`, `processarControladorPublicacoes` e `processarControladorAjaxExterno` (`<web>/SeiIntegracao.php:83-87`) e `processarControladorWebServices` (`<web>/SeiIntegracao.php:88`). O núcleo os chama no fim do despacho de `<web>/controlador.php:1926`, `<web>/controlador_ajax.php:564`, `<web>/controlador_externo.php:90`, `<web>/publicacoes/controlador_publicacoes.php:46`, `<web>/controlador_ajax_externo.php:34` e `<web>/controlador_ws.php:32`.
- Identificação do módulo: métodos abstratos `getNome`, `getVersao` e `getInstituicao` (`<web>/SeiIntegracao.php:8-10`), exibidos na tela `Módulos` (título em `<web>/modulo_lista.php:28`, colunas `Nome`, `Versão` e `Instituição` em `<web>/modulo_lista.php:49-51`, ação `modulo_listar` em `<web>/controlador.php:1640`).
- Capítulo e código: o capítulo 9 tem uma seção `## <evento>` por evento, comparável aos métodos públicos de `SeiIntegracao`; o capítulo 8 tem uma seção por classe, comparável aos arquivos de `<web>/api/`; o capítulo 10 tem uma seção por operação, comparável às funções de `<web>/rn/SeiRN.php`. Concilie as listas antes de afirmar cobertura de um tema.
- InfraPHP: classes base `InfraDTO.php`, `InfraRN.php`, `InfraBD.php`, `InfraPagina.php`, `InfraSessao.php`, `InfraException.php` e `InfraScriptVersao.php` em `<php>/infra/infra_php/`, referência do capítulo 4.
- Scripts de versão de módulo: `ScriptSip` (`<php>/sip/web/ScriptSip.php`) para recursos, perfis e itens de menu no SIP, e `InfraScriptVersao` (`<php>/infra/infra_php/InfraScriptVersao.php`) para o controle de versões. Os scripts de módulos em `<php>/sei/scripts/` e `<php>/sip/scripts/` são exemplos de uso.
- Permissão: o nome do recurso é o nome da ação; páginas chamam `validarLink` e `validarPermissao`, como em `<web>/procedimento_escolher_tipo.php:23-25`, e a verificação fica em `InfraSessao::validarPermissao` (`<php>/infra/infra_php/InfraSessao.php:884`).
- Corroboração: catálogos derivados dos capítulos 8 a 10 nas skills `sei-mod-api-classes`, `sei-mod-api-eventos` e `sei-mod-api-operacoes` (`.agents/skills/sei-mod-api-*/references/catalogo-*.md`) e padrões do projeto em `.agents/references/padrao-*.md`. São evidência complementar; a prova é o código.
- Amostra de descoberta, evento `gerarDocumento`: declaração em `<web>/SeiIntegracao.php:42`, com parâmetro `DocumentoAPI`; disparo em `<web>/rn/DocumentoRN.php:685`, na gravação do documento gerado; seção `## gerarDocumento` em `docs/manuais/sei/manual_md/sei_modulos_manual_dev_9_eventos.md:364`; implementação real em `<web>/modulos/apoio-plano-trabalho/MdAptIntegracao.php:169`.

## Interface e textos

- Contratos: nome do método, parâmetros, tipos e retorno são literais da declaração em `<web>/SeiIntegracao.php`, nas classes de `<web>/api/` e em `<web>/rn/SeiRN.php`. Quando o manual oficial divergir do código, cite o código e registre a divergência.
- Mensagens: críticas do núcleo por `InfraException` (`adicionarValidacao`, `lancarValidacao`), literais no PHP; mensagens de carga de módulo em `<web>/SEI.php:63`, `76`, `80` e `84`.
- Extensões visíveis: botões, ícones e trechos de tela devolvidos por eventos de montagem aparecem na interface do núcleo, no ponto em que o evento é disparado. Para ilustrar, a captura mostra esse ponto da tela com um módulo de exemplo ativo, e o texto identifica o evento.
- Imagens do manual oficial: `docs/manuais/sei/imagens/imageNNN.*`, referenciadas pelos capítulos com `../imagens/`.
- Rótulos de menu não estão no código. Um caminho de menu só entra no manual com confirmação do responsável.
- Traduções: não aplicável.

## Personas e acesso

| Persona ou público | Objetivo e tarefas | Conhecimento relevante | Perfil e restrições | Fonte e confirmação |
|---|---|---|---|---|
| Desenvolvedor de módulos SEI | Criar, ativar e manter módulos: classe de integração, eventos, controladores, classes da API, operações da `SeiRN`, InfraPHP e scripts de versão | PHP, InfraPHP, padrões do projeto e banco de dados com suporte a mais de um SGBD | Trabalha no repositório e no ambiente Docker local (`fontes/sei/ops_sei-docker`). A ativação exige editar a chave `Modulos` do `ConfiguracaoSEI.php`, e os scripts de atualização exigem acesso ao servidor da instalação | Resposta do responsável em 2026-10-08 ("desenvolvimento") |

## Publicação e recursos

- Destino: pasta de publicação `docs/manuais/sei/` e pasta de imagens `imagens/` ao lado do manual (`--pasta-imagens imagens` no verificador). Essa pasta já guarda as imagens do manual oficial (`imageNNN`); use nomes descritivos que não colidam com elas.
- Manual anterior: o manual oficial `SEI-Modulos-v5.0` em `docs/manuais/sei/` (`.md` único, `.docx`, `.odt` e `.pdf`), dividido por capítulo em `docs/manuais/sei/manual_md/`. É documento mantido fora da skill e fora do perfil do verificador: os nomes não seguem o padrão slug e os capítulos ficam em `manual_md/`, abaixo da pasta de publicação. Use-o como evidência complementar e base de comparação; não o converta nem o reescreva sem pedido explícito.
- Slug de manual novo: a definir na execução que criar o manual.
- Logo: `<web>/svg/sei_login.svg` (SVG 150 x 150, logotipo do SEI), escolhida pelo responsável e copiada sem alteração para `docs/manuais/sei/imagens/` como `logo-sei.svg`.
- Renderizador: GitLab da Anatel (`git.anatel.gov.br`, remoto `origin`). Manual em Markdown puro, sem HTML.
- Âncoras: automáticas do GitLab. Evite títulos com pontuação entre espaços, como ` - `.
- Aviso de captura: citação de uma linha com negrito, conforme `references/formato-manual.md`.
- Dados sensíveis: exemplos de código sem credenciais, chaves ou dados pessoais; capturas em ambiente de teste, com dados fictícios.
- Coleta manual: desenvolvedor responsável.

## Validação e limites

- Checks locais: verificador da skill para manual novo no destino, contagem de travessão com Python, conferência manual do sumário e conferência de cada nome de classe, método e constante citado com `grep -a` no núcleo.
- Observação de interface: nenhuma autorizada neste adaptador. Conferência em tela e captura dependem de pedido na execução.
- Evidência complementar: manual oficial, catálogos das skills `sei-mod-api-*`, `.agents/references/padrao-*.md` e gabaritos `abc/exemplo` e `trf4/julgamento`.
- Lacunas conhecidas: correspondência tema a tema entre o manual oficial v5.0 e o código 5.0.5; versão implantada; slug do manual novo; procedimento e padrão de geração de prints da equipe, a indicar no grupo "Publicação e recursos"; renderização no GitLab não observada.
- Bloqueio: nenhum para preparar ou usar o adaptador.
