import pandas as pd
import re
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_PROCESSED_DIR


def clean_data(input_path):
    print(f" 正在读取并清洗: {input_path}")
    df = pd.read_excel(input_path)
    # 核心清洗逻辑
    comment_column_names = ['弹幕内容']
    for column_name in comment_column_names:
        # 1. 去重
        df.drop_duplicates(subset=column_name, inplace=True)
        # 2. 正则去噪 (只保留汉字、字母、数字)
        df[column_name] = df[column_name].apply(lambda x: re.sub(r'[^\w\s]', '', str(x)))
        # 3. 去空
        df.dropna(subset=[column_name], inplace=True)
        # 4. 长度过滤
        min_length = 3
        df = df[df[column_name].apply(lambda x: len(str(x)) >= min_length)]

    # 生成输出路径
    filename = os.path.basename(input_path)
    clean_filename = f"Cleaned_{filename}"
    output_path = os.path.join(DATA_PROCESSED_DIR, clean_filename)

    # 保存
    df.to_excel(output_path, index=False)
    print(f" 清洗完成！文件已保存至: {output_path}")

    return output_path