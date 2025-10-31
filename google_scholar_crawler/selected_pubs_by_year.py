import csv
import json
import os
from pathlib import Path
import argparse
from typing import List, Optional, Tuple


def read_long_ids_for_year(csv_path: str, year: str) -> List[str]:
    long_ids: List[str] = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('pub_year') == str(year):
                long_ids.append(row.get('long_id', ''))
    return [i for i in long_ids if i]


def find_citations_by_long_id(data: dict, target_long_id: str) -> Tuple[Optional[int], Optional[str]]:
    for paper_id, paper_info in data.get('publications', {}).items():
        if paper_info.get('author_pub_id') == target_long_id:
            return paper_info.get('num_citations'), paper_id
    return None, None


def run_for_year(year: int, csv_path: Optional[str] = None, src_json: Optional[str] = None) -> None:
    results_dir = Path('results')
    sel_dir = results_dir / 'selected_pubs'
    sel_dir.mkdir(parents=True, exist_ok=True)

    # inputs
    csv_file = Path(csv_path) if csv_path else (results_dir / 'all_publications.csv')
    # Prefer year-specific json if present, otherwise fallback to generic
    if src_json:
        gs_path = Path(src_json)
    else:
        year_json = results_dir / f'gs_data_{year}.json'
        gs_path = year_json if year_json.exists() else (results_dir / 'gs_data.json')

    if not csv_file.exists() or not gs_path.exists():
        print(f"[warn] prerequisites missing: {csv_file} or {gs_path} not found; skip {year}")
        return

    long_ids = read_long_ids_for_year(str(csv_file), str(year))
    data = json.load(open(gs_path, 'r'))

    # If CSV is empty or missing rows (only header), derive long_ids from json directly
    if not long_ids:
        pubs = data.get('publications', {})
        for pid, pinfo in pubs.items():
            bib = pinfo.get('bib', {})
            if str(bib.get('pub_year') or '') == str(year):
                long_id = pinfo.get('author_pub_id') or pid
                if long_id:
                    long_ids.append(long_id)

    saved = 0
    for long_id in long_ids:
        citations, paper_id = find_citations_by_long_id(data, long_id)
        if paper_id is None:
            continue
        paper_id = paper_id.split(':')[-1]
        shieldio_data = {
            'schemaVersion': 1,
            'label': 'citations',
            'message': f"{citations}",
        }
        with open(sel_dir / f'{paper_id}.json', 'w') as fh:
            json.dump(shieldio_data, fh)
        saved += 1

    print(f"[{year}] saved {saved} selected_pubs files.")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--year', type=int, required=True)
    parser.add_argument('--csv', type=str, default=None, help='Optional year-specific CSV to read from')
    parser.add_argument('--src', type=str, default=None, help='Optional gs_data json (defaults to results/gs_data_<year>.json or results/gs_data.json)')
    args = parser.parse_args()
    run_for_year(args.year, csv_path=args.csv, src_json=args.src)


if __name__ == '__main__':
    main()
