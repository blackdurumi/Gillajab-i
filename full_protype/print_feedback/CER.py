import fastwer
import jamotools
import jiwer
from korean_romanizer.romanizer import Romanizer
import pandas as pd
from IPython.display import display


def CER(ground_truth, users):
    '''
    print correct_phoneme, user's phoneme
    print correct_sentence, user's sentence
    print WER, MER, WIL, char_CER, phoneme_CER, Accuracy of CER
    print Char Error
    print Phoneme Best Error


    :param ground_truth: Correct phoneme
    :param users: User's phoneme
    :return: None
    '''
    kor_eng_list = [
        ['ㅂ', 'p0'],
        ['ㅍ', 'ph'],
        ['ㅃ', 'pp'],
        ['ㄷ', 't0'],
        ['ㅌ', 'th'],
        ['ㄸ', 'tt'],
        ['ㄱ', 'k0'],
        ['ㅋ', 'kh'],
        ['ㄲ', 'kk'],
        ['ㅅ', 's0'],
        ['ㅆ', 'ss'],
        ['ㅎ', 'h0'],
        ['ㅈ', 'c0'],
        ['ㅊ', 'ch'],
        ['ㅉ', 'cc'],
        ['ㅁ', 'mm'],
        ['ㄴ', 'nn'],
        ['ㄹ', 'rr'],
        ['ㅂ', 'pf'],
        ['ㅍ', 'ph'],
        ['ㄷ', 'tf'],
        ['ㅌ', 'th'],
        ['ㄱ', 'kf'],
        ['ㅋ', 'kh'],
        ['ㄲ', 'kk'],
        ['ㅅ', 's0'],
        ['ㅆ', 'ss'],
        ['ㅎ', 'h0'],
        ['ㅈ', 'c0'],
        ['ㅊ', 'ch'],
        ['ㅁ', 'mf'],
        ['ㄴ', 'nf'],
        ['ㅇ', 'ng'],
        ['ㄹ', 'll'],
        ['ㄱㅅ', 'ks'],
        ['ㄴㅈ', 'nc'],
        ['ㄴㅎ', 'nh'],
        ['ㄹㄱ', 'lk'],
        ['ㄹㅁ', 'lm'],
        ['ㄹㅂ', 'lb'],
        ['ㄹㅅ', 'ls'],
        ['ㄹㅌ', 'lt'],
        ['ㄹㅍ', 'lp'],
        ['ㄹㅎ', 'lh'],
        ['ㅂㅅ', 'ps'],
        ['ㅣ', 'ii'],
        ['ㅔ', 'ee'],
        ['ㅐ', 'qq'],
        ['ㅏ', 'aa'],
        ['ㅡ', 'xx'],
        ['ㅓ', 'vv'],
        ['ㅜ', 'uu'],
        ['ㅗ', 'oo'],
        ['ㅖ', 'ye'],
        ['ㅒ', 'yq'],
        ['ㅑ', 'ya'],
        ['ㅕ', 'yv'],
        ['ㅠ', 'yu'],
        ['ㅛ', 'yo'],
        ['ㅟ', 'wi'],
        ['ㅚ', 'wo'],
        ['ㅙ', 'wq'],
        ['ㅞ', 'we'],
        ['ㅘ', 'wa'],
        ['ㅝ', 'wv'],
        ['ㅢ', 'xi']]

    eng_kor_list = [[i[1], i[0]] for i in kor_eng_list]
    df = pd.DataFrame(eng_kor_list, columns=['eng', 'kor'])

    transformation = jiwer.Compose([
        jiwer.RemoveMultipleSpaces(),
        jiwer.RemoveWhiteSpace(replace_by_space=False),
        jiwer.RemovePunctuation()
    ])

    ground_truth_phoneme = ground_truth
    hypothesis_phoneme = users

    ground_truth_char = jamotools.join_jamos(ground_truth_phoneme)
    hypothesis_char = jamotools.join_jamos(hypothesis_phoneme)

    wer = jiwer.wer(ground_truth_char, hypothesis_char)  ## Word Error Rate
    mer = jiwer.mer(ground_truth_char, hypothesis_char)  ## Match Error Rate
    wil = jiwer.wil(ground_truth_char, hypothesis_char)  ## Word Information Lost

    CER_PHONEME = fastwer.score(list(transformation(ground_truth_phoneme)), list(transformation(hypothesis_phoneme)),
                                char_level=True)  ## Phoneme Error Rate
    CER_CHAR = fastwer.score(list(transformation(ground_truth_char)), list(transformation(hypothesis_char)),
                             char_level=True)  ## Char Error Rate

    print(len(ground_truth_phoneme), len(hypothesis_phoneme))
    print(f"ground_truth(phoneme): {ground_truth_phoneme}")
    print(f"hypothesis(phoneme): {hypothesis_phoneme}")

    print('=' * 30)
    print(len(ground_truth_char), len(hypothesis_char))
    print(f"ground_truth(char): {ground_truth_char}")
    print(f"hypothesis(char): {hypothesis_char}")
    print(type(hypothesis_char))

    print('=' * 30)
    print(f"wer:{wer:.4f}, mer:{mer:.4f}, wil:{wil:.4f}")
    print(f"CER(char): {CER_CHAR}")
    print(f"CER(phoneme): {CER_PHONEME}")

    if CER_PHONEME == 0:
        print("Perfect")
    elif 0 < CER_PHONEME <= 2:
        print('Accuracy: 98~99%')
    elif 2 < CER_PHONEME <= 10:
        print('Accuracy: 90~95%')
    elif CER_PHONEME > 10:
        print('Accuracy: Below 90%')

    # error_part = [{"idx":i, 'ground_truth':k, 'Users': t} for i,k in enumerate(list(ground_truth_char)) for j,t in enumerate(list(hypothesis_char)) if i==j if k != t]
    char_idx = [i for i, k in enumerate(list(ground_truth_char)) for j, t in enumerate(list(hypothesis_char)) if i == j
                if k != t]
    char_true = [[k, Romanizer(k).romanize()] for i, k in enumerate(list(ground_truth_char)) for j, t in
                 enumerate(list(hypothesis_char)) if i == j if k != t]
    char_false = [[t, Romanizer(t).romanize()] for i, k in enumerate(list(ground_truth_char)) for j, t in
                  enumerate(list(hypothesis_char)) if i == j if k != t]

    phoneme_idx = [i for i, k in enumerate(list(transformation(ground_truth_phoneme))) for j, t in
                   enumerate(list(transformation(hypothesis_phoneme))) if i == j if k != t]
    phoneme_true = [k for i, k in enumerate(list(transformation(ground_truth_phoneme))) for j, t in
                    enumerate(list(transformation(hypothesis_phoneme))) if i == j if k != t]
    phoneme_false = [t for i, k in enumerate(list(transformation(ground_truth_phoneme))) for j, t in
                     enumerate(list(transformation(hypothesis_phoneme))) if i == j if k != t]

    kor_phoneme = [df[df.kor == k].eng.values[0] for k in phoneme_false]

    print('=' * 30)
    # print(f"error_idx:{idx}")
    print("Modify")
    print("ordinal ==> change")
    print()

    for i, k in enumerate(char_idx):

        true_roma = Romanizer("{}".format(ground_truth_char[k - 1:k + 4]))
        user_roma = Romanizer("{}".format(hypothesis_char[k - 1:k + 4]))

        if ' ' not in (ground_truth_char[k - 1:k + 4]).strip():
            # if (ground_truth_char[k-1:k+4]).strip() != (ground_truth_char[k-2:k+3]).strip():
            print(
                f"{hypothesis_char[k - 1:k + 4]}({user_roma.romanize()}) ==> {ground_truth_char[k - 1:k + 4]}({true_roma.romanize()})")

        # print('yes')

    print("=" * 30)
    print('Final')
    print()

    a = 'qwertyuiopasdfghjklzxcvbnmQWERTYUIOPASDFGHJKLZXCVBNM'
    for i in char_idx:
        a = a.replace(a[i], '所')

    for i in a:
        if i.startswith('所') == False:
            a = a.replace(i, '  ')

    # hypothesis_char2 = ''.join([i.ljust(2) for i in hypothesis_char])
    # ground_truth_char2 = ''.join([i.ljust(2) for i in ground_truth_char])
    # a2 = ''.join([i.ljust(2) for i in a])

    hypothesis_char = hypothesis_char.replace(' ', '  ')
    ground_truth_char = ground_truth_char.replace(' ', '  ')

    print(' ' * (len('Your Pronounce(korean):  ')) + a)
    print('Your Pronounce(korean): ', "{}".format(hypothesis_char))
    print('Right Pronounce(korean): '"{}".format(ground_truth_char))
    print()

    print('Your Pronounce(romaji): ', Romanizer("{}".format(hypothesis_char)).romanize())
    print('Right Pronounce(romaji): ', Romanizer("{}".format(ground_truth_char)).romanize())
    print()

    char_f = [f"{i[0]} : {i[1]}" for i in char_false]
    char_t = [f"{i[0]} : {i[1]}" for i in char_true]
    # print(f"Wrong Char:{char_f}")
    # print()
    # print(f"Right Char:{char_t}")
    # print()
    print()
    print("#####Char Error#####")
    char_error_df = pd.DataFrame(char_f, char_t).reset_index()
    char_error_df.columns = ['False_char', ' True_char']
    display(char_error_df)

    print()
    print("######Phoneme Best Error#######")
    phoneme_error_df = pd.DataFrame(phoneme_false, kor_phoneme).reset_index()
    phoneme_error_df.columns = ['eng', 'kor']

    q = pd.DataFrame(phoneme_error_df.value_counts()).reset_index()
    q.columns = ['eng', 'kor', 'error_num']

    display(q.head())
    print()
    print(f"you have to practice {q.kor.values[:5]} phoneme")


