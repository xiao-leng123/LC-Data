import pandas as pd
import plotly.graph_objects as go

# 加载数据
df = pd.read_csv('秦皇岛天气最值.csv', encoding='GBK')

# 构造完整日期列，这里将每个月份的日期统一设置为该月的第一天
df['日期'] = pd.to_datetime(df['年份'].astype(str) + '-' + df['月份'].astype(str) + '-01')

# 筛选年份范围
df = df[df['年份'] >= 2011]

# 初始化图表
fig = go.Figure()

# 年份列表
years = sorted(df['年份'].unique())

# 用于更新按钮的列表
buttons = []

# 对每个年份添加数据
for year in years:
    filtered_df = df[df['年份'] == year]
    # 添加最低气温柱状图
    fig.add_trace(
        go.Bar(
            x=filtered_df['月份'], y=filtered_df['最低气温_min'],
            name=f'最低气温 {year}',
            visible=(year == years[0])  # 只有第一个年份默认可见
        )
    )
    # 添加平均气温柱状图
    fig.add_trace(
        go.Bar(
            x=filtered_df['月份'], y=filtered_df['平均气温'],
            name=f'平均气温 {year}',
            visible=(year == years[0])
        )
    )
    # 最后添加最高气温柱状图
    fig.add_trace(
        go.Bar(
            x=filtered_df['月份'], y=filtered_df['最高气温_max'],
            name=f'最高气温 {year}',
            visible=(year == years[0])
        )
    )

    # 创建按钮
    buttons.append(dict(
        label=str(year),
        method='update',
        args=[{'visible': [y == year for y in years for _ in range(3)]},  # 对应年份的数据可见
              {'title': f'{year}年气温数据'}]
    ))

# 添加按钮到图表
fig.update_layout(
    updatemenus=[{
        'type': 'dropdown',
        'direction': 'down',
        'x': 0.5,
        'y': 1.2,
        'showactive': True,
        'buttons': buttons
    }],
    barmode='stack',
    title=f'{years[0]}年气温数据'
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度气温堆叠柱状图.html', include_plotlyjs='cdn')
