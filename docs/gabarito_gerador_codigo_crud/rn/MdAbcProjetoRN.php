<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
 * 29/03/2026 - criado por abc
 *
 * Versão do Gerador de Código: 1.46.4
 **/


require_once __DIR__ . '/../SEI.php';

/**
 * @method MdAbcProjetoDTO cadastrar(MdAbcProjetoDTO $objMdAbcProjetoDTO)
 * @method MdAbcProjetoDTO[] listar(MdAbcProjetoDTO $objMdAbcProjetoDTO)
 * @method MdAbcProjetoDTO|null consultar(MdAbcProjetoDTO $objMdAbcProjetoDTO)
 * @method MdAbcProjetoDTO|null bloquear(MdAbcProjetoDTO $objMdAbcProjetoDTO)
 * @method void alterar(MdAbcProjetoDTO $objMdAbcProjetoDTO)
 * @method void excluir(MdAbcProjetoDTO[] $arrObjMdAbcProjetoDTO)
 * @method void desativar(MdAbcProjetoDTO[] $arrObjMdAbcProjetoDTO)
 * @method void reativar(MdAbcProjetoDTO[] $arrObjMdAbcProjetoDTO)
 */
class MdAbcProjetoRN extends InfraRN
{
  protected function inicializarObjInfraIBanco(): InfraIBanco
  {
    return BancoSEI::getInstance();
  }

