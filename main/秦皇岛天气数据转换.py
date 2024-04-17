# 导入CSV库
import csv

# Step 1: 打开文本文件进行读取
with open("秦皇岛天气数据.txt", "r", encoding="utf-8") as text_file:
    # 读取文本文件的所有行
    lines = text_file.readlines()

# Step 2: 准备CSV数据
# 分割每行中的数据并去除两端的空格
csv_data = [line.strip().split() for line in lines]

# Step 3: 将数据写入CSV文件
with open("秦皇岛天气数据.csv", "w", encoding="utf-8", newline="") as csv_file:
    writer = csv.writer(csv_file)
    writer.writerows(csv_data)
