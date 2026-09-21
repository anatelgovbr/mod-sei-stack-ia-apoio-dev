<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

class MdAbcRelContratoProjINT extends InfraINT
{

  public static function montarSelectIdMdAbcContrato($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $numIdMdAbcContrato='', $numIdMdAbcProjeto=''): string
  {
    $objMdAbcRelContratoProjDTO = new MdAbcRelContratoProjDTO();
    $objMdAbcRelContratoProjDTO->retNumIdMdAbcContrato();
    $objMdAbcRelContratoProjDTO->retNumIdMdAbcProjeto();
    $objMdAbcRelContratoProjDTO->retNumIdMdAbcContrato();

    if ($numIdMdAbcContrato!=='') {
      $objMdAbcRelContratoProjDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
    }

    if ($numIdMdAbcProjeto!=='') {
      $objMdAbcRelContratoProjDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
    }

    $objMdAbcRelContratoProjDTO->setOrdNumIdMdAbcContrato(InfraDTO::$TIPO_ORDENACAO_ASC);

    $objMdAbcRelContratoProjRN = new MdAbcRelContratoProjRN();
    $arrObjMdAbcRelContratoProjDTO = $objMdAbcRelContratoProjRN->listar($objMdAbcRelContratoProjDTO);

    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObjMdAbcRelContratoProjDTO, 'IdMdAbcContrato ou IdMdAbcProjeto', 'IdMdAbcContrato');
  }
}
