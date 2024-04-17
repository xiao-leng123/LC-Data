import pandas as pd

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')  # 确保文件路径正确

# 将日期列转换为日期类型，并提取年份信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year

# 筛选2016年及之后的数据
df = df[df['年份'] >= 2016]

# 计算每年每个空气质量等级的天数
aqi_counts = df.groupby(['年份', '空气质量']).size().reset_index(name='天数')
import plotly.graph_objects as go

# 初始化图表
fig = go.Figure()

# 年份列表
years = sorted(df['年份'].unique())

# 为每个年份创建一个饼图轨迹
for year in years:
    year_data = aqi_counts[aqi_counts['年份'] == year]

    fig.add_trace(go.Pie(
        labels=year_data['空气质量'],
        values=year_data['天数'],
        name=str(year),
        visible=(year == years[0])  # 只有第一个年份默认可见
    ))

# 创建年份选择按钮
buttons = []

for year in years:
    buttons.append(dict(
        label=str(year),
        method='update',
        args=[{'visible': [year == y for y in years]},
              {'title': f'{year}年空气质量等级分布'}],
    ))

# 更新图表布局，添加按钮
fig.update_layout(
    updatemenus=[{
        'type': 'dropdown',
        'direction': 'down',
        'x': 0.5,
        'y': 1.2,
        'showactive': True,
        'buttons': buttons
    }],
    title=f'{years[0]}年空气质量等级分布'
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度天气污染等级饼图.html', include_plotlyjs='cdn')
