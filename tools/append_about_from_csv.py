#!/usr/bin/env python3
"""
Append missing papers for a given year into _pages/about.md without changing
existing hand-written content. It scans the year section and appends new list
items for any papers present in results/all_publications_<year>.csv but missing
from that section (matched by short_id).

Each appended item contains:
  - Title linking to its Google Scholar citation page
  - The citation badge that points to google-scholar-stats-<year>

Usage:
  python3 tools/append_about_from_csv.py --year 2022 [--dry-run]
"""
from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ABOUT = Path('_pages/about.md')


def load_csv(year: int) -> list[dict]:
    p = Path('results') / f'all_publications_{year}.csv'
    rows: list[dict] = []
    with open(p, newline='', encoding='utf-8') as f:
        for row in csv.DictReader(f):
            rows.append(row)
    return rows


def extract_year_block(text: str, year: int) -> tuple[int, int]:
    hdr = f'## ⌛️ {year}'
    start = text.find(hdr)
    if start < 0:
        # create new block at end
        return len(text), len(text)
    # find next "## ⌛️ " header
    idx = text.find('## ⌛️ ', start + len(hdr))
    if idx < 0:
        idx = len(text)
    return start, idx


def short_ids_in_block(block: str) -> set[str]:
    ids = set(re.findall(r"citation_for_view=OlLjVUcAAAAJ:([A-Za-z0-9_\-]+)", block))
    return ids


def compose_item(year: int, title: str, short_id: str) -> str:
    scholar = (
        f"https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:{short_id}"
    )
    badge = (
        f"<a href='{scholar}'><img src=\"https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fyangchengbupt%2Fyangchengbupt.github.io%2Fgoogle-scholar-stats-{year}%2Fselected_pubs%2F{short_id}.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations\"></a>"
    )
    return f"- [{title}]({scholar}) {badge}\n"


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('--year', type=int, required=True)
    ap.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()

    rows = load_csv(args.year)
    text = ABOUT.read_text(encoding='utf-8')
    s, e = extract_year_block(text, args.year)
    block = text[s:e]
    existing = short_ids_in_block(block)

    added = []
    for r in rows:
        sid = r.get('short_id', '').strip()
        if not sid or sid in existing:
            continue
        title = r.get('title', '').strip()
        added.append(compose_item(args.year, title, sid))

    if not added:
        print('[info] no new items to append')
        return 0

    hdr = f'## ⌛️ {args.year}'
    if s == e:  # block not found, append a new one
        inject = '\n' + hdr + '\n\n' + ''.join(added) + '\n'
        new_text = text + inject
    else:
        # append to the end of the block (before next year header)
        # find last non-empty line within block
        prefix = text[:e]
        suffix = text[e:]
        new_block = block.rstrip() + '\n' + ''.join(added) + '\n'
        new_text = text[:s] + new_block + suffix

    if args.dry_run:
        print('[dry-run] would append', len(added), 'items')
        print('--- sample ---')
        print(''.join(added[:3]))
        return 0

    ABOUT.write_text(new_text, encoding='utf-8')
    print(f'[write] appended {len(added)} items to {ABOUT}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

