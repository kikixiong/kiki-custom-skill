# Typo Patterns & Corrections

Common input errors and normalization strategies.

## 1. No-Space Mixed Language Patterns

### Chinese → English Transition

```
帮我refactor代码    →  帮我 refactor 代码
把pipeline优化      →  把 pipeline 优化
检查这个codebase   →  检查这个 codebase
```

### English → Chinese Transition

```
refactor这个模块    →  refactor 这个模块
optimize性能        →  optimize 性能
cleanup代码库       →  cleanup 代码库
```

### Detection Rule

- Scan for transitions: `[Chinese][a-zA-Z]` or `[a-zA-Z][Chinese]` (Unicode ranges)
- Insert space at transition points
- Preserve existing spaces

## 2. Pinyin Typo Mappings

### Common Action Words

| Pinyin | Chinese | English | Frequency |
|--------|---------|---------|-----------|
| zhengli | 整理 | organize, tidy up | Very High |
| youhua | 优化 | optimize | Very High |
| wanshan | 完善 | improve, complete | Very High |
| jiancha | 检查 | check, verify | High |
| xiugai | 修改 | modify, fix | High |
| chuli | 处理 | process, handle | High |
| tianjia | 添加 | add | Medium |
| shanchu | 删除 | delete | Medium |
| gengxin | 更新 | update | Medium |
| ceshi | 测试 | test | Medium |
| fenxi | 分析 | analyze | Medium |
| bushu | 部署 | deploy | Medium |
| jiankong | 监控 | monitor | Low |
| qingchu | 清除 | clear, clean | Low |

### Context Clues

Pinyin typos usually appear:
- At sentence start: "zhengli一下代码"
- After "帮我": "帮我youhua这个"
- Before "一下": "wanshan一下"

### Detection Strategy

```
IF word matches [a-z]+ (lowercase only)
AND word length >= 4
AND appears in common-pinyin-list
AND surrounded by Chinese characters or "一下"
THEN likely pinyin typo
```

## 3. English Typo Patterns

### Common Misspellings

| Typo | Correct | Type | Edit Distance |
|------|---------|------|---------------|
| refatcor | refactor | transposition | 2 |
| refctor | refactor | omission | 1 |
| refacotr | refactor | transposition | 2 |
| optmize | optimize | omission | 1 |
| optimzie | optimize | transposition | 1 |
| anaylze | analyze | transposition | 1 |
| analzye | analyze | transposition | 2 |
| tidypu | tidyup | transposition | 1 |
| tiydp | tidyup | multiple errors | 2 |
| cleaup | cleanup | omission | 1 |
| claenup | cleanup | transposition | 1 |
| procces | process | duplication | 1 |
| prcess | process | omission | 2 |

### Action Verbs Library (for fuzzy matching)

**Code/Development:**
- refactor, optimize, cleanup, tidyup
- debug, fix, modify, update
- test, validate, verify
- build, compile, deploy
- organize, structure, format

**Documentation:**
- improve, enhance, complete
- document, annotate, comment
- review, check, verify
- edit, revise, update

**Data/Analysis:**
- process, analyze, transform
- visualize, plot, chart
- clean, filter, aggregate
- merge, join, split

### Fuzzy Matching Strategy

For unknown words that don't match exactly:

1. Calculate edit distance to all action verbs
2. If min distance ≤ 2, suggest closest match
3. If multiple matches at same distance, use context
4. If distance > 2, treat as unknown word

## 4. Hybrid Error Examples

### Example 1: Multiple Error Types

```
Input:  "帮我refatcor一下这个代码库"
Step 1: Add spaces → "帮我 refatcor 一下 这个 代码库"
Step 2: Fix typo  → "帮我 refactor 一下 这个 代码库"
Step 3: Clarify   → "Refactor the codebase: [detailed steps]"
```

### Example 2: Pinyin + No Space

```
Input:  "youhua这个pipeline的性能"
Step 1: Add spaces → "youhua 这个 pipeline 的 性能"
Step 2: Fix pinyin → "优化 这个 pipeline 的 性能"
Step 3: Clarify    → "Optimize the pipeline performance: [steps]"
```

### Example 3: Multiple English Typos

```
Input:  "帮我cleaup和optmize代码"
Step 1: Add spaces → "帮我 cleaup 和 optmize 代码"
Step 2: Fix typos  → "帮我 cleanup 和 optimize 代码"
Step 3: Clarify    → "Clean up and optimize the code: [steps]"
```

## 5. Confidence Levels

### High Confidence (>90%) - Auto-correct silently

- Edit distance = 1 and unique closest match
- Known pinyin in pinyin-list
- Single space missing at obvious boundary

**Examples:**
- "refctor" → refactor (distance=1, unique)
- "youhua" → 优化 (known pinyin)
- "帮我refactor代码" → add space

### Medium Confidence (70-90%) - Acknowledge correction

- Edit distance = 2 and unique closest match
- Pinyin-like but not in common list
- Context suggests specific interpretation

**Examples:**
- "refatcor" → refactor (distance=2, but context clear)
- "zhenli" → 整理 (close to zhengli)

**Response format:**
```
"I'll refactor the code (interpreting 'refatcor' as 'refactor')..."
```

### Low Confidence (<70%) - Ask for clarification

- Edit distance > 2
- Multiple equally likely matches
- Unknown word with no context clues

