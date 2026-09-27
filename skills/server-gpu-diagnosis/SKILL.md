---
name: server-gpu-diagnosis
description: 排查 CUDA、GPU 可见性、环境、显存和服务器运行问题。
metadata:
  source-repository: xll0328/skill_sony
  source-revision: e2d15ad91892f90f0cdc7db6a82971f2de0b659d
  local-profile: kiki-custom-skill
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Server GPU Diagnosis

Diagnose the requested remote GPU environment. The default host is SSH
`cnic-ps`; check that its actual hostname is `ps`. No GPU/model/data diagnostics
may fall back to CPU or MPS on the user's Mac.

## Locate the environment

For scbenchmark/scGRAIN, use `/data1/jiaqi/scREBOUND` and the actual run's
`formal_worktrees/<run_id>` / `runs/<run_id>` records. Other projects use their
own recorded roots. Identify the exact Python executable, container or conda
environment from the launch record; do not guess an environment name.

## Diagnosis ladder

1. Read remote hostname, job/namespace, GPU allocation and visibility settings.
2. Read remote `nvidia-smi`, device-node visibility, disk status and the target
   process's existing logs. Respect assigned devices and locks.
3. Inspect environment/package metadata and project dependency pins. Distinguish
   driver visibility, container visibility and framework compatibility. A working
   `nvidia-smi` alone does not prove the training environment sees CUDA.
4. Read existing diagnostics/preflight scripts before deciding whether to run
   them. Do not execute a script just because it is named `preflight`: it may
   allocate GPUs, run a model or mutate shared state.
5. If a framework-level diagnostic is needed within the user's authorized scope,
   run only the smallest relevant check on the remote host in the recorded
   environment and assigned GPU context. Do not run training/forward/inference
   or profiling as an implicit diagnosis step.

## Interpretation and output

- Driver visible but framework unavailable: inspect package/runtime compatibility.
- Missing device nodes: inspect the current remote namespace/container allocation.
- Partial visibility: inspect scheduler allocation and CUDA_VISIBLE_DEVICES.
- OOM: inspect recorded memory use, batch/context settings and other processes;
  do not kill processes or change hyperparameters automatically.

Report the failing layer, observed evidence and smallest authorized corrective
step. Do not modify SSH/VPN/routes, seize GPUs, stop others' jobs, reinstall a
shared environment or launch an experiment just to obtain a cleaner diagnostic.
If the host is unreachable, report that blocker without a local fallback.
