# Padrao de Auditoria SIP + SEI

Referencia autoritativa do fluxo completo de auditoria nos modulos SEI:
registro de recursos no SIP (script de instalacao) e verificacao em runtime
nas classes RN.


## Convencao de nomenclatura de recursos

Formato: `{prefixo_modulo}_{entidade}_{operacao}`

- `prefixo_modulo`: sigla do modulo (ex: `md_apt`, `md_lit`, `pen`)
- `entidade`: nome snake_case da entidade principal (ex: `etapa_pl_doc_modelo`)
- `operacao`: uma de `cadastrar`, `alterar`, `consultar`, `listar`, `excluir`, `selecionar`, mais `desativar` e `reativar` quando a entidade tem `sin_ativo`

Mapa de metodo da RN para recurso:

| Metodo da RN | Recurso validado |
|---|---|
| `cadastrarControlado` | `_cadastrar` |
| `alterarControlado` | `_alterar` |
| `excluirControlado` | `_excluir` |
| `desativarControlado` | `_desativar` |
| `reativarControlado` | `_reativar` |
| `consultarConectado` | `_consultar` |
| `bloquearConectado` | `_consultar`, compartilhado com consultar |
| `listarConectado` | `_listar` |
| `contarConectado` | `_listar`, compartilhado com listar |

Duas operacoes compartilham recurso com outra: `bloquear` usa o recurso de
`consultar`, e `contar` usa o recurso de `listar`. As demais tem recurso proprio.

---

## Script SIP — template de instalacao

```php
// 1. Registrar recursos e vincular ao perfil
$objRecursoDTO = $this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilAdministrador, 'md_xxx_listar');
$this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilAdministrador, 'md_xxx_cadastrar');
$this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilAdministrador, 'md_xxx_alterar');
$this->adicionarRecursoPerfil($numIdSistemaSei, $numIdPerfilAdministrador, 'md_xxx_excluir');

// 2. Criar item de menu (usa o recurso listar como ancora)
$this->adicionarItemMenu(
    $numIdSistemaSei,
    $numIdPerfilAdministrador,
    $numIdMenuSei,
    $numIdItemMenuSeiAdministracao,
    $objRecursoDTO->getNumIdRecurso(),  // recurso listar
    'Rotulo do Menu',
    0
);

// 3. Registrar regra de auditoria — apenas operacoes de escrita
$this->_cadastrarAuditoria($numIdSistemaSei, 'Modulo_Nome_Snake', [
    "'md_xxx_cadastrar'",
    "'md_xxx_alterar'",
    "'md_xxx_excluir'"
]);
// 'listar' NAO entra na regra de auditoria
```

---

## RN PHP — chamadas por tipo de operacao

### Escrita (cadastrar / alterar / excluir)

```php
protected function cadastrarControlado(MdXxxEntidadeDTO $objDTO): MdXxxEntidadeDTO
{
    try {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_xxx_entidade_cadastrar', __METHOD__, $objDTO);
        // validacoes de negocio...
        $objBD = new MdXxxEntidadeBD($this->getObjInfraIBanco());
        return $objBD->cadastrar($objDTO);
    } catch (Exception $e) {
        throw new InfraException('Erro ao cadastrar.', $e);
    }
}
```

Para `excluir`, o terceiro argumento e `$arrObjDTO` (array):

```php
SessaoSEI::getInstance()->validarAuditarPermissao('md_xxx_entidade_excluir', __METHOD__, $arrObjDTO);
```

### Leitura (consultar / listar / contar)

Leitura por lista e por contagem usa o recurso `listar`. Leitura de registro unico usa `consultar`:

