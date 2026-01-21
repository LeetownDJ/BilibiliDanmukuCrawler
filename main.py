import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from config import TARGET_OID, START_DATE, END_DATE
from src.spider import run_spider
from src.cleaner import clean_data
from src.analyzer import analyze_sentiment, generate_wordcloud, count_keywords, analyze_topics


def main():
    print("=== Bilibili网站视频弹幕爬取程序 ===")
    # 数据采集 调用 spider.py 里的函数，它会返回下载好的文件路径
    raw_file = run_spider(TARGET_OID, START_DATE, END_DATE)
    if not raw_file:
        print(" 爬虫未获取到数据，程序结束。")
        return

    # 数据清洗 把爬下来的文件传给 cleaner.py
    if os.path.exists(raw_file):
        clean_file = clean_data(raw_file)
    else:
        print("找不到原始文件，跳过清洗。")
        return

    # 数据分析 把清洗好的文件传给 analyzer.py
    if clean_file and os.path.exists(clean_file):
        print("\n--- 开始执行分析模块 ---")
        # A. 情感分析
        analyze_sentiment(clean_file)
        # B. 词云生成
        generate_wordcloud(clean_file)
        # C. 热词统计
        count_keywords(clean_file)
        # D. LDA 主题挖掘
        # 设定分成 3 类话题，每个话题看 5 个关键词
        analyze_topics(clean_file, num_topics=3, num_words=5)
        print(f"\n 所有分析结果已保存至 data/results/ 目录")
    else:
        print(" 清洗文件不存在，无法分析。")


if __name__ == '__main__':
    main()