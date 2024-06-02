"""
@filename:attitude.py.py
@author:Hu Tingting
@time:2024-05-30

"""
'''
合并三个视频的csv文件
计算情感倾向值
自定义分类情感倾向类别
'''

import pandas as pd
from snownlp import SnowNLP

# 读取CSV文件
file1 = './output/comment1.csv'
file2 = './output/comment2.csv'
file3 = './output/comment3.csv'

df1 = pd.read_csv(file1, encoding='utf-8')
df2 = pd.read_csv(file2, encoding='utf-8')
df3 = pd.read_csv(file3, encoding='utf-8')

# 定义一个函数来分析情感倾向
def analyze_sentiment(comment):
    if pd.isnull(comment) or not isinstance(comment, str):
        return None  # 如果评论为空或非字符串，返回None
    s = SnowNLP(comment)
    return s.sentiments

# 定义一个函数来分类情感倾向
def classify_sentiment(score):
    if score is None:
        return None
    elif score > 0.8:
        return "非常积极"
    elif score > 0.6:
        return "较为积极"
    elif score > 0.4:
        return "中立"
    elif score > 0.2:
        return "较为消极"
    else:
        return "非常消极"

# 分别处理每个数据框
df1['sentiment'] = df1['内容'].apply(analyze_sentiment)
df2['sentiment'] = df2['内容'].apply(analyze_sentiment)
df3['sentiment'] = df3['内容'].apply(analyze_sentiment)

# 对每个数据框添加情感分类列
df1['sentiment_class'] = df1['sentiment'].apply(classify_sentiment)
df2['sentiment_class'] = df2['sentiment'].apply(classify_sentiment)
df3['sentiment_class'] = df3['sentiment'].apply(classify_sentiment)

# 合并三个数据框
combined_df = pd.concat([df1, df2, df3], ignore_index=True)

# 保存合并后的数据框到新的CSV文件
combined_df.to_csv('./output/combined_comments.csv', index=False, encoding='utf-8-sig')

print("处理完成并保存到 ./output/combined_comments.csv 文件中。")



