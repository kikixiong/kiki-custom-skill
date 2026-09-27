---
name: prompt-clarifier
description: Use when user input has Chinese-English mixing, pinyin typos, front/back nasal confusion (前后鼻音 ing/in eng/en), homophones (同音字 的地得 在再), missing punctuation, run-on sentences, or vague instructions. Rewrites messy input into clear, actionable English.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# Prompt Clarifier

Converts vague, mixed-language prompts into clear, actionable English instructions.

## When to Use

Use this skill when the user's request:
- Mixes Chinese and English ("帮我tidyup这个codebase")
- Uses vague verbs ("完善一下", "优化一下", "注意一下")
- Lacks specific steps or acceptance criteria
- Uses informal/colloquial expressions
- Contains typos or input errors (see Typo Handling below)
- Has no punctuation or sentence breaks (run-on text)
- Contains front/back nasal confusion (前后鼻音, see below)
- Contains homophone errors (同音字, see below)

**Do NOT use** when:
- Request is already clear and specific
- User explicitly wants to use Chinese
- It's a simple question (not a task instruction)

## Typo Handling

Common input errors to recognize and normalize:

### 1. No-Space Mixed Language

Chinese-English without spaces:

| User Input (no space) | Normalized |
|----------------------|------------|
| "帮我tidyup代码" | "帮我 tidyup 代码" |
| "把pipeline优化一下" | "把 pipeline 优化一下" |
| "refactor这个模块" | "refactor 这个模块" |

**Recognition pattern:** Look for Chinese-to-English or English-to-Chinese transitions without spaces.

### 2. Pinyin Typos

Chinese characters typed as pinyin by mistake:

| User Input (typo) | Likely Intent |
|------------------|---------------|
| "zhengli一下代码" | "整理一下代码" (tidyup) |
| "youhua这个函数" | "优化这个函数" (optimize) |
| "wanshan文档" | "完善文档" (improve) |
| "jiancha一下" | "检查一下" (check) |

**Recognition pattern:** Lowercase alphabetic strings that match common Chinese action words in pinyin.

**Common pinyin → Chinese mapping:**
- zhengli → 整理 (organize)
- youhua → 优化 (optimize)
- wanshan → 完善 (improve)
- jiancha → 检查 (check)
- xiugai → 修改 (modify)
- chuli → 处理 (process)

### 3. English Typos

Letter order mistakes or common misspellings:

| User Input (typo) | Likely Intent |
|------------------|---------------|
| "refatcor" | "refactor" |
| "optmize" | "optimize" |
| "anaylze" | "analyze" |
| "tidypu" | "tidyup" |

**Recognition strategy:**
- Check edit distance (Levenshtein) ≤ 2
- Match against common action verbs library
- If unclear, proceed with best guess and mention in response

### 4. Front/Back Nasal Confusion (前后鼻音)

Extremely common in Chinese speakers' input, especially from voice-to-text or fast typing:

| Confused Pair | Examples |
|--------------|----------|
| in ↔ ing | "信xin/星xing", "民min/明ming", "品pin/平ping" |
| en ↔ eng | "分fen/风feng", "真zhen/争zheng", "人ren/仍reng" |
| an ↔ ang | "看kan/康kang", "反fan/方fang", "三san/桑sang" |
| ian ↔ iang | "前qian/强qiang", "连lian/量liang" |
| uan ↔ uang | "关guan/光guang", "换huan/黄huang" |

**Common mistyped words in context:**

| Wrong (nasal error) | Correct | Context Clue |
|---------------------|---------|-------------|
| "运行(xing)" typed as "运信(xin)" | 运行 | followed by code/program |
| "性(xing)能" typed as "信(xin)能" | 性能 | talking about performance |
| "模型(xing)" typed as "模信(xin)" | 模型 | ML context |
| "影(ying)响" typed as "因(yin)响" | 影响 | talking about impact |
| "功能(neng)" typed as "功嫩(nen)" | 功能 | talking about features |
| "训练(lian)" typed as "训脸(lian)" | 训练 | ML training context |
| "环(huan)境" typed as "黄(huang)境" | 环境 | talking about environment |

