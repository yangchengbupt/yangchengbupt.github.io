from scholarly import scholarly, ProxyGenerator
import jsonpickle
import json
from datetime import datetime
import os
import time
import random
import shutil
from pathlib import Path
import argparse
from typing import Optional, Dict


def init_proxy():
    pg = ProxyGenerator()
    try:
        # Free proxies are unreliable but better than hitting rate limits immediately
        if not pg.FreeProxies():
            print("[warn] No free proxies acquired; proceeding without proxies.")
        scholarly.use_proxy(pg)
    except Exception as e:
        print(f"[warn] Failed to initialize proxies: {e}")


def fetch_author(author_id: str, max_retries: int = 5, base_delay: float = 2.0) -> Optional[Dict]:
    """Fetch full author (including publications) like legacy main, with retries."""
    init_proxy()
    for attempt in range(1, max_retries + 1):
        try:
            author: dict = scholarly.search_author_id(author_id)
            scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
            if not author or 'name' not in author or 'publications' not in author:
                raise RuntimeError("Unexpected response while fetching author data")
            return author
        except Exception as e:
            wait = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1.0)
            print(f"[warn] Attempt {attempt}/{max_retries} failed: {e}. Retrying in {wait:.1f}s...")
            time.sleep(wait)
            init_proxy()
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True)
    args = parser.parse_args()

    author_id = os.environ.get('GOOGLE_SCHOLAR_ID')
    if not author_id:
        print('[error] Missing env GOOGLE_SCHOLAR_ID; skip crawling to avoid failure.')
        return 0

    author = fetch_author(author_id)

    # On failure, keep previous data if available to avoid breaking the workflow
    year = args.year
    results_dir = Path(__file__).resolve().parents[1] / 'results'
    results_dir.mkdir(parents=True, exist_ok=True)
    year_json = results_dir / f'gs_data_{year}.json'

    if author is None:
        print('[warn] Failed to fetch from Google Scholar (likely blocked or CAPTCHA).')
        # If year-specific exists, keep it
        if year_json.exists():
            print(f'[info] Found existing {year_json}; keeping it.')
            return 0
        # Else fallback to generic results/gs_data.json if present
        # Try repo results first, then cwd variants as extra safety
        generic = results_dir / 'gs_data.json'
        if not generic.exists():
            alt = Path('results') / 'gs_data.json'
            if alt.exists():
                generic = alt
        if generic.exists():
            try:
                shutil.copyfile(generic, year_json)
                print(f'[info] Copied {generic} to {year_json} for downstream steps.')
            except Exception as e:
                print(f"[warn] Failed to copy fallback data: {e}")
            return 0
        # Minimal stub
        minimal = {"name": "unknown", "citedby": 0, "updated": str(datetime.now()), "publications": {}}
        with open(year_json, 'w', encoding='utf-8') as f:
            json.dump(minimal, f, ensure_ascii=False)
        print(f'[info] Wrote minimal stub {year_json}.')
        return 0

    # Robust filtering without per-publication fill (which is rate-limited on CI)
    pubs = author.get('publications', [])
    total = len(pubs)
    pubs_filtered = []
    for pub in pubs:
        bib = pub.get('bib', {})
        py = str(bib.get('pub_year') or '')
        if py == str(year):
            # Ensure essential keys exist to unblock downstream steps
            if 'num_citations' not in pub:
                pub['num_citations'] = pub.get('num_citations', 0)
            pubs_filtered.append(pub)
    print(f"[info] Publications total={total}, year={year} matched={len(pubs_filtered)}")

    # Normalize and persist (year-specific)
    data = {
        'container_type': 'Author',
        'filled': ['basics', 'publications', 'indices', 'counts'],
        'scholar_id': author_id,
        'name': author.get('name'),
        'affiliation': author.get('affiliation'),
        'interests': author.get('interests'),
        'citedby': author.get('citedby', 0),
        'updated': str(datetime.now()),
        'publications': {v['author_pub_id']: v for v in pubs_filtered},
    }

    print(json.dumps(data, indent=2))

    with open(year_json, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
