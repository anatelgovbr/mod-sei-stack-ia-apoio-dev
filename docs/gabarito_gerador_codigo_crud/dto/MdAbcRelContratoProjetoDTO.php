<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

class MdAbcRelContratoProjetoDTO extends InfraDTO
{
  public function getStrNomeTabela(): ?string
  {
    return 'md_abc_rel_contrato_projeto';
  }

  /**
   * @throws InfraException
   */
  public function montar(): void
  {
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcContrato', 'id_md_abc_contrato');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcProjeto', 'id_md_abc_projeto');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_DTA, 'Associacao', 'dta_associacao');

    $this->adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_NUM, 'IdMdAbcContratoMdAbcContrato', 'id_md_abc_contrato', 'md_abc_contrato');

    $this->configurarPK('IdMdAbcContrato', InfraDTO::$TIPO_PK_INFORMADO);
    $this->configurarPK('IdMdAbcProjeto', InfraDTO::$TIPO_PK_INFORMADO);

  }
}
