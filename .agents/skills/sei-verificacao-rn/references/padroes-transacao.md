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
Um metodo `*Controlado` contem somente persistencia em banco. E-mail, Solr,
indexacao e integracoes externas ficam em um wrapper publico, depois do retorno
da operacao transacional. O retorno marca o ponto em que a `InfraRN` ja concluiu
o commit.

Motivo: efeito colateral que falha dentro da transacao pode acionar `cancelarTransacao()`
e desfazer silenciosamente a persistencia critica. Alem disso, efeito lento dentro da
transacao aumenta o tempo de lock no banco.

**Conforme:**
```php
public function gerarProcedimentoComEfeitos(MdAbcProcedimentoDTO $objDTO)
{
    FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(true);

    $retorno = $this->gerarProcedimento($objDTO);

    FeedSEIProtocolos::getInstance()->setBolAcumularFeeds(false);
    FeedSEIProtocolos::getInstance()->indexarFeeds();

    try {
        $objEmailRN = new MdAbcEmailNotificacaoRN();
        $objEmailRN->notificar($retorno->getArrParametrosEmail());
    } catch (Exception $e) {
        // falha de notificacao nao desfaz o que ja foi persistido
    }

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

### Tres tecnicas que o wrapper precisa aplicar

1. **Acumular indexacao do Solr.** Ligar `setBolAcumularFeeds(true)` antes da operacao
   transacional, desligar depois e so entao chamar `indexarFeeds()`. Sem isso cada
   protocolo indexa individualmente durante a transacao.
2. **Isolar a notificacao em `try/catch`.** Falha de e-mail nao pode propagar erro para
   o fluxo que ja persistiu. O manual usa `catch` vazio nesse ponto; registrar o erro em
   log e preferivel a engolir silenciosamente.
3. **Extrair um metodo interno quando o `Controlado` crescer.** Se a persistencia tiver
   varios passos, mover para `<operacao>Interno()` e deixar o `Controlado` chamando so
   esse metodo. E organizacao de leitura, nao muda o limite da transacao.

**Nao conforme, chamada direta ao metodo protegido:**
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

### Divergencia consciente

O exemplo do capitulo 3 do manual coloca `indexarFeeds()` e o envio de e-mail dentro de `gerarProcedimentoControlado`. Este repositorio nao segue esse exemplo: efeito externo fica no wrapper publico, depois do retorno. Nao "corrigir" o codigo do modulo para a forma do exemplo.

A decomposicao em `<operacao>Interno` e adotada como organizacao de leitura, nao como fronteira transacional.

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

## A3 - Recurso de leitura correto por operacao

**Severidade:** Erro
**Base:** `.agents/references/padrao-auditoria-sip-sei.md`

Operacoes de leitura usam `validarAuditarPermissao`, e o recurso muda conforme a operacao. Nenhum recurso de leitura entra na regra de auditoria do SIP.

| Metodo | Recurso |
|---|---|
| `listarConectado` | `_listar` |
| `contarConectado` | `_listar`, compartilhado com listar |
| `consultarConectado` | `_consultar` |
| `bloquearConectado` | `_consultar`, compartilhado com consultar |

Helpers internos e caminhos de hook ou evento sem usuario nao recebem verificacao de sessao artificial.

**Conforme:**
```php
protected function consultarConectado(MdAbcItemDTO $objDTO)
{
    SessaoSEI::getInstance()->validarAuditarPermissao(
        'md_abc_item_consultar',
        __METHOD__,
        $objDTO
    );
}

