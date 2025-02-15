import csv

def create_paper_info(arxiv_row):
    """
    Creates the 'paper_info' string from a row in arxiv_results.csv.
    """
    title = arxiv_row.get("title", "Title Not Found")
    arxiv_link = arxiv_row.get("arxiv_link", "")
    authors = arxiv_row.get("authors", "Authors Not Found")
    
    part_1 = """- <span class="conference-badge">Conference Name</span>"""

    paper_info = part_1 + f'[{title}]({arxiv_link})\n{authors}'
    
    return paper_info

def create_paper_message(paper_info, citation_message):
    """
    Combines paper_info and citation_message.
    """
    paper_message = paper_info+ "\n\n\n" + citation_message
    return paper_message

def post_process(paper_message):
    # 如果存在""，则替换为"
    paper_message = paper_message.replace('""', '"')
    
    
    return paper_message

def main():
    """
    Main function: Reads data, merges based on ID, and writes the combined output.
    """
    arxiv_filename = "./results/arxiv_results.csv"
    publications_filename = "./results/all_publications.csv"
    output_filename = "./results/combined_papers.csv"

    # Load data, keyed by ID this time
    arxiv_data = {}
    with open(arxiv_filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            arxiv_data[int(row["id"])] = row  # Key by integer ID

    publications_data = {}
    with open(publications_filename, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            publications_data[int(row["id"])] = row  # Key by integer ID ("序号")


    with open(output_filename, "w", newline="", encoding="utf-8") as outfile:
        fieldnames = ["id", "title", "paper_message", "year"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        # Iterate through arxiv_data, as it's the basis for the output
        for arxiv_id, arxiv_row in arxiv_data.items():
            # Find matching publication data by ID
            publications_row = publications_data.get(arxiv_id)

            if publications_row:
                paper_info = create_paper_info(arxiv_row)
                citation_message = publications_row["citation_message"]  # Get citation from publications
                pub_year = publications_row["pub_year"]
                paper_message = create_paper_message(paper_info, citation_message)
                paper_message = post_process(paper_message)

                writer.writerow({
                    "id": arxiv_id,  # Use the common ID
                    "title": arxiv_row["title"],  # Use title from arxiv_data
                    "paper_message": paper_message,
                    "year": pub_year
                })
            else:
                # Handle missing publication (shouldn't happen with ID matching, but good to check)
                print(f"Warning: No publication entry found for ID: {arxiv_id}")
                writer.writerow({
                    "id": arxiv_id,
                    "论文标题": arxiv_row["title"],
                    "paper_message": "No publication data found.\\n\\n\\n",
                    "year": "Year Not Found"
                })

    print(f"Combined paper information saved to {output_filename}")
    
    # 将csv文件转为json文件，要求正确显示结构化数据
    
    import pandas as pd
    df = pd.read_csv(output_filename)
    df.to_json('./results/combined_papers.json', orient='records', force_ascii=False)
    print("combined_papers.json文件已生成")

if __name__ == "__main__":
    main()