#!/usr/bin/env python3
"""
Filter and rank papers based on research interests.
"""

import json
import re
import sys
from pathlib import Path
from collections import defaultdict

SCRIPT_DIR = Path(__file__).parent
CONFIG_DIR = SCRIPT_DIR.parent / "config"


def load_interests():
    """Load research interests from config"""
    with open(CONFIG_DIR / "research_interests.json") as f:
        return json.load(f)["interests"]


def calculate_relevance(paper, interests):
    """
    Calculate relevance score for a paper
    
    Returns:
        tuple: (score, matched_interests, matched_keywords)
    """
    text = f"{paper['title']} {paper['abstract']}"
    
    matched_interests = []
    matched_keywords = defaultdict(list)
    
    for interest in interests:
        interest_matches = []
        for keyword in interest["keywords"]:
            pattern = rf"(?<![A-Za-z0-9]){re.escape(keyword)}(?![A-Za-z0-9])"
            if re.search(pattern, text, flags=re.IGNORECASE):
                interest_matches.append(keyword)
        
        if interest_matches:
            matched_interests.append(interest["name"])
            matched_keywords[interest["name"]] = interest_matches
    
    # Calculate score
    # High priority interests get 2x weight
    score = 0
    for interest in interests:
        if interest["name"] in matched_interests:
            base_score = len(matched_keywords[interest["name"]])
            if interest["priority"] == "high":
                score += base_score * 2
            else:
                score += base_score
    
    return score, matched_interests, dict(matched_keywords)


def rank_papers(papers, interests):
    """
    Rank papers by relevance
    
    Returns:
        List of (paper, score, matched_interests, matched_keywords) tuples
    """
    ranked = []
    
    for paper in papers:
        score, matched_interests, matched_keywords = calculate_relevance(paper, interests)
        
        if score > 0:  # Only include papers with at least one match
            ranked.append({
                "paper": paper,
                "score": score,
                "matched_interests": matched_interests,
                "matched_keywords": matched_keywords
            })
    
    # Sort by score (descending)
    ranked.sort(key=lambda x: x["score"], reverse=True)
    
    return ranked


def categorize_papers(ranked_papers):
    """
    Categorize papers into top_picks, worth_reading, quick_glance
    """
    categories = {
        "top_picks": [],
        "worth_reading": [],
        "quick_glance": []
    }
    
    for item in ranked_papers:
        score = item["score"]
        num_interests = len(item["matched_interests"])
        
        # Top picks: High score OR multiple interest areas matched
        if score >= 4 or num_interests >= 2:
            categories["top_picks"].append(item)
        # Worth reading: Medium score
        elif score >= 2:
            categories["worth_reading"].append(item)
        # Quick glance: Low score but still relevant
        else:
            categories["quick_glance"].append(item)
    
    return categories


def main():
    """Filter and rank papers from stdin or file"""
    # Read papers
    if len(sys.argv) > 1:
        with open(sys.argv[1]) as f:
            papers = json.load(f)
    else:
        papers = json.load(sys.stdin)
    
    interests = load_interests()
    
    print(f"Filtering {len(papers)} papers...", file=sys.stderr)
    
    # Rank papers
    ranked = rank_papers(papers, interests)
    
    print(f"Found {len(ranked)} relevant papers", file=sys.stderr)
    
    # Categorize
    categorized = categorize_papers(ranked)
    categorized["_meta"] = {"scanned_count": len(papers)}
    
    print(f"  Top picks: {len(categorized['top_picks'])}", file=sys.stderr)
    print(f"  Worth reading: {len(categorized['worth_reading'])}", file=sys.stderr)
    print(f"  Quick glance: {len(categorized['quick_glance'])}", file=sys.stderr)
    
    # Output categorized results
    print(json.dumps(categorized, indent=2))


if __name__ == "__main__":
    main()
