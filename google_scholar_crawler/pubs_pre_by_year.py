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
        citation_message_part_2 = (
            "'><img src=\"https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2F"
        )
        citation_message_part_3 = (
            ".json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations\"></a>."
        )
        citation_message = (
            citation_message_part_1 + short_id + citation_message_part_2 + short_id + citation_message_part_3
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
    args = parser.parse_args()

    results_dir = Path("results")
    gs_path = results_dir / "gs_data.json"
    if not gs_path.exists():
        raise FileNotFoundError(f"{gs_path} not found. Run main.py first to refresh gs_data.json")

    data = json.load(open(gs_path, "r", encoding="utf-8"))
    pubs = extract_year_publications(data, args.year)
    out_csv = Path(args.out) if args.out else results_dir / f"all_publications_{args.year}.csv"
    save_csv(pubs, out_csv)
    print(f"Saved {len(pubs)} rows to {out_csv}")


if __name__ == "__main__":
    main()

