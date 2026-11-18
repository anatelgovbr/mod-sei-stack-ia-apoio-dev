# Foco, Enter, barras de comandos, teclas de atalho e ordenação de grid em telas SEI

## Aplicação

Aplique esta referência quando a entrega criar página de módulo montada com `PaginaSEI`, interna ou externa, ou alterar campos de filtro, campos de formulário, barra de comandos, tecla de atalho ou grid de página existente. Em página existente, aplique o padrão à tela alterada pela demanda e registre como observação o desvio preexistente nas partes que a demanda não toca, conforme "Mudanças cirúrgicas" do `AGENTS.md`. O core tem variações nesses controles; as regras abaixo escolhem, entre elas, o padrão mínimo do projeto.

## Foco inicial

A função `inicializar()`, chamada por `abrirBody($strTitulo, 'onload="inicializar();"')`, posiciona o foco no elemento indicado. Quando esse elemento estiver oculto ou desabilitado no modo atual, use o próximo campo habilitado na ordem de tabulação.

| Tela e modo | Elemento com foco | Exemplo no core |
|---|---|---|
| Lista com campo de filtro, inclusive `_selecionar` | primeiro campo de filtro; em `_selecionar`, depois de `infraReceberSelecao()` | `assunto_lista.php`, `contato_lista.php` |
| Lista sem campo de filtro | `btnFechar`; em `_selecionar`, `btnFecharSelecao` depois de `infraReceberSelecao()` | `orgao_lista.php` |
| `_cadastrar` e `_alterar` | primeiro campo editável do formulário | `retorno_programado_cadastro.php` |
| `_consultar` | `btnFechar`, depois de `infraDesabilitarCamposAreaDados()` | `bloco_cadastro.php` |

Muitas páginas do core e o gabarito TRF4 focam `btnCancelar` em `_alterar`, e o Enter passa a cancelar a alteração. O padrão do projeto foca o primeiro campo editável também nesse modo.

## Botão padrão do Enter

O Enter em campo de texto envia o formulário pelo botão padrão: o primeiro `type="submit"` do `<form>` na ordem do documento. Como `montarBarraComandosSuperior($arrComandos)` vem logo depois da abertura do `<form>`, o botão padrão é o primeiro submit de `$arrComandos`.

- Lista com campo de filtro: o primeiro submit é `<button type="submit" accesskey="P" id="sbmPesquisar" name="sbmPesquisar" value="Pesquisar" class="infraButton"><span class="infraTeclaAtalho">P</span>esquisar</button>`. Quando um rótulo da página já usa a tecla P, o Pesquisar sai sem `accesskey` e sem o destaque da letra, conforme "Teclas de atalho". Quando outro comando entrar antes no array, use `array_unshift`, como em `bloco_lista.php`. Select ou checkbox com `onchange="this.form.submit()"` complementa o Pesquisar, que continua presente.
- Cadastro e alteração: o primeiro submit é o Salvar, `<button type="submit" accesskey="S" name="sbmCadastrar<Entidade>" value="Salvar" class="infraButton">` ou `name="sbmAlterar<Entidade>"`, identificado no servidor por `PaginaSEI::POST('sbm...')`.
- Os demais comandos levam `type="button"`, inclusive Novo, Fechar, Cancelar, Excluir e Imprimir. Um `<button>` sem `type` é submit e pode virar o botão padrão.
- A validação fica em `onsubmit="return OnSubmitForm();"` do `<form>`, percorrida igualmente pelo Enter e pelo clique. Pesquisar declarado como `type="button"` com envio por JavaScript deixa o Enter sem pesquisa.
- No envio pelo Enter ou pelo clique, o POST leva o `name` do botão padrão. `form.submit()` por JavaScript, usado em `onchange` e na ordenação, envia o formulário sem botão. Por isso a gravação é identificada pelo nome do Salvar, e a lista aplica os filtros a cada envio, com ou sem botão.
- Componentes com Enter próprio mantêm seu comportamento: `textarea` quebra linha, o autocompletar do infra (`InfraAjax.js`) consome o Enter, e campo de inclusão de item pode usar o Enter para adicionar à lista, como `transportarEmailEnter` em `unidade_cadastro.php`. Os demais campos de texto deixam o Enter chegar ao botão padrão; as máscaras `infraMascara*` já o deixam passar.

## Barras de comandos

