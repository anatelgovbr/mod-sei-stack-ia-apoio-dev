<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
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

  PaginaSEI::getInstance()->prepararSelecao('md_abc_rel_contrato_proj_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcContrato','selMdAbcProjeto'));

  switch ($_GET['acao']) {
    case 'md_abc_rel_contrato_proj_excluir':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcRelContratoProjDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcRelContratoProjDTO = new MdAbcRelContratoProjDTO();
           $arrStrIdComposto = explode('-',$strId);
          $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato($arrStrIdComposto[1]);
          $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto($arrStrIdComposto[2]);
          $arrObjMdAbcRelContratoProjDTO[] = $objMdAbcRelContratoProjDTO;
        }
        $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
        $objMdAbcRelContratoProjRN->excluir($arrObjMdAbcRelContratoProjDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    /*
    case 'md_abc_rel_contrato_proj_desativar':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcRelContratoProjDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcRelContratoProjDTO = new MdAbcRelContratoProjDTO();
           $arrStrIdComposto = explode('-',$strId);
          $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato($arrStrIdComposto[1]);
          $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto($arrStrIdComposto[2]);
          $arrObjMdAbcRelContratoProjDTO[] = $objMdAbcRelContratoProjDTO;
        }
        $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
        $objMdAbcRelContratoProjRN->desativar($arrObjMdAbcRelContratoProjDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    case 'md_abc_rel_contrato_proj_reativar':
      $strTitulo = 'Reativar Associações';
      if (PaginaSEI::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcRelContratoProjDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcRelContratoProjDTO = new MdAbcRelContratoProjDTO();
           $arrStrIdComposto = explode('-',$strId);
          $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato($arrStrIdComposto[1]);
          $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto($arrStrIdComposto[2]);
          $arrObjMdAbcRelContratoProjDTO[] = $objMdAbcRelContratoProjDTO;
        }
        $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
        $objMdAbcRelContratoProjRN->reativar($arrObjMdAbcRelContratoProjDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    */

    case 'md_abc_rel_contrato_proj_selecionar':
      $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar Associação','Selecionar Associações');

      //Se cadastrou alguem
      if (PaginaSEI::GET('acao_origem')==='md_abc_rel_contrato_proj_cadastrar' && isset($_GET['id_md_abc_contrato'], $_GET['id_md_abc_projeto'])) {
        PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('id_md_abc_contrato').'-'.PaginaSEI::GET('id_md_abc_projeto'));
      }
      break;

    case 'md_abc_rel_contrato_proj_listar':
      $strTitulo = 'Associações';
      break;

    default:
      throw new InfraException("Ação '".PaginaSEI::GET('acao')."' não reconhecida.");
  }

  $arrComandos = array();
  if (PaginaSEI::GET('acao')==='md_abc_rel_contrato_proj_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  /* if (PaginaSEI::GET('acao')==='md_abc_rel_contrato_proj_listar' || PaginaSEI::GET('acao')==='md_abc_rel_contrato_proj_selecionar') { */
    $bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNova" value="Nova" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_proj_cadastrar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ova</button>';
    }
  /* } */

  $objMdAbcRelContratoProjDTO = new MdAbcRelContratoProjDTO();
  $objMdAbcRelContratoProjDTO->retNumIdMdAbcContrato();
  $objMdAbcRelContratoProjDTO->retNumIdMdAbcProjeto();
  //$objMdAbcRelContratoProjDTO->retDtaAssociacao();
  //$objMdAbcRelContratoProjDTO->retNumIdMdAbcContratoMdAbcContrato();
  $numIdMdAbcContrato = PaginaSEI::getInstance()->recuperarCampo('selMdAbcContrato');
  if ($numIdMdAbcContrato!=='') {
    $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
  }

  $numIdMdAbcProjeto = PaginaSEI::getInstance()->recuperarCampo('selMdAbcProjeto');
  if ($numIdMdAbcProjeto!=='') {
    $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
  }

