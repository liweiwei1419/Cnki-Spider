from bs4 import BeautifulSoup
import re

with open('test.html', 'r', encoding='utf-8') as fr:
    content = fr.read()

    soup = BeautifulSoup(content, 'lxml')
    total_num = re.search(r'找到.*?(\d+,?\d+).*?条结果',content).group(1)
    print(total_num)
    next_btn = soup.select('div.TitleLeftCell a')[-1]
    if next_btn.get_text() == '下一页':
        print("有下一页按钮")
        # 点击下一页按钮，继续爬取
    else:
        print('--- 爬虫停止 ---')
