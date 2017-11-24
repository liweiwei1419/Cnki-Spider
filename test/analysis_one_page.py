from bs4 import BeautifulSoup

import pandas as pd
import re

subtitle_pattern = r'id="catalog_TI_SUB">副标题：</label>(.*?)</p>'
publish_date_pattern = r'id="catalog_DATE">报纸日期：</label>(.*?)</p>'
layer_name_pattern = r'id="catalog_LM">版名：</label>(.*?)</p>'
layer_num_pattern = r'<label id="catalog_BH">版号：</label>(.*?)</p>'
category_num_pattern = r'<label id="catalog_ZTCLS">分类号：</label>(.*?)</p>'


# 使用正则表达式解析文本
def parse_info(body, pattern):
    model = re.search(pattern, body)
    if model is None:
        return ''
    else:
        return model.group(1)


lines = []

for i in range(1, 21):
    with open('pager{}.html'.format(i), encoding='utf-8') as fr:
        try:
            body = fr.read()

            line = []
            soup = BeautifulSoup(body, 'lxml')
            # 1 正文标题
            title = soup.select('#mainArea h2.title')[0].text
            # 2 副标题
            # subtitle = soup.select('.wxBaseinfo > p')[0].text
            subtitle = parse_info(body, subtitle_pattern)
            # 3 正文快照，后面要加 [0]
            content_snapshot = soup.select('#ChDivSummary')[0].text
            # 4 报纸日期
            publish_date = parse_info(body, publish_date_pattern)
            # 5 版名
            layer_name = parse_info(body, layer_name_pattern)
            # 6 版号
            layer_num = parse_info(body, layer_num_pattern)
            # 7 分类号
            category_num = parse_info(body,category_num_pattern)
            # 8 报纸名
            newspaper_name = soup.select('.sourinfo a[target="kcmstarget"]')[0].text
            # 9 报纸所在地
            newspaper_site = soup.select('.sourinfo p')[1].text
            # 10 报纸所在地地址
            newspaper_location = soup.select('.sourinfo p')[2].text
            # 11 报纸级别
            newspaper_level = soup.select('.sourinfo p')[3].text
            # 12 报纸网址
            newspaper_url = soup.select('.sourinfo a[target="kcmstarget"]')[1].text
            # 13 作者（要考虑到有多个作者的情况）
            author1 = ''
            author2 = ''
            author3 = ''
            author = soup.select('.author span')
            if len(author) == 1:
                author1 = author[0].text
            if len(author) == 2:
                author1 = author[0].text
                author2 = author[1].text
            if len(author) == 3:
                author1 = author[0].text
                author2 = author[1].text
                author3 = author[2].text


            # 写入 excel（优化的时候，使用缓存，分批追加写入）
            # line.append(title, subtitle, content_snapshot, publish_date, layer_name, layer_num, category_num, newspaper_name,newspaper_site, newspaper_location, newspaper_level, newspaper_url, author)
            line.append('联想')
            line.append('品牌')
            line.append('危机')
            line.append(title)
            line.append(subtitle)
            line.append(content_snapshot)
            line.append(publish_date)
            line.append(layer_name)
            line.append(layer_num)
            line.append(category_num)
            line.append(newspaper_name)
            line.append(newspaper_site)
            line.append(newspaper_location)
            line.append(newspaper_level)
            line.append(newspaper_url)
            line.append(author1)
            line.append(author2)
            line.append(author3)
            lines.append(line)
        except Exception:
            print("文章 {} 解析出问题".format(i))
            continue

df = pd.DataFrame(lines,
                  columns=['关键字1', '关键词2', '关键字3', '正文标题', '副标题', '正文快照', '报纸日期', '版名', '版号', '分类号', '报纸名', '报纸所在地',
                           '报纸所在地地址', '报纸级别', '报纸网址', '作者1','作者2','作者3'])

import datetime

today = datetime.date.today().strftime('%Y-%m-%d')
df.to_excel('./result/result_{}.xls'.format(today))
