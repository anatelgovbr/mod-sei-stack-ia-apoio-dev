# Gestão de multa

Lançamento da multa aplicada no processo litigioso como crédito no Sistema de Arrecadação e divisão desse crédito em boletos, usados pelo usuário que gerencia a multa do processo.

Fora do escopo: retificação, majoração e cancelamento do lançamento (ainda não documentados); envio do documento do interessado quando o tipo de controle dispensa o número complementar (questão em aberto com a área de negócio).

Regras de negócio: [regras-de-negocio.md](../regras-de-negocio.md).

## Inclusão do lançamento

### RF-LIT-001: Obter o número complementar do interessado

Enquanto o tipo de controle exige o número complementar do interessado, quando o lançamento é incluído sem esse número, o sistema deve obter o número no Sistema de Arrecadação e enviá-lo no lançamento.

- Verificação: teste automatizado - [MdLitIncluirLancamentoRNTest](../../../../tests/unit/sei/web/modulos/litigioso/rn/MdLitIncluirLancamentoRNTest.php), caso "lançamento sem Fistel, controle exige complemento"; caso indesejado em RF-LIT-004 e RF-LIT-005.

### RF-LIT-002: Gravar o número complementar obtido

Quando o Sistema de Arrecadação devolve o número complementar do interessado, o sistema deve gravar o número no cadastro do interessado.

- Verificação: teste automatizado - [MdLitNumeroInteressadoRNTest](../../../../tests/unit/sei/web/modulos/litigioso/rn/MdLitNumeroInteressadoRNTest.php), integração em SOAP 1.1 e 1.2; caso indesejado em RF-LIT-005.

### RF-LIT-003: Enviar o número complementar já informado

Enquanto o tipo de controle exige o número complementar do interessado, quando o lançamento já tem esse número, o sistema deve enviar o número informado no lançamento.

- Verificação: teste automatizado - [MdLitIncluirLancamentoRNTest](../../../../tests/unit/sei/web/modulos/litigioso/rn/MdLitIncluirLancamentoRNTest.php), caso "lançamento com Fistel, controle exige complemento".

### RF-LIT-004: Recusar o lançamento sem a integração do número complementar

Se a integração "Gerar Número do Interessado para Entidade não Outorgada" não está parametrizada, então o sistema deve recusar o lançamento e orientar a parametrização pela Administração do SEI.

- Verificação: teste automatizado - [MdLitNumeroInteressadoRNTest](../../../../tests/unit/sei/web/modulos/litigioso/rn/MdLitNumeroInteressadoRNTest.php), caso "Gerar Número do Interessado sem integração cadastrada".

### RF-LIT-005: Interromper o lançamento quando o número complementar falha

Se o Sistema de Arrecadação falha ao gerar o número complementar do interessado, então o sistema deve interromper o lançamento e manter o interessado sem número.

- Verificação: teste automatizado - [MdLitNumeroInteressadoRNTest](../../../../tests/unit/sei/web/modulos/litigioso/rn/MdLitNumeroInteressadoRNTest.php), caso "SIGEC fora do ar".

## Fracionamento

### RF-LIT-006: Valorar cada decisão no fracionamento

Quando o usuário fraciona a multa, o sistema deve considerar, para cada decisão, o valor da decisão conforme a RN-LIT-001.

- Verificação: teste automatizado - [MdLitLancamentoINTTest](../../../../tests/unit/sei/web/modulos/litigioso/int/MdLitLancamentoINTTest.php), casos sem origem, majoração, redução, origem sem lançamento e origem sem multa.
