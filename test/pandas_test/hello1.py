with open('urls.csv', 'r', encoding='utf-8') as fr:
    paper_links = fr.readlines()
    paper_links = paper_links[0:10]

print(paper_links)
