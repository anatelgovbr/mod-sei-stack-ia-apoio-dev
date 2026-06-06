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

  PaginaSEI::getInstance()->prepararSelecao('{{TABLE_NAME}}_selecionar');
{{LIST_POST_PERSISTENCE_LINES}}
  switch ($strAcao) {
{{LIST_SWITCH_CASES}}
    default:
      throw new InfraException("A��o '".$strAcao."' n�o reconhecida.");
  }

  $arrComandos = array();
{{LIST_TOP_COMMANDS}}
  $obj{{CLASS_NAME}}DTO = new {{CLASS_NAME}}DTO();
{{LIST_DTO_RETURN_LINES}}
{{LIST_FILTER_APPLY_LINES}}
  PaginaSEI::getInstance()->prepararOrdenacao($obj{{CLASS_NAME}}DTO, '{{LIST_SORT_FIELD}}', InfraDTO::$TIPO_ORDENACAO_ASC);

  $obj{{CLASS_NAME}}RN = new {{CLASS_NAME}}RN();
  $arrObj{{CLASS_NAME}}DTO = $obj{{CLASS_NAME}}RN->listar($obj{{CLASS_NAME}}DTO);

  $numRegistros = count($arrObj{{CLASS_NAME}}DTO);

  if ($numRegistros > 0) {
{{LIST_ACTION_FLAG_LINES}}
{{LIST_BULK_COMMAND_LINES}}
    $strResultado = '';
    $strResultado .= '<table style="width: 99%" class="infraTable">' . "\n";
    $strResultado .= '<caption class="infraCaption">' . PaginaSEI::getInstance()->gerarCaptionTabela('{{ENTITY_LABEL_PLURAL}}', $numRegistros) . '</caption>';
    $strResultado .= '<thead><tr>';
{{LIST_HEADER_LINES}}
    $strResultado .= '</tr></thead><tbody>' . "\n";
    $strCssTr = '';
    for ($i = 0; $i < $numRegistros; $i++) {
{{LIST_TR_COLOR_LOGIC}}
{{LIST_ROW_LINES}}
      $strResultado .= '</td></tr>' . "\n";
    }
    $strResultado .= '</tbody>' . "\n";
    $strResultado .= '</table>';
  }

{{LIST_BOTTOM_COMMANDS}}
{{LIST_FILTER_SELECT_LINES}}
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
{{LIST_STYLE_LINES}}
<?php if (0) { ?></style><?php } ?>
<?php
PaginaSEI::getInstance()->fecharStyle();
PaginaSEI::getInstance()->montarJavaScript();
PaginaSEI::getInstance()->abrirJavaScript();
?>
<?php if (0) { ?><script type="text/javascript"><?php } ?>

 function inicializar()
{
{{LIST_INITIALIZE_LINES}}
}

{{LIST_JAVASCRIPT_FUNCTIONS}}

<?php if (0) { ?></script><?php } ?>
<?php
PaginaSEI::getInstance()->fecharJavaScript();
PaginaSEI::getInstance()->fecharHead();
PaginaSEI::getInstance()->abrirBody($strTitulo ?? false, 'onload="inicializar();"');
?>
<form id="frm{{CLASS_NAME}}Lista" method="post" action="<?=SessaoSEI::getInstance()->assinarLink('controlador.php?acao='.$strAcao.'&acao_origem='.$strAcao)?>">
<?php
PaginaSEI::getInstance()->montarBarraComandosSuperior($arrComandos ?? false);
{{LIST_FILTER_FORM_BLOCK}}
PaginaSEI::getInstance()->montarAreaTabela($strResultado ?? false,$numRegistros ?? false);
PaginaSEI::getInstance()->montarBarraComandosInferior($arrComandos ?? false);
?>
</form>
<?php
PaginaSEI::getInstance()->fecharBody();
PaginaSEI::getInstance()->fecharHtml();
