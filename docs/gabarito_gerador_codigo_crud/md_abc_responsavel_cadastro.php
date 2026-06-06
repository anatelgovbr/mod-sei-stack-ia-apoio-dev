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

  Paginaabc::getInstance()->verificarSelecao('md_abc_responsavel_selecionar');

  Paginaabc::getInstance()->salvarCamposPost(array('selMdAbcContrato'));

  $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_responsavel_cadastrar':
      $strTitulo = 'Novo Responsável';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcResponsavel" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(null);
      $numIdMdAbcContrato = Paginaabc::getInstance()->recuperarCampo('selMdAbcContrato');
      if ($numIdMdAbcContrato !=='') {
        $objMdAbcResponsavelDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
      } else {
        $objMdAbcResponsavelDTO->setNumIdMdAbcContrato(null);
      }

      $objMdAbcResponsavelDTO->setStrNome(Paginaabc::POST('txtNome'));
      $objMdAbcResponsavelDTO->setStrCargo(Paginaabc::POST('txtCargo'));
      $objMdAbcResponsavelDTO->setStrEmail(Paginaabc::POST('txtEmail'));

      if (isset($_POST['sbmCadastrarMdAbcResponsavel'])) {
        try {
          $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
          $objMdAbcResponsavelDTO = $objMdAbcResponsavelRN->cadastrar($objMdAbcResponsavelDTO);
          Paginaabc::getInstance()->adicionarMensagem('Responsável "'.$objMdAbcResponsavelDTO->getStrNome().'" cadastrado com sucesso.');
          header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').'&id_md_abc_responsavel='.$objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel().Paginaabc::getInstance()->montarAncora($objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel())));
          die;
        } catch (Exception $e) {
          Paginaabc::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_responsavel_alterar':
      $strTitulo = 'Alterar Responsável';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcResponsavel" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_responsavel'])) {
        $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(Paginaabc::GET('id_md_abc_responsavel'));
        $objMdAbcResponsavelDTO->retTodos();
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelDTO = $objMdAbcResponsavelRN->consultar($objMdAbcResponsavelDTO);
        if ($objMdAbcResponsavelDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(Paginaabc::POST('hdnIdMdAbcResponsavel'));
        $objMdAbcResponsavelDTO->setNumIdMdAbcContrato(Paginaabc::POST('selMdAbcContrato'));
        $objMdAbcResponsavelDTO->setStrNome(Paginaabc::POST('txtNome'));
        $objMdAbcResponsavelDTO->setStrCargo(Paginaabc::POST('txtCargo'));
        $objMdAbcResponsavelDTO->setStrEmail(Paginaabc::POST('txtEmail'));
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora($objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcResponsavel'])) {
        try {
          $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
          $objMdAbcResponsavelRN->alterar($objMdAbcResponsavelDTO);
          Paginaabc::getInstance()->adicionarMensagem('Responsável "'.$objMdAbcResponsavelDTO->getStrNome().'" alterado com sucesso.');
          header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora($objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel())));
          die;
        } catch (Exception $e) {
          Paginaabc::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_responsavel_consultar':
      $strTitulo = 'Consultar Responsável';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora(Paginaabc::GET('id_md_abc_responsavel'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(Paginaabc::GET('id_md_abc_responsavel'));
      $objMdAbcResponsavelDTO->setBolExclusaoLogica(false);
      $objMdAbcResponsavelDTO->retTodos();
      $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
      $objMdAbcResponsavelDTO = $objMdAbcResponsavelRN->consultar($objMdAbcResponsavelDTO);
      if ($objMdAbcResponsavelDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . Paginaabc::GET('acao') . "' não reconhecida.");
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('null','&nbsp;',$objMdAbcResponsavelDTO->getNumIdMdAbcContrato());

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

#lblNome {position:absolute;left:0;top:0;width:95%;}
#txtNome {position:absolute;left:0;top:40%;width:95%;}

#lblCargo {position:absolute;left:0;top:0;width:50%;}
#txtCargo {position:absolute;left:0;top:40%;width:50%;}

#lblEmail {position:absolute;left:0;top:0;width:95%;}
#txtEmail {position:absolute;left:0;top:40%;width:95%;}

<?php if(0){?></style><?php }?>
<?php
Paginaabc::getInstance()->fecharStyle();
Paginaabc::getInstance()->montarJavaScript();
Paginaabc::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_responsavel_cadastrar') {
    document.getElementById('selMdAbcContrato').focus();
  } else if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_responsavel_consultar') {
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

  if (infraTrim(document.getElementById('txtNome').value)=='') {
    alert('Informe N Nome.');
    document.getElementById('txtNome').focus();
    return false;
  }

  if (infraTrim(document.getElementById('txtCargo').value)=='') {
    alert('Informe G Cargo.');
    document.getElementById('txtCargo').focus();
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
<form id="frmMdAbcResponsavelCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao').'&acao_origem='.Paginaabc::GET('acao'))?>">
<?php
Paginaabc::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//Paginaabc::getInstance()->montarAreaValidacao();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcContrato" for="selMdAbcContrato" accesskey="o" class="infraLabelObrigatorio">C<span class="infraTeclaAtalho">o</span>ntrato:</label>
  <select id="selMdAbcContrato" name="selMdAbcContrato" class="infraSelect" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>">
  <?=$strItensSelMdAbcContrato??false?>
  </select>
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblNome" for="txtNome" accesskey="o" class="infraLabelObrigatorio">N<span class="infraTeclaAtalho">o</span>me:</label>
  <input type="text" id="txtNome" name="txtNome" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcResponsavelDTO->getStrNome())?>" onkeypress="return infraMascaraTexto(this,event,100);" maxlength="100" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblCargo" for="txtCargo" accesskey="o" class="infraLabelObrigatorio">Carg<span class="infraTeclaAtalho">o</span>:</label>
  <input type="text" id="txtCargo" name="txtCargo" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcResponsavelDTO->getStrCargo())?>" onkeypress="return infraMascaraTexto(this,event,50);" maxlength="50" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblEmail" for="txtEmail" accesskey="o" class="infraLabelOpcional">E-mail:</label>
  <input type="text" id="txtEmail" name="txtEmail" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcResponsavelDTO->getStrEmail())?>" onkeypress="return infraMascaraTexto(this,event,100);" maxlength="100" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcResponsavel" name="hdnIdMdAbcResponsavel" value="<?=$objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel()?>" />
  <?php
  //Paginaabc::getInstance()->montarAreaDebug();
  Paginaabc::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
Paginaabc::getInstance()->fecharBody();
Paginaabc::getInstance()->fecharHtml();
