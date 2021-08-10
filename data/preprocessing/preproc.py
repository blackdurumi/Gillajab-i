import os
import shutil
from aihub_txt_preprocessing import sentence_filter

if __name__ == "__main__":
    proc_dir = os.getcwd() + "\\processed"
    trans = open("./processed/trans.txt", "w")
    os.chdir('../[원천]8.쇼핑_shopping_01/data/remote/KoreanSpeech/data/2_Validation/raw/09_쇼핑/shopping_01')

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
