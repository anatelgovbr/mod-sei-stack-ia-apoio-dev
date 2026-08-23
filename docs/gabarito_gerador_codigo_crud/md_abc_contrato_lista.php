<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * Versão do Gerador de Código: 1.46.4
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

  Paginaabc::getInstance()->prepararSelecao('md_abc_contrato_selecionar');

  Paginaabc::getInstance()->salvarCamposPost(array('selMdAbcAquisicao'));

  switch ($_GET['acao']) {
    case 'md_abc_contrato_excluir':
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcContratoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcContratoDTO = new MdAbcContratoDTO();
          $objMdAbcContratoDTO->setNumIdMdAbcContrato($strId);
          $arrObjMdAbcContratoDTO[] = $objMdAbcContratoDTO;
        }
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoRN->excluir($arrObjMdAbcContratoDTO);
        Paginaabc::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    /*
    case 'md_abc_contrato_desativar':
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcContratoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcContratoDTO = new MdAbcContratoDTO();
          $objMdAbcContratoDTO->setNumIdMdAbcContrato($strId);
          $arrObjMdAbcContratoDTO[] = $objMdAbcContratoDTO;
        }
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoRN->desativar($arrObjMdAbcContratoDTO);
        Paginaabc::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    case 'md_abc_contrato_reativar':
      $strTitulo = 'Reativar Contratos';
      if (Paginaabc::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcContratoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcContratoDTO = new MdAbcContratoDTO();
          $objMdAbcContratoDTO->setNumIdMdAbcContrato($strId);
          $arrObjMdAbcContratoDTO[] = $objMdAbcContratoDTO;
        }
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoRN->reativar($arrObjMdAbcContratoDTO);
        Paginaabc::getInstance()->adicionarMensagem('Operação realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    */

    case 'md_abc_contrato_selecionar':
      $strTitulo = Paginaabc::getInstance()->getTituloSelecao('Selecionar Contrato','Selecionar Contratos');

      //Se cadastrou alguem
      if (Paginaabc::GET('acao_origem')==='md_abc_contrato_cadastrar' && isset($_GET['id_md_abc_contrato'])) {
        Paginaabc::getInstance()->adicionarSelecionado(Paginaabc::GET('id_md_abc_contrato'));
      }
      break;

    case 'md_abc_contrato_listar':
      $strTitulo = 'Contratos';
      break;

    default:
      throw new InfraException("Ação '".Paginaabc::GET('acao')."' não reconhecida.");
  }

  $arrComandos = array();
  if (Paginaabc::GET('acao')==='md_abc_contrato_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  /* if (Paginaabc::GET('acao')==='md_abc_contrato_listar' || Paginaabc::GET('acao')==='md_abc_contrato_selecionar') { */
    $bolAcaoCadastrar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNovo" value="Novo" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_cadastrar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ovo</button>';
    }
  /* } */

  $objMdAbcContratoDTO = new MdAbcContratoDTO();
  $objMdAbcContratoDTO->retNumIdMdAbcContrato();
  //$objMdAbcContratoDTO->retStrNumero();
  //$objMdAbcContratoDTO->retDtaAssinatura();
  //$objMdAbcContratoDTO->retDinValor();
  //$objMdAbcContratoDTO->retStrObservacao();
  $numIdMdAbcAquisicao = Paginaabc::getInstance()->recuperarCampo('selMdAbcAquisicao');
  if ($numIdMdAbcAquisicao!=='') {
    $objMdAbcContratoDTO->setNumIdMdAbcAquisicao($numIdMdAbcAquisicao);
  }

