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

  PaginaSEI::getInstance()->verificarSelecao('md_abc_aquisicao_selecionar');

  PaginaSEI::getInstance()->salvarCamposPost(array('selMdAbcProjeto'));

  $objMdAbcAquisicaoDTO = new MdAbcAquisicaoDTO();
  $strDesabilitar = '';
  $arrComandos = array();
  
  switch ($_GET['acao']) {
    case 'md_abc_aquisicao_cadastrar':
      $strTitulo = 'Nova Aquisição';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmCadastrarMdAbcAquisicao" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.$_GET['acao']).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      $objMdAbcAquisicaoDTO->setNumIdMdAbcAquisicao(null);
      $numIdMdAbcProjeto = PaginaSEI::getInstance()->recuperarCampo('selMdAbcProjeto');
      if ($numIdMdAbcProjeto !=='') {
        $objMdAbcAquisicaoDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
      } else {
        $objMdAbcAquisicaoDTO->setNumIdMdAbcProjeto(null);
      }

      $objMdAbcAquisicaoDTO->setStrDescricao(PaginaSEI::POST('txtDescricao'));
      $objMdAbcAquisicaoDTO->setDinCusto(PaginaSEI::POST('txtCusto'));

      if (isset($_POST['sbmCadastrarMdAbcAquisicao'])) {
        try {
          $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
          $objMdAbcAquisicaoDTO = $objMdAbcAquisicaoRN->cadastrar($objMdAbcAquisicaoDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Aquisição "'.$objMdAbcAquisicaoDTO->getStrDescricao().'" cadastrada com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').'&id_md_abc_aquisicao='.$objMdAbcAquisicaoDTO->getNumIdMdAbcAquisicao().PaginaSEI::getInstance()->montarAncora($objMdAbcAquisicaoDTO->getNumIdMdAbcAquisicao())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_aquisicao_alterar':
      $strTitulo = 'Alterar Aquisição';
      $arrComandos[] = '<button type="submit" accesskey="S" name="sbmAlterarMdAbcAquisicao" value="Salvar" class="infraButton"><span class="infraTeclaAtalho">S</span>alvar</button>';
      $strDesabilitar = 'disabled="disabled"';

      if (isset($_GET['id_md_abc_aquisicao'])) {
        $objMdAbcAquisicaoDTO->setNumIdMdAbcAquisicao(PaginaSEI::GET('id_md_abc_aquisicao'));
        $objMdAbcAquisicaoDTO->retTodos();
        $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
        $objMdAbcAquisicaoDTO = $objMdAbcAquisicaoRN->consultar($objMdAbcAquisicaoDTO);
        if ($objMdAbcAquisicaoDTO===null) {
          throw new InfraException("Registro não encontrado.");
        }
      } else {
        $objMdAbcAquisicaoDTO->setNumIdMdAbcAquisicao(PaginaSEI::POST('hdnIdMdAbcAquisicao'));
        $objMdAbcAquisicaoDTO->setNumIdMdAbcProjeto(PaginaSEI::POST('selMdAbcProjeto'));
        $objMdAbcAquisicaoDTO->setStrDescricao(PaginaSEI::POST('txtDescricao'));
        $objMdAbcAquisicaoDTO->setDinCusto(PaginaSEI::POST('txtCusto'));
      }

      $arrComandos[] = '<button type="button" accesskey="C" name="btnCancelar" id="btnCancelar" value="Cancelar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcAquisicaoDTO->getNumIdMdAbcAquisicao())).'\';" class="infraButton"><span class="infraTeclaAtalho">C</span>ancelar</button>';

      if (isset($_POST['sbmAlterarMdAbcAquisicao'])) {
        try {
          $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
          $objMdAbcAquisicaoRN->alterar($objMdAbcAquisicaoDTO);
          PaginaSEI::getInstance()->adicionarMensagem('Aquisição "'.$objMdAbcAquisicaoDTO->getStrDescricao().'" alterada com sucesso.');
          header('Location: '.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora($objMdAbcAquisicaoDTO->getNumIdMdAbcAquisicao())));
          die;
        } catch (Exception $e) {
          PaginaSEI::getInstance()->processarExcecao($e);
        }
      }
      break;

    case 'md_abc_aquisicao_consultar':
      $strTitulo = 'Consultar Aquisição';
      $arrComandos[] = '<button type="button" accesskey="F" name="btnFechar" value="Fechar" onclick="location.href=\''.SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::getInstance()->getAcaoRetorno().'&acao_origem='.PaginaSEI::GET('acao').PaginaSEI::getInstance()->montarAncora(PaginaSEI::GET('id_md_abc_aquisicao'))).'\';" class="infraButton"><span class="infraTeclaAtalho">F</span>echar</button>';
      $objMdAbcAquisicaoDTO->setNumIdMdAbcAquisicao(PaginaSEI::GET('id_md_abc_aquisicao'));
      $objMdAbcAquisicaoDTO->setBolExclusaoLogica(false);
      $objMdAbcAquisicaoDTO->retTodos();
      $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
      $objMdAbcAquisicaoDTO = $objMdAbcAquisicaoRN->consultar($objMdAbcAquisicaoDTO);
      if ($objMdAbcAquisicaoDTO===null) {
        throw new InfraException("Registro não encontrado.");
      }
      break;

    default:
      throw new InfraException("Ação '" . PaginaSEI::GET('acao') . "' não reconhecida.");
  }

  $strItensSelMdAbcProjeto = MdAbcProjetoINT::montarSelectIdentificacao('null','&nbsp;',$objMdAbcAquisicaoDTO->getNumIdMdAbcProjeto());

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
#lblMdAbcProjeto {position:absolute;left:0;top:0;width:25%;}
#selMdAbcProjeto {position:absolute;left:0;top:40%;width:25%;}

#lblDescricao {position:absolute;left:0;top:0;width:50%;}
#txtDescricao {position:absolute;left:0;top:40%;width:50%;}

#lblCusto {position:absolute;left:0;top:0;width:25%;}
#txtCusto {position:absolute;left:0;top:40%;width:25%;}

<?php if(0){?></style><?php }?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if(0){?><script type="text/javascript"><?php }?>

function inicializar()
{
  if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_aquisicao_cadastrar') {
    document.getElementById('selMdAbcProjeto').focus();
  } else if ('<?=PaginaSEI::GET('acao')?>' === 'md_abc_aquisicao_consultar') {
    infraDesabilitarCamposAreaDados();
  } else {
    document.getElementById('btnCancelar').focus();
  }
  infraEfeitoTabelas(true);
}

