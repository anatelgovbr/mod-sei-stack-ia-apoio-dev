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

  Paginaabc::getInstance()->prepararSelecao('md_abc_rel_contrato_projeto_selecionar');

  Paginaabc::getInstance()->salvarCamposPost(array('selMdAbcContrato','selMdAbcProjeto'));

  switch ($_GET['acao']) {
    case 'md_abc_rel_contrato_projeto_excluir':
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcRelContratoProjetoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcRelContratoProjetoDTO = new MdAbcRelContratoProjetoDTO();
           $arrStrIdComposto = explode('-',$strId);
          $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato($arrStrIdComposto[1]);
          $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto($arrStrIdComposto[2]);
          $arrObjMdAbcRelContratoProjetoDTO[] = $objMdAbcRelContratoProjetoDTO;
        }
        $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
        $objMdAbcRelContratoProjetoRN->excluir($arrObjMdAbcRelContratoProjetoDTO);
        Paginaabc::getInstance()->adicionarMensagem('OperaÃ§Ã£o realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    /*
    case 'md_abc_rel_contrato_projeto_desativar':
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcRelContratoProjetoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcRelContratoProjetoDTO = new MdAbcRelContratoProjetoDTO();
           $arrStrIdComposto = explode('-',$strId);
          $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato($arrStrIdComposto[1]);
          $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto($arrStrIdComposto[2]);
          $arrObjMdAbcRelContratoProjetoDTO[] = $objMdAbcRelContratoProjetoDTO;
        }
        $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
        $objMdAbcRelContratoProjetoRN->desativar($arrObjMdAbcRelContratoProjetoDTO);
        Paginaabc::getInstance()->adicionarMensagem('OperaÃ§Ã£o realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    case 'md_abc_rel_contrato_projeto_reativar':
      $strTitulo = 'Reativar AssociaÃ§Ãµes';
      if (Paginaabc::GET('acao_confirmada')!=='sim') {
        break;
      }
      try {
        $arrStrIds = Paginaabc::getInstance()->getArrStrItensSelecionados();
        $arrObjMdAbcRelContratoProjetoDTO = array();
        foreach ($arrStrIds as $strId) {
          $objMdAbcRelContratoProjetoDTO = new MdAbcRelContratoProjetoDTO();
           $arrStrIdComposto = explode('-',$strId);
          $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato($arrStrIdComposto[1]);
          $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto($arrStrIdComposto[2]);
          $arrObjMdAbcRelContratoProjetoDTO[] = $objMdAbcRelContratoProjetoDTO;
        }
        $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
        $objMdAbcRelContratoProjetoRN->reativar($arrObjMdAbcRelContratoProjetoDTO);
        Paginaabc::getInstance()->adicionarMensagem('OperaÃ§Ã£o realizada com sucesso.');
      } catch (Exception $e) {
        Paginaabc::getInstance()->processarExcecao($e);
      } 
      header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao_origem').'&acao_origem='.Paginaabc::GET('acao')));
      die;

    */

    case 'md_abc_rel_contrato_projeto_selecionar':
      $strTitulo = Paginaabc::getInstance()->getTituloSelecao('Selecionar AssociaÃ§Ã£o','Selecionar AssociaÃ§Ãµes');

      //Se cadastrou alguem
      if (Paginaabc::GET('acao_origem')==='md_abc_rel_contrato_projeto_cadastrar' && isset($_GET['id_md_abc_contrato'], $_GET['id_md_abc_projeto'])) {
        Paginaabc::getInstance()->adicionarSelecionado(Paginaabc::GET('id_md_abc_contrato').'-'.Paginaabc::GET('id_md_abc_projeto'));
      }
      break;

    case 'md_abc_rel_contrato_projeto_listar':
      $strTitulo = 'AssociaÃ§Ãµes';
      break;

    default:
      throw new InfraException("AÃ§Ã£o '".Paginaabc::GET('acao')."' nÃ£o reconhecida.");
  }

  $arrComandos = array();
  if (Paginaabc::GET('acao')==='md_abc_rel_contrato_projeto_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="T" id="btnTransportarSelecao" value="Transportar" onclick="infraTransportarSelecao();" class="infraButton"><span class="infraTeclaAtalho">T</span>ransportar</button>';
  }

  /* if (Paginaabc::GET('acao')==='md_abc_rel_contrato_projeto_listar' || Paginaabc::GET('acao')==='md_abc_rel_contrato_projeto_selecionar') { */
    $bolAcaoCadastrar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_cadastrar');
    if ($bolAcaoCadastrar) {
      $arrComandos[] = '<button type="button" accesskey="N" id="btnNova" value="Nova" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_projeto_cadastrar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">N</span>ova</button>';
    }
  /* } */

  $objMdAbcRelContratoProjetoDTO = new MdAbcRelContratoProjetoDTO();
  $objMdAbcRelContratoProjetoDTO->retNumIdMdAbcContrato();
  $objMdAbcRelContratoProjetoDTO->retNumIdMdAbcProjeto();
  //$objMdAbcRelContratoProjetoDTO->retDtaAssociacao();
  //$objMdAbcRelContratoProjetoDTO->retNumIdMdAbcContratoMdAbcContrato();
  $numIdMdAbcContrato = Paginaabc::getInstance()->recuperarCampo('selMdAbcContrato');
  if ($numIdMdAbcContrato!=='') {
    $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
  }

  $numIdMdAbcProjeto = Paginaabc::getInstance()->recuperarCampo('selMdAbcProjeto');
  if ($numIdMdAbcProjeto!=='') {
    $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
  }

