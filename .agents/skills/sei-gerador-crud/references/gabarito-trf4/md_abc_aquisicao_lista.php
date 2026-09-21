<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/



try {
  require_once __DIR__ . '/SEI.php';


  session_start();

  //////////////////////////////////////////////////////////////////////////////
  //InfraDebug::getInstance()->setBolLigado(false);
  //InfraDebug::getInstance()->setBolDebugInfra(true);
  //InfraDebug::getInstance()->limpar();
  //////////////////////////////////////////////////////////////////////////////

  SessaoSEI::getInstance()->validarLink();

  SessaoSEI::getInstance()->validarPermissao($_GET['acao']);

  PaginaSEI::getInstance()->prepararSelecao('md_abc_aquisicao_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcProjeto'));

  switch ($_GET['acao']) {
    case 'md_abc_aquisicao_excluir':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcAquisicaoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcAquisicaoDTO = new MdAbcAquisicaoDTO();
          $objMdAbcAquisicaoDTO->setNumIdMdAbcAquisicao($strId);
          $arrObjMdAbcAquisicaoDTO[] = $objMdAbcAquisicaoDTO;
        }
        $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
        $objMdAbcAquisicaoRN->excluir($arrObjMdAbcAquisicaoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    /*
    case 'md_abc_aquisicao_desativar':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcAquisicaoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcAquisicaoDTO = new MdAbcAquisicaoDTO();
          $objMdAbcAquisicaoDTO->setNumIdMdAbcAquisicao($strId);
          $arrObjMdAbcAquisicaoDTO[] = $objMdAbcAquisicaoDTO;
        }
        $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
        $objMdAbcAquisicaoRN->desativar($arrObjMdAbcAquisicaoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    case 'md_abc_aquisicao_reativar':
      $strTitulo = 'Reativar Aquisições';
      if (PaginaSEI::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcAquisicaoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcAquisicaoDTO = new MdAbcAquisicaoDTO();
          $objMdAbcAquisicaoDTO->setNumIdMdAbcAquisicao($strId);
          $arrObjMdAbcAquisicaoDTO[] = $objMdAbcAquisicaoDTO;
        }
        $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
        $objMdAbcAquisicaoRN->reativar($arrObjMdAbcAquisicaoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    */

    case 'md_abc_aquisicao_selecionar':
      $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar Aquisição','Selecionar Aquisições');

      //Se cadastrou alguem
      if (PaginaSEI::GET('acao_origem')==='md_abc_aquisicao_cadastrar' && isset($_GET['id_md_abc_aquisicao'])) {
        PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('id_md_abc_aquisicao'));
      }
      break;

    case 'md_abc_aquisicao_listar':
      $strTitulo = 'Aquisições';
      break;

    default:
      throw new InfraException("Ação '".PaginaSEI::GET('acao')."' não reconhecida.");
  }

  $arrComandos = array();
  if (PaginaSEI::GET('acao')==='md_abc_aquisicao_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  /* if (PaginaSEI::GET('acao')==='md_abc_aquisicao_listar' || PaginaSEI::GET('acao')==='md_abc_aquisicao_selecionar') { */
    $bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNova" value="Nova" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_aquisicao_cadastrar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ova</button>';
    }
  /* } */

  $objMdAbcAquisicaoDTO = new MdAbcAquisicaoDTO();
  $objMdAbcAquisicaoDTO->retNumIdMdAbcAquisicao();
  $objMdAbcAquisicaoDTO->retStrDescricao();
  //$objMdAbcAquisicaoDTO->retDinCusto();
  //$objMdAbcAquisicaoDTO->retStrIdentificacaoMdAbcProjeto();
  $numIdMdAbcProjeto = PaginaSEI::getInstance()->recuperarCampo('selMdAbcProjeto');
  if ($numIdMdAbcProjeto!=='') {
    $objMdAbcAquisicaoDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
  }

