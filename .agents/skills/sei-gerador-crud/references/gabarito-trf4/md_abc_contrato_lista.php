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

  PaginaSEI::getInstance()->prepararSelecao('md_abc_contrato_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcAquisicao'));

  switch ($_GET['acao']) {
    case 'md_abc_contrato_excluir':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcContratoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcContratoDTO = new MdAbcContratoDTO();
          $objMdAbcContratoDTO->setNumIdMdAbcContrato($strId);
          $arrObjMdAbcContratoDTO[] = $objMdAbcContratoDTO;
        }
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoRN->excluir($arrObjMdAbcContratoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    /*
    case 'md_abc_contrato_desativar':
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcContratoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcContratoDTO = new MdAbcContratoDTO();
          $objMdAbcContratoDTO->setNumIdMdAbcContrato($strId);
          $arrObjMdAbcContratoDTO[] = $objMdAbcContratoDTO;
        }
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoRN->desativar($arrObjMdAbcContratoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    case 'md_abc_contrato_reativar':
      $strTitulo = 'Reativar Contratos';
      if (PaginaSEI::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = PaginaSEI::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcContratoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcContratoDTO = new MdAbcContratoDTO();
          $objMdAbcContratoDTO->setNumIdMdAbcContrato($strId);
          $arrObjMdAbcContratoDTO[] = $objMdAbcContratoDTO;
        }
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoRN->reativar($arrObjMdAbcContratoDTO);
        PaginaSEI::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        PaginaSEI::getInstance()->processarExcecao($e);
      } 
      header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao_origem').'&acao_origem='.PaginaSEI::GET('acao')));
      die;

    */

    case 'md_abc_contrato_selecionar':
      $strTitulo = PaginaSEI::getInstance()->getTituloSelecao('Selecionar Contrato','Selecionar Contratos');

      //Se cadastrou alguem
      if (PaginaSEI::GET('acao_origem')==='md_abc_contrato_cadastrar' && isset($_GET['id_md_abc_contrato'])) {
        PaginaSEI::getInstance()->adicionarSelecionado(PaginaSEI::GET('id_md_abc_contrato'));
      }
      break;

    case 'md_abc_contrato_listar':
      $strTitulo = 'Contratos';
      break;

    default:
      throw new InfraException("Ação '".PaginaSEI::GET('acao')."' não reconhecida.");
  }

  $arrComandos = array();
  if (PaginaSEI::GET('acao')==='md_abc_contrato_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  /* if (PaginaSEI::GET('acao')==='md_abc_contrato_listar' || PaginaSEI::GET('acao')==='md_abc_contrato_selecionar') { */
    $bolAcaoCadastrar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNovo" value="Novo" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_cadastrar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ovo</button>';
    }
  /* } */

  $objMdAbcContratoDTO = new MdAbcContratoDTO();
  $objMdAbcContratoDTO->retNumIdMdAbcContrato();
  //$objMdAbcContratoDTO->retStrNumero();
  //$objMdAbcContratoDTO->retDtaAssinatura();
  //$objMdAbcContratoDTO->retDinValor();
  //$objMdAbcContratoDTO->retStrObservacao();
  $numIdMdAbcAquisicao = PaginaSEI::getInstance()->recuperarCampo('selMdAbcAquisicao');
  if ($numIdMdAbcAquisicao!=='') {
    $objMdAbcContratoDTO->setNumIdMdAbcAquisicao($numIdMdAbcAquisicao);
  }

