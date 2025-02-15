import re
import json
import os
import random

# add some new things for extracting selected publications and get the shieldio data

def clean_title(title):
    """
    如果标题以 (xxxx) 开头，则移除该部分，并去除 ')' 后的空格。
    
    参数:
        title (str): 原始标题。
        
    返回:
        str: 清理后的标题。
    """
    # 正则表达式匹配以 (xxxx) 开头的模式
    pattern = r'^\([^\)]+\)\s*'
    cleaned_title = re.sub(pattern, '', title)
    return cleaned_title

def read_titles(filename):
    # 从csv文件中读取标题，标题是第二列，从第二行开始
    titles = []
    with open (filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            title = line.split(',')[1]
            titles.append(title)
    return titles

def read_long_ids_2024_before(filename):
    # 从csv文件中读取标题，标题是第二列，从第二行开始
    long_ids = []
    with open (filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            long_id = line.split(',')[2]
            year = line.split(',')[4]
            if year < '2024':
                long_ids.append(long_id)
    return long_ids

def read_long_ids_2024_and_now(filename):
    # 从csv文件中读取标题，标题是第二列，从第二行开始
    long_ids = []
    with open (filename, 'r') as file:
        lines = file.readlines()
        for line in lines[1:]:
            long_id = line.split(',')[2]
            year = line.split(',')[4]
            if year == '2024':
                long_ids.append(long_id)
    return long_ids

def extract_titles(markdown_content):
    """
    从给定的 Markdown 内容中提取 '## 🔖 Selected Publications' 部分的出版物标题，并进行清理。
    
    参数:
        markdown_content (str): Markdown 文件的内容。
    
    返回:
        list: 提取并清理后的标题列表。
    """
    titles = []
    in_selected_publications = False
    extract_next_line = False  # 标志是否需要提取下一行的标题

    # 按行分割内容
    lines = markdown_content.split('\n')
    
    for line_number, line in enumerate(lines, 1):
        # 检查是否进入 '## 🔖 Selected Publications' 部分
        if not in_selected_publications:
            # # 📝 Publications
            if re.match(r'^#\s*📝\s*Publications', line):
                in_selected_publications = True
                # print(f"进入 'Selected Publications' 部分 (第 {line_number} 行)")
            continue
        else:
            # 如果遇到新的标题（以 '#' 开头），则退出
            if re.match(r'^#\s*🎖\s*Honors\s*and\s*Awards', line):
                # print(f"遇到新标题，停止提取 (第 {line_number} 行)")
                break
            
            # 检查当前行是否以 '-', '*', '+' 开头
            if re.match(r'^[\-\*\+]\s+', line):
                extract_next_line = True
                # print(f"找到以 '-', '*', 或 '+' 开头的行 (第 {line_number} 行)，准备提取下一行的标题")
                continue  # 继续到下一行

            # 如果标志为需要提取下一行的标题
            if extract_next_line:
                # 使用正则表达式提取方括号中的内容
                match = re.search(r'\[([^\]]+)\]\([^)]+\)', line)
                if match:
                    title = match.group(1).strip()
                    # 清理标题
                    # cleaned_title = clean_title(title)
                    titles.append(title)
                    # print(f"提取并清理标题: {cleaned_title} (第 {line_number} 行)")
                # else:
                #     print(f"第 {line_number} 行未找到匹配的标题格式")
                extract_next_line = False  # 重置标志

    return titles

def find_citations_by_long_id(data, target_long_id):
    """
    从Google Scholar数据中查找指定长ID论文的引用数量
    
    参数:
    data (dict): Google Scholar数据字典
    target_long_id (str): 要查找的论文长ID
    
    返回:
    tuple: (引用数量, 论文ID) 如果找到论文，否则返回 (None, None)
    """
    # 遍历publications字典
    for paper_id, paper_info in data['publications'].items():
        # 获取当前论文长ID
        current_long_id = paper_info['author_pub_id']
        
        # 比较长ID
        if current_long_id == target_long_id:
            return paper_info['num_citations'], paper_id
    
    return None, None

def find_citations_by_title(data, target_title):
    """
    从Google Scholar数据中查找指定标题论文的引用数量
    
    参数:
    data (dict): Google Scholar数据字典
    target_title (str): 要查找的论文标题
    
    返回:
    tuple: (引用数量, 论文ID) 如果找到论文，否则返回 (None, None)
    """
    # 转换目标标题为小写，用于不区分大小写的比较
    target_title = target_title.lower().strip()
    
    # 遍历publications字典
    for paper_id, paper_info in data['publications'].items():
        # 获取当前论文标题并转换为小写
        current_title = paper_info['bib']['title'].lower().strip()
        
        # 比较标题
        if current_title == target_title:
            return paper_info['num_citations'], paper_id
    
    return None, None

# 假设您的 Markdown 文件名为 'publications.md'
# markdown_file = '../_pages/about.md'

# try:
#     # 读取 Markdown 文件内容
#     with open(markdown_file, 'r', encoding='utf-8') as file:
#         content = file.read()
#     print("Markdown 文件已成功读取。\n")
# except FileNotFoundError:
#     print(f"文件 '{markdown_file}' 未找到。请检查路径是否正确。")
#     exit(1)
# except Exception as e:
#     print(f"读取文件时出错: {e}")
#     exit(1)

def title_citations():

    # 提取并清理标题
    # publication_titles = extract_titles(content)

    publication_titles = read_titles('results/all_publications.csv')
    # print(test_titles)

    json_file = f'results/gs_data.json'
    selected_data = json.load(open(json_file, 'r'))

    for title in publication_titles:
        cleaned_title = clean_title(title)
        
        if title == cleaned_title:
        # 提取第一个单词作为关键字
            keyword = cleaned_title.split()[0]
        else:
        # 提取没清理前的第一个()中的内容作为关键字
            keyword = title.split()[0]
        # 去除括号
        keyword = keyword[1:-1]
        # print(f"提取并清理标题: {cleaned_title}，关键字: {keyword}")
        
        # 在results文件夹下创建selected_pubs文件夹，如果不存在
        if not os.path.exists('results/selected_pubs'):
            os.makedirs('results/selected_pubs')
        
        citations, paper_id = find_citations_by_title(selected_data, cleaned_title)
        
        # print(paper_id)
        
        # paper_id里面有一个:，只需要后面的部分
        if paper_id is not None:
            paper_id = paper_id.split(':')[-1]
        
        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            # 变成字符串
            "message": f"{citations}",
        }
        
        # 保存为json文件
        with open(f'results/selected_pubs/{paper_id}.json', 'w') as file:
            json.dump(shieldio_data, file)
        

    print("已成功提取并保存所选出版物的引用数据。")
    
    return

def long_id_citations():
    
    global count
    count = 0
    
    # long_ids
    long_ids = read_long_ids_2024_before('results/all_publications.csv')
    # print(long_ids)
    
    long_ids.append('OlLjVUcAAAAJ:RYcK_YlVTxYC', 'OlLjVUcAAAAJ:lSLTfruPkqcC', 'OlLjVUcAAAAJ:_Qo2XoVZTnwC',
                    'OlLjVUcAAAAJ:yD5IFk8b50cC')
    
    json_file = f'results/gs_data.json'
    selected_data = json.load(open(json_file, 'r'))
    
    for long_id in long_ids:
        citations, paper_id = find_citations_by_long_id(selected_data, long_id)
        
        if paper_id is not None:
            paper_id = paper_id.split(':')[-1]
            
        # if paper_id == 'yD5IFk8b50cC':
        #     print(f"论文 {paper_id} 的引用数为 {citations}")
        
        shieldio_data = {
            "schemaVersion": 1,
            "label": "citations",
            # 变成字符串
            "message": f"{citations}",
        }
        
        # print(f"论文 {paper_id} 的引用数为 {citations}")
        
        # 检查是否存在selected_pubs文件夹，如果不存在则创建
        import os
        if not os.path.exists('results/selected_pubs'):
            os.makedirs('results/selected_pubs')
        
        # 检查是否存在paper_id.json文件，如果不存在则创建
        # if not os.path.exists(f'results/selected_pubs/{paper_id}.json'):
        #     os.mknod(f'results/selected_pubs/{paper_id}.json')
    
        try:
            
            with open(f'results/selected_pubs/{paper_id}.json', 'w') as file:
                json.dump(shieldio_data, file)
                count += 1
        
        except Exception as e:
            print(f"保存文件时出错: {e}")
            print(f"论文 {paper_id} 的引用数为 {citations}")
            continue

    
    # print("已成功提取并保存所选出版物的引用数据。")
    print(f"共有 {count} 篇论文的引用数据已保存。")
    
    return

if __name__ == '__main__':
    # title_citations()
    long_id_citations()