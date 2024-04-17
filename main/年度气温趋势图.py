import pandas as pd
import plotly.graph_objs as go

# 替换为你的CSV文件路径
df = pd.read_csv('秦皇岛天气最值.csv', encoding='GBK')

# 构造完整日期列，这里将每个月份的日期统一设置为该月的第一天
df['日期'] = pd.to_datetime(df['年份'].astype(str) + '-' + df['月份'].astype(str) + '-01')

# 排序，确保日期顺序正确
df.sort_values(by='日期', inplace=True)

# 创建图表
fig = go.Figure()

# 添加最高气温折线图
fig.add_trace(
    go.Scatter(x=df['日期'], y=df['最高气温_max'], name='最高气温', mode='lines')
)

# 添加最低气温折线图
fig.add_trace(
    go.Scatter(x=df['日期'], y=df['最低气温_min'], name='最低气温', mode='lines')
)

# 设置图表布局
fig.update_layout(
    title_text='秦皇岛最高气温和最低气温趋势',
    xaxis_title='日期',
    yaxis_title='气温 (°C)',
    xaxis=dict(
        rangeselector=dict(
            buttons=list([
                dict(count=1, label="1年", step="year", stepmode="backward"),
                dict(count=2, label="2年", step="year", stepmode="backward"),
                dict(count=5, label="5年", step="year", stepmode="backward"),
                dict(step="all")
            ])
        ),
        rangeslider=dict(visible=True),
        type="date"
    )
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度气温趋势图.html', include_plotlyjs='cdn')
