'''
此為使用Selenium自動化爬取Instagram網紅資訊的爬蟲程式碼
其中要讀取的csv檔為從其他網站爬下來的資訊
詳見"網紅配方"的爬蟲程式碼
此篇從個人的主頁面爬下名字、帳號、有無驗證、總貼文數、粉絲數、追蹤人數、自我介紹、前12篇貼文連結
'''
'''
This is a web scraping code using Selenium for automating the extraction of information about Instagram influencers.
The CSV file to be read contains information scraped from another website.
Please refer to the web scraping code for "網紅配方" for more details.
This script is designed to scrape information from an individual's profile page, including their name, account username, verification status, total number of posts, number of followers, following count, self-introduction, links to the latest 12 posts.
'''


from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup as bs
from time import sleep
import os
import csv
import random
import requests
username = '123@gmail.com'  # type loggin username
pwd = '123'  # type loggin passwd

# 創建存放csv的資料夾
save_dir = './IG_info'
if not os.path.exists(save_dir):
    print(f"保存數據的目錄 {save_dir} 不存在，已創建 {save_dir}")
    os.makedirs(save_dir)
else:
    print("KOL_info 目錄已存在，將開始爬蟲")

# 創建抓圖片的資料夾
pic_save_dir = './IG_img'
if not os.path.exists(pic_save_dir):
    print(f"保存數據的目錄 {pic_save_dir} 不存在，已創建 {pic_save_dir}")
    os.makedirs(pic_save_dir)
else:
    print("IG_img 目錄已存在，將開始爬蟲")

# 配置Chrome WebDriver
my_options = webdriver.ChromeOptions()
my_options.add_argument("--start-maximized")
my_options.add_argument("--incognito")
my_options.add_argument("--disable-popup-blocking")
my_options.add_argument("--disable-notifications")
my_options.add_argument("--lang=zh-TW")

# 初始化Chrome WebDriver
driver = webdriver.Chrome(options=my_options)
# 存放所有的List
ig_names = []
ig_accounts = []
ig_checks = []
ig_posts = []
ig_fans = []
ig_follows = []
ig_introductions = []
ig_links_1 = []
ig_links_2 = []
ig_links_3 = []
ig_links_4 = []
ig_links_5 = []
ig_links_6 = []
ig_links_7 = []
ig_links_8 = []
ig_links_9 = []
ig_links_10 = []
ig_links_11 = []
ig_links_12 = []
ig_pics_1 = []
ig_pics_2 = []
ig_pics_3 = []
ig_pics_4 = []
ig_pics_5 = []
ig_pics_6 = []
ig_pics_7 = []
ig_pics_8 = []
ig_pics_9 = []
ig_pics_10 = []
ig_pics_11 = []
ig_pics_12 = []


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


