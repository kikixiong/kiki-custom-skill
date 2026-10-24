---
name: llm-app-router
description: LLM 应用、RAG、Agent 与安全的总入口：LangChain、LlamaIndex、DSPy、多 agent、结构化输出/JSON、向量库、embedding、tracing 评测、guardrails、越狱/注入检测，先用它再按表读取具体 skill
---

# LLM 应用、RAG、Agent 与安全 Router

本分类的叶子 skill 已设为仅显式调用（Claude Code：frontmatter `disable-model-invocation: true`；Codex：`agents/openai.yaml` 中 `policy.allow_implicit_invocation: false`），不在自动列表里。本 skill 是它们的二级目录。

## 用法

1. 按下表选 1 个主 skill（必要时加 1～2 个辅助）；拿不准时看“默认选择”和“不用于”列。
2. 用文件读取工具读取 `@@KIKI_SKILLS_DIR@@/<目录名>/SKILL.md`，按其正文执行。**不要**通过技能调用机制加载叶子（Claude Code 的 Skill 工具会因仅显式调用而失败）。
3. 叶子正文里的相对路径（`references/`、`scripts/`）按该 SKILL.md 所在目录解析；叶子要求“调用某 skill”时同样改为 Read 其 SKILL.md。
4. 正文含 Codex 专有能力（Codex MCP、原生 imagegen、`~/.codex`、automation API）时：在 Codex 中照常使用；在 Claude Code 中换成等价物（Agent 子代理、本地脚本），没有等价物就告诉用户。
5. 用户点名某 skill（Claude Code 输入 `/名字`，Codex 输入 `$名字`）时直接用它。选定后告诉用户“用的是 X”。
6. 请求属于其他分类时改读对应 router：`paper-router`、`research-router`、`experiment-router`、`ml-train-router`、`ml-infer-router`、`ml-domain-router`、`quant-router`、`coding-router`、`meta-router`。

标记：⚠C = 含 Codex 专有用法；重 = 多阶段重型流程，仅在用户明确要求时用。

## 默认选择（没有特殊信号时）

| 请求 | 默认 |
|---|---|
| 搭 LLM 应用、agent、tool calling | `langchain` |
| 对文档或私有数据做 RAG 问答 | `llamaindex` |
| 让 LLM 输出 JSON 或 Pydantic 结构 | `instructor` |
| 选向量数据库、做语义检索 | `chroma` |
| LLM 应用 tracing 与评测 | `langsmith` |
| LLM 输入输出安全过滤 | `nemo-guardrails` |

## 应用框架

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `langchain` | 用 LangChain 搭 chain/ReAct agent、tool calling、memory、RAG，切换 OpenAI/Anthropic 等 provider | 以文档摄取和索引为主的 RAG 用 llamaindex；要自动优化 prompt 用 dspy |
| `llamaindex` | 用 LlamaIndex 做文档摄取（300+ connector）、向量索引、query engine、私有数据问答 | 通用 agent、工具链编排用 langchain；只要向量库存储用 chroma/qdrant |
| `dspy` | 用 DSPy 声明式写 LM 程序，用 optimizer 自动优化 prompt/few-shot，模块化 RAG | 手写 chain/agent 用 langchain；只需约束输出格式用 outlines/instructor |

## Agent

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `crewai` | 用 CrewAI 搭基于角色的多 agent 协作（researcher/writer），按顺序或层级流程执行 | 单 agent 加工具调用用 langchain；可视化、常驻、定时触发的 agent 用 autogpt |
| `autogpt` | 用 AutoGPT 平台做可视化低代码 agent，常驻运行，用 webhook/定时触发 | 用代码编排多角色协作用 crewai；在代码里写 agent 用 langchain |

## 结构化输出

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `guidance` | 用 Microsoft Guidance 以 regex/grammar 约束生成，交错写 Pythonic 多步生成流程 | 用 Pydantic/JSON Schema 在本地模型或 vLLM 上约束生成用 outlines；API 输出抽取加重试用 instructor |
| `outlines` | 用 Outlines 按 JSON Schema/Pydantic 约束解码，跑本地 Transformers、vLLM、llama.cpp | OpenAI/Anthropic API 抽取加校验重试用 instructor；regex 交错式模板用 guidance |
| `instructor` | 用 Instructor 从 OpenAI/Anthropic API 响应中按 Pydantic 抽取结构化数据，自动校验、重试、流式输出部分结果 | 本地模型做 token 级约束解码用 outlines/guidance |

## 向量检索

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `chroma` | 用 Chroma 做本地或自托管的轻量 embedding 库，适合 notebook 原型、带 metadata 过滤的 RAG | 十亿级向量或 GPU 纯 k-NN 用 faiss；托管 serverless 用 pinecone；生产自部署分布式用 qdrant |
| `faiss` | 用 FAISS 做大规模（百万到十亿）稠密向量 k-NN，选 IVF/HNSW 索引、GPU 加速 | 需要 metadata 过滤或数据库功能用 chroma/qdrant；托管服务用 pinecone |
| `pinecone` | 用 Pinecone 托管 serverless 向量库，自动扩缩容、dense+sparse 混合检索、namespace | 自托管或离线环境用 qdrant/chroma；纯本地 ANN 库用 faiss |
| `qdrant` | 用 Qdrant（Rust）做生产级自部署向量库，带 payload 过滤的混合检索、分片副本、多向量 | 快速原型用 chroma；托管服务用 pinecone；无需数据库的纯 ANN 用 faiss |
| `sentence-transformers` | 用 sentence-transformers 生成文本/多语言/图像 embedding，做语义相似度、聚类、RAG 编码 | 存储和检索向量用 chroma/faiss/qdrant/pinecone |

## 可观测性

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `langsmith` | 用 LangSmith 做 LLM 应用 trace、数据集评测、回归测试和线上监控，LangChain 生态首选 | 要开源自托管或用 OpenTelemetry 用 phoenix |
| `phoenix` | 用 Arize Phoenix 做开源自托管 LLM tracing（OpenTelemetry）、评测、prompt/模型对比实验 | 用 LangChain 托管平台、商业 SaaS 用 langsmith |

## 安全护栏

| skill | 用于 | 不用于（改用） |
|---|---|---|
| `llamaguard` | 用 Meta LlamaGuard 7-8B 对输入/输出做内容安全分类（暴力、色情、武器、自残等类别） | 只检测 prompt 注入/越狱用 prompt-guard；可编程多种 rail 用 nemo-guardrails |
| `nemo-guardrails` | 用 NeMo Guardrails 和 Colang 编写运行时护栏：越狱、幻觉/事实核查、PII、毒性检测 | 单独做内容分类模型用 llamaguard；轻量注入检测用 prompt-guard |
| `prompt-guard` | 用 Meta Prompt Guard 86M 轻量检测 prompt injection/jailbreak，过滤 RAG 第三方数据，支持多语言 | 对有害内容分类用 llamaguard；完整运行时护栏框架用 nemo-guardrails |
