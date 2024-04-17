import pandas as pd
import plotly.graph_objects as go

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 将日期列转换为日期类型，并提取年份和月份信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 筛选2016年及之后的数据
df_filtered = df[df['年份'] >= 2016]

# 初始化图表
fig = go.Figure()

# 年份列表
years = sorted(df_filtered['年份'].unique())

# 为每个年份的每个月份绘制AQI的箱线图
for year in years:
    df_year = df_filtered[df_filtered['年份'] == year]
    for month in sorted(df_year['月份'].unique()):
        df_month = df_year[df_year['月份'] == month]

        fig.add_trace(go.Box(
            y=df_month['AQI'],
            name=f'{month}月',
            legendgroup=f'{year}',  # 设置图例分组
            showlegend=True if month == 1 else False,  # 只为每个年份的第一个月份显示图例
            visible=(year == years[0]),  # 只有第一个年份默认可见
            boxmean=True  # 显示均值
        ))

# 创建年份选择按钮
buttons = []
for year in years:
    visible = [(year == y) for y in years for _ in range(12)]  # 每个年份有12个月份
    button = dict(
        label=str(year),
        method="update",
        args=[{"visible": visible},
              {"title": f"{year}年AQI分布情况"}]
    )
    buttons.append(button)

# 更新图表布局，添加按钮
fig.update_layout(
    updatemenus=[{
        "type": "dropdown",
        "direction": "down",
        "x": 0.5,
        "y": 1.2,
        "showactive": True,
        "buttons": buttons
    }],
    title=f"{years[0]}年AQI分布情况"
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度AQI箱线图.html', include_plotlyjs='cdn')
