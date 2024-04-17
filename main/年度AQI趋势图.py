import pandas as pd
import plotly.graph_objects as go

# 加载数据，确保替换为你的CSV文件路径
df = pd.read_csv('秦皇岛天气最值.csv', encoding='GBK')

# 由于年份和月份分开，我们构造一个日期字符串用于图表的X轴标签，这里简化处理，将每月的日期统一假设为每月的第一天
df['日期'] = pd.to_datetime(df['年份'].astype(str) + '-' + df['月份'].astype(str) + '-01')

# 筛选出2016到2024年的数据
df_filtered = df[(df['年份'] >= 2016) & (df['年份'] <= 2024)]

# 排序，确保日期顺序正确
df_filtered.sort_values(by='日期', inplace=True)

# 创建图表
fig = go.Figure()

# 添加最高AQI折线图
fig.add_trace(
    go.Scatter(x=df_filtered['日期'], y=df_filtered['AQI_max'], name='最高AQI', mode='lines')
)

# 添加最低AQI折线图
fig.add_trace(
    go.Scatter(x=df_filtered['日期'], y=df_filtered['AQI_min'], name='最低AQI', mode='lines')
)

# 设置图表布局
fig.update_layout(
    title_text='秦皇岛最高AQI和最低AQI趋势',
    xaxis_title='日期',
    yaxis_title='AQI',
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
plot(fig, filename='年度AQI趋势图.html', include_plotlyjs='cdn')
