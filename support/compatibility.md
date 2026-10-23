# Kiki Custom Skill — runtime configuration

Use the current task's instructions and the host/project's AGENTS.md or
CLAUDE.md. This collection does not choose a host, project, account or GPU.

## Installed paths

- Client: `@@KIKI_AGENT@@`.
- Skills: `@@KIKI_SKILLS_DIR@@`.
- Shared helpers and references: `@@KIKI_SUPPORT_DIR@@`.
- Current agent home: `@@KIKI_AGENT_HOME@@`.
- Installer Python: `@@KIKI_PYTHON@@`; optional TeX launcher: `@@KIKI_LATEXMK@@`.
- Research helper root: `@@KIKI_SUPPORT_DIR@@/aris`.
- Curated AcademicForge corpus: `@@KIKI_SUPPORT_DIR@@/academicforge`.

Read resources relative to the owning skill and write outputs relative to the
actual project. Never execute unfilled example placeholders.

## Machine-specific configuration

If present, read `@@KIKI_AGENT_HOME@@/skill-config/kiki-custom-skill/environment.md`
for this machine's additional configuration. Existing user and project
instructions remain authoritative. The installer neither creates nor replaces
this optional file. Record only task-relevant host aliases, project locations,
environments and execution limits there; keep credentials in their existing
credential store. Do not copy machine-specific values back into this repository.

Infer required settings from the current task and existing project configuration.
Ask one concise, grouped question only for missing information needed to proceed.
Do not demand remote-host configuration for tasks that do not use a remote host.

## Client capabilities

- Use tools actually available in this session. Map historical tool names to the
  current client's file, shell, browser/search and agent capabilities.
- Inherit the current configured model unless the user selects another. Do not
  assume a provider-specific model, runtime, dependency or plugin is installed.
- Reuse existing access to the service involved in the task. Installation does
  not transfer login sessions or authorize external actions. Investigate access
  when a requested operation fails, rather than probing unrelated accounts.
- Use a supported scheduling capability only when monitoring is requested.
  Existing channel configuration does not authorize sending messages.
- `agents/openai.yaml` is Codex metadata; Claude Code reads SKILL.md and supports
  slash invocation. Disclose missing capabilities instead of inventing results.

## Writing and workflow

- Choose the relevant writing workflow for the task: `kiki-paper-writing` or
  the multi-stage `kiki-paper-workflow`, with specialists when useful.
- Follow the user's verification policy, including explicit no-tests requests.
  Avoid repetitive review rounds or approval gates without a concrete risk.
- Author, affiliation, venue and project facts come from the actual manuscript.
  Preserve source attribution without adopting an upstream author's identity.
- An optional SCFM corpus is external: use `KIKI_SCFM_LIBRARY` or the library
  helper's `--library` argument. Never fabricate access to absent documents.

## Experiments

Determine the authorized execution environment, project root, Python environment,
data, weights and device allocation from the current task and local configuration.
Do not default to a particular server, provider, workstation or GPU count.

Before an authorized run, inspect host identity, assigned devices, disk,
processes, environment, data/weights, destination and locks. Respect queues and
existing workloads; use isolated outputs and resumable checkpoints for long jobs.
Honor local execution restrictions. A failed remote connection does not authorize
switching execution location, stopping another run or changing the experiment.

A single status request means one inspection. Recommend intervention for an
unhealthy run unless the user already authorized that intervention.

## Sources and updates

Keep licenses and source provenance. Plugin/system reference snapshots are not
installed by the script; use the client's own management for those capabilities.
Update through Git and rerun the installer. Existing targets are backed up,
unrelated skills are retained and machine-specific configuration stays local.
