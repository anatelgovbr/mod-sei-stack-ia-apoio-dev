# Spec Kit Extension Hooks

Hook file: `.specify/extensions.yml`.

Workflows may check hooks before and after major phases. Adapters are responsible
for displaying and executing hooks using the capabilities of the current tool.

## Hook Names

- `hooks.before_specify`
- `hooks.after_specify`
- `hooks.before_plan`
- `hooks.after_plan`
- `hooks.before_tasks`
- `hooks.after_tasks`
- `hooks.before_implement`
- `hooks.after_implement`

## Rules

- If `.specify/extensions.yml` is missing, continue silently.
- If the file cannot be parsed, continue silently.
- Ignore hooks with `enabled: false`.
- Treat hooks without `enabled` as enabled.
- Do not evaluate non-empty `condition` expressions unless the adapter has a
  dedicated hook executor.
- Hooks with `optional: true` are presented to the developer.
- Hooks with `optional: false` are automatic if the adapter supports execution.