if __name__  == "__main__":

    ground_truth = 'ㅅㅓㅇㅅㅜㅋㅐㅈㅣㄴㅡㄴ ㅅㅏㄹㅏㅁㅡ ㄴㅕㄴㅐㄹㅡㄹ ㅎㅏㄷㅏㄱㅏ ㅁㅜㄴㅈㅔㄱㅏ ㅅㅐㅇㄱㅕㅆㅡㄹ ㄸㅐ ㅈㅏㅅㅣㄴㅡㄹ ㄷㅗㄹㅏㅂㅗㄴㅡㄴ ㅅㅏㄹㅏㅁㅣㅇㅑ'
    users = 'ㅅㅓㅇㅅㅜㄱㅎㅐㅈㅣㄴㅡㄴ ㅅㅏㄹㅏㅁㅇㅡㄴ ㅇㅕㄴㅇㅐㄹㅡㄹ ㅎㅏㄷㅏㄱㅏ ㅁㅜㄴㅈㅔㄱㅏ ㅅㅐㅇㄱㅕㅆㅇㅡㄹ ㄸㅐ ㅈㅏㅅㅣㄴㅇㅡㄹ ㄷㅗㄹㅇㅏㅂㅗㄴㅡㄴ ㅅㅏㄹㅏㅁㅇㅣㅇㅑ'
    CER(ground_truth, users)