# Adaptador: Módulo SEI Apoio a Plano de Trabalho (APT)

Caminhos relativos à raiz do repositório SEI da Anatel. `<php>` abrevia `fontes/sei/src/main/php`. Última conferência: 2026-10-08, árvore de trabalho do branch `adr_spec_docs_stack_ia` sobre a revisão `3f3fdf1f4a`, com a revalidação do modelo na geração.

## Reconhecimento e alcance

- Nome oficial na integração: `SEI Apoio a Plano de Trabalho` (`<php>/sei/web/modulos/apoio-plano-trabalho/MdAptIntegracao.php:26`). Nome no menu e nos títulos de tela: `Apoio a Plano de Trabalho`. Sigla: APT. Instituição: Anatel (`MdAptIntegracao.php:46`).
- Pistas de inclusão: pasta `<php>/sei/web/modulos/apoio-plano-trabalho/`, classe `MdAptIntegracao`, prefixo `md_apt_`, recursos SIP `md_apt_etapa_pl_doc_modelo_listar`, `_cadastrar`, `_alterar` e `_excluir`, scripts `<php>/sei/scripts/sei_atualizar_versao_modulo_apt.php` e `<php>/sip/scripts/sip_atualizar_versao_modulo_apt.php`, parâmetro `VERSAO_MODULO_APT` e requisitos em `docs/requisitos-ancorados/apoio-plano-trabalho/`.
- Pistas de exclusão: demais pastas de `<php>/sei/web/modulos/` e scripts de outros módulos em `sei/scripts` e `sip/scripts`.
- Componentes do módulo: páginas `md_apt_etapa_pl_doc_modelo_lista.php` e `md_apt_etapa_pl_doc_modelo_cadastro.php`, `rn/MdAptEtapaPlDocModeloRN.php`, `dto/MdAptEtapaPlDocModeloDTO.php`, `bd/MdAptEtapaPlDocModeloBD.php`, `js/apoio_plano_trabalho.js`, `css/apoio_plano_trabalho.css` e `MdAptIntegracao.php` (controlador de páginas, controlador AJAX e evento `gerarDocumento`).
- Componentes compartilhados que entram no alcance quando a tarefa passa por eles: Plano de Trabalho do core (`<php>/sei/web/plano_trabalho/`), geração de documento (`<php>/sei/web/documento_cadastro.php`, `<php>/sei/web/rn/DocumentoRN.php`), árvore do processo (`<php>/sei/web/arvore_visualizar.php`, `<php>/sei/web/int/ProcedimentoINT.php`, `<php>/sei/web/int/ProtocoloINT.php`), API interna (`<php>/sei/web/rn/SeiRN.php`) e InfraPHP (`<php>/infra/infra_php/`, `<php>/infra/infra_js/`).
- Fronteira: o módulo não cria planos, etapas, itens nem documentos. Esses objetos são do core e só são lidos pelo módulo.

## Versão e variante

- Fontes de versão: `MdAptIntegracao::getVersao()` (`MdAptIntegracao.php:34-37`), `$versaoAtualDesteModulo` nos scripts SEI e SIP (linha 12 de cada um), README do módulo e parâmetro `VERSAO_MODULO_APT` em Infra > Parâmetros do SEI e do SIP.
- Variante: a versão 1.0.0 não distingue revisões. O ramo `correcoes_apt` (`d214f8ea3d`) e a árvore de trabalho conferida em 2026-10-08 mantêm 1.0.0 e acrescentam a revalidação do modelo na geração (`MdAptIntegracao::gerarDocumento` chama `validarProtocoloModelo` em `MdAptIntegracao.php:202`); a revisão `3f3fdf1f4a` não tem essa revalidação. Para saber qual variante um manual descreve, confira se `gerarDocumento` chama `validarProtocoloModelo` na revisão examinada e pergunte ao responsável qual revisão está implantada.
- Requisito de plataforma: o README do módulo pede SEI 5.0.4 ou superior; o script SEI aceita `SEI_VERSAO >= 4.1.5` e ambos exigem `VERSAO_INFRA >= 2.29.0` (`sei_atualizar_versao_modulo_apt.php:129-136`). Divergência fora do alcance de manuais de uso.
- Ativação: chave `Modulos` do `ConfiguracaoSEI.php` com `'MdAptIntegracao' => 'apoio-plano-trabalho'` (README do módulo). O que cada pessoa vê depende dos perfis do SIP da instalação.
- Idioma: interface somente em português brasileiro, com textos literais no PHP e no JS. Não há arquivos de tradução.

## Leitura da codebase

