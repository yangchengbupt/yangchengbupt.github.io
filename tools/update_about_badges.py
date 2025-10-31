#!/usr/bin/env python3
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ABOUT = ROOT / '_pages' / 'about.md'
GS_JSON = ROOT / 'results' / 'gs_data.json'

def build_id_year_map():
    data = json.loads(GS_JSON.read_text(encoding='utf-8'))
    m = {}
    for pid, info in data.get('publications', {}).items():
        sid = pid.split(':')[-1]
        year = str(info.get('bib', {}).get('pub_year') or '')
        if sid and year:
            m[sid] = year
    return m

def replace_anchor_with_include(text: str, id2year: dict) -> tuple[str, int]:
    # Matches the full <a ...><img ...></a> block targeting scholar + shields
    # Captures the short_id (same id appears twice typically)
    pattern = re.compile(
        r"<a href='https://scholar\.google\.com/citations\?view_op=view_citation&hl=[^']+&user=[^']+&citation_for_view=[^:]+:([A-Za-z0-9_\-]+)'>\s*<img src=\"https://img\.shields\.io/endpoint\?url=[^\"]+selected_pubs%2F\1\.json[^\"]*\"\s*>\s*</a>\.",
        re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        sid = m.group(1)
        year = id2year.get(sid)
        if not year:
            return m.group(0)
        return "{% include gs_badge.html short_id='" + sid + "' year='" + year + "' %}"

    new_text, n = pattern.subn(repl, text)
    return new_text, n

def main():
    if not ABOUT.exists() or not GS_JSON.exists():
        print('about.md or results/gs_data.json missing; abort')
        return 1
    id2year = build_id_year_map()
    original = ABOUT.read_text(encoding='utf-8')
    updated, n = replace_anchor_with_include(original, id2year)

    # Pass 2: inline includes placed on their own line -> move to the best previous line
    lines = updated.splitlines()
    include_re = re.compile(r"^\s*\{\%\s*include\s+gs_badge\.html\s+short_id='[^']+'\s+year='[0-9]{4}'\s*\%\}\s*$")
    source_re = re.compile(r"\[!\[\]\([^)]+source\+code|Source\s+Code|Source\+Code", re.IGNORECASE)
    title_re = re.compile(r"\[[^\]]+\]\(https?://[^)]+\)")  # markdown link line
    skip_re = re.compile(r"^\s*(<!--|<span class=\"conference-badge\")")
    out = []
    for idx, line in enumerate(lines):
        if include_re.match(line):
            # choose attach target within the same block
            i = len(out) - 1
            # step 1: walk back to find best candidate line within this item
            best = None
            j = i
            while j >= 0 and (idx - (j+1)) <= 6:  # look back up to ~6 lines
                cand = out[j]
                if cand.strip() == "" or skip_re.match(cand):
                    j -= 1
                    continue
                if source_re.search(cand):
                    best = j
                    break
                if best is None and title_re.search(cand):
                    best = j
                j -= 1
            if best is None and i >= 0:
                best = i
            if best is not None and best >= 0:
                # remove trailing two-space hard breaks
                out[best] = out[best].rstrip()
                if out[best].endswith("  "):
                    out[best] = out[best].rstrip()
                out[best] = out[best] + " " + line.strip()
            else:
                out.append(line)
            continue
        out.append(line)
    updated2 = "\n".join(out) + ("\n" if updated.endswith("\n") else "")

    ABOUT.write_text(updated2, encoding='utf-8')
    print(f'Replaced {n} scholar badges with Liquid include; inlined standalone includes')
    return 0

if __name__ == '__main__':
    raise SystemExit(main())
