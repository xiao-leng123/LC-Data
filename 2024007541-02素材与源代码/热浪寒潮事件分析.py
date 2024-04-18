import pandas as pd
import plotly.graph_objects as go


# 定义检测热浪和寒潮事件的函数
def detect_temperature_events(data, column, threshold, min_days=3, above=True):
    events = []
    in_event = False
    event_start = None

    for i, row in data.iterrows():
        if (above and row[column] > threshold) or (not above and row[column] < threshold):
            if not in_event:
                in_event = True
                event_start = row['日期']
            # If it's the last row and still in an event, close the event
            if i == len(data) - 1:
                events.append({'start': event_start, 'end': row['日期'],
                               'duration': (pd.to_datetime(row['日期']) - pd.to_datetime(event_start)).days + 1})
        else:
            if in_event:
                # End the event if it has been going on for long enough
                if (pd.to_datetime(row['日期']) - pd.to_datetime(event_start)).days >= min_days:
                    events.append({'start': event_start, 'end': data.iloc[i - 1]['日期'],
                                   'duration': (pd.to_datetime(data.iloc[i - 1]['日期']) - pd.to_datetime(
                                       event_start)).days + 1})
                in_event = False
    return events


# 加载数据
weather_data = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')

# 检测热浪和寒潮事件
heatwaves = detect_temperature_events(weather_data, '最高气温', 30, 3, above=True)
cold_spells = detect_temperature_events(weather_data, '最低气温', -10, 3, above=False)

# 创建图表
fig = go.Figure()

# 为热浪事件添加条形
for event in heatwaves:
    fig.add_trace(go.Bar(
        x=[event['start']],  # 使用事件开始日期作为x轴
        y=[event['duration']],  # 使用事件持续时间作为y轴高度
        name='热浪',
        marker_color='red'  # 设置条形颜色为红色
    ))

# 为寒潮事件添加条形
for event in cold_spells:
    fig.add_trace(go.Bar(
        x=[event['start']],
        y=[event['duration']],
        name='寒潮',
        marker_color='blue'
    ))

# 更新图表布局
fig.update_layout(
    barmode='group',  # 分组模式，使得热浪和寒潮的条形并列显示
    title='秦皇岛热浪和寒潮事件持续时间',
    xaxis_title='事件开始日期',
    yaxis_title='持续天数',
    yaxis=dict(type='linear'),  # 确保y轴为线性刻度，适合表示持续天数
    legend_title='事件类型'
)

# 显示图表
from plotly.offline import plot
plot(fig, filename='热浪寒潮事件分析.html', include_plotlyjs='cdn')
