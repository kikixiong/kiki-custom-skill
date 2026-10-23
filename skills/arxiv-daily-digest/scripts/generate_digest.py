#!/usr/bin/env python3
"""
Generate markdown digest from categorized papers.
"""

import json
import sys
from datetime import datetime
from pathlib import Path
from local_config import CONFIG_DIR, DATA_DIR, load_json
from collections import Counter

SCRIPT_DIR = Path(__file__).parent


def load_settings():
    """Load digest settings"""
    return load_json("digest_settings.json")


def format_paper_full(item):
    """Format paper with full details (for top picks)"""
    paper = item["paper"]
    
    # Format authors (first 3 + et al.)
    authors = paper["authors"]
    if len(authors) <= 3:
        author_str = ", ".join(authors)
    else:
        author_str = ", ".join(authors[:3]) + " et al."
    
    # Format matched interests
    interests_str = " | ".join(item["matched_interests"])
    
    # Format matched keywords
    keywords_str = []
    for interest, kws in item["matched_keywords"].items():
        keywords_str.append(f"**{interest}**: {', '.join(kws[:3])}")
    keywords_detail = "\n  ".join(keywords_str)
    
    return f"""### 📄 {paper['title']}
- **Authors**: {author_str}
- **arXiv**: [{paper.get('arxiv_id', paper.get('id', 'unknown'))}](https://arxiv.org/abs/{paper.get('arxiv_id', paper.get('id', 'unknown'))}) | [PDF](https://arxiv.org/pdf/{paper.get('arxiv_id', paper.get('id', 'unknown'))}.pdf)
- **Categories**: {', '.join(paper['categories'])}
- **Relevance**: {interests_str} (Score: {item['score']})
- **Matched Keywords**: 
  {keywords_detail}
- **Abstract**: {paper['abstract'][:400]}{'...' if len(paper['abstract']) > 400 else ''}

---
"""


def format_paper_brief(item):
    """Format paper with brief details (for worth reading)"""
    paper = item["paper"]
    
    # Format authors (first author + et al.)
    author_str = paper["authors"][0] + (" et al." if len(paper["authors"]) > 1 else "")
    
    interests_str = " | ".join(item["matched_interests"])
    
    return f"""### {paper['title']}
- **Authors**: {author_str}
- **arXiv**: [{paper.get('arxiv_id', paper.get('id', 'unknown'))}](https://arxiv.org/abs/{paper.get('arxiv_id', paper.get('id', 'unknown'))})
- **Relevance**: {interests_str}
- **Abstract**: {paper['abstract'][:250]}{'...' if len(paper['abstract']) > 250 else ''}

"""


def format_paper_minimal(item):
    """Format paper with minimal details (for quick glance)"""
    paper = item["paper"]
    interests_str = " | ".join(item["matched_interests"])
    return f"- **[{paper['title']}](https://arxiv.org/abs/{paper.get('arxiv_id', paper.get('id', 'unknown'))})** - {interests_str}\n"


def generate_stats(categorized):
    """Generate statistics about the digest"""
    # Count papers by interest area
    interest_counts = Counter()
    
    for category in ["top_picks", "worth_reading", "quick_glance"]:
        for item in categorized[category]:
            for interest in item["matched_interests"]:
                interest_counts[interest] += 1
    
    return interest_counts


def generate_digest(categorized, settings):
    """Generate complete markdown digest"""
    date_str = datetime.now().strftime("%Y-%m-%d")
    relevant_count = sum(
        len(categorized[category])
        for category in ["top_picks", "worth_reading", "quick_glance"]
    )
    scanned_count = categorized.get("_meta", {}).get("scanned_count", relevant_count)
    
    # Get limits from settings
    limits = settings["delivery"]["max_papers"]
    
    # Truncate categories if needed
    top_picks = categorized["top_picks"][:limits["top_picks"]]
    worth_reading = categorized["worth_reading"][:limits["worth_reading"]]
    quick_glance = categorized["quick_glance"][:limits["quick_glance"]]
    
    # Generate stats
    stats = generate_stats(categorized)
    
    # Build digest
    digest = f"""# 🔬 arXiv Daily Digest - {date_str}

> Your personalized research paper summary

"""
    
    # Top Picks section
    if top_picks:
        digest += f"""## 🔥 Top Picks ({len(top_picks)} papers)
*High relevance to your research interests*

"""
        for item in top_picks:
            digest += format_paper_full(item)
    
    # Worth Reading section
    if worth_reading:
        digest += f"""## 📚 Worth Reading ({len(worth_reading)} papers)
*Moderately relevant to your interests*

"""
        for item in worth_reading:
            digest += format_paper_brief(item)
        digest += "\n---\n\n"
    
    # Quick Glance section
    if quick_glance:
        digest += f"""## 📖 Quick Glance ({len(quick_glance)} papers)
*Tangentially related*

"""
        for item in quick_glance:
            digest += format_paper_minimal(item)
        digest += "\n---\n\n"
    
    # Statistics section
    digest += f"""## 📊 Category Breakdown

"""
    for interest, count in stats.most_common():
        digest += f"- **{interest}**: {count} paper(s)\n"
    
    digest += f"""
---

**Total papers scanned**: {scanned_count}  
**Relevant papers matched**: {relevant_count}  
**Generated**: {datetime.now().strftime("%Y-%m-%d %H:%M %Z")}  
**Powered by**: arXiv Daily Digest 🤖
"""
    
    return digest


def main():
    """Generate digest from categorized papers"""
    # Read categorized papers
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            categorized = json.load(f)
    else:
        categorized = json.load(sys.stdin)
    
    settings = load_settings()
    
    # Generate digest
    digest = generate_digest(categorized, settings)
    
    # Output
    print(digest)
    
    # Save to file if configured
    if settings["storage"]["save_digest"]:
        output_dir = DATA_DIR / settings["storage"]["save_path"]
        output_dir.mkdir(parents=True, exist_ok=True)
        output_file = output_dir / f"digest_{datetime.now().strftime('%Y%m%d')}.md"
        
        with open(output_file, "w") as f:
            f.write(digest)
        
        print(f"\n[Digest saved to {output_file}]", file=sys.stderr)


if __name__ == "__main__":
    main()
