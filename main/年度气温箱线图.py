import pandas as pd
import plotly.graph_objects as go

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')  # 确保路径正确

# 将日期列转换为日期类型，并提取年份和月份
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 初始化图表
fig = go.Figure()

# 年份列表
years = sorted(df['年份'].unique())

# 对每个年份绘制每个月份的最高气温和最低气温箱线图
for year in years:
    df_year = df[df['年份'] == year]
    for month in range(1, 13):  # 1到12月
        df_month = df_year[df_year['月份'] == month]
        # 最高气温箱线图
        fig.add_trace(go.Box(y=df_month['最高气温'], name=f'{month}月', boxmean='sd', visible=(year == years[0])))
        # 最低气温箱线图
        fig.add_trace(go.Box(y=df_month['最低气温'], name=f'{month}月', boxmean='sd', visible=(year == years[0])))

# 为每个年份创建一个按钮
buttons = []
for i, year in enumerate(years):
    # 设置对应年份的图形为可见
    visible = [False] * len(years) * 24  # 每年有12个月，每月两个箱线图（最高和最低气温）
    visible[i*24:(i+1)*24] = [True] * 24
    button = dict(label=str(year),
                  method="update",
                  args=[{"visible": visible},
                        {"title": f"{year}年气温分布情况"}])
    buttons.append(button)

# 更新图表布局
fig.update_layout(
    updatemenus=[dict(active=0,
                      buttons=buttons,
                      direction="down",
                      pad={"r": 10, "t": 10},
                      showactive=True,
                      x=0.5,
                      xanchor="left",
                      y=1.15,
                      yanchor="top")],
    title=f"{years[0]}年气温分布情况"
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='年度气温箱线图.html', include_plotlyjs='cdn')
