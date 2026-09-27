# arXiv Daily Digest Workflow

## Daily Execution Flow

```
Cron triggers at 09:00 GMT+8
         ↓
1. Fetch Papers (fetch_papers.py)
   - Query arXiv API for configured categories
   - Filter by submission date (last 2 days)
   - Save raw papers to data/papers_YYYYMMDD.json
         ↓
2. Filter & Rank (filter_papers.py)
   - Load research interests config
   - Match papers against keywords
   - Calculate relevance scores
   - Categorize into top/medium/low priority
         ↓
3. Generate Digest (generate_digest.py)
   - Format papers into markdown
   - Add statistics and breakdown
   - Save to data/digests/digest_YYYYMMDD.md
         ↓
4. Report in Codex
   - Send digest via Telegram
   - Announce completion
```

## Manual Testing

### Full workflow
```bash
cd @@KIKI_SKILLS_DIR@@/arxiv-daily-digest
./scripts/run_digest.sh
```

### Step-by-step

```bash
# 1. Fetch papers
python3 scripts/fetch_papers.py > /tmp/papers.json

# 2. Filter papers
cat /tmp/papers.json | python3 scripts/filter_papers.py > /tmp/filtered.json

# 3. Generate digest
cat /tmp/filtered.json | python3 scripts/generate_digest.py
```

## Customization Points

### 1. Add Research Interest

Edit `config/research_interests.json`:
```json
{
  "id": "new_topic",
  "name": "New Topic",
  "keywords": ["keyword1", "keyword2"],
  "priority": "high"
}
```

### 2. Change Scoring Logic

Edit `filter_papers.py`, function `calculate_relevance()`:
```python
# Current: High priority = 2x weight
# Customize as needed
```

### 3. Adjust Categorization Thresholds

Edit `filter_papers.py`, function `categorize_papers()`:
```python
# Current thresholds:
# - Top picks: score >= 4 OR num_interests >= 2
# - Worth reading: score >= 2
# - Quick glance: score >= 1
```

### 4. Modify Digest Format

Edit `generate_digest.py`, functions:
- `format_paper_full()` - Top picks format
- `format_paper_brief()` - Worth reading format
- `format_paper_minimal()` - Quick glance format

## Troubleshooting

### No papers fetched
- Check network connectivity
- Verify arXiv API is accessible: `curl http://export.arxiv.org/api/query?search_query=cat:cs.AI&max_results=1`
- Check category IDs in config

### No relevant papers
- Review keyword list
- Add more variations and synonyms
- Check if papers match interests manually

### Digest too long for Telegram
- Reduce max_papers limits in settings
- Shorten abstract excerpts in format functions
- Split into multiple messages

### Cron job not running
- Check cron status: use Codex automation tool
- Verify schedule expression
- Check session logs

## File Structure

```
arxiv-daily-digest/
├── SKILL.md                    # This file
├── scripts/
│   ├── run_digest.sh          # Main orchestrator
│   ├── fetch_papers.py        # Step 1: Fetch from arXiv
│   ├── filter_papers.py       # Step 2: Filter & rank
│   └── generate_digest.py     # Step 3: Generate markdown
├── config/
│   ├── research_interests.json  # User interests
│   ├── arxiv_categories.json    # Categories to monitor
│   └── digest_settings.json     # Delivery settings
├── data/
│   ├── papers_YYYYMMDD.json     # Cached papers
│   └── digests/
│       └── digest_YYYYMMDD.md   # Generated digests
└── references/
    ├── arxiv-api.md             # API reference
    └── workflow.md              # This file
```

## Performance

- Paper fetching: ~5-10 seconds per category
- Filtering: <1 second for 100 papers
- Digest generation: <1 second
- **Total**: ~30-60 seconds for full workflow

## Future Improvements

- Cache paper metadata to avoid re-fetching
- Add LLM-powered summaries for top picks
- Implement similarity deduplication (not just exact ID)
- Add citation tracking
- Weekly/monthly aggregated digests
