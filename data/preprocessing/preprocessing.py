import re
import os
import tarfile
import pandas as pd
from g2pk import G2p
from jamotools import split_syllables
import tqdm


class Unzip:
    """
    A class to unzip tar.gz files which AI hub provides
    """

    def __init__(self, tar_path, to_path):
        """
        Constructs all the necessary attributes for the Unzip class
        :param tar_path: str
            Path of directory where tar.gz files are stored
        :param to_path: str
            Path to save unzipped files
        """
        self.tar_path = tar_path
        self.to_path = to_path

    def unzip(self, tar_path, to_path):
        """
        Unzip tar.gz files into desired directory
        :param tar_path: str
            Path of directory where tar.gz files are stored
        :param to_path: str
            Path to save unzipped files
        :return: None
        """
        self.tar_path = tar_path
        self.to_path = to_path

        folder = re.findall(r'(/[A-Za-z]+?)/$', self.tar_path)[0] # Validation or Training

        for path, dir, filenames in os.walk(self.tar_path):
            # Get only label data
            files = list(filter(lambda filename: '[라벨]' in filename and 'tar.gz' in filename, filenames))

        for _ in files:
            # Unzip files into desired directory
            tar = tarfile.open(self.tar_path + _, 'r:gz')
            tar.extractall(path=self.to_path + folder)
            tar.close()


class SentenceCleaner:
    """
     A class to remove unnecessary characters in the sentences
     """

    def __init__(self, sentence):
        """
        Constructs all the necessary attributes for the SentenceCleaner class
        :param sentence: str
            Sentence which needs to be refined
        """
        self.sentence = sentence

    def bracket_filter(self, sentence):
        """
        Filters bracket in the sentence, remain the second one
        :param sentence: str
            Sentence which needs to be refined
        :return: new_sentence: str
            Sentence with bracket removed and remain the word in the second bracket
        """
        self.sentence = sentence
        new_sentence = str()
        flag = False

        for ch in self.sentence:

            if ch == '(' and flag == False:
                flag = True
                continue

            if ch == '(' and flag == True:
                flag = False
                continue

            if ch != ')' and flag == False: #
                new_sentence += ch

        return new_sentence

    def special_filter(self, sentence):
        """
        Filters special characters in the sentence
        :param sentence: str
            Sentence which needs to be refined
        :return: new_sentence: str
            Sentence with special character removed or replaced
        """
        self.sentence = sentence

        SENTENCE_MARK = ['?', '!']
        NOISE = ['o', 'n', 'u', 'b', 'l']
        EXCEPT = ['/', '+', '*', '-', '@', '$', '^', '&', '[', ']', '=', ':', ';', '.', ',']

        new_sentence = str()

        for idx, ch in enumerate(self.sentence):
            if ch not in SENTENCE_MARK:
                # o/, n/ 등 처리
                if idx + 1 < len(self.sentence) and ch in NOISE and self.sentence[idx + 1] == '/':
                    continue

            if ch == '#':
                new_sentence += '샾'

            elif ch not in EXCEPT:
                new_sentence += ch

        pattern = re.compile(r'\s\s+')

        new_sentence = re.sub(pattern, ' ', new_sentence.strip())

        return new_sentence

    def sentence_filter(self, sentence) -> str:
        """
        Runs bracket_filter and special_filter together and return the refined sentence
        :param sentence: str
            Sentence which needs to filter special characters
        :return: filtered_sentence: str
            Completely filtered sentence
        """
        self.sentence = sentence

        filtered_sentence = self.special_filter(self.bracket_filter(self.sentence))

        return filtered_sentence


