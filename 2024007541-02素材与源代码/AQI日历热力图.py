import pandas as pd
import plotly.graph_objects as go
import numpy as np
import calendar

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 将日期列转换为日期类型，并提取年份、月份和日信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month
df['日'] = df['日期'].dt.day

# 筛选2016年及之后的数据
df = df[df['年份'] >= 2016]

# 假设空气质量数据在列'空气质量'中，将分类数据转换为数值（优:1, 良:2, 轻度污染:3, 中度污染:4, 重度污染:5, 严重污染:6）
quality_mapping = {
    '优': 1,
    '良': 2,
    '轻度污染': 3,
    '中度污染': 4,
    '重度污染': 5,
    '严重污染': 6
}
df['空气质量数值'] = df['空气质量'].map(quality_mapping)

# 年份列表
years = sorted(df['年份'].unique())

# 初始化图表
fig = go.Figure()

# 为每个年份绘制热力图
for year in sorted(df['年份'].unique()):
    z = np.full((12, 31), np.nan)  # 初始化矩阵，12个月，每个月最多31天
    for month in range(1, 13):
        days_in_month = calendar.monthrange(year, month)[1]  # 获取该月的天数
        for day in range(1, days_in_month + 1):
            condition = (df['年份'] == year) & (df['月份'] == month) & (df['日'] == day)
            air_quality_value = df.loc[condition, '空气质量数值']
            if not air_quality_value.empty:
                z[month - 1, day - 1] = air_quality_value.values[0]

    fig.add_trace(go.Heatmap(
        z=z,
        x=list(range(1, 32)),  # 日期
        y=list(calendar.month_name[1:]),  # 月份名称
        colorscale=[(0, 'lightgreen'), (0.5, 'yellow'), (1, 'red')],  # 自定义颜色映射
        showscale=True,
        name=str(year),
        visible=(year == sorted(df['年份'].unique())[0])  # 只有第一个年份默认可见
    ))

# 创建年份选择按钮
buttons = [
    dict(
        label=str(year),
        method="update",
        args=[{"visible": [year == y for y in sorted(df['年份'].unique())]},
              {"title": f"空气质量日历热力图 - {year}年"}]
    ) for year in sorted(df['年份'].unique())
]

# 更新图表布局，添加按钮
fig.update_layout(
    updatemenus=[{
        "type": "dropdown",
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.5,
        "y": 1.2,
        "xanchor": "left",
        "yanchor": "top",
        "buttons": buttons
    }],
    title="选择年份查看空气质量日历热力图"
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='AQI日历热力图.html', include_plotlyjs='cdn')
