<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4Âª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * VersÃ£o do Gerador de CÃ³digo: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

class MdAbcContratoDTO extends InfraDTO
{
  public function getStrNomeTabela(): ?string
  {
    return 'md_abc_contrato';
  }

  /**
   * @throws InfraException
   */
  public function montar(): void
  {
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcContrato', 'id_md_abc_contrato');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcAquisicao', 'id_md_abc_aquisicao');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Numero', 'numero');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_DTA, 'Assinatura', 'dta_assinatura');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_DIN, 'Valor', 'din_valor');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Observacao', 'observacao');


    $this->configurarPK('IdMdAbcContrato', InfraDTO::$TIPO_PK_SEQUENCIAL);

  }
}
