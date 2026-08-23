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

  Paginaabc::getInstance()->verificarSelecao('md_abc_contrato_selecionar');

  Paginaabc::getInstance()->salvarCamposPost(array('selMdAbcAquisicao'));

  $objMdAbcContratoDTO = new MdAbcContratoDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_contrato_cadastrar':
      $strTitulo = 'Novo Contrato';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcContrato" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $objMdAbcContratoDTO->setNumIdMdAbcContrato(null);
      $numIdMdAbcAquisicao = Paginaabc::getInstance()->recuperarCampo('selMdAbcAquisicao');
      if ($numIdMdAbcAquisicao !=='') {
        $objMdAbcContratoDTO->setNumIdMdAbcAquisicao($numIdMdAbcAquisicao);
      } else {
        $objMdAbcContratoDTO->setNumIdMdAbcAquisicao(null);
      }

      $objMdAbcContratoDTO->setStrNumero(Paginaabc::POST('txtNumero'));
      $objMdAbcContratoDTO->setDtaAssinatura(Paginaabc::POST('txtAssinatura'));
      $objMdAbcContratoDTO->setDinValor(Paginaabc::POST('txtValor'));
      $objMdAbcContratoDTO->setStrObservacao(Paginaabc::POST('txtObservacao'));

      if (isset($_POST['sbmCadastrarMdAbcContrato'])) {
        try {
          $objMdAbcContratoRN = new MdAbcContratoRN();
          $objMdAbcContratoDTO = $objMdAbcContratoRN->cadastrar($objMdAbcContratoDTO);
          Paginaabc::getInstance()->adicionarMensagem('Contrato "'.$objMdAbcContratoDTO->getNumIdMdAbcContrato().'" cadastrado com sucesso.');
          header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').'&id_md_abc_contrato='.$objMdAbcContratoDTO->getNumIdMdAbcContrato().Paginaabc::getInstance()->montarAncora($objMdAbcContratoDTO->getNumIdMdAbcContrato())));
          die;
        } catch (Exception $e) {
          Paginaabc::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_contrato_alterar':
      $strTitulo = 'Alterar Contrato';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcContrato" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_contrato'])) {
        $objMdAbcContratoDTO->setNumIdMdAbcContrato(Paginaabc::GET('id_md_abc_contrato'));
        $objMdAbcContratoDTO->retTodos();
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoDTO = $objMdAbcContratoRN->consultar($objMdAbcContratoDTO);
        if ($objMdAbcContratoDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcContratoDTO->setNumIdMdAbcContrato(Paginaabc::POST('hdnIdMdAbcContrato'));
        $objMdAbcContratoDTO->setNumIdMdAbcAquisicao(Paginaabc::POST('selMdAbcAquisicao'));
        $objMdAbcContratoDTO->setStrNumero(Paginaabc::POST('txtNumero'));
        $objMdAbcContratoDTO->setDtaAssinatura(Paginaabc::POST('txtAssinatura'));
        $objMdAbcContratoDTO->setDinValor(Paginaabc::POST('txtValor'));
        $objMdAbcContratoDTO->setStrObservacao(Paginaabc::POST('txtObservacao'));
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora($objMdAbcContratoDTO->getNumIdMdAbcContrato())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcContrato'])) {
        try {
          $objMdAbcContratoRN = new MdAbcContratoRN();
          $objMdAbcContratoRN->alterar($objMdAbcContratoDTO);
          Paginaabc::getInstance()->adicionarMensagem('Contrato "'.$objMdAbcContratoDTO->getNumIdMdAbcContrato().'" alterado com sucesso.');
          header('Location: '.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora($objMdAbcContratoDTO->getNumIdMdAbcContrato())));
          die;
        } catch (Exception $e) {
          Paginaabc::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_contrato_consultar':
      $strTitulo = 'Consultar Contrato';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::getInstance()->getAcaoRetorno().'&acao_origem='.Paginaabc::GET('acao').Paginaabc::getInstance()->montarAncora(Paginaabc::GET('id_md_abc_contrato'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcContratoDTO->setNumIdMdAbcContrato(Paginaabc::GET('id_md_abc_contrato'));
      $objMdAbcContratoDTO->setBolExclusaoLogica(false);
      $objMdAbcContratoDTO->retTodos();
      $objMdAbcContratoRN = new MdAbcContratoRN();
      $objMdAbcContratoDTO = $objMdAbcContratoRN->consultar($objMdAbcContratoDTO);
      if ($objMdAbcContratoDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . Paginaabc::GET('acao') . "' não reconhecida.");
  }

  $strItensSelMdAbcAquisicao = MdAbcAquisicaoINT::montarSelect???????('null','&nbsp;',$objMdAbcContratoDTO->getNumIdMdAbcAquisicao());

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
#lblMdAbcAquisicao {position:absolute;left:0;top:0;width:25%;}
#selMdAbcAquisicao {position:absolute;left:0;top:40%;width:25%;}

#lblNumero {position:absolute;left:0;top:0;width:20%;}
#txtNumero {position:absolute;left:0;top:40%;width:20%;}

#lblAssinatura {position:absolute;left:0;top:0;width:25%;}
#txtAssinatura {position:absolute;left:0;top:40%;width:25%;}
#imgCalAssinatura {position:absolute;left:26%;top:45%;}

#lblValor {position:absolute;left:0;top:0;width:25%;}
#txtValor {position:absolute;left:0;top:40%;width:25%;}

#lblObservacao {position:absolute;left:0;top:0;width:95%;}
#txtObservacao {position:absolute;left:0;top:40%;width:95%;}

<?php if(0){?></style><?php }?>
<?php
Paginaabc::getInstance()->fecharStyle();
Paginaabc::getInstance()->montarJavaScript();
Paginaabc::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_contrato_cadastrar') {
    document.getElementById('selMdAbcAquisicao').focus();
  } else if ('<?=Paginaabc::GET('acao')?>' === 'md_abc_contrato_consultar') {
    infraDesabilitarCamposAreaDados();
  } else {
    document.getElementById('btnCancelar').focus();
  }
  infraEfeitoTabelas(true);
}

function validarCadastro()
{
  if (!infraSelectSelecionado('selMdAbcAquisicao')) {
    alert('Selecione um Aquisição.');
    document.getElementById('selMdAbcAquisicao').focus();
    return false;
  }

  if (infraTrim(document.getElementById('txtNumero').value)=='') {
    alert('Informe N Número.');
    document.getElementById('txtNumero').focus();
    return false;
  }

  if (infraTrim(document.getElementById('txtAssinatura').value)=='') {
    alert('Informe D Data de Assinatura.');
    document.getElementById('txtAssinatura').focus();
    return false;
  }

  if (!infraValidarData(document.getElementById('txtAssinatura'))) {
    return false;
  }

  if (infraTrim(document.getElementById('txtValor').value)=='') {
    alert('Informe V Valor.');
    document.getElementById('txtValor').focus();
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
<form id="frmMdAbcContratoCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=Sessaoabc::getInstance()->assinarLink('controlador.php?acao='.Paginaabc::GET('acao').'&acao_origem='.Paginaabc::GET('acao'))?>">
<?php
Paginaabc::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//Paginaabc::getInstance()->montarAreaValidacao();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcAquisicao" for="selMdAbcAquisicao" accesskey="a" class="infraLabelObrigatorio"><span class="infraTeclaAtalho">A</span>quisição:</label>
  <select id="selMdAbcAquisicao" name="selMdAbcAquisicao" class="infraSelect" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>">
  <?=$strItensSelMdAbcAquisicao??false?>
  </select>
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblNumero" for="txtNumero" accesskey="n" class="infraLabelObrigatorio"><span class="infraTeclaAtalho">N</span>úmero:</label>
  <input type="text" id="txtNumero" name="txtNumero" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcContratoDTO->getStrNumero())?>" onkeypress="return infraMascaraTexto(this,event,20);" maxlength="20" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblAssinatura" for="txtAssinatura" accesskey="a" class="infraLabelObrigatorio">D<span class="infraTeclaAtalho">a</span>ta de Assinatura:</label>
  <input type="text" id="txtAssinatura" name="txtAssinatura" onkeypress="return infraMascaraData(this, event)" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcContratoDTO->getDtaAssinatura())?>" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
  <img id="imgCalAssinatura" title="Selecionar Data de Assinatura" alt="Selecionar Data de Assinatura" src="<?=Paginaabc::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario('txtAssinatura',this);" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblValor" for="txtValor" accesskey="o" class="infraLabelObrigatorio">Val<span class="infraTeclaAtalho">o</span>r:</label>
  <input type="text" id="txtValor" name="txtValor" onkeydown="return infraMascaraDinheiro(this, event)" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcContratoDTO->getDinValor())?>" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
Paginaabc::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblObservacao" for="txtObservacao" accesskey="a" class="infraLabelOpcional">Observ<span class="infraTeclaAtalho">a</span>ção:</label>
  <input type="text" id="txtObservacao" name="txtObservacao" class="infraText" value="<?=Paginaabc::tratarHTML($objMdAbcContratoDTO->getStrObservacao())?>" onkeypress="return infraMascaraTexto(this,event,500);" maxlength="500" tabindex="<?=Paginaabc::getInstance()->getProxTabDados()?>" />
<?php
Paginaabc::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcContrato" name="hdnIdMdAbcContrato" value="<?=$objMdAbcContratoDTO->getNumIdMdAbcContrato()?>" />
  <?php
  //Paginaabc::getInstance()->montarAreaDebug();
  Paginaabc::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
Paginaabc::getInstance()->fecharBody();
Paginaabc::getInstance()->fecharHtml();
