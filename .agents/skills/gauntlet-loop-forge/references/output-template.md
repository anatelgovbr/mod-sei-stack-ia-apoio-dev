# Final Prompt Assembly

The returned artifact has two parts, in this order, and both parts ship every time.

## Part 1: the user's prompt, unchanged

Reproduce the prompt the user supplied, verbatim: its wording, its fields, its filled values, and its placeholders. Parameters the user wrote for the loop, such as the bar, the behavior to preserve, or the maximum effort, belong to that prompt and stay where the user put them.

When the prompt lacks a fact the loop needs, ask for it in the interview and leave the user's text as it is.

When the user brought a goal instead of a prompt, there is no text to reproduce: write this part from the interview answers, keeping the user's own words wherever they exist. The line that invoked this skill is the request, not the prompt, so it stays out of the artifact.

## Part 2: the loop block, appended after it

Whoever runs the artifact never reads this skill, so write every rule out in full inside the block. A bullet below that names a `SKILL.md` section tells you where to read the definition, not what to write.

Copy every identifier, section title, path and command from its source, worded as the source words it, after reading that source. When the source skips an id inside a range, list the ids it carries instead of the range.

Emit these headings exactly, in this order, `##` for the title and `###` for the sections:

```
## Gauntlet Loop de Verificação

### O que é relevante verificar

- ...
- ...

### Fluxo do Time de Agentes em Loop

- ...
- ...

### Papéis

- ...
- ...

### Registro

- ...
- ...

### Limites de Esforço de Verificação em Loop

Todos finitos:
- ...
- ...
```

The three headings above are the spine: keep them, in that order, with the limits section last. Give every other scope its own `###` section instead of nesting it inside one of the three, and name it in the same plain style. For a team-and-loop mission the usual ones are `### Papéis`, `### Pacote de Despacho`, `### Rodada Local`, `### Estados`, `### Integração`, `### Autorização Escrita` and `### Registro`. One scope per section, and a list inside a section goes one level deep at most. When the user's prompt is in another language, translate the headings and keep the order and the meaning. In Portuguese, write the bar as `padrão de qualidade`, the ledger as `registro`, a workstream as `frente`, the lead as `coordenador`, a fresh verifier as `verificador independente`, the dispatch packet as `pacote de despacho`, and a human gate as `autorização escrita`, everywhere you write, including the decisions you record in part 1 and any field label. Text quoted from the user keeps the user's own words. Keep the statuses `PASS`, `FAIL` and `CAPPED` as they are, and write the rest as `INCONCLUSIVO`, `BLOQUEADO`, `ESCALAR` and `PARADO`. When that prompt carries a human gate, such as waiting for approval before editing, open the block with the step the rounds apply to, and start no round before the gate.

Write a set of three or more items as a list, one per line, with the item's name leading: roles, assigned criteria, mandatory gates, limits and statuses. A rule that binds two items gets its own line after the list, so it stays in one place.

### O que é relevante verificar

- the bar: name it, and require the verifier to obtain and inspect the real bar or measurement before judging;
- the acceptance criteria and the hard gates, each with a credible evidence path;
- the decomposition: the lead splits the mission into the smallest independently judgeable workstreams and chooses the split itself;
- coverage: every artifact and dimension in scope has an owner, and an unowned cell is a coverage hole;
- evidence: the verifier inspects the actual current artifact, an executor's claim is not evidence, and a mandatory gate that never ran is missing evidence;
- absence claims, written as `SKILL.md` section 6 defines them;
- what must be preserved, and what stays out of scope.

### Fluxo do Time de Agentes em Loop

- roles, one agent per role: lead, one executor per workstream, a fresh verifier per cycle, integrator, fresh final verifier;
- degraded environment: when the runtime opens no separate context per role, say so in the first answer and call the verification self-assessment;
- the dispatch packet, the workstream boundary, the local cycle and the statuses, written as `SKILL.md` sections 5, 7 and 8 define them, with the domain's own vocabulary named beside the loop statuses;
- integration: assemble the locally passing pieces, inspect interfaces and consistency, run the global gates, and use a fresh final verifier;
- human gates: what takes explicit written approval;
- ledger: the progress artifact and the fields it holds.

### Limites de Esforço de Verificação em Loop

Open the section with `Todos finitos:` and then one limit per line, each carrying its derived integer. Keep this order and these names, replacing `buscador` and `verificador` with the role names this mission uses:

```
Todos finitos:
- frentes de trabalho: no máximo 3
- rodadas por frente: no máximo 8
- execuções do buscador por frente: no máximo 8
- execuções do verificador por frente: no máximo 11
- rodadas de integração: no máximo 4
- reserva para integração e verificação final: 4 rodadas das 22 e 25 minutos dos 120, que as frentes não podem gastar
- tempo de uma execução do buscador: no máximo 15 minutos
- tempo de uma execução do verificador: no máximo 10 minutos
- agentes simultâneos: no máximo 3
- profundidade de delegação: 1, ou seja, buscador e verificador não abrem outros agentes
- rodadas somadas em todo o trabalho: no máximo 22
- agentes abertos em todo o trabalho: no máximo 54
- tempo total: no máximo 120 minutos
- ampliar qualquer limite por conta própria: proibido
```

Those integers are the set for 8 rounds per workstream across 3 workstreams. Derive the set for the effort the user gave with `references/bounded-execution.md`, carry the integers themselves, and leave the formulas and the internal limit names behind in the forge.

Close the section with the accounting rules: every retry, replan, second opinion and re-verification counts against these limits; the lead checks the remaining budget before each spawn and refuses one that would invade the reserve; the run stops as soon as the evidence supports the result; and two consecutive rounds without progress change the strategy instead of repeating the attempt up to the ceiling. The terminal state reported is the one the run reached, and an exhausted ceiling is reported as `CAPPED`.

## Conditional software clauses

Include only when the software profile is active and the clause is relevant:

- "For behavior-changing work, use a bounded TDD micro-loop: define the next behavior, prove a focused test fails for the expected reason when feasible, implement the smallest coherent change to make it pass, refactor while green, then run the broader relevant regression and integration gates."
- "A verifier must confirm that the tests meaningfully represent the acceptance behavior, that they were not weakened to obtain green, and that the actual current code and runtime pass the relevant functional, contract, reliability, security, performance, migration, and compatibility gates."
- "For bug fixes, prefer a pre-fix regression test. For refactors and legacy work, establish characterization tests before risky structural change. Use task-appropriate alternatives when strict red-first TDD is not meaningful."

Select the risk-relevant gates from the software references, and carry only those into the final prompt.
