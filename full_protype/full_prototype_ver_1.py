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
import numpy  # Make sure NumPy is loaded before it is used in the callback
assert numpy  # avoid "imported but unused" message (W0611)
import librosa
import myprosody as mysp
import re

#1. 영상오디오 STT 사용 한국어 문장 출력
'''
이부분은 정훈이랑 근형이가 실험해보고 결과 append.
'''
print('-'*80)
print('영상의 오디오 STT: 솔직히 다 때려치고 제주도 가서 한달살이 하고싶다.')
print('-'*80)

#2. 한국어 로마지로 변환
#from romanizer import KoreanRomanizer
#tester = KoreanRomanizer()
#print(tester.romanize('응애 나 아기산붕 제주도 가고싶어 울어'))

class KoreanRomanizer:
    def __init__(self):
        self.sent = ""
        print("Romanizer Initialized")
    def romanize(self, sent):
        self.sent = sent
        g2p = Pororo(task="g2p", lang="ko")
        r = Romanizer(g2p(self.sent))
        return r.romanize()

tester = KoreanRomanizer()
print('-'*80)
print('영상의 오디오를 로마자로 변환: ',tester.romanize('솔직히 다 때려치고 제주도 가서 한달살이 하고싶다.'))
print('-'*80)

#3. 한국어 영어로 변환
'''
번역 API
'''
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

print('영상의 음성 영어로 번역: ',translate('솔직히 다 때려치고 제주도 가서 한달살이 하고싶다.'))
print('-'*80)

#4. 사용자의 목소리 실시간 입력
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
                print('-' * 80)
                print('녹음 중지하려면 interrupt')
                print('-' * 80)
                while True:
                    file.write(q.get())

    except KeyboardInterrupt:
        print('\nRecording finished: ' + repr(args.filename))
        #parser.exit(0)
#    except Exception as e:
#        parser.exit(type(e).__name__ + ': ' + str(e))

#if __name__ == '__main__':
recorder()
print('the name of the audiofile is :', full_filename)
full_filename = re.sub('\.wav$','',full_filename)
print('after removing .wav: ', full_filename)
print('-'*80)


#마이프로소디 사용 뽑기
import myprosody as mysp
data, samplerate = librosa.load(f'/Users/jonghyunlee/PycharmProjects/Voice/{full_filename}.wav', sr=48000)
sf.write(f'/Users/jonghyunlee/PycharmProjects/Voice/dataset/audioFiles/{full_filename}_encoded.wav',data, samplerate, "PCM_24")

name = f'{full_filename}_encoded'
path = r'/Users/jonghyunlee/PycharmProjects/Voice'

print(mysp.myspgend(name,path))
print('-'*80)
print(mysp.mysppron(name,path))
#print('-'*80)
#print(mysp.mysptotal(name,path))
