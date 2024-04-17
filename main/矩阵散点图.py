import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# 加载数据
df = pd.read_csv('秦皇岛天气数据.csv', encoding='GBK')
df['日期'] = pd.to_datetime(df['日期'])
df['年份'] = df['日期'].dt.year

# 天气数据处理：如果有"~"符号，以"~"后的为准
df['天气'] = df['天气'].apply(lambda x: x.split('~')[-1])

# 初始化Dash应用
app = dash.Dash(__name__)

# 应用布局
app.layout = html.Div([
    html.H1("年平均气温、AQI、风力的散点矩阵图"),
    dcc.Dropdown(
        id='year-dropdown',
        options=[{'label': year, 'value': year} for year in sorted(df['年份'].unique()) if year >= 2016],
        value=2016  # 默认选择2016年
    ),
    dcc.Graph(id='scatter-matrix-graph')
])

# 回调函数更新图表
@app.callback(
    Output('scatter-matrix-graph', 'figure'),
    [Input('year-dropdown', 'value')]
)
def update_figure(selected_year):
    filtered_df = df[df['年份'] == selected_year]
    # 创建散点矩阵图，以平均气温、AQI、风力为维度
    fig = px.scatter_matrix(filtered_df,
                            dimensions=['平均气温', 'AQI', '风力'],
                            title=f"{selected_year}年平均气温、AQI、风力的散点矩阵图")
    return fig

# 运行应用
if __name__ == '__main__':
    app.run_server(debug=True)
