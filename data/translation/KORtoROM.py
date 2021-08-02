from korean_romanizer.romanizer import Romanizer


if __name__=="__main__":
    korstring = "내 심장 안을 파헤쳐 네 말들이 난 아무것도 아닌 기분만 들지"
    r = Romanizer(korstring)
    print(r.romanize())