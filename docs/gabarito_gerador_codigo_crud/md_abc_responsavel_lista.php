<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4Âª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * VersÃ£o do Gerador de CÃ³digo: 1.46.4
 **/



try {
  require_once __DIR__ . '/abc.php';


  session_start();

  //////////////////////////////////////////////////////////////////////////////
  //InfraDebug::getInstance()->setBolLigado(false);
  //InfraDebug::getInstance()->setBolDebugInfra(true);
  //InfraDebug::getInstance()->limpar();
  //////////////////////////////////////////////////////////////////////////////

  Sessaoabc::getInstance()->validarLink();

  Sessaoabc::getInstance()->validarPermissao($_GET['acao']);

  Paginaabc::getInstance()->prepararSelecao('md_abc_responsavel_selecionar');

  Paginaabc::getInstance()->salvarCamposPost(array('selMdAbcContrato'));

  switch ($_GET['acao']) {
    case 'md_abc_responsavel_excluir':
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcResponsavelDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
          $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel($strId);
          $arrObjMdAbcResponsavelDTO[] = $objMdAbcResponsavelDTO;
        }
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelRN->excluir($arrObjMdAbcResponsavelDTO);
        Paginaabc::getInstance()->adicionarMensagem('OperaÃ§Ã£o realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    /*
    case 'md_abc_responsavel_desativar':
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcResponsavelDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
          $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel($strId);
          $arrObjMdAbcResponsavelDTO[] = $objMdAbcResponsavelDTO;
        }
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelRN->desativar($arrObjMdAbcResponsavelDTO);
        Paginaabc::getInstance()->adicionarMensagem('OperaÃ§Ã£o realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    case 'md_abc_responsavel_reativar':
      $strTitulo = 'Reativar ResponsÃ¡veis';
      if (Paginaabc::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcResponsavelDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
          $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel($strId);
          $arrObjMdAbcResponsavelDTO[] = $objMdAbcResponsavelDTO;
        }
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelRN->reativar($arrObjMdAbcResponsavelDTO);
        Paginaabc::getInstance()->adicionarMensagem('OperaÃ§Ã£o realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    */

    case 'md_abc_responsavel_selecionar':
      $strTitulo = Paginaabc::getInstance()->getTituloSelecao('Selecionar ResponsÃ¡vel','Selecionar ResponsÃ¡veis');

      //Se cadastrou alguem
      if (Paginaabc::GET('acao_origem')==='md_abc_responsavel_cadastrar' && isset($_GET['id_md_abc_responsavel'])) {
        Paginaabc::getInstance()->adicionarSelecionado(Paginaabc::GET('id_md_abc_responsavel'));
      }
      break;

    case 'md_abc_responsavel_listar':
      $strTitulo = 'ResponsÃ¡veis';
      break;

    default:
      throw new InfraException("AÃ§Ã£o '".Paginaabc::GET('acao')."' nÃ£o reconhecida.");
  }

  $arrComandos = array();
  if (Paginaabc::GET('acao')==='md_abc_responsavel_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  /* if (Paginaabc::GET('acao')==='md_abc_responsavel_listar' || Paginaabc::GET('acao')==='md_abc_responsavel_selecionar') { */
    $bolAcaoCadastrar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNovo" value="Novo" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_cadastrar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ovo</button>';
    }
  /* } */

  $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
  $objMdAbcResponsavelDTO->retNumIdMdAbcResponsavel();
  $objMdAbcResponsavelDTO->retStrNome();
  //$objMdAbcResponsavelDTO->retStrCargo();
  //$objMdAbcResponsavelDTO->retStrEmail();
  //$objMdAbcResponsavelDTO->retNumIdMdAbcContratoMdAbcContrato();
  $numIdMdAbcContrato = Paginaabc::getInstance()->recuperarCampo('selMdAbcContrato');
  if ($numIdMdAbcContrato!=='') {
    $objMdAbcResponsavelDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
  }

/* 
  if (Paginaabc::GET('acao')==='md_abc_responsavel_reativar') {
    //Lista somente inativos
    $objMdAbcResponsavelDTO->setBolExclusaoLogica(false);
    $objMdAbcResponsavelDTO->setStrSinAtivo('N');
  }
 */
  Paginaabc::getInstance()->prepararOrdenacao($objMdAbcResponsavelDTO, 'Nome', InfraDTO::$TIPO_ORDENACAO_ASC);
  //Paginaabc::getInstance()->prepararPaginacao($objMdAbcResponsavelDTO);

  $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
  $arrObjMdAbcResponsavelDTO = $objMdAbcResponsavelRN->listar($objMdAbcResponsavelDTO);

  //Paginaabc::getInstance()->processarPaginacao($objMdAbcResponsavelDTO);

  /** @var MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO */

  $numRegistros = count($arrObjMdAbcResponsavelDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (Paginaabc::GET('acao')==='md_abc_responsavel_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_consultar');
      $bolAcaoAlterar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
/*     } elseif (Paginaabc::GET('acao')==='md_abc_responsavel_reativar') {
      $bolAcaoReativar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_reativar');
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = Sessaoabc::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_excluir');
      $bolAcaoDesativar = false;
 */    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_consultar');
      $bolAcaoAlterar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = Sessaoabc::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_excluir');
      $bolAcaoDesativar = Sessaoabc::getInstance()->verificarPermissao('md_abc_responsavel_desativar');
    }

    /* 
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_desativar&acao_origem='.Paginaabc::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_reativar&acao_origem='.Paginaabc::GET('acao').'&acao_confirmada=sim');
    }
     */

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_excluir&acao_origem='.Paginaabc::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    /* if (Paginaabc::GET('acao')!=='md_abc_responsavel_reativar') { */
      $strCaptionTabela = 'ResponsÃ¡veis';
    /* } else {
      $strCaptionTabela = 'ResponsÃ¡veis Inativos';
    } */

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.Paginaabc::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.Paginaabc::getInstance()->getThCheck().'</th>'."\n";
    }
    $strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'Nome','Nome',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'Cargo','Cargo',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'E-mail','Email',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'Contrato','IdMdAbcContratoMdAbcContrato',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">AÃ§Ãµes</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.Paginaabc::getInstance()->getTrCheck($i,$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel(),$arrObjMdAbcResponsavelDTO[$i]->getStrNome()).'</td>';
      }
      $strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getStrNome()).'</td>';
      //$strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getStrCargo()).'</td>';
      //$strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getStrEmail()).'</td>';
      //$strResultado .= '<td style="text-align: center">'.Paginaabc::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcContratoMdAbcContrato()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= Paginaabc::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_consultar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao').'&id_md_abc_responsavel='.$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel()).'" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeConsultar().'" title="Consultar ResponsÃ¡vel" alt="Consultar ResponsÃ¡vel" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_alterar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao').'&id_md_abc_responsavel='.$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel()).'" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeAlterar().'" title="Alterar ResponsÃ¡vel" alt="Alterar ResponsÃ¡vel" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel();
        $strDescricao = Paginaabc::getInstance()->formatarParametrosJavaScript($arrObjMdAbcResponsavelDTO[$i]->getStrNome());
      }
