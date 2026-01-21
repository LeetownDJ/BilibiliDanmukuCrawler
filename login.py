import json
import time
from playwright.sync_api import sync_playwright

# Cookie 保存的文件名
COOKIE_FILE = 'cookie.json'

def get_cookie():

    with sync_playwright() as p:
        # 启动浏览器 (headless=False 表示显示界面)
        browser = p.chromium.launch(headless=False)
        context = browser.new_context()
        page = context.new_page()

        print("正在打开 Bilibili 登录页...")
        page.goto("https://passport.bilibili.com/login")

        print("\n 请在弹出的浏览器中扫码登录！")

        # === 核心修改：改为检测 Cookie 字段 ===
        start_time = time.time()
        while True:
            # 获取当前所有 Cookies
            cookies = context.cookies()
            # 提取所有 Cookie 的名字
            cookie_names = [c['name'] for c in cookies]
            # 只要发现了'SESSDATA'，就说明登录成功了
            if "SESSDATA" in cookie_names:
                print("\n 登录成功！")
                break
            # 超时机制 (防止无限死循环)
            if time.time() - start_time > 120:  # 120秒超时
                print(" 登录超时，程序退出。请重新运行。")
                browser.close()
                return
            time.sleep(1)


        # 整理并保存 Cookie
        cookie_dict = {item['name']: item['value'] for item in cookies}
        with open(COOKIE_FILE, 'w', encoding='utf-8') as f:
            json.dump(cookie_dict, f)
        print(f"\n Cookie 已成功保存至 {COOKIE_FILE}")
        time.sleep(2)
        browser.close()

if __name__ == '__main__':
    get_cookie()