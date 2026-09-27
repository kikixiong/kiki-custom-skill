# Common Vague Patterns & Clarifications

This reference provides extensive examples for the most common vague prompt patterns.

## Code & Development

### 1. Cleanup/Tidyup

**Vague:**
- "帮我tidyup一下这个repo"
- "cleanup the codebase"
- "整理一下项目代码"

**Clarified:**
```
Clean up and organize the codebase:
- Remove unused imports and dead code
- Fix linting and formatting issues (run formatter)
- Organize files into logical directories
- Rename poorly-named variables/functions
- Remove commented-out code blocks
- Ensure consistent code style across files
```

### 2. Refactor

**Vague:**
- "重构一下这个模块"
- "refactor this file"

**Clarified:**
```
Refactor the module to improve maintainability:
- Extract repeated logic into reusable functions
- Simplify complex conditionals
- Break down large functions (>50 lines)
- Improve error handling
- Add docstrings and type hints
- Ensure single responsibility principle
```

### 3. Fix

**Vague:**
- "修一下这个bug"
- "改改这个函数"
- "fix this issue"

**Clarified:**
```
Debug and fix the issue:
- Reproduce the error
- Identify root cause
- Implement fix with minimal code changes
- Add test case to prevent regression
- Verify fix doesn't break existing functionality
```

### 4. Optimize

**Vague:**
- "优化一下性能"
- "optimize this code"
- "提升一下速度"

**Clarified:**
```
Optimize performance:
- Profile code to identify bottlenecks
- Improve algorithmic complexity where possible
- Cache expensive computations
- Use vectorized operations (numpy/pandas)
- Parallelize independent tasks
- Benchmark before/after improvements
```

### 5. Add Tests

**Vague:**
- "加点测试"
- "补充一下test cases"

**Clarified:**
```
Add comprehensive test coverage:
- Write unit tests for core functions
- Add integration tests for workflows
- Test edge cases and error conditions
- Ensure at least 80% code coverage
- Add docstrings explaining what each test validates
```

## Documentation & Papers

### 1. Improve

**Vague:**
- "完善一下README"
- "improve the documentation"
- "把文档写好一点"

**Clarified:**
```
Improve documentation:
- Add missing sections (installation, usage, examples)
- Fix broken links and outdated info
- Add code examples for key features
- Improve clarity and organization
- Add troubleshooting section
- Ensure consistent formatting
```

### 2. Review

**Vague:**
- "看看论文有没有问题"
- "review the paper"
- "检查一下文档"

**Clarified:**
```
Review the paper thoroughly:
- Check for typos and grammar errors
- Verify all citations are properly formatted
- Ensure figures are referenced in text
- Check that all references in bibliography are cited
- Verify equations are numbered consistently
- Ensure section flow and transitions are smooth
```

### 3. Fix References

**Vague:**
- "修一下论文的references"
- "check citations"
- "注意broken references"

**Clarified:**
```
Fix citation and reference issues:
- Remove fake or placeholder citations
- Verify all DOIs/URLs are valid and accessible
- Ensure all in-text citations have bibliography entries
- Remove uncited references from bibliography
- Check citation format consistency (APA/IEEE/etc.)
- Fix broken cross-references (sections, figures, tables)
```

### 4. Add Comments

**Vague:**
- "把注释补一下"
- "add some comments"
- "代码注释太少了"

**Clarified:**
```
Improve code comments:
- Add docstrings to all public functions/classes
- Document parameter types and return values
- Explain non-obvious logic or algorithms
- Add inline comments for complex code blocks
- Document any assumptions or constraints
- Keep comments up-to-date with code changes
```

## Data & Analysis

### 1. Process

**Vague:**
- "处理一下这个数据"
- "process the dataset"
- "把数据弄一下"

**Clarified:**
```
Process and clean the dataset:
- Load data and inspect structure
- Handle missing values (drop/impute)
- Remove duplicates
- Fix data type issues
- Normalize/scale numerical features
- Encode categorical variables
- Save cleaned dataset
```

### 2. Analyze

**Vague:**
- "分析一下这个结果"
- "analyze this data"
- "看看数据有什么特点"

**Clarified:**
```
Analyze the dataset:
- Generate summary statistics (mean, median, std)
- Visualize key distributions (histograms, boxplots)
- Check correlations between variables
- Identify outliers or anomalies
- Test statistical hypotheses if applicable
- Document findings and insights
```

### 3. Visualize

**Vague:**
- "可视化一下结果"
- "plot this data"
- "画个图看看"

**Clarified:**
```
Create visualizations:
- Plot distributions of key variables
- Create comparison plots (before/after, groups)
- Add clear labels, titles, and legends
- Use appropriate color schemes
- Save high-resolution figures
- Add captions explaining what to observe
```

## System & Infrastructure

### 1. Setup

**Vague:**
- "搭建一下环境"
- "setup the project"
- "配置一下服务器"

**Clarified:**
```
Set up the development environment:
- Install required dependencies (list versions)
- Configure environment variables
- Set up database/services
- Run initial migrations/setup scripts
- Verify installation with test commands
- Document setup steps in README
```

### 2. Deploy

**Vague:**
- "部署一下这个服务"
- "deploy to production"

**Clarified:**
```
Deploy the service to production:
- Build production-ready artifacts
- Run tests before deployment
- Deploy to staging first for validation
- Update production with zero downtime
- Verify deployment health
- Rollback plan if issues occur
```

### 3. Monitor

**Vague:**
- "监控一下服务"
- "check if it's running"
- "看看有没有问题"

**Clarified:**
```
Monitor service health:
- Check CPU/memory usage
- Review error logs for issues
- Verify API endpoints respond correctly
- Check database connection pool
- Monitor request latency
- Set up alerts for anomalies
```

## Common Chinese-English Hybrid Terms

| Chinese/Hybrid | English Equivalent |
|----------------|-------------------|
| tidyup | organize, clean up |
| refactor | restructure, reorganize |
| 优化 | optimize, improve efficiency |
| 完善 | improve, enhance, complete |
| 修/改 | fix, modify, correct |
| 看看 | review, check, investigate |
| 搞定 | complete, finish, resolve |
| 处理 | process, handle |
| 弄一下 | work on, handle |
| 注意 | check for, ensure, verify |
| 补充 | add, supplement |
| 检查 | check, verify, validate |

## Action Verbs Library

Use these specific action verbs instead of vague ones:

**Creation:**
- Create, Build, Generate, Initialize, Set up

**Modification:**
- Refactor, Reorganize, Restructure, Simplify, Extract

**Quality:**
- Fix, Correct, Repair, Debug, Resolve

**Enhancement:**
- Improve, Optimize, Enhance, Upgrade, Streamline

**Verification:**
- Verify, Validate, Check, Test, Review

**Documentation:**
- Document, Explain, Describe, Annotate, Comment

**Analysis:**
- Analyze, Investigate, Profile, Benchmark, Measure