  private function validarStrIdentificacao(MdAbcProjetoDTO $objMdAbcProjetoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcProjetoDTO->getStrIdentificacao())) {
      $objInfraException->adicionarValidacao('Identificação não informada.');
    } else {
      $objMdAbcProjetoDTO->setStrIdentificacao(trim($objMdAbcProjetoDTO->getStrIdentificacao()));
      if (strlen($objMdAbcProjetoDTO->getStrIdentificacao())>50) {
        $objInfraException->adicionarValidacao('Identificação possui tamanho superior a 50 caracteres.');
      }
    }
  }

  private function validarStrDescricao(MdAbcProjetoDTO $objMdAbcProjetoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcProjetoDTO->getStrDescricao())) {
      $objMdAbcProjetoDTO->setStrDescricao(null);
    } else {
      $objMdAbcProjetoDTO->setStrDescricao(trim($objMdAbcProjetoDTO->getStrDescricao()));
    }
  }

  private function validarDtaCadastramento(MdAbcProjetoDTO $objMdAbcProjetoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcProjetoDTO->getDtaCadastramento())) {
      $objInfraException->adicionarValidacao('Data de Início não informada.');
    } elseif (!InfraData::validarData($objMdAbcProjetoDTO->getDtaCadastramento())) {
      $objInfraException->adicionarValidacao('Data de Início inválida.');
    }
  }

  private function validarStrSinAtivo(MdAbcProjetoDTO $objMdAbcProjetoDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcProjetoDTO->getStrSinAtivo())) {
      $objInfraException->adicionarValidacao('Sinalizador de Exclusão Lógica não informado.');
    } elseif (!InfraUtil::isBolSinalizadorValido($objMdAbcProjetoDTO->getStrSinAtivo())) {
      $objInfraException->adicionarValidacao('Sinalizador de Exclusão Lógica inválido.');
    }
  }

  /**
   * @param MdAbcProjetoDTO $objMdAbcProjetoDTO
   * @return MdAbcProjetoDTO
   * @throws InfraException
   */
  protected function cadastrarControlado(MdAbcProjetoDTO $objMdAbcProjetoDTO): MdAbcProjetoDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_cadastrar', __METHOD__, $objMdAbcProjetoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      $this->validarStrIdentificacao($objMdAbcProjetoDTO, $objInfraException);
      $this->validarStrDescricao($objMdAbcProjetoDTO, $objInfraException);
      $this->validarDtaCadastramento($objMdAbcProjetoDTO, $objInfraException);
      $this->validarStrSinAtivo($objMdAbcProjetoDTO, $objInfraException);

      $objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcProjetoBD->cadastrar($objMdAbcProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro cadastrando Projeto.', $e);
    }
  }

  /**
   * @param MdAbcProjetoDTO $objMdAbcProjetoDTO
   * @return void
   * @throws InfraException
   */
  protected function alterarControlado(MdAbcProjetoDTO $objMdAbcProjetoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_alterar', __METHOD__, $objMdAbcProjetoDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      if ($objMdAbcProjetoDTO->isSetStrIdentificacao()) {
        $this->validarStrIdentificacao($objMdAbcProjetoDTO, $objInfraException);
      }

      if ($objMdAbcProjetoDTO->isSetStrDescricao()) {
        $this->validarStrDescricao($objMdAbcProjetoDTO, $objInfraException);
      }

      if ($objMdAbcProjetoDTO->isSetDtaCadastramento()) {
        $this->validarDtaCadastramento($objMdAbcProjetoDTO, $objInfraException);
      }

      if ($objMdAbcProjetoDTO->isSetStrSinAtivo()) {
        $this->validarStrSinAtivo($objMdAbcProjetoDTO, $objInfraException);
      }


      $objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      $objMdAbcProjetoBD->alterar($objMdAbcProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro alterando Projeto.', $e);
    }
  }

  /**
   * @param MdAbcProjetoDTO[] $arrObjMdAbcProjetoDTO
   * @return void
   * @throws InfraException
   */
  protected function excluirControlado(array $arrObjMdAbcProjetoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_excluir', __METHOD__, $arrObjMdAbcProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcProjetoDTO as $objMdAbcProjetoDTO) {
        $objMdAbcProjetoBD->excluir($objMdAbcProjetoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro excluindo Projeto.', $e);
    }
  }

  /**
   * @param MdAbcProjetoDTO $objMdAbcProjetoDTO
   * @return MdAbcProjetoDTO|null
   * @throws InfraException
   */
  protected function consultarConectado(MdAbcProjetoDTO $objMdAbcProjetoDTO): ?MdAbcProjetoDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_consultar', __METHOD__, $objMdAbcProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcProjetoBD->consultar($objMdAbcProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro consultando Projeto.', $e);
    }
  }

  /**
   * @param MdAbcProjetoDTO $objMdAbcProjetoDTO
   * @return MdAbcProjetoDTO[]
   * @throws InfraException
   */
  protected function listarConectado(MdAbcProjetoDTO $objMdAbcProjetoDTO): array
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_listar', __METHOD__, $objMdAbcProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcProjetoBD->listar($objMdAbcProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro listando Projetos.', $e);
    }
  }

  /**
   * @param MdAbcProjetoDTO $objMdAbcProjetoDTO
   * @return int
   * @throws InfraException
   */
  protected function contarConectado(MdAbcProjetoDTO $objMdAbcProjetoDTO): int
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_listar', __METHOD__, $objMdAbcProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      return $objMdAbcProjetoBD->contar($objMdAbcProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro contando Projeto.', $e);
    }
  }

  /**
   * @param MdAbcProjetoDTO[] $arrObjMdAbcProjetoDTO
   * @return void
   * @throws InfraException
   */
  protected function desativarControlado(array $arrObjMdAbcProjetoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_desativar', __METHOD__, $arrObjMdAbcProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcProjetoDTO as $objMdAbcProjetoDTO) {
        $objMdAbcProjetoBD->desativar($objMdAbcProjetoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro desativando Projeto.', $e);
    }
  }

  /**
   * @param MdAbcProjetoDTO[] $arrObjMdAbcProjetoDTO
   * @return void
   * @throws InfraException
   */
  protected function reativarControlado(array $arrObjMdAbcProjetoDTO): void
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_reativar', __METHOD__, $arrObjMdAbcProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcProjetoDTO as $objMdAbcProjetoDTO) {
        $objMdAbcProjetoBD->reativar($objMdAbcProjetoDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro reativando Projeto.', $e);
    }
  }

  /**
   * @param  MdAbcProjetoDTO $objMdAbcProjetoDTO
   * @return MdAbcProjetoDTO|null
   * @throws InfraException
   */
  protected function bloquearConectado(MdAbcProjetoDTO $objMdAbcProjetoDTO): ?MdAbcProjetoDTO
  {
    try {
      SessaoSEI::getInstance()->validarAuditarPermissao('md_abc_projeto_consultar', __METHOD__, $objMdAbcProjetoDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcProjetoBD = new MdAbcProjetoBD($this->getObjInfraIBanco());

      return $objMdAbcProjetoBD->bloquear($objMdAbcProjetoDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro bloqueando Projeto.', $e);
    }
  }
}
