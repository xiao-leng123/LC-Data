import plotly.graph_objects as go
import pandas as pd

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 转换日期列为日期类型，并提取年份信息
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year

# 确保天气类型列存在并为字符串类型，假设列名为'天气'
df['天气'] = df['天气'].astype(str)

# 天气类型转换
def transform_weather(weather):
    if '~' in weather:
        return weather.split('~')[-1].strip()  # 取~后面的天气状态
    return weather

df['天气'] = df['天气'].apply(transform_weather)

# 天气类型简化，将一些特定的类型归为晴、多云等主要类型
weather_mapping = {
    '多云~晴': '晴',
    '阴~晴': '晴',
    '晴~多云': '多云',
    '小雨~多云': '多云',
    '晴~阴': '阴',
    # 可以根据需要添加更多映射规则
}
df['天气'] = df['天气'].replace(weather_mapping)

# 年份列表
years = sorted(df['年份'].unique())

# 初始化图表
fig = go.Figure()

# 为每个年份添加饼图轨迹
for year in years:
    df_year = df[df['年份'] == year]
    weather_counts = df_year['天气'].value_counts(normalize=True) * 100

    fig.add_trace(go.Pie(
        labels=weather_counts.index,
        values=weather_counts.values,
        name=str(year),
        visible=(year == years[0])  # 只有最初的年份默认可见
    ))

# 创建年份选择按钮
buttons = [
    dict(
        args=[{"visible": [True if str(year) in t.name else False for t in fig.data]},
              {"title": f"{year}年天气类型分布", "annotations": []}],
        label=str(year),
        method="update"
    ) for year in years
]

# 添加一个按钮来隐藏所有图层
buttons.append(
    dict(
        args=[{"visible": [False] * len(fig.data)},
              {"title": "选择年份查看天气类型分布", "annotations": []}],
        label="隐藏",
        method="update"
    )
)

# 更新图表布局，添加按钮
fig.update_layout(
    updatemenus=[{
        "buttons": buttons,
        "direction": "down",
        "pad": {"r": 10, "t": 10},
        "showactive": True,
        "x": 0.5,
        "y": 1.15,
        "xanchor": "left",
        "yanchor": "top"
    }],
    title="选择年份查看天气类型分布"
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='天气分布饼图.html', include_plotlyjs='cdn')