def crawl():
    # 讀取URL列表
    file_path = "./KOL詳細資料_XXK-XXK.csv"  # 這裡修改為指定檔案
    urls = []

    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # 跳過標題行
            for row in reader:
                url = row[4]
                urls.append(url)
    except Exception as e:
        print(f"讀取URL文件時發生錯誤: {e}")

    # 打開CSV文件以追加模式
    csv_file_path = os.path.join(save_dir, f"IG主頁資訊_5K-10K.csv")
    with open(csv_file_path, 'a', newline='', encoding='utf-8-sig') as csvfile:
        fieldnames = ['KOL名字', 'IG帳號', '有無驗證', '總貼文數', '粉絲數', '追蹤人數', '自介', '第1篇貼文', '檔名1', '第2篇貼文', '檔名2', '第3篇貼文', '檔名3', '第4篇貼文', '檔名4',
                      '第5篇貼文', '檔名5', '第6篇貼文', '檔名6', '第7篇貼文', '檔名7', '第8篇貼文', '檔名8', '第9篇貼文', '檔名9', '第10篇貼文', '檔名10', '第11篇貼文', '檔名11', '第12篇貼文', '檔名12']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for url in urls:
            try:
                driver.get(url)
                # 生成介於15-30秒之間的隨機數
                delay = random.randint(60, 90)
                sleep(delay)
                soup = bs(driver.page_source, "lxml")
                # 所有soup要select的位置
                name_scrap = soup.select('div.x7a106z.x972fbf.xcfux6l.x1qhh985.xm0m39n.x9f619.x78zum5.xdt5ytf.x2lah0s.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1n2onr6.x11njtxf.xwonja6.x1dyjupv.x1onnzdu.xwrz0qm.xgmu61r.x1nbz2ho.xbjc6do span.x1lliihq.x1plvlek.xryxfnj.x1n2onr6.x193iq5w.xeuugli.x1fj9vlw.x13faqbe.x1vvkbs.x1s928wv.xhkezso.x1gmr53x.x1cpjm7i.x1fgarty.x1943h6x.x1i0vuye.xvs91rp.x1s688f.x5n08af.x10wh9bi.x1wdrske.x8viiok.x18hxmgj')
                accout_scrap = soup.select(
                    'div.x6s0dn4.x78zum5.x1q0g3np.xs83m0k.xeuugli.x1n2onr6 h2.x1lliihq.x1plvlek')
                check_scrap = soup.select(
                    'div.x9f619.xjbqb8w.x78zum5.x168nmei.x13lgxp2.x5pf9jr.xo71vjh.x1gslohp.x1i64zmx.x1n2onr6.x1plvlek.xryxfnj.x1c4vz4f.x2lah0s.xdt5ytf.xqjyukv.x1qjc9v5.x1oa3qoh.x1nhvcw1 svg.x1lliihq.x1n2onr6')
                post_scrap = soup.select(
                    'span._ac2a span.html-span.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x1hl2dhg.x16tdsg8.x1vvkbs')
                introduction_scrap = soup.select(
                    'h1._aacl._aaco._aacu._aacx._aad6._aade')
                link_scrap = soup.select(
                    'div._aabd._aa8k._al3l a.x1i10hfl.xjbqb8w.x6umtig.x1b1mbwd.xaqea5y.xav7gou.x9f619.x1ypdohk.xt0psk2.xe8uvvx.xdj266r.x11i5rnm.xat24cr.x1mh8g0r.xexx8yu.x4uap5.x18d9i69.xkhd6sd.x16tdsg8.x1hl2dhg.xggy1nq.x1a2a7pz._a6hd')
                img_scrap = soup.select(
                    'div._aabd._aa8k._al3l img.x5yr21d.xu96u03.x10l6tqk.x13vifvy.x87ps6o.xh8yej3')[:12]

                # 獲取帳號
                if accout_scrap:
                    ig_account = [
                        account_element.text for account_element in accout_scrap]
                    ig_accounts.append(', '.join(ig_account))
                else:
                    ig_accounts.append("None")

                # 獲取名字
                if name_scrap:
                    ig_name = [
                        name_element.text for name_element in name_scrap]
                    ig_names.append(', '.join(ig_name))
                else:
                    ig_names.append(', '.join(ig_account))

                # 確認有沒有官方認證，有驗證=1，沒驗證=0
                if check_scrap:
                    ig_checks.append("1")
                else:
                    ig_checks.append("0")

                # 獲取總貼文數
                if len(post_scrap) >= 3:
                    post_element = post_scrap[0]
                    try:
                        post_text = post_element.text
                        if "萬" in post_element:
                            post_text = post_text.replace("萬", "").strip()
                            value = float(post_text) * 10000
                            ig_posts.append(str(int(value)))
                        else:
                            ig_posts.append(post_text)
                    except ValueError:
                        ig_posts.append("0")

                # 獲取粉絲數
                if len(post_scrap) >= 3:
                    fan_element = post_scrap[1]
                    try:
                        fan_text = fan_element.text
                        if "萬" in fan_text:
                            fan_text = fan_text.replace(
                                "萬", "").strip()  # 去掉 "萬" 並去除空格
                            value = float(fan_text) * 10000
                            ig_fans.append(str(int(value)))
                        else:
                            ig_fans.append(fan_text)
                    except Exception as e:
                        print(f"錯誤: {e}")

                # 獲取追蹤數
                if len(post_scrap) >= 3:
                    follow_element = post_scrap[2]
                    try:
                        value = int(float(follow_element.text))
                        if "萬" in follow_element.text:
                            value *= 10000
                        ig_follows.append(str(value))
                    except ValueError:
                        ig_follows.append("0")

                # 獲取自介
                if introduction_scrap:
                    ig_introduction = [
                        introduction_element.text for introduction_element in introduction_scrap]
                    ig_introductions.append(', '.join(ig_introduction))
                else:
                    ig_introductions.append("None")

                # 獲取貼文連結(1-12)
                ig_links = []
                if len(link_scrap) >= 12:
                    for i in range(1, 13):
                        ig_link = link_scrap[i - 1].get('href')
                        full_url = "https://www.instagram.com" + ig_link
                        ig_links.append(full_url)
                # 分散包裝12篇貼文
                ig_links_lists = [ig_links_1, ig_links_2, ig_links_3, ig_links_4, ig_links_5,
                                  ig_links_6, ig_links_7, ig_links_8, ig_links_9, ig_links_10, ig_links_11, ig_links_12]
                for i in range(12):
                    ig_links_lists[i].append(ig_links[i])

                # 下載圖片
                ig_pics = []
                for index, (img_tag, post_link) in enumerate(zip(img_scrap, ig_links)):
                    img_url = img_tag['src']

                    # 使用分別抓取的網址來命名每個圖像
                    unique_identifier = post_link.split("/")[-2]
                    img_name = f'{unique_identifier}.jpg'

                    img_path = os.path.join(pic_save_dir, img_name)

                    try:
                        # 下載圖片
                        response = requests.get(img_url)
                        with open(img_path, 'wb') as img_file:
                            img_file.write(response.content)
                    except Exception as e:
                        print(f"下載圖片時發生錯誤：{str(e)}")

                    ig_pics.append(unique_identifier)
                # 分散包裝12篇貼文的圖檔名
                ig_pics_lists = [ig_pics_1, ig_pics_2, ig_pics_3, ig_pics_4, ig_pics_5,
                                 ig_pics_6, ig_pics_7, ig_pics_8, ig_pics_9, ig_pics_10, ig_pics_11, ig_pics_12]
                for i in range(12):
                    ig_pics_lists[i].append(ig_pics[i])

                # 寫入CSV文件
                writer.writerow({'KOL名字': ig_names[-1], 'IG帳號': ig_accounts[-1], '有無驗證': ig_checks[-1], '總貼文數': ig_posts[-1], '粉絲數': ig_fans[-1], '追蹤人數': ig_follows[-1], '自介': ig_introductions[-1], '第1篇貼文': ig_links_1[-1], '檔名1': ig_pics_1[-1], '第2篇貼文': ig_links_2[-1], '檔名2': ig_pics_2[-1], '第3篇貼文': ig_links_3[-1], '檔名3': ig_pics_3[-1], '第4篇貼文': ig_links_4[-1], '檔名4': ig_pics_4[-1],
                                '第5篇貼文': ig_links_5[-1], '檔名5': ig_pics_5[-1], '第6篇貼文': ig_links_6[-1], '檔名6': ig_pics_6[-1], '第7篇貼文': ig_links_7[-1], '檔名7': ig_pics_7[-1], '第8篇貼文': ig_links_8[-1], '檔名8': ig_pics_8[-1], '第9篇貼文': ig_links_9[-1], '檔名9': ig_pics_9[-1], '第10篇貼文': ig_links_10[-1], '檔名10': ig_pics_10[-1], '第11篇貼文': ig_links_11[-1], '檔名11': ig_pics_11[-1], '第12篇貼文': ig_links_12[-1], '檔名12': ig_pics_12[-1]})

                print(f"已完成 {len(ig_names)} 條記錄")

            except Exception as e:
                # 發生異常時記錄錯誤信息
                driver.get(url)
                soup = bs(driver.page_source, "lxml")
                accout_scrap = soup.select(
                    'div.x6s0dn4.x78zum5.x1q0g3np.xs83m0k.xeuugli.x1n2onr6 h2.x1lliihq.x1plvlek')
                # 獲取帳號
                if accout_scrap:
                    ig_account = [
                        account_element.text for account_element in accout_scrap]
                    ig_accounts.append(', '.join(ig_account))
                print(f"{ig_account}頁面出問題，請於error裡面確認")
                with open("./IG_info/error_log_5K-10K.csv", "a", newline='', encoding='utf-8-sig') as error_log_file:
                    error_log_writer = csv.writer(error_log_file)
                    error_log_writer.writerow([url, str(e)])
                continue  # 繼續處理下一個URL

    print("爬蟲已完成")
    print(f"CSV文件儲存成功，腳本已結束")


if __name__ == "__main__":
    visit()
    loggin()
    crawl()
