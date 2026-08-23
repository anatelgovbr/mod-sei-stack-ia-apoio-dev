# Mapa: Modulos com Scripts de Instalacao Existentes

## Proposito

Manifesto explicito que vincula cada pasta de modulo aos seus scripts de instalacao/atualizacao.
Usado como fonte de verdade pelos guards das skills para:

1. **Impedir criacao de novos scripts** quando ja existe script para o mesmo lado SEI ou SIP do modulo.
2. **Tornar obrigatoria a atualizacao do script SEI** quando houver novo DTO, nova tabela, nova entidade CRUD base ou quando colunas forem acrescentadas a um DTO existente.
3. **Tornar obrigatoria a atualizacao do script SIP** somente quando houver impacto real em recursos, perfis, menus, parametros ou versionamento.

Consultar este arquivo ANTES de qualquer trabalho em `fontes/sei/src/main/php/sei/web/modulos/`.

---

## Regra fundamental

> **Se um lado do modulo possui script nesta lista, NUNCA crie outro script para esse mesmo lado.
> A adicao de um novo DTO, de nova tabela, de nova entidade CRUD base ou de novas colunas em um DTO existente EXIGE atualizacao do script SEI aplicavel.
> Recursos, perfis, menus, parametros ou versionamento EXIGEM atualizacao do script SIP somente quando houver impacto real.**
> Outros tipos de arquivo (RN, BD, paginas, JS, CSS, SVG, eventos, etc.) nao disparam essa obrigatoriedade por si so.

---

## Modulos mapeados

| Pasta do modulo (relativa a `modulos/`)  | Script SEI (`sei/scripts/`)                                        | Script SIP (`sip/scripts/`)                                        |
|------------------------------------------|--------------------------------------------------------------------|--------------------------------------------------------------------|
| `relacionamento-institucional/`          | `sei_atualizar_versao_modulo_relacionamento_institucional.php`     | `sip_atualizar_versao_modulo_relacionamento_institucional.php`     |
| `centraliza-modulos/`                    | `sei_atualizar_versao_modulo_centraliza_modulos.php`               | `sip_atualizar_versao_modulo_centraliza_modulos.php`               |
| `correios/`                              | `sei_atualizar_versao_modulo_correios.php`                         | `sip_atualizar_versao_modulo_correios.php`                         |
| `ia/`                                    | `sei_atualizar_versao_modulo_ia.php`                               | `sip_atualizar_versao_modulo_ia.php`                               |
| `litigioso/`                             | `sei_atualizar_versao_modulo_litigioso.php`                        | `sip_atualizar_versao_modulo_litigioso.php`                        |
| `pesquisa/`                              | `sei_atualizar_versao_modulo_pesquisa.php`                         | `sip_atualizar_versao_modulo_pesquisa.php`                         |
| `peticionamento/`                        | `sei_atualizar_versao_modulo_peticionamento.php`                   | `sip_atualizar_versao_modulo_peticionamento.php`                   |
| `pen/`                                   | `mod-pen/sei_atualizar_versao_modulo_pen.php`                      | `mod-pen/sip_atualizar_versao_modulo_pen.php` (ha tambem o legado `sip_atualizar_versao_modulo_pen.php`) |
| `utilidades/`                            | `sei_atualizar_versao_modulo_utilidades.php`                       | `sip_atualizar_versao_modulo_utilidades.php`                       |
| `cgu/`                                   | `md_cgu_eouv_atualizar_modulo.php`                                 | `md_cgu_eouv_atualizar_modulo.php`                                 |
| `trf4/julgamento/`                       | `md_julgar_atualizacao_sei.php`                                    | `md_julgar_atualizacao_sip.php`                                    |
| `apoio-plano-trabalho/`                  | `sei_atualizar_versao_modulo_apt.php`                              | `sip_atualizar_versao_modulo_apt.php`                              |

---

## Modulos sem scripts locais confirmados

| Pasta do modulo      | Observacao                            |
|----------------------|---------------------------------------|
| `abc/`               | Modulo de exemplo/gabarito TRF4       |
| `mod-sei-estatisticas/` | Sem scripts conhecidos             |
| `ws_complementar/`   | Sem scripts conhecidos                |
| `wssei/`             | Sem scripts conhecidos                |

---

## Modulos novos (nao mapeados)

Se o modulo-alvo nao constar em nenhuma das tabelas acima, ou se um dos lados
estiver marcado como nao localizado:
1. Verificar fisicamente em `sei/scripts/` e `sip/scripts/` se ha arquivo com nome relacionado.
2. Se encontrado: adicionar o modulo neste mapa antes de prosseguir.
3. Se confirmado ausente: criar scripts novos via `sei-gerador-scripts-release` e `sip-gerador-scripts-release`, conforme o escopo.

---

## Manutencao deste mapa

Atualizar esta tabela sempre que:
- Um novo modulo receber seus primeiros scripts de instalacao.
- Um script for renomeado.
- Um modulo for descontinuado (manter o registro com nota de descontinuacao).

Nao remover entradas. Apenas marcar como `[DESCONTINUADO]` quando aplicavel.
