import os
import shutil
from aihub_txt_preprocessing import sentence_filter

if __name__ == "__main__":
    """
    aihub_data_dir 에 있는 aihub 데이터를
    현재 폴더(preprocessing)내에 processed 폴더에
    kaldi style로 변환하여 저장해주는 py파일
    
    실행 전 aihub_data_dir를 잘 지정하자
    """
    aihub_data_dir = '../[원천]8.쇼핑_shopping_01/data/remote/KoreanSpeech/data/2_Validation/raw/09_쇼핑/shopping_01'
    proc_dir = os.getcwd() + "\\processed"

    # kaldi style을 보면 trans.txt에 wav파일의 id와 text가 저장되어있음. 이를 생성하기 위함
    trans = open("./processed/shopping.trans.txt", "w")

    # json, wav, txt파일이 있는 폴더의 부모 폴더로 위치 변경 해줌
    os.chdir(aihub_data_dir)

    # 이후 하위 폴더를 순회하면서 kaldi 디렉토리 style로 변환해줌
    for dlist in os.listdir():
        os.chdir(dlist)
        flist = os.listdir()
        for file in flist:
            if file[-3:] == "wav":
                shutil.copy(os.getcwd() + '/' + file, proc_dir)
            elif file[-3:] == "txt":
                curfile = open(file, "r", encoding='utf-8').read()
                curfile = sentence_filter(curfile)
                trans.write(file[:-4] + " " + curfile + "\n")
            elif file[-4:] == "json":
                pass
        os.chdir('..')

    trans.close()
