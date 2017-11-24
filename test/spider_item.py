import csv
from selenium import webdriver

driver = webdriver.Chrome(executable_path='/Users/liwei/chromedriver')
with open('urls.csv', 'r', encoding='utf-8') as fr:
    rows = csv.reader(fr)
    print(type(rows))

    count = 0
    for row in rows:
        #if count == 3:
        #    break
        driver.get(row[1])
        with open('pager{}.html'.format(row[0]), 'w', encoding='utf-8') as fw:
            fw.write(driver.page_source)
        count += 1

print("end")
