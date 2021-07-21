#!/usr/bin/env python
# coding: utf-8

from pytube import YouTube
from bs4 import BeautifulSoup
from selenium.webdriver import Chrome, ChromeOptions
import time
import os
import warnings
import glob

warnings.filterwarnings(action='ignore')


# get_driver - 드라이버 가져오기
def get_driver():
    options = ChromeOptions()
    options.add_argument('headless') #창이 뜨지 않게 처리
    options.add_argument('disable-gpu') #gpu 비활성화
    # options.add_argument(
    #     'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
    driver = Chrome(options=options)
    return driver


# search - 검색 결과 page source 리턴
def search(keyword):
    driver = get_driver()

    url = 'https://www.youtube.com/results?search_query=' + keyword
    driver.get(url)

    # last_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    #
    # pages = 10
    # for i in range(pages):  # 스크롤 100번까지로 제한
    #     driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")
    #
    #     # time.sleep(3)
    #
    #     new_page_height = driver.execute_script("return document.documentElement.scrollHeight")
    #
    #     if new_page_height*i > last_page_height:
    #         break
    #
    #     last_page_height = new_page_height

    dom = BeautifulSoup(driver.page_source, 'lxml')
    return dom


# get_url - 검색 결과창의 모든 동영상 url 받아오기
def get_url(keyword):
    dom = search(keyword)
    href = [a.attrs['href'] for a in dom.select('a#video-title')]
    url = ['https://www.youtube.com' + h for h in href]
    return url


# chk_cap - 한국어 자막 유무 체크 (없으면 None 리턴)
def chk_cap(yt):
    lang = 'ko'
    yt_cap = yt.captions.get_by_language_code(lang)
    return yt_cap

# get_data - pytube 라이브러리를 사용하여 오디오, 자막 파일 받아오기
def get_data():
    # 경로 설정
    audio_path = './audio_data/'
    cap_path = './caption/'
    url = get_url()
    url = list(set(url)) # 중복 제거
    for _ in url:
        try:
            yt = YouTube(_)
            if chk_cap(yt) != None and yt.length < 1200: # 한글 자막이 있고 20분 이내인 동영상일 경우
                # 오디오 다운로드
                print(yt.streams.filter(only_audio=True))
                out_file=yt.streams.filter(only_audio=True).first().download(output_path=audio_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.mp3'
                os.rename(out_file, new_file)
                print(yt.title + ".mp3 has been successfully downloaded")
                # 자막 다운로드
                print(yt.captions.all())
                out_file = yt.captions['ko'].download(title=yt.title, output_path=cap_path)
                base, ext = os.path.splitext(out_file)
                new_file = base + '.txt'
                os.rename(out_file, new_file)
                print(yt.title + ".txt has been successfully downloaded")
        except Exception:
            continue            
            

if __name__ == "__main__":
    f = open("search_keywords.txt", "r") # reading keyword list file
    lines = f.readlines()
    for keyword in lines:
        keyword = keyword.strip()
        print("Searching youtube data about " + keyword)
        get_data(keyword)

    f.close()
