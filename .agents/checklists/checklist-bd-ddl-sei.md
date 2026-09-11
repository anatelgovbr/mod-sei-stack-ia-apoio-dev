# Checklist de BD, DDL e Release SEI

Checklist operacional para revisar `*BD.php`, DDL e scripts de release SEI/SIP.

## Fontes de verdade

- `.agents/references/padrao-modelagem-dados.md`
- `.agents/references/padrao-scripts-release.md`
- `.agents/references/gates-de-implementacao.md` - `R1`, `R3`, `R5`, `R6`
- `.agents/checklists/checklist-seguranca.md` - `B1-B6`
- `.agents/security/matriz-vulnerabilidades-sei.md` - `V05`

## Quando usar

- `*BD.php`
- scripts `sei_atualizar_versao_modulo_*.php`
- scripts `sip_atualizar_versao_modulo_*.php`
- DDLs SQL e revisao pre-release

## Checklist operacional

| # | Item | Origem | Severidade |
|---|---|---|---|
| 1 | DDL usa tipos portaveis e evita construtos proprietarios sem necessidade; para sequencias nativas, seguir a estrategia multi-SGBD prevista no manual | `B1`, `DB08`, manual cap. 5 `Sequencias` | BLOQUEANTE |
| 2 | `CREATE TABLE` usa `InfraMetaBD::tipo*()` e helpers do core quando disponiveis | `padrao-scripts-release.md` | ALTA |
| 3 | PK, FK, AK, indice e sequence respeitam naming e limite de tamanho | `DB03`, `DB05`, `DB07`, `DB10`, `DB11` | BLOQUEANTE/AVISO |
| 4 | FK relevante possui indice explicito ou helper equivalente | `DB09` | AVISO |
| 5 | Nao ha concatenacao insegura de entrada em SQL customizado | `B6`, `V05` | BLOQUEANTE |
| 6 | Mudanca estrutural em modulo mapeado atualiza o script existente do modulo | `R1`, `R6` | BLOQUEANTE |
| 7 | Impacto de release no lado SEI, SIP ou ambos esta refletido no(s) script(s) correto(s) | `R1`, `R4`, `R6` | BLOQUEANTE |
| 8 | `getVersao()` em `*Integracao.php` esta sincronizado com os scripts quando houver bump de release | `R3` | BLOQUEANTE |
| 9 | DDL N:N nao cria sequence desnecessaria | `padrao-modelagem-dados.md` secao `Sequencias / auto-incremento` | ALTA |

## Observacoes praticas

- Para `ALTER TABLE`, PK, FK e indice, preferir helper do core ao SQL bruto.
- Em modulo ja mapeado em `mapa-modulos-scripts.md`, nao criar script novo.
- `AUTO_INCREMENT` e `IDENTITY` aparecem no manual apenas como implementacao de
  sequence multi-SGBD, nao como estrategia geral para tabela funcional comum.

---

## Isolamento e extensao da camada BD

- [ ] A classe de terceira camada herda de `InfraBD` e repassa ao construtor a instancia de banco recebida.
- [ ] **Uma BD persiste ou atualiza dados em uma unica tabela.** Nao gravar em duas tabelas na mesma classe.
- [ ] **Nao ha comunicacao direta entre BDs.** Se a operacao precisar de duas tabelas, quem orquestra e a RN.
- [ ] Comportamento especifico implementado pelos pontos de extensao do `InfraBD`, e nao por SQL solto no meio do metodo.
- [ ] `getObjInfraIBanco()` usado para recuperar o objeto de banco passado ao construtor, em vez de instanciar um novo.

A regra de uma tabela por BD e o que permite ao gate identificar acoplamento indevido entre entidades. Quebra-la costuma indicar que a modelagem precisa de uma entidade nova, e nao de uma BD maior.
