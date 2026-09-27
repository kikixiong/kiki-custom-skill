#!/usr/bin/env python3
"""Build, search and read a page-grounded personal paper library; no model calls."""
import argparse
from collections import Counter
import json
import math
import os
from pathlib import Path
import re
import unicodedata
from html.parser import HTMLParser

SKILL = Path(__file__).resolve().parents[1]
KINDS = ("abstract", "introduction", "related_work", "method", "experiments", "discussion", "caption")
STOP = set("a an the of to and or in on for with by from as is are be that this we our it at into using model models paper papers".split())
ALIASES = {
    "对比": "contrastive", "互补": "complementary disjoint", "视图": "views panels",
    "细胞": "cell", "表示": "representation embeddings", "重建": "reconstruction",
    "基因": "gene", "扰动": "perturbation", "泛化": "generalization transfer",
    "批次": "batch", "采样": "sampling", "注释": "annotation", "消融": "ablation",
    "负样本": "negative negatives", "正样本": "positive positives", "预训练": "pretraining",
    "零样本": "zero shot", "跨物种": "cross species", "噪声": "noise",
    "因果": "causal", "调控": "regulatory", "效率": "efficiency memory runtime",
}


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def identity(path):
    stat = path.stat()
    return {"bytes": stat.st_size, "mtime_ns": stat.st_mtime_ns}


def tokens(text):
    text = unicodedata.normalize("NFKC", text).lower()
    words = re.findall(r"[a-z][a-z0-9]*", text)
    return [w for w in words if w not in STOP and len(w) > 1]


def html_units(path):
    """Keep HTML headings/anchors as units instead of inventing PDF page numbers."""
    class Sections(HTMLParser):
        def __init__(self):
            super().__init__()
            self.units, self.parents, self.buffer = [], [], []
            self.heading, self.anchor, self.skip = "Preamble", "", 0

        def flush(self):
            text = " ".join(" ".join(self.buffer).split())
            if text:
                self.units.append({"heading": self.heading, "anchor": self.anchor, "text": text})
            self.buffer = []

        def handle_starttag(self, tag, attrs):
            attrs = dict(attrs)
            if tag in ("script", "style"):
                self.skip += 1
            if tag in ("section", "figure"):
                self.parents.append(attrs.get("id", ""))
            if re.fullmatch(r"h[1-6]", tag):
                self.flush()
                self.anchor = attrs.get("id") or next((x for x in reversed(self.parents) if x), "")

        def handle_endtag(self, tag):
            if tag in ("script", "style"):
                self.skip = max(0, self.skip - 1)
            if tag in ("section", "figure") and self.parents:
                self.parents.pop()
            if re.fullmatch(r"h[1-6]", tag):
                self.heading = " ".join(" ".join(self.buffer).split())
                self.buffer = [self.heading]

        def handle_data(self, data):
            if not self.skip:
                self.buffer.append(data)

    parser = Sections()
    parser.feed(path.read_text(encoding="utf-8"))
    parser.flush()
    return parser.units


def source_path(root, paper):
    return (root / (paper.get("html") or paper["pdf"])).resolve()


