# Padrao de Auditoria SIP + SEI

Referencia autoritativa do fluxo completo de auditoria nos modulos SEI:
registro de recursos no SIP (script de instalacao) e verificacao em runtime
nas classes RN.


## Convencao de nomenclatura de recursos

Formato: `{prefixo_modulo}_{entidade}_{operacao}`

- `prefixo_modulo`: sigla do modulo (ex: `md_apt`, `md_lit`, `pen`)
- `entidade`: nome snake_case da entidade principal (ex: `etapa_pl_doc_modelo`)
- `operacao`: uma de `listar`, `cadastrar`, `alterar`, `excluir`

Todas as operacoes de leitura (consultar, listar, contar) usam o mesmo
recurso `listar` — nao ha recurso `consultar` ou `contar` separado.

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

Todas as operacoes de leitura usam o recurso `listar`:

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
| `md_xxx_listar` | consultar / listar / contar | Nao |
| `md_xxx_cadastrar` | cadastrar | Sim |
| `md_xxx_alterar` | alterar | Sim |
| `md_xxx_excluir` | excluir | Sim |

Inconsistencia frequente: recurso registrado no SIP mas ausente da regra
de auditoria (ou vice-versa). O gate `sei-verificacao-rn` detecta a
ausencia na RN (A1/A2); a consistencia com o script SIP e verificada
manualmente via `sei-menu-pagina`.
