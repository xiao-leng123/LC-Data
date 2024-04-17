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
        options=[{'label': i, 'value': i} for i in df['年'].unique()],
        value=df['年'].unique()[0]  # 默认值
    ),
    dcc.Dropdown(
        id='month-dropdown',
        options=[{'label': i, 'value': i} for i in range(1, 13)],
        value=1  # 默认值
    ),
    dcc.Graph(id='temperature-graph')
])

@app.callback(
    Output('temperature-graph', 'figure'),
    [Input('year-dropdown', 'value'),
     Input('month-dropdown', 'value')]
)
def update_graph(selected_year, selected_month):
    filtered_df = df[(df['年'] == selected_year) & (df['月'] == selected_month)]

    fig = go.Figure()
    fig.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['最高气温'], name='最高气温', mode='lines+markers'))
    fig.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['最低气温'], name='最低气温', mode='lines+markers'))
    # 添加平均气温折线
    fig.add_trace(go.Scatter(x=filtered_df['日期'], y=filtered_df['平均气温'], name='平均气温', mode='lines+markers', line=dict(color='green')))

    # 更新图表布局
    fig.update_layout(
        title=f'{selected_year}年{selected_month}月气温变化',
        xaxis_title='日期',
        yaxis_title='气温 (°C)',
        legend_title='气温类型',
        xaxis=dict(
            tickformat='%Y-%m-%d',  # 设置日期格式
            tickangle=-45  # 倾斜日期标签以提高可读性
        )
    )
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
