import json
import csv
import argparse
from pathlib import Path


def extract_year_publications(data: dict, year: str):
    pubs = []
    for pub_id, pub_data in data.get("publications", {}).items():
        if "bib" not in pub_data:
            continue
        pub_year = str(pub_data["bib"].get("pub_year") or "")
        if pub_year != str(year):
            continue
        title = pub_data["bib"].get("title")
        long_id = pub_id
        short_id = pub_id.split(":")[-1]
        citation_message_part_1 = (
            "<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:"
        )
        # Point shields to this repo and year-specific results branch
        citation_message_part_2 = (
            "'><img src=\"https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Fyangchengbupt%2Fyangchengbupt.github.io%2Fgoogle-scholar-stats-"
        )
        citation_message_part_3 = (
            "/selected_pubs%2F"  # completed later with short_id
            ".json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations\"></a>."
        )
        citation_message = (
            citation_message_part_1
            + short_id
            + citation_message_part_2
            + str(year)
            + citation_message_part_3.replace("/selected_pubs%2F", f"/selected_pubs%2F{short_id}")
        )
        pubs.append(
            {
                "title": title,
                "long_id": long_id,
                "short_id": short_id,
                "pub_year": pub_year,
                "citation_message": citation_message,
            }
        )
    return pubs


def save_csv(rows, out_csv: Path):
    out_csv.parent.mkdir(parents=True, exist_ok=True)
    with open(out_csv, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(
            f, fieldnames=["id", "title", "long_id", "short_id", "pub_year", "citation_message"]
        )
        writer.writeheader()
        for i, r in enumerate(rows, start=1):
            writer.writerow(
                {
                    "id": i,
                    "title": r["title"],
                    "long_id": r["long_id"],
                    "short_id": r["short_id"],
                    "pub_year": r["pub_year"],
                    "citation_message": r["citation_message"],
                }
            )


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--year", required=True)
    parser.add_argument("--out", default=None, help="Output CSV path; default results/all_publications_<year>.csv")
    parser.add_argument("--src", default=None, help="Source gs_data json; default results/gs_data.json or results/gs_data_<year>.json if exists")
    args = parser.parse_args()

    # Anchor to repository root results/
    results_dir = Path(__file__).resolve().parents[1] / "results"
    if args.src:
        gs_path = Path(args.src)
    else:
        # Prefer year-specific json if available
        yjson = results_dir / f"gs_data_{args.year}.json"
        gs_path = yjson if yjson.exists() else (results_dir / "gs_data.json")
    if not gs_path.exists():
        raise FileNotFoundError(f"{gs_path} not found. Run main.py first to refresh gs_data.json")

    data = json.load(open(gs_path, "r", encoding="utf-8"))
    pubs = extract_year_publications(data, args.year)

    # Merge with generic results (union by long_id) to avoid undercount when year json is partial
    generic = Path(__file__).resolve().parents[1] / "results" / "gs_data.json"
    if generic.exists():
        try:
            data2 = json.load(open(generic, "r", encoding="utf-8"))
            pubs2 = extract_year_publications(data2, args.year)
            before = len(pubs)
            seen = {p["long_id"] for p in pubs}
            for r in pubs2:
                if r["long_id"] not in seen:
                    pubs.append(r)
                    seen.add(r["long_id"])
            if len(pubs) > before:
                print(f"[info] Merge with generic added {len(pubs)-before} rows (now {len(pubs)}).")
        except Exception as e:
            print(f"[warn] Merge with generic failed: {e}")
    out_csv = Path(args.out) if args.out else results_dir / f"all_publications_{args.year}.csv"
    save_csv(pubs, out_csv)
    print(f"Saved {len(pubs)} rows to {out_csv}")


if __name__ == "__main__":
    main()
