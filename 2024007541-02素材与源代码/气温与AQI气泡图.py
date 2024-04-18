import pandas as pd
import plotly.graph_objects as go

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')  # 请确保文件路径正确

# 转换日期列为日期类型，并提取年份和月份信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year

# 筛选2016年及之后的数据
df_filtered = df[df['年份'] >= 2016]

# 检查并转换AQI和平均气温列为数值类型
df_filtered['AQI'] = pd.to_numeric(df_filtered['AQI'], errors='coerce')
df_filtered['平均气温'] = pd.to_numeric(df_filtered['平均气温'], errors='coerce')

# 年份列表
years = sorted(df_filtered['年份'].unique())

# 初始化图表
fig = go.Figure()

# 为每个年份添加散点图轨迹
for year in years:
    df_year = df_filtered[df_filtered['年份'] == year]

    # 移除AQI或平均气温中的NaN值
    df_year = df_year.dropna(subset=['AQI', '平均气温'])

    # 确保AQI列没有NaN值后再创建气泡图
    fig.add_trace(go.Scatter(
        x=df_year['平均气温'],  # 使用平均气温数据
        y=df_year['AQI'],  # 使用AQI值
        mode='markers',
        marker=dict(
            size=df_year['AQI'] / 5,  # 用AQI值除以5作为气泡大小，调整大小以便于观察
            opacity=0.5
        ),
        name=f'{year}',
        visible=(year == years[0])  # 只有第一个年份默认可见
    ))

# 创建年份选择按钮
buttons = []
for i, year in enumerate(years):
    visible = [False] * len(years)  # 每个年份有一个散点图轨迹
    visible[i] = True
    button = dict(
        label=str(year),
        method="update",
        args=[{"visible": visible},
              {"title": f"平均气温与AQI的关系气泡图 - {year}年"}]
    )
    buttons.append(button)

# 更新图表布局，添加按钮
fig.update_layout(
    updatemenus=[{
        "type": "dropdown",
        "direction": "down",
        "x": 0.5,
        "y": 1.15,
        "showactive": True,
        "buttons": buttons
    }],
    title=f"平均气温与AQI的关系气泡图 - {years[0]}年",
    xaxis_title="平均气温 (°C)",
    yaxis_title="AQI",
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='气温与AQI气泡图.html', include_plotlyjs='cdn')
