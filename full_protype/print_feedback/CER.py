# ! pip install jiwer
# ! pip install pybind11 fastwer
# ! pip install jamotools
# ! pip install korean_romanizer

import fastwer
import jamotools
import jiwer
from korean_romanizer.romanizer import Romanizer
import numpy as np


def CER(ground_truth, users):
    '''
    print Char Error Rate between ground_truth & user

    :param ground_truth: ground_truth text(phoneme)
    :param users: users text(phoneme)
    :return: None
    '''
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

    error_part = [{"idx": i, 'ground_truth': k, 'Users': t} for i, k in enumerate(list(ground_truth_char)) for j, t in
                  enumerate(list(hypothesis_char)) if i == j if k != t]
    idx = [i for i, k in enumerate(list(ground_truth_char)) for j, t in enumerate(list(hypothesis_char)) if i == j if
           k != t]
    true = [k for i, k in enumerate(list(ground_truth_char)) for j, t in enumerate(list(hypothesis_char)) if i == j if
            k != t]
    false = [t for i, k in enumerate(list(ground_truth_char)) for j, t in enumerate(list(hypothesis_char)) if i == j if
             k != t]

    print('=' * 30)
    print(f"error_idx:{idx}")
    print("<Modify>")
    print("ordinal ==> change")
    print()

    for i, k in enumerate(idx):
        true_roma = Romanizer("{}".format(ground_truth_char[k - 1:k + 4]))
        user_roma = Romanizer("{}".format(hypothesis_char[k - 1:k + 4]))

        print(
            f"{hypothesis_char[k - 1:k + 4]}({user_roma.romanize()}) ==> {ground_truth_char[k - 1:k + 4]}({true_roma.romanize()})")

    print("=" * 30)
    print('Final')
    print()

    print('Your Pronounce: ', Romanizer("{}".format(hypothesis_char)).romanize())
    print('Right Pronounce: ', Romanizer("{}".format(ground_truth_char)).romanize())

ground_truth = 'ㅅㅓㅇㅅㅜㅋㅐㅈㅣㄴㅡㄴ ㅅㅏㄹㅏㅁㅡ ㄴㅕㄴㅐㄹㅡㄹ ㅎㅏㄷㅏㄱㅏ ㅁㅜㄴㅈㅔㄱㅏ ㅅㅐㅇㄱㅕㅆㅡㄹ ㄸㅐ ㅈㅏㅅㅣㄴㅡㄹ ㄷㅗㄹㅏㅂㅗㄴㅡㄴ ㅅㅏㄹㅏㅁㅣㅇㅑ'
users = 'ㅅㅓㅇㅅㅜㄱㅎㅐㅈㅣㄴㅡㄴ ㅅㅏㄹㅏㅁㅇㅡㄴ ㅇㅕㄴㅇㅐㄹㅡㄹ ㅎㅏㄷㅏㄱㅏ ㅁㅜㄴㅈㅔㄱㅏ ㅅㅐㅇㄱㅕㅆㅇㅡㄹ ㄸㅐ ㅈㅏㅅㅣㄴㅇㅡㄹ ㄷㅗㄹㅇㅏㅂㅗㄴㅡㄴ ㅅㅏㄹㅏㅁㅇㅣㅇㅑ'


CER(ground_truth, users)



