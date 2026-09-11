# ADR-001: Processo Python persistente via socket Unix

## Status

Aceita em 2026-08-24.

## Contexto

O SEI precisa usar o `anonimizador-dp 1.1.0` para anonimizar textos extraidos
de documentos. A execucao de um processo Python por chamada recarrega spaCy,
as dependencias e o modelo NER, resultando em latencia observada de 20 a 50
segundos. Um prototipo com processo persistente e socket Unix reduziu as
chamadas subsequentes para menos de 100 ms em textos pequenos.

O processamento deve permanecer local ao pod ou container do SEI para evitar
que textos com dados pessoais trafeguem pela rede. Existem documentos com
texto extraido superior ao limite padrao de 3.000.000 de caracteres do spaCy;
um caso sintetico conhecido possui aproximadamente 5,7 milhoes de caracteres.

## Opcoes consideradas

### Processo Python por chamada

Tem menor complexidade operacional, mas recarrega o modelo em cada chamada,
apresenta alta latencia e pode criar varios processos pesados concorrentes.

### Processo persistente local por pod

Carrega o modelo uma vez, atende os modulos pelo filesystem local e nao expoe
porta de rede. Exige inicializacao e supervisao pela imagem do SEI.

### Servico separado

Permite escala e atualizacao independentes, mas exige API, autenticacao,
criptografia, observabilidade e disponibilidade proprias. Tambem faz o texto
com dados pessoais trafegar pela rede.

## Decisao

Usar um processo Python persistente por pod ou container, executado como o
usuario do Apache e acessado exclusivamente pelo socket Unix:

`/opt/anonimizador/run/anonimizador.sock`

O servidor sera versionado em:

`sei/scripts/anonimizador/servidor_anonimizador.py`

O processo executara em foreground e sera iniciado e supervisionado pelo
mecanismo da imagem. Modulos PHP serao apenas clientes e nao poderao iniciar o
daemon por `exec`, `nohup` ou mecanismo equivalente.

O contrato v1 usa JSON UTF-8, uma requisicao por conexao, e oferece as
operacoes `status` e `anonimizar`. A requisicao completa tera limite inicial
de 32 MiB. O PDF original nao sera enviado ao servidor, somente seu texto
extraido.

Textos extensos serao divididos internamente em blocos de ate 1.000.000 de
caracteres, priorizando limites de paragrafo, linha, frase e palavra. Os blocos
serao processados sequencialmente com a mesma engine e recompostos na ordem
original. O servidor nao aumentara `nlp.max_length` para acomodar o documento
inteiro.

A primeira versao usara um worker serial por pod. Paralelismo somente sera
adicionado mediante teste de carga que demonstre necessidade.

A indisponibilidade sera retornada como erro ao modulo consumidor, que definira
se bloqueia ou degrada seu fluxo. A saude do daemon nao bloqueara a readiness
geral do SEI.

## Consequencias

### Positivas

- elimina a recarga do modelo em cada chamada;
- mantem os dados no pod ou container do SEI;
- oferece um contrato unico para modulos consumidores;
- isola do PHP os limites e o particionamento exigidos pelo spaCy;
- permite evoluir a implementacao sem alterar clientes compativeis com o
  contrato v1.

### Negativas

- adiciona um processo a ser supervisionado em cada pod;
- mantem uma copia do modelo em memoria por pod;
- o worker serial pode formar fila sob concorrencia elevada;
- entidades que atravessem uma fronteira de bloco exigem validacao funcional;
- alteracoes no servidor exigem nova imagem e reinicio dos pods para carregar
  o codigo.

## Responsabilidades

Este repositorio entrega o servidor, os testes, o contrato, o cliente de
diagnostico e o roteiro operacional. A equipe responsavel pela imagem entrega
o Dockerfile, startup, supervisao e manifests reais, preservando o entrypoint
existente e o rollback por digest.