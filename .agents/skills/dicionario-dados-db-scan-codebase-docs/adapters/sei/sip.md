# Adaptador: SIP

Família InfraPHP. Aplique `convencoes-infraphp.md`.

## Reconhecimento

Reconheça SIP e `docs/dicionario_dados/sip/` como evidências diretas. Nome como `servico`, `sistema`, `recurso`, `perfil`, `menu` ou `login_sso` é provisório; discrimine-o pelo script, DTOs e destino.

## Fonte estrutural

`fontes/sei/src/main/php/sip/scripts/atualizar_versao_sip.php`, classe `VersaoSipRN extends InfraScriptVersao`, sobre `BancoSip`. A definição de dados para conferência fica em `fontes/sei/src/main/php/sip/web/dto/` e `bd/`.

## Versionamento

Regras comuns de versão-alvo, âncora, assinatura de bloco, baseline e bloqueios para adaptadores `setArrVersoes` ficam em `convencoes-infraphp.md`.

### Gramática e ordenação

O rodapé chama `setArrVersoes` com chaves `M.m.*` e métodos `versao_M_m_0`. Ordene pelo mapa.

### Identificadores e âncoras

- A numeração do SIP é independente da numeração do SEI.

### Extração por versão

Localize a entrada do mapa, delimite o método apontado por contagem de chaves e preserve a ordem das operações. Siga apenas auxiliares chamados pelo bloco. Registre o efeito estrutural por `BancoSip` e mantenha separado qualquer objeto homônimo encontrado no SEI.

### Versão-alvo

Leia `const SIP_VERSAO` em `fontes/sei/src/main/php/sip/web/Sip.php` a cada execução. Não derive esse valor da faixa estrutural nem de `SEI_VERSAO`.

## Títulos

- Dicionários: `Dicionário de Dados do SIP`.
- `CHANGELOG.md`: `Changelog do SIP`.
- Relatório de atualização: aplique o template de `convencoes-infraphp.md` com slug `sip`.

## Camadas semânticas

| Evidência | Caminhos |
|---|---|
| Estrutura | `sip/scripts/atualizar_versao_sip.php` |
| Modelo, regra, consulta e escrita | `sip/web/dto/`, `rn/` e `bd/` |
| Integração | `sip/web/ws/` e `.wsdl` |
| Interface e comportamento | páginas `sip/web/*.php` e `sip/web/js/*.js` |
| Documentação, relatórios, testes e comentários | inventarie no escopo a cada execução |

## Estratégia de busca

Siga a ordem de investigação de `convencoes-infraphp.md` sobre `sip/web/`. Exclua `assinatura/` e `sso/` sem referência direta. Confirme o lado do banco e não combine homônimos do SEI.

## Particularidades

- Tabela homônima em SEI e SIP representa objetos distintos até prova estrutural em contrário.
- Limpeza de artefato por `DROP TABLE` só afeta o dicionário quando o objeto pertence ao alcance documentado do SIP.

## Validações

- Confirme `BancoSip` e os DTOs SIP para cada tabela ou coluna analisada.
- Valide que a versão do título veio de `SIP_VERSAO`, separada da faixa estrutural.
- Restrinja mudanças aos objetos alcançados pelos blocos estruturais comprovados.

## Bloqueios

- Objeto homônimo em outro esquema sem confirmação de lado: bloqueie.

## Destino

- Dicionários e `CHANGELOG.md`: `docs/dicionario_dados/sip/`.