/* 
  if (Paginaabc::GET('acao')==='md_abc_rel_contrato_projeto_reativar') {
    //Lista somente inativos
    $objMdAbcRelContratoProjetoDTO->setBolExclusaoLogica(false);
    $objMdAbcRelContratoProjetoDTO->setStrSinAtivo('N');
  }
 */
  Paginaabc::getInstance()->prepararOrdenacao($objMdAbcRelContratoProjetoDTO, 'IdMdAbcContrato', InfraDTO::$TIPO_ORDENACAO_ASC);
  //Paginaabc::getInstance()->prepararPaginacao($objMdAbcRelContratoProjetoDTO);

  $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
  $arrObjMdAbcRelContratoProjetoDTO = $objMdAbcRelContratoProjetoRN->listar($objMdAbcRelContratoProjetoDTO);

  //Paginaabc::getInstance()->processarPaginacao($objMdAbcRelContratoProjetoDTO);

  /** @var MdAbcRelContratoProjetoDTO[] $arrObjMdAbcRelContratoProjetoDTO */

  $numRegistros = count($arrObjMdAbcRelContratoProjetoDTO);

  if ($numRegistros > 0) {

    $bolCheck = false;

    if (Paginaabc::GET('acao')==='md_abc_rel_contrato_projeto_selecionar') {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_consultar');
      $bolAcaoAlterar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_alterar');
      $bolAcaoImprimir = false;
      //$bolAcaoGerarPlanilha = false;
      $bolAcaoExcluir = false;
      $bolAcaoDesativar = false;
      $bolCheck = true;
/*     } elseif (Paginaabc::GET('acao')==='md_abc_rel_contrato_projeto_reativar') {
      $bolAcaoReativar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_reativar');
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_consultar');
      $bolAcaoAlterar = false;
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = Sessaoabc::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_excluir');
      $bolAcaoDesativar = false;
 */    } else {
      $bolAcaoReativar = false;
      $bolAcaoConsultar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_consultar');
      $bolAcaoAlterar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_alterar');
      $bolAcaoImprimir = true;
      //$bolAcaoGerarPlanilha = Sessaoabc::getInstance()->verificarPermissao('infra_gerar_planilha_tabela');
      $bolAcaoExcluir = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_excluir');
      $bolAcaoDesativar = Sessaoabc::getInstance()->verificarPermissao('md_abc_rel_contrato_projeto_desativar');
    }

    /* 
    if ($bolAcaoDesativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="t" id="btnDesativar" value="Desativar" onclick="acaoDesativacaoMultipla();" class="infraButton">Desa<span class="infraTeclaAtalho">t</span>ivar</button>';
      $strLinkDesativar = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_projeto_desativar&acao_origem='.Paginaabc::GET('acao'));
    }

    if ($bolAcaoReativar) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="R" id="btnReativar" value="Reativar" onclick="acaoReativacaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">R</span>eativar</button>';
      $strLinkReativar = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_projeto_reativar&acao_origem='.Paginaabc::GET('acao').'&acao_confirmada=sim');
    }
     */

    if ($bolAcaoExcluir) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="E" id="btnExcluir" value="Excluir" onclick="acaoExclusaoMultipla();" class="infraButton"><span class="infraTeclaAtalho">E</span>xcluir</button>';
      $strLinkExcluir = Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_projeto_excluir&acao_origem='.Paginaabc::GET('acao'));
    }

    /*
    if ($bolAcaoGerarPlanilha) {
      $bolCheck = true;
      $arrComandos[] = '<button type="button" accesskey="P" id="btnGerarPlanilha" value="Gerar Planilha" onclick="infraGerarPlanilhaTabela(\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=infra_gerar_planilha_tabela').'\');" class="infraButton">Gerar <span class="infraTeclaAtalho">P</span>lanilha</button>';
    }
    */

    $strResultado = '';

    /* if (Paginaabc::GET('acao')!=='md_abc_rel_contrato_projeto_reativar') { */
      $strCaptionTabela = 'AssociaÃ§Ãµes';
    /* } else {
      $strCaptionTabela = 'AssociaÃ§Ãµes Inativas';
    } */

    $strResultado .= '<table style="width: 99%" class="infraTable">'."\n";
    $strResultado .= '<caption class="infraCaption">'.Paginaabc::getInstance()->gerarCaptionTabela($strCaptionTabela,$numRegistros).'</caption>';
    $strResultado .= '<thead><tr>';
    if ($bolCheck) {
       $strResultado .= '<th class="infraTh" style="width: 1%">'.Paginaabc::getInstance()->getThCheck().'</th>'."\n";
    }
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcRelContratoProjetoDTO,'Data de AssociaÃ§Ã£o','Associacao',$arrObjMdAbcRelContratoProjetoDTO).'</th>'."\n";
    //$strResultado .= '<th class="infraTh">'.Paginaabc::getInstance()->getThOrdenacao($objMdAbcRelContratoProjetoDTO,'Contrato','IdMdAbcContratoMdAbcContrato',$arrObjMdAbcRelContratoProjetoDTO).'</th>'."\n";
    $strResultado .= '<th class="infraTh">AÃ§Ãµes</th>'."\n";
    $strResultado .= '</tr></thead><tbody>'."\n";
    $strCssTr='';
    for($i = 0;$i < $numRegistros; $i++) {

      $strCssTr = ($strCssTr==='<tr class="infraTrClara">')?'<tr class="infraTrEscura">':'<tr class="infraTrClara">';
      $strResultado .= $strCssTr;

      if ($bolCheck) {
        $strResultado .= '<td style="vertical-align: center">'.Paginaabc::getInstance()->getTrCheck($i,$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContrato().'-'.$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcProjeto(),$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContrato()).'</td>';
      }
      //$strResultado .= '<td>'.Paginaabc::tratarHTML($arrObjMdAbcRelContratoProjetoDTO[$i]->getDtaAssociacao()).'</td>';
      //$strResultado .= '<td style="text-align: center">'.Paginaabc::tratarHTML($arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContratoMdAbcContrato()).'</td>';
      $strResultado .= '<td style="text-align: center">';

      $strResultado .= Paginaabc::getInstance()->getAcaoTransportarItem($i,$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContrato().'-'.$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcProjeto());

      if ($bolAcaoConsultar) {
        $strResultado .= '<a href="'.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_projeto_consultar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContrato().'&id_md_abc_projeto='.$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcProjeto()).'" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeConsultar().'" title="Consultar AssociaÃ§Ã£o" alt="Consultar AssociaÃ§Ã£o" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoAlterar) {
        $strResultado .= '<a href="'.Sessaoabc::getInstance()->assinarLink('controlador.php?acao=md_abc_rel_contrato_projeto_alterar&acao_origem='.Paginaabc::GET('acao').'&acao_retorno='.Paginaabc::GET('acao').'&id_md_abc_contrato='.$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContrato().'&id_md_abc_projeto='.$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcProjeto()).'" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeAlterar().'" title="Alterar AssociaÃ§Ã£o" alt="Alterar AssociaÃ§Ã£o" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoDesativar || $bolAcaoReativar || $bolAcaoExcluir) {
        $strId = $arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContrato().'-'.$arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcProjeto();
        $strDescricao = Paginaabc::getInstance()->formatarParametrosJavaScript($arrObjMdAbcRelContratoProjetoDTO[$i]->getNumIdMdAbcContrato());
      }