/* 
  if (Paginaabc::GET('acao')==='md_abc_contrato_reativar') {
    //Lista somente inativos
    $objMdAbcContratoDTO->setBolExclusaoLogica(false);
    $objMdAbcContratoDTO->setStrSinAtivo('N');
  }
 */
  Paginaabc::getInstance()->prepararOrdenacao($objMdAbcContratoDTO, 'IdMdAbcContrato', InfraDTO::$TIPO_ORDENACAO_ASC);
  //Paginaabc::getInstance()->prepararPaginacao($objMdAbcContratoDTO);

  $objMdAbcContratoRN = new MdAbcContratoRN();
  $arrObjMdAbcContratoDTO = $objMdAbcContratoRN->listar($objMdAbcContratoDTO);

  //Paginaabc::getInstance()->processarPaginacao($objMdAbcContratoDTO);

  /** @var MdAbcContratoDTO[] $arrObjMdAbcContratoDTO */

  $numRegistros = count($arrObjMdAbcContratoDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (Paginaabc::GET('acao')==='md_abc_contrato_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_consultar');
      $bolAcaoAlterar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
/*     } elseif (Paginaabc::GET('acao')==='md_abc_contrato_reativar') {
      $bolAcaoReativar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_reativar');
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = Sessaoabc::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_excluir');
      $bolAcaoDesativar = false;
 */    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_consultar');
      $bolAcaoAlterar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = Sessaoabc::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_excluir');
      $bolAcaoDesativar = Sessaoabc::getInstance()->verificarPermissao('md_abc_contrato_desativar');
    }

    /* 
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_desativar&acao_origem='.Paginaabc::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_reativar&acao_origem='.Paginaabc::GET('acao').'&acao_confirmada=sim');
    }
     */

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_excluir&acao_origem='.Paginaabc::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    /* if (Paginaabc::GET('acao')!=='md_abc_contrato_reativar') { */
      $strCaptionTabela = 'Contratos';
    /* } else {
      $strCaptionTabela = 'Contratos Inativos';
    } */

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.Paginaabc::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.Paginaabc::getInstance()->getThCheck().'</th>'."\n";
    }
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Número','Numero',$arrObjMdAbcContratoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Data de Assinatura','Assinatura',$arrObjMdAbcContratoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Valor','Valor',$arrObjMdAbcContratoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcContratoDTO,'Observação','Observacao',$arrObjMdAbcContratoDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">Ações</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.Paginaabc::getInstance()->getTrCheck($i,$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato(),$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato()).'</td>';
      }
      //$strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcContratoDTO[$i]->getStrNumero()).'</td>';
      //$strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcContratoDTO[$i]->getDtaAssinatura()).'</td>';
      //$strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcContratoDTO[$i]->getDinValor()).'</td>';
      //$strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcContratoDTO[$i]->getStrObservacao()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= Paginaabc::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_consultar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato()).'" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeConsultar().'" title="Consultar Contrato" alt="Consultar Contrato" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_contrato_alterar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato()).'" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeAlterar().'" title="Alterar Contrato" alt="Alterar Contrato" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato();
        $strDescricao = Paginaabc::getInstance()->formatarParametrosJavaScript($arrObjMdAbcContratoDTO[$i]->getNumIdMdAbcContrato());
      }
/* 
      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeDesativar().'" title="Desativar Contrato" alt="Desativar Contrato" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeReativar().'" title="Reativar Contrato" alt="Reativar Contrato" class="infraImg" /></a>&nbsp;';
      }
 */

      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeExcluir().'" title="Excluir Contrato" alt="Excluir Contrato" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (Paginaabc::GET('acao')==='md_abc_contrato_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

  $strItensSelMdAbcAquisicao = MdAbcAquisicaoINT::montarSelect???????('','Todos',$numIdMdAbcAquisicao);
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
#lblMdAbcAquisicao {position:absolute;left:0;top:0;width:25%;}
#selMdAbcAquisicao {position:absolute;left:0;top:40%;width:25%;}

<?php if(0){?></style><?php }?>
<?php
Paginaabc::getInstance()->fecharStyle();
Paginaabc::getInstance()->montarJavaScript();
Paginaabc::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_contrato_selecionar') {
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
Paginaabc::getInstance()->fecharJavaScript();
Paginaabc::getInstance()->fecharHead();
Paginaabc::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcContratoLista" method="post" action="<?=Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao').'&acao_origem='.Paginaabc::GET('acao'))?>">
  <?php
  Paginaabc::getInstance()->montarBarraComandosSuperior($arrComandos??false);
  Paginaabc::getInstance()->abrirAreaDados('5em');
  ?>
  <label id="lblMdAbcAquisicao" for="selMdAbcAquisicao" accesskey="a" class="infraLabelOpcional"><span class="infraTeclaAtalho">A</span>quisição:</label>
  <select id="selMdAbcAquisicao" name="selMdAbcAquisicao" onchange="this.form.submit();" class="infraSelect" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" >
  <?=$strItensSelMdAbcAquisicao??false?>
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
