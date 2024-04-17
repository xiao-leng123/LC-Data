import pandas as pd
import plotly.graph_objs as go

# 加载数据（确保路径正确，并且文件中包含平均气温的列）
df = pd.read_csv('秦皇岛天气最值.csv', encoding='GBK')

# 获取所有年份
years = df['年份'].unique()

# 创建图表
fig = go.Figure()

# 为每个年份添加最高气温、最低气温和平均气温的数据轨迹
for year in years:
    filtered_df = df[df['年份'] == year]

    # 添加最高气温和最低气温的轨迹
    fig.add_trace(
        go.Scatter(x=filtered_df['月份'], y=filtered_df['最高气温_max'], name='最高气温', mode='lines+markers',
                   visible=False))
    fig.add_trace(
        go.Scatter(x=filtered_df['月份'], y=filtered_df['最低气温_min'], name='最低气温', mode='lines+markers',
                   visible=False))

    # 添加平均气温的轨迹
    fig.add_trace(go.Scatter(x=filtered_df['月份'], y=filtered_df['平均气温'], name='平均气温', mode='lines+markers',
                             visible=False, line=dict(color='green')))

# 创建按钮
buttons = []

for i, year in enumerate(years):
    visibility = [False] * len(years) * 3  # 每个年份有三条线
    visibility[i * 3:(i + 1) * 3] = [True, True, True]  # 设置当前年份为可见
    button = dict(label=str(year),
                  method='update',
                  args=[{'visible': visibility},
                        {'title': f'{year}年的气温'}])
    buttons.append(button)

# 将按钮添加到图表中
fig.update_layout(
    showlegend=True,
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'pad': {"r": 10, "t": 10},
        'showactive': True,
        'x': 1,
        'xanchor': 'right',
        'y': 1.1,
        'yanchor': 'top'
    }]
)

# 设置默认显示第一个年份的数据
fig.data[0].visible = True
fig.data[1].visible = True
fig.data[2].visible = True  # 默认显示平均气温线

# 显示图表
from plotly.offline import plot
plot(fig, filename='历年气温折线图.html', include_plotlyjs='cdn')
