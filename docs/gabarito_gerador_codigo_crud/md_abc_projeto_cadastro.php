<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
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

  PaginaSEI::getInstance()->verificarSelecao('md_abc_projeto_selecionar');

  $objMdAbcProjetoDTO = new MdAbcProjetoDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_projeto_cadastrar':
      $strTitulo = 'Novo Projeto';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcProjeto" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $objMdAbcProjetoDTO->setNumIdMdAbcProjeto(null);
      $objMdAbcProjetoDTO->setStrIdentificacao(PaginaSEI::POST('txtIdentificacao'));
      $objMdAbcProjetoDTO->setStrDescricao(PaginaSEI::POST('txtDescricao'));
      $objMdAbcProjetoDTO->setDtaCadastramento(PaginaSEI::POST('txtCadastramento'));
      $objMdAbcProjetoDTO->setStrSinAtivo('S');

      if (isset($_POST['sbmCadastrarMdAbcProjeto'])) {
        try {
          $objMdAbcProjetoRN = new MdAbcProjetoRN();
          $objMdAbcProjetoDTO = $objMdAbcProjetoRN->cadastrar($objMdAbcProjetoDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Projeto "'.$objMdAbcProjetoDTO->getStrIdentificacao().'" cadastrado com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').'&id_md_abc_projeto='.$objMdAbcProjetoDTO->getNumIdMdAbcProjeto().PaginaSEI::getInstance()->montarAncora($objMdAbcProjetoDTO->getNumIdMdAbcProjeto())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_projeto_alterar':
      $strTitulo = 'Alterar Projeto';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcProjeto" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_projeto'])) {
        $objMdAbcProjetoDTO->setNumIdMdAbcProjeto(PaginaSEI::GET('id_md_abc_projeto'));
        $objMdAbcProjetoDTO->retTodos();
        $objMdAbcProjetoRN = new MdAbcProjetoRN();
        $objMdAbcProjetoDTO = $objMdAbcProjetoRN->consultar($objMdAbcProjetoDTO);
        if ($objMdAbcProjetoDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcProjetoDTO->setNumIdMdAbcProjeto(PaginaSEI::POST('hdnIdMdAbcProjeto'));
        $objMdAbcProjetoDTO->setStrIdentificacao(PaginaSEI::POST('txtIdentificacao'));
        $objMdAbcProjetoDTO->setStrDescricao(PaginaSEI::POST('txtDescricao'));
        $objMdAbcProjetoDTO->setDtaCadastramento(PaginaSEI::POST('txtCadastramento'));
        $objMdAbcProjetoDTO->setStrSinAtivo('S');
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcProjetoDTO->getNumIdMdAbcProjeto())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcProjeto'])) {
        try {
          $objMdAbcProjetoRN = new MdAbcProjetoRN();
          $objMdAbcProjetoRN->alterar($objMdAbcProjetoDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Projeto "'.$objMdAbcProjetoDTO->getStrIdentificacao().'" alterado com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcProjetoDTO->getNumIdMdAbcProjeto())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_projeto_consultar':
      $strTitulo = 'Consultar Projeto';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora(PaginaSEI::GET('id_md_abc_projeto'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcProjetoDTO->setNumIdMdAbcProjeto(PaginaSEI::GET('id_md_abc_projeto'));
      $objMdAbcProjetoDTO->setBolExclusaoLogica(false);
      $objMdAbcProjetoDTO->retTodos();
      $objMdAbcProjetoRN = new MdAbcProjetoRN();
      $objMdAbcProjetoDTO = $objMdAbcProjetoRN->consultar($objMdAbcProjetoDTO);
      if ($objMdAbcProjetoDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . PaginaSEI::GET('acao') . "' não reconhecida.");
  }


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
#lblIdentificacao {position:absolute;left:0;top:0;width:50%;}
#txtIdentificacao {position:absolute;left:0;top:40%;width:50%;}

#lblDescricao {position:absolute;left:0;top:0;width:25%;}
#txtDescricao {position:absolute;left:0;top:40%;width:25%;}

#lblCadastramento {position:absolute;left:0;top:0;width:25%;}
#txtCadastramento {position:absolute;left:0;top:40%;width:25%;}
#imgCalCadastramento {position:absolute;left:26%;top:45%;}

<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_projeto_cadastrar') {
    document.getElementById('txtIdentificacao').focus();
  } else if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_projeto_consultar') {
    infraDesabilitarCamposAreaDados();
  } else {
    document.getElementById('btnCancelar').focus();
  }
  infraEfeitoTabelas(true);
}

function validarCadastro()
{
  if (infraTrim(document.getElementById('txtIdentificacao').value)=='') {
    alert('Informe a Identificação.');
    document.getElementById('txtIdentificacao').focus();
    return false;
  }

  if (infraTrim(document.getElementById('txtCadastramento').value)=='') {
    alert('Informe a Data de Início.');
    document.getElementById('txtCadastramento').focus();
    return false;
  }

  if (!infraValidarData(document.getElementById('txtCadastramento'))) {
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
<form id="frmMdAbcProjetoCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
<?php
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//PaginaSEI::getInstance()->montarAreaValidacao();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblIdentificacao" for="txtIdentificacao" accesskey="I" class="infraLabelObrigatorio"><span class="infraTeclaAtalho">I</span>dentificação:</label>
  <input type="text" id="txtIdentificacao" name="txtIdentificacao" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcProjetoDTO->getStrIdentificacao())?>" onkeypress="return infraMascaraTexto(this,event,50);" maxlength="50" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblDescricao" for="txtDescricao" accesskey="D" class="infraLabelOpcional"><span class="infraTeclaAtalho">D</span>escrição:</label>
  <input type="text" id="txtDescricao" name="txtDescricao" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcProjetoDTO->getStrDescricao())?>" onkeypress="return infraMascaraTexto(this,event);" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblCadastramento" for="txtCadastramento" accesskey="A" class="infraLabelObrigatorio">D<span class="infraTeclaAtalho">a</span>ta de Início:</label>
  <input type="text" id="txtCadastramento" name="txtCadastramento" onkeypress="return infraMascaraData(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcProjetoDTO->getDtaCadastramento())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
  <img id="imgCalCadastramento" title="Selecionar Data de Início" alt="Selecionar Data de Início" src="<?=PaginaSEI::getInstance()->getIconeCalendario()?>" class="infraImg" onclick="infraCalendario('txtCadastramento',this);" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcProjeto" name="hdnIdMdAbcProjeto" value="<?=$objMdAbcProjetoDTO->getNumIdMdAbcProjeto()?>" />
  <?php
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
