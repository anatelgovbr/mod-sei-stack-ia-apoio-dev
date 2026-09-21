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

  PaginaSEI::getInstance()->verificarSelecao('md_abc_contrato_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcAquisicao'));

  $objMdAbcContratoDTO = new MdAbcContratoDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_contrato_cadastrar':
      $strTitulo = 'Novo Contrato';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcContrato" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $objMdAbcContratoDTO->setNumIdMdAbcContrato(null);
      $numIdMdAbcAquisicao = PaginaSEI::getInstance()->recuperarCampo('selMdAbcAquisicao');
      if ($numIdMdAbcAquisicao !=='') {
        $objMdAbcContratoDTO->setNumIdMdAbcAquisicao($numIdMdAbcAquisicao);
      } else {
        $objMdAbcContratoDTO->setNumIdMdAbcAquisicao(null);
      }

      $objMdAbcContratoDTO->setStrNumero(PaginaSEI::POST('txtNumero'));
      $objMdAbcContratoDTO->setDtaAssinatura(PaginaSEI::POST('txtAssinatura'));
      $objMdAbcContratoDTO->setDinValor(PaginaSEI::POST('txtValor'));
      $objMdAbcContratoDTO->setStrObservacao(PaginaSEI::POST('txtObservacao'));

      if (isset($_POST['sbmCadastrarMdAbcContrato'])) {
        try {
          $objMdAbcContratoRN = new MdAbcContratoRN();
          $objMdAbcContratoDTO = $objMdAbcContratoRN->cadastrar($objMdAbcContratoDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Contrato "'.$objMdAbcContratoDTO->getNumIdMdAbcContrato().'" cadastrado com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').'&id_md_abc_contrato='.$objMdAbcContratoDTO->getNumIdMdAbcContrato().PaginaSEI::getInstance()->montarAncora($objMdAbcContratoDTO->getNumIdMdAbcContrato())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_contrato_alterar':
      $strTitulo = 'Alterar Contrato';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcContrato" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_contrato'])) {
        $objMdAbcContratoDTO->setNumIdMdAbcContrato(PaginaSEI::GET('id_md_abc_contrato'));
        $objMdAbcContratoDTO->retTodos();
        $objMdAbcContratoRN = new MdAbcContratoRN();
        $objMdAbcContratoDTO = $objMdAbcContratoRN->consultar($objMdAbcContratoDTO);
        if ($objMdAbcContratoDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcContratoDTO->setNumIdMdAbcContrato(PaginaSEI::POST('hdnIdMdAbcContrato'));
        $objMdAbcContratoDTO->setNumIdMdAbcAquisicao(PaginaSEI::POST('selMdAbcAquisicao'));
        $objMdAbcContratoDTO->setStrNumero(PaginaSEI::POST('txtNumero'));
        $objMdAbcContratoDTO->setDtaAssinatura(PaginaSEI::POST('txtAssinatura'));
        $objMdAbcContratoDTO->setDinValor(PaginaSEI::POST('txtValor'));
        $objMdAbcContratoDTO->setStrObservacao(PaginaSEI::POST('txtObservacao'));
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcContratoDTO->getNumIdMdAbcContrato())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcContrato'])) {
        try {
          $objMdAbcContratoRN = new MdAbcContratoRN();
          $objMdAbcContratoRN->alterar($objMdAbcContratoDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Contrato "'.$objMdAbcContratoDTO->getNumIdMdAbcContrato().'" alterado com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcContratoDTO->getNumIdMdAbcContrato())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_contrato_consultar':
      $strTitulo = 'Consultar Contrato';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora(PaginaSEI::GET('id_md_abc_contrato'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcContratoDTO->setNumIdMdAbcContrato(PaginaSEI::GET('id_md_abc_contrato'));
      $objMdAbcContratoDTO->setBolExclusaoLogica(false);
      $objMdAbcContratoDTO->retTodos();
      $objMdAbcContratoRN = new MdAbcContratoRN();
      $objMdAbcContratoDTO = $objMdAbcContratoRN->consultar($objMdAbcContratoDTO);
      if ($objMdAbcContratoDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . PaginaSEI::GET('acao') . "' não reconhecida.");
  }

  $strItensSelMdAbcAquisicao = MdAbcAquisicaoINT::montarSelectDescricao('null','&nbsp;',$objMdAbcContratoDTO->getNumIdMdAbcAquisicao());

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
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_contrato_cadastrar') {
    document.getElementById('selMdAbcAquisicao').focus();
  } else if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_contrato_consultar') {
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
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo??false,'onload="inicializar();"');
?>
<form id="frmMdAbcContratoCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
<?php
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//PaginaSEI::getInstance()->montarAreaValidacao();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcAquisicao" for="selMdAbcAquisicao" accesskey="a" class="infraLabelObrigatorio"><span class="infraTeclaAtalho">A</span>quisição:</label>
  <select id="selMdAbcAquisicao" name="selMdAbcAquisicao" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>">
  <?=$strItensSelMdAbcAquisicao??false?>
  </select>
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblNumero" for="txtNumero" accesskey="n" class="infraLabelObrigatorio"><span class="infraTeclaAtalho">N</span>úmero:</label>
  <input type="text" id="txtNumero" name="txtNumero" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcContratoDTO->getStrNumero())?>" onkeypress="return infraMascaraTexto(this,event,20);" maxlength="20" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblAssinatura" for="txtAssinatura" accesskey="a" class="infraLabelObrigatorio">D<span class="infraTeclaAtalho">a</span>ta de Assinatura:</label>
  <input type="text" id="txtAssinatura" name="txtAssinatura" onkeypress="return infraMascaraData(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcContratoDTO->getDtaAssinatura())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
  <img id="imgCalAssinatura" title="Selecionar Data de Assinatura" alt="Selecionar Data de Assinatura" src="<?=PaginaSEI::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario('txtAssinatura',this);" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblValor" for="txtValor" accesskey="o" class="infraLabelObrigatorio">Val<span class="infraTeclaAtalho">o</span>r:</label>
  <input type="text" id="txtValor" name="txtValor" onkeydown="return infraMascaraDinheiro(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcContratoDTO->getDinValor())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblObservacao" for="txtObservacao" accesskey="a" class="infraLabelOpcional">Observ<span class="infraTeclaAtalho">a</span>ção:</label>
  <input type="text" id="txtObservacao" name="txtObservacao" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcContratoDTO->getStrObservacao())?>" onkeypress="return infraMascaraTexto(this,event,500);" maxlength="500" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcContrato" name="hdnIdMdAbcContrato" value="<?=$objMdAbcContratoDTO->getNumIdMdAbcContrato()?>" />
  <?php
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
