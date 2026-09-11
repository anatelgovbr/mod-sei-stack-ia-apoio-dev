# Padrão de Codificação PHP — Convenções SEI/TRF4

Convenções específicas do ecossistema SEI adotadas pelo TRF4. Não cobre regras gerais de PHP
(PSR, formatação de blocos, indentação etc.) que o modelo já conhece.

---

## Disposição dos Elementos

Todo arquivo PHP do SEI deve seguir esta ordem de seções:

1. Bloco de identificação
2. Seção de *includes*
3. Declarações de classe ou interface
4. Instanciação de classes e processamentos
5. Liberação de recursos (conexão, resultset, arrays...)
6. Geração de HTML

---

## Bloco de Identificação

Todo arquivo deve iniciar com o bloco de cabeçalho da instituição:

```php
/*

* TRIBUNAL REGIONAL FEDERAL DA 4ª REGIÃO
* 99/99/9999 – criado por SSS
* 99/99/9999 - Alterado por SSS: (descrição resumida...)

*/
```

> **Nota CRUD generator:** não sintetize este bloco em arquivos gerados automaticamente
> a menos que o artefato de origem realmente o exija ou haja solicitação explícita.

---

## Nomenclatura de Classes de Módulo SEI

Classes criadas em módulos SEI devem usar o prefixo `Md` seguido da sigla da instituição
e do módulo, em PascalCase:

```
MdAbcPedido
MdRiClassificacao
```

### Nome do arquivo igual ao nome da classe

A classe e salva em arquivo com o mesmo nome, incluindo a caixa. A classe `AbcExemploIntegracao` mora em `AbcExemploIntegracao.php`, e `MdAbcPedidoRN` mora em `MdAbcPedidoRN.php`.

Vale para toda classe do módulo, não só para a de integração. Em servidor Linux o sistema de arquivos diferencia maiúsculas de minúsculas, então divergência de caixa quebra o carregamento em produção mesmo funcionando em ambiente local com sistema de arquivos insensível.

---

## Prefixo de Instâncias

Instâncias de classe usam o prefixo `obj` seguido do nome da classe:

```
objMdAbcPedido
objProcedimentoAPI
```

Múltiplas instâncias da mesma classe usam sufixo descritivo em camelCase (sem sublinhado):

```
objMdAbcPedidoOriginal
objMdAbcPedidoReclassificado
```

---

## Prefixos de Atributos e Variáveis Locais

O tipo do dado determina o prefixo da variável (atributos de classe e variáveis locais seguem
a mesma convenção):

| Tipo             | Prefixo | Exemplo              |
|------------------|---------|----------------------|
| Número           | `num`   | `numIdade`           |
| Valor monetário  | `din`   | `dinSalario`         |
| String           | `str`   | `strNome`            |
| Data             | `dta`   | `dtaNascimento`      |
| Data/Hora        | `dth`   | `dthEntrega`         |
| Array            | `arr`   | `arrObjProcessos`    |
| Booleano         | `bol`   | `bolEntregue`        |

---

## Variáveis de Sessão

Variáveis de sessão usam prefixo `S_` em maiúsculas, termos compostos separados por sublinhado:

```
S_USUARIO
S_NOME_SISTEMA
```

---

## Sintaxe Moderna de Arrays

Em codigo PHP novo ou alterado, nao usar `array()`.
Use sempre a sintaxe curta `[]`, compativel com o baseline atual do projeto em PHP 8.2.

Exemplos:

```php
$arrItens = [];
$arrItens = ['a', 'b'];
```

Evitar:

```php
$arrItens = array();
$arrItens = array('a', 'b');
```

Regra de migracao:

- Ao editar um trecho, normalizar `array()` para `[]` quando a alteracao for local e segura.
- Nao fazer refatoracao massiva apenas para trocar sintaxe sem necessidade funcional.

---

## Tipagem Segura

Em codigo PHP novo ou alterado, preferir tipagem explicita quando o contrato for
claro e a compatibilidade com a heranca estiver confirmada.

Aplicar por ordem de seguranca:

1. propriedades com atribuicoes estaveis e previsiveis
2. metodos `private` e helpers locais
3. construtores
4. metodos `public`/`protected` sem heranca relevante
5. overrides de classes do core, apenas apos confirmar compatibilidade da assinatura

Regras:

- Em overrides, verificar primeiro a assinatura no core (`SeiIntegracao`, `InfraRN`,
  `InfraDTO` ou classe pai concreta) antes de adicionar ou estreitar tipos.
- Tipo de retorno pode ser adicionado quando o contrato estiver claro e permanecer
  compativel com a heranca.
