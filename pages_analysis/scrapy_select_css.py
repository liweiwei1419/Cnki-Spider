from scrapy.selector import Selector

with open('test.html', encoding='utf-8') as fr:
    body = fr.read()

# 第 1 个不能要，其它都要
rows = Selector(text=body).css(".GridTableContent tr")
# print(len(rows[1:]))
print(rows[1:][0].extract())
for item in rows[1:]:
    # print(item.extract())
    order_number = item.css('td:nth-child(1)::text').extract()[0]
    href = item.css('td:nth-child(2) > a::attr(href)').extract()[0]
    title = item.css('td:nth-child(2) > a::text').extract()[0]
    print(order_number, href, title)