protected function listarConectado(MdAbcItemDTO $objDTO)
{
    SessaoSEI::getInstance()->validarAuditarPermissao(
        'md_abc_item_listar',
        __METHOD__,
        $objDTO
    );
}
```

**Nao conforme:** usar `_listar` em `consultar` ou em `bloquear`. O recurso `_consultar` existe e e o que o gerador produz.

---

## T7 - `getIdConexao()` nao devolve recurso de conexao

**Severidade:** Erro

O manual e explicito: `getIdConexao()` devolve um identificador, nao um recurso de conexao do PHP. Ele nao pode ser usado em chamada direta da extensao do banco. Por questao de seguranca, o recurso de conexao e privado e controlado pela classe de banco do `InfraPHP`.

Uso legitimo e apenas testar se ja existe conexao aberta antes de abrir:

```php
if (BancoSEI::getInstance()->getIdConexao() == null) {
    BancoSEI::getInstance()->abrirConexao();
}
```

**Nao conforme:** passar o retorno de `getIdConexao()` para `mysqli_*`, `oci_*`, `pg_*` ou equivalente. O modulo nunca fala direto com a extensao do banco.

## T8 - Contrato completo dos metodos `Conectado` e `Controlado`

**Severidade:** Erro
A T1 fixa qual sufixo usar por tipo de operacao. Esta regra fixa o resto do contrato, que o manual detalha e que a T1 sozinha nao cobre.

| Item | Regra |
|---|---|
| Classe | A classe de regra de negocio herda de `InfraRN`, direta ou indiretamente |
| Visibilidade | O metodo com sufixo e `protected`, nunca `public` nem `private` |
| Parametro | O metodo aceita **um unico parametro**: o DTO da entidade ou um array encapsulador. Nao aceita multiplos parametros |
| `Conectado` | Abre conexao **se ainda nao estiver aberta**. Nao abre transacao |
| `Controlado` | Abre conexao **e** transacao, cada uma **se ainda nao estiver aberta** |
| Chamada | O consumidor chama o metodo publico sem sufixo, resolvido pela `InfraRN`. Nunca o metodo protegido |

O detalhe do "se ainda nao estiver aberta" importa em chamada encadeada: uma RN que chama outra RN nao abre uma segunda transacao, reaproveita a que ja existe.

**Conforme:**
```php
class MdAbcPedidoRN extends InfraRN
{
    protected function inicializarObjInfraIBanco(): InfraIBanco
    {
        return BancoSEI::getInstance();
    }

    protected function cadastrarControlado(MdAbcPedidoDTO $objDTO): MdAbcPedidoDTO
    {
        // um unico parametro, visibilidade protected, sufixo correto
    }
}
```

**Nao conforme:**
```php
public function cadastrarControlado(MdAbcPedidoDTO $objDTO, $numIdUsuario) // ERRO: public e dois parametros
```

---

## T9 - Antipadrao: uma transacao por elemento do laco

**Severidade:** Erro

Metodo `Conectado` que percorre uma colecao e, para cada elemento, chama uma operacao `Controlado`, abre uma transacao por elemento. O manual manda analisar se o proprio metodo do laco nao deveria ser `Controlado`, para garantir uma unica transacao em todo o processamento.

**Nao conforme:**
```php
protected function processarTudoConectado(array $arrObjDTO): void
{
    foreach ($arrObjDTO as $objDTO) {
        $this->cadastrar($objDTO); // abre e fecha uma transacao a cada volta
    }
}
```

**Conforme:**
```php
protected function processarTudoControlado(array $arrObjDTO): void
{
    foreach ($arrObjDTO as $objDTO) {
        $this->cadastrar($objDTO); // reaproveita a transacao ja aberta
    }
}
```

Consequencia do antipadrao: falha no elemento 40 de 50 deixa 39 gravados e 11 fora, sem atomicidade. Alem disso, o custo de abrir e confirmar transacao repete por elemento.

Quando a atomicidade total nao for desejada, por exemplo em processamento em lote que deve continuar apos falha isolada, a escolha por `Conectado` e legitima e deve estar registrada em comentario no metodo.

---

## T10 - Controle manual exige mecanismo auxiliar de estado

**Severidade:** Alerta
Quando o modulo assume o controle manual pelo `BancoSEI`, o conjunto e `abrirConexao()`, `abrirTransacao()`, `confirmarTransacao()`, `cancelarTransacao()` e `fecharConexao()`.

Em chamadas encadeadas entre metodos, o manual exige **implementar um mecanismo de controle auxiliar** para saber se a conexao ou a transacao ja foi aberta antes de tentar abrir de novo. Sem esse controle, o metodo interno abre uma segunda transacao ou fecha uma conexao que o chamador ainda usa.

Antes de escrever esse mecanismo, reveja a T4: na maioria dos casos a resposta certa e usar `InfraRN` com sufixo e deixar o controle com o framework.

---

## T11 - A RN repete as validacoes ja feitas na interface

**Severidade:** Erro
Todas as regras de negocio levantadas sao implementadas na RN, **inclusive as regras simples que a interface ja valida**, como tamanho maximo de campo e obrigatoriedade.

Motivo: a interface nao e o unico caminho de entrada. A mesma RN e alcancada por WebService, por evento de outro modulo e por script de tarefa, e nenhum deles passa pela validacao da tela.

---

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
| T7 | `getIdConexao()` usado como recurso de conexao | **Erro** |
| T8 | Contrato dos metodos `Conectado` e `Controlado` | **Erro** |
| T9 | Uma transacao por elemento do laco | **Erro** |
| T10 | Controle manual sem mecanismo auxiliar de estado | **Aviso** |
| T11 | RN sem as validacoes ja feitas na interface | **Erro** |
| A1 | Escrita com validarPermissao sem auditoria | **Erro** |
| A2 | Escrita sem verificacao de permissao/auditoria | **Aviso** |
| A3 | Recurso de leitura errado por operacao | **Erro** |
