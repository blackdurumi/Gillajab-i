# !pip install youtube_dl

import youtube_dl
import os
# from google.colab import drive
# drive.mount('/content/drive')

class YoutubeCrawler:
  def __init__(self):
    self.channel_id = ""
  def get_audio(self, channel_id):
    PATH = os.path.join("./drive/Shareddrives", "Data Youth Campus - 4조 Database", 'non-native') # change to your path
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
      videos = ydl.extract_info(f'https://www.youtube.com/c/{channel_id}/videos')

if __name__ == '__main__':
  crawler = YoutubeCrawler()
  with open('channel_names.txt', 'r', encoding='utf-8') as f:
   lst = [x.strip() for x in f.readlines()]

  for channel_id in lst:
    crawler.get_audio(channel_id)

  f.close()
