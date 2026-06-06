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

  Paginaabc::getInstance()->verificarSelecao('md_abc_rel_contrato_projeto_selecionar');

  Paginaabc::getInstance()->salvarCamposPost(array('selMdAbcContrato','selMdAbcProjeto'));

  $objMdAbcRelContratoProjetoDTO = new MdAbcRelContratoProjetoDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_rel_contrato_projeto_cadastrar':
      $strTitulo = 'Nova Associação';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcRelContratoProjeto" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $numIdMdAbcContrato = Paginaabc::getInstance()->recuperarCampo('selMdAbcContrato');
      if ($numIdMdAbcContrato !=='') {
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
      } else {
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato(null);
      }

      $numIdMdAbcProjeto = Paginaabc::getInstance()->recuperarCampo('selMdAbcProjeto');
      if ($numIdMdAbcProjeto !=='') {
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
      } else {
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto(null);
      }

      $objMdAbcRelContratoProjetoDTO->setDtaAssociacao(Paginaabc::POST('txtAssociacao'));

      if (isset($_POST['sbmCadastrarMdAbcRelContratoProjeto'])) {
        try {
          $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
          $objMdAbcRelContratoProjetoDTO = $objMdAbcRelContratoProjetoRN->cadastrar($objMdAbcRelContratoProjetoDTO);
          Paginaabc::getInstance()->adicionarMensagem('Associação "'.$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato().'" cadastrada com sucesso.');
          header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').'&id_md_abc_contrato='.$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato().'&id_md_abc_projeto='.$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcProjeto().Paginaabc::getInstance()->montarAncora($objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato().'-'.$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcProjeto())));
          die;
        } catch (Exception $e) {
          Paginaabc::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_rel_contrato_projeto_alterar':
      $strTitulo = 'Alterar Associação';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcRelContratoProjeto" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_contrato'], $_GET['id_md_abc_projeto'])) {
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato(Paginaabc::GET('id_md_abc_contrato'));
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto(Paginaabc::GET('id_md_abc_projeto'));
        $objMdAbcRelContratoProjetoDTO->retTodos();
        $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
        $objMdAbcRelContratoProjetoDTO = $objMdAbcRelContratoProjetoRN->consultar($objMdAbcRelContratoProjetoDTO);
        if ($objMdAbcRelContratoProjetoDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato(Paginaabc::POST('hdnIdMdAbcContrato'));
        $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto(Paginaabc::POST('hdnIdMdAbcProjeto'));
        $objMdAbcRelContratoProjetoDTO->setDtaAssociacao(Paginaabc::POST('txtAssociacao'));
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora($objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato().'-'.$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcProjeto())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcRelContratoProjeto'])) {
        try {
          $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
          $objMdAbcRelContratoProjetoRN->alterar($objMdAbcRelContratoProjetoDTO);
          Paginaabc::getInstance()->adicionarMensagem('Associação "'.$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato().'" alterada com sucesso.');
          header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora($objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato().'-'.$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcProjeto())));
          die;
        } catch (Exception $e) {
          Paginaabc::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_rel_contrato_projeto_consultar':
      $strTitulo = 'Consultar Associação';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora(Paginaabc::GET('id_md_abc_contrato').'-'.Paginaabc::GET('id_md_abc_projeto'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato(Paginaabc::GET('id_md_abc_contrato'));
      $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto(Paginaabc::GET('id_md_abc_projeto'));
      $objMdAbcRelContratoProjetoDTO->setBolExclusaoLogica(false);
      $objMdAbcRelContratoProjetoDTO->retTodos();
      $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
      $objMdAbcRelContratoProjetoDTO = $objMdAbcRelContratoProjetoRN->consultar($objMdAbcRelContratoProjetoDTO);
      if ($objMdAbcRelContratoProjetoDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . Paginaabc::GET('acao') . "' não reconhecida.");
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('null','&nbsp;',$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato());
  $strItensSelMdAbcProjeto = MdAbcProjetoINT::montarSelect???????('null','&nbsp;',$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcProjeto());

} catch(Exception $e) {
  Paginaabc::getInstance()->processarExcecao($e);
}

Paginaabc::getInstance()->montarDocType();
Paginaabc::getInstance()->abrirHtml();
Paginaabc::getInstance()->abrirHead();
Paginaabc::getInstance()->montarMeta();
Paginaabc::getInstance()->montarTitle(Paginaabc::getInstance()->getStrNomeSistema() . ' - ' . ($strTitulo??false));
Paginaabc::getInstance()->montarStyle();
Paginaabc::getInstance()->abrirStyle();
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
Paginaabc::getInstance()->fecharStyle();
Paginaabc::getInstance()->montarJavaScript();
Paginaabc::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_rel_contrato_projeto_cadastrar') {
    document.getElementById('selMdAbcContrato').focus();
  } else if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_rel_contrato_projeto_consultar') {
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
Paginaabc::getInstance()->fecharJavaScript();
Paginaabc::getInstance()->fecharHead();
Paginaabc::getInstance()->abrirBody($strTitulo??false,'onload="inicializar();"');
?>
<form id="frmMdAbcRelContratoProjetoCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao').'&acao_origem='.Paginaabc::GET('acao'))?>">
<?php
Paginaabc::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//Paginaabc::getInstance()->montarAreaValidacao();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcContrato" for="selMdAbcContrato" accesskey="o" class="infraLabelObrigatorio">C<span class="infraTeclaAtalho">o</span>ntrato:</label>
  <select id="selMdAbcContrato" name="selMdAbcContrato" class="infraSelect" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" <?=$strDesabilitar?>>
  <?=$strItensSelMdAbcContrato??false?>
  </select>
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcProjeto" for="selMdAbcProjeto" accesskey="o" class="infraLabelObrigatorio">Pr<span class="infraTeclaAtalho">o</span>jeto:</label>
  <select id="selMdAbcProjeto" name="selMdAbcProjeto" class="infraSelect" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" <?=$strDesabilitar?>>
  <?=$strItensSelMdAbcProjeto??false?>
  </select>
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblAssociacao" for="txtAssociacao" accesskey="a" class="infraLabelObrigatorio">D<span class="infraTeclaAtalho">a</span>ta de Associação:</label>
  <input type="text" id="txtAssociacao" name="txtAssociacao" onkeypress="return infraMascaraData(this, event)" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcRelContratoProjetoDTO->getDtaAssociacao())?>" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
  <img id="imgCalAssociacao" title="Selecionar Data de Associação" alt="Selecionar Data de Associação" src="<?=Paginaabc::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario('txtAssociacao',this);" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcContrato" name="hdnIdMdAbcContrato" value="<?=$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcContrato()?>" />
  <input type="hidden" id="hdnIdMdAbcProjeto" name="hdnIdMdAbcProjeto" value="<?=$objMdAbcRelContratoProjetoDTO->getNumIdMdAbcProjeto()?>" />
  <?php
  //Paginaabc::getInstance()->montarAreaDebug();
  Paginaabc::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
Paginaabc::getInstance()->fecharBody();
Paginaabc::getInstance()->fecharHtml();
