'''
此為使用Selenium自動化爬取Instagram網紅貼文資訊的爬蟲程式碼
需先執行"IG_scrap_csv"從主頁爬取連結，才能從這讀取csv進行爬蟲
此程式碼從貼文連結爬取圖片、帳號、打卡地點、文本內容、文本字數、貼文時間、爬蟲時間、PO文天數、按讚數、留言數、留言內容、該留言按讚數
'''
'''
This is a web scraping code using Selenium to automate the extraction of Instagram influencer post information.
You need to execute "IG_scrap_csv" first to crawl links from the main page before using this to read the CSV file and proceed with web scraping.
This code extracts images, account usernames, check-in locations, text content, text character count, post time, crawling time, days since posting, likes count, comments count, comment content, and the number of likes for each comment from post links.
'''

from selenium import webdriver
from selenium.webdriver.common.by import By
import pyautogui
from bs4 import BeautifulSoup as bs
from time import sleep
import re
import os
import csv
import random
import datetime
username = '123@gmail.com'  # type loggin username
pwd = '123'  # type loggin passwd

# 創建抓貼文資訊的資料夾
post_save_dir = './post_info'
if not os.path.exists(post_save_dir):
    print(f"保存數據的目錄 {post_save_dir} 不存在，已創建 {post_save_dir}")
    os.makedirs(post_save_dir)
else:
    print("post_info 目錄已存在，將開始爬蟲")

# 配置Chrome WebDriver
my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")
my_options.add_argument("--incognito")
my_options.add_argument("--disable-popup-blocking")
my_options.add_argument("--disable-notifications")
my_options.add_argument("--lang=zh-TW")


# 初始化Chrome WebDriver
driver = webdriver.Chrome(options=my_options)

post_accounts = []
post_locals = []
post_contents = []
contents_len = []
post_times = []
current_time = datetime.datetime.now()
crawl_times = []
time_differences = []
post_likes = []
comment_counts = []
all_comments = []
cc_counts = []
cc_want = []
comment_likes = []
foreign_key = []


def visit():
    url = "https://www.instagram.com/"
    driver.get(url)
    sleep(5)


def loggin():
    # 輸入帳密
    account = driver.find_element(
        By.CSS_SELECTOR, 'input[name="username"][value]')
    account.send_keys(username)
    sleep(6)
    password = driver.find_element(
        By.CSS_SELECTOR, 'input[name="password"][value]')
    password.send_keys(pwd)
    sleep(5)
    # 登入
    button = driver.find_element(
        By.CSS_SELECTOR, "button._acan._acap._acas._aj1-")
    button.click()
    sleep(6)


def scroll():
    scroll_count = 6
    for _ in range(scroll_count):
        pyautogui.scroll(-100000)
        sleep(3)


