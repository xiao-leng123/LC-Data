import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import numpy as np

df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 示例数据预处理步骤
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 转换日期列为日期类型，并提取年份、月份
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year
df['月份'] = df['日期'].dt.month

# 删除风向为“微风”的记录
df = df[df['风向'] != '微风']

# 创建3行4列的子图布局
fig = make_subplots(rows=3, cols=4, specs=[[{'type': 'polar'}] * 4] * 3)

# 遍历每个月份，为每个月份创建风向图并放入相应的子图位置
for month in range(1, 13):
    # 这里只是示例，假设每个月的风力数据为1-8随机数，风向为8个基本方向
    fig.add_trace(go.Barpolar(
        r=[(month + i) % 8 + 1 for i in range(8)],  # 示例风力值
        theta=['北', '东北', '东', '东南', '南', '西南', '西', '西北'],
        name=f"{month}月",
    ), row=(month-1)//4 + 1, col=(month-1)%4 + 1)

# 手动添加月份标签作为注释
fig.update_layout(
    height=900,  # 调整图表大小以适应
    width=1200,
    title_text="1-12月风向图矩阵",
    annotations=[]  # 清除自动生成的子图标题
)

for month in range(1, 13):
    # 计算注释位置
    x_pos = ((month-1)%4) * (1/4) + 0.08  # X位置基于子图的列位置
    y_pos = 1 - ((month-1)//4) * (1/3) - 0.05  # Y位置基于子图的行位置
    fig.add_annotation(
        x=x_pos, y=y_pos,
        xref="paper", yref="paper",
        text=f"{month}月",
        showarrow=False,
        font=dict(size=12),
        bgcolor="rgba(255,255,255,0.5)"  # 背景色提高可读性
    )

# 显示图表
from plotly.offline import plot
plot(fig, filename='每月风力图(矩阵版).html', include_plotlyjs='cdn')