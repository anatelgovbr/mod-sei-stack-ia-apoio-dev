<?php
/**
 * TRIBUNAL REGIONAL FEDERAL DA 4Âª REGIÃO
 * 15/04/2026 - criado por rafaelmontedo@hotmail.com
 *
 * VersÃ£o do Gerador de CÃ³digo: 1.46.4
 **/


require_once __DIR__ . '/../abc.php';

/**
 * @method MdAbcResponsavelDTO cadastrar(MdAbcResponsavelDTO $objMdAbcResponsavelDTO)
 * @method MdAbcResponsavelDTO[] listar(MdAbcResponsavelDTO $objMdAbcResponsavelDTO)
 * @method MdAbcResponsavelDTO|null consultar(MdAbcResponsavelDTO $objMdAbcResponsavelDTO)
 * @method MdAbcResponsavelDTO|null bloquear(MdAbcResponsavelDTO $objMdAbcResponsavelDTO)
 * @method void alterar(MdAbcResponsavelDTO $objMdAbcResponsavelDTO)
 * @method void excluir(MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO)
 * @method void desativar(MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO)
 * @method void reativar(MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO)
 */
class MdAbcResponsavelRN extends InfraRN
{
  protected function inicializarObjInfraIBanco(): InfraIBanco
  {
    return Bancoabc::getInstance();
  }

  private function validarNumIdMdAbcContrato(MdAbcResponsavelDTO $objMdAbcResponsavelDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcResponsavelDTO->getNumIdMdAbcContrato())) {
      $objInfraException->adicionarValidacao('Contrato nÃ£o informadC.');
    }
  }

  private function validarStrNome(MdAbcResponsavelDTO $objMdAbcResponsavelDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcResponsavelDTO->getStrNome())) {
      $objInfraException->adicionarValidacao('Nome nÃ£o informadN.');
    } else {
      $objMdAbcResponsavelDTO->setStrNome(trim($objMdAbcResponsavelDTO->getStrNome()));
      if (strlen($objMdAbcResponsavelDTO->getStrNome())>100) {
        $objInfraException->adicionarValidacao('Nome possui tamanho superior a 100 caracteres.');
      }
    }
  }

  private function validarStrCargo(MdAbcResponsavelDTO $objMdAbcResponsavelDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcResponsavelDTO->getStrCargo())) {
      $objInfraException->adicionarValidacao('Cargo nÃ£o informadG.');
    } else {
      $objMdAbcResponsavelDTO->setStrCargo(trim($objMdAbcResponsavelDTO->getStrCargo()));
      if (strlen($objMdAbcResponsavelDTO->getStrCargo())>50) {
        $objInfraException->adicionarValidacao('Cargo possui tamanho superior a 50 caracteres.');
      }
    }
  }

  private function validarStrEmail(MdAbcResponsavelDTO $objMdAbcResponsavelDTO, InfraException $objInfraException): void
  {
    if (InfraString::isBolVazia($objMdAbcResponsavelDTO->getStrEmail())) {
      $objMdAbcResponsavelDTO->setStrEmail(null);
    } else {
      $objMdAbcResponsavelDTO->setStrEmail(trim($objMdAbcResponsavelDTO->getStrEmail()));
      if (strlen($objMdAbcResponsavelDTO->getStrEmail())>100) {
        $objInfraException->adicionarValidacao('E-mail possui tamanho superior a 100 caracteres.');
      }
    }
  }

  /**
   * @param MdAbcResponsavelDTO $objMdAbcResponsavelDTO
   * @return MdAbcResponsavelDTO
   * @throws InfraException
   */
  protected function cadastrarControlado(MdAbcResponsavelDTO $objMdAbcResponsavelDTO): MdAbcResponsavelDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_cadastrar', __METHOD__, $objMdAbcResponsavelDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      $this->validarNumIdMdAbcContrato($objMdAbcResponsavelDTO, $objInfraException);
      $this->validarStrNome($objMdAbcResponsavelDTO, $objInfraException);
      $this->validarStrCargo($objMdAbcResponsavelDTO, $objInfraException);
      $this->validarStrEmail($objMdAbcResponsavelDTO, $objInfraException);

      $objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      return $objMdAbcResponsavelBD->cadastrar($objMdAbcResponsavelDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro cadastrando ResponsÃ¡vel.', $e);
    }
  }

  /**
   * @param MdAbcResponsavelDTO $objMdAbcResponsavelDTO
   * @return void
   * @throws InfraException
   */
  protected function alterarControlado(MdAbcResponsavelDTO $objMdAbcResponsavelDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_alterar', __METHOD__, $objMdAbcResponsavelDTO);

      //Regras de Negocio
      $objInfraException = new InfraException();

      if ($objMdAbcResponsavelDTO->isSetNumIdMdAbcContrato()) {
        $this->validarNumIdMdAbcContrato($objMdAbcResponsavelDTO, $objInfraException);
      }

      if ($objMdAbcResponsavelDTO->isSetStrNome()) {
        $this->validarStrNome($objMdAbcResponsavelDTO, $objInfraException);
      }

      if ($objMdAbcResponsavelDTO->isSetStrCargo()) {
        $this->validarStrCargo($objMdAbcResponsavelDTO, $objInfraException);
      }

      if ($objMdAbcResponsavelDTO->isSetStrEmail()) {
        $this->validarStrEmail($objMdAbcResponsavelDTO, $objInfraException);
      }


      $objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      $objMdAbcResponsavelBD->alterar($objMdAbcResponsavelDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro alterando ResponsÃ¡vel.', $e);
    }
  }

  /**
   * @param MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO
   * @return void
   * @throws InfraException
   */
  protected function excluirControlado(array $arrObjMdAbcResponsavelDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_excluir', __METHOD__, $arrObjMdAbcResponsavelDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcResponsavelDTO as $objMdAbcResponsavelDTO) {
        $objMdAbcResponsavelBD->excluir($objMdAbcResponsavelDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro excluindo ResponsÃ¡vel.', $e);
    }
  }

  /**
   * @param MdAbcResponsavelDTO $objMdAbcResponsavelDTO
   * @return MdAbcResponsavelDTO|null
   * @throws InfraException
   */
  protected function consultarConectado(MdAbcResponsavelDTO $objMdAbcResponsavelDTO): ?MdAbcResponsavelDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_consultar', __METHOD__, $objMdAbcResponsavelDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      return $objMdAbcResponsavelBD->consultar($objMdAbcResponsavelDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro consultando ResponsÃ¡vel.', $e);
    }
  }

  /**
   * @param MdAbcResponsavelDTO $objMdAbcResponsavelDTO
   * @return MdAbcResponsavelDTO[]
   * @throws InfraException
   */
  protected function listarConectado(MdAbcResponsavelDTO $objMdAbcResponsavelDTO): array
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_listar', __METHOD__, $objMdAbcResponsavelDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      return $objMdAbcResponsavelBD->listar($objMdAbcResponsavelDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro listando ResponsÃ¡veis.', $e);
    }
  }

  /**
   * @param MdAbcResponsavelDTO $objMdAbcResponsavelDTO
   * @return int
   * @throws InfraException
   */
  protected function contarConectado(MdAbcResponsavelDTO $objMdAbcResponsavelDTO): int
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_listar', __METHOD__, $objMdAbcResponsavelDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      return $objMdAbcResponsavelBD->contar($objMdAbcResponsavelDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro contando ResponsÃ¡vel.', $e);
    }
  }

  /**
   * @param MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO
   * @return void
   * @throws InfraException
   */
