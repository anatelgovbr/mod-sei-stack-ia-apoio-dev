<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4Âª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * VersÃ£o do Gerador de CÃ³digo: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

class MdAbcRelContratoProjetoINT extends InfraINT
{

  public static function montarSelectIdMdAbcContrato($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $numIdMdAbcContrato='', $numIdMdAbcProjeto=''): string
  {
    $objMdAbcRelContratoProjetoDTO = new MdAbcRelContratoProjetoDTO();
    $objMdAbcRelContratoProjetoDTO->retNumIdMdAbcContrato();
    $objMdAbcRelContratoProjetoDTO->retNumIdMdAbcProjeto();
    $objMdAbcRelContratoProjetoDTO->retNumIdMdAbcContrato();

    if ($numIdMdAbcContrato!=='') {
      $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
    }

    if ($numIdMdAbcProjeto!=='') {
      $objMdAbcRelContratoProjetoDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
    }

    $objMdAbcRelContratoProjetoDTO->setOrdNumIdMdAbcContrato(InfraDTO::$TIPO_ORDENACAO_ASC);

    $objMdAbcRelContratoProjetoRN = new MdAbcRelContratoProjetoRN();
    $arrObjMdAbcRelContratoProjetoDTO = $objMdAbcRelContratoProjetoRN->listar($objMdAbcRelContratoProjetoDTO);

    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObjMdAbcRelContratoProjetoDTO, 'IdMdAbcContrato ou IdMdAbcProjeto', 'IdMdAbcContrato');
  }
}
