import os
import json

# ================= 基础路径配置 =================
# 项目根目录
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# 数据存储路径
DATA_RAW_DIR = os.path.join(BASE_DIR, 'data', 'raw')
DATA_PROCESSED_DIR = os.path.join(BASE_DIR, 'data', 'processed')
DATA_RESULTS_DIR = os.path.join(BASE_DIR, 'data', 'results')
RESOURCE_DIR = os.path.join(BASE_DIR, 'data', 'resources')
LOG_DIR = os.path.join(BASE_DIR, 'data', 'logs')

# 自动创建所有必要的目录
for path in [DATA_RAW_DIR, DATA_PROCESSED_DIR, LOG_DIR, DATA_RESULTS_DIR]:
    os.makedirs(path, exist_ok=True)

# ================= 资源配置 =================
# 字体路径 (Windows默认黑体)
FONT_PATH = r'C:\Windows\Fonts\simhei.ttf'
# 停用词路径
STOP_WORDS_PATH = os.path.join(RESOURCE_DIR, 'stopwords.txt')

# ================= 爬虫参数配置 =================
TARGET_OID = '247962216'      # 视频 CID
START_DATE = '2023-12-01'     # 开始日期
END_DATE   = '2023-12-25'     # 结束日期

# === Cookie 自动加载逻辑 ===
COOKIE_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'cookie.json')

def load_cookie():
    if os.path.exists(COOKIE_FILE):
        try:
            with open(COOKIE_FILE, 'r', encoding='utf-8') as f:
                cookie_dict = json.load(f)
                cookie_str = "; ".join([f"{k}={v}" for k, v in cookie_dict.items()])
                return cookie_str
        except Exception as e:
            print(f" Cookie 文件读取失败: {e}")
            return ""
    else:
        return ""

# 获取动态 Cookie
MY_COOKIE = load_cookie()

if not MY_COOKIE:
    print(" 警告：未找到本地 Cookie 文件，请先运行 'python login.py' 进行扫码登录！")
    MY_COOKIE = "你的备用手动Cookie(可选)"

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
    'Cookie': MY_COOKIE,
    'Referer': 'https://www.bilibili.com/'
}
