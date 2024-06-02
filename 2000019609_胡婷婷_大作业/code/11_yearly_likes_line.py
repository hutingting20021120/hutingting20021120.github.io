"""
@filename:test.py
@author:Hu Tingting
@time:2024-05-31

"""
'''
按年份生成点赞量与情感倾向关系折线图
合并显示在一张图里
'''
import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Line

# 1. 读取 CSV 文件并加载数据
df = pd.read_csv("./output/combined_comments.csv", parse_dates=["时间"])  # 替换为你的 CSV 文件路径，解析时间列

# 添加一列提取年份
df['year'] = df['时间'].dt.year

# 2. 按年份和情感倾向对数据进行分组，并计算点赞量的均值
grouped = df.groupby(['year', 'sentiment_class'])['点赞量'].mean().reset_index().round(3)

# 3. 使用 Pyecharts 生成折线图
years = sorted(df['year'].unique())  # 获取所有年份
sentiments = ['非常消极', '较为消极', '中立', '较为积极', '非常积极']  # 情感倾向顺序

line = Line()
for year in years:
    data = grouped[grouped['year'] == year]
    likes_mean = data['点赞量'].tolist()

    line.add_xaxis(sentiments)
    line.add_yaxis(
        series_name=str(year),
        y_axis=likes_mean,
    )

line.set_global_opts(title_opts=opts.TitleOpts(title="不同年份评论点赞量与情感倾向的关系"),
                     xaxis_opts=opts.AxisOpts(type_="category", name="情感倾向"),
                     yaxis_opts=opts.AxisOpts(type_="value", name="点赞量均值"),
                     legend_opts=opts.LegendOpts(pos_left="right"))

line.render("./output/yearly_likes_line_chart.html")
