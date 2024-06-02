"""
@filename:use_cookie.py
@author:Hu Tingting
@time:2024-04-25

"""
'''
用于验证上一步获取的cookies是否能成功登录页面
'''
import time
import json  # 导入json模块
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

options = Options()
browser = webdriver.Chrome(options=options)

# 先建立连接, 随后才可以可修改cookie
browser.get('https://www.bilibili.com/video/BV1b54y127L2/')
browser.maximize_window()
# 删除这次登录时，浏览器自动储存到本地的cookie
browser.delete_all_cookies()

# 读取之前已经储存到本地的cookie
cookies_filename = './data/my_cookies3.json'
cookies_file = open(cookies_filename, 'r', encoding='utf-8')
cookies_list = json.loads(cookies_file.read())
print(cookies_list)

for cookie in cookies_list:  # 把cookie添加到本次连接
    browser.add_cookie(cookie)

# 再次访问网站，由于cookie的作用，从而实现免登陆访问
browser.get("https://www.bilibili.com/video/BV1YT4y1H7Fq/")
time.sleep(3)

# 将页面保存为图片，便于查看是否登录成功
browser.save_screenshot("./output/bilibili_login1.png")



time.sleep(6)
browser.quit()