- Raízes: as listadas em "Reconhecimento e alcance", mais `docs/requisitos-ancorados/apoio-plano-trabalho/`, `docs/dicionario_dados/apoio-plano-trabalho/` e o README do módulo.
- Extensões: `.php`, `.js`, `.css` e `.md`.
- Codificação: PHP do módulo, do core e da InfraPHP em ISO-8859-1 com CRLF (conferido com `file`). O JS do módulo é ASCII e usa escapes como `ã` em `alert` e `confirm`. Os `.md` são UTF-8.
- Leitura: `iconv -f latin1 -t utf-8 <arquivo> | tr -d '\r' | cat -n`. Busca: `grep -a` sempre, porque sem `-a` o `grep` desta máquina (ugrep) trata o PHP Latin-1 como binário e devolve vazio. `rg` não está instalado.
- Exclusões comprovadas: `<php>/sei/web/editor/` e demais módulos. O módulo não tem testes automatizados nesta revisão (`fontes/sei/src/test` não tem testes do módulo).
- Ferramentas: `grep -a`, `iconv`, `file`, `git` e `python3`.

## Pontes de evidência

- Ação para página: `MdAptIntegracao::processarControlador` (`MdAptIntegracao.php:55-73`) liga `md_apt_etapa_pl_doc_modelo_listar` e `_excluir` à lista e `_cadastrar` e `_alterar` ao cadastro. AJAX: `processarControladorAjax` (`MdAptIntegracao.php:81-89`), ação `md_apt_etapa_pl_doc_modelo_salvar`.
- Permissão: o nome do recurso SIP é o nome da ação. Páginas chamam `validarLink` e `validarPermissao($strAcao)`; a RN chama `validarAuditarPermissao`; ícones e botões condicionais usam `verificarPermissao`. Busca: `grep -a -n "Permissao(" <arquivo>`.
- Menu: o script SIP cria o item `Apoio a Plano de Trabalho` sob o item cujo rótulo é `Administracao` ou `Administração`, ligado ao recurso `md_apt_etapa_pl_doc_modelo_listar` e ao perfil `Administrador` (`sip_atualizar_versao_modulo_apt.php:178-197` e `282-301`). O rótulo exibido do menu pai é dado do SIP.
- Caminho visível: monte o caminho com o rótulo do menu SIP, o título da página (`$strTitulo` passado a `abrirBody`), o texto do link e o `title` dos ícones. Nunca use a ação ou a URL como navegação.
- Geração a partir de item de etapa: ícone `Plano de Trabalho` na barra do processo (`ProcedimentoINT.php:935-944`) ou do documento (`ProtocoloINT.php:1082-1086`), página `Plano de Trabalho` (`plano_trabalho/plano_trabalho_detalhar.php`), ícone `Incluir Documento` do item (`plano_trabalho_detalhar.php:263-265`), página `Gerar Documento do Plano de Trabalho` (`plano_trabalho/item_etapa_incluir_documento.php`), página `Gerar Documento` (`documento_cadastro.php:66-271`), gravação em `DocumentoRN.php:647-687`, evento `gerarDocumento` do módulo e abertura do editor (`arvore_visualizar.php:72-73` e `502-503`).
- Entidade: `MdAptEtapaPlDocModeloDTO` mapeia `md_apt_etapa_pl_doc_modelo` (item de etapa e documento modelo) e obtém o protocolo formatado por junção com `protocolo`. Significado das colunas em `docs/dicionario_dados/apoio-plano-trabalho/`.
- Corroboração: `docs/requisitos-ancorados/apoio-plano-trabalho/` descreve RN-APT, RF-APT e RT-APT. Confronte cada afirmação com o código da revisão examinada; os requisitos podem descrever outra variante.

## Interface e textos

- Labels, cabeçalhos de coluna, títulos de ícone e botões: literais no PHP das páginas (`label`, `th`, `title` e `alt` de `img`, `button`). Mensagens de confirmação e alerta do cliente: `js/apoio_plano_trabalho.js`, com escapes Unicode a decodificar.
- Títulos de tela: variável `$strTitulo` de cada página. Título de tabela: `InfraPagina::gerarCaptionTabela`, que monta `Lista de <entidade> (N registros):` (`<php>/infra/infra_php/InfraPagina.php:2916-2950`).
- Mensagens de sucesso: `PaginaSEI::adicionarMensagem`. Críticas: `InfraException` com `adicionarValidacao` ou `lancarValidacao`. Na janela do cadastro, o erro do AJAX vira alerta do navegador (`<php>/infra/infra_js/InfraAjax.js:232-246`) e a janela continua aberta.
- Críticas do core que aparecem no módulo: `SeiRN::consultarDocumento` (`SeiRN.php:2619-2689`) e `InfraSessao::validarPermissao` (`<php>/infra/infra_php/InfraSessao.php:884-898`).
- Textos vindos de banco: nomes de plano, etapa e item, número de protocolo, sigla de unidade e rótulos de menu do SIP. Explique a variável e não invente valores.
- Ícones: o módulo usa `getIconeConsultar`, `getIconeAlterar` e `getIconeExcluir` com `title` próprio. O mesmo ícone de alterar serve a `Associar Protocolo Modelo` e a `Alterar Associação`.
- Janela: `infraAbrirJanelaModal(url, 700, 360)` (`js/apoio_plano_trabalho.js:20-23`) com `pagina_simples=1`.
- Variantes por persona: `verificarPermissao` controla ícones da lista (`md_apt_etapa_pl_doc_modelo_lista.php:52-57`, `194-208`) e o botão `Salvar` do cadastro (`md_apt_etapa_pl_doc_modelo_cadastro.php:80-82`, `128-130`).
- Código sem chamador nesta revisão: `acaoExclusaoMultipla`, `filtrar`, `recarregarAssociacoesApt` e `enviarFormulario` no JS e o seletor `#selPlanoTrabalho` no CSS. Não documentar como funcionalidade.
- Traduções: não aplicável.

