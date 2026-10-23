"""Local configuration and runtime storage for arXiv Daily Digest."""
import argparse
import json
import os
from pathlib import Path

AGENT_HOME = Path("@@KIKI_AGENT_HOME@@")
CONFIG_DIR = Path(os.environ.get("ARXIV_DIGEST_CONFIG_DIR") or
                  AGENT_HOME / "skill-config" / "arxiv-daily-digest").expanduser()
DATA_DIR = Path(os.environ.get("ARXIV_DIGEST_DATA_DIR") or
                AGENT_HOME / "skill-data" / "arxiv-daily-digest").expanduser()


def load_json(name):
    path = CONFIG_DIR / name
    if not path.is_file():
        raise SystemExit(f"Missing digest configuration: {path}. Copy the bundled config templates there and fill in your interests and categories first.")
    try:
        with path.open(encoding="utf-8") as handle:
            config = json.load(handle)
    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON in {path}: {error}") from error
    if not isinstance(config, dict):
        raise SystemExit(f"Configuration must be a JSON object: {path}")
    return config


def check_config():
    categories = load_json("arxiv_categories.json").get("categories", [])
    interests = load_json("research_interests.json").get("interests", [])
    settings = load_json("digest_settings.json")
    if (not isinstance(categories, list) or
            not all(isinstance(item, dict) and isinstance(item.get("id"), str) and
                    item["id"].strip() and isinstance(item.get("check_daily", True), bool)
                    for item in categories) or
            not any(item.get("check_daily", True) for item in categories)):
        raise SystemExit(f"Select at least one arXiv category in {CONFIG_DIR / 'arxiv_categories.json'}.")
    if (not isinstance(interests, list) or not interests or
            not all(isinstance(item, dict) and isinstance(item.get("name"), str) and
                    item["name"].strip() and isinstance(item.get("keywords"), list) and
                    item["keywords"] and all(isinstance(word, str) and word.strip() for word in item["keywords"]) and
                    item.get("priority") in ("high", "medium") for item in interests)):
        raise SystemExit(f"Add each interest's name, keywords and priority to {CONFIG_DIR / 'research_interests.json'}.")
    delivery = settings.get("delivery")
    limits = delivery.get("max_papers") if isinstance(delivery, dict) else None
    storage = settings.get("storage")
    if (not isinstance(limits, dict) or
            not all(type(limits.get(key)) is int and limits[key] >= 0
                    for key in ("top_picks", "worth_reading", "quick_glance")) or
            not isinstance(storage, dict) or not isinstance(storage.get("save_digest"), bool) or
            not isinstance(storage.get("save_path"), str) or not storage["save_path"].strip()):
        raise SystemExit("Configure nonnegative delivery.max_papers limits and storage.save_digest/save_path in digest_settings.json; start from the bundled template.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data-dir", action="store_true", help="Print the configured data directory without fetching papers.")
    args = parser.parse_args()
    if args.data_dir:
        print(DATA_DIR)
    else:
        check_config()