A página monta a mesma barra de comandos no topo e no rodapé, conforme o esqueleto de página do manual (cap. 4, `InfraPagina`). O padrão vale em 91 das 91 listas e em 74 dos 77 cadastros do core, e `trf4/julgamento` e `peticionamento` o seguem.

1. `PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos);` logo depois da abertura do `<form>`.
2. `PaginaSEI::getInstance()->montarBarraComandosInferior(preg_replace('/ accesskey="[^"]*"/', '', $arrComandos));` antes de `</form>`: na lista, depois de `montarAreaTabela`; no cadastro, depois de `fecharAreaDados`. O core passa o mesmo `$arrComandos` às duas barras; o padrão do projeto tira o `accesskey` da barra inferior e mantém rótulo e letra destacada. Com `accesskey` repetido, o Chrome e o Edge clicam no botão de baixo e levam o foco ao rodapé, e o Firefox só alterna o foco entre os dois botões, sem clicar; sem a repetição, a tecla aciona o botão do topo nos três navegadores.

A `InfraPagina` decide se imprime a barra inferior (`InfraPaginaEsquema3::montarBarraComandosInferior`): imprime em página sem `montarAreaTabela`, como cadastro e consulta, e em lista cuja maior tabela passa de 15 linhas; `$bolForcarMontagem = true` força a impressão. Por isso a chamada fica em toda lista e todo cadastro, e a página não testa o tamanho.

## Teclas de atalho

Botão da barra de comandos e rótulo de campo declaram a tecla em `accesskey` e destacam a mesma letra no texto com `<span class="infraTeclaAtalho">`, que a `InfraPagina` sublinha (manual cap. 4). O valor tem um caractere, igual à letra destacada e na caixa em que ela aparece no rótulo: `<button type="button" accesskey="x" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton">E<span class="infraTeclaAtalho">x</span>cluir</button>`. No core há desvios a não copiar: em `serie_lista.php`, "Novo Grupo" destaca G e declara `accesskey="N"`; em `tipo_procedimento_lista.php`, `accesskey="Fechar"` tem mais de um caractere e o navegador o ignora.

O usuário aciona a tecla com `Alt` + letra no Chrome e no Edge e com `Alt` + `Shift` + letra no Firefox, em que `Alt` sem `Shift` abre o menu do navegador. As letras C, D, E e F ficam fora do padrão porque o navegador as consome antes da página: no Edge, `Alt+C` abre o Copilot; no Chrome e no Edge, `Alt+D` vai à barra de endereço e `Alt+E` e `Alt+F` abrem o menu. As demais letras acionam o elemento nos três navegadores, conforme teste de 2026-11 no Windows com Chrome 157, Edge 157 e Firefox 160 em perfil limpo.

| Comando | Letra | Letra no core e nos módulos |
|---|---|---|
| Pesquisar | `P` | igual |
| Novo, Nova | `N` | igual |
| Salvar | `S` | igual |
| Cancelar | `a`, em `C<span class="infraTeclaAtalho">a</span>ncelar` | `C` |
| Fechar | `a`, em `Fech<span class="infraTeclaAtalho">a</span>r` | `F` no core; `c` em vários módulos |
| Excluir | `x`, em `E<span class="infraTeclaAtalho">x</span>cluir` | `E`; `x` em `litigioso` e `correios` |
| Desativar | `t`, em `Desa<span class="infraTeclaAtalho">t</span>ivar` | igual |
| Reativar | `R` | igual |
| Imprimir | `I` | igual |
| Transportar | `T` | igual |
| Voltar | `V` | igual |
| Limpar | `L` | igual |

Cada letra aparece uma vez por página, entre botões e rótulos, sem distinção de maiúscula e minúscula. Fechar e Cancelar compartilham `a` porque não dividem a barra: Cancelar fica em `_cadastrar` e `_alterar`, e Fechar, em `_consultar` e na lista. Quando um rótulo de campo disputa a letra de um comando, o rótulo escolhe outra letra do próprio texto fora de C, D, E e F; a exceção é o Pesquisar, que, acionado também pelo Enter, cede a letra ao rótulo. Sem letra livre, o elemento sai sem `accesskey` e sem destaque.

## Ordenação de grid

Vale para tabela de registros montada com `montarAreaTabela` a partir de `listar`. Tabela de edição dentro de formulário, como `infraTabelaDinamica`, e tabela de ordem manual ficam fora desta seção.

