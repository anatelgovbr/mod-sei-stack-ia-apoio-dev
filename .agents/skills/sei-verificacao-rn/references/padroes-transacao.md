# Padrões de Transação em InfraRN, Manual TRF4

Baseado em `sei_modulos_manual_dev_4_infraphp.md`, Seção "InfraRN (2ª Camada)".

---

## T1 - Sufixo correto por operacao

**Severidade:** Aviso
**Base:** Manual SEI MD §InfraRN - Mecanismo de Controle de Transacao

A classe `InfraRN` implementa controle automatico de conexao e transacao.
Para CRUD padronizado, metodos de **escrita** tendem a usar o sufixo
`Controlado` e metodos de **leitura** tendem a usar o sufixo `Conectado`.
Aplicar esta regra apenas quando o nome do metodo realmente representar um CRUD
padrao.

| Tipo | Sufixo | Abre | Uso |
|------|--------|------|-----|
| Escrita | `Controlado` | Conexao + Transacao | insert, update, delete |
| Leitura | `Conectado` | Conexao apenas | select, count |

**Conforme:**
```php
protected function cadastrarControlado($objDTO) {
    // transacao aberta automaticamente
}

protected function consultarConectado($objDTO) {
    // apenas conexao, sem transacao
}
```

**Nao conforme:**
```php
// operacao de escrita com Conectado
protected function cadastrarConectado($objDTO) {
    // conexao sem transacao para operacao de escrita
}
```

---

## T2 - `inicializarObjInfraIBanco()`

**Severidade:** Erro
**Base:** Manual SEI MD §InfraRN

A classe RN **deve** implementar o metodo `inicializarObjInfraIBanco()`
retornando `BancoSEI::getInstance()`. Sem isso, o controle de transacao
nao funciona.

**Conforme:**
```php
class MdRiRestauranteRN extends InfraRN {

    protected function inicializarObjInfraIBanco() {
        return BancoSEI::getInstance();
    }
}
```

**Nao conforme:**
```php
// falta o metodo
class MdRiRestauranteRN extends InfraRN {
    // sem inicializarObjInfraIBanco()
}
```

---

## T3 - RN nao chama BD de outra classe

**Severidade:** Erro
**Base:** Manual SEI MD §Arquitetura em Camadas

RN se comunica apenas com sua propria BD. Para acessar logica de outra
entidade, a RN deve chamar a RN correspondente, que por sua vez usa sua propria
BD.

**Conforme:**
```php
protected function cadastrarControlado($objDTO) {
    $objBD = new MdRiRestauranteBD($this->getObjInfraIBanco());
    $objBD->cadastrar($objDTO);
}
```

**Nao conforme:**
```php
protected function cadastrarControlado($objDTO) {
    $objBD = new MdRiCardapioBD($this->getObjInfraIBanco()); // ERRO
}
```

---

## T4 - Controle manual de conexao/transacao merece revisao

**Severidade:** Aviso
**Base:** Manual SEI MD §InfraRN

O framework gerencia automaticamente abertura e fechamento de conexoes.
Chamadas como `fecharConexao()`, `commitTransacao()` e similares exigem
contexto claro, porque podem contornar o fluxo padrao da `InfraRN`.

**Conforme:**
```php
protected function cadastrarControlado($objDTO) {
    // a InfraRN controla conexao e transacao automaticamente
}
```

**Revisar:**
```php
protected function cadastrarControlado($objDTO) {
    $this->getObjInfraIBanco()->fecharConexao();
}
```

---

## T5 - `try/catch` com `InfraException` e encadeamento de erro

**Severidade:** Aviso
**Base:** padrao recorrente nos exemplos do manual

Usar `try/catch` com `InfraException` encadeando o erro original e um padrao
recorrente nos exemplos do manual. Tratar como recomendacao contextual; nao
inferir erro automaticamente quando a excecao pode propagar com contexto
suficiente.

**Conforme:**
```php
protected function cadastrarControlado($objDTO) {
    try {
        // logica...
    } catch (Exception $e) {
        throw new InfraException("Erro ao cadastrar restaurante.", $e);
    }
}
```

**Revisar:**
```php
protected function cadastrarControlado($objDTO) {
    // sem try/catch - excecao propagada sem contexto adicional
}
```

---

## T6 - Efeitos externos somente apos o retorno transacional

**Severidade:** Erro
**Base:** AGENTS.md, secao Padrao Transacional Obrigatorio

Um metodo `*Controlado` contem somente persistencia em banco. E-mail, Solr,
indexacao e integracoes externas ficam em um wrapper publico, depois do retorno
da operacao transacional. O retorno marca o ponto em que a `InfraRN` ja concluiu
o commit.

Motivo: efeito colateral que falha dentro da transacao pode acionar `cancelarTransacao()`
e desfazer silenciosamente a persistencia critica.

**Conforme:**
```php
public function gerarProcedimentoComEfeitos(MdAbcProcedimentoDTO $objDTO)
{
    $retorno = $this->gerarProcedimento($objDTO);
    FeedSEIProtocolos::getInstance()->indexarFeeds();
    return $retorno;
}

protected function gerarProcedimentoControlado(MdAbcProcedimentoDTO $objDTO)
{
    $objBD = new MdAbcProcedimentoBD($this->getObjInfraIBanco());
    return $objBD->cadastrar($objDTO);
}
```

