import csv
import arxiv
import time
import re

def sanitize_title(title):
    """
    Sanitize the title for arXiv API search.  Removes special characters
    and excessive whitespace that might cause search issues.
    """
    # Remove non-alphanumeric characters (except spaces and hyphens)
    title = re.sub(r'[^\w\s-]', '', title)
    # Replace multiple spaces/hyphens with a single space
    title = re.sub(r'[\s-]+', ' ', title)
    return title.strip()


def search_arxiv(title):
    """
    Searches arXiv for a paper by title and returns relevant information.

    Args:
        title: The title of the paper.

    Returns:
        A tuple: (authors, arxiv_link) or (None, None) if not found.
        authors is a string of comma-separated author names.
    """
    try:
        # Sanitize the title before searching
        sanitized_title = sanitize_title(title)
        
        search = arxiv.Search(
            query=f'ti:"{sanitized_title}"',  # Search in the title field
            max_results=5,  # Limit results to avoid excessive API calls
            sort_by=arxiv.SortCriterion.Relevance,  # Sort by relevance
            sort_order=arxiv.SortOrder.Descending
        )

        for result in search.results():
            # Check if the result title is a close match (case-insensitive)
            if result.title.lower().strip() == title.lower().strip() :   
                authors = ", ".join(author.name for author in result.authors)
                arxiv_link = f"https://arxiv.org/abs/{result.entry_id.split('/')[-1]}"
                return authors, arxiv_link
            # Fuzzy Title Matching:
            elif are_titles_similar(sanitized_title, result.title):
                authors = ", ".join(author.name for author in result.authors)
                arxiv_link = f"https://arxiv.org/abs/{result.entry_id.split('/')[-1]}"
                return authors, arxiv_link
            
        return None, None  # No matching paper found
    except arxiv.ArxivError as e:
        print(f"ArXiv API error: {e}")
        return None, None
    except Exception as e:  # Catch other potential errors
        print(f"An unexpected error occurred: {e}")
        return None, None

def are_titles_similar(title1, title2):
    """
    Check if two titles are similar, accounting for minor differences.

    Args:
        title1 (str): The first title.
        title2 (str): The second title.

    Returns:
        bool: True if the titles are similar, False otherwise.
    """

    # Lowercase and remove punctuation:
    title1 = re.sub(r'[^\w\s]', '', title1).lower()
    title2 = re.sub(r'[^\w\s]', '', title2).lower()

    # Tokenize (split into words):
    words1 = title1.split()
    words2 = title2.split()

    # Check for common words (e.g., 80% overlap):
    common_words = set(words1) & set(words2)
    if len(common_words) / max(len(words1), len(words2)) >= 0.8:  # 80% threshold
        return True

    return False

def main():
    """
    Main function to read publication data, search arXiv, and save results.
    """
    input_filename = "./results/all_publications.csv"  # Replace with your input CSV filename
    output_filename = "./results/arxiv_results.csv"  # Replace with desired output filename

    with open(input_filename, "r", encoding="utf-8") as infile, \
            open(output_filename, "w", newline="", encoding="utf-8") as outfile:

        reader = csv.DictReader(infile)
        fieldnames = ["id", "title", "authors", "arxiv_link"]
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        writer.writeheader()

        for i, row in enumerate(reader):
            title = row["title"]
            print(f"Processing: {title}")
            authors, arxiv_link = search_arxiv(title)

            # Handle cases where no results are found
            if authors is None:
                authors = "Not Found"
            if arxiv_link is None:
                arxiv_link = "Not Found"
            
            writer.writerow({
                "id": i + 1,
                "title": title,
                "authors": authors,
                "arxiv_link": arxiv_link
            })

            # Add a delay to avoid overwhelming the arXiv API.
            time.sleep(3)

    print(f"ArXiv search results saved to {output_filename}")
if __name__ == "__main__":
    main()