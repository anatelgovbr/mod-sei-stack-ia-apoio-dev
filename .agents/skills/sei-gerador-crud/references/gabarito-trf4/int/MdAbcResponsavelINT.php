<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

class MdAbcResponsavelINT extends InfraINT
{

  public static function montarSelectNome($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $numIdMdAbcContrato=''): string
  {
    $objMdAbcResponsavelDTO = new MdAbcResponsavelDTO();
    $objMdAbcResponsavelDTO->retNumIdMdAbcResponsavel();
    $objMdAbcResponsavelDTO->retStrNome();

    if ($numIdMdAbcContrato!=='') {
      $objMdAbcResponsavelDTO->setNumIdMdAbcContrato($numIdMdAbcContrato);
    }

    $objMdAbcResponsavelDTO->setOrdStrNome(InfraDTO::$TIPO_ORDENACAO_ASC);

    $objMdAbcResponsavelRN = new MdAbcResponsavelRN();
    $arrObjMdAbcResponsavelDTO = $objMdAbcResponsavelRN->listar($objMdAbcResponsavelDTO);

    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObjMdAbcResponsavelDTO, 'IdMdAbcResponsavel', 'Nome');
  }
}
