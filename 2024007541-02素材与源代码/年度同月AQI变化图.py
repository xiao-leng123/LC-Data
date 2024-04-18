import pandas as pd
import plotly.graph_objects as go

# 加载数据
df = pd.read_csv('秦皇岛天气最值.csv', encoding='GBK')

# 筛选2016年到2024年的数据
df_filtered = df[(df['年份'] >= 2016) & (df['年份'] <= 2024)]

# 准备图表
fig = go.Figure()

# 月份列表
months = sorted(df_filtered['月份'].unique())
for month in months:
    # 筛选指定月份的数据
    month_df = df_filtered[df_filtered['月份'] == month]

    # 添加最高AQI的折线图
    fig.add_trace(go.Scatter(
        x=month_df['年份'], y=month_df['AQI_max'],
        mode='lines+markers',
        name=f'最高AQI - {month}月',
        visible=(month == 1)  # 仅1月份默认可见
    ))

    # 添加最低AQI的折线图
    fig.add_trace(go.Scatter(
        x=month_df['年份'], y=month_df['AQI_min'],
        mode='lines+markers',
        name=f'最低AQI - {month}月',
        visible=(month == 1)  # 仅1月份默认可见
    ))

    # 添加平均AQI的折线图
    fig.add_trace(go.Scatter(
        x=month_df['年份'], y=month_df['平均AQI'],
        mode='lines+markers',
        name=f'平均AQI - {month}月',
        visible=(month == 1)  # 仅1月份默认可见
    ))
# 生成月份选择按钮
buttons = []

for month in months:
    # 设置每个按钮对应的图表可见性
    visibility = [(m == month) for m in months for _ in range(3)]

    button = dict(
        label=f"{month}月",
        method="update",
        args=[{"visible": visibility},
              {"title": f"{month}月的AQI变化趋势"}]
    )
    buttons.append(button)

# 将按钮添加到图表布局中
fig.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.5,
        "xanchor": "left",
        "y": 1.15,
        "yanchor": "top"
    }],
    title="选择月份查看AQI变化趋势",
    xaxis_title="年份",
    yaxis_title="AQI"
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度同年同月AQI变化图.html', include_plotlyjs='cdn')