/* 
  if (PaginaSEI::GET('acao')==='md_abc_rel_contrato_proj_reativar') {
    //Lista somente inativos
    $objMdAbcRelContratoProjDTO->setBolExclusaoLogica(false);
    $objMdAbcRelContratoProjDTO->setStrSinAtivo('N');
  }
 */
  PaginaSEI::getInstance()->prepararOrdenacao($objMdAbcRelContratoProjDTO, 'IdMdAbcContrato', InfraDTO::$TIPO_ORDENACAO_ASC);
  //PaginaSEI::getInstance()->prepararPaginacao($objMdAbcRelContratoProjDTO);

  $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
  $arrObjMdAbcRelContratoProjDTO = $objMdAbcRelContratoProjRN->listar($objMdAbcRelContratoProjDTO);

  //PaginaSEI::getInstance()->processarPaginacao($objMdAbcRelContratoProjDTO);

  /** @var MdAbcRelContratoProjDTO[] $arrObjMdAbcRelContratoProjDTO */

  $numRegistros = count($arrObjMdAbcRelContratoProjDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (PaginaSEI::GET('acao')==='md_abc_rel_contrato_proj_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
/*     } elseif (PaginaSEI::GET('acao')==='md_abc_rel_contrato_proj_reativar') {
      $bolAcaoReativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_reativar');
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_excluir');
      $bolAcaoDesativar = false;
 */    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_excluir');
      $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_rel_contrato_proj_desativar');
    }

    /* 
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_proj_desativar&acao_origem='.PaginaSEI::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_proj_reativar&acao_origem='.PaginaSEI::GET('acao').'&acao_confirmada=sim');
    }
     */

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_proj_excluir&acao_origem='.PaginaSEI::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    /* if (PaginaSEI::GET('acao')!=='md_abc_rel_contrato_proj_reativar') { */
      $strCaptionTabela = 'Associações';
    /* } else {
      $strCaptionTabela = 'Associações Inativas';
    } */

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.PaginaSEI::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.PaginaSEI::getInstance()->getThCheck().'</th>'."\n";
    }
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcRelContratoProjDTO,'Data de Associação','Associacao',$arrObjMdAbcRelContratoProjDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcRelContratoProjDTO,'Contrato','IdMdAbcContratoMdAbcContrato',$arrObjMdAbcRelContratoProjDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">Ações</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContrato().'-'.$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcProjeto(),$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContrato()).'</td>';
      }
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcRelContratoProjDTO[$i]->getDtaAssociacao()).'</td>';
      //$strResultado .= '<td style="text-align: center">'.PaginaSEI::tratarHTML($arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContratoMdAbcContrato()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContrato().'-'.$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcProjeto());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_proj_consultar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContrato().'&id_md_abc_projeto='.$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcProjeto()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeConsultar().'" title="Consultar Associação" alt="Consultar Associação" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_proj_alterar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContrato().'&id_md_abc_projeto='.$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcProjeto()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeAlterar().'" title="Alterar Associação" alt="Alterar Associação" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContrato().'-'.$arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcProjeto();
        $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript($arrObjMdAbcRelContratoProjDTO[$i]->getNumIdMdAbcContrato());
      }
/* 
      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeDesativar().'" title="Desativar Associação" alt="Desativar Associação" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeReativar().'" title="Reativar Associação" alt="Reativar Associação" class="infraImg" /></a>&nbsp;';
      }
 */

      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeExcluir().'" title="Excluir Associação" alt="Excluir Associação" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (PaginaSEI::GET('acao')==='md_abc_rel_contrato_proj_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('','Todos',$numIdMdAbcContrato);
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
#lblMdAbcContrato {position:absolute;left:0;top:0;width:25%;}
#selMdAbcContrato {position:absolute;left:0;top:40%;width:25%;}

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
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_rel_contrato_proj_selecionar') {
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
  if (confirm('Confirma desativação da Associação \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcRelContratoProjLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjLista').submit();
  }
}

function acaoDesativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma Associação selecionada.');
    return;
  }
  if (confirm('Confirma desativação das Associações selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcRelContratoProjLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoReativar??false) { ?>
function acaoReativar(id,desc)
{
  if (confirm('Confirma reativação da Associação \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcRelContratoProjLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjLista').submit();
  }
}

function acaoReativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma Associação selecionada.');
    return;
  }
  if (confirm('Confirma reativação das Associações selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcRelContratoProjLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjLista').submit();
  }
}
<?php }  */?>

<?php if ($bolAcaoExcluir??false) { ?>
function acaoExcluir(id,desc)
{
  if (confirm('Confirma exclusão da Associação \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcRelContratoProjLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcRelContratoProjLista').submit();
  }
}

function acaoExclusaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma Associação selecionada.');
    return;
  }
  if (confirm('Confirma exclusão das Associações selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcRelContratoProjLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcRelContratoProjLista').submit();
  }
}
<?php } ?>

<?php if(0){?></script><?php }?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcRelContratoProjLista" method="post" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
  <?php
  PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
  PaginaSEI::getInstance()->abrirAreaDados('5em');
  ?>
  <label id="lblMdAbcContrato" for="selMdAbcContrato" accesskey="o" class="infraLabelOpcional">C<span class="infraTeclaAtalho">o</span>ntrato:</label>
  <select id="selMdAbcContrato" name="selMdAbcContrato" onchange="this.form.submit();" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" >
  <?=$strItensSelMdAbcContrato??false?>
  </select>

  <?php
  PaginaSEI::getInstance()->fecharAreaDados();
  PaginaSEI::getInstance()->abrirAreaDados('5em');
  ?>
  <label id="lblMdAbcProjeto" for="selMdAbcProjeto" accesskey="o" class="infraLabelOpcional">Pr<span class="infraTeclaAtalho">o</span>jeto:</label>
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
