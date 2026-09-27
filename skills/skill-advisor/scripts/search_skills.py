#!/usr/bin/env python3
"""
Search for similar skills based on a description.
Uses simple keyword matching and scoring.
"""

import json
import sys
import re
from pathlib import Path
from typing import List, Dict, Tuple
from collections import Counter

def load_index() -> Dict:
    """Load the skills index."""
    index_file = Path(__file__).parent.parent / "references" / "skills_index.json"
    
    if not index_file.exists():
        print("❌ Skills index not found. Run index_skills.py first.")
        sys.exit(1)
    
    with open(index_file, 'r', encoding='utf-8') as f:
        return json.load(f)

def tokenize(text: str) -> List[str]:
    """Simple tokenization: lowercase, split on non-alphanumeric."""
    text = text.lower()
    tokens = re.findall(r'\b\w+\b', text)
    # Filter out common stopwords
    stopwords = {'a', 'an', 'the', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
                 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'should',
                 'can', 'could', 'may', 'might', 'must', 'to', 'of', 'in', 'on', 'at',
                 'for', 'with', 'from', 'by', 'as', 'or', 'and', 'but', 'if', 'when',
                 'use', 'using', 'used'}
    return [t for t in tokens if t not in stopwords and len(t) > 2]

def calculate_similarity(query_tokens: List[str], skill: Dict) -> float:
    """Calculate similarity score between query and skill."""
    # Combine name and description
    skill_text = f"{skill.get('name', '')} {skill.get('description', '')}"
    skill_tokens = tokenize(skill_text)
    
    if not skill_tokens:
        return 0.0
    
    # Count matching tokens
    query_counter = Counter(query_tokens)
    skill_counter = Counter(skill_tokens)
    
    # Calculate overlap
    matching_tokens = sum((query_counter & skill_counter).values())
    
    # Normalize by query length (how much of query is covered)
    coverage = matching_tokens / len(query_tokens) if query_tokens else 0
    
    # Boost score if skill name matches
    name_tokens = tokenize(skill.get('name', ''))
    name_match = len(set(query_tokens) & set(name_tokens)) / len(query_tokens) if query_tokens else 0
    
    # Final score: weighted combination
    score = coverage * 0.7 + name_match * 0.3
    
    return score

def search_skills(query: str, top_k: int = 5) -> List[Tuple[float, Dict]]:
    """Search for skills matching the query."""
    index = load_index()
    query_tokens = tokenize(query)
    
    if not query_tokens:
        print("❌ No meaningful tokens in query")
        return []
    
    # Score all skills
    scored_skills = []
    for skill in index['skills']:
        score = calculate_similarity(query_tokens, skill)
        if score > 0:
            scored_skills.append((score, skill))
    
    # Sort by score (descending)
    scored_skills.sort(reverse=True, key=lambda x: x[0])
    
    return scored_skills[:top_k]

def format_results(results: List[Tuple[float, Dict]]) -> str:
    """Format search results as markdown."""
    if not results:
        return "No similar skills found."
    
    output = []
    output.append(f"Found {len(results)} similar skill(s):\n")
    
    for i, (score, skill) in enumerate(results, 1):
        name = skill.get('name', 'Unknown')
        desc = skill.get('description', 'No description')
        path = skill.get('_dir', '')
        
        output.append(f"**{i}. {name}** (similarity: {score:.2%})")
        output.append(f"   📝 {desc}")
        output.append(f"   📁 {path}")
        output.append("")
    
    return '\n'.join(output)

def main():
    if len(sys.argv) < 2:
        print("Usage: search_skills.py <query>")
        print("Example: search_skills.py 'document processing pdf editing'")
        sys.exit(1)
    
    query = ' '.join(sys.argv[1:])
    print(f"🔍 Searching for: {query}\n")
    
    results = search_skills(query, top_k=8)
    print(format_results(results))
    
    if results and results[0][0] > 0.4:
        print("💡 Tip: Consider using/extending existing skill instead of creating a new one.")
    elif results:
        print("💡 Tip: Some similar skills exist, but your use case might be different enough to warrant a new skill.")
    else:
        print("✅ No similar skills found - this looks like a unique use case!")

if __name__ == "__main__":
    main()
