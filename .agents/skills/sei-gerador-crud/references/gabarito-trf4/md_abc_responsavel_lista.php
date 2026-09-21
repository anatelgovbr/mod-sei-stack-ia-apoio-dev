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

  PaginaSEI::getInstance()->prepararSelecao('md_abc_responsavel_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcContrato'));

  switch ($_GET['acao']) {
    case 'md_abc_responsavel_excluir':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcResponsavelDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
          $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel($strId);
          $arrObjMdAbcResponsavelDTO[] = $objMdAbcResponsavelDTO;
        }
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelRN->excluir($arrObjMdAbcResponsavelDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    /*
    case 'md_abc_responsavel_desativar':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcResponsavelDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
          $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel($strId);
          $arrObjMdAbcResponsavelDTO[] = $objMdAbcResponsavelDTO;
        }
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelRN->desativar($arrObjMdAbcResponsavelDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    case 'md_abc_responsavel_reativar':
      $strTitulo = 'Reativar Responsáveis';
      if (PaginaSEI::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcResponsavelDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
          $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel($strId);
          $arrObjMdAbcResponsavelDTO[] = $objMdAbcResponsavelDTO;
        }
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelRN->reativar($arrObjMdAbcResponsavelDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    */

    case 'md_abc_responsavel_selecionar':
      $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar Responsável','Selecionar Responsáveis');

      //Se cadastrou alguem
      if (PaginaSEI::GET('acao_origem')==='md_abc_responsavel_cadastrar' && isset($_GET['id_md_abc_responsavel'])) {
        PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('id_md_abc_responsavel'));
      }
      break;

    case 'md_abc_responsavel_listar':
      $strTitulo = 'Responsáveis';
      break;

    default:
      throw new InfraException("Ação '".PaginaSEI::GET('acao')."' não reconhecida.");
  }

  $arrComandos = array();
  if (PaginaSEI::GET('acao')==='md_abc_responsavel_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  /* if (PaginaSEI::GET('acao')==='md_abc_responsavel_listar' || PaginaSEI::GET('acao')==='md_abc_responsavel_selecionar') { */
    $bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNovo" value="Novo" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_cadastrar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ovo</button>';
    }
  /* } */

  $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
  $objMdAbcResponsavelDTO->retNumIdMdAbcResponsavel();
  $objMdAbcResponsavelDTO->retStrNome();
  //$objMdAbcResponsavelDTO->retStrCargo();
  //$objMdAbcResponsavelDTO->retStrEmail();
  //$objMdAbcResponsavelDTO->retNumIdMdAbcContratoMdAbcContrato();
  $numIdMdAbcContrato = PaginaSEI::getInstance()->recuperarCampo('selMdAbcContrato');
  if ($numIdMdAbcContrato!=='') {
    $objMdAbcResponsavelDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
  }

/* 
  if (PaginaSEI::GET('acao')==='md_abc_responsavel_reativar') {
    //Lista somente inativos
    $objMdAbcResponsavelDTO->setBolExclusaoLogica(false);
    $objMdAbcResponsavelDTO->setStrSinAtivo('N');
  }
 */
  PaginaSEI::getInstance()->prepararOrdenacao($objMdAbcResponsavelDTO, 'Nome', InfraDTO::$TIPO_ORDENACAO_ASC);
  //PaginaSEI::getInstance()->prepararPaginacao($objMdAbcResponsavelDTO);

  $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
  $arrObjMdAbcResponsavelDTO = $objMdAbcResponsavelRN->listar($objMdAbcResponsavelDTO);

  //PaginaSEI::getInstance()->processarPaginacao($objMdAbcResponsavelDTO);

  /** @var MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO */

  $numRegistros = count($arrObjMdAbcResponsavelDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (PaginaSEI::GET('acao')==='md_abc_responsavel_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
/*     } elseif (PaginaSEI::GET('acao')==='md_abc_responsavel_reativar') {
      $bolAcaoReativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_reativar');
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_excluir');
      $bolAcaoDesativar = false;
 */    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_excluir');
      $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_responsavel_desativar');
    }

    /* 
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_desativar&acao_origem='.PaginaSEI::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_reativar&acao_origem='.PaginaSEI::GET('acao').'&acao_confirmada=sim');
    }
     */

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_excluir&acao_origem='.PaginaSEI::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    /* if (PaginaSEI::GET('acao')!=='md_abc_responsavel_reativar') { */
      $strCaptionTabela = 'Responsáveis';
    /* } else {
      $strCaptionTabela = 'Responsáveis Inativos';
    } */

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.PaginaSEI::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.PaginaSEI::getInstance()->getThCheck().'</th>'."\n";
    }
    $strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'Nome','Nome',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'Cargo','Cargo',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'E-mail','Email',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcResponsavelDTO,'Contrato','IdMdAbcContratoMdAbcContrato',$arrObjMdAbcResponsavelDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">Ações</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel(),$arrObjMdAbcResponsavelDTO[$i]->getStrNome()).'</td>';
      }
      $strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getStrNome()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getStrCargo()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getStrEmail()).'</td>';
      //$strResultado .= '<td style="text-align: center">'.PaginaSEI::tratarHTML($arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcContratoMdAbcContrato()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_consultar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_responsavel='.$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeConsultar().'" title="Consultar Responsável" alt="Consultar Responsável" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_responsavel_alterar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_responsavel='.$arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeAlterar().'" title="Alterar Responsável" alt="Alterar Responsável" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcResponsavelDTO[$i]->getNumIdMdAbcResponsavel();
        $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript($arrObjMdAbcResponsavelDTO[$i]->getStrNome());
      }
/* 
      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeDesativar().'" title="Desativar Responsável" alt="Desativar Responsável" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeReativar().'" title="Reativar Responsável" alt="Reativar Responsável" class="infraImg" /></a>&nbsp;';
      }
 */

      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeExcluir().'" title="Excluir Responsável" alt="Excluir Responsável" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (PaginaSEI::GET('acao')==='md_abc_responsavel_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('','Todos',$numIdMdAbcContrato);
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

<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_responsavel_selecionar') {
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
  if (confirm('Confirma desativação do Responsável \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}

function acaoDesativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Responsável selecionado.');
    return;
  }
  if (confirm('Confirma desativação dos Responsáveis selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoReativar??false) { ?>
function acaoReativar(id,desc)
{
  if (confirm('Confirma reativação do Responsável \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}

function acaoReativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Responsável selecionado.');
    return;
  }
  if (confirm('Confirma reativação dos Responsáveis selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}
<?php }  */?>

<?php if ($bolAcaoExcluir??false) { ?>
function acaoExcluir(id,desc)
{
  if (confirm('Confirma exclusão do Responsável \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}

function acaoExclusaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Responsável selecionado.');
    return;
  }
  if (confirm('Confirma exclusão dos Responsáveis selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcResponsavelLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcResponsavelLista').submit();
  }
}
<?php } ?>

<?php if(0){?></script><?php }?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcResponsavelLista" method="post" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
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
  PaginaSEI::getInstance()->montarAreaTabela($strResultado??false,$numRegistros??false);
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