/* 
      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeDesativar().'" title="Desativar ResponsÃ¡vel" alt="Desativar ResponsÃ¡vel" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeReativar().'" title="Reativar ResponsÃ¡vel" alt="Reativar ResponsÃ¡vel" class="infraImg" /></a>&nbsp;';
      }
 */

      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeExcluir().'" title="Excluir ResponsÃ¡vel" alt="Excluir ResponsÃ¡vel" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (Paginaabc::GET('acao')==='md_abc_responsavel_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('','Todos',$numIdMdAbcContrato);
} catch (Exception $e) {
  Paginaabc::getInstance()->processarExcecao($e);
}

Paginaabc::getInstance()->montarDocType();
Paginaabc::getInstance()->abrirHtml();
Paginaabc::getInstance()->abrirHead();
Paginaabc::getInstance()->montarMeta();
Paginaabc::getInstance()->montarTitle(Paginaabc::getInstance()->getStrNomeSistema().' - '.($strTitulo??false));
Paginaabc::getInstance()->montarStyle();
Paginaabc::getInstance()->abrirStyle();
?>
<?php if(0){?><style><?php }?>
#lblMdAbcContrato {position:absolute;left:0;top:0;width:25%;}
#selMdAbcContrato {position:absolute;left:0;top:40%;width:25%;}

<?php if(0){?></style><?php }?>
<?php
Paginaabc::getInstance()->fecharStyle();
Paginaabc::getInstance()->montarJavaScript();
Paginaabc::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_responsavel_selecionar') {
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
  if (confirm('Confirma desativaÃ§Ã£o do ResponsÃ¡vel \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}

function acaoDesativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum ResponsÃ¡vel selecionado.');
    return;
  }
  if (confirm('Confirma desativaÃ§Ã£o dos ResponsÃ¡veis selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoReativar??false) { ?>
function acaoReativar(id,desc)
{
  if (confirm('Confirma reativaÃ§Ã£o do ResponsÃ¡vel \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}

function acaoReativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum ResponsÃ¡vel selecionado.');
    return;
  }
  if (confirm('Confirma reativaÃ§Ã£o dos ResponsÃ¡veis selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}
<?php }  */?>

<?php if ($bolAcaoExcluir??false) { ?>
function acaoExcluir(id,desc)
{
  if (confirm('Confirma exclusÃ£o do ResponsÃ¡vel \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}

function acaoExclusaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum ResponsÃ¡vel selecionado.');
    return;
  }
  if (confirm('Confirma exclusÃ£o dos ResponsÃ¡veis selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}
<?php } ?>

<?php if(0){?></script><?php }?>
<?php
Paginaabc::getInstance()->fecharJavaScript();
Paginaabc::getInstance()->fecharHead();
Paginaabc::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcResponsavelLista" method="post" action="<?=Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao').'&acao_origem='.Paginaabc::GET('acao'))?>">
  <?php
  Paginaabc::getInstance()->montarBarraComandosSuperior($arrComandos??false);
  Paginaabc::getInstance()->abrirAreaDados('5em');
  ?>
  <label id="lblMdAbcContrato" for="selMdAbcContrato" accesskey="o" class="infraLabelOpcional">C<span class="infraTeclaAtalho">o</span>ntrato:</label>
  <select id="selMdAbcContrato" name="selMdAbcContrato" onchange="this.form.submit();" class="infraSelect" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" >
  <?=$strItensSelMdAbcContrato??false?>
  </select>

  <?php
  Paginaabc::getInstance()->fecharAreaDados();
  Paginaabc::getInstance()->montarAreaTabela($strResultado??false,$numRegistros??false);
  //Paginaabc::getInstance()->montarAreaDebug();
  Paginaabc::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
Paginaabc::getInstance()->fecharBody();
Paginaabc::getInstance()->fecharHtml();
