import pandas as pd
import plotly.graph_objects as go

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')  # 确保文件路径正确

# 将日期列转换为日期类型，并提取年份信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year

# 筛选2016年及之后的数据
df_filtered = df[df['年份'] >= 2016]

# 年份列表
years = sorted(df_filtered['年份'].unique())

# 初始化图表
fig = go.Figure()

import plotly.graph_objects as go

# 年份列表
years = sorted(df_filtered['年份'].unique())

# 初始化图表
fig = go.Figure()

# 为每个年份添加散点图轨迹
for year in years:
    df_year = df_filtered[df_filtered['年份'] == year]

    # 平均气温与AQI的关系
    fig.add_trace(go.Scatter(
        x=df_year['平均气温'],  # 使用平均气温数据
        y=df_year['AQI'],
        mode='markers',
        name=f'{year}',
        marker=dict(size=8, opacity=0.5),
        visible=(year == years[0])  # 只有第一个年份默认可见
    ))

# 创建年份选择按钮
buttons = []
for i, year in enumerate(years):
    visible = [False] * len(years)  # 每个年份有一个散点图轨迹
    visible[i] = True
    button = dict(
        label=str(year),
        method="update",
        args=[{"visible": visible},
              {"title": f"平均气温与AQI的关系散点图 - {year}年"}]
    )
    buttons.append(button)

# 更新图表布局，添加按钮
fig.update_layout(
    updatemenus=[{
        "type": "dropdown",
        "direction": "down",
        "x": 0.5,
        "y": 1.15,
        "showactive": True,
        "buttons": buttons
    }],
    title=f"平均气温与AQI的关系散点图 - {years[0]}年",
    xaxis_title="平均气温 (°C)",
    yaxis_title="AQI",
    legend_title="年份"
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='气温与AQI散点图.html', include_plotlyjs='cdn')
