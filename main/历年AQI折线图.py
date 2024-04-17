import pandas as pd
import plotly.graph_objs as go

# 加载数据，确保替换为你的CSV文件路径
df = pd.read_csv('秦皇岛天气最值.csv', encoding='GBK')

# 通过条件筛选来获取2016年及以后的所有年份
years = df[df['年份'] >= 2016]['年份'].unique()

# 创建图表
fig = go.Figure()

# 为每个年份添加最高AQI、最低AQI和平均AQI的数据轨迹
for year in years:
    filtered_df = df[df['年份'] == year]

    # 添加最高AQI轨迹
    fig.add_trace(
        go.Scatter(
            x=filtered_df['月份'],
            y=filtered_df['AQI_max'],
            name=f'{year} 最高AQI',
            mode='lines+markers',
            visible=False  # 初始设置为不可见
        )
    )

    # 添加最低AQI轨迹
    fig.add_trace(
        go.Scatter(
            x=filtered_df['月份'],
            y=filtered_df['AQI_min'],
            name=f'{year} 最低AQI',
            mode='lines+markers',
            visible=False  # 初始设置为不可见
        )
    )

    # 添加平均AQI轨迹
    fig.add_trace(
        go.Scatter(
            x=filtered_df['月份'],
            y=filtered_df['平均AQI'],
            name=f'{year} 平均AQI',
            mode='lines+markers',
            visible=False,  # 初始设置为不可见
            line=dict(color='green')
        )
    )

# 初始化按钮列表
buttons = []

# 为每个年份创建一个按钮，以更新图表显示相应年份的数据
for i, year in enumerate(years):
    # 计算每个按钮的可见性数组
    visibility = [False] * len(years) * 3  # 每个年份有三个轨迹
    visibility[i * 3:(i + 1) * 3] = [True, True, True]  # 当前年份轨迹设置为可见

    # 创建按钮
    button = dict(
        label=str(year),
        method='update',
        args=[{'visible': visibility},
              {'title': f'{year}年AQI'}]
    )
    buttons.append(button)

# 更新图表布局，添加下拉菜单
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
    }],
    title=f"{min(years)}年AQI"  # 设置初始显示的年份为2016年或之后的第一个年份
)

# 设置第一个年份(2016或之后的第一个年份)的轨迹为可见
visibility = [False] * len(fig.data)
visibility[:3] = [True, True, True]
fig.update_traces(visible=False)
fig.update_traces(visible=True, overwrite=True, selector=dict(name=f"{min(years)} 最高AQI"))
fig.update_traces(visible=True, overwrite=True, selector=dict(name=f"{min(years)} 最低AQI"))
fig.update_traces(visible=True, overwrite=True, selector=dict(name=f"{min(years)} 平均AQI"))

# 显示图表
from plotly.offline import plot
plot(fig, filename='历年AQI折线图.html', include_plotlyjs='cdn')
