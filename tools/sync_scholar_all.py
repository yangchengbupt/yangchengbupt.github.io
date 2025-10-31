#!/usr/bin/env python3
"""
Sync all papers from Google Scholar into local results/ data, with throttling
and id-based dedup.

What it does:
  - Fetch the author's publications list (no per-paper fill to avoid rate-limit)
  - Build a set of existing short_ids from:
      * results/all_publications.csv (if present)
      * results/all_publications_*.csv (if present)
  - For each publication not present locally:
      * Append to results/all_publications_<year>.csv (create file if missing)
      * Create/overwrite results/selected_pubs/<short_id>.json with citations
  - Optionally update results/gs_data.json by merging missing publications

Usage:
  GOOGLE_SCHOLAR_ID=<id> python3 tools/sync_scholar_all.py [--delay 2.5] [--dry-run]

Notes:
  - No network proxy is configured here; if you want, you can enable it similar
    to google_scholar_crawler/main_by_year.py (ProxyGenerator FreeProxies).
  - This script throttles nothing intensive because we do not per-paper fill.
"""
from __future__ import annotations

import argparse
import csv
import json
import os
import time
from pathlib import Path
from typing import Dict, Iterable, List, Tuple

from scholarly import scholarly, ProxyGenerator


def init_proxy(disable: bool) -> None:
    if disable:
        return
    pg = ProxyGenerator()
    try:
        # Gracefully ignore failures; many environments don't need proxies.
        if not pg.FreeProxies():
            print("[warn] No free proxies acquired; proceeding without proxies.")
        scholarly.use_proxy(pg)
    except Exception as e:
        print(f"[warn] Failed to initialize proxies: {e}")


def fetch_author(author_id: str, *, retries: int = 5, base_delay: float = 2.0, disable_proxy: bool = False) -> Dict:
    import random, time
    init_proxy(disable_proxy)
    last = None
    for attempt in range(1, retries + 1):
        try:
            author: dict = scholarly.search_author_id(author_id)
            # Lighter fill to reduce chance of rate limiting
            scholarly.fill(author, sections=["basics", "publications"])  # omit indices/counts
            if not author or 'publications' not in author:
                raise RuntimeError('Empty author payload')
            return author
        except Exception as e:
            last = e
            wait = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1)
            print(f"[warn] fetch_author attempt {attempt}/{retries} failed: {e}. retry in {wait:.1f}s")
            time.sleep(wait)
            init_proxy(disable_proxy)
    raise last


def load_existing_ids(results_dir: Path) -> set:
    ids = set()
    # main CSV
    main_csv = results_dir / "all_publications.csv"
    if main_csv.exists():
        with open(main_csv, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("short_id"):
                    ids.add(row["short_id"].strip())
    # year CSVs
    for p in results_dir.glob("all_publications_*.csv"):
        with open(p, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                if row.get("short_id"):
                    ids.add(row["short_id"].strip())
    return ids


def append_to_year_csv(results_dir: Path, year: str, rows: List[Dict]) -> None:
    out = results_dir / f"all_publications_{year}.csv"
    is_new = not out.exists()
    with open(out, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f,
            fieldnames=["id", "title", "long_id", "short_id", "pub_year", "citation_message"],
        )
        if is_new:
            writer.writeheader()
        start_idx = sum(1 for _ in open(out, encoding="utf-8")) - 1 if not is_new else 0
        for i, r in enumerate(rows, start=1):
            idx = start_idx + i
            writer.writerow({
                "id": idx,
                "title": r["title"],
                "long_id": r["long_id"],
                "short_id": r["short_id"],
                "pub_year": r["pub_year"],
                "citation_message": r["citation_message"],
            })


def shields_message(repo: str, year: str, sid: str) -> str:
    return (
        f"<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:{sid}'>"
        f"<img src=\"https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2F{repo}%2Fgoogle-scholar-stats-{year}/selected_pubs%2F{sid}.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations\"></a>."
    )


def ensure_selected_pub(results_dir: Path, sid: str, citations: int) -> None:
    sel = results_dir / "selected_pubs" / f"{sid}.json"
    sel.parent.mkdir(parents=True, exist_ok=True)
    data = {"schemaVersion": 1, "label": "citations", "message": f"{citations}"}
    with open(sel, "w", encoding="utf-8") as f:
        json.dump(data, f)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--delay", type=float, default=2.0, help="Delay between lightweight calls (seconds)")
    ap.add_argument("--no-proxy", action="store_true", help="Disable proxy usage even if available")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--repo", default="yangchengbupt/yangchengbupt.github.io")
    args = ap.parse_args()

    author_id = os.environ.get("GOOGLE_SCHOLAR_ID")
    if not author_id:
        print("[error] Missing env GOOGLE_SCHOLAR_ID")
        return 1

    results_dir = Path("results")
    results_dir.mkdir(exist_ok=True)

    author = fetch_author(author_id, disable_proxy=args.no_proxy)
    pubs = author.get("publications", [])
    print(f"[info] fetched publications: {len(pubs)}")

    existing = load_existing_ids(results_dir)
    print(f"[info] existing short_ids: {len(existing)}")

    to_add_by_year: Dict[str, List[Dict]] = {}
    for pub in pubs:
        sid = pub.get("author_pub_id", "").split(":")[-1]
        if not sid or sid in existing:
            continue
        bib = pub.get("bib", {})
        title = bib.get("title") or ""
        year = str(bib.get("pub_year") or "")
        if not year:
            continue
        citations = pub.get("num_citations", 0)
        row = {
            "title": title,
            "long_id": pub.get("author_pub_id"),
            "short_id": sid,
            "pub_year": year,
            "citation_message": shields_message(args.repo, year, sid),
        }
        to_add_by_year.setdefault(year, []).append(row)
        if not args.dry_run:
            ensure_selected_pub(results_dir, sid, citations)
        time.sleep(args.delay)

    total_added = sum(len(v) for v in to_add_by_year.values())
    print(f"[info] new items to add: {total_added}")
    if args.dry_run:
        for y, rows in sorted(to_add_by_year.items()):
            print(f"  {y}: {len(rows)}")
        return 0

    for y, rows in to_add_by_year.items():
        append_to_year_csv(results_dir, y, rows)
        print(f"[write] appended {len(rows)} rows to all_publications_{y}.csv")

    # Merge to results/gs_data.json (optional, lightweight without fill)
    base = results_dir / "gs_data.json"
    if base.exists():
        try:
            data = json.load(open(base, "r", encoding="utf-8"))
        except Exception:
            data = {"publications": {}}
    else:
        data = {"publications": {}}
    for y, rows in to_add_by_year.items():
        for r in rows:
            long_id = r["long_id"]
            sid = r["short_id"]
            if not long_id:
                continue
            if long_id not in data.get("publications", {}):
                data.setdefault("publications", {})[long_id] = {
                    "author_pub_id": long_id,
                    "bib": {"title": r["title"], "pub_year": r["pub_year"]},
                    "num_citations": 0,
                }
    with open(base, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)
    print("[done] gs_data.json updated (merged new placeholders without fill)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
