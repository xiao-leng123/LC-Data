import pandas as pd
import plotly.graph_objects as go

df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 示例数据预处理步骤
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 转换日期列为日期类型，并提取年份、月份
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 删除风向为“微风”的记录
df = df[df['风向'] != '微风']

# 初始化图表
fig = go.Figure()

# 为每个月份添加图表轨迹
for month in range(1, 13):
    df_month = df[df['月份'] == month]
    fig.add_trace(go.Barpolar(
        r=df_month['风力'],
        theta=df_month['风向'],
        name=f"{month}月",
        visible=(month == 1)  # 仅1月份默认可见
    ))

# 创建月份选择按钮
buttons = [
    dict(
        label=f"{month}月",
        method="update",
        args=[{"visible": [m == month for m in range(1, 13)]},
              {"title": f"所有年份{month}月风向和风力情况"}]
    )
    for month in range(1, 13)
]

# 更新图表布局
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
    title="选择月份查看所有年份风向和风力情况",
    polar=dict(radialaxis=dict(visible=True))
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='每月风力图.html', include_plotlyjs='cdn')