## Personas e acesso

| Persona ou público | Objetivo e tarefas | Conhecimento relevante | Perfil e restrições | Fonte e confirmação |
|---|---|---|---|---|
| Administrador do SEI que associa documentos modelo | Associar, trocar e excluir o documento modelo de cada item de etapa | Planos de trabalho do SEI e documentos de editor interno | Perfil SIP `Administrador` recebe os quatro recursos do módulo e o menu (`sip_atualizar_versao_modulo_apt.php:178-197`). As telas também exigem `plano_trabalho_listar`, `plano_trabalho_consultar`, `etapa_trabalho_listar`, `item_etapa_listar` e `item_etapa_consultar` (RNs em `<php>/sei/web/plano_trabalho/rn/`), e a validação do protocolo exige `documento_consultar` e `protocolo_listar` (`DocumentoRN.php:1861`, `ProtocoloRN.php:1884`). A instalação do módulo não concede essas permissões do core | Público do briefing de 2026-10-06; perfis do core na instalação não determinados |
| Usuário do SEI que gera documento a partir de item de etapa | Gerar documento de editor interno a partir de item com documento modelo | Processos, plano de trabalho do processo e editor do SEI | Precisa de `plano_trabalho_detalhar` e `item_etapa_incluir_documento`, do processo aberto na unidade, de tipo de documento ligado ao item e de acesso da unidade ao item (`plano_trabalho_detalhar.php:121` e `263`). Não precisa das permissões do módulo (`MdAptIntegracao.php:169-227`, `MdAptEtapaPlDocModeloRN.php:196-211`) | Público do briefing de 2026-10-06; perfis SIP que concedem esses recursos não determinados |

## Publicação e recursos

- Destino: pasta de publicação `docs/manuais/apoio-plano-trabalho/`, com o mesmo nome da pasta do módulo em `docs/requisitos-ancorados/`, e pasta de imagens `imagens/` ao lado do manual (`--pasta-imagens imagens` no verificador). Manual atual: `docs/manuais/apoio-plano-trabalho/manual-apoio-plano-trabalho.md`, slug `manual-apoio-plano-trabalho`, criado em 2026-10-06, sem manual anterior.
- Logo: `<php>/sei/web/svg/sei_login.svg` (SVG 150 x 150, logotipo do SEI), escolhida pelo responsável e copiada sem alteração para a pasta de imagens do manual como `logo-sei.svg`.
- Renderizador: GitLab da Anatel (`git.anatel.gov.br`, remoto `origin`). Manual em Markdown puro, sem HTML.
- Âncoras: automáticas do GitLab (minúsculas, remove caracteres que não sejam letra, número, hífen ou sublinhado, troca espaço por hífen e mantém acentos). Evite títulos com pontuação entre espaços, como ` - `, que geram hífens seguidos e podem divergir entre GitLab e o verificador.
- Aviso de captura: citação de uma linha com negrito, conforme `references/formato-manual.md`.
- Dados sensíveis: capturas em homologação, com plano, item, protocolo, usuário, unidade e processo fictícios ou mascarados.
- Coleta manual: desenvolvedor ou usuário responsável, em ambiente com o módulo 1.0.0 na revisão documentada e com a persona indicada em cada aviso.

## Validação e limites

- Checks locais: verificador da skill, contagem de travessão com Python e conferência manual do sumário. `php -l` só quando houver PHP alterado.
- Observação de interface: nenhum ambiente navegável autorizado em 2026-10-06. Em 2026-10-07, a sessão de testes `0de99f2b-3942-46ee-bbb5-de83c18531d8` observou o SEI 5.0.5 local com o módulo da árvore de trabalho, inclusive a geração sem o texto do modelo em unidade que não pode consultar o documento modelo; dela vem a captura `janela-associar-protocolo-modelo.png`. As demais afirmações do manual são comprovadas no código.
- Evidência complementar: README do módulo, `docs/requisitos-ancorados/apoio-plano-trabalho/` e dicionário de dados.
- Lacunas conhecidas: rótulo exibido do menu pai `Administração` (dado do SIP); perfis do SIP que concedem as permissões do core; variante implantada; procedimento e padrão de geração de prints da equipe, a indicar no grupo "Publicação e recursos"; renderização no GitLab não observada.
- Bloqueio: nenhum para escrita. A leitura visual (M07) depende de acesso ao GitLab da Anatel.
