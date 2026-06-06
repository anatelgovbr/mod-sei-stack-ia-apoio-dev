<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

class MdAbcAquisicaoDTO extends InfraDTO
{
  public function getStrNomeTabela(): ?string
  {
    return 'md_abc_aquisicao';
  }

  /**
   * @throws InfraException
   */
  public function montar(): void
  {
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcAquisicao', 'id_md_abc_aquisicao');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_NUM, 'IdMdAbcProjeto', 'id_md_abc_projeto');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_STR, 'Descricao', 'descricao');
    $this->adicionarAtributoTabela(InfraDTO::$PREFIXO_DIN, 'Custo', 'din_custo');

    $this->adicionarAtributoTabelaRelacionada(InfraDTO::$PREFIXO_STR, 'IdentificacaoMdAbcProjeto', 'identificacao', 'md_abc_projeto');

    $this->configurarPK('IdMdAbcAquisicao', InfraDTO::$TIPO_PK_SEQUENCIAL);

  }
}
