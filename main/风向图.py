import pandas as pd
import plotly.graph_objects as go
import numpy as np

df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 示例数据清洗和转换函数
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 转换日期列为日期类型，并提取年份、月份
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 删除风向为“微风”的记录
df = df[df['风向'] != '微风']

# 年份列表
years = sorted(df['年份'].unique())

# 初始化图表
fig = go.Figure()

# 为每个年份添加极坐标图轨迹
for year in years:
    df_year = df[df['年份'] == year]
    # 这里假设风向数据已经是整理好的
    fig.add_trace(go.Barpolar(
        r=df_year['风力'],
        theta=df_year['风向'],
        name=str(year),
        visible=(year == min(years))  # 只有最初的年份默认可见
    ))

# 创建年份选择按钮
buttons = [
    dict(
        label=str(year),
        method="update",
        args=[{"visible": [y == year for y in years]},
              {"title": f"风向和风力情况- {year}年"}]
    )
    for year in years
]

# 更新图表布局，添加年份选择按钮
fig.update_layout(
    updatemenus=[{
        "type": "dropdown",
        "buttons": buttons,
        "direction": "down",
        "x": 0.5,
        "y": 1.2,
        "xanchor": "left",
        "yanchor": "top"
    }],
    title="选择年份查看风向和风力情况",
    polar=dict(radialaxis=dict(visible=True))
)

# 显示图表
# from plotly.offline import plot
# plot(fig, filename='风向图.html', include_plotlyjs='cdn')
fig.show()
