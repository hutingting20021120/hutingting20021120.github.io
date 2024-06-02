"""
@filename:calendar.py.py
@author:Hu Tingting
@time:2024-05-31

"""
'''
按年份生成日历图，合并显示在一个html文件中
'''

import pandas as pd
from pyecharts import options as opts
from pyecharts.charts import Calendar, Page

# 读取CSV文件
data = pd.read_csv('./output/combined_comments.csv')

# 将时间列转换为日期时间类型
data['时间'] = pd.to_datetime(data['时间'])

# 创建页面
page = Page()

# 创建日历图
for year in range(2024, 2019, -1):  # 从2024年到2020年倒序遍历
    # 筛选出当前年份的数据
    year_data = data[data['时间'].dt.year == year]
    # 统计每天的数据量
    daily_count = year_data['时间'].dt.date.value_counts()
    # 准备日历图数据
    calendar_data = [(str(date), count) for date, count in daily_count.items()]
    # 创建Calendar图表
    calendar = (
        Calendar()
        .add("", calendar_data, calendar_opts=opts.CalendarOpts(range_=str(year)))
        .set_global_opts(
            title_opts=opts.TitleOpts(title=f"{year} Daily Activity Calendar"),
            visualmap_opts=opts.VisualMapOpts(max_=max(daily_count), min_=min(daily_count), is_show=False),
        )
    )
    # 将日历图添加到页面中
    page.add(calendar)

# 保存为HTML文件
page.render("./output/combined_calendar.html")
