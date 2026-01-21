import pandas as pd
import jieba
import os
import matplotlib.pyplot as plt
import seaborn as sns
from wordcloud import WordCloud
from snownlp import SnowNLP
from collections import Counter
from gensim import corpora, models
import re
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import DATA_RESULTS_DIR,FONT_PATH, STOP_WORDS_PATH


plt.rcParams['font.sans-serif'] = ['SimHei']  # 用黑体显示中文
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题

def _load_stopwords():
    stopwords = set()
    if os.path.exists(STOP_WORDS_PATH):
        with open(STOP_WORDS_PATH, 'r', encoding='utf-8') as f:
            for line in f:
                stopwords.add(line.strip())
        print(f"已加载停用词表，共 {len(stopwords)} 个词")
    else:
        print(f"警告：未找到停用词文件 {STOP_WORDS_PATH}，将不进行过滤")
    return stopwords


def analyze_sentiment(file_path):
    print(f"正在进行情感分析: {os.path.basename(file_path)}")
    df = pd.read_excel(file_path)

    # 定义简单的情感计算函数
    def get_sentiment(text):
        if not isinstance(text, str) or not text:
            return 0.5
        return SnowNLP(text).sentiments

    # 计算情感得分
    df['sentiment'] = df['弹幕内容'].astype(str).apply(get_sentiment)

    # --- 绘图 1: 直方图 ---
    plt.figure(figsize=(10, 6))
    sns.histplot(df['sentiment'], bins=20, kde=True, color='skyblue')
    plt.title('弹幕情感倾向分布 (0=消极, 1=积极)')
    plt.xlabel('情感得分')
    plt.ylabel('数量')

    # 保存图片
    hist_path = os.path.join(DATA_RESULTS_DIR, 'sentiment_hist.png')
    plt.savefig(hist_path)
    plt.close()  # 关闭画布，释放内存
    print(f"   -> 直方图已保存: {hist_path}")

    # --- 绘图 2: 饼图 ---
    plt.figure(figsize=(8, 8))
    pos_count = len(df[df['sentiment'] > 0.5])
    neg_count = len(df[df['sentiment'] <= 0.5])

    plt.pie([pos_count, neg_count],
            labels=['积极', '消极'],
            colors=['lightcoral', 'lightskyblue'],
            autopct='%1.1f%%',
            startangle=140)
    plt.title('弹幕情感占比')

    # 保存图片
    pie_path = os.path.join(DATA_RESULTS_DIR, 'sentiment_pie.png')
    plt.savefig(pie_path)
    plt.close()
    print(f"   -> 饼图已保存: {pie_path}")

    # 打印平均值
    avg = df['sentiment'].mean()
    print(f"   -> 平均情感得分: {avg:.4f}")


def generate_wordcloud(file_path):
    print(f" 正在生成词云...")
    df = pd.read_excel(file_path)
    stopwords = _load_stopwords()

    text_corpus = ' '.join(df['弹幕内容'].astype(str))
    seg_generator = jieba.cut(text_corpus, cut_all=False)

    # 过滤停用词和单字
    seg_list = [w for w in seg_generator if len(w) > 1 and w not in stopwords]
    seg_str = ' '.join(seg_list)

    if not seg_str:
        print(" 有效词汇不足，无法生成词云")
        return

    # 生成对象
    wc = WordCloud(
        width=1000, height=600,
        background_color='white',
        font_path=FONT_PATH,  # 从 config 读入的字体路径
        collocations=False
    ).generate(seg_str)

    # 保存图片
    wc_path = os.path.join(DATA_RESULTS_DIR, 'wordcloud.png')
    wc.to_file(wc_path)
    print(f"   -> 词云图已保存: {wc_path}")


def count_keywords(file_path, top_n=10):
    print(f" 正在统计 Top {top_n} 热词...")
    df = pd.read_excel(file_path)
    stopwords = _load_stopwords()

    text_corpus = ' '.join(df['弹幕内容'].astype(str))
    words = jieba.cut(text_corpus, cut_all=False)

    # 过滤
    filtered_words = [w for w in words if len(w) > 1 and w not in stopwords]

    # 计数
    counter = Counter(filtered_words)
    common_words = counter.most_common(top_n)

    print("-" * 30)
    print("热词排行榜 ")
    for i, (word, count) in enumerate(common_words, 1):
        print(f"Top {i}: {word} ({count}次)")
    print("-" * 30)


def analyze_topics(file_path, num_topics=3, num_words=5):
    """
    功能4：LDA 主题模型分析 (进阶挖掘)
    :param num_topics: 你想把弹幕分成几类？(默认3类)
    :param num_words: 每个主题显示几个关键词？
    """
    print(f" 正在进行 LDA 主题模型分析 (挖掘深层话题)...")
    df = pd.read_excel(file_path)
    stopwords = _load_stopwords()

    # 1. 预处理：再次分词，准备喂给模型
    # 我们需要一个 List of List 格式：[['视频', '好看'], ['剧情', '离谱'], ...]
    docs = []
    for content in df['弹幕内容'].astype(str):
        words = jieba.cut(content)
        # 过滤停用词、短词、纯数字
        filtered_words = [w for w in words if len(w) > 1 and w not in stopwords and not w.isdigit()]
        if filtered_words:
            docs.append(filtered_words)

    if not docs:
        print("⚠️ 有效词汇不足，无法进行 LDA 分析")
        return

    # 2. 构建词典 (给每个词编个号)
    dictionary = corpora.Dictionary(docs)

    # 3. 构建语料库 (把文本变成向量)
    corpus = [dictionary.doc2bow(text) for text in docs]

    # 4. 训练 LDA 模型
    # passes=10 表示模型把数据反复看10遍，学的更准
    lda_model = models.LdaModel(corpus, num_topics=num_topics, id2word=dictionary, passes=10)

    # 5. 输出结果 & 可视化
    print("-" * 30)
    print(f"🔥 AI 发现的 {num_topics} 个潜在讨论主题 🔥")

    topic_data = []

    for topic_id, topic in lda_model.print_topics(num_words=num_words):
        # topic 格式长这样: '0.050*"剧情" + 0.030*"特效" ...'
        # 我们用正则提取出中文词，方便展示
        words = re.findall(r'"(.*?)"', topic)
        topic_name = f"主题 {topic_id + 1}: {', '.join(words)}"
        print(topic_name)

        # 存下来画图用
        # 简单起见，我们假设每个主题权重均等，或者你可以后续深入挖掘每个文档的主题分布
        topic_data.append({'Topic': f"Topic {topic_id + 1}", 'Keywords': '\n'.join(words)})

    print("-" * 30)

    # --- 绘图：虽然 LDA 主要是看词，但我们可以画个简单的关键词展示图 ---
    # 这里我们做一个简单的文本图保存
    plt.figure(figsize=(10, 6))
    plt.axis('off')  # 不显示坐标轴
    plt.title(f'LDA 模型挖掘出的 {num_topics} 大主题', fontsize=16)

    # 在画布上写字
    for idx, data in enumerate(topic_data):
        plt.text(0.1, 0.8 - idx * 0.2,
                 f"{data['Topic']} (核心词):",
                 fontsize=14, fontweight='bold', color='darkblue')
        plt.text(0.15, 0.75 - idx * 0.2,
                 data['Keywords'].replace('\n', ', '),
                 fontsize=12, color='dimgray')

    lda_path = os.path.join(DATA_RESULTS_DIR, 'lda_topics.png')
    plt.savefig(lda_path)
    plt.close()
    print(f"   -> 主题分析图已保存: {lda_path}")