```php
protected function listarConectado(MdXxxEntidadeDTO $objDTO): array
{
    try {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_xxx_entidade_listar', __METHOD__, $objDTO);
        $objBD = new MdXxxEntidadeBD($this->getObjInfraIBanco());
        return $objBD->listar($objDTO);
    } catch (Exception $e) {
        throw new InfraException('Erro ao listar.', $e);
    }
}

protected function consultarConectado(MdXxxEntidadeDTO $objDTO): ?MdXxxEntidadeDTO
{
    try {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_xxx_entidade_consultar', __METHOD__, $objDTO);
        $objBD = new MdXxxEntidadeBD($this->getObjInfraIBanco());
        return $objBD->consultar($objDTO);
    } catch (Exception $e) {
        throw new InfraException('Erro ao consultar.', $e);
    }
}

protected function bloquearConectado(MdXxxEntidadeDTO $objDTO): ?MdXxxEntidadeDTO
{
    try {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_xxx_entidade_consultar', __METHOD__, $objDTO);
        $objBD = new MdXxxEntidadeBD($this->getObjInfraIBanco());
        return $objBD->bloquear($objDTO);
    } catch (Exception $e) {
        throw new InfraException('Erro ao bloquear.', $e);
    }
}
```

### Helper interno (hook / evento / tarefa)

Metodos chamados exclusivamente de contexto de sistema (sem sessao de usuario)
nao devem ter verificacao de permissao. Documentar no PHPDoc o motivo.

```php
protected function substituirConteudoDocumentoControlado(array $arrParametros): void
{
    // Chamado pelo hook — sem sessao de usuario ativa
    try {
        // ...
    } catch (Exception $e) {
        throw new InfraException('Erro ao substituir conteudo.', $e);
    }
}
```

---

## Regras de consistencia SIP x RN

| Recurso SIP | Metodo RN | Entra em _cadastrarAuditoria? |
|-------------|-----------|-------------------------------|
| `md_xxx_listar` | listar / contar | Nao |
| `md_xxx_consultar` | consultar / bloquear | Nao |
| `md_xxx_selecionar` | selecao em tela | Nao |
| `md_xxx_cadastrar` | cadastrar | Sim |
| `md_xxx_alterar` | alterar | Sim |
| `md_xxx_excluir` | excluir | Sim |
| `md_xxx_desativar` | desativar | Sim |
| `md_xxx_reativar` | reativar | Sim |

Inconsistencia frequente: recurso registrado no SIP mas ausente da regra
de auditoria (ou vice-versa). O gate `sei-verificacao-rn` detecta a
ausencia na RN (A1/A2); a consistencia com o script SIP e verificada
manualmente via `sei-menu-pagina`.

---

### Recurso fora de regra de auditoria

Se o recurso nao fizer parte de nenhuma regra de auditoria no SIP, `validarAuditarPermissao` executa apenas a validacao de permissao, sem gravar trilha. A chamada nao falha e nao avisa.

Consequencia: chamar `validarAuditarPermissao` nao garante auditoria. A garantia vem de o recurso estar na regra, o que e responsabilidade do script SIP.

### Prefixo do nome da regra de auditoria

O manual recomenda que as regras de auditoria de modulo usem o prefixo `MD_<instituicao/modulo>` no nome. Sem o prefixo, a regra de um modulo colide com a de outro modulo instalado no mesmo SIP.

Esta convencao vale para o **nome da regra de auditoria**, e nao se confunde com a convencao de recurso, que neste repositorio e minuscula.

### Recurso do metodo `bloquear`

O metodo `bloquear` compartilha o recurso do metodo `consultar` e nao recebe recurso proprio. `bloquearConectado` valida `md_<modulo>_<entidade>_consultar`.

### Auditoria de permissao na RN e opcional no gerador oficial

O gerador do InfraPHP oferece, na secao `Permissoes na RN`, a escolha de o codigo gerado prever ou nao auditoria das permissoes por Regras de Auditoria do SIP.

Este repositorio e mais estrito que o manual: a auditoria de permissao em metodo de escrita da RN e obrigatoria, conforme `AGENTS.md`. Ao usar o gerador oficial, marcar a opcao. Codigo gerado sem ela precisa ser ajustado antes de entrar no modulo.