def build(root):
    from pypdf import PdfReader
    manifest = read_json(root / "manifest.json")
    chunks, states, page_data = [], {}, {}
    ids = set()
    for paper in manifest["papers"]:
        pid = paper["id"]
        if pid in ids:
            raise ValueError(f"Duplicate paper ID: {pid}")
        ids.add(pid)
        source = source_path(root, paper)
        if paper.get("html"):
            units = html_units(source)
            pages = [u["text"] for u in units]
        else:
            if not source.read_bytes()[:5] == b"%PDF-":
                raise ValueError(f"Not a PDF: {source}")
            reader = PdfReader(source)
            pages = [page.extract_text() or "" for page in reader.pages]
            units = [{"text": t, "heading": f"PDF page {i + 1}", "anchor": ""} for i, t in enumerate(pages)]
        if len(pages) != paper["page_count"]:
            raise ValueError(f"Page count changed for {pid}; inspect version before indexing")
        states[pid] = identity(source)
        page_data[pid] = units
        for section in paper["sections"]:
            start, end = section["pages"]
            if section["kind"] not in KINDS or not 1 <= start <= end <= len(pages):
                raise ValueError(f"Invalid section for {pid}: {section}")
            for number in range(start, end + 1):
                # Preserve the raw page separately. Join line-end word breaks for search.
                selected = pages[number - 1]
                trim = section.get("trim", {}).get(str(number), {})
                if "start_at" in trim:
                    selected = selected[selected.index(trim["start_at"]):]
                if "end_before" in trim:
                    selected = selected[:selected.index(trim["end_before"])]
                cleaned = re.sub(r"([A-Za-z])-\s*\n\s*([a-z])", r"\1\2", selected)
                cleaned = re.sub(r"(?m)^\s*\d{1,3}\s*$", "", cleaned)
                words = cleaned.split()
                if len(words) < 12:
                    raise ValueError(f"Unreadable indexed page: {pid} p.{number}; inspect/OCR first")
                for offset in range(0, len(words), 180):
                    text = " ".join(words[offset:offset + 240])
                    chunks.append({"paper": pid, "kind": section["kind"],
                                   "heading": section["heading"], "page": number,
                                   "anchor": units[number - 1]["anchor"],
                                   "tags": section.get("tags", ""), "text": text})
    # All source validation precedes writes, preventing a partial source import.
    for pid, pages in page_data.items():
        write_json(root / "index/pages" / f"{pid}.json", pages)
    dest = root / "index/chunks.jsonl"
    dest.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")
    write_json(root / "index/state.json", {"manifest": identity(root / "manifest.json"), "pdfs": states})
    print(json.dumps({"papers": len(page_data), "source_units": sum(map(len, page_data.values())),
                      "chunks": len(chunks), "index": str(dest)}, ensure_ascii=False))


def load(root):
    manifest = read_json(root / "manifest.json")
    state = read_json(root / "index/state.json")
    if state["manifest"] != identity(root / "manifest.json"):
        raise ValueError("Manifest changed. Inspect source versions and run build.")
    papers = {p["id"]: p for p in manifest["papers"]}
    for pid, paper in papers.items():
        if identity(source_path(root, paper)) != state["pdfs"].get(pid):
            raise ValueError(f"Source changed: {pid}. Inspect version and run build.")
    return papers


