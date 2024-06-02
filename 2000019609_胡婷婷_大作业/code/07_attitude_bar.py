"""
@filename:attitude_bar.py
@author:Hu Tingting
@time:2024-05-30

"""
'''
生成情感倾向条形图
'''
import pandas as pd
from pyecharts.charts import Bar
from pyecharts import options as opts

# 读取CSV文件
file_path = './output/combined_comments.csv'
df = pd.read_csv(file_path, encoding='utf-8')

# 情感倾向类别顺序
sentiment_order = ['非常消极', '较为消极', '中立', '较为积极', '非常积极']

# 统计各种情感倾向类别的数量
sentiment_count = df['sentiment_class'].value_counts().loc[sentiment_order]

# 准备数据
x_data = sentiment_count.index.tolist()
y_data = sentiment_count.values.tolist()

# 绘制条形图
bar = (
    Bar()
    .add_xaxis(x_data)
    .add_yaxis("情感倾向类别数量", y_data)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="情感倾向类别数量分布条形图"),
        xaxis_opts=opts.AxisOpts(name="情感倾向类别", type_="category", axislabel_opts={"interval": 0, "rotate": 45}),
        yaxis_opts=opts.AxisOpts(name="数量"),
    )
)

# 生成HTML文件（可选）
bar.render('./output/sentiment_distribution_bar_chart.html')

# 显示图表
bar.render_notebook()

