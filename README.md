# 🚀 Bilibili Danmaku Analysis System (B站弹幕爬取分析系统)

> 一个基于 Python 的 Bilibili 弹幕采集、清洗与可视化分析系统。
> 采用模块化设计 (ETL 架构)，支持历史弹幕抓取、情感分析、词云生成及热词统计。

## 📖 项目简介

本项目旨在对 B站特定视频的弹幕数据进行深度挖掘。通过模拟浏览器请求获取历史弹幕数据，利用 Pandas 进行数据清洗与预处理，最后结合 NLP 技术（Jieba 分词、SnowNLP）进行情感倾向分析和可视化展示。

**核心价值**：
* **自动化采集**：突破 B 站前端限制，按日期范围批量抓取历史弹幕。
* **工程化设计**：采用标准的 `Config` + `Src` + `Main` 分层架构，解耦性强。
* **多维分析**：提供“情感分布”、“高频热词”及“词云图”三种维度的舆情报告。

---

## 🛠️ 技术栈 (Tech Stack)

* **语言**: Python 3.8+
* **爬虫**: `requests` (API 抓取), `re` (正则解析)
* **数据处理**: `pandas` (清洗与统计), `numpy`
* **自然语言处理**: `jieba` (中文分词), `snownlp` (情感分析)
* **可视化**: `matplotlib`, `seaborn`, `wordcloud`

---

## 📂 项目结构

```text
BilibiliDanmukuCrawler/
├── config.py              # [配置中心] 全局参数、路径、Cookie、爬取目标
├── main.py                # [程序入口] 调度 Spider, Cleaner, Analyzer
├── requirements.txt       # [依赖文件] 项目所需的第三方库
├── src/                   # [源代码目录]
│   ├── spider.py          # [采集模块] 负责网络请求、反爬策略、正则提取
│   ├── cleaner.py         # [清洗模块] 去重、去噪、异常值处理
│   └── analyzer.py        # [分析模块] 情感打分、绘图、词云生成
└── data/                  # [数据仓库] (程序自动生成)
    ├── raw/               # 存放原始 Excel 数据
    ├── processed/         # 存放清洗后的数据
    ├── results/           # 存放最终生成的分析图表 (词云、饼图等)
    └── resources/         # 存放停用词表 (stopwords.txt)

