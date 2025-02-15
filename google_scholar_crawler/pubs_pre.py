import json
import csv

def extract_publication_info(json_data):
    """
    从JSON数据中提取论文信息。

    Args:
        json_data: 包含作者信息的JSON数据。

    Returns:
        一个列表，每个元素是一个字典，包含一篇论文的信息。
    """
    publications = []
    if "publications" in json_data:
        for pub_id, pub_data in json_data["publications"].items():
            if "bib" in pub_data:  # 确保存在bib信息
                title = pub_data["bib"].get("title")
                long_id = pub_id
                short_id = pub_id.split(":")[-1]
                pub_year = pub_data["bib"].get("pub_year")
                citation_message_part_1 = """<a href='https://scholar.google.com/citations?view_op=view_citation&hl=zh-CN&user=OlLjVUcAAAAJ&citation_for_view=OlLjVUcAAAAJ:"""
                citation_message_part_2 = """'><img src="https://img.shields.io/endpoint?url=https%3A%2F%2Fraw.githubusercontent.com%2Falbertyang33%2Falbertyang33.github.io%2Fgoogle-scholar-stats%2Fselected_pubs%2F"""
                citation_message_part_3 = """.json&logo=Google%20Scholar&labelColor=f6f6f6&color=9cf&style=flat&label=citations"></a>."""
                citation_message = citation_message_part_1 + short_id + citation_message_part_2 + short_id + citation_message_part_3
                # pub_year 必须是字符串类型，才能写入文件
                pub_year = str(pub_year) if pub_year is not None else "" # 转换为字符串，处理None

                publications.append({
                    "title": title,
                    "long_id": long_id,
                    "short_id": short_id,
                    "pub_year": pub_year,
                    "citation_message": citation_message
                })
    return publications

def sort_publications_by_year(publications):
    """
    按年份对论文进行倒序排序。

    Args:
        publications: 论文信息列表。

    Returns:
        排序后的论文信息列表。
    """
    return sorted(publications, key=lambda x: x["pub_year"], reverse=True)

def save_publications_to_csv(publications, filename):
    """
    将论文信息保存到CSV文件。

    Args:
        publications: 排序后的论文信息列表。
        filename: CSV文件名。
    """
    with open(filename, "w", newline="", encoding="utf-8") as csvfile:
        fieldnames = ["id", "title", "long_id", "short_id", "pub_year", "citation_message"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for i, pub in enumerate(publications):
            writer.writerow({
                "id": i + 1,
                "title": pub["title"],
                "long_id": pub["long_id"],
                "short_id": pub["short_id"],
                "pub_year": pub["pub_year"],
                "citation_message": pub["citation_message"]
            })

def main():
    """
    主函数，读取JSON文件，提取、排序、保存论文信息。
    """
    # 读取JSON文件 (替换为你的JSON文件路径)
    with open("./results/gs_data.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # 提取论文信息
    publications = extract_publication_info(data)

    # 按年份倒序排序
    sorted_publications = sort_publications_by_year(publications)

    # 保存到CSV文件 (替换为你想要保存的CSV文件路径)
    save_publications_to_csv(sorted_publications, "./results/all_publications.csv")
    print("论文信息已保存到 all_publications.csv")

if __name__ == "__main__":
    main()