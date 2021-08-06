# !pip install --upgrade google-cloud-speech==1.3.2
import json
import urllib.request
from korean_romanizer.romanizer import Romanizer
from pororo import Pororo
import argparse
import tempfile
import queue
import sys
import sounddevice as sd
import soundfile as sf
import numpy
assert numpy
import librosa
import myprosody as mysp
import re
import io
import os
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
import time

"""
########## 1. 영상 오디오 STT 사용해서 한국어 문장 출력 ##########
"""

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./voltaic-day-321901-f0ba9adaf731.json" #API
speech_file = "./example.wav"
"""
내가 임의로 녹음한 음성오디오. "솔직히 다 때려치고 제주도 가서 한달살이 하고싶다" 라는 음성. 추후 영상의 음성을 인식하는 코드 append 필요.
"""

client = speech.SpeechClient()
"""
google cloud speech 의 speechclient API 인스턴스화.
"""

with io.open(speech_file, 'rb') as audio_file:
    content = audio_file.read()

"""
io 모듈로 오디오를 읽는다. read() 함수로 오디오를 읽고 content 에 저장.
"""

audio = types.RecognitionAudio(content=content)
config = types.RecognitionConfig(
    encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
    #encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
    #sample_rate_hertz=16000,
    #enableWordTimeOffsets=True,
    language_code='ko-KR')

"""
content을 recognitionaudio() 함수를 통해 audio에 저장
recognitionconfig() 함수를 통해 config 을 정의하고 config 에 저장 = 추후 영상 오디오가 어떤 형식인지(wav, flac, samplerate, bit depth)
에 따라 코드 수정 필요
"""

response = client.recognize(config, audio)

"""
SpeechClient를 인스턴스화 한 client에 recognize() 함수를 통해 정의한 config, audio를 읽고 response 에 저장
"""

for result in response.results:
    print(u'영상의 오디오 Transcript: {}'.format(result.alternatives[0].transcript))
    print(u'Confidence: {}'.format(result.alternatives[0].confidence))

print('-'*80)
time.sleep(3)

"""
########## 2.영상의 오디오를 로마자로 변환 ##########
"""


class KoreanRomanizer:
    def __init__(self):
        self.sent = ""
        print("Romanizer Initialized")
    def romanize(self, sent):
        self.sent = sent
        g2p = Pororo(task="g2p", lang="ko")
        r = Romanizer(g2p(self.sent))
        return r.romanize()

"""
romanize 함수는 뽀로로의 g2p 패키지를 사용.
"""

tester = KoreanRomanizer()
"""
KoreanRomanizer 클래스를 tester 에 인스턴스화.
"""

print('-'*80)
print('영상의 오디오를 로마자로 변환: ',tester.romanize(result.alternatives[0].transcript))
print('-'*80)
time.sleep(3)

"""
########## 3.영상의 오디오를 영어로 번역 ##########
"""

client_id = "PEDMV9jlEiGwITMbVl9S" # 개발자센터에서 발급받은 Client ID 값
client_secret = "0y7PXg98mI" # 개발자센터에서 발급받은 Client Secret 값

def translate(korstring):
    string = korstring
    encText = urllib.parse.quote(string)
    data = "source=ko&target=en&text=" + encText
    url = "https://openapi.naver.com/v1/papago/n2mt"
    request = urllib.request.Request(url)
    request.add_header("X-Naver-Client-Id",client_id)
    request.add_header("X-Naver-Client-Secret",client_secret)
    response = urllib.request.urlopen(request, data=data.encode("utf-8"))
    rescode = response.getcode()
    if rescode==200:
        response_body = json.load(response)
        return response_body['message']['result']['translatedText']
    else:
        return "Error Code: {}".format(rescode)

print('영상의 오디오를 영어로 번역: ',translate(result.alternatives[0].transcript))
print('-'*80)
time.sleep(3)

"""
########## 4.사용자의 목소리를 실시간으로 입력 ##########
"""

def int_or_str(text):
    try:
        return int(text)
    except ValueError:
        return text

def recorder():

    def callback(indata, frames, time, status):

        if status:
            print(status, file=sys.stderr)
        q.put(indata.copy())

    parser = argparse.ArgumentParser(add_help=False)

    parser.add_argument('-l', '--list-devices', \
                        action='store_true', help='show list of audio devices and exit')

    args, remaining = parser.parse_known_args()

    if args.list_devices:
        print(sd.query_devices())
        parser.exit(0)

    parser = argparse.ArgumentParser(description=__doc__, \
                                     formatter_class=argparse.RawDescriptionHelpFormatter, \
                                     parents=[parser])
    parser.add_argument('filename', nargs='?', metavar='FILENAME', \
                        help='audio file to store recording to')
    parser.add_argument('-d', '--device', type=int_or_str, \
                        help='input device (numeric ID or substring)')
    parser.add_argument('-r', '--samplerate', type=int, help='sampling rate')
    parser.add_argument('-c', '--channels', type=int, default=1, help='number of input channels')
    parser.add_argument('-t', '--subtype', type=str, help='sound file subtype (e.g. "PCM_24")')
    args = parser.parse_args(remaining)

    q = queue.Queue()

    try:
        if args.samplerate is None:
            device_info = sd.query_devices(args.device, 'input')
            # soundfile expects an int, sounddevice provides a float:
            args.samplerate = int(device_info['default_samplerate'])
        if args.filename is None:
            args.filename = tempfile.mktemp(prefix='rec_unlimited_test',
                                            suffix='.wav', dir='')
            global full_filename
            full_filename = args.filename

        with sf.SoundFile(args.filename, mode='x', samplerate=args.samplerate,
                          channels=args.channels, subtype=args.subtype) as file:
            with sd.InputStream(samplerate=args.samplerate, device=args.device,
                                channels=args.channels, callback=callback):
                print('녹음 중지하려면 interrupt')
                print('-' * 80)
                while True:
                    file.write(q.get())

    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(args.filename))

"""
위 함수가 파이썬에서 바로 음성을 받는 함수다.
dir 에 rec_unlimited_test .wav 음성을 저장해준다
"""


recorder()

"""
함수를 돌리면 음성녹음이 시작된다. doc의 사용예시를 보니깐 키보드 아무키나 누르면 녹음이 중지되야하는데
내 컴에선 커널을 interrupt 해야만 녹음이 중지된다. 해걸 필요
"""

print('the name of the audiofile is :', full_filename)
"""
파일명을 출력
"""

full_filename = re.sub('\.wav$','',full_filename)
print('after removing .wav: ', full_filename)
"""
정규식으로 .wav 없애준다. 나중에 모델 학습시킬때 보통 파이썬 내 함수명엔 .wav 가 없으니 용이하다
"""

print('-'*80)
time.sleep(3)


data, samplerate = librosa.load(f'/Users/jonghyunlee/PycharmProjects/Voice/{full_filename}.wav', sr=48000)
sf.write(f'/Users/jonghyunlee/PycharmProjects/Voice/dataset/audioFiles/{full_filename}_encoded.wav',data, samplerate, "PCM_24")

"""
이부분은 사용자가 녹음한 오디오의 sample rate 와 bit depth 를 바꿔주는 부분이다.
"""

name = f'{full_filename}_encoded'
path = r'/Users/jonghyunlee/PycharmProjects/Voice'

print(mysp.myspgend(name,path))
print('-'*80)
print(mysp.mysppron(name,path))
