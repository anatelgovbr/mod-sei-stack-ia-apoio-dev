<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

class MdAbcContratoINT extends InfraINT
{

  public static function montarSelectNumero($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $numIdMdAbcProjeto='', $numIdMdAbcAquisicao=''): string
  {
    $objMdAbcContratoDTO = new MdAbcContratoDTO();
    $objMdAbcContratoDTO->retNumIdMdAbcContrato();
    $objMdAbcContratoDTO->retStrNumero();

    if ($numIdMdAbcProjeto!=='') {
      $objMdAbcContratoDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
    }

    if ($numIdMdAbcAquisicao!=='') {
      $objMdAbcContratoDTO->setNumIdMdAbcAquisicao($numIdMdAbcAquisicao);
    }

    $objMdAbcContratoDTO->setOrdStrNumero(InfraDTO::$TIPO_ORDENACAO_ASC);

    $objMdAbcContratoRN = new MdAbcContratoRN();
    $arrObjMdAbcContratoDTO = $objMdAbcContratoRN->listar($objMdAbcContratoDTO);

    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObjMdAbcContratoDTO, 'IdMdAbcContrato', 'Numero');
  }
}
