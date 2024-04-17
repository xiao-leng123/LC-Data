import pandas as pd
import plotly.graph_objects as go

# 假设的节假日日期
holidays = {
    '元旦': ['2016-01-01', '2017-01-01', '2018-01-01', '2019-01-01', '2020-01-01'],
    '春节': ['2016-02-08', '2017-01-28', '2018-02-16', '2019-02-05', '2020-01-25'],
    '清明节': ['2016-04-04', '2017-04-04', '2018-04-05', '2019-04-05', '2020-04-04'],
    '劳动节': ['2016-05-01', '2017-05-01', '2018-05-01', '2019-05-01', '2020-05-01'],
    '端午节': ['2016-06-09', '2017-05-30', '2018-06-18', '2019-06-07', '2020-06-25'],
    '国庆节': ['2016-10-01', '2017-10-01', '2018-10-01', '2019-10-01', '2020-10-01'],
}

# 加载天气数据
weather_data = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')
weather_data['日期'] = pd.to_datetime(weather_data['日期'])

# 统计每个节假日的天气情况
holiday_weather = {}
for holiday, dates in holidays.items():
    holiday_dates = pd.to_datetime(dates)
    holiday_data = weather_data[weather_data['日期'].isin(holiday_dates)]
    if not holiday_data.empty:
        # 计算每个节假日的平均气温和最常见的天气类型
        avg_temp = holiday_data['平均气温'].mean()
        most_common_weather = holiday_data['天气'].mode()[0]
        holiday_weather[holiday] = {'平均气温': avg_temp, '常见天气': most_common_weather}

# 将结果转换为DataFrame
holiday_weather_df = pd.DataFrame(holiday_weather).T.reset_index().rename(columns={'index': '节假日'})

# 使用Plotly绘制图表
fig = go.Figure(data=[
    go.Bar(name='平均气温', x=holiday_weather_df['节假日'], y=holiday_weather_df['平均气温']),
])

# 更新图表的布局
fig.update_layout(
    title='节假日的平均气温',
    xaxis_title='节假日',
    yaxis_title='平均气温 (℃)',
)

fig.show()