/* 
      if ($bolAcaoDesativar) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoDesativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeDesativar().'" title="Desativar AssociaÃ§Ã£o" alt="Desativar AssociaÃ§Ã£o" class="infraImg" /></a>&nbsp;';
      }

      if ($bolAcaoReativar) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoReativar(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeReativar().'" title="Reativar AssociaÃ§Ã£o" alt="Reativar AssociaÃ§Ã£o" class="infraImg" /></a>&nbsp;';
      }
 */

      if ($bolAcaoExcluir) {
        $strResultado .= '<a href="'.Paginaabc::getInstance()->montarAncora($strId).'" onclick="acaoExcluir(\''.$strId.'\',\''.$strDescricao.'\');" tabindex="'.Paginaabc::getInstance()->getProxTabTabela().'"><img src="'.Paginaabc::getInstance()->getIconeExcluir().'" title="Excluir AssociaÃ§Ã£o" alt="Excluir AssociaÃ§Ã£o" class="infraImg" /></a>&nbsp;';
      }

      $strResultado .= '</td></tr></tbody>'."\n";
    }
    $strResultado .= '</table>';
  }
  if (Paginaabc::GET('acao')==='md_abc_rel_contrato_projeto_selecionar') {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFecharSelecao" value="Fechar" onclick="window.close();" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  } else {
    $arrComandos[] = '<button type="button" accesskey="F" id="btnFechar" value="Fechar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao')).'\'" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('','Todos',$numIdMdAbcContrato);
  $strItensSelMdAbcProjeto = MdAbcProjetoINT::montarSelect???????('','Todos',$numIdMdAbcProjeto);
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

