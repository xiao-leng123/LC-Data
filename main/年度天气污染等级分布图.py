import pandas as pd
import plotly.graph_objects as go

# 加载数据，假设完整的日期信息在'日期'列
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')  # 替换为实际的文件路径

# 将'日期'列转换为日期类型，并提取年份信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year

# 筛选2016年及之后的数据
df = df[df['年份'] >= 2016]

# 计算每年每个空气质量等级的天数
# 假设空气质量等级在'空气质量'列
aqi_yearly = df.groupby(['年份', '空气质量']).size().unstack(fill_value=0)

# 计算每年空气质量等级的频率（百分比）
aqi_yearly_percentage = aqi_yearly.div(aqi_yearly.sum(axis=1), axis=0) * 100

# 初始化图表
fig = go.Figure()

# 空气质量等级列表
aqi_levels = aqi_yearly_percentage.columns

# 添加柱状图轨迹，为每个空气质量等级
for level in aqi_levels:
    fig.add_trace(go.Bar(
        x=aqi_yearly_percentage.index,
        y=aqi_yearly_percentage[level],
        name=str(level),
    ))

# 更新图表布局为堆叠模式
fig.update_layout(
    barmode='stack',
    title='2016年及以后年度空气质量等级分布',
    xaxis=dict(title='年份', type='category'),
    yaxis=dict(title='频率 (%)'),
    legend_title='空气质量等级',
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度天气污染等级分布图.html', include_plotlyjs='cdn')
