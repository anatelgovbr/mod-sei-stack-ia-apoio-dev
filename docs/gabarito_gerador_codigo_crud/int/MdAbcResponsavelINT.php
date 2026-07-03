<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4Âª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * VersÃ£o do Gerador de CÃ³digo: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

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
