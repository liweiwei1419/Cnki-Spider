import pandas as pd

import pandas as pd

papers = []

paper_1 = [1, '李威', 60, 60, 60]
paper_2 = [2, '周光', 100, 90, 80]
paper_3 = [3, '吴迪', 70, 80, 100]

papers.append(paper_1)
papers.append(paper_2)
papers.append(paper_3)

df = pd.DataFrame(papers, columns=['学号', '姓名', '语文', '数学', '英语'])

df.to_csv('./hello.csv', encoding='utf-8', index=False, mode='a', columns=None,header=False)
