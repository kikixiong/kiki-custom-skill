---
name: ml-infer-router
description: 推理部署、量化、评测与算力的总入口：vLLM/SGLang/TensorRT-LLM/llama.cpp 部署，投机解码，AWQ/GPTQ/HQQ/bitsandbytes/GGUF 量化，剪枝，lm-eval/代码评测，Modal/Lambda/SkyPilot 云 GPU。先用它再按表读取具体 skill
---

# 推理部署、量化、评测与算力 Router

本分类的叶子 skill 已设为仅显式调用（Claude Code：frontmatter `disable-model-invocation: true`；Codex：`agents/openai.yaml` 中 `policy.allow_implicit_invocation: false`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用文件读取工具读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**通过技能调用机制加载叶子（Claude Code 的 Skill 工具会因仅显式调用而失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时：在 Codex 中照常使用；在 Claude Code 中换成等价物（Agent 子代理、本地脚本），没有等价物就告诉用户。
5. 用户点名某 skill（Claude Code 输入 `/名字`，Codex 输入 `$名字`）时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`experiment-router`、`ml-train-router`、`llm-app-router`、`ml-domain-router`、`quant-router`、`coding-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 部署一个 LLM 推理服务/OpenAI 兼容接口 | `vllm` |
| 把模型量化成 4-bit 用于 GPU 推理 | `awq` |
| 在 Mac/CPU 本地跑模型 | `llama-cpp` |
| 在显存不足时加载大模型或做 QLoRA | `bitsandbytes` |
| 跑基准评测模型能力 | `lm-evaluation-harness` |
| 租云 GPU 跑训练任务 | `skypilot` |

## 推理服务

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `vllm` | 用 vLLM 部署 OpenAI 兼容 API、PagedAttention/continuous batching 提吞吐、张量并行多卡服务 | 强结构化输出/前缀复用多改用 sglang；极致 NVIDIA 优化用 tensorrt-llm；CPU/Mac 用 llama-cpp |
| `sglang` | SGLang 服务、RadixAttention 前缀缓存、JSON/regex 约束解码、agent 工具调用、多轮对话 | 通用 OpenAI API 高吞吐部署用 vllm；纯客户端约束生成库用 outlines/guidance |
| `tensorrt-llm` | NVIDIA A100/H100 上用 TensorRT-LLM 编译引擎、FP8/INT4、in-flight batching 求最低延迟 | 快速上线或非 NVIDIA 硬件用 vllm；CPU/边缘设备用 llama-cpp |
| `llama-cpp` | llama.cpp 在 CPU、Apple Silicon、AMD/Intel GPU、边缘设备上跑推理或起本地 server | GGUF 转换和量化类型选择用 gguf；NVIDIA GPU 生产服务用 vllm |

## 量化

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `gguf` | HF 模型转 GGUF、选 Q4_K_M 等量化类型、imatrix 量化、llama.cpp 格式流程 | 只需运行推理/硬件加速配置用 llama-cpp；GPU 4-bit 量化用 awq/gptq |
| `awq` | AutoAWQ 做 4-bit 激活感知量化，指令/多模态模型，Marlin kernel，配合 vLLM 部署 | 超大模型分组 PTQ 或 QLoRA 生态用 gptq；无校准数据用 hqq；加载即量化用 bitsandbytes |
| `gptq` | AutoGPTQ 后训练 4-bit 量化、group-wise 配置、70B/405B 上消费级 GPU、带校准集 | 更看重精度保持和速度用 awq；无需校准用 hqq；训练时 QLoRA 用 bitsandbytes |
| `hqq` | HQQ 无校准数据快速量化到 4/3/2-bit，HF/vLLM 集成，量化模型上 LoRA | 需要成熟 4-bit 生产部署用 awq/gptq；8-bit/NF4 即时加载用 bitsandbytes |
| `bitsandbytes` | transformers 中 load_in_8bit/4bit、NF4/FP4、QLoRA 训练、8-bit 优化器省显存 | 追求推理速度的离线 4-bit 量化用 awq/gptq；CPU 部署用 gguf |

## 推理加速

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `speculative-decoding` | 投机解码、draft model、Medusa 多头、lookahead/Jacobi 解码降低生成延迟 | 部署服务框架本身用 vllm/sglang；压缩模型体积用量化或 model-pruning |

## 模型压缩

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `model-pruning` | Wanda/SparseGPT 剪枝、结构化/非结构化、2:4 N:M 稀疏、免重训压缩 | 降低位宽用 awq/gptq/hqq/bitsandbytes；蒸馏小模型用 knowledge-distillation |

## 评测

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `lm-evaluation-harness` | lm-eval 跑 MMLU/GSM8K/HellaSwag 等学术基准，对比模型、追踪训练进度，HF/vLLM 后端 | 代码生成 pass@k 评测用 bigcode-evaluation-harness；Slurm/Docker 规模化多 harness 用 nemo-evaluator |
| `bigcode-evaluation-harness` | 代码模型评测：HumanEval、MBPP、MultiPL-E 多语言、pass@k 指标 | 通用知识/推理基准用 lm-evaluation-harness；企业级多后端评测用 nemo-evaluator |
| `nemo-evaluator` 重 | NeMo Evaluator 容器化跑 100+ 基准，含安全/VLM，在本地 Docker、Slurm、云上规模化复现 | 单机快速跑学术基准用 lm-evaluation-harness；专门代码评测用 bigcode-evaluation-harness |

## 算力平台

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `modal` | Modal serverless GPU：按需跑函数、批处理自动扩缩、把模型部署成 web endpoint | 需要 SSH 独占实例用 lambda-labs；跨云选价/spot 编排用 skypilot；AutoDL 用 autodl-experiment |
| `lambda-labs` | Lambda Labs 按需/预留 GPU 实例、SSH 访问、持久文件系统、多节点集群训练 | 无服务器按调用计费用 modal；多云成本优化用 skypilot；AutoDL 实例用 autodl-manager |
| `skypilot` | SkyPilot 跨多云调度训练/批任务、spot 实例自动恢复、GPU 比价、managed jobs | 单一平台 serverless 用 modal；固定 Lambda 实例用 lambda-labs；AutoDL 用 autodl-experiment |
