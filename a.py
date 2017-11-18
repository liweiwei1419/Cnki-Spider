from bs4_test import BeautifulSoup

def handle_url(url):
    new_str = url[4:]
    return "http://kns.cnki.net/KCMS" + new_str

with open('test.html', 'r', encoding='utf-8') as fr:
    content = fr.read()
    # print(content)

# "lxml" 必须指定
soup = BeautifulSoup(content, "lxml")
result = soup.select('a[class="fz14"]')

import csv
with open('result.csv','a',encoding='utf-8') as fw:
    writer = csv.writer(fw)

    for index, item in enumerate(result):
        print(index, handle_url(item['href']), item.text)
        writer.writerow(list((str(index), handle_url(item['href']), item.text)))