1. Antes do `listar`, chame `PaginaSEI::getInstance()->prepararOrdenacao($objDTO, '<Atributo>', InfraDTO::$TIPO_ORDENACAO_ASC)`, ou `$TIPO_ORDENACAO_DESC`, uma vez por tabela. Escolha a coluna e a direção padrão pela leitura natural dos dados, por exemplo nome em ordem ascendente ou data mais recente primeiro, e informe as duas na entrega.
2. Em cada coluna que exibe valor ordenável, monte o cabeçalho com `getThOrdenacao($objDTO, '<Rótulo>', '<Atributo>', $arrObjDTO)`, com uma chave de ordenação própria por coluna.
3. O `<Atributo>` padrão do passo 1 é a chave de uma coluna com seta da mesma tabela, para a seta selecionada indicar a ordenação padrão.
4. A escolha do usuário é o primeiro critério. Desempate por `setOrd*` vem depois de `prepararOrdenacao`, porque `InfraDTO` aplica os critérios na ordem das chamadas.
5. A ordenação vale para o conjunto inteiro. Com `prepararPaginacao`, a chave de cada coluna com seta é atributo com coluna SQL, porque o core ordena atributo sem coluna SQL apenas no array carregado, isto é, na página atual. Para coluna calculada em grid paginado, crie chave SQL, deixe a coluna sem seta ou, se o conjunto for pequeno e limitado, desligue a paginação. Atributos `arr`, `obj` e `bin` não aceitam ordenação.
6. Ficam sem seta apenas o checkbox (`getThCheck`), a coluna Ações e a coluna sem chave válida pelo passo 5. Liste essas colunas na entrega, com o motivo.
7. Em página com mais de uma tabela, cada tabela usa o próprio `$strSelecao` em `prepararOrdenacao`, `getThOrdenacao`, `prepararPaginacao`, `processarPaginacao` e `montarAreaTabela`, para que os campos `hdn<Selecao>CampoOrd` e `hdn<Selecao>TipoOrd` fiquem separados.

## Verificação

A verificação termina quando cada item abaixo tiver evidência ou estiver registrado como pendente, com o motivo.

1. No código, cite arquivo e linha do foco em `inicializar()`, do primeiro submit de `$arrComandos`, das chamadas `montarBarraComandosSuperior` e `montarBarraComandosInferior`, com a letra de cada `accesskey` de comando e de rótulo, e, em grid, de `prepararOrdenacao` e de cada `getThOrdenacao`, com a lista das colunas sem seta.
2. No navegador, em sessão do SEI com acesso à tela, em cada modo criado ou alterado:
   - depois do carregamento, `document.activeElement.id` é o elemento indicado em "Foco inicial";
   - Enter em campo de texto do filtro aciona o Pesquisar e aplica o filtro; no cadastro, aciona o Salvar e o servidor processa a gravação ou a validação. O navegador não envia o formulário pelo Enter em `select`: em filtro com foco em `select`, verifique a pesquisa pela troca de opção e pelo clique no Pesquisar;
   - `[...document.querySelectorAll('[accesskey]')].filter(e => e.accessKey).map(e => e.accessKey.toLowerCase())` devolve letras sem repetição e sem `c`, `d`, `e` e `f`;
   - com a barra inferior visível, a tecla de atalho de cada comando criado ou alterado aciona o botão do topo. No navegador controlado por Playwright, `page.keyboard.press('Alt+KeyP')` não aciona `accesskey` no Chromium; envie a tecla pelo CDP, com `modifiers: 1` (Alt), em três eventos `Input.dispatchKeyEvent`: `rawKeyDown`, `char` com `text` e `unmodifiedText` iguais à letra, e `keyUp`;
   - no primeiro acesso da ação na sessão, a coluna padrão exibe a seta selecionada na direção padrão: imagem `seta_acima_selecionada` ou `seta_abaixo_selecionada`, com título "Ordenar <Rótulo> Ascendente" ou "Descendente". O core guarda a última ordenação na sessão, por ação; uma ordenação anterior na mesma sessão muda o estado inicial;
   - a seta de outra coluna reordena os registros, move a seta selecionada e preserva os filtros; com paginação, a ordem vale entre as páginas.
3. O `audit.py` de `sei-verificacao-pagina` não verifica foco, botão padrão, barras de comandos, teclas de atalho nem ordenação; seu `PASS` não cobre esta verificação. Sem navegador ou sem acesso à tela, registre o item 2 como pendente.
