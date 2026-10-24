---
name: ml-domain-router
description: 多模态、机器人与可解释性的总入口：CLIP、BLIP-2、LLaVA、SAM、Stable Diffusion、Whisper、MusicGen、pi0/OpenVLA/Cosmos Policy、LIBERO、TransformerLens、SAE、nnsight、pyvene、activation patching。先用它再按表读取具体 skill
---

# 多模态、机器人与可解释性 Router

本分类的叶子 skill 已设为仅显式调用（Claude Code：frontmatter `disable-model-invocation: true`；Codex：`agents/openai.yaml` 中 `policy.allow_implicit_invocation: false`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用文件读取工具读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**通过技能调用机制加载叶子（Claude Code 的 Skill 工具会因仅显式调用而失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时：在 Codex 中照常使用；在 Claude Code 中换成等价物（Agent 子代理、本地脚本），没有等价物就告诉用户。
5. 用户点名某 skill（Claude Code 输入 `/名字`，Codex 输入 `$名字`）时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`experiment-router`、`ml-train-router`、`ml-infer-router`、`llm-app-router`、`quant-router`、`coding-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 零样本图像分类或以文搜图 | `clip` |
| 看图回答问题/与图片对话 | `llava` |
| 文本生成图片 | `stable-diffusion` |
| 音频/视频转文字 | `whisper` |
| 微调或部署机器人 VLA 策略（未指明模型） | `openpi` |
| 机制可解释性/activation patching（未指明框架） | `transformer-lens` |

## 视觉理解

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `clip` | CLIP 零样本图像分类、图文相似度、以图搜图/以文搜图、跨模态检索与 embedding | 生成图像描述用 blip-2；多轮看图对话用 llava；像素级分割用 segment-anything |
| `blip-2` | BLIP-2（Q-Former）图像描述 captioning、单轮 VQA、图文检索，冻结视觉编码器+LLM | 只需相似度/零样本分类用 clip；多轮指令式看图聊天用 llava |
| `llava` | LLaVA 多轮看图对话、视觉指令微调、VLM 聊天机器人、文档图像理解 | 纯 caption 用 blip-2；检索/分类用 clip |
| `segment-anything` | SAM 用点/框/mask 提示分割任意物体、自动生成全图 mask、交互式标注 | 图像分类/检索用 clip；生成或 inpainting 用 stable-diffusion |

## 生成

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `stable-diffusion` | Stable Diffusion/Diffusers 文生图、图生图、inpainting/outpainting、自定义扩散 pipeline | 音乐/音效生成用 audiocraft；分割 mask 生成用 segment-anything |

## 语音音频

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `whisper` | Whisper 语音转文字 ASR、播客/会议/视频转录、多语种识别与翻译成英文 | 由文本生成音乐或音效用 audiocraft |
| `audiocraft` | AudioCraft MusicGen 文生音乐、AudioGen 文生音效、旋律条件生成、EnCodec 编解码 | 语音识别/转录用 whisper；图像生成用 stable-diffusion |

## 机器人 VLA

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `openpi` 重 | OpenPI pi0/pi0-fast/pi0.5 在 LeRobot 数据上 JAX/PyTorch 微调、checkpoint 转换、policy server 部署，ALOHA/DROID/LIBERO | OpenVLA-OFT 复现/动作头训练用 openvla-oft；Cosmos Policy 仿真评测用 cosmos-policy |
| `openvla-oft` 重 | OpenVLA-OFT/OFT+ 复现论文、LoRA+FiLM、L1/diffusion 连续动作头训练，LIBERO 评测与 ALOHA 部署 | pi0 系列微调/serving 用 openpi；NVIDIA Cosmos Policy 评测用 cosmos-policy |
| `cosmos-policy` 重 | NVIDIA Cosmos Policy 在 LIBERO/RoboCasa 仿真评测、无头 EGL 渲染、集群启动与推理延迟 profiling | 训练/微调 pi0 用 openpi；训练 OpenVLA-OFT 用 openvla-oft |

## 可解释性

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `transformer-lens` | TransformerLens HookPoint 与 activation cache、注意力模式、电路分析、GPT 类小模型 activation patching | 训练/分析 SAE 特征用 saelens；70B+ 远程或任意架构用 nnsight；声明式因果干预/IIT 用 pyvene |
| `saelens` | SAELens 训练与分析稀疏自编码器 SAE、特征发现、superposition/单语义特征研究 | 一般 hook/电路分析用 transformer-lens；因果干预实验用 pyvene |
| `nnsight` | nnsight 读写任意 PyTorch 模型内部激活，NDIF remote=True 远程跑 70B+ 大模型可解释性实验 | GPT 小模型电路分析用 transformer-lens；声明式干预配置/IIT 训练用 pyvene |
| `pyvene` | pyvene 声明式（dict 配置）因果干预、ROME 式 causal tracing、interchange intervention training | 快速 hook 探查/注意力分析用 transformer-lens；远程超大模型用 nnsight；SAE 用 saelens |
