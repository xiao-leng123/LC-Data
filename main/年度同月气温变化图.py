import pandas as pd
import plotly.graph_objs as go

# 加载数据，确保替换为你的CSV文件路径
df = pd.read_csv('秦皇岛天气最值.csv', encoding='GBK')
df['日期'] = pd.to_datetime(df['年份'].astype(str) + '-' + df['月份'].astype(str) + '-01')

# 获取所有年份
years = sorted(df['年份'].unique())

# 创建图表
fig = go.Figure()

# 月份列表
months = sorted(df['月份'].unique())

# 对于每个月份，添加所有年份的最高气温和最低气温的轨迹
for month in months:
    # 筛选出该月份的所有年份的数据
    month_df = df[df['月份'] == month]

    # 添加最高气温的折线图
    fig.add_trace(
        go.Scatter(
            x=month_df['年份'],
            y=month_df['最高气温_max'],
            name=f'{month}月最高气温',
            mode='lines+markers',
            visible=(month == 1)  # 默认显示1月的数据
        )
    )

    # 添加最低气温的折线图
    fig.add_trace(
        go.Scatter(
            x=month_df['年份'],
            y=month_df['最低气温_min'],
            name=f'{month}月最低气温',
            mode='lines+markers',
            visible=(month == 1)  # 默认显示1月的数据
        )
    )

# 生成月份选择按钮
buttons = []
for i, month in enumerate(months):
    visibility = [False] * len(months) * 2  # 每个月份有两条轨迹（最高气温和最低气温）
    visibility[i * 2:(i + 1) * 2] = [True, True]  # 设置当前选定月份的轨迹为可见

    button = dict(
        label=f"{month}月",
        method="update",
        args=[{"visible": visibility},
              {"title": f"展示每年{month}月的最高气温和最低气温"}]
    )
    buttons.append(button)

# 更新图表布局，添加下拉菜单
fig.update_layout(
    updatemenus=[{
        'buttons': buttons,
        'direction': 'down',
        'pad': {"r": 10, "t": 10},
        'showactive': True,
        'x': 0.5,
        'xanchor': 'left',
        'y': 1.15,
        'yanchor': 'top'
    }],
    title="选择月份查看每年的最高气温和最低气温"
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度同年同月气温变化图.html', include_plotlyjs='cdn')
