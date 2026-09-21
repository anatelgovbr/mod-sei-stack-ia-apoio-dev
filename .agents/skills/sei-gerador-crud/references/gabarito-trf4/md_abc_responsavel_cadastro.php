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

  PaginaSEI::getInstance()->verificarSelecao('md_abc_responsavel_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcContrato'));

  $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_responsavel_cadastrar':
      $strTitulo = 'Novo Responsável';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcResponsavel" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(null);
      $numIdMdAbcContrato = PaginaSEI::getInstance()->recuperarCampo('selMdAbcContrato');
      if ($numIdMdAbcContrato !=='') {
        $objMdAbcResponsavelDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
      } else {
        $objMdAbcResponsavelDTO->setNumIdMdAbcContrato(null);
      }

      $objMdAbcResponsavelDTO->setStrNome(PaginaSEI::POST('txtNome'));
      $objMdAbcResponsavelDTO->setStrCargo(PaginaSEI::POST('txtCargo'));
      $objMdAbcResponsavelDTO->setStrEmail(PaginaSEI::POST('txtEmail'));

      if (isset($_POST['sbmCadastrarMdAbcResponsavel'])) {
        try {
          $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
          $objMdAbcResponsavelDTO = $objMdAbcResponsavelRN->cadastrar($objMdAbcResponsavelDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Responsável "'.$objMdAbcResponsavelDTO->getStrNome().'" cadastrado com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').'&id_md_abc_responsavel='.$objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel().PaginaSEI::getInstance()->montarAncora($objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_responsavel_alterar':
      $strTitulo = 'Alterar Responsável';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcResponsavel" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_responsavel'])) {
        $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(PaginaSEI::GET('id_md_abc_responsavel'));
        $objMdAbcResponsavelDTO->retTodos();
        $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
        $objMdAbcResponsavelDTO = $objMdAbcResponsavelRN->consultar($objMdAbcResponsavelDTO);
        if ($objMdAbcResponsavelDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(PaginaSEI::POST('hdnIdMdAbcResponsavel'));
        $objMdAbcResponsavelDTO->setNumIdMdAbcContrato(PaginaSEI::POST('selMdAbcContrato'));
        $objMdAbcResponsavelDTO->setStrNome(PaginaSEI::POST('txtNome'));
        $objMdAbcResponsavelDTO->setStrCargo(PaginaSEI::POST('txtCargo'));
        $objMdAbcResponsavelDTO->setStrEmail(PaginaSEI::POST('txtEmail'));
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcResponsavel'])) {
        try {
          $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
          $objMdAbcResponsavelRN->alterar($objMdAbcResponsavelDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Responsável "'.$objMdAbcResponsavelDTO->getStrNome().'" alterado com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_responsavel_consultar':
      $strTitulo = 'Consultar Responsável';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora(PaginaSEI::GET('id_md_abc_responsavel'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcResponsavelDTO->setNumIdMdAbcResponsavel(PaginaSEI::GET('id_md_abc_responsavel'));
      $objMdAbcResponsavelDTO->setBolExclusaoLogica(false);
      $objMdAbcResponsavelDTO->retTodos();
      $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
      $objMdAbcResponsavelDTO = $objMdAbcResponsavelRN->consultar($objMdAbcResponsavelDTO);
      if ($objMdAbcResponsavelDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . PaginaSEI::GET('acao') . "' não reconhecida.");
  }

  $strItensSelMdAbcContrato = MdAbcContratoINT::montarSelectIdMdAbcContrato('null','&nbsp;',$objMdAbcResponsavelDTO->getNumIdMdAbcContrato());

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

#lblNome {position:absolute;left:0;top:0;width:95%;}
#txtNome {position:absolute;left:0;top:40%;width:95%;}

#lblCargo {position:absolute;left:0;top:0;width:50%;}
#txtCargo {position:absolute;left:0;top:40%;width:50%;}

#lblEmail {position:absolute;left:0;top:0;width:95%;}
#txtEmail {position:absolute;left:0;top:40%;width:95%;}

<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_responsavel_cadastrar') {
    document.getElementById('selMdAbcContrato').focus();
  } else if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_responsavel_consultar') {
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
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false,'onload="inicializar();"');
?>
<form id="frmMdAbcResponsavelCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
<?php
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//PaginaSEI::getInstance()->montarAreaValidacao();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcContrato" for="selMdAbcContrato" accesskey="o" class="infraLabelObrigatorio">C<span class="infraTeclaAtalho">o</span>ntrato:</label>
  <select id="selMdAbcContrato" name="selMdAbcContrato" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>">
  <?=$strItensSelMdAbcContrato??false?>
  </select>
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblNome" for="txtNome" accesskey="o" class="infraLabelObrigatorio">N<span class="infraTeclaAtalho">o</span>me:</label>
  <input type="text" id="txtNome" name="txtNome" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcResponsavelDTO->getStrNome())?>" onkeypress="return infraMascaraTexto(this,event,100);" maxlength="100" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblCargo" for="txtCargo" accesskey="o" class="infraLabelObrigatorio">Carg<span class="infraTeclaAtalho">o</span>:</label>
  <input type="text" id="txtCargo" name="txtCargo" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcResponsavelDTO->getStrCargo())?>" onkeypress="return infraMascaraTexto(this,event,50);" maxlength="50" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblEmail" for="txtEmail" accesskey="o" class="infraLabelOpcional">E-mail:</label>
  <input type="text" id="txtEmail" name="txtEmail" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcResponsavelDTO->getStrEmail())?>" onkeypress="return infraMascaraTexto(this,event,100);" maxlength="100" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcResponsavel" name="hdnIdMdAbcResponsavel" value="<?=$objMdAbcResponsavelDTO->getNumIdMdAbcResponsavel()?>" />
  <?php
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