**Recognition strategy:** Use surrounding context (ML, code, research) to disambiguate. When a character doesn't make semantic sense but its nasal-swapped counterpart does, auto-correct silently.

### 5. Homophone Errors (同音字)

Characters that sound identical but have different meanings. Very common in fast Chinese typing:

| Wrong | Correct | Rule |
|-------|---------|------|
| 的/地/得 | 的(noun modifier), 地(adverb marker), 得(complement marker) | "跑的快"→"跑得快", "慢慢的走"→"慢慢地走" |
| 在/再 | 在(at/is doing), 再(again/then) | "在试一次"→"再试一次", "再这里"→"在这里" |
| 做/作 | 做(do/make), 作(compose/regard as) | "做为"→"作为", "作事"→"做事" |
| 以/已 | 以(with/by), 已(already) | "以经"→"已经", "已后"→"以后" |
| 那/哪 | 那(that), 哪(which/where) | "那里？"→"哪里？" (questions) |
| 它/他/她 | 它(it), 他(he), 她(she) | Use context for correct pronoun |

**Handling:** These errors don't affect comprehension for the model. Silently interpret the correct meaning based on context. Do NOT correct the user or point these out — just understand the intent.

### 6. Run-on Sentences (无标点断句)

Chinese input often lacks punctuation entirely. Parse by semantic boundaries:

**Example:**
```
Input:  "然后帮我写一个skill可以吗就是有时候我输入会有拼音错误同音或者前后鼻音错误之类的以及有时候没有断句或者中英文夹杂的"
Parse:  "然后帮我写一个skill可以吗？就是有时候我输入会有拼音错误、同音或者前后鼻音错误之类的，以及有时候没有断句，或者中英文夹杂的。"
Intent: "Can you write a skill for me? Sometimes my input has pinyin typos, homophone errors, front/back nasal confusion, missing punctuation, or mixed Chinese-English."
```

**Parsing strategy:**
1. Look for discourse markers as break points: 就是, 然后, 以及, 但是, 所以, 因为, 或者, 还有, 比如
2. Look for question particles: 吗, 呢, 吧
3. Look for topic shifts: new subject or verb phrase
4. Reconstruct with proper punctuation before interpreting

### 7. Hybrid Typos

Combination of multiple error types:

```
"帮我refatcor一下这个代码库的信能youhua一下"
  ↓
1. Normalize spacing: "帮我 refatcor 一下 这个 代码库 的 信能 youhua 一下"
2. Fix English typo: refatcor → refactor
3. Fix nasal confusion: 信能 → 性能 (xin→xing)
4. Fix pinyin: youhua → 优化
5. Add punctuation: "帮我 refactor 一下这个代码库的性能，优化一下。"
6. English: "Refactor and optimize the codebase performance."
```

### Handling Strategy

When encountering typos:

1. **Auto-correct silently** if confidence is high (>90%)
   - Common typos in established patterns
   - Single character transposition
   - Known pinyin mappings

2. **Acknowledge correction** if confidence is medium (70-90%)
   - "I'll [action] (interpreting 'refatcor' as 'refactor')..."

3. **Ask for clarification** if confidence is low (<70%)
   - "Did you mean 'refactor' or something else?"

**Default approach:** Be generous with interpretation, but mention uncertainty when present.

## Transformation Framework

### Step 1: Identify Core Intent

Map vague expressions to specific actions:

| Vague Expression | Core Intent |
|-----------------|-------------|
| tidyup / 整理 | Organize, refactor, clean up |
| 完善 | Improve, enhance, add missing parts |
| 优化 | Optimize, make more efficient |
| 注意 | Check for, verify, ensure |
| 修一下 | Fix, repair, correct |
| 看看 | Review, analyze, investigate |
| 搞一下 | Work on, handle, process |

### Step 2: Expand to Concrete Steps

Transform single vague verb into **specific, actionable steps**:

**Template:**
```
[Action verb] [target]: [step 1], [step 2], [step 3], and [acceptance criteria].
```

**Examples:**

