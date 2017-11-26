import csv
from cnki_spider.spiderLog import SpiderLog
import pandas as pd


class CnkiCsvExcel:
    def __init__(self):
        self.log = SpiderLog()
        self.title = ['序号', '关键字1', '关键词2', '关键字3', '正文标题', '副标题', '正文快照', '报纸日期', '版名', '版号', '分类号', '报纸名',
                      '报纸所在地',
                      '报纸所在地地址', '报纸级别', '报纸网址', '作者1', '作者2', '作者3']
        self.fr = open('output.csv', 'r', encoding='utf-8')
        self.log.info('--- 打开文件 ---')
        self.rows = csv.reader(self.fr)

    def __del__(self):
        self.log.info("--- 关闭文件 ---")
        self.fr.close()

    def write_data_from_csv(self):
        lines = []
        for line in self.rows:
            lines.append(line)

        df = pd.DataFrame(lines, columns=self.title)
        # pip install openpyxl
        df.to_excel('./items.xlsx', index=False)


if __name__ == '__main__':
    cnkiCsvExcel = CnkiCsvExcel()
    cnkiCsvExcel.write_data_from_csv()