class DataProcessor(SentenceCleaner):
    """
     A class to process label data to be ready to transform into the Kaldi format
     """
    def __init__(self, path, types, folder, wdir):
        """
        Constructs all the necessary attributes for the DataProcessor class
        :param path: str
            Path of directory where label file exists
        :param types: str
            File types; either 'scripts' or 'metadata'
        :param folder: str
            Folder that file exists; either 'Training' or 'Validation'
        :param wdir: str
            Path of directory that audio files are stored
        """
        self.path = path
        self.types = types
        self.folder = folder
        self.wdir = wdir

    def files(self, path):
        """
        Returns list of files exist in the directory corresponding to the path
        :param path: str
            Path of directory where label file exists
        :return: file_list: list
            List contains all files in the directory, also in the child directory
        """
        self.path = path

        file_list = []

        for file_path, dir, filenames in os.walk(path):
            for filename in filenames:
                file_list.append(os.path.join(file_path, filename))

        return file_list

    def concat_data(self, path, types, folder):
        """
        Concatenates files all together which are same types(scripts/metadata) from same folders(Training/Validation)
        and returns the path of created file
        :param path: str
            Path of directory where label file exists
        :param types: str
            File types; either 'scripts' or 'metadata'
        :param folder: str
            Folder that file exists; either 'Training' or 'Validation'
        :return: filepath: str
            Path of created file in the function, will use it when making data frame
        """
        self.types = types

        # list of files to concatenate
        file_list = [_ for _ in self.files(path) if types in _ and folder in _]

        filepath = path + f'{folder}_{types}_base.txt'

        # if file not exists in directory
        if filepath not in os.listdir(path):

            with open(filepath, 'w') as f1:
                for i, file in enumerate(file_list):
                    # read files in the file_list
                    with open(file, 'r') as f2:
                        # read lines of the file if exists
                        while True:
                            line = f2.readline()
                            if not line:
                                break
                            # write line in the file
                            f1.write(line)

            # close files
            f2.close()
            f1.close()

        else: # if file already exists
            print(f'{filepath} already exists')

        return filepath

    def mkdf(self, path, wdir):
        """
        Makes data frame, add columns and modify path of audio files to transform files
        :param path: str
            Path of directory where label file exists
        :param wdir: str
            Path of directory that audio files are stored
        :return: df: pd.DataFrame
            data frame made of concatenated files
        """
        folder = path.split('/')[-1].split('_')[0] # Training or Validation

        if 'scripts' in path.split('/')[-1]:
            df = pd.read_csv(path, sep='::', header=None, engine='python')
            df.columns = ['path', 'txt']
            df.dropna(inplace=True)

            # remove white space in front of the sentence
            df.txt = df.txt.apply(lambda _: ' '.join(_.split(' ')[1:]) if _.startswith(' ') else _)

            # make spk columns in specific format(includes first alphabet of folder, category and audio file name)
            df['spk'] = df.path.apply(
                lambda _: _.split('/')[1].split('.')[1][0] + '_' + _.split('/')[-1].split('.')[0][0] + '_' +
                          _.split('/')[-1].split('.')[0].split('_')[1])

            # add 'val_' to the beginning of the values if the files is in Validation folder
            df['name'] = df.path.apply(lambda _: 'val_' + _.split('/')[-1].split('.')[0] if folder == 'Validation' else
            _.split('/')[-1].split('.')[0])

        elif 'metadata' in path.split('/')[-1]:
            df = pd.read_csv(path, sep='|', header=None, engine='python')
            df.columns = ['path', 'n1', 'n2', 'gender', 'n3', 'n4', 'n5', 'n6', 'n7']  # n#: useless columns
            df.gender = df.gender.apply(lambda _: _.lower()) # convert to lowercase
            df = df[['path', 'gender']]

        # change the path to the directory that audio files exists
        df.path = df.path.apply(
            lambda _: (wdir + _.split('/')[-1].split('_')[0] + '/val_' + _.split('/')[-1]).replace(' ',
                                                                                                   '') if folder == 'Validation' else (
                        wdir + _.split('/')[-1].split('_')[0] + '/' + _.split('/')[-1]).replace(' ', ''))

        return df

    def merge_df(self, script_df, metadata_df, on='path'):
        """
        Merges script data frame and metadata data frame for spk2gender
        :param script_df: pd.DataFrame
            Data Frame contains all script files made by mkdf function
        :param metadata_df: pd.DataFrame
            Data Frame contains all metadata files made by mkdf function
        :param on: str
            Key columns to merge(default: 'path')
        :return: merged_df: pd.DataFrame
            Sorted data frame contains every column need
        """
        merged_df = script_df.merge(metadata_df, how='inner', on=on) # inner join to get
        merged_df.sort_values(by='name', inplace=True) # sort values in ascending order(Kaldi format requires to sort

        return merged_df

    def final_df(self, path, folder, wdir):
        """
        Runs concat_data, mkdf, merge_df and returns complete data frame
        :param path: str
            Path of directory where label file exists
        :param folder: str
            Folder that file exists; either 'Training' or 'Validation'
        :param wdir: str
            Path of directory that audio files are stored
        :return: df: pd.DataFrame
            Complete data frame
        """

        # concatenate files into one file
        scripts = self.concat_data(path, 'scripts', folder)
        metadata = self.concat_data(path, 'metadata', folder)

        # create data frame
        s_df = self.mkdf(scripts, wdir)
        m_df = self.mkdf(metadata, wdir)

        # merge data frame and sort values in ascending order
        df = self.merge_df(s_df, m_df)

        return df

    def sentence_prep(self, path, folder, wdir, run_tqdm=True):
        """
        Refines sentences in txt columns then transforms sentences into pronounced way and then transforms sentences into phoneme
        :param path: str
            Path of directory where label file exists
        :param folder: str
            Folder that file exists; either 'Training' or 'Validation'
        :param wdir: str
            Path of directory that audio files are stored
        :param run_tqdm: bool
            Whether run tqdm to see the progress of sentence transformation or not
        :return: df: pd.DataFrame
            Data frame completed to convert scripts(colname: txt) into phoneme in pronounced way
        """
        self.path = path
        self.folder = folder
        self.wdir = wdir

        g2p = G2p()

        df = self.final_df(path, folder, wdir)
        df.dropna(inplace=True) # just in case null value exists

        if run_tqdm == True: # see the progress of sentence transformation
            tqdm.pandas() # since we use apply function on pd.Series type
            df.txt = df.txt.progress_apply(lambda _: split_syllables(g2p(self.sentence_filter(_))))
            
        else:
            df.txt = df.txt.apply(lambda _: split_syllables(g2p(self.sentence_filter(_))))

        return df

    # run only when folder is Validation
    def split_df(self, validation_df):
        """
        Splits validation_df into test and valid data frames
        :param validation_df: pd.DataFrame
            Data frame of files in Validation folder which needs to be split
        :return: test_df, val_df : tuple contains data frame
            indexing needed to work on the each data frame
        """
        # test: 'play', 'shopping' category, valid: the other categories
        test_df = validation_df.loc[validation_df.name.isin(list(filter(lambda _: 'play' in _ or 'shopping' in _, validation_df.name)))]
        val_df = validation_df.loc[validation_df.name.isin(list(filter(lambda _: 'play' not in _ or 'shopping' not in _, validation_df.name)))]

        # to avoid copy warning
        test_df = test_df.copy()
        val_df = val_df.copy()

        # replace to the correct path
        test_df.path = test_df.path.str.replace('train_data_01/train_data', 'test_data_01/test_data')
        val_df.path = val_df.path.str.replace('train_data_01/train_data', 'test_data_01/valid_data')

        return test_df, val_df


