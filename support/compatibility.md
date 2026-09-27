# Kiki Custom Skill — personal runtime profile

This collection is for Kiki's personal use across Codex and Claude Code. Use
the current task's instructions and the host's AGENTS.md/CLAUDE.md first.

## Installed paths

- Client: `@@KIKI_AGENT@@`; machine profile: `@@KIKI_PROFILE@@`.
- Skills: `@@KIKI_SKILLS_DIR@@`.
- Shared helpers and references: `@@KIKI_SUPPORT_DIR@@`.
- Current agent home: `@@KIKI_AGENT_HOME@@`.
- Installer Python: `@@KIKI_PYTHON@@`; optional TeX launcher: `@@KIKI_LATEXMK@@`.
- Research helper root: `@@KIKI_SUPPORT_DIR@@/aris`.
- Curated AcademicForge corpus: `@@KIKI_SUPPORT_DIR@@/academicforge`.

Read resources relative to the owning skill, and write project outputs relative
to the actual task/project. Never execute unfilled example placeholders. Machine
labels do not set a research-project root or choose a GPU automatically.

## Client capabilities and authorization

- Discover tools available in this session. Translate historical tool names into
  the current client's filesystem, shell, browser/search and agent capabilities.
  Do not assume Codex-specific MCP/tool names exist in Claude Code or on a server.
- Inherit the current configured model. Native image/presentation/document tools
  are preferred when present; otherwise use an appropriate installed capability
  or the explicitly selected backend. Do not invent unavailable tools or outputs.
- Reuse existing GitHub/Overleaf access on the current machine. Installation does
  not transfer Mac login sessions or imply remote access. No routine auth/login
  probes; investigate only an actual failed requested operation. Never copy tokens.
- Periodic monitoring uses a current client's supported scheduling capability
  only when requested. If none exists, report that limitation rather than claiming
  a monitor was scheduled. Existing channel config does not authorize messaging.
- `agents/openai.yaml` is Codex metadata; Claude Code uses SKILL.md. Use slash skill
  invocation in Claude Code. Lack of a platform-specific tool is a disclosed
  capability limitation, not a reason to silently run a different experiment.

## Writing and workflow

- Default personal paper writing: `kiki-paper-writing` (Kiki Paper Writing).
- Full multi-stage paper workflow when requested: `kiki-paper-workflow`.
- Use the smallest relevant specialist. Avoid stacking routers, universal review
  rounds and repetitive approval/test gates. Honor the user's no-tests instruction.
- Author, affiliation, venue, grant agency and project facts come from the actual
  manuscript/task. Preserve source attribution without adopting a vendor identity.
- The optional SCFM paper corpus is external: use `KIKI_SCFM_LIBRARY` or the
  library helper's `--library` argument. Never fabricate access to absent PDFs.

## Experiments

- Kiki's default authorized experiment host is `cnic-ps`, expected hostname `ps`.
  The user may explicitly select another host, including either A6000 machine.
  Installing skills is not authorization to launch or change an experiment.
- scbenchmark/scGRAIN root on CNIC: `/data1/jiaqi/scREBOUND`; use isolated
  `formal_worktrees/<run_id>` and `runs/<run_id>`. Other projects/hosts use their
  actual recorded paths, Python environment, data and weights.
- Before an authorized launch, inspect host identity, assigned GPUs, disk,
  processes, environment, data/weights, outputs and locks. Respect existing queues;
  keep jobs detached with resumable checkpoints and small audit artifacts.
- The local Mac must never run training, forward/inference, probes, profiling or
  model/data experiments, including CPU/MPS and tiny runs. No local fallback when
  a remote is unavailable. Do not alter SSH/VPN/routes or terminate unrelated jobs.
- A single status request means one read. An unhealthy run produces a stop
  recommendation unless terminating that exact run was already authorized.

## Sources and updates

Keep original licenses, pinned asset snapshots and evidence boundaries intact.
The optional plugin/system reference archive is not installed by the script.
Use each client's own plugin/system management for those capabilities. Update
this collection through Git and rerun its installer; existing targets are backed
up and unrelated skills are retained.
