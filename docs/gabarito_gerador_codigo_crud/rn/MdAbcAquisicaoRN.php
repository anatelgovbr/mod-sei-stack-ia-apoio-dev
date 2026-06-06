<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

/**
 * @method MdAbcAquisicaoDTO cadastrar(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO)
 * @method MdAbcAquisicaoDTO[] listar(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO)
 * @method MdAbcAquisicaoDTO|null consultar(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO)
 * @method MdAbcAquisicaoDTO|null bloquear(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO)
 * @method void alterar(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO)
 * @method void excluir(MdAbcAquisicaoDTO[] $arrObjMdAbcAquisicaoDTO)
 * @method void desativar(MdAbcAquisicaoDTO[] $arrObjMdAbcAquisicaoDTO)
 * @method void reativar(MdAbcAquisicaoDTO[] $arrObjMdAbcAquisicaoDTO)
 */
class MdAbcAquisicaoRN extends InfraRN
{
  protected function inicializarObjInfraIBanco(): InfraIBanco
  {
    return BancoSEI::getInstance();
  }

  private function validarNumIdMdAbcProjeto(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcAquisicaoDTO->getNumIdMdAbcProjeto())) {
      $objInfraException->adicionarValidacao('Projeto não informado.');
    }
  }

  private function validarStrDescricao(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcAquisicaoDTO->getStrDescricao())) {
      $objInfraException->adicionarValidacao('Descrição não informada.');
    } else {
      $objMdAbcAquisicaoDTO->setStrDescricao(trim($objMdAbcAquisicaoDTO->getStrDescricao()));
      if (strlen($objMdAbcAquisicaoDTO->getStrDescricao())>50) {
        $objInfraException->adicionarValidacao('Descrição possui tamanho superior a 50 caracteres.');
      }
    }
  }

  private function validarDinCusto(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcAquisicaoDTO->getDinCusto())) {
      $objInfraException->adicionarValidacao('Custo não informado.');
    }
  }

  /**
   * @param MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO
   * @return MdAbcAquisicaoDTO
   * @throws InfraException
   */
  protected function cadastrarControlado(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO): MdAbcAquisicaoDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_cadastrar', __METHOD__, $objMdAbcAquisicaoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      $this->validarNumIdMdAbcProjeto($objMdAbcAquisicaoDTO, $objInfraException);
      $this->validarStrDescricao($objMdAbcAquisicaoDTO, $objInfraException);
      $this->validarDinCusto($objMdAbcAquisicaoDTO, $objInfraException);

      $objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      return $objMdAbcAquisicaoBD->cadastrar($objMdAbcAquisicaoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro cadastrando Aquisição.', $e);
    }
  }

  /**
   * @param MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO
   * @return void
   * @throws InfraException
   */
  protected function alterarControlado(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_alterar', __METHOD__, $objMdAbcAquisicaoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      if ($objMdAbcAquisicaoDTO->isSetNumIdMdAbcProjeto()) {
        $this->validarNumIdMdAbcProjeto($objMdAbcAquisicaoDTO, $objInfraException);
      }

      if ($objMdAbcAquisicaoDTO->isSetStrDescricao()) {
        $this->validarStrDescricao($objMdAbcAquisicaoDTO, $objInfraException);
      }

      if ($objMdAbcAquisicaoDTO->isSetDinCusto()) {
        $this->validarDinCusto($objMdAbcAquisicaoDTO, $objInfraException);
      }


      $objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      $objMdAbcAquisicaoBD->alterar($objMdAbcAquisicaoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro alterando Aquisição.', $e);
    }
  }

  /**
   * @param MdAbcAquisicaoDTO[] $arrObjMdAbcAquisicaoDTO
   * @return void
   * @throws InfraException
   */
  protected function excluirControlado(array $arrObjMdAbcAquisicaoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_excluir', __METHOD__, $arrObjMdAbcAquisicaoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcAquisicaoDTO as $objMdAbcAquisicaoDTO) {
        $objMdAbcAquisicaoBD->excluir($objMdAbcAquisicaoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro excluindo Aquisição.', $e);
    }
  }

  /**
   * @param MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO
   * @return MdAbcAquisicaoDTO|null
   * @throws InfraException
   */
  protected function consultarConectado(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO): ?MdAbcAquisicaoDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_consultar', __METHOD__, $objMdAbcAquisicaoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      return $objMdAbcAquisicaoBD->consultar($objMdAbcAquisicaoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro consultando Aquisição.', $e);
    }
  }

  /**
   * @param MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO
   * @return MdAbcAquisicaoDTO[]
   * @throws InfraException
   */
  protected function listarConectado(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO): array
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_listar', __METHOD__, $objMdAbcAquisicaoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      return $objMdAbcAquisicaoBD->listar($objMdAbcAquisicaoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro listando Aquisições.', $e);
    }
  }

  /**
   * @param MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO
   * @return int
   * @throws InfraException
   */
  protected function contarConectado(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO): int
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_listar', __METHOD__, $objMdAbcAquisicaoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      return $objMdAbcAquisicaoBD->contar($objMdAbcAquisicaoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro contando Aquisição.', $e);
    }
  }

  /**
   * @param MdAbcAquisicaoDTO[] $arrObjMdAbcAquisicaoDTO
   * @return void
   * @throws InfraException
   */
/*   protected function desativarControlado(array $arrObjMdAbcAquisicaoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_desativar', __METHOD__, $arrObjMdAbcAquisicaoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcAquisicaoDTO as $objMdAbcAquisicaoDTO) {
        $objMdAbcAquisicaoBD->desativar($objMdAbcAquisicaoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro desativando Aquisição.', $e);
    }
  }
 */
  /**
   * @param MdAbcAquisicaoDTO[] $arrObjMdAbcAquisicaoDTO
   * @return void
   * @throws InfraException
   */
/*   protected function reativarControlado(array $arrObjMdAbcAquisicaoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_reativar', __METHOD__, $arrObjMdAbcAquisicaoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcAquisicaoDTO as $objMdAbcAquisicaoDTO) {
        $objMdAbcAquisicaoBD->reativar($objMdAbcAquisicaoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro reativando Aquisição.', $e);
    }
  }
 */
  /**
   * @param  MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO
   * @return MdAbcAquisicaoDTO|null
   * @throws InfraException
   */
/*   protected function bloquearConectado(MdAbcAquisicaoDTO $objMdAbcAquisicaoDTO): ?MdAbcAquisicaoDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_aquisicao_consultar', __METHOD__, $objMdAbcAquisicaoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcAquisicaoBD = new MdAbcAquisicaoBD($this->getObjInfraIBanco());

      return $objMdAbcAquisicaoBD->bloquear($objMdAbcAquisicaoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro bloqueando Aquisição.', $e);
    }
  } */
}
