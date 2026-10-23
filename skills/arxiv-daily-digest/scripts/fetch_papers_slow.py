#!/usr/bin/env python3
"""
Fetch recent papers from arXiv using arXiv API.
Rate-limited version with delays between requests.
"""

import json
import sys
import time
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from local_config import CONFIG_DIR, DATA_DIR, load_json

SCRIPT_DIR = Path(__file__).parent

ARXIV_API_BASE = "http://export.arxiv.org/api/query"


def load_categories():
    """Load arXiv categories from config"""
    config = load_json("arxiv_categories.json")
    categories = [cat["id"] for cat in config["categories"] if cat.get("check_daily", True)]
    if not categories:
        raise SystemExit(f"Select arXiv categories in {CONFIG_DIR / 'arxiv_categories.json'} first.")
    return categories


def fetch_category_papers(category, max_results=100):
    """
    Fetch recent papers from a specific arXiv category
    """
    start_date = (datetime.now() - timedelta(days=2)).strftime("%Y%m%d%H%M%S")
    end_date = datetime.now().strftime("%Y%m%d%H%M%S")
    
    query = f"cat:{category} AND submittedDate:[{start_date} TO {end_date}]"
    
    params = {
        "search_query": query,
        "start": 0,
        "max_results": max_results,
        "sortBy": "submittedDate",
        "sortOrder": "descending"
    }
    
    url = f"{ARXIV_API_BASE}?{urllib.parse.urlencode(params)}"
    
    try:
        req = urllib.request.Request(
            url,
            headers={
                'User-Agent': 'Mozilla/5.0 (compatible; arXiv-digest-bot/1.0; mail@example.com)'
            }
        )
        with urllib.request.urlopen(req, timeout=60) as response:
            data = response.read()
        
        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom", 
              "arxiv": "http://arxiv.org/schemas/atom"}
        
        papers = []
        for entry in root.findall("atom:entry", ns):
            arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
            title = " ".join(entry.find("atom:title", ns).text.split())
            authors = [author.find("atom:name", ns).text 
                      for author in entry.findall("atom:author", ns)]
            abstract = " ".join(entry.find("atom:summary", ns).text.split())
            categories = [cat.attrib["term"] 
                         for cat in entry.findall("atom:category", ns)]
            published = entry.find("atom:published", ns).text
            updated = entry.find("atom:updated", ns).text
            pdf_link = f"https://arxiv.org/pdf/{arxiv_id}.pdf"
            
            papers.append({
                "arxiv_id": arxiv_id,
                "title": title,
                "authors": authors,
                "abstract": abstract,
                "categories": categories,
                "published": published,
                "updated": updated,
                "pdf_link": pdf_link,
                "primary_category": category
            })
        
        return papers
    
    except Exception as e:
        print(f"Error fetching {category}: {e}", file=sys.stderr)
        return []


def deduplicate_papers(papers):
    """Remove duplicate papers"""
    seen = set()
    unique = []
    for paper in papers:
        if paper["arxiv_id"] not in seen:
            seen.add(paper["arxiv_id"])
            unique.append(paper)
    return unique


def main():
    """Fetch papers from all configured categories"""
    categories = load_categories()
    
    print(f"Fetching papers from {len(categories)} categories...", file=sys.stderr)
    
    all_papers = []
    for i, category in enumerate(categories):
        if i > 0:
            time.sleep(3)  # Wait 3 seconds between requests
        print(f"  - {category}...", file=sys.stderr)
        papers = fetch_category_papers(category)
        all_papers.extend(papers)
        print(f"    Found {len(papers)} papers", file=sys.stderr)
    
    all_papers = deduplicate_papers(all_papers)
    
    print(f"\nTotal: {len(all_papers)} unique papers", file=sys.stderr)
    
    output_file = DATA_DIR / f"papers_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, "w") as f:
        json.dump(all_papers, f, indent=2)
    
    print(f"Saved to {output_file}", file=sys.stderr)
    print(json.dumps(all_papers, indent=2))


if __name__ == "__main__":
    main()
