#!/usr/bin/env python3
"""
Fetch recent papers from arXiv using arXiv API.
More reliable than browser scraping.
"""

import json
import re
import sys
import time
import urllib.error
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pathlib import Path
from local_config import CONFIG_DIR, DATA_DIR, load_json

SCRIPT_DIR = Path(__file__).parent

ARXIV_API_BASE = "https://export.arxiv.org/api/query"
ARXIV_RSS_BASE = "https://rss.arxiv.org/rss"
REQUEST_INTERVAL_SECONDS = 3.1
MAX_FETCH_ATTEMPTS = 4
RETRYABLE_HTTP_CODES = {429, 500, 502, 503, 504}
_last_request_at = 0.0


def load_categories():
    """Load arXiv categories from config"""
    config = load_json("arxiv_categories.json")
    categories = [cat["id"] for cat in config["categories"] if cat.get("check_daily", True)]
    if not categories:
        raise SystemExit(f"Select arXiv categories in {CONFIG_DIR / 'arxiv_categories.json'} first.")
    return categories


def fetch_category_papers_rss(category):
    """Fetch the latest announced papers from an official arXiv category RSS feed."""
    global _last_request_at

    url = f"{ARXIV_RSS_BASE}/{category}"
    elapsed = time.monotonic() - _last_request_at
    if elapsed < REQUEST_INTERVAL_SECONDS:
        time.sleep(REQUEST_INTERVAL_SECONDS - elapsed)

    try:
        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Codex-arXiv-Daily-Digest/1.0"},
        )
        _last_request_at = time.monotonic()
        with urllib.request.urlopen(request, timeout=30) as response:
            data = response.read()

        root = ET.fromstring(data)
        namespaces = {
            "arxiv": "http://arxiv.org/schemas/atom",
            "dc": "http://purl.org/dc/elements/1.1/",
        }
        papers = []

        for item in root.findall("./channel/item"):
            link = (item.findtext("link") or "").strip()
            arxiv_id = link.rstrip("/").split("/")[-1]
            description = (item.findtext("description") or "").strip()
            announce_type = (
                item.findtext("arxiv:announce_type", default="", namespaces=namespaces)
                or ""
            ).strip().lower()
            if "replace" in announce_type:
                continue
            abstract_marker = "Abstract:"
            abstract = (
                description.split(abstract_marker, 1)[1].strip()
                if abstract_marker in description
                else description
            )
            creator = item.findtext("dc:creator", default="", namespaces=namespaces)
            authors = [author.strip() for author in creator.split(",") if author.strip()]
            categories = [
                element.text.strip()
                for element in item.findall("category")
                if element.text and element.text.strip()
            ]
            announced = (item.findtext("pubDate") or "").strip()

            papers.append({
                "arxiv_id": arxiv_id,
                "title": " ".join((item.findtext("title") or "").split()),
                "authors": authors or ["Unknown"],
                "abstract": " ".join(abstract.split()),
                "categories": categories or [category],
                "published": announced,
                "updated": announced,
                "pdf_link": f"https://arxiv.org/pdf/{arxiv_id}.pdf",
                "primary_category": category,
                "announce_type": announce_type or "unknown",
            })

        return papers
    except Exception as e:
        print(f"Error fetching RSS for {category}: {e}", file=sys.stderr)
        return []


def fetch_category_papers(category, max_results=100):
    """
    Fetch recent papers from a specific arXiv category
    
    Args:
        category: arXiv category ID (e.g., "cs.AI")
        max_results: Maximum number of papers to fetch
    
    Returns:
        List of paper dictionaries
    """
    # Query for papers submitted in last 2 days (to account for timezone differences)
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
    
    global _last_request_at

    for attempt in range(1, MAX_FETCH_ATTEMPTS + 1):
        elapsed = time.monotonic() - _last_request_at
        if elapsed < REQUEST_INTERVAL_SECONDS:
            time.sleep(REQUEST_INTERVAL_SECONDS - elapsed)

        request = urllib.request.Request(
            url,
            headers={"User-Agent": "Codex-arXiv-Daily-Digest/1.0"},
        )

        try:
            _last_request_at = time.monotonic()
            with urllib.request.urlopen(request, timeout=60) as response:
                data = response.read()
            break
        except urllib.error.HTTPError as e:
            if e.code not in RETRYABLE_HTTP_CODES or attempt == MAX_FETCH_ATTEMPTS:
                print(f"Error fetching {category}: {e}", file=sys.stderr)
                return []

            retry_after = e.headers.get("Retry-After")
            delay = float(retry_after) if retry_after and retry_after.isdigit() else 10 * attempt
            print(
                f"HTTP {e.code} fetching {category}; "
                f"retrying in {delay:.0f}s ({attempt}/{MAX_FETCH_ATTEMPTS})...",
                file=sys.stderr,
            )
            time.sleep(delay)
        except Exception as e:
            if attempt == MAX_FETCH_ATTEMPTS:
                print(f"Error fetching {category}: {e}", file=sys.stderr)
                return []

            delay = 10 * attempt
            print(
                f"Error fetching {category}: {e}; "
                f"retrying in {delay}s ({attempt}/{MAX_FETCH_ATTEMPTS})...",
                file=sys.stderr,
            )
            time.sleep(delay)
    else:
        return []

    try:
        # Parse XML
        root = ET.fromstring(data)
        ns = {"atom": "http://www.w3.org/2005/Atom", 
              "arxiv": "http://arxiv.org/schemas/atom"}
        
        papers = []
        for entry in root.findall("atom:entry", ns):
            # Extract arXiv ID
            arxiv_id = entry.find("atom:id", ns).text.split("/abs/")[-1]
            
            # Extract title (clean up whitespace)
            title = " ".join(entry.find("atom:title", ns).text.split())
            
            # Extract authors
            authors = [author.find("atom:name", ns).text 
                      for author in entry.findall("atom:author", ns)]
            
            # Extract abstract (clean up whitespace)
            abstract = " ".join(entry.find("atom:summary", ns).text.split())
            
            # Extract categories
            categories = [cat.attrib["term"] 
                         for cat in entry.findall("atom:category", ns)]
            
            # Extract published date
            published = entry.find("atom:published", ns).text
            
            # Extract updated date (for v2, v3, etc.)
            updated = entry.find("atom:updated", ns).text
            
            # PDF link
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
    """Remove duplicate papers (same arXiv ID)"""
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
    for category in categories:
        print(f"  - {category}...", file=sys.stderr)
        papers = fetch_category_papers_rss(category)
        all_papers.extend(papers)
        print(f"    Found {len(papers)} papers", file=sys.stderr)
    
    # Deduplicate
    all_papers = deduplicate_papers(all_papers)
    
    print(f"\nTotal: {len(all_papers)} unique papers", file=sys.stderr)
    
    # Save to file
    output_file = DATA_DIR / f"papers_{datetime.now().strftime('%Y%m%d')}.json"
    with open(output_file, "w") as f:
        json.dump(all_papers, f, indent=2)
    
    print(f"Saved to {output_file}", file=sys.stderr)
    
    # Also output to stdout for piping
    print(json.dumps(all_papers, indent=2))


if __name__ == "__main__":
    main()
