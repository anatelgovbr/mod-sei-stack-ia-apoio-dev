# Controle Litigioso (sigla LIT)

O módulo controla os processos litigiosos de fiscalização, das situações e decisões até a gestão da multa aplicada, com lançamento, retificação, majoração e fracionamento dos créditos no Sistema de Arrecadação.

- Requisitos técnicos: [requisitos-tecnicos.md](requisitos-tecnicos.md)
- Dicionário de dados: [docs/dicionario_dados/litigioso/](../../dicionario_dados/litigioso/)
- Instalação e operação: [README do módulo](../../../fontes/sei/src/main/php/sei/web/modulos/litigioso/README.md)
- Como manter esta documentação: [docs/requisitos-ancorados/README.md](../README.md)

## Regras de negócio

O texto de cada regra está em [regras-de-negocio.md](regras-de-negocio.md).

- Decisão
  - RN-LIT-001: Valor de decisão que substitui decisão lançada

## Requisitos funcionais

- [Gestão de multa](requisitos-funcionais/gestao-de-multa.md): número complementar do interessado na inclusão do lançamento e valor das decisões no fracionamento.

## Glossário

| Termo | Definição |
|---|---|
| Sistema de Arrecadação | Sistema externo que registra os créditos da multa e emite os boletos, acessado pelas integrações parametrizadas na Administração do SEI. |
| Número complementar do interessado | Número que identifica o interessado no Sistema de Arrecadação, o Fistel, enviado em cada lançamento da multa. |
| Tipo de controle litigioso | Configuração administrativa que define, entre outros pontos, se o lançamento exige o número complementar do interessado. |
| Lançamento | Crédito da multa registrado no Sistema de Arrecadação, que gera um boleto. |
| Decisão de origem | Decisão anterior que uma nova decisão substitui no mesmo processo. |
| Valor da decisão | Valor que uma decisão acrescenta ao lançamento, conforme a RN-LIT-001. |
| Fracionamento | Divisão das decisões de um lançamento em um boleto inicial e boletos secundários. |
| Boleto inicial e boletos secundários | No fracionamento, o boleto inicial é o lançamento de origem da família, e os boletos secundários são os lançamentos vinculados a ele. |
