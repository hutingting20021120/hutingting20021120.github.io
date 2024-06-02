"""
@filename:test.py.py
@author:Hu Tingting
@time:2024-05-31

"""
'''
按年份生成情感倾向类别柱状图，和情感倾向值变化折线图
合并显示在同一个图里
'''
from pyecharts.charts import Bar, Line
from pyecharts import options as opts
from pyecharts.commons.utils import JsCode
import pandas as pd

# 读取 CSV 文件
df = pd.read_csv('./output/combined_comments.csv')

# 转换时间列为 datetime 类型
df['时间'] = pd.to_datetime(df['时间'])

# 提取年份
df['年份'] = df['时间'].dt.year.astype(str)

# 计算每年的情感倾向指数均值，并保留三位小数
sentiment_mean = df.groupby('年份')['sentiment'].mean().round(3)

# 计算每年的情感倾向类别数量
sentiment_counts = df.groupby(['年份', 'sentiment_class']).size().unstack(fill_value=0)

# 调整情感倾向类型的顺序
sentiment_order = ['非常消极', '较为消极', '中立', '较为积极', '非常积极']
sentiment_counts = sentiment_counts[sentiment_order]

# 创建图表
combined_chart = (
    Bar()
    .add_xaxis(sentiment_counts.index.tolist())
    .extend_axis(
        yaxis=opts.AxisOpts(
            name="情感倾向指数均值",
            type_="value",
            min_=0,
            max_=1,
            axislabel_opts=opts.LabelOpts(formatter="{value}"),
            position="right",
            offset=0,
        )
    )
    .add_yaxis("非常消极", sentiment_counts['非常消极'].tolist(), yaxis_index=0)
    .add_yaxis("较为消极", sentiment_counts['较为消极'].tolist(), yaxis_index=0)
    .add_yaxis("中立", sentiment_counts['中立'].tolist(), yaxis_index=0)
    .add_yaxis("较为积极", sentiment_counts['较为积极'].tolist(), yaxis_index=0)
    .add_yaxis("非常积极", sentiment_counts['非常积极'].tolist(), yaxis_index=0)
    .set_global_opts(
        title_opts=opts.TitleOpts(title="年份情感分析"),
        yaxis_opts=opts.AxisOpts(name="数量", type_="value"),
        legend_opts=opts.LegendOpts(
            pos_bottom="1%",
            pos_left="center",
            orient="horizontal",
            type_="scroll",
            item_height=10,
            item_width=30,
            textstyle_opts=opts.TextStyleOpts(font_size=12),
        ),
    )
)

# 绘制情感倾向指数均值折线图
combined_chart_line = (
    Line()
    .add_xaxis(sentiment_mean.index.tolist())
    .add_yaxis(
        "情感倾向指数均值",
        sentiment_mean.tolist(),
        yaxis_index=1,
        linestyle_opts=opts.LineStyleOpts(width=2)
    )
)

# 合并图表
combined_chart.overlap(combined_chart_line)

# 渲染为 HTML 文件
combined_chart.render('./output/sentiment_analysis_combined.html')



