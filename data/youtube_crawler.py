!pip install youtube-dl
!pip install --upgrade google-api-python-client google-auth-httplib2 google-auth-oauthlib

from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from oauth2client.tools import argparser
import os.path
from __future__ import unicode_literals
import youtube_dl
from google.colab import drive
drive.mount('/content/drive')

class YoutubeCrawler:
  def __init__(self):
    DEVELOPER_KEY = "AIzaSyBdVs0MPCwbcoQi3ZUwV_RfwaQ_xFlbxJc" # 코드 공유 금지!
    YOUTUBE_API_SERVICE_NAME="youtube"
    YOUTUBE_API_VERSION="v3"
    self.youtube = build(YOUTUBE_API_SERVICE_NAME,YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY)
    self.keyword = ""
    self.folder= ""
  def get_url(self, keyword):
    url_ = []
    for i in range(5): # 250 videos total
      try:
        i = self.youtube.search().list(
          q = keyword,
          type = 'video',
          part = "snippet",
          pageToken = 'CDIQAA',
          maxResults = 50 
          ).execute()
      except Exception as e:
        print(e)
        continue

      for _ in i['items']:
        url_.append(_['id']['videoId'])
    url = ['https://www.youtube.com/watch?v=' + u for u in url_]
    return url
  def get_audio(self, keyword, folder):
    PATH = os.path.join("./drive/Shareddrives", "Data Youth Campus - 4조 Database", folder)
    url = self.get_url(keyword)
    url = list(set(url)) # 중복 제거
    for _ in url:
      try:
        ydl_opts = {
            'format' : 'bestaudio/best',
            'postprocessors' : [{
                'key' : 'FFmpegExtractAudio',
                'preferredcodec' : 'wav',
                'preferredquality' : '1400',
            }],
            'outtmpl' : PATH + '/%(title)s.%(ext)s',
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
          ydl.download([_])          
      except Exception:
        continue

if __name__ == '__main__':
  crawler = YoutubeCrawler()
  with open('search_keywords.txt', 'r') as f:
    d = dict(x.strip().split(sep="\t", maxsplit=1) for x in f) # 딕셔너리로 변환

  for keyword, folder in d.items():
    crawler.get_audio(keyword, folder)

  f.close()