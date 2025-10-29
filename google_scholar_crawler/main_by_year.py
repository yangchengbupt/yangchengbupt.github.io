from scholarly import scholarly, ProxyGenerator
import json
import os
import time
import random
from datetime import datetime
from pathlib import Path
import argparse


def init_proxy():
    pg = ProxyGenerator()
    try:
        if not pg.FreeProxies():
            print("[warn] No free proxies acquired; proceeding without proxies.")
        scholarly.use_proxy(pg)
    except Exception as e:
        print(f"[warn] Failed to initialize proxies: {e}")


def fetch_year(author_id: str, year: int, max_retries: int = 5, base_delay: float = 2.0):
    """Fetch publications for a specific year. Throttle every 5 items by 3s."""
    init_proxy()
    for attempt in range(1, max_retries + 1):
        try:
            # Fetch minimal author info
            author = scholarly.search_author_id(author_id)
            scholarly.fill(author, sections=["basics", "indices", "counts"])  # light fill

            pubs_for_year = []
            got_target = False
            passed_target = False

            # Iterate publications, typically ordered by year desc
            idx = 0
            try:
                pub_iter = scholarly.search_author_pubs(author_id)
                for pub in pub_iter:
                    idx += 1
                    try:
                        scholarly.fill(pub)  # need bib.pub_year
                    except Exception as fe:
                        print(f"[warn] fill pub failed: {fe}")
                        continue

                    bib = pub.get("bib", {})
                    py = str(bib.get("pub_year") or "")
                    if py.isdigit():
                        pyi = int(py)
                    else:
                        pyi = -1

                    if pyi == year:
                        pubs_for_year.append(pub)
                        got_target = True
                    elif pyi != -1 and pyi < year and got_target:
                        # Already went past target year in a desc list; we can stop early
                        passed_target = True
                        break

                    if idx % 5 == 0:
                        time.sleep(3)
            except Exception:
                # Fallback: bulk fill publications and filter
                scholarly.fill(author, sections=["publications"])  # heavier
                pubs = author.get("publications", [])
                for i, p in enumerate(pubs, start=1):
                    try:
                        scholarly.fill(p)
                    except Exception:
                        continue
                    bib = p.get("bib", {})
                    py = str(bib.get("pub_year") or "")
                    if py == str(year):
                        pubs_for_year.append(p)
                    if i % 5 == 0:
                        time.sleep(3)

            # Construct minimal author dict carrying only target-year publications
            result = {
                "container_type": "Author",
                "filled": ["basics", "publications", "indices", "counts"],
                "scholar_id": author_id,
                "name": author.get("name"),
                "affiliation": author.get("affiliation"),
                "interests": author.get("interests"),
                "citedby": author.get("citedby"),
                "updated": str(datetime.now()),
                "publications": {v["author_pub_id"]: v for v in pubs_for_year},
            }
            return result
        except Exception as e:
            wait = base_delay * (2 ** (attempt - 1)) + random.uniform(0, 1.0)
            print(f"[warn] Attempt {attempt}/{max_retries} failed: {e}. Retrying in {wait:.1f}s…")
            time.sleep(wait)
            init_proxy()
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", type=int, required=True)
    args = parser.parse_args()

    author_id = os.environ.get("GOOGLE_SCHOLAR_ID")
    if not author_id:
        print("[error] Missing env GOOGLE_SCHOLAR_ID; skip crawling.")
        return 0

    data = fetch_year(author_id, args.year)
    if data is None:
        print("[warn] Failed to fetch year data; exiting 0 to avoid pipeline break.")
        return 0

    results_dir = Path(__file__).resolve().parents[1] / "results"
    results_dir.mkdir(parents=True, exist_ok=True)
    out_json = results_dir / f"gs_data_{args.year}.json"
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)
    print(f"Saved year data to {out_json}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