class PathProcessor:
    """
     A class to create the file and directory to meet the requirement (Kaldi format)
     """
    def __init__(self, path, folder):
        """
        Constructs all the necessary attributes for the DataProcessor class
        :param path: str
            Path of directory desired to work on
        :param folder: str
            Folder needs to be created
        """
        self.path = path
        self.folder = folder

    def mkdir(self, path, folder):
        """
        Creates directories corresponding to Kaldi format
        :param path: str
            Path of directory desired to work on
        :param folder: str
            Folder needs to be created
        :return: None
        """
        # change directory
        os.chdir(path)
        try:
            # create data folder
            os.mkdir('data')
            print('data folder created')
            
        except FileExistsError: # if data folder exists
            print('data folder already exists')

        os.chdir('./data') # change directory to data
        path = './' + folder
        try:
            os.mkdir(path) # create required folder under data folder
            print(f'{folder} folder created')
            
        except FileExistsError:
            print(f'{folder} folder already exists')

        os.chdir(path) # revert to original path

    def mkfile(self, df, col1, col2, filename):
        """
        Creates files corresponding to Kaldi format
        :param df: pd.DataFrame
            Data frame used to make the file
        :param col1: str
            First column in the file (should exist in data frame)
        :param col2: str
            Second column in the file (should exist in data frame)
        :param filename: str
            File name to save
        :return: None
        """
        trans_df = df[[col1, col2]]
        trans_df.to_csv(f'{filename}', header=None, index=False, sep=' ')

    def transform_data(self, df, path, folder):
        """
        Runs mkdir and mkfile and finalize preprocessing
        :param df: pd.DataFrame

        :param path: str
            Path of directory desired to work on
        :param folder: str
            Folder needs to be created
        :return: None
        """
        self.path = path
        self.folder = folder
        self.mkdir(path, folder)
        # text
        self.mkfile(df, 'name', 'txt', 'text_')
        # since there shouldn't be quotation marks on script, extra work needed
        with open('text', 'w') as f1:
            # read file created by mkfile function
            with open('text_', 'r') as f2:
                while True:
                    line = f2.readline()
                    # remove quotation mark
                    line = line.replace('"', '')
                    if not line:
                        break
                    # write the new file
                    f1.write(line)
                    
        # close the file
        f2.close()
        f1.close()
        # remove the unnecessary file
        os.remove('text_')

        # wav.scp
        self.mkfile(df, 'name', 'path', 'wav.scp')

        # utt2spk
        self.mkfile(df, 'name', 'spk', 'utt2spk')

        # spk2utt
        self.mkfile(df, 'spk', 'name', 'spk2utt')

        # spk2gender
        self.mkfile(df, 'spk', 'gender', 'spk2gender')