/* 
  if (PaginaSEI::GET('acao')==='md_abc_contrato_reativar') {
    //Lista somente inativos
    $objMdAbcContratoDTO->setBolExclusaoLogica(false);
    $objMdAbcContratoDTO->setStrSinAtivo('N');
  }
 */
  PaginaSEI::getInstance()->prepararOrdenacao($objMdAbcContratoDTO, 'IdMdAbcContrato', InfraDTO::$TIPO_ORDENACAO_ASC);
  //PaginaSEI::getInstance()->prepararPaginacao($objMdAbcContratoDTO);

  $objMdAbcContratoRN = new MdAbcContratoRN();
  $arrObjMdAbcContratoDTO = $objMdAbcContratoRN->listar($objMdAbcContratoDTO);

  //PaginaSEI::getInstance()->processarPaginacao($objMdAbcContratoDTO);

  /** @var MdAbcContratoDTO[] $arrObjMdAbcContratoDTO */

  $numRegistros = count($arrObjMdAbcContratoDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (PaginaSEI::GET('acao')==='md_abc_contrato_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
/*     } elseif (PaginaSEI::GET('acao')==='md_abc_contrato_reativar') {
      $bolAcaoReativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_reativar');
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_excluir');
      $bolAcaoDesativar = false;
 */    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_consultar');
      $bolAcaoAlterar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = SessaoSEI::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_excluir');
      $bolAcaoDesativar = SessaoSEI::getInstance()->verificarPermissao('md_abc_contrato_desativar');
    }

    /* 
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_desativar&acao_origem='.PaginaSEI::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_reativar&acao_origem='.PaginaSEI::GET('acao').'&acao_confirmada=sim');
    }
     */

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_excluir&acao_origem='.PaginaSEI::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    /* if (PaginaSEI::GET('acao')!=='md_abc_contrato_reativar') { */
      $strCaptionTabela = 'Contratos';
    /* } else {
      $strCaptionTabela = 'Contratos Inativos';
    } */

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.PaginaSEI::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.PaginaSEI::getInstance()->getThCheck().'</th>'."\n";
    }
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Número','Numero',$arrObjMdAbcContratoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Data de Assinatura','Assinatura',$arrObjMdAbcContratoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Valor','Valor',$arrObjMdAbcContratoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.PaginaSEI::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Observação','Observacao',$arrObjMdAbcContratoDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">Ações</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.PaginaSEI::getInstance()->getTrCheck($i,$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato(),$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato()).'</td>';
      }
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcContratoDTO[$i]->getStrNumero()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcContratoDTO[$i]->getDtaAssinatura()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcContratoDTO[$i]->getDinValor()).'</td>';
      //$strResultado .= '<td>'.PaginaSEI::tratarHTML($arrObjMdAbcContratoDTO[$i]->getStrObservacao()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= PaginaSEI::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_consultar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeConsultar().'" title="Consultar Contrato" alt="Consultar Contrato" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.SessaoSEI::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_alterar&acao_origem='.PaginaSEI::GET('acao').'&acao_retorno='.PaginaSEI::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato()).'" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeAlterar().'" title="Alterar Contrato" alt="Alterar Contrato" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato();
        $strDescricao = PaginaSEI::getInstance()->formatarParametrosJavaScript($arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato());
      }
/* 
      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeDesativar().'" title="Desativar Contrato" alt="Desativar Contrato" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeReativar().'" title="Reativar Contrato" alt="Reativar Contrato" class="infraImg" /></a>&nbsp;';
      }
 */

      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.PaginaSEI::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.PaginaSEI::getInstance()->getProxTabTabela().'"><img src="'.PaginaSEI::getInstance()->getIconeExcluir().'" title="Excluir Contrato" alt="Excluir Contrato" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (PaginaSEI::GET('acao')==='md_abc_contrato_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

  $strItensSelMdAbcAquisicao = MdAbcAquisicaoINT::montarSelectDescricao('','Todos',$numIdMdAbcAquisicao);
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
#lblMdAbcAquisicao {position:absolute;left:0;top:0;width:25%;}
#selMdAbcAquisicao {position:absolute;left:0;top:40%;width:25%;}

<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_contrato_selecionar') {
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
  if (confirm('Confirma desativação do Contrato \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcContratoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcContratoLista').submit();
  }
}

function acaoDesativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Contrato selecionado.');
    return;
  }
  if (confirm('Confirma desativação dos Contratos selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcContratoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcContratoLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoReativar??false) { ?>
function acaoReativar(id,desc)
{
  if (confirm('Confirma reativação do Contrato \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcContratoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcContratoLista').submit();
  }
}

function acaoReativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Contrato selecionado.');
    return;
  }
  if (confirm('Confirma reativação dos Contratos selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcContratoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcContratoLista').submit();
  }
}
<?php }  */?>

<?php if ($bolAcaoExcluir??false) { ?>
function acaoExcluir(id,desc)
{
  if (confirm('Confirma exclusão do Contrato \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcContratoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcContratoLista').submit();
  }
}

function acaoExclusaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhum Contrato selecionado.');
    return;
  }
  if (confirm('Confirma exclusão dos Contratos selecionados?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcContratoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcContratoLista').submit();
  }
}
<?php } ?>

<?php if(0){?></script><?php }?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcContratoLista" method="post" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
  <?php
  PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
  PaginaSEI::getInstance()->abrirAreaDados('5em');
  ?>
  <label id="lblMdAbcAquisicao" for="selMdAbcAquisicao" accesskey="a" class="infraLabelOpcional"><span class="infraTeclaAtalho">A</span>quisição:</label>
  <select id="selMdAbcAquisicao" name="selMdAbcAquisicao" onchange="this.form.submit();" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" >
  <?=$strItensSelMdAbcAquisicao??false?>
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
