import pandas as pd
import plotly.graph_objects as go

# 加载和准备数据
weather_data = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')
weather_data['日期'] = pd.to_datetime(weather_data['日期'])
weather_data = weather_data[weather_data['日期'].dt.year >= 2016]

# 绘图
fig = go.Figure()

# 获取年份列表
years = sorted(weather_data['日期'].dt.year.unique())

# 为每个年份添加一个隐藏的柱状图
for year in years:
    yearly_data = weather_data[weather_data['日期'].dt.year == year]
    air_quality_counts = yearly_data['空气质量'].value_counts().reset_index()
    air_quality_counts.columns = ['空气质量等级', '日数']

    fig.add_trace(
        go.Bar(
            x=air_quality_counts['空气质量等级'],
            y=air_quality_counts['日数'],
            name=str(year),
            visible=(year == years[0])
        )
    )

# 创建一个按钮为每个年份
buttons = []
for i, year in enumerate(years):
    buttons.append(
        dict(
            label=str(year),
            method="update",
            args=[{"visible": [year == y for y in years]},
                  {"title": f"空气质量等级日数 - {year}"}]
        )
    )

# 添加按钮到图表布局
fig.update_layout(
    updatemenus=[{
        "type": "dropdown",
        "direction": "down",
        "x": 0.5,  #
        "y": 1.05,
        "xanchor": "center",
        "yanchor": "bottom",
        "showactive": True,
        "buttons": buttons
    }],
    title=f"空气质量等级日数 - {years[0]}"
)

from plotly.offline import plot
plot(fig, filename='空气质量天数统计图.html', include_plotlyjs='cdn')