#lblMdAbcProjeto {position:absolute;left:0;top:0;width:25%;}
#selMdAbcProjeto {position:absolute;left:0;top:40%;width:25%;}

<?php if(0){?></style><?php }?>
<?php
Paginaabc::getInstance()->fecharStyle();
Paginaabc::getInstance()->montarJavaScript();
Paginaabc::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_rel_contrato_projeto_selecionar') {
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
  if (confirm('Confirma desativaÃ§Ã£o da AssociaÃ§Ã£o \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcRelContratoProjetoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjetoLista').submit();
  }
}

function acaoDesativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma AssociaÃ§Ã£o selecionada.');
    return;
  }
  if (confirm('Confirma desativaÃ§Ã£o das AssociaÃ§Ãµes selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcRelContratoProjetoLista').action='<?=$strLinkDesativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjetoLista').submit();
  }
}
<?php } ?>

<?php if ($bolAcaoReativar??false) { ?>
function acaoReativar(id,desc)
{
  if (confirm('Confirma reativaÃ§Ã£o da AssociaÃ§Ã£o \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcRelContratoProjetoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjetoLista').submit();
  }
}

function acaoReativacaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma AssociaÃ§Ã£o selecionada.');
    return;
  }
  if (confirm('Confirma reativaÃ§Ã£o das AssociaÃ§Ãµes selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcRelContratoProjetoLista').action='<?=$strLinkReativar??false?>';
    document.getElementById('frmMdAbcRelContratoProjetoLista').submit();
  }
}
<?php }  */?>

<?php if ($bolAcaoExcluir??false) { ?>
function acaoExcluir(id,desc)
{
  if (confirm('Confirma exclusÃ£o da AssociaÃ§Ã£o \"' + desc + '\"?')) {
    document.getElementById('hdnInfraItemId').value=id;
    document.getElementById('frmMdAbcRelContratoProjetoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcRelContratoProjetoLista').submit();
  }
}

function acaoExclusaoMultipla()
{
  if (document.getElementById('hdnInfraItensSelecionados').value=='') {
    alert('Nenhuma AssociaÃ§Ã£o selecionada.');
    return;
  }
  if (confirm('Confirma exclusÃ£o das AssociaÃ§Ãµes selecionadas?')) {
    document.getElementById('hdnInfraItemId').value='';
    document.getElementById('frmMdAbcRelContratoProjetoLista').action='<?=$strLinkExcluir??false?>';
    document.getElementById('frmMdAbcRelContratoProjetoLista').submit();
  }
}
<?php } ?>

<?php if(0){?></script><?php }?>
<?php
Paginaabc::getInstance()->fecharJavaScript();
Paginaabc::getInstance()->fecharHead();
Paginaabc::getInstance()->abrirBody($strTitulo??false, 'onload="inicializar();"');
?>
<form id="frmMdAbcRelContratoProjetoLista" method="post" action="<?=Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao').'&acao_origem='.Paginaabc::GET('acao'))?>">
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
  Paginaabc::getInstance()->abrirAreaDados('5em');
  ?>
  <label id="lblMdAbcProjeto" for="selMdAbcProjeto" accesskey="o" class="infraLabelOpcional">Pr<span class="infraTeclaAtalho">o</span>jeto:</label>
  <select id="selMdAbcProjeto" name="selMdAbcProjeto" onchange="this.form.submit();" class="infraSelect" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" >
  <?=$strItensSelMdAbcProjeto??false?>
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
