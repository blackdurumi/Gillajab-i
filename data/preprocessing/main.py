# -*- coding: utf-8 -*-

# !pip install g2pk
# !pip install jamotools

from preprocessing import Unzip, DataProcessor, PathProcessor


def main(to_path, wdir, *tar_path, unzip=False):
  """
  Run all the process for the preprocessing
  :param to_path: str
    Path to save unzipped files
  :param wdir: str
    Path of directory that audio files are stored
  :param tar_path: *args(optional)
    Path of directory where tar.gz files are stored
  :param unzip: bool (default=False)
    Whether unzip file or not
  :return: None
  """

    # create instance of classes
    dp = DataProcessor()
    pp = PathProcessor()

    # unzip file if unzip == True
    if unzip == True:
        uz = Unzip()
        tar_path = list(tar_path)

        for _ in tar_path:
            print(_)
            uz.unzip(_, to_path)

    # process label file in the Training folder
    train_df = dp.sentence_prep(to_path, 'Training', wdir)

    # process label file in the Validation folder
    validation_df = dp.sentence_prep(to_path, 'Validation', wdir)

    # split validation_df into test_df and val_df
    spl_df = dp.split_df(validation_df) # returns tuple
    test_df = spl_df[0]
    val_df = spl_df[1]

    # transform path and file corresponding to Kaldi format
    pp.transform_data(train_df, to_path, 'train_data_01')
    pp.transform_data(train_df, to_path, 'train_nodev')
    pp.transform_data(validation_df, to_path, 'test_data_01')
    pp.transform_data(test_df, to_path, 'test_clean')
    pp.transform_data(val_df, to_path, 'train_dev')


if __name__ == '__main__':
    # path where tar.gz files exist
    # t_path = '/content/drive/Shareddrives/Data Youth Campus - 4조 Database/한국인 대화 음성 데이터/Training/'
    # v_path = '/content/drive/Shareddrives/Data Youth Campus - 4조 Database/한국인 대화 음성 데이터/Validation/'

    # directory to work on
    to_path = '/content/drive/MyDrive/dialogue/'

    # directory where audio files exist
    wdir = '/home/kwangho/datacampusteam4/espnet-new/egs2/zeroth_korean/asr1/downloads/train_data_01/train_data/'

    # execute
    main(to_path, wdir)