def search(root, args):
    papers = load(root)
    if args.paper and args.paper not in papers:
        raise ValueError(f"Unknown paper ID: {args.paper}")
    query = args.query
    for phrase, expansion in ALIASES.items():
        if phrase in query:
            query += " " + expansion
    terms = set(tokens(query))
    if not terms:
        raise ValueError("No searchable terms. Use English scientific keywords or supported Chinese terms.")
    chunks = [json.loads(line) for line in (root / "index/chunks.jsonl").read_text(encoding="utf-8").splitlines()]
    chunks = [c for c in chunks if
              (not args.section or c["kind"] == args.section) and
              (not args.paper or c["paper"] == args.paper) and
              (args.include_project or papers[c["paper"]]["role"] != "project")]
    counters = [Counter(tokens(c["text"])) for c in chunks]
    df = Counter(term for counts in counters for term in counts)
    n = len(chunks)
    avg = sum(sum(c.values()) for c in counters) / max(n, 1)
    ranked = []
    for chunk, counts in zip(chunks, counters):
        length = sum(counts.values())
        score = 0.0
        matched = terms & counts.keys()
        meta = set(tokens(chunk["tags"] + " " + chunk["heading"] + " " + papers[chunk["paper"]]["tags"]))
        # Metadata helps recall but cannot fabricate relevance for a completely unmatched query.
        if not matched and not terms & meta:
            continue
        for term in matched:
            freq = counts[term]
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * freq * 2.2 / (freq + 1.2 * (0.25 + 0.75 * length / max(avg, 1)))
        score += 0.65 * len(terms & meta)
        score += 1.3 * len(terms & set(tokens(chunk["heading"])))
        ranked.append((score, chunk))
    ranked.sort(key=lambda pair: (-pair[0], pair[1]["paper"], pair[1]["page"]))
    results, seen = [], set()
    for score, chunk in ranked:
        pid = chunk["paper"]
        if pid in seen:
            continue
        seen.add(pid)
        paper = papers[pid]
        words = chunk["text"].split()
        hits = [i for i, w in enumerate(words) if set(tokens(w)) & terms]
        start = max(0, (hits[0] if hits else 0) - 18)
        results.append({"paper": pid, "title": paper["title"], "role": paper["role"],
                        "version": paper["version"], "publication_status": paper["publication_status"],
                        "section": chunk["heading"], "kind": chunk["kind"],
                        "pdf_page": None if paper.get("html") else chunk["page"],
                        "html_unit": chunk["page"] if paper.get("html") else None,
                        "html_anchor": chunk["anchor"] or None,
                        "locator_granularity": "HTML heading unit" if paper.get("html") else "curated page window",
                        "local_source": str(source_path(root, paper)), "source": paper["source_url"],
                        "score": round(score, 4), "excerpt": " ".join(words[start:start + 100]),
                        "read_command": f"python3 {Path(__file__).resolve()} --library '{root}' read {pid} --units {chunk['page']}"})
        if len(results) == args.top:
            break
    print(json.dumps({"query": args.query, "expanded_query": query, "results": results,
                      "notice": "Read source pages before writing. Excerpts are source text, not reusable draft prose."}, ensure_ascii=False, indent=2))


def read_pages(root, args):
    papers = load(root)
    if args.paper not in papers:
        raise ValueError(f"Unknown paper ID: {args.paper}")
    pages = read_json(root / "index/pages" / f"{args.paper}.json")
    parts = args.pages.split(":")
    start = int(parts[0])
    end = int(parts[-1])
    if len(parts) > 2 or not 1 <= start <= end <= len(pages):
        raise ValueError(f"Invalid source units; expected 1 through {len(pages)}")
    print(papers[args.paper]["title"] + "\n" + papers[args.paper]["version"])
    for number in range(start, end + 1):
        unit = pages[number - 1]
        kind = "HTML section" if papers[args.paper].get("html") else "PDF page"
        print(f"\n--- {kind} {number}: {unit['heading']} #{unit['anchor']} ---\n{unit['text']}")


def main():
    config = read_json(SKILL / "references/library.json")
    parser = argparse.ArgumentParser(description=__doc__)
    library_root = os.environ.get("KIKI_SCFM_LIBRARY") or config.get("root")
    parser.add_argument("--library", type=Path, default=Path(library_root).expanduser() if library_root else None)
    commands = parser.add_subparsers(dest="command", required=True)
    commands.add_parser("build")
    query = commands.add_parser("search")
    query.add_argument("query")
    query.add_argument("--section", choices=KINDS)
    query.add_argument("--paper")
    query.add_argument("--top", type=int, default=3)
    query.add_argument("--include-project", action="store_true")
    reader = commands.add_parser("read")
    reader.add_argument("paper")
    reader.add_argument("--pages", "--units", dest="pages", required=True)
    args = parser.parse_args()
    if args.library is None:
        parser.error("Set KIKI_SCFM_LIBRARY or pass --library /actual/library/path; the paper library is not bundled.")
    args.library = args.library.expanduser()
    if args.command == "search" and not 1 <= args.top <= 20:
        parser.error("--top must be between 1 and 20")
    try:
        if args.command == "build":
            build(args.library)
        elif args.command == "search":
            search(args.library, args)
        else:
            read_pages(args.library, args)
    except (OSError, ValueError, ImportError) as error:
        parser.exit(2, f"Library error: {error}\n")


if __name__ == "__main__":
    main()