/* 
  if (PaginaSEI::GET('acao')==='md_abc_aquisicao_reativar') {
    //Lista somente inativos
    $objMdAbcAquisicaoDTO->setBolExclusaoLogica(false);
    $objMdAbcAquisicaoDTO->setStrSinAtivo('N');
  }
 */
  PaginaSEI::getInstance()->prepararOrdenacao($objMdAbcAquisicaoDTO, 'Descricao', InfraDTO::$TIPO_ORDENACAO_ASC);
  //PaginaSEI::getInstance()->prepararPaginacao($objMdAbcAquisicaoDTO);

  $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
  $arrObjMdAbcAquisicaoDTO = $objMdAbcAquisicaoRN->listar($objMdAbcAquisicaoDTO);

  //PaginaSEI::getInstance()->processarPaginacao($objMdAbcAquisicaoDTO);

  /** @var MdAbcAquisicaoDTO[] $arrObjMdAbcAquisicaoDTO */

  $numRegistros = count($arrObjMdAbcAquisicaoDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (PaginaSEI::GET('acao')==='md_abc_aquisicao_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
/*     } elseif (PaginaSEI::GET('acao')==='md_abc_aquisicao_reativar') {
      $bolAcaoReativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_reativar');
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_excluir');
      $bolAcaoDesativar = false;
 */    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_excluir');
      $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_aquisicao_desativar');
    }

    /* 
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_aquisicao_desativar&acao_origem='.PaginaSEI::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_aquisicao_reativar&acao_origem='.PaginaSEI::GET('acao').'&acao_confirmada=sim');
    }
     */

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_aquisicao_excluir&acao_origem='.PaginaSEI::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    /* if (PaginaSEI::GET('acao')!=='md_abc_aquisicao_reativar') { */
      $strCaptionTabela = 'Aquisições';
    /* } else {
      $strCaptionTabela = 'Aquisições Inativas';
    } */

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.PaginaSEI::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.PaginaSEI::getInstance()->getThCheck().'</th>'."\n";
    }
    $strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcAquisicaoDTO,'Descrição','Descricao',$arrObjMdAbcAquisicaoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcAquisicaoDTO,'Custo','Custo',$arrObjMdAbcAquisicaoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcAquisicaoDTO,'Projeto','IdentificacaoMdAbcProjeto',$arrObjMdAbcAquisicaoDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">Ações</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObjMdAbcAquisicaoDTO[$i]->getNumIdMdAbcAquisicao(),$arrObjMdAbcAquisicaoDTO[$i]->getStrDescricao()).'</td>';
      }
      $strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcAquisicaoDTO[$i]->getStrDescricao()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcAquisicaoDTO[$i]->getDinCusto()).'</td>';
      //$strResultado .= '<td style="text-align: center">'.PaginaSEI::tratarHTML($arrObjMdAbcAquisicaoDTO[$i]->getStrIdentificacaoMdAbcProjeto()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcAquisicaoDTO[$i]->getNumIdMdAbcAquisicao());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_aquisicao_consultar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_aquisicao='.$arrObjMdAbcAquisicaoDTO[$i]->getNumIdMdAbcAquisicao()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeConsultar().'" title="Consultar Aquisição" alt="Consultar Aquisição" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_aquisicao_alterar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_aquisicao='.$arrObjMdAbcAquisicaoDTO[$i]->getNumIdMdAbcAquisicao()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeAlterar().'" title="Alterar Aquisição" alt="Alterar Aquisição" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcAquisicaoDTO[$i]->getNumIdMdAbcAquisicao();
        $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript($arrObjMdAbcAquisicaoDTO[$i]->getStrDescricao());
      }
/* 
      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeDesativar().'" title="Desativar Aquisição" alt="Desativar Aquisição" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeReativar().'" title="Reativar Aquisição" alt="Reativar Aquisição" class="infraImg" /></a>&nbsp;';
      }
 */

      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeExcluir().'" title="Excluir Aquisição" alt="Excluir Aquisição" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (PaginaSEI::GET('acao')==='md_abc_aquisicao_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

  $strItensSelMdAbcProjeto = MdAbcProjetoINT::montarSelectIdentificacao('','Todos',$numIdMdAbcProjeto);
} catch (Exception $e) {
  PaginaSEI::getInstance()->processarExcecao($e);
}

PaginaSEI::getInstance()->montarDocType();
PaginaSEI::getInstance()->abrirHtml();
PaginaSEI::getInstance()->abrirHead();
PaginaSEI::getInstance()->montarMeta();
PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema().' - '.($strTitulo??false));
PaginaSEI::getInstance()->montarStyle();
PaginaSEI::getInstance()->abrirStyle();
?>
<?php if(0){?><style><?php }?>
#lblMdAbcProjeto {position:absolute;left:0;top:0;width:25%;}
#selMdAbcProjeto {position:absolute;left:0;top:40%;width:25%;}

<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_aquisicao_selecionar') {
    infraReceberSelecao();
    document.getElementById('btnFecharSelecao').focus();
  } else {
    document.getElementById('btnFechar').focus();
  }
  infraEfeitoTabelas(true);
}

<?php /* if ($bolAcaoDesativar??false) { ?>
function acaoDesativar(id,desc)
{
  if (confirm('Confirma desativação da Aquisição \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcAquisicaoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcAquisicaoLista').submit();
  }
}

function acaoDesativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma Aquisição selecionada.');
    return;
  }
  if (confirm('Confirma desativação das Aquisições selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcAquisicaoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcAquisicaoLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoReativar??false) { ?>
function acaoReativar(id,desc)
{
  if (confirm('Confirma reativação da Aquisição \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcAquisicaoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcAquisicaoLista').submit();
  }
}

function acaoReativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma Aquisição selecionada.');
    return;
  }
  if (confirm('Confirma reativação das Aquisições selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcAquisicaoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcAquisicaoLista').submit();
  }
}
<?php }  */?>

<?php if ($bolAcaoExcluir??false) { ?>
function acaoExcluir(id,desc)
{
  if (confirm('Confirma exclusão da Aquisição \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcAquisicaoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcAquisicaoLista').submit();
  }
}

function acaoExclusaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma Aquisição selecionada.');
    return;
  }
  if (confirm('Confirma exclusão das Aquisições selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcAquisicaoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcAquisicaoLista').submit();
  }
}
<?php } ?>

<?php if(0){?></script><?php }?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcAquisicaoLista" method="post" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
  <?php
  PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
  PaginaSEI::getInstance()->abrirAreaDados('5em');
  ?>
  <label id="lblMdAbcProjeto" for="selMdAbcProjeto" accesskey="P" class="infraLabelOpcional"><span class="infraTeclaAtalho">P</span>rojeto:</label>
  <select id="selMdAbcProjeto" name="selMdAbcProjeto" onchange="this.form.submit();" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" >
  <?=$strItensSelMdAbcProjeto??false?>
  </select>

  <?php
  PaginaSEI::getInstance()->fecharAreaDados();
  PaginaSEI::getInstance()->montarAreaTabela($strResultado??false,$numRegistros??false);
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
