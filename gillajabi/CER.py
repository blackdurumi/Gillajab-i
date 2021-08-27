import fastwer
import jamotools
import jiwer
from korean_romanizer.romanizer import Romanizer
import pandas as pd
import streamlit as st
import numpy as np
from error_detect import append_md, print_md, diff, levenshtein

def CER(ground_truth, users):

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
    remove_punc = jiwer.Compose([jiwer.RemovePunctuation()])
    ground_truth_phoneme = ground_truth
    hypothesis_phoneme = users

    ground_truth_char = remove_punc(jamotools.join_jamos(ground_truth_phoneme))
    hypothesis_char = remove_punc(jamotools.join_jamos(hypothesis_phoneme))

    CER_PHONEME = fastwer.score(list(transformation(ground_truth_phoneme)), list(transformation(hypothesis_phoneme)),
                                char_level=True)  ## Phoneme Error Rate
    CER_CHAR = fastwer.score(list(transformation(ground_truth_char)), list(transformation(hypothesis_char)),
                             char_level=True)  ## Char Error Rate

    st.write('\n\n\n')

    acc = ""
    if CER_PHONEME == 0:
        st.write("Perfect")
        st.write("Your Korean is perfect!")
        return None
    elif 0 < CER_PHONEME <= 2:
        acc = "98~99%"
    elif 2 < CER_PHONEME <= 10:
        acc = "90~95%"
    elif CER_PHONEME > 10:
        acc = "Below 90%"

    st.markdown(f"""
                |Accuracy|CER(Character)|CER(Phoneme)|
                |:---:|:---:|:---:|
                |{acc}|{CER_CHAR}|{CER_PHONEME}|""")

    st.write("=" * 30)
    st.markdown('**Comparing Your Pronunciation!**')

    ans, usr, dif = diff(ground_truth, users)

    append_md(ans + " ", "blue")
    print_md()

    for i, phon in enumerate(usr):
        append_md(phon, "black" if dif[i] else "red")
    print_md()


    append_md(Romanizer(ans).romanize(), "black")
    print_md()

    for i, val in enumerate(usr):
        append_md(Romanizer(val).romanize(), "black" if dif[i] else "red")
    print_md()

    dif2 = levenshtein(users, ground_truth)
    append_md(ground_truth + " ", "blue")
    print_md()

    error_count = dict()

    for i, phon in enumerate(users):
        append_md(phon, "black" if dif2[i] else "red")
    print_md()

    for i, phon in enumerate(users):
        if dif2[i] is False and phon is not " ":
            if phon in error_count.keys():
                error_count[phon] += 1
            else:
                error_count[phon] = 1

    error_count = sorted(error_count.items(), key=lambda x: x[1], reverse=True)

    error_num = [i[1] for i in error_count]
    error_phon_kor = [i[0] for i in error_count]
    error_phon_eng = [df[df.kor == k].eng.values[0] for k in error_phon_kor]

    phoneme_error_df = pd.DataFrame(error_phon_kor, error_phon_eng).reset_index()
    phoneme_error_df.columns=['kor','eng']

    phoneme_error_df = [f"{i[1]}({i[0]})" for i in np.array(phoneme_error_df.iloc[:])]

    st.markdown(f"""
                    |Phoneme Error|
                    |:---:|
                    |{phoneme_error_df}|""")

    st.markdown('**The Red Phonemes are where your pronunciation was a bit off. Try again untill your Accuracy is Perfect!** :blush:')
    st.write(" ")
    st.markdown('**The Phoneme Error box is where your phoneme pronunciation was wrong. Try to look at the red phonemes again!**')

    st.write('')


