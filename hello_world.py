import requests

r = requests.get('http://www.cnki.net/')
r.encoding = 'utf-8'
print(r.text)
