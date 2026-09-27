---
name: arxiv-daily-digest
description: Automatically fetch, filter, rank, and summarize arXiv papers based on the user's configured research interests. Use when the user wants daily arXiv paper updates, personalized paper recommendations, research interest configuration, or scheduled research digests.
---

## Kiki runtime configuration

Read [the installed runtime profile](@@KIKI_SUPPORT_DIR@@/compatibility.md).
Use the current client's available tools and this machine's paths. A copied
skill does not provide account authorization, GPU allocation or missing tools.

# arXiv Daily Digest

Automated research paper monitoring system that:
- Fetches new papers from arXiv daily
- Filters by your research interests
- Ranks papers by relevance
- Generates personalized digest
- Delivers via Telegram at scheduled time

## Quick Start

### 1. Test Manual Run

```bash
cd @@KIKI_SKILLS_DIR@@/arxiv-daily-digest
./scripts/run_digest.sh
```

This will:
1. Fetch today's papers from arXiv
2. Filter by research interests
3. Generate digest markdown
4. Save to `data/digests/digest_YYYYMMDD.md`

### 2. Configure Research Interests

Edit `config/research_interests.json`:

```json
{
  "interests": [
    {
      "id": "your_topic",
      "name": "Display Name",
      "keywords": ["keyword1", "keyword2", ...],
      "priority": "high"  // or "medium"
    }
  ]
}
```

**Current interests**:
- Single Cell & Biology AI
- Tabular ML
- Agent Systems
- Graph Learning
- Sports AI

### 3. Set Up Daily Cron Job

Use Codex automations to schedule the daily digest:

```bash
# The automation will run the digest and report the result in Codex
# Time: 09:00 GMT+8 (01:00 GMT) daily
```

