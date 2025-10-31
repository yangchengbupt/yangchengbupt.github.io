#!/usr/bin/env python3
"""
Normalize publication years to Google Scholar's year and fix citation_message
branch targets accordingly. This ensures cases like AgentVerse (arXiv 2023,
Scholar 2024) use Scholar's year in CSVs and badges.

Actions:
  - For each results/all_publications_*.csv and results/all_publications.csv:
      * If row has a short_id, look up Scholar year from results/gs_data.json.
      * When mismatch or unset, set pub_year to Scholar year and rewrite
        citation_message to google-scholar-stats-<ScholarYear> branch.
  - Optionally emit an enriched arxiv_results_enriched.csv with matched
    gs_year and short_id by fuzzy (normalized) title match (best-effort).

Usage:
  python3 tools/fix_years_by_scholar.py [--enrich-arxiv]
"""
from __future__ import annotations

import argparse
import csv
import json
import re
from pathlib import Path

REPO = 'yangchengbupt/yangchengbupt.github.io'


def load_gs_years(gs_path: Path) -> tuple[dict[str, str], dict[str, str]]:
    """Return (short_id -> year, normalized_title -> year) maps."""
    data = json.loads(gs_path.read_text(encoding='utf-8'))
    id2year: dict[str, str] = {}
    title2year: dict[str, str] = {}
    for pid, info in data.get('publications', {}).items():
        sid = pid.split(':')[-1]
        year = str(info.get('bib', {}).get('pub_year') or '')
        title = str(info.get('bib', {}).get('title') or '')
        if sid and year:
            id2year[sid] = year
        if title and year:
            title2year[norm(title)] = year
    return id2year, title2year


def norm(s: str) -> str:
    s = s.lower()
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"[^a-z0-9\s]", "", s)
    return s


def shields(repo: str, year: str, sid: str) -> str:
    return (
        f"<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:{sid}'>"
        f"<img src=\"https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2F{repo}%2Fgoogle-scholar-stats-{year}/selected_pubs%2F{sid}.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations\"></a>."
    )


def fix_csv(p: Path, id2year: dict[str, str]) -> int:
    rows = list(csv.DictReader(p.read_text(encoding='utf-8').splitlines()))
    changed = 0
    for r in rows:
        sid = (r.get('short_id') or '').strip()
        if not sid:
            continue
        y = id2year.get(sid)
        if not y:
            continue
        if r.get('pub_year') != y or f'google-scholar-stats-{y}' not in (r.get('citation_message') or ''):
            r['pub_year'] = y
            r['citation_message'] = shields(REPO, y, sid)
            changed += 1
    if changed:
        with open(p, 'w', newline='', encoding='utf-8') as f:
            w = csv.DictWriter(f, fieldnames=['id','title','long_id','short_id','pub_year','citation_message'])
            w.writeheader()
            for r in rows:
                w.writerow(r)
    return changed


def enrich_arxiv(arxiv_csv: Path, title2year: dict[str, str]) -> int:
    out = arxiv_csv.with_name('arxiv_results_enriched.csv')
    rows = list(csv.DictReader(arxiv_csv.read_text(encoding='utf-8').splitlines()))
    for r in rows:
        t = norm(r.get('title') or '')
        r['gs_year'] = title2year.get(t, '')
    with open(out, 'w', newline='', encoding='utf-8') as f:
        fieldnames = list(rows[0].keys()) + ([] if 'gs_year' in rows[0] else ['gs_year'])
        w = csv.DictWriter(f, fieldnames=fieldnames)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    return len(rows)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--enrich-arxiv', action='store_true')
    args = ap.parse_args()

    res = Path('results')
    gs_path = res / 'gs_data.json'
    if not gs_path.exists():
        print('[error] results/gs_data.json not found')
        return 1
    id2year, title2year = load_gs_years(gs_path)

    changed = 0
    # Fix per-year CSVs
    for p in sorted(res.glob('all_publications_*.csv')):
        changed += fix_csv(p, id2year)
    # Fix main CSV if exists
    p0 = res / 'all_publications.csv'
    if p0.exists():
        changed += fix_csv(p0, id2year)
    print(f'[done] normalized CSVs; rows updated: {changed}')

    if args.enrich_arxiv:
        a = res / 'arxiv_results.csv'
        if a.exists():
            n = enrich_arxiv(a, title2year)
            print(f'[done] wrote arxiv_results_enriched.csv with {n} rows')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