function validarCadastro()
{
  if (!infraSelectSelecionado('selMdAbcProjeto')) {
    alert('Selecione um Projeto.');
    document.getElementById('selMdAbcProjeto').focus();
    return false;
  }

  if (infraTrim(document.getElementById('txtDescricao').value)=='') {
    alert('Informe a Descrição.');
    document.getElementById('txtDescricao').focus();
    return false;
  }

  if (infraTrim(document.getElementById('txtCusto').value)=='') {
    alert('Informe o Custo.');
    document.getElementById('txtCusto').focus();
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
<form id="frmMdAbcAquisicaoCadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.PaginaSEI::GET('acao').'&acao_origem='.PaginaSEI::GET('acao'))?>">
<?php
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos??false);
//PaginaSEI::getInstance()->montarAreaValidacao();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblMdAbcProjeto" for="selMdAbcProjeto" accesskey="P" class="infraLabelObrigatorio"><span class="infraTeclaAtalho">P</span>rojeto:</label>
  <select id="selMdAbcProjeto" name="selMdAbcProjeto" class="infraSelect" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>">
  <?=$strItensSelMdAbcProjeto??false?>
  </select>
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblDescricao" for="txtDescricao" accesskey="D" class="infraLabelObrigatorio"><span class="infraTeclaAtalho">D</span>escrição:</label>
  <input type="text" id="txtDescricao" name="txtDescricao" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcAquisicaoDTO->getStrDescricao())?>" onkeypress="return infraMascaraTexto(this,event,50);" maxlength="50" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
  <label id="lblCusto" for="txtCusto" class="infraLabelObrigatorio">Custo:</label>
  <input type="text" id="txtCusto" name="txtCusto" onkeydown="return infraMascaraDinheiro(this, event)" class="infraText" value="<?=PaginaSEI::tratarHTML($objMdAbcAquisicaoDTO->getDinCusto())?>" tabindex="<?=PaginaSEI::getInstance()->getProxTabDados()?>" />
<?php
PaginaSEI::getInstance()->fecharAreaDados();
?>
  <input type="hidden" id="hdnIdMdAbcAquisicao" name="hdnIdMdAbcAquisicao" value="<?=$objMdAbcAquisicaoDTO->getNumIdMdAbcAquisicao()?>" />
  <?php
  //PaginaSEI::getInstance()->montarAreaDebug();
  PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos??false);
  ?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
