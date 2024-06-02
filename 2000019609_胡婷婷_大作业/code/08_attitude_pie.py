"""
@filename:attitude_pie.py
@author:Hu Tingting
@time:2024-05-30

"""
'''
生成情感倾向饼图
'''
import pandas as pd
from pyecharts.charts import Pie
from pyecharts import options as opts

# 读取CSV文件
file_path = './output/combined_comments.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 情感倾向类别顺序
sentiment_order = ['非常消极', '较为消极', '中立', '较为积极', '非常积极']

# 统计各种情感倾向类别的数量
sentiment_count = df['sentiment_class'].value_counts().reindex(sentiment_order).fillna(0)

# 准备数据
data_pair = [(sentiment, int(count)) for sentiment, count in zip(sentiment_count.index, sentiment_count.values)]

# 绘制饼图
pie = (
    Pie()
    .add("", data_pair)
    .set_global_opts(title_opts=opts.TitleOpts(title="情感倾向类别占比饼图"))
    .set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {d}%"))
)

# 生成HTML文件
pie.render('./output/sentiment_distribution_pie_chart.html')

# 显示图表
pie.render_notebook()
