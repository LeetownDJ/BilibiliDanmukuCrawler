import requests
import re
import pandas as pd
import time
import random
import os
from datetime import datetime, timedelta
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import HEADERS, DATA_RAW_DIR

# 生成从 start 到 end 的所有日期字符串列表
def generate_date_list(start, end):
    start_dt = datetime.strptime(start, '%Y-%m-%d')
    end_dt = datetime.strptime(end, '%Y-%m-%d')
    date_list = []
    curr = start_dt
    while curr <= end_dt:
        date_list.append(curr.strftime('%Y-%m-%d'))
        curr += timedelta(days=1)
    return date_list


def run_spider(oid, start_date, end_date):
    # 生成日期列表
    dates_to_crawl = generate_date_list(start_date, end_date)
    print(f"️ 计划爬取: OID={oid}, 时间={start_date} ~ {end_date}, 共 {len(dates_to_crawl)} 天")

    all_danmu = []  # 用于存储所有日期的弹幕

    for date in dates_to_crawl:
        # 构造 URL
        url = f'https://api.bilibili.com/x/v2/dm/web/history/seg.so?type=1&oid={oid}&date={date}'

        print(f"正在爬取 {date} ... ", end="")

        try:
            # 发送请求 (使用 config.py 里配置好的 HEADERS)
            response = requests.get(url=url, headers=HEADERS)

            if response.status_code == 200:
                raw_data = response.text
                daily_data = re.findall('.*?([\u4e00-\u9fa5]+).*?', raw_data)

                if daily_data:
                    all_danmu.extend(daily_data)
                    print(f"成功 (获取 {len(daily_data)} 条)")
                else:
                    print(f"无数据")
            else:
                print(f"失败 (状态码 {response.status_code})")

        except Exception as e:
            print(f"出错 ({e})")

        # 随机休眠，防封
        sleep_time = random.uniform(1, 3)
        time.sleep(sleep_time)

    # 保存数据
    if all_danmu:
        print("\n 正在保存文件...")
        df = pd.DataFrame(all_danmu, columns=['弹幕内容'])

        # 文件名加上日期范围，并保存到 data/raw/ 目录
        filename = f'弹幕_{start_date}_{end_date}.xlsx'
        output_path = os.path.join(DATA_RAW_DIR, filename)

        df.to_excel(output_path, index=False)

        print(f" 爬取完成！总共获取 {len(df)} 条弹幕。")
        print(f"文件已保存为: {output_path}")

        return output_path  # 返回路径给 main.py 使用
    else:
        print("\n 没有抓取到任何数据，请检查 Cookie 或日期范围。")
        return None