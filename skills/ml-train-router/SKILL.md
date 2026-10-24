---
name: ml-train-router
description: 模型训练、微调与 RL 的总入口：分布式训练、DeepSpeed/FSDP/Megatron、LoRA/QLoRA 微调、SFT/DPO/GRPO/PPO、RLHF、蒸馏合并、MoE、长上下文、分词、语料清洗。先用它再按表读取具体 skill
---

# 模型训练、微调与 RL Router

本分类的叶子 skill 已设为仅手动调用（`disable-model-invocation: true`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用 Read 读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**用 Skill 工具调叶子（已禁止模型调用，会失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时换成 Claude Code 等价物（Agent 子代理、本地脚本）；没有等价物就告诉用户。
5. 用户点名某 skill 或 `/名字` 时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`experiment-router`、`ml-infer-router`、`llm-app-router`、`ml-domain-router`、`quant-router`、`coding-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| LLM LoRA/QLoRA 微调（未指定框架） | `llama-factory` |
| SFT/DPO/奖励模型等 HF 后训练 | `trl-fine-tuning` |
| 大模型 GRPO/PPO 强化学习（多机） | `verl` |
| 给 PyTorch 脚本加多卡分布式 | `accelerate` |
| 超大模型预训练并行策略 | `megatron-core` |
| 训练显存不够、ZeRO/offload | `deepspeed` |

## 分布式训练

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `accelerate` | 给已有 PyTorch 脚本加多卡/混合精度，accelerate config/launch，统一封装 DDP/FSDP/DeepSpeed | 调 ZeRO 细节用 deepspeed；手写 fully_shard 用 pytorch-fsdp2 |
| `deepspeed` | DeepSpeed ZeRO 1/2/3、offload、ds_config、pipeline 并行、1-bit Adam | 只想简单启动多卡用 accelerate；TP/PP 超大模型用 megatron-core |
| `pytorch-fsdp2` | 在训练脚本中加 fully_shard、DeviceMesh/DTensor、混合精度、分片 checkpoint | 整套预训练框架用 torchtitan；高层封装用 accelerate/pytorch-lightning |
| `ray-train` | Ray 集群多节点训练编排、Ray Tune 超参搜索、容错与弹性扩缩 | 数据预处理/批量推理用 ray-data；单机多卡用 accelerate |

## 微调框架

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `axolotl` | 用 Axolotl YAML 配置做 LoRA/QLoRA/全参 SFT 及 DPO/KTO/ORPO | 要 WebUI 零代码用 llama-factory；追求单卡速度用 unsloth |
| `llama-factory` | LLaMA-Factory WebUI/CLI 零代码微调 Qwen/Llama 等，QLoRA、多模态 | YAML 精细配置用 axolotl；写代码用 peft/trl-fine-tuning |
| `unsloth` | Unsloth 单卡快速省显存 LoRA/QLoRA 微调，FastLanguageModel | 多机大规模用 deepspeed/axolotl；只问 LoRA 原理与配置用 peft |
| `peft` | HF PEFT 库：LoraConfig、QLoRA、adapter 合并/多 adapter 切换 | SFT/DPO 训练流程用 trl-fine-tuning；量化细节用 bitsandbytes |

## 大规模预训练

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `megatron-core` 重 | Megatron-Core/Megatron-LM 训练 >1B 模型，TP/PP/SP/CP/EP 并行与 MFU 调优 | PyTorch 原生 4D 并行用 torchtitan；Megatron 上做 RL 用 slime/miles |
| `torchtitan` 重 | torchtitan 预训练 Llama3/DeepSeek V3，FSDP2+TP+PP+CP、Float8、torch.compile | 仅给自有脚本加 FSDP2 用 pytorch-fsdp2；NVIDIA 栈用 megatron-core |

## 训练框架

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `pytorch-lightning` | 用 LightningModule/Trainer、callbacks 组织通用训练循环并自动分布式 | HF 生态 LLM 微调用 trl-fine-tuning/axolotl；Lightning 的 LLM 用 litgpt |

## 后训练与对齐

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `trl-fine-tuning` | TRL 的 SFTTrainer、DPOTrainer、PPO、RewardTrainer 等通用 RLHF 流程 | 专做 GRPO 推理奖励用 grpo-rl-training；大规模 RL 用 verl/openrlhf |
| `grpo-rl-training` | 用 TRL GRPOTrainer 训练推理/结构化输出，设计奖励函数 | 多机大模型 GRPO 用 verl/openrlhf；SFT/DPO 用 trl-fine-tuning |
| `simpo` | SimPO 无参考模型偏好优化，替代 DPO 的对齐训练 | 标准 DPO/PPO 用 trl-fine-tuning |
| `constitutional-ai` | Constitutional AI：自我批评修订 + RLAIF 做安全/无害化对齐 | 推理时安全过滤用 llamaguard/nemo-guardrails |

## 大规模 RL

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `openrlhf` 重 | OpenRLHF 基于 Ray+vLLM+ZeRO-3 做 7B-70B PPO/GRPO/RLOO/DPO | 火山 verl 生态用 verl；Megatron+SGLang 用 slime |
| `verl` 重 | verl（Volcano Engine）PPO/GRPO 大规模后训练，FSDP/Megatron 后端、vLLM rollout | Ray+vLLM 轻量方案用 openrlhf；单机小规模用 grpo-rl-training |
| `slime` 重 | slime（Megatron+SGLang）RL 训练，GLM 模型、自定义数据生成 rollout | MoE FP8/INT4 企业级用 miles；通用 RL 用 verl |
| `miles` 重 | miles（slime fork）大 MoE FP8/INT4 RL、训推一致、speculative RL | 标准 slime 流程用 slime；非 Megatron 栈用 verl |
| `torchforge` | Meta torchforge PyTorch 原生 agentic RL，Monarch+TorchTitan，算法与基础设施解耦 | 成熟生产 RL 用 verl/openrlhf；纯预训练用 torchtitan |

## 模型压缩与合并

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `knowledge-distillation` | teacher-student 蒸馏、soft target、reverse KLD、MiniLLM 压缩模型 | 免训练合并用 model-merging；量化用 gptq/awq；剪枝用 model-pruning |
| `model-merging` | mergekit 合并微调模型：SLERP、TIES、DARE、Task Arithmetic | 需训练小模型继承能力用 knowledge-distillation |

## 架构与技术

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `moe-training` | 训练 MoE（Mixtral/DeepSeek 式），路由、负载均衡、专家并行 | Megatron 大规模 EP 用 megatron-core；MoE 的 RL 用 miles |
| `long-context` | 扩展上下文窗口：RoPE 缩放、YaRN、ALiBi、位置插值 | 注意力算子加速/省显存用 flash-attention；线性架构用 mamba/rwkv |
| `nanogpt` | 从零学习/复现 GPT-2，Karpathy nanoGPT，Shakespeare 小实验 | 生产级多架构实现与微调用 litgpt |
| `litgpt` | LitGPT 预训练/微调 Llama/Gemma/Phi/Qwen，单文件实现，LoRA/QLoRA | 教学最小实现用 nanogpt；HF 生态微调用 axolotl/peft |
| `mamba` | Mamba/Mamba-2 SSM 选择性状态空间模型训练与推理 | RNN-Transformer 混合用 rwkv；Transformer 扩上下文用 long-context |
| `rwkv` | RWKV（含 RWKV-7）线性复杂度 RNN 架构训练与推理 | SSM 架构用 mamba |
| `flash-attention` | flash-attn/SDPA 加速注意力、长序列显存优化、sliding window、H100 FP8 | 位置编码扩窗用 long-context；推理服务优化用 vllm/sglang |

## 分词与数据

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `huggingface-tokenizers` | HF tokenizers 训练 BPE/WordPiece/Unigram 词表、对齐 offset、padding/truncation | 多语种/CJK、T5 类 SentencePiece 模型用 sentencepiece |
| `sentencepiece` | SentencePiece 在原始文本上训练 BPE/Unigram，多语种与 CJK | HF fast tokenizer 流水线用 huggingface-tokenizers |
| `nemo-curator` | NeMo Curator GPU 清洗预训练语料：模糊/语义去重、质量过滤、PII 脱敏 | 通用分布式 ETL/批量推理用 ray-data |
| `ray-data` | Ray Data 分布式流式 ETL、预处理、多模态加载、批量推理 | LLM 语料去重质量过滤用 nemo-curator；分布式训练用 ray-train |
