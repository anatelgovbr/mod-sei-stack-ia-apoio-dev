<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

class MdAbcResponsavelDTO extends InfraDTO
{
  public function getStrNomeTabela(): ?string
  {
    return 'md_abc_responsavel';
  }

  /**
   * @throws InfraException
   */
  public function montar(): void
  {
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcResponsavel', 'id_md_abc_responsavel');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcContrato', 'id_md_abc_contrato');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Nome', 'nome');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Cargo', 'cargo');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Email', 'email');

    $this->adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_NUM, 'IdMdAbcContratoMdAbcContrato', 'id_md_abc_contrato', 'md_abc_contrato');

    $this->configurarPK('IdMdAbcResponsavel', InfraDTO::$TIPO_PK_SEQUENCIAL);

  }
}
