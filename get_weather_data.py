import datetime
from datetime import datetime,timedelta
import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os

def GetData(website: str, savepath: str):
 
    browser.get(website)

    print("--> Waiting for web page response...")
    # 需要等一下，直到带有aria-label属性且值为table of contents的表格加载完成
    wait = WebDriverWait(browser, 30)
    #try:
    wait.until(EC.presence_of_element_located((By.XPATH, "//table[@aria-label='table of contents']")))
    sleep(2)
    """ except:
        print('Warning: Timeout!\n--> Reopening the web page...')
        GetData(website, savepath) """
    
    print("--> Fetching web page data...")
    soup = BeautifulSoup(browser.page_source, "lxml")
    
    dh = soup.find_all("table",attrs={"aria-label":"table of contents"})
    data_colhead = dh[0].find_all('button')     # 表头
    data_rows = dh[0].find_all('span')          # 表内容

    # 得到表数据
    print("--> Extracting web page data...")
    datalist = []
    for i in data_rows:
        if i.string != None:
            datalist.append(i.string)
            
    final = []
    temp = []
    count = 0
    for i in datalist:
        if count < 17:
            temp.append(i)
            count += 1
        else:
            final.append(temp)
            count = 1
            temp = []
            temp.append(i)
    final.append(temp)
            
    datalist = final

    new_block = []
    final = []
    for i in datalist:
        new_block.append(i[0])
        new_block.append(i[1]+i[2])
        new_block.append(i[3]+i[4])
        new_block.append(i[5]+i[6])
        new_block.append(i[7])
        new_block.append(i[8]+i[9])
        new_block.append(i[10]+i[11])
        new_block.append(i[12]+i[13])
        new_block.append(i[14]+i[15])
        new_block.append(i[16])
        final.append(new_block)
        new_block = []
        
    datalist = final

    table = pd.DataFrame(datalist)
    table.columns = [c.text for c in data_colhead]

    table.to_csv(path_or_buf=savepath)
    print("--> Data extraction completed！！")

def datelist(start: str,end: str) -> list:
    date_list = [] 
    begin_date = datetime.strptime(start, r"%Y-%m-%d") 
    end_date = datetime.strptime(end,r"%Y-%m-%d") 
    while begin_date <= end_date: 
        year = str(int(begin_date.strftime('%Y')))
        month = str(int(begin_date.strftime('%m')))
        day = str(int(begin_date.strftime('%d')))
        date_str = year+'-'+month+'-'+day
        date_list.append(year+'-'+month+'-'+day) 
        # 日期加法days=1 months=1等等
        begin_date += timedelta(days=1) 
    return date_list

if __name__ == '__main__':

    from tqdm import tqdm
    savepath = '../RawDatas/weather_data/'
    a = tqdm(datelist('2015-8-1', '2020-3-1'))

    # 打开chrome浏览器（需提前安装好chromedriver）
    chrome_options=Options()
    chrome_options.add_argument('--headless --ignore-certificate-errors')           # 无界面浏览
    browser = webdriver.Chrome(options=chrome_options)
    # browser = webdriver.PhantomJS()
    print("--> Opening the web page...")

    for i in a:
        if os.path.exists(savepath + i + '.csv'):
            print (i + '.csv has already existed, continue...')
            continue
        GetData("https://www.wunderground.com/history/daily/cn/shanghai/ZSSS/date/" + i, savepath + i + '.csv')

    browser.close()