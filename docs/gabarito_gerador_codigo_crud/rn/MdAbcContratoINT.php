<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

class MdAbcContratoINT extends InfraINT
{

  public static function montarSelectIdMdAbcContrato($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $numIdMdAbcAquisicao=''): string
  {
    $objMdAbcContratoDTO = new MdAbcContratoDTO();
    $objMdAbcContratoDTO->retNumIdMdAbcContrato();
    $objMdAbcContratoDTO->retNumIdMdAbcContrato();

    if ($numIdMdAbcAquisicao!=='') {
      $objMdAbcContratoDTO->setNumIdMdAbcAquisicao($numIdMdAbcAquisicao);
    }

    $objMdAbcContratoDTO->setOrdNumIdMdAbcContrato(InfraDTO::$TIPO_ORDENACAO_ASC);

    $objMdAbcContratoRN = new MdAbcContratoRN();
    $arrObjMdAbcContratoDTO = $objMdAbcContratoRN->listar($objMdAbcContratoDTO);

    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObjMdAbcContratoDTO, 'IdMdAbcContrato', 'IdMdAbcContrato');
  }
}
