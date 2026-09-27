#!/bin/bash
# Main orchestrator for arXiv daily digest

set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKSPACE_DIR="$(dirname "$SCRIPT_DIR")"
DATA_DIR="$WORKSPACE_DIR/data"
TODAY=$(date +%Y%m%d)

echo "🔬 arXiv Daily Digest - $(date)"
echo "======================================"
echo

# Step 1: Fetch papers from arXiv
echo "📥 Step 1: Fetching papers from arXiv..."
PAPERS_FILE="$DATA_DIR/papers_${TODAY}.json"

if [ -f "$PAPERS_FILE" ]; then
    echo "   ℹ️  Using cached papers from $PAPERS_FILE"
    PAPERS=$(cat "$PAPERS_FILE")
else
    PAPERS=$(python3 "$SCRIPT_DIR/fetch_papers.py")
fi

PAPER_COUNT=$(echo "$PAPERS" | jq '. | length')
echo "   ✅ Found $PAPER_COUNT papers"
echo

# Step 2: Filter and rank papers
echo "🔍 Step 2: Filtering and ranking papers..."
CATEGORIZED=$(echo "$PAPERS" | python3 "$SCRIPT_DIR/filter_papers.py")

TOP_COUNT=$(echo "$CATEGORIZED" | jq '.top_picks | length')
WORTH_COUNT=$(echo "$CATEGORIZED" | jq '.worth_reading | length')
GLANCE_COUNT=$(echo "$CATEGORIZED" | jq '.quick_glance | length')

echo "   ✅ Categorized:"
echo "      🔥 Top picks: $TOP_COUNT"
echo "      📚 Worth reading: $WORTH_COUNT"
echo "      📖 Quick glance: $GLANCE_COUNT"
echo

# Step 3: Generate digest
echo "📝 Step 3: Generating digest..."
DIGEST=$(echo "$CATEGORIZED" | python3 "$SCRIPT_DIR/generate_digest.py")

echo "   ✅ Digest generated"
echo

# Save digest to file
DIGEST_FILE="$DATA_DIR/digests/digest_${TODAY}.md"
mkdir -p "$(dirname "$DIGEST_FILE")"
echo "$DIGEST" > "$DIGEST_FILE"

echo "💾 Digest saved to: $DIGEST_FILE"
echo

# Output digest for delivery
echo "======================================"
echo "$DIGEST"
