import requests
import pandas as pd
import time

url = "https://tianqi.2345.com/Pc/GetHistory"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
}

# 爬取年份和月份对应的表格
def craw_table(year, month):
    params = {
        "areaInfo[areaId]": 54449,  # 秦皇岛的ID
        "areaInfo[areaType]": 2,
        "date[year]": year,
        "date[month]": month
    }
    resp = requests.get(url, headers=headers, params=params)
    # 增加调试信息
    if resp.status_code != 200:
        print(f"请求失败，状态码：{resp.status_code}, URL: {resp.url}")
        return pd.DataFrame()  # 返回空的DataFrame
    try:
        data = resp.json()["data"]
        df = pd.read_html(data)[0]
        return df
    except Exception as e:
        print(f"解析失败，错误：{e}, 响应内容：{resp.text[:500]}")
        return pd.DataFrame()  # 返回空的DataFrame

df_list = []
for year in range(2011, 2025):
    for month in range(1, 13):
        if year == 2024 and month > 1:  # 只到2024年1月
            break
        print("正在爬取：", year, "年", month, "月的数据...")
        df = craw_table(year, month)
        if not df.empty:
            df_list.append(df)
        time.sleep(1)  # 增加延时，避免过快发送请求

if df_list:
    pd.concat(df_list).to_csv("秦皇岛的2011年1月到2024年1月天气数据123.csv", index=False)
    print("数据爬取完成并已保存到CSV文件。")
else:
    print("没有获取到任何数据。")
