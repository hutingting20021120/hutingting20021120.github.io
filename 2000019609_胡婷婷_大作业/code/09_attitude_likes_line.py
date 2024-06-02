"""
@filename:attitude_likes_scatter.py.py
@author:Hu Tingting
@time:2024-05-30

"""
'''
生成情感倾向与点赞量关系折线图
'''
import pandas as pd
from pyecharts.charts import Line
from pyecharts import options as opts

# 读取CSV文件
file_path = './output/combined_comments.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 将情感倾向转换为类别型数据并排序
df['sentiment'] = df['sentiment'].astype(float)
df['sentiment'] = pd.cut(df['sentiment'], bins=[-float('inf'), 0.2, 0.4, 0.6, 0.8, float('inf')],
                         labels=["非常消极", "较为消极", "中立", "较为积极", "非常积极"])
df['sentiment'] = df['sentiment'].astype(str)

# 删除含有 NaN 值的行
df.dropna(subset=['sentiment'], inplace=True)

# 计算点赞量的均值
likes_mean = df.groupby('sentiment')['点赞量'].mean().reset_index()

# 调整 x 轴顺序
x_order = ["非常消极", "较为消极", "中立", "较为积极", "非常积极"]
likes_mean = likes_mean[likes_mean['sentiment'].isin(x_order)]

# 绘制折线图
line = (
    Line()
    .add_xaxis(x_order)
    .add_yaxis("点赞量均值", likes_mean['点赞量'].tolist(), is_symbol_show=True,
               label_opts=opts.LabelOpts(is_show=False))
    .set_global_opts(title_opts=opts.TitleOpts(title="点赞量与情感倾向关系"),
                     xaxis_opts=opts.AxisOpts(type_="category"))
)

# 生成HTML文件（可选）
line.render('./output/sentiment_likes_line_chart.html')

# 显示图表
line.render_notebook()