`gerarProcedimento()` e a operacao publica resolvida pela `InfraRN` para
`gerarProcedimentoControlado()`. O wrapper nao chama o metodo protegido
diretamente.

**Nao conforme, chamada direta ao método protegido:**
```php
public function gerarProcedimentoComEfeitos(MdAbcProcedimentoDTO $objDTO)
{
    $retorno = $this->gerarProcedimentoControlado($objDTO);
    FeedSEIProtocolos::getInstance()->indexarFeeds();
    return $retorno;
}
```

A chamada direta nao passa pelo fluxo publico da `InfraRN`, portanto o efeito
nao possui evidencia de que ocorreu depois do commit.

**Nao conforme (T006, BLOCK):**
```php
protected function gerarProcedimentoControlado($arrParametros)
{
    // persistencia e efeito colateral misturados na mesma transacao
    $objBD->cadastrar($objDTO);
    MdAbcEmailNotificacaoRN::notificar($arrParametros); // ERRO: dentro da transacao
}
```

---

## A1 - Metodo de escrita deve usar `validarAuditarPermissao`

**Severidade:** Erro
**Base:** padrao observado em todos os modulos SEI com trilha de auditoria ativa

Metodos de escrita (`cadastrar`, `alterar`, `excluir` e variantes) devem chamar
`SessaoSEI::getInstance()->validarAuditarPermissao(...)`, nunca `validarPermissao`
puro. O `validarPermissao` valida o acesso mas nao grava trilha; a omissao da
auditoria e silenciosa e so descoberta em auditoria forense posterior.

O terceiro argumento e o DTO ou array de DTOs da operacao.

**Conforme:**
```php
protected function cadastrarControlado(MdAptEtapaPlDocModeloDTO $objDTO): MdAptEtapaPlDocModeloDTO
{
    try {
        SessaoSEI::getInstance()->validarAuditarPermissao('md_apt_etapa_pl_doc_modelo_cadastrar', __METHOD__, $objDTO);
        // ...
    } catch (Exception $e) {
        throw new InfraException('Erro ao cadastrar.', $e);
    }
}
```

**Nao conforme (A001, BLOCK):**
```php
protected function cadastrarControlado(MdAptEtapaPlDocModeloDTO $objDTO): MdAptEtapaPlDocModeloDTO
{
    SessaoSEI::getInstance()->validarPermissao('md_apt_etapa_pl_doc_modelo_cadastrar'); // sem trilha
}
```

---

## A2 - Metodo de escrita sem verificacao de permissao

**Severidade:** Aviso
**Base:** guardrail local, confirmar intencionalidade

Metodo de escrita sem nenhuma chamada de permissao ou auditoria. Pode ser
intencional quando o metodo e um helper chamado exclusivamente de contexto
interno (hook de evento, tarefa agendada) onde nao ha sessao de usuario ativa.
Nao bloqueia. Exige revisao para confirmar que o caminho de chamada nunca
vem de requisicao HTTP direta.

**Conforme (helper de hook):**
```php
protected function substituirConteudoDocumentoControlado(array $arrParametros): void
{
    // chamado apenas pelo hook md_apt_substituir_documento, sem sessao de usuario
    try {
        // logica interna...
    } catch (Exception $e) {
        throw new InfraException('Erro ao substituir conteudo.', $e);
    }
}
```

**Revisar (A002, WARN):**
```php
protected function excluirControlado(array $arrObjDTO): void
{
    // sem validarAuditarPermissao e sem validarPermissao
    $objBD = new MdAptEtapaPlDocModeloBD($this->getObjInfraIBanco());
    // ...
}
```

---

## A3 - Leitura publica usa o recurso `_listar`

**Severidade:** Erro
**Base:** AGENTS.md, secao Guardrails Universais

Operacoes publicas de leitura `consultar`, `listar` e `contar` devem usar
`validarAuditarPermissao` com o recurso `_listar`. Helpers internos e caminhos
de hook ou evento sem usuario nao recebem verificacao de sessao artificial.

**Conforme:**
```php
protected function consultarConectado(MdAbcItemDTO $objDTO)
{
    SessaoSEI::getInstance()->validarAuditarPermissao(
        'md_abc_item_listar',
        __METHOD__,
        $objDTO
    );
}
```

---

## Matriz de severidade

| ID | Regra | Sev |
|----|-------|-----|
| T1 | Sufixo correto para CRUD padronizado | **Aviso** |
| T2 | inicializarObjInfraIBanco() | **Erro** |
| T3 | RN nao chama BD de outra classe | **Erro** |
| T4 | Controle manual de conexao/transacao merece revisao | **Aviso** |
| T5 | try/catch com `InfraException` e encadeamento de erro | **Aviso** |
| T6 | Efeitos externos somente apos retorno transacional | **Erro** |
| A1 | Escrita com validarPermissao sem auditoria | **Erro** |
| A2 | Escrita sem verificacao de permissao/auditoria | **Aviso** |
| A3 | Leitura publica sem recurso `_listar` | **Erro** |