**Examples:**
- "rfctr" → ? (distance=3 from refactor)
- "yhoa" → ? (not clear if 优化)

**Response format:**
```
"Did you mean 'refactor', 'restructure', or something else?"
```

## 6. Front/Back Nasal Confusion (前后鼻音)

The most common phonetic error in Chinese input. Speakers from many regions (especially southern China) cannot distinguish these pairs.

### Nasal Pairs

| Final | Confused With | Example Characters |
|-------|--------------|-------------------|
| -in | -ing | 心xin/星xing, 金jin/京jing, 林lin/灵ling, 民min/明ming, 品pin/平ping, 新xin/兴xing |
| -en | -eng | 分fen/风feng, 真zhen/争zheng, 人ren/仍reng, 很hen/横heng, 门men/萌meng |
| -an | -ang | 看kan/康kang, 反fan/方fang, 三san/桑sang, 干gan/刚gang, 半ban/帮bang |
| -ian | -iang | 前qian/强qiang, 连lian/量liang, 天tian/糖tang*, 见jian/江jiang |
| -uan | -uang | 关guan/光guang, 换huan/黄huang, 万wan/王wang* |
| -in | -ing (verb context) | 运信→运行, 模信→模型, 进信→进行, 执信→执行 |

### High-Frequency Errors in Tech/Research Context

| Mistyped | Correct | Pinyin Error | Context |
|----------|---------|-------------|---------|
| 模信 | 模型(moxing) | xin→xing | ML model |
| 运信 | 运行(yunxing) | xin→xing | run/execute |
| 性(xing)能 typed 信能 | 性能 | xin→xing | performance |
| 训连 | 训练(xunlian) | lian→lian (tone) | training |
| 影因 | 影响(yingxiang) | yin→ying | impact |
| 环(huan)境 typed 黄境 | 环境 | huan→huang | environment |
| 功嫩 | 功能(gongneng) | nen→neng | function/feature |
| 引情 | 引擎(yinqing) | qin→qing | engine |
| 进成 | 进程(jincheng) | chen→cheng | process |

### Detection Strategy

```
IF character doesn't make semantic sense in context
AND swapping nasal final produces a valid word
AND the valid word fits the domain (code/ML/research)
THEN auto-correct silently (high confidence)
```

## 7. Homophone Errors (同音字)

### Most Common Confusions

| Group | Characters | Correct Usage | Common Error |
|-------|-----------|---------------|-------------|
| de | 的(possessive/adj), 地(adverb), 得(complement) | 跑得快, 慢慢地走, 我的书 | All written as 的 |
| zai | 在(at/doing), 再(again) | 在这里, 再试一次 | 在/再 swapped |
| zuo | 做(do), 作(compose) | 做事, 作为 | 做为→作为 |
| yi | 以(with), 已(already) | 以后, 已经 | 以经→已经, 已后→以后 |
| na | 那(that), 哪(which) | 哪里？那里。 | 那 in questions |
| ta | 他(he), 她(she), 它(it) | pronoun context | wrong gender |
| bi | 必(must), 毕(finish) | 必须, 毕竟 | 必竟→毕竟 |

### Handling

These do NOT affect meaning comprehension. The model should:
1. Silently interpret the correct meaning
2. Never correct the user on these
3. Just understand the intent and proceed

## 8. Run-on Sentences (无标点断句)

### Break Point Markers

| Type | Markers | Action |
|------|---------|--------|
| Conjunction | 然后, 以及, 而且, 并且, 但是, 不过 | Insert comma before |
| Causal | 因为, 所以, 因此 | Insert comma/period before |
| Transition | 就是, 比如, 比如说, 也就是说 | Insert comma/dash before |
| Question | 吗, 呢, 吧 | Insert question mark after |
| Alternative | 或者, 还是 | Insert comma before |
| Addition | 还有, 另外 | Insert comma/period before |
| Sequence | 首先, 然后, 最后, 接着 | Insert period/comma before |

### Example Parsing

```
Input:  "我想跑一下benchmark然后把结果整理一下发给导师就是用那个scbench的数据跑四个embedding然后对比一下"
Parsed: "我想跑一下benchmark，然后把结果整理一下发给导师。就是用那个scbench的数据跑四个embedding，然后对比一下。"
English: "Run the benchmark, compile the results, and send them to my supervisor. Specifically, run four embeddings on the scbench data and compare them."
```

## 9. Implementation Notes

### Preprocessing Pipeline

```
1. Normalize spacing (Chinese-English boundaries)
2. Detect and fix pinyin typos
3. Fuzzy match English words
4. Proceed with clarification
```

### Edge Cases

**DON'T over-correct:**
- Proper nouns: "TidyData" is a package name, not "Tidy Data"
- Code identifiers: "refactorUtil" might be intentional
- Domain terms: "optim" in PyTorch optimizer context

**Context matters:**
- "rm" in "帮我rm这个文件" → keep "rm" (command name)
- "rm" in "帮我rmeove这个文件" → fix to "remove"

### Testing Checklist

- [ ] No-space Chinese-English mixing
- [ ] Common pinyin typos (zhengli, youhua, wanshan)
- [ ] English transpositions (refatcor, optmize)
- [ ] Hybrid errors (multiple types)
- [ ] High/medium/low confidence scenarios
- [ ] Edge cases (proper nouns, code terms)
