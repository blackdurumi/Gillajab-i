import os
import shutil
import tarfile
from aihub_txt_preprocessing import sentence_filter
import jamotools
from g2pk import G2p


def search(dirname):
    g2p = G2p()
    try:
        flist = os.listdir(dirname)
        for file in flist:
            full_filename = dirname+'/'+file
            if os.path.isdir(full_filename):
                search(full_filename)
            else:
                if file[-3:] == "wav":
                    shutil.copy(full_filename, proc_dir)
                elif file[-3:] == "txt":
                    curfile = open(full_filename, "r", encoding='utf-8').read()
                    if curfile is None:
                        continue
                    curfile = sentence_filter(curfile)
                    # G2pk가 설치되는 환경에서 아래 코드의 주석을 해제하면 음소 sequence로까지 변환 가능
                    # curfile = jamotools.split_syllables(u"{}".format(g2p(curfile)))
                    trans.write(file[:-4] + " " + curfile + "\n")
                elif file[-4:] == "json":
                    pass
    except PermissionError:
        pass


if __name__ == "__main__":
    """
    aihub_data_dir 에 있는 aihub 데이터(압축 해제된 상태이어야 함)를
    processed 폴더에
    kaldi style로 변환하여 저장해주는 py파일
    """

    ############################################################
    # 아래의 두 경로를 지정해줄 것 #
    ############################################################
    aihub_data_dir = "../aihub_data"
    proc_dir = os.path.join(os.getcwd(), "processed")
    ############################################################

    # 압축파일이 있다면 해제
    for l in os.listdir(aihub_data_dir):
        if l[-7:]==".tar.gz":
            tar = tarfile.open(aihub_data_dir+l)
            tar.extractall(path=aihub_data_dir)
            tar.close()

    # kaldi style을 보면 trans.txt에 wav파일의 id와 text가 저장되어있음. 이를 생성하기 위함
    trans = open("./processed/trans.txt", "w")

    # 이후 aihub_data_dir 하위 폴더를 순회하면서 kaldi 디렉토리 style로 변환해줌
    search(aihub_data_dir)

    trans.close()