| Vague Input | Clear Output |
|------------|--------------|
| "帮我tidyup一下这个codebase" | "Clean up and refactor the codebase: organize imports, remove unused code, fix formatting inconsistencies, improve code structure, and ensure all files follow project conventions." |
| "把这个pipeline的注释完善一下" | "Improve comments in the pipeline code: add docstrings to all functions, explain complex logic blocks, document parameter types and return values, and ensure code intent is clear for maintainers." |
| "注意一下论文的typo和broken references" | "Review the paper for errors: fix spelling and grammar mistakes, verify all citations are valid and properly formatted, check that all references in bibliography are actually cited in text, and remove any fake or placeholder references." |
| "优化一下这个模型的训练速度" | "Optimize model training speed: profile current bottlenecks, implement data loading improvements (e.g., multi-worker DataLoader), use mixed precision training if applicable, and benchmark speed improvements." |

### Step 3: Preserve Context

Keep contextual references intact:
- "这个codebase" → "the codebase" / "this codebase"
- "这个pipeline" → "the pipeline" / "this pipeline"
- "论文" → "the paper"
- "模型" → "the model"

### Step 4: Add Scope and Constraints

If the original prompt implies constraints, make them explicit:

| Original | Add Constraints |
|----------|----------------|
| "改一下代码" | "Refactor the code **without changing external API**" |
| "优化性能" | "Optimize performance **while maintaining accuracy**" |
| "完善文档" | "Improve documentation **following the existing style guide**" |

## Common Domains

### Code/Development

**Vague patterns:**
- "整理代码", "重构一下", "cleanup codebase"

**Clarified patterns:**
- Organize imports and remove unused ones
- Fix code formatting and linting issues
- Remove dead/commented-out code
- Improve variable/function naming
- Extract repeated logic into functions
- Add type hints (Python) or JSDoc (JS)

### Documentation/Papers

**Vague patterns:**
- "完善文档", "改改论文", "fix the paper"

**Clarified patterns:**
- Fix typos and grammar errors
- Verify citations and references
- Improve section transitions
- Add missing explanations
- Ensure consistent terminology
- Check formatting and style

### Data/Analysis

**Vague patterns:**
- "处理一下数据", "看看这个结果", "analyze this"

**Clarified patterns:**
- Load and inspect data structure
- Check for missing/invalid values
- Generate summary statistics
- Visualize key distributions
- Identify outliers or anomalies
- Document findings

## Usage Workflow

When you receive a vague prompt:

1. **Acknowledge** the request
2. **Clarify** using this framework
3. **Confirm** with user:
   - "I understand you want to: [clarified instruction]. Is this correct?"
   - OR directly proceed if confidence is high
4. **Execute** the clarified instruction

**Example interaction:**

**User:** "帮我tidyup一下这个codebase里面的代码"

**You:** 
```
I'll clean up and refactor the codebase:
- Organize imports and remove unused ones
- Fix code formatting issues
- Remove dead code
- Improve code structure and naming

Starting now...
```

## Tips

- **Be specific but not verbose**: Include key steps, but don't write an essay
- **Action-oriented**: Use imperative verbs (Fix, Verify, Improve, Ensure)
- **Measurable**: Include what "done" looks like
- **Preserve user's target**: Don't assume broader scope than implied

## Edge Cases

**When NOT to clarify:**

```
# Already clear
"Refactor the authentication module to use JWT tokens instead of sessions"
→ No clarification needed, execute directly

# User preference for Chinese
"用中文解释一下这个算法"
→ Respond in Chinese, don't translate to English

# Simple question
"这个代码是干什么的？"
→ Answer directly, no clarification needed
```

**When to ask for more info:**

```
# Ambiguous target
"优化一下" (optimize what?)
→ Ask: "Which part would you like me to optimize?"

# Conflicting constraints
"既要快又要准确" (need both speed and accuracy)
→ Clarify priority: "Should I prioritize speed or accuracy?"
```

## Advanced: Detailed Typo Handling

For comprehensive typo patterns and fuzzy matching strategies, see:
- **[references/typo-patterns.md](references/typo-patterns.md)** - Extensive typo library including:
  - Pinyin-to-Chinese mappings (zhengli, youhua, etc.)
  - English fuzzy matching (refatcor→refactor)
  - Confidence level guidelines
  - Hybrid error correction examples

Load this reference when encountering unusual typos or when you need detailed correction strategies.
