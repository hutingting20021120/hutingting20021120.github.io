"""
@filename:crawl_gpt.py
@author:Hu Tingting
@time:2024-05-29

"""
'''
爬取某个视频评论区数据
封装为了函数，只需在末尾主体部分修改视频url、cookie文件储存地址和csv文件输出地址
爬取n个视频则需运行n次，最后得到n个csv文件（后续再合并处理）

'''

from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
import time
import csv
import json
from tqdm import tqdm

def crawl_comments(video_url, cookies_file_path, output_file_path):
    # 启动 Chrome 服务
    chrome_path = r'C:\Program Files\Python312\Scripts\chromedriver.exe'  # chromedriver 路径
    chrome_service = Service(chrome_path)
    chrome_service.start()

    driver = webdriver.Chrome(service=chrome_service)

    try:
        # 先建立连接, 随后才可以可修改cookie
        driver.get(video_url)
        driver.maximize_window()

        # 删除这次登录时，浏览器自动储存到本地的cookie
        driver.delete_all_cookies()

        # 读取之前已经储存到本地的cookie
        with open(cookies_file_path, 'r', encoding='utf-8') as cookies_file:
            cookies_list = json.load(cookies_file)

        # 把cookie添加到本次连接
        for cookie in cookies_list:
            driver.add_cookie(cookie)

        # 再次访问网站，由于cookie的作用，从而实现免登陆访问
        driver.get(video_url)
        input("登录成功后回车")   # 登录较慢，选择手动等待

        # 生成表格
        with open(output_file_path, 'w', newline='', encoding='utf-8-sig') as csvfile:
            fieldnames = ['用户名', '时间', '内容', '点赞量']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()

            print("开始处理滑动页面")
            # 定义一个变量，用于记录上一次页面评论数，以便判断是否加载了新的评论
            last_comments_count = 0
            # 定义一个循环，直到没有新的评论加载为止
            while True:
                # 执行JavaScript将页面滚动到底部
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)  # 等待页面加载
                # 获取当前页面所有评论
                comments = driver.find_elements(By.CSS_SELECTOR, 'div.reply-item')
                # 如果当前评论数和上一次相同，说明没有新的评论加载了，可以退出循环
                if len(comments) == last_comments_count:
                    break
                # 更新上一次评论数为当前评论数
                last_comments_count = len(comments)

            # 处理主评论
            print('开始处理评论')

            comments = driver.find_elements(By.CSS_SELECTOR, 'div.reply-item')
            # 开启进度条
            pbar = tqdm(total=len(comments), desc="爬取评论")

            for comment in comments:
                user_name = comment.find_element(By.CSS_SELECTOR, 'div.user-name').text.strip()
                reply_time = comment.find_element(By.CSS_SELECTOR, 'span.reply-time').text.strip()
                root_reply = comment.find_element(By.CSS_SELECTOR, 'div.root-reply')
                info = root_reply.find_element(By.CSS_SELECTOR, 'span.reply-content').text.strip()
                likes = comment.find_element(By.CSS_SELECTOR, 'span.reply-like').text.strip() or 0

                writer.writerow({'用户名': user_name, '时间': reply_time, '内容': info, '点赞量': likes})
                pbar.update(1)

                # 检查是否有子评论
                try:
                    sub_user_container = comment.find_element(By.CSS_SELECTOR, 'div.sub-reply-container')
                except NoSuchElementException:
                    sub_user_container = None

                if sub_user_container:
                    # 检查是否有折叠的子评论
                    try:
                        view_more_btn = comment.find_element(By.CSS_SELECTOR, 'span.view-more-btn')
                        if not view_more_btn.is_displayed():
                            # 滚动页面使按钮可见
                            driver.execute_script("arguments[0].scrollIntoView();", view_more_btn)
                        # 使用 ActionChains 模拟鼠标点击
                        action = ActionChains(driver)
                        action.move_to_element(view_more_btn).click().perform()
                        time.sleep(2)  # 等待回复加载
                    except NoSuchElementException:
                        pass  # 没有折叠的子评论

                    # 处理子评论
                    subcomments = comment.find_elements(By.CSS_SELECTOR, 'div.sub-reply-item')
                    for subcomment in subcomments:
                        sub_id = subcomment.find_element(By.CSS_SELECTOR, 'div.sub-user-name').text.strip()
                        sub_time = subcomment.find_element(By.CSS_SELECTOR, 'span.sub-reply-time').text.strip()
                        sub_info = subcomment.find_element(By.CSS_SELECTOR, 'span.reply-content').text.strip()
                        sub_likes = subcomment.find_element(By.CSS_SELECTOR, 'span.sub-reply-like').text.strip() or 0

                        writer.writerow({'用户名': sub_id, '时间': sub_time, '内容': sub_info, '点赞量': sub_likes})
                        pbar.update(1)

            pbar.close()  # 处理完毕后关闭进度条

    except Exception as e:
        print(f"发生异常: {str(e)}")

    finally:
        driver.quit()  # 关闭浏览器

# 主体部分，调用函数
# 视频链接
video_url = "https://www.bilibili.com/video/BV1b54y127L2/"
# 存储登录状态的 cookie 文件路径
cookies_file_path = './data/my_cookies3.json'
# 输出评论的 CSV 文件路径
output_file_path = './output/comment3.csv'
# 调用爬取评论的函数
crawl_comments(video_url, cookies_file_path, output_file_path)