- Nao adicionar tipo de parametro em override quando o metodo pai estiver sem tipo
  ou quando isso estreitar a assinatura de forma incompativel.
- Preferir tipos nativos (`string`, `int`, `bool`, `float`, `array`, `?Tipo`,
  `int|float`) antes de anotacoes ambiguas.
- Nao introduzir `declare(strict_types=1)` sem solicitacao explicita do desenvolvedor.
- Nao fazer refatoracao estrutural apenas para forcar tipagem.

Paginas procedurais `*_lista.php` e `*_cadastro.php` ficam fora do escopo padrao de
tipagem. So extrair helpers/funcoes para tipar quando o desenvolvedor pedir essa
refatoracao explicitamente.

---

## PHPDoc Breve em Metodos

Metodos PHP novos ou alterados devem receber PHPDoc breve quando a leitura do
comportamento nao for trivial ou quando houver ganho claro de manutencao.

Regras:

- Comecar com uma frase curta explicando o que o metodo faz.
- Incluir `@param`, `@return` e `@throws` quando agregarem contexto util.
- Em arrays, complementar com tipo em PHPDoc quando o tipo interno importar
  (ex.: `string[]`, `MdAptAssocEtapaModeloDTO[]`).
- Evitar comentarios redundantes ou mecanicos, como "Retorna o valor" ou
  "Inicializa a variavel" sem contexto adicional.
- Nao criar blocos longos em funcoes triviais so para repetir a assinatura.

---

## Prefixos de Elementos HTML

Elementos HTML em páginas SEI seguem a tabela abaixo:

| Elemento                    | Prefixo |
|-----------------------------|---------|
| `<input type="text">`       | `txt`   |
| `<input type="password">`   | `pwd`   |
| `<input type="checkbox">`   | `chk`   |
| `<input type="radio">`      | `rdo`   |
| `<input type="submit">`     | `sbm`   |
| `<input type="reset">`      | `rst`   |
| `<input type="file">`       | `fil`   |
| `<input type="hidden">`     | `hdn`   |
| `<input type="image">`      | `img`   |
| `<input type="button">`     | `btn`   |
| `<form>`                    | `frm`   |
| `<div>`                     | `div`   |
| `<table>`                   | `tbl`   |
| `<frame>`                   | `fra`   |
| `<iframe>`                  | `ifr`   |
| `<textarea>`                | `txa`   |
| `<label>`                   | `lbl`   |
| `<select>`                  | `sel`   |

Exemplo:

```
btnFechar
tblAcordaosPublicados
txtNomeParte
```

## Diagnostico de acento quebrado

Antes de mexer no conteudo do arquivo, conferir as duas causas possiveis, nesta ordem:

1. **Codificacao do arquivo.** O arquivo PHP e ISO-8859-1, sem BOM, sem caractere fora de Latin-1.
2. **`default_charset` do PHP.** O runtime precisa estar coerente com `ISO-8859-1`. Arquivo correto com `default_charset` divergente produz acento quebrado do mesmo jeito.

Nao assumir `UTF-8` como padrao implicito do projeto. O erro mais comum e corrigir o arquivo quando o defeito esta no runtime, ou o contrario.

## Convencoes de nomenclatura, quadro completo

| Elemento | Regra |
|---|---|
| Nome de arquivo | Apenas letras minusculas, numeros e sublinhado, mais a extensao |
| Um arquivo por classe | Classe ou interface usa arquivo individual, com o nome do arquivo obrigatoriamente igual ao da classe |
| Indentacao | De dois a quatro espacos por nivel. **Nunca tabulacao** |
| Nome de classe | Substantivo no singular, prefixo `Md` mais a sigla da instituicao e do modulo, em PascalCase |
| Sem preposicoes | Nao usar preposicao nos nomes |
| Constantes | Todas as letras em maiusculo |
| Metodos | Verbo no infinitivo, apenas letras minusculas |
| Atributos e variaveis | Prefixo mais qualificador |
| Elementos HTML | Prefixo mais qualificador |

O prefixo `md` seguido da sigla vale para todos os artefatos, nao so para classes: recursos, tabelas, parametros, chaves de cache e atributos de sessao.

## InfraException

**`try/catch` obrigatorio.** Para que o tratamento de erro ocorra de forma adequada, todo o codigo e implementado com blocos `try ... catch`, encadeando a excecao original. Ver a regra T5 em `.agents/skills/sei-verificacao-rn/references/padroes-transacao.md`.

**Validacao imediata.** A `InfraException` oferece o lancamento imediato de uma excecao contendo a validacao passada como parametro. Usar para regra de negocio violada, em vez de montar mensagem solta e interromper o fluxo por outro caminho.
