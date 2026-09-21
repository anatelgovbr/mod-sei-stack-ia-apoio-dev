<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

class MdAbcProjetoINT extends InfraINT
{

  public static function montarSelectIdentificacao($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado): string
  {
    $objMdAbcProjetoDTO = new MdAbcProjetoDTO();
    $objMdAbcProjetoDTO->retNumIdMdAbcProjeto();
    $objMdAbcProjetoDTO->retStrIdentificacao();

    if ($strValorItemSelecionado!=null) {
      $objMdAbcProjetoDTO->setBolExclusaoLogica(false);
      $objMdAbcProjetoDTO->adicionarCriterio(array('SinAtivo', 'IdMdAbcProjeto'), array(InfraDTO::$OPER_IGUAL, InfraDTO::$OPER_IGUAL), array('S', $strValorItemSelecionado), InfraDTO::$OPER_LOGICO_OR);
    }

    $objMdAbcProjetoDTO->setOrdStrIdentificacao(InfraDTO::$TIPO_ORDENACAO_ASC);

    $objMdAbcProjetoRN = new MdAbcProjetoRN();
    $arrObjMdAbcProjetoDTO = $objMdAbcProjetoRN->listar($objMdAbcProjetoDTO);

    return parent::montarSelectArrInfraDTO($strPrimeiroItemValor, $strPrimeiroItemDescricao, $strValorItemSelecionado, $arrObjMdAbcProjetoDTO, 'IdMdAbcProjeto', 'Identificacao');
  }
}
