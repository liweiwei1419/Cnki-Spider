import requests
import re


# 参考资料：
# 【图文详解】python爬虫实战——5分钟做个图片自动下载器
# http://www.jianshu.com/p/19c846daccb3
def downloadPic(html, keyword):
    pic_url = re.findall('"objURL":"(.*?)"', html, re.S)

    # 第几张图片
    print('找到关键词:' + keyword + '的图片，现在开始下载图片...')
    for index, each in enumerate(pic_url):
        print('正在下载第' + str(index + 1) + '张图片，图片地址:' + str(each))
        try:
            pic = requests.get(each, timeout=10)
        except Exception:
            # except requests.exceptions.ConnectionError:
            print('第 {} 张图片无法下载'.format(index + 1))
            continue

        path_name = './pics//{}_{}.jpg'.format(key_word, index + 1)
        fp = open(path_name, 'wb')
        fp.write(pic.content)
        fp.close()


if __name__ == '__main__':
    key_word = '董文华'
    url = 'https://image.baidu.com/search/flip?tn=baiduimage&ie=utf-8&word={}&ct=201326592&ic=0&lm=-1&width=&height=&v=flip'.format(
        key_word)
    result = requests.get(url)
    downloadPic(result.text, key_word)
