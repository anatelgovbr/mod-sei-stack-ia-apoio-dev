<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

class MdAbcAquisicaoINT extends InfraINT
{

  public static function montarSelectDescricao($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $numIdMdAbcProjeto=''): string
  {
    $objMdAbcAquisicaoDTO = new MdAbcAquisicaoDTO();
    $objMdAbcAquisicaoDTO->retNumIdMdAbcAquisicao();
    $objMdAbcAquisicaoDTO->retStrDescricao();

    if ($numIdMdAbcProjeto!=='') {
      $objMdAbcAquisicaoDTO->setNumIdMdAbcProjeto($numIdMdAbcProjeto);
    }

    $objMdAbcAquisicaoDTO->setOrdStrDescricao(InfraDTO::$TIPO_ORDENACAO_ASC);

    $objMdAbcAquisicaoRN = new MdAbcAquisicaoRN();
    $arrObjMdAbcAquisicaoDTO = $objMdAbcAquisicaoRN->listar($objMdAbcAquisicaoDTO);

    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObjMdAbcAquisicaoDTO, 'IdMdAbcAquisicao', 'Descricao');
  }
}
