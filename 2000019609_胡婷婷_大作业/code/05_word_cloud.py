"""
@filename:word_cloud.py.py
@author:Hu Tingting
@time:2024-05-31

"""
'''
生成词云图
基于本研究主题考虑，只保留了名词作为生成词云的素材。
'''
import pandas as pd
import jieba.posseg as pseg
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import WordCloud

# 读取CSV文件，指定内容列的数据类型为字符串，并将其中的浮点数转换为字符串
data = pd.read_csv('./output/combined_comments.csv', dtype={'内容': str}, converters={'内容': str})

# 合并所有评论
all_comments = ' '.join(data['内容'])

# 使用jieba进行分词和词性标注
words = pseg.cut(all_comments)

# 停用词表
stopwords = {'我们','你们','意思',"他们", "这个", "那个", "一些",'有点','感觉','视频','博主','好帅','厨子','大家','账号','飞哥'}  # 添加你认为需要的停用词

# 仅保留名词并统计词频
word_counts = Counter()
for word, flag in words:
    if flag.startswith('n') and word not in stopwords and len(word) > 1:
        word_counts[word] += 1

# 生成词云图
wordcloud = (
    WordCloud()
    .add("", word_counts.items(), word_size_range=[20, 100])
    .set_global_opts(title_opts=opts.TitleOpts(title="Pakistan WordCloud"))
)

# 保存为HTML文件
wordcloud.render("./output/wordcloud.html")







