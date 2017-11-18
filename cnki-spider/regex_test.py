import re

str1 = '<p><label id="catalog_TI_SUB">副标题：</label>——2009中国区域品牌传播论坛暨“好客山东”旅游品牌与价值推广会议专家发言摘要</p>'

pattern = r'id="catalog_TI_SUB">副标题：</label>(.*?)</p>'
mo = re.search(pattern, str1)
print(mo.group(1))
