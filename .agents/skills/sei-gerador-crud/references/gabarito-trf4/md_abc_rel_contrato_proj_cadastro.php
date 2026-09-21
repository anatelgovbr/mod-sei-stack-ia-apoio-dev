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

  PaginaSEI::getInstance()->verificarSelecao('md_abc_rel_contrato_proj_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcContrato','selMdAbcProjeto'));

  $objMdAbcRelContratoProjDTO = new MdAbcRelContratoProjDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_rel_contrato_proj_cadastrar':
      $strTitulo = 'Nova Associação';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcRelContratoProj" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $numIdMdAbcContrato = PaginaSEI::getInstance()->recuperarCampo('selMdAbcContrato');
      if ($numIdMdAbcContrato !=='') {
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
      } else {
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato(null);
      }

      $numIdMdAbcProjeto = PaginaSEI::getInstance()->recuperarCampo('selMdAbcProjeto');
      if ($numIdMdAbcProjeto !=='') {
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
      } else {
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto(null);
      }

      $objMdAbcRelContratoProjDTO->setDtaAssociacao(PaginaSEI::POST('txtAssociacao'));

      if (isset($_POST['sbmCadastrarMdAbcRelContratoProj'])) {
        try {
          $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
          $objMdAbcRelContratoProjDTO = $objMdAbcRelContratoProjRN->cadastrar($objMdAbcRelContratoProjDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Associação "'.$objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato().'" cadastrada com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').'&id_md_abc_contrato='.$objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato().'&id_md_abc_projeto='.$objMdAbcRelContratoProjDTO->getNumIdMdAbcProjeto().PaginaSEI::getInstance()->montarAncora($objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato().'-'.$objMdAbcRelContratoProjDTO->getNumIdMdAbcProjeto())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_rel_contrato_proj_alterar':
      $strTitulo = 'Alterar Associação';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcRelContratoProj" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_contrato'], $_GET['id_md_abc_projeto'])) {
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato(PaginaSEI::GET('id_md_abc_contrato'));
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto(PaginaSEI::GET('id_md_abc_projeto'));
        $objMdAbcRelContratoProjDTO->retTodos();
        $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
        $objMdAbcRelContratoProjDTO = $objMdAbcRelContratoProjRN->consultar($objMdAbcRelContratoProjDTO);
        if ($objMdAbcRelContratoProjDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato(PaginaSEI::POST('hdnIdMdAbcContrato'));
        $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto(PaginaSEI::POST('hdnIdMdAbcProjeto'));
        $objMdAbcRelContratoProjDTO->setDtaAssociacao(PaginaSEI::POST('txtAssociacao'));
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato().'-'.$objMdAbcRelContratoProjDTO->getNumIdMdAbcProjeto())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcRelContratoProj'])) {
        try {
          $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
          $objMdAbcRelContratoProjRN->alterar($objMdAbcRelContratoProjDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Associação "'.$objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato().'" alterada com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato().'-'.$objMdAbcRelContratoProjDTO->getNumIdMdAbcProjeto())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_rel_contrato_proj_consultar':
      $strTitulo = 'Consultar Associação';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora(PaginaSEI::GET('id_md_abc_contrato').'-'.PaginaSEI::GET('id_md_abc_projeto'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato(PaginaSEI::GET('id_md_abc_contrato'));
      $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto(PaginaSEI::GET('id_md_abc_projeto'));
      $objMdAbcRelContratoProjDTO->setBolExclusaoLogica(false);
      $objMdAbcRelContratoProjDTO->retTodos();
      $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
      $objMdAbcRelContratoProjDTO = $objMdAbcRelContratoProjRN->consultar($objMdAbcRelContratoProjDTO);
      if ($objMdAbcRelContratoProjDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . PaginaSEI::GET('acao') . "' não reconhecida.");
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('null','&nbsp;',$objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato());
  $strItensSelMdAbcProjeto = MdAbcProjetoINT::montarSelectIdentificacao('null','&nbsp;',$objMdAbcRelContratoProjDTO->getNumIdMdAbcProjeto());

} catch(Exception $e) {
  PaginaSEI::getInstance()->processarExcecao($e);
}

PaginaSEI::getInstance()->montarDocType();
PaginaSEI::getInstance()->abrirHtml();
PaginaSEI::getInstance()->abrirHead();
PaginaSEI::getInstance()->montarMeta();
PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema() . ' - ' . ($strTitulo??false));
PaginaSEI::getInstance()->montarStyle();
PaginaSEI::getInstance()->abrirStyle();
?>
<?php if(0){?><style><?php }?>
#lblMdAbcContrato {position:absolute;left:0;top:0;width:25%;}
#selMdAbcContrato {position:absolute;left:0;top:40%;width:25%;}

#lblMdAbcProjeto {position:absolute;left:0;top:0;width:25%;}
#selMdAbcProjeto {position:absolute;left:0;top:40%;width:25%;}

#lblAssociacao {position:absolute;left:0;top:0;width:25%;}
#txtAssociacao {position:absolute;left:0;top:40%;width:25%;}
#imgCalAssociacao {position:absolute;left:26%;top:45%;}

<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_rel_contrato_proj_cadastrar') {
    document.getElementById('selMdAbcContrato').focus();
  } else if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_rel_contrato_proj_consultar') {
    infraDesabilitarCamposAreaDados();
  } else {
    document.getElementById('btnCancelar').focus();
  }
  infraEfeitoTabelas(true);
}

function validarCadastro()
{
  if (!infraSelectSelecionado('selMdAbcContrato')) {
    alert('Selecione um Contrato.');
    document.getElementById('selMdAbcContrato').focus();
    return false;
  }

  if (!infraSelectSelecionado('selMdAbcProjeto')) {
    alert('Selecione um Projeto.');
    document.getElementById('selMdAbcProjeto').focus();
    return false;
  }

  if (infraTrim(document.getElementById('txtAssociacao').value)=='') {
    alert('Informe D Data de Associação.');
    document.getElementById('txtAssociacao').focus();
    return false;
  }

  if (!infraValidarData(document.getElementById('txtAssociacao'))) {
    return false;
  }

  return true;
}

function OnSubmitForm()
{
  return validarCadastro();
}

<?php if(0){?></script><?php }?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false,'onload="inicializar();"');
?>
<form id="frmMdAbcRelContratoProjCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
<?php
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//PaginaSEI::getInstance()->montarAreaValidacao();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcContrato" for="selMdAbcContrato" accesskey="o" class="infraLabelObrigatorio">C<span class="infraTeclaAtalho">o</span>ntrato:</label>
  <select id="selMdAbcContrato" name="selMdAbcContrato" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" <?=$strDesabilitar?>>
  <?=$strItensSelMdAbcContrato??false?>
  </select>
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcProjeto" for="selMdAbcProjeto" accesskey="o" class="infraLabelObrigatorio">Pr<span class="infraTeclaAtalho">o</span>jeto:</label>
  <select id="selMdAbcProjeto" name="selMdAbcProjeto" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" <?=$strDesabilitar?>>
  <?=$strItensSelMdAbcProjeto??false?>
  </select>
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblAssociacao" for="txtAssociacao" accesskey="a" class="infraLabelObrigatorio">D<span class="infraTeclaAtalho">a</span>ta de Associação:</label>
  <input type="text" id="txtAssociacao" name="txtAssociacao" onkeypress="return infraMascaraData(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcRelContratoProjDTO->getDtaAssociacao())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
  <img id="imgCalAssociacao" title="Selecionar Data de Associação" alt="Selecionar Data de Associação" src="<?=PaginaSEI::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario('txtAssociacao',this);" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcContrato" name="hdnIdMdAbcContrato" value="<?=$objMdAbcRelContratoProjDTO->getNumIdMdAbcContrato()?>" />
  <input type="hidden" id="hdnIdMdAbcProjeto" name="hdnIdMdAbcProjeto" value="<?=$objMdAbcRelContratoProjDTO->getNumIdMdAbcProjeto()?>" />
  <?php
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
