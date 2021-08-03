from pororo import Pororo


if __name__=="__main__":
    asr = Pororo(task='asr', lang='ko')
    asr('example.wav')