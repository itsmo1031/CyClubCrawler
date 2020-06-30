from urllib.error import HTTPError
from selenium import webdriver
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os
import urllib.request
import requests

clubId =  # Set your club id
folderName =  # Set folder name

session = requests.Session()
session.get('http://club.cyworld.com/club/board/PhotoViewer/index.asp?club_id=%d' % clubId)


def download_file(url, local_filename):
    r = session.get(url, stream=True)
    with open(local_filename, 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024):
            if chunk:
                f.write(chunk)
    return local_filename


driverPath =  # Set driver path

if not os.path.exists(folderName):
    os.mkdir(folderName)

driver = webdriver.Chrome(driverPath)
driver.get("http://club.cyworld.com/club/board/PhotoViewer/index.asp?club_id=52016317")
driver.implicitly_wait(5)
driver.find_element_by_xpath('//*[@id="scroll_box"]/div/div[1]/ul/li[1]/a').click()
driver.implicitly_wait(3)

for i in range(6675):
    try:
        image = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, '//*[@id="imgBigEl"]/a/img'))
        )
    except TimeoutException:
        driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/a[2]').click()
        continue

    src = image.get_attribute('src')
    alt = image.get_attribute('alt')
    alt = alt.replace('?', '')
    alt = alt.replace('<', '(')
    alt = alt.replace('>', ')')
    alt = alt.replace('"', '\'')

    uploadDate = WebDriverWait(driver, 20).until(
        EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/div[2]/div/p'))
    ).text
    uploadDate = uploadDate.replace('-', '')
    split = src.split('%2E')

    src = src.replace('%2E', '.')

    # 확장자 정의
    fileExt = split[1]

    # 파일 이름 설정
    fileName = os.path.join(folderName, uploadDate + ') ' + alt + '.%s' % fileExt)
    fileId = 1

    while os.path.exists(fileName):
        fileName = os.path.join(folderName, uploadDate + ') ' + alt + '-%d.%s' % (fileId, fileExt))
        fileId += 1

    # 파일 저장
    print(download_file(src, fileName))

    # 다음 사진 클릭
    driver.find_element_by_xpath('/html/body/div[1]/div[3]/div[2]/a[2]').click()

driver.close();
