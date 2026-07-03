# Padrões de Transação em InfraRN — Manual TRF4

Baseado em `sei_modulos_manual_dev_4_infraphp.md` — Seção "InfraRN (2ª Camada)".

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

## T6 - Split `*Controlado` / `*Interno` quando ha efeitos colaterais

**Severidade:** Erro
**Base:** AGENTS.md — Padrao Transacional Obrigatorio

Quando um metodo `*Controlado` precisa disparar efeitos colaterais (indexacao Solr,
e-mail, integracao externa), a persistencia em banco deve ficar em um metodo `*Interno`
separado. O `*Controlado` orquestra: chama o `*Interno` (dentro da transacao) e dispara
os efeitos somente apos o commit.

Motivo: efeito colateral que falha dentro da transacao pode acionar `cancelarTransacao()`
e desfazer silenciosamente a persistencia critica.

**Conforme:**
```php
protected function gerarProcedimentoControlado($arrParametros)
{
    FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(true);
    $retorno = $this->gerarProcedimentoInterno($arrParametros);

    FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(false);
    FeedSEIProtocolos::getInstance()->indexarFeeds();

    try {
        $rn = new MdAbcEmailNotificacaoRN();
        $rn->notificar($retorno['parametrosEmail']);
    } catch (Exception $e) {}

    return $retorno['parametrosRecibo'];
}

protected function gerarProcedimentoInterno($arrParametros)
{
    // Apenas persistencia em banco; executado dentro da transacao.
}
```

**Nao conforme (T006 — BLOCK):**
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
`SessaoSEI::getInstance()->validarAuditarPermissao(...)` — nunca `validarPermissao`
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

**Nao conforme (A001 — BLOCK):**
```php
protected function cadastrarControlado(MdAptEtapaPlDocModeloDTO $objDTO): MdAptEtapaPlDocModeloDTO
{
    SessaoSEI::getInstance()->validarPermissao('md_apt_etapa_pl_doc_modelo_cadastrar'); // sem trilha
}
```

---

## A2 - Metodo de escrita sem verificacao de permissao

**Severidade:** Aviso
**Base:** guardrail local — confirmar intencionalidade

Metodo de escrita sem nenhuma chamada de permissao ou auditoria. Pode ser
intencional quando o metodo e um helper chamado exclusivamente de contexto
interno (hook de evento, tarefa agendada) onde nao ha sessao de usuario ativa.
Nao bloqueia — exige revisao para confirmar que o caminho de chamada nunca
vem de requisicao HTTP direta.

**Conforme (helper de hook):**
```php
protected function substituirConteudoDocumentoControlado(array $arrParametros): void
{
    // chamado apenas pelo hook md_apt_substituir_documento — sem sessao de usuario
    try {
        // logica interna...
    } catch (Exception $e) {
        throw new InfraException('Erro ao substituir conteudo.', $e);
    }
}
```

**Revisar (A002 — WARN):**
```php
protected function excluirControlado(array $arrObjDTO): void
{
    // sem validarAuditarPermissao e sem validarPermissao
    $objBD = new MdAptEtapaPlDocModeloBD($this->getObjInfraIBanco());
    // ...
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
| T6 | Split `*Controlado`/`*Interno` quando ha efeitos colaterais | **Erro** |
| A1 | Escrita com validarPermissao sem auditoria | **Erro** |
| A2 | Escrita sem verificacao de permissao/auditoria | **Aviso** |
