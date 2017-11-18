from bs4_test import BeautifulSoup

with open('test.html', encoding='utf-8') as fr:
    body = fr.read()

# 第 1 个不能要，其它都要
soup = BeautifulSoup(body, 'lxml')
rows = soup.select(".GridTableContent tr")

#print(rows[1:][0])
for item in rows[1:]:
    #print(type(item))
    order_number = item.select('td')[0].text
    href = item.select('a')[0].get('href')
    title = item.select('a')[0].text
    #print(order_number)
    print(order_number,href,title)
