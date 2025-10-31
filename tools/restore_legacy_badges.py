#!/usr/bin/env python3
"""
Convert inline `{% include gs_badge.html short_id='..' year='YYYY' %}` to the
original hard-coded HTML anchor+image badge, staying on the same line.

It also optionally updates any existing legacy badges to point to the
year-suffixed branch `google-scholar-stats-<YEAR>` using the year derived from
results/gs_data.json. If a short_id -> year mapping is missing, the script
keeps the original text unchanged and reports it.

Usage:
  python3 tools/restore_legacy_badges.py [-n]

Flags:
  -n, --dry-run   Do not write back, only print summary
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
ABOUT = ROOT / '_pages' / 'about.md'
GS_JSON = ROOT / 'results' / 'gs_data.json'

OWNER = 'yangchengbupt'
REPO = 'yangchengbupt.github.io'
SCHOLAR_USER = 'OlLjVUcAAAAJ'


def load_year_map() -> dict[str, str]:
    mp: dict[str, str] = {}
    if not GS_JSON.exists():
        return mp
    data = json.loads(GS_JSON.read_text(encoding='utf-8'))
    for pid, info in data.get('publications', {}).items():
        sid = pid.split(':')[-1]
        year = str(info.get('bib', {}).get('pub_year') or '')
        if sid and year:
            mp[sid] = year
    return mp


def build_badge(short_id: str, year: str) -> str:
    raw = f"https://raw.githubusercontent.com/{OWNER}/{REPO}/google-scholar-stats-{year}/selected_pubs/{short_id}.json"
    json_url = quote(raw, safe='')
    shields = (
        "https://img.shields.io/endpoint?url="
        + json_url
        + "&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"
    )
    scholar_link = (
        "https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user="
        + SCHOLAR_USER
        + "&citation_for_view="
        + SCHOLAR_USER
        + ":"
        + short_id
    )
    return (
        "<a href='"
        + scholar_link
        + "'><img src=\""
        + shields
        + "\"></a>"
    )


def convert(text: str, mp: dict[str, str]) -> tuple[str, int, int]:
    # 1) Replace include tags with legacy badges
    inc_re = re.compile(
        r"\{\%\s*include\s+gs_badge\.html\s+short_id='([^']+)'\s+year='([0-9]{4})'\s*\%\}")
    repl_count = 0

    def inc_repl(m: re.Match) -> str:
        nonlocal repl_count
        sid, year = m.group(1), m.group(2)
        repl_count += 1
        return build_badge(sid, year)

    text2 = inc_re.sub(inc_repl, text)

    # 2) Update existing legacy badges that point to non-year branch
    #    or wrong owner/repo. Use year from map when available.
    #    Capture short_id and optional year.
    leg_re = re.compile(
        r"<a href='https://scholar\.google\.com/citations\?view_op=view_citation&hl=[^']+&user=[^']+&citation_for_view=[^:]+:([A-Za-z0-9_\-]+)'>\s*"
        r"<img src=\"https://img\.shields\.io/endpoint\?url=https%3A%2F%2Fraw\.githubusercontent\.com%2F[^%]+%2F[^%]+%2F(?:google-scholar-stats(?:-([0-9]{4}))?)%2Fselected_pubs%2F\1\.json[^\"]*\"\s*>\s*</a>"
    )
    upd = 0

    def leg_repl(m: re.Match) -> str:
        nonlocal upd
        sid = m.group(1)
        year = m.group(2) or mp.get(sid)
        if not year:
            return m.group(0)
        upd += 1
        return build_badge(sid, year)

    text3 = leg_re.sub(leg_repl, text2)
    return text3, repl_count, upd


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument('-n', '--dry-run', action='store_true')
    args = ap.parse_args()

    if not ABOUT.exists():
        print('about.md not found')
        return 1
    mp = load_year_map()
    src = ABOUT.read_text(encoding='utf-8')
    out, repl, upd = convert(src, mp)
    if out != src and not args.dry_run:
        ABOUT.write_text(out, encoding='utf-8')
    print(f'converted includes: {repl}, updated legacy badges: {upd}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())

