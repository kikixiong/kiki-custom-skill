# Kiki execution notes for the Anthropic Skill Creator

This copy retains the Anthropic workflow and bundled scripts. These notes adapt
execution to the current Codex or Claude Code environment; they do not make the
Claude-specific scripts native Codex evaluation tools.

## Choose the requested depth

For importing an upstream version or making a narrow edit, use file and static
checks. Follow the current user's verification policy; do not automatically run
baseline agents, benchmarks, repeated review rounds, or description optimization.
Use those workflows when the user requests evaluation or authorizes a specific
evaluation plan. Reuse intent and decisions already clear from the conversation.

## Runtime differences

- In Codex, use the actual available file, browser and subagent tools. References
  to Claude in the general authoring workflow mean the current assistant.
- `scripts/run_eval.py`, `scripts/improve_description.py`, and `scripts/run_loop.py`
  call `claude -p`. They require an available Claude CLI and existing authorized
  access. Their results measure Claude behavior, not Codex skill triggering.
  Do not pass a Codex/GPT model ID as a Claude model or invent replacement calls.
- Record token counts and timing only when the runtime actually supplies them;
  otherwise mark them unavailable rather than inventing benchmark measurements.
- `scripts/quick_validate.py` and packaging require PyYAML. The file validator
  checks structure; it does not establish behavioral quality. Do not install
  model runtimes or launch model/data evaluations as part of a file update.
- Evaluation workloads must follow the current user's execution and data-handling
  restrictions. Use the authorized environment; do not infer a particular host
  or silently switch execution location.

## Review output

Use the bundled viewer when evaluating outputs. A static HTML export is suitable
when a browser server is unavailable. Open artifacts using the current client's
actual tools; the upstream `present_files` and TodoList tools may not exist.
