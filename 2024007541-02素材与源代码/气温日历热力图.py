import pandas as pd
import plotly.graph_objects as go
import numpy as np

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 转换日期列为日期类型，并提取年份、月份和日信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month
df['日'] = df['日期'].dt.day

# 假设我们关注的是平均气温
df['平均气温'] = pd.to_numeric(df['平均气温'], errors='coerce')  # 确保是数值类型

# 年份列表
years = sorted(df['年份'].unique())

# 初始化图表
fig = go.Figure()

# 为每个年份绘制热力图
for year in years:
    df_year = df[df['年份'] == year]
    heatmap_data = np.full((31, 12), np.nan)  # 使用NaN初始化数组，31天，12月

    for _, row in df_year.iterrows():
        day = row['日'] - 1  # 0为基数索引
        month = row['月份'] - 1  # 0为基数索引
        heatmap_data[day, month] = row['平均气温']

    fig.add_trace(go.Heatmap(
        z=heatmap_data,
        x=list(range(1, 13)),  # 1到12月
        y=list(range(1, 32)),  # 1到31日
        colorscale='Viridis',
        showscale=True,
        name=str(year),
        visible=(year == years[0])  # 只有第一个年份默认可见
    ))

# 创建年份选择按钮
buttons = []
for i, year in enumerate(years):
    visible = [False] * len(years)
    visible[i] = True  # 使选定年份的热力图可见
    button = dict(
        label=str(year),
        method="update",
        args=[{"visible": visible},
              {"title": f"{year}年平均气温日历视图"}]
    )
    buttons.append(button)

# 更新图表布局，添加按钮
fig.update_layout(
    updatemenus=[{
        "type": "dropdown",
        "direction": "down",
        "x": 0.5,
        "y": 1.2,
        "showactive": True,
        "buttons": buttons
    }],
    title=f"{years[0]}年平均气温日历视图",
    xaxis=dict(title="月份"),
    yaxis=dict(title="日期")
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='气温日历热力图.html', include_plotlyjs='cdn')
