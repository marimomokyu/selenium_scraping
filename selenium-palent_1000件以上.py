# coding:utf-8
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from time import sleep
import chromedriver_binary
import requests
from bs4 import BeautifulSoup
import sys
import time
import csv
import pprint

list_urls = [ \
'https://ninteishien.force.com/NSK_CertificationList?prefectures=福岡県#', \
]


#python3.9.6 64bitで実行するとうまくいく
#うまくいかない場合はターミナルから[python3 XXXX.py]で実行
# ブラウザを開く。
driver = webdriver.Chrome()
for list_url in list_urls:
        
    # driver.get("https://ninteishien.force.com/NSK_CertificationList?prefectures=長崎県#") 
    driver.get(list_url) 

    # 最初はポップアップが表示されるのでクリック
    # <a href="#" onclick="isValid(); return false;" class="btn_search">この条件で検索する</a>
    search = driver.find_element_by_class_name('btn_search') 
    search.click()

    # 5秒間待機してみる。
    sleep(4)

    # 場合によっては1000件以上表示されるので判定　
    # <span id="NSK_CertificationList:form:j_id139">検索結果の内、1000件のみを表示しております。</span>
    if len(driver.find_elements_by_id('NSK_CertificationList:form:j_id139')) > 0 :
        # 1000件以上
        isMax = True
        continue
    else:
        # 1000件未満
        isMax = False

    with open('/Users/tsutsumi/csv/親情報_1000件以上.csv', 'a') as f:
        writer_palent = csv.writer(f)
        # ページ数チェック用
        counti = 1
        while True:
            # 紳士的に5秒スリープ
            time.sleep(4)
            # 現在どのページを表示しているのかを求める
            nowViewPage = driver.find_element_by_css_selector(".paginate_btn.active").text
            # もしページ遷移していなかったら終了
            if not nowViewPage == str(counti):
                break
            # テーブル内容取得
            tableElem = driver.find_element_by_class_name("c_table_contents")
            trs = tableElem.find_elements(By.TAG_NAME, "tr")

            # ページ内のリンクをすべて取得
            new_list = driver.find_elements_by_xpath("//a[@href]")
            hrefs_parent =[]
            for x in new_list: 
                if "NSK_CertifiedRecordView" in str(x.get_attribute("href")):
                    hrefs_parent.append(x)

            # ヘッダ行は除いて取得
            for j in range(2,len(trs)):
                tds = trs[j].find_elements(By.TAG_NAME, "td")
                lineDebug = ""
                line = []
                for k in range(0,len(tds)):
                    # if k < len(tds)-1:
                    lineDebug += "%s," % (tds[k].text)
                    line.append(tds[k].text)
                    if k == len(tds)-1:
                        lineDebug += "%s," % (hrefs_parent[j-2].get_attribute("href"))
                        line.append(hrefs_parent[j-2].get_attribute("href"))

                pprint.pprint(lineDebug+"\r\n")
                writer_palent.writerow(line)    
            # 次ページに遷移 1 2 3 4 5 > >> のボタンの中の>ボタンを押下
            # ボタンじゃなくてjsなので直接指定
            try:
                driver.execute_script("javascript:var a=function(){return doPaging('next', true);if(window != window.top){var f = document.getElementById('NSK_CertificationList:form');f.action += (f.action.indexOf('?') == -1 ? '?' : '&');};};var b=function(){if(typeof jsfcljs == 'function'){jsfcljs(document.getElementById('NSK_CertificationList:form'),'NSK_CertificationList:form:j_id160,NSK_CertificationList:form:j_id160','');}return false};return (a()==false) ? false : b();")
            except Exception as e:
                pprint.pprint('=== エラー内容 ===')
                pprint.pprint('type:' + str(type(e)))
                pprint.pprint('args:' + str(e.args))
                pprint.pprint('message:' + e.message)
                pprint.pprint('e自身:' + str(e))
                driver.quit()
            counti = counti + 1


    # ブラウザを終了する。
    # driver.close()