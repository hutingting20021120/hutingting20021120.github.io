"""
@filename:get_cookie.py
@author:Hu Tingting
@time:2024-04-25

"""

'''
配合手工操作登录网站，获取cookies，保存到本地，以备后续使用
'''
import json
from selenium import webdriver
from selenium.webdriver.chrome.options import Options #用于设置浏览器启动的一些参数
import time

options = Options()
browser = webdriver.Chrome(options=options)
# 【手动修改】输入bilibili某个视频网址，注意不是bilibili首页网址，截止到/BVXXXXXXX/
browser.get('https://www.bilibili.com/video/BV1b54y127L2/')
browser.maximize_window()

input("请登录，然后按回车……")  # 等待用手机扫码登录, 登录后回车即可

cookies_dict = browser.get_cookies()
cookies_json = json.dumps(cookies_dict)

# 登录完成后,将cookies保存到本地文件
# 【手动修改】文件名，可以分别命名为my_cookies1/2/3
out_filename = './data/my_cookies3.json'
out_file = open(out_filename, 'w', encoding='utf-8')
out_file.write(cookies_json)
out_file.close()
print('Cookies文件已写入：' + out_filename)

time.sleep(5)
browser.quit()