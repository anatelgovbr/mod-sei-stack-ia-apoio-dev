<?php

try {
  require_once dirname(__FILE__) . '/../../SEI.php';

  session_start();

  //////////////////////////////////////////////////////////////////////////////
  //InfraDebug::getInstance()->setBolLigado(false);
  //InfraDebug::getInstance()->setBolDebugInfra(true);
  //InfraDebug::getInstance()->limpar();
  //////////////////////////////////////////////////////////////////////////////

  SessaoSEI::getInstance()->validarLink();

  $strAcao = PaginaSEI::GET('acao');
  SessaoSEI::getInstance()->validarPermissao($strAcao);

  PaginaSEI::getInstance()->verificarSelecao('{{TABLE_NAME}}_selecionar');
  // Persist FK select state here when applicable.
{{CAD_POST_PERSISTENCE_LINES}}
  $obj{{CLASS_NAME}}DTO = new {{CLASS_NAME}}DTO();
  $strDesabilitar = '';
  $arrComandos = array();

  switch ($strAcao) {
    // Render cadastrar, alterar, consultar, and default branches here.
{{CAD_SWITCH_CASES}}
    default:
      throw new InfraException("Ação '" . $strAcao . "' não reconhecida.");
  }

{{CAD_AUXILIARY_SELECT_LINES}}
} catch (Exception $e) {
  PaginaSEI::getInstance()->processarExcecao($e);
}

PaginaSEI::getInstance()->montarDocType();
PaginaSEI::getInstance()->abrirHtml();
PaginaSEI::getInstance()->abrirHead();
PaginaSEI::getInstance()->montarMeta();
PaginaSEI::getInstance()->montarTitle(PaginaSEI::getInstance()->getStrNomeSistema() . ' - ' . ($strTitulo ?? false));
PaginaSEI::getInstance()->montarStyle();
PaginaSEI::getInstance()->abrirStyle();
?>
<?php if (0) { ?><style><?php } ?>
{{CAD_STYLE_LINES}}
<?php if (0) { ?></style><?php } ?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if (0) { ?><script type="text/javascript"><?php } ?>

function inicializar()
{
  // Focus first field on create, disable form on consult, or focus cancel.
{{CAD_INITIALIZE_LINES}}
}

function validarCadastro()
{
  // Render required-field checks and masks here.
{{CAD_VALIDATE_LINES}}
  return true;
}

function OnSubmitForm()
{
  return validarCadastro();
}

<?php if (0) { ?></script><?php } ?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo ?? false, 'onload="inicializar();"');
?>
<form id="frm{{CLASS_NAME}}Cadastro" method="post" onsubmit="return OnSubmitForm();" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.$strAcao.'&acao_origem='.$strAcao)?>">
<?php
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos ?? false);
PaginaSEI::getInstance()->abrirAreaDados('5em');
?>
<!-- Render labels and widgets here. FK uses select loaded from the related INT helper; every varchar uses input. -->
{{CAD_FORM_FIELDS_BLOCK}}
<?php
PaginaSEI::getInstance()->fecharAreaDados();
?>
<!-- Render hidden PK fields here. -->
{{CAD_HIDDEN_FIELDS_BLOCK}}
<?php
PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos ?? false);
?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