/*   protected function desativarControlado(array $arrObjMdAbcResponsavelDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_desativar', __METHOD__, $arrObjMdAbcResponsavelDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcResponsavelDTO as $objMdAbcResponsavelDTO) {
        $objMdAbcResponsavelBD->desativar($objMdAbcResponsavelDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro desativando ResponsÃ¡vel.', $e);
    }
  }
 */
  /**
   * @param MdAbcResponsavelDTO[] $arrObjMdAbcResponsavelDTO
   * @return void
   * @throws InfraException
   */
/*   protected function reativarControlado(array $arrObjMdAbcResponsavelDTO): void
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_reativar', __METHOD__, $arrObjMdAbcResponsavelDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());
      foreach ($arrObjMdAbcResponsavelDTO as $objMdAbcResponsavelDTO) {
        $objMdAbcResponsavelBD->reativar($objMdAbcResponsavelDTO);
      }

    } catch (Exception $e) {
      throw new InfraException('Erro reativando ResponsÃ¡vel.', $e);
    }
  }
 */
  /**
   * @param  MdAbcResponsavelDTO $objMdAbcResponsavelDTO
   * @return MdAbcResponsavelDTO|null
   * @throws InfraException
   */
/*   protected function bloquearConectado(MdAbcResponsavelDTO $objMdAbcResponsavelDTO): ?MdAbcResponsavelDTO
  {
    try {
      Sessaoabc::getInstance()->validarAuditarPermissao('md_abc_responsavel_consultar', __METHOD__, $objMdAbcResponsavelDTO);

      //Regras de Negocio
      //$objInfraException = new InfraException();

      //$objInfraException->lancarValidacoes();

      $objMdAbcResponsavelBD = new MdAbcResponsavelBD($this->getObjInfraIBanco());

      return $objMdAbcResponsavelBD->bloquear($objMdAbcResponsavelDTO);

    } catch (Exception $e) {
      throw new InfraException('Erro bloqueando ResponsÃ¡vel.', $e);
    }
  } */
}
