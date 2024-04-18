import pandas as pd

# 加载CSV文件
df = pd.read_csv('秦皇岛天气数据.csv', encoding='gbk')

# 使用正则表达式提取“风向”
df['风向'] = df['风力风向'].str.extract(r'([东南西北]+风)')
# 提取“风力”
df['风力'] = df['风力风向'].str.extract(r'(\d+级|\d+-\d+级|\d+级)')

# 对于缺失的风向和风力，分别填充为“微风”和“1级”
df['风向'].fillna('微风', inplace=True)
df['风力'].fillna('1级', inplace=True)

# 将处理后的DataFrame保存到新的CSV文件中
df.to_csv('秦皇岛天气数据_风向风力分列修正_空值处理.csv', index=False, encoding='gbk')
