from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')
df['日期'] = pd.to_datetime(df['日期'])
df['年'] = df['日期'].dt.year
df['月'] = df['日期'].dt.month

app = Dash(__name__)

app.layout = html.Div([
    dcc.Dropdown(
        id='year-dropdown',
        # 筛选2016年及以后的年份作为选项
        options=[{'label': i, 'value': i} for i in df['年'].unique() if i >= 2016],
        value=min(i for i in df['年'].unique() if i >= 2016)  # 默认选中2016年或第一个可用的年份
    ),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': i, 'value': i} for i in range(1, 13)],
        value=1  # 默认选中1月
    ),
    dcc.Graph(id='aqi-graph')
])

@app.callback(
    Output('aqi-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_graph(selected_year, selected_month):
    # 根据选择的年份和月份筛选数据
    filtered_df = df[(df['年'] == selected_year) & (df['月'] == selected_month)]

    # 创建图表
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['AQI'], name='AQI', mode='lines+markers'))

    # 更新图表布局，设置y轴为线性比例
    fig.update_layout(
        title=f'{selected_year}年{selected_month}月每日AQI变化',
        xaxis_title='日期',
        yaxis_title='AQI',
        yaxis=dict(type='linear'),  # 确保y轴使用线性比例
        xaxis=dict(
            tickformat='%Y-%m-%d',  # 设置日期格式
            tickangle=-45  # 倾斜日期标签以提高可读性
        ),
        legend_title='AQI'
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