def crawl():
    # 讀取URL列表
    file_path = "./IG主頁資訊_XXXK.csv"  # 這裡修改為指定檔案
    urls = []

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳過標題行
            for row in reader:
                find_url = row[7::2]
                urls.extend(find_url)
    except Exception as e:
        print(f"讀取URL文件時發生錯誤: {e}")

    # 打開CSV文件以追加模式
    csv_file_path = os.path.join(post_save_dir, f"貼文資訊_test.csv")
    fieldnames = ['檔名', '帳號', '打卡地點', '文本內容', '文本字數',
                  '貼文時間', '爬蟲時間', 'PO文天數', '按讚數', '留言數']
    csv_file_path2 = os.path.join(post_save_dir, f"留言資訊_test.csv")
    fieldnames2 = ['檔名', '帳號', '留言內容', '按讚數', '留言數']
    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        with open(csv_file_path2, 'a', newline='', encoding='utf-8-sig') as csvfile2:
            writer2 = csv.DictWriter(csvfile2, fieldnames=fieldnames2)
            writer2.writeheader()

            for url in urls:
                try:
                    post_comments = []
                    driver.get(url)
                    # 生成介於30到60秒之間的隨機數
                    delay = random.randint(30, 60)
                    sleep(delay)
                    soup = bs(driver.page_source, "lxml")

                    account_scrap = soup.select(
                        'span._aacl._aaco._aacw._aacx._aad7._aade')
                    local_scrap = soup.select(
                        'a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz.x5n08af.x9n4tj2._a6hd')
                    content_scrap = soup.select(
                        'span.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.xt0psk2.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')
                    time_scrap = soup.select(
                        'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.x1yxbuor.xo1l8bm.x1roi4f4.x1s3etm8.x676frb.x10wh9bi.x1wdrske.x8viiok.x18hxmgj time._aaqe')
                    like_scrap = soup.select(
                        'span.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.xt0psk2.x1i0vuye.xvs91rp.x1s688f.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj span.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs')
                    count_scrap = soup.find('meta', {'name': 'description'})
                    foreign_scrap = soup.find('meta', {'property': 'og:url'})

                    # 獲取連結建
                    if foreign_scrap:
                        key = foreign_scrap['content']
                        parts = key.split('/')
                        code = parts[-2]
                        foreign_key.append(code)
                    else:
                        foreign_key.append('None')

                    # 獲取帳號
                    if len(account_scrap) >= 1:
                        account_element = account_scrap[0]
                        value = account_element.text
                        post_accounts.append(value)

                    # 獲取打卡地點
                    if local_scrap:
                        post_local = [
                            local_element.text for local_element in local_scrap]
                        post_locals.append(', '.join(post_local))
                    else:
                        post_locals.append('None')

                    # 獲取文本內容
                    if content_scrap:
                        post_content = [
                            content_element.text for content_element in content_scrap]
                        post_contents.append(', '.join(post_content))
                    else:
                        post_contents.append("None")

                    # 獲取文本字數
                    if content_scrap:
                        word_element = content_scrap[0].text
                        word_element = word_element.replace(" ", "").replace(
                            "\n", "").replace("\r", "").replace("\t", "")
                        content_word = len(word_element)
                        contents_len.append(content_word)
                    else:
                        contents_len.append(0)

                    # 獲取貼文時間
                    if time_scrap:
                        time_element = time_scrap[0]
                        post_time_str = time_element['datetime']
                        post_time_str = post_time_str.split('T')[0]
                        post_time = datetime.datetime.fromisoformat(
                            post_time_str)
                        formatted_post_time = post_time.strftime('%Y-%m-%d')
                        post_times.append(formatted_post_time)
                        # 獲取當前時間
                        crawl_time_element = current_time.date()
                        crawl_time = crawl_time_element.strftime('%Y-%m-%d')
                        crawl_times.append(crawl_time)
                        # 獲取時間差
                        for i in range(len(post_times)):
                            time_difference = crawl_time_element - post_time.date()
                        time_differences.append(time_difference.days)

                    # 獲取按讚數
                    if like_scrap:
                        like_text = like_scrap[0].text
                        if "萬" in like_text:
                            like_text = like_text.replace(
                                "萬", "").strip()  # 去掉 "萬" 並去除空格
                            value = float(like_text) * 10000
                            post_likes.append(str(int(value)))
                        else:
                            post_likes.append(like_text)

                    # 獲取留言數
                    if count_scrap:
                        c_key = count_scrap['content']
                        c_parts = c_key.split(' ')
                        c_code = c_parts[2]
                        comment_counts.append(int(c_code))
                    else:
                        comment_counts.append(0)

                    # 滾10次
                    scroll()
                    sleep(5)
                    # 載入元素
                    soup = bs(driver.page_source, "lxml")
                    comment_scrap = soup.select(
                        'span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.xo1l8bm.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')
                    cl_scrap = soup.select(
                        'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1xmf6yo.x1uhb9sk.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.x1q0g3np.xqjyukv.x6s0dn4.x1oa3qoh.x1nhvcw1')
                    elements_raw = soup.select(
                        'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh')

                    # 獲取留言內容
                    if comment_scrap:
                        for i, comment_element in enumerate(comment_scrap):
                            comment_text = comment_element.text
                            # 只将奇数索引的评论追加到post_comments列表
                            if i % 2 == 0 and i != 0:
                                all_comments.append(comment_text)

                    # 獲取留言按讚數
                    for comment in cl_scrap:
                        like_span = comment.find(
                            'span', string=re.compile(r'\d+\s?個讚'))
                        if like_span:
                            like_text = like_span.text
                            like_count = re.search(r'\d+', like_text).group()
                            comment_likes.append(int(like_count))
                        else:
                            like_span = comment.find('span', text="1 個讚")
                            if like_span:
                                comment_likes.append(1)
                            else:
                                comment_likes.append(0)

                    # 獲取該留言中留言數
                    elementa = ['x9f619', 'xjbqb8w', 'x78zum5', 'x168nmei', 'x13lgxp2', 'x5pf9jr', 'xo71vjh', 'x1uhb9sk', 'x1plvlek',
                                'xryxfnj', 'x1iyjqo2', 'x2lwn1j', 'xeuugli', 'xdt5ytf', 'xqjyukv', 'x1qjc9v5', 'x1oa3qoh', 'x1nhvcw1']
                    elementb = ['x9f619', 'xjbqb8w', 'x78zum5', 'x168nmei', 'x13lgxp2', 'x5pf9jr', 'xo71vjh', 'x1uhb9sk', 'x1plvlek',
                                'xryxfnj', 'x1c4vz4f', 'x2lah0s', 'xdt5ytf', 'xqjyukv', 'x1qjc9v5', 'x1oa3qoh', 'x1nhvcw1', 'x540dpk']

                    for i in range(len(elements_raw)):
                        current_class = elements_raw[i].get('class')
                        if current_class == elementa or current_class == elementb:
                            cc_want.append(elements_raw[i])

                    cc_want.pop(0)  # 去掉貼文的

                    for i in range(len(cc_want)):
                        if cc_want[i].get('class') == elementb:
                            text = cc_want[i].text
                            numeric_part = re.sub(r'[^0-9]', '', text)
                            cc_counts.append(int(numeric_part))
                        elif i < len(cc_want) - 1 and cc_want[i].get('class') == cc_want[i+1].get('class') == elementa:
                            cc_counts.append('0')

                    # 寫入貼文資訊CSV
                    writer.writerow({'檔名': foreign_key[-1], '帳號': post_accounts[-1], '打卡地點': post_locals[-1], '文本內容': post_contents[-1], '文本字數': contents_len[-1],
                                    '貼文時間': post_times[-1], '爬蟲時間': crawl_times[-1], 'PO文天數': time_differences[-1], '按讚數': post_likes[-1], '留言數': comment_counts[-1]})
                    print(f"已完成第 {len(post_accounts)} 篇貼文資訊")

                    # 寫入留言資訊CSV
                    for alcomment, like, c_count in zip(all_comments, comment_likes, cc_counts):
                        writer2.writerow(
                            {'檔名': foreign_key[-1], '帳號': post_accounts[-1], '留言內容': alcomment, '按讚數': like, '留言數': c_count})
                    print(f"已完成第 {len(foreign_key)} 篇貼文的留言資訊")

                except Exception as e:
                    # 發生異常時記錄錯誤信息
                    print(f"發生異常，請至error.csv中確認")
                    with open("./post_info/error_log_XXK-XXK.csv", "a", newline='', encoding='utf-8-sig') as error_log_file:  # 需修改儲存路徑
                        error_log_writer = csv.writer(error_log_file)
                        error_log_writer.writerow([url, str(e)])
                    continue  # 繼續處理下一個URL

    print("爬蟲已完成")
    print(f"CSV文件儲存成功，腳本已結束")


if __name__ == "__main__":
    visit()
    loggin()
    crawl()