See [Cron Setup](#cron-setup) section below for exact configuration.

## Configuration

### Research Interests (`config/research_interests.json`)

Define your research areas and keywords:

- **id**: Unique identifier
- **name**: Display name in digest
- **keywords**: List of keywords to match (case-insensitive)
- **priority**: "high" (2x weight) or "medium"

**Tip**: Add synonyms and common abbreviations to keywords for better matching.

### arXiv Categories (`config/arxiv_categories.json`)

Select which arXiv categories to monitor:

- `cs.AI` - Artificial Intelligence
- `cs.LG` - Machine Learning
- `cs.MA` - Multiagent Systems
- `q-bio.GN` - Genomics
- `q-bio.MN` - Molecular Networks
- `stat.ML` - Machine Learning (Statistics)
- `cs.NE` - Neural and Evolutionary Computing

Set `check_daily: true` for categories you want to monitor.

### Digest Settings (`config/digest_settings.json`)

Control digest generation and delivery:

```json
{
  "delivery": {
    "max_papers": {
      "top_picks": 5,      // Maximum top-priority papers
      "worth_reading": 10,  // Maximum medium-priority papers
      "quick_glance": 15    // Maximum low-priority papers
    }
  },
  "storage": {
    "save_digest": true,
    "save_path": "data/digests/",
    "retention_days": 30
  }
}
```

## How It Works

### 1. Paper Fetching

Uses arXiv API to fetch papers from configured categories submitted in the last 2 days.

**Script**: `scripts/fetch_papers.py`

For each paper, extracts:
- Title, authors, abstract
- arXiv ID and categories
- Publication/update dates
- PDF link

### 2. Filtering & Ranking

Matches papers against research interest keywords.

**Script**: `scripts/filter_papers.py`

**Scoring**:
- Each keyword match: +1 point
- High-priority interest match: 2x multiplier
- Papers are categorized by score:
  - **Top picks**: Score ≥4 OR ≥2 interest areas matched
  - **Worth reading**: Score ≥2
  - **Quick glance**: Score ≥1

### 3. Digest Generation

Formats papers into markdown digest.

**Script**: `scripts/generate_digest.py`

**Sections**:
- 🔥 **Top Picks**: Full details (title, authors, abstract, matched keywords)
- 📚 **Worth Reading**: Brief summaries
- 📖 **Quick Glance**: Title + link only
- 📊 **Category Breakdown**: Paper counts by interest area

## Cron Setup

### Create Codex Automation

This runs the digest in a standalone Codex automation and reports the generated markdown:

```bash
# Ask Codex to create a daily automation for the following task:
```

Run arXiv daily digest:
cd @@KIKI_SKILLS_DIR@@/arxiv-daily-digest && ./scripts/run_digest.sh
Return the generated digest summary and saved digest path.
```

**Schedule**: Daily at 01:00 UTC (09:00 GMT+8)

**What it does**:
1. Runs digest generation script
2. Captures the markdown output
3. Reports the digest or saved path in Codex

### Manual Trigger

To trigger immediately (for testing):

```bash
cd @@KIKI_SKILLS_DIR@@/arxiv-daily-digest
./scripts/run_digest.sh
```

## Output

### Digest Format

```markdown
# 🔬 arXiv Daily Digest - 2026-03-18

> Your personalized research paper summary

## 🔥 Top Picks (3 papers)
*High relevance to your research interests*

### 📄 [Paper Title]
- **Authors**: Author 1, Author 2 et al.
- **arXiv**: [2603.12345](https://arxiv.org/abs/2603.12345) | [PDF](...)
- **Categories**: cs.LG, cs.AI
- **Relevance**: Single Cell & Biology AI | Tabular ML (Score: 8)
- **Matched Keywords**: 
  **Single Cell & Biology AI**: foundation model, gene expression
  **Tabular ML**: tabular, foundation model
- **Abstract**: [First 400 chars...]

---

## 📚 Worth Reading (5 papers)
...

## 📖 Quick Glance (10 papers)
...

## 📊 Category Breakdown
- Single Cell & Biology AI: 5 paper(s)
- Graph Learning: 3 paper(s)
- Agent Systems: 2 paper(s)

---
Generated: 2026-03-18 09:00 GMT+8
```

### Storage

Digests are saved to:
```
data/digests/digest_YYYYMMDD.md
```

Raw papers are cached in:
```
data/papers_YYYYMMDD.json
```

## Customization

### Add New Research Interest

1. Edit `config/research_interests.json`
2. Add new interest object with keywords
3. Re-run digest to see results

### Change Delivery Time

1. Update the Codex automation schedule
2. Example for 08:00 GMT+8 (00:00 UTC):
   ```json
   "expr": "0 0 * * *"
   ```

### Increase Paper Limit

Edit `config/digest_settings.json`:
```json
"max_papers": {
  "top_picks": 10,      // Increase from 5
  "worth_reading": 20,   // Increase from 10
  "quick_glance": 30     // Increase from 15
}
```

## Troubleshooting

### No Papers Found

- Check if arXiv API is accessible
- Verify category IDs in config are correct
- Try expanding date range in `fetch_papers.py`

### No Relevant Papers

- Review keyword list in research interests
- Add more synonyms and variations
- Lower priority threshold in `filter_papers.py`

### Delivery Failed

- Check Telegram connection
- Verify the Codex automation destination and output settings
- Check digest file in `data/digests/`

## Manual Components

### Fetch Papers Only

```bash
python3 scripts/fetch_papers.py > papers.json
```

### Filter Papers

```bash
cat papers.json | python3 scripts/filter_papers.py > filtered.json
```

### Generate Digest

```bash
cat filtered.json | python3 scripts/generate_digest.py > digest.md
```

## Dependencies

- **python3**: Core scripting
- **jq**: JSON processing in bash
- **urllib**: HTTP requests (built-in)
- **xml.etree**: XML parsing (built-in)

## Future Enhancements

- [ ] LLM-powered paper summaries
- [ ] Weekly digest with trend analysis
- [ ] Citation tracking
- [ ] PDF download for top papers
- [ ] Multi-language support
- [ ] Web UI for configuration

## Notes

- arXiv updates daily at ~20:00 EST
- Papers are fetched for last 2 days to account for timezone differences
- Duplicate papers (cross-listed) are automatically removed
- API calls are respectful (no aggressive scraping)

## References

- [arXiv API Documentation](https://arxiv.org/help/api/index)
- [arXiv Category Taxonomy](https://arxiv.org/category_taxonomy)

---

**Skill created**: 2026-03-18  
**Origin**: Migrated from OpenClaw and adapted for Codex
