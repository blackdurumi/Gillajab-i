import jamotools
import streamlit as st

all_md=list()

def print_md():
    st.markdown(''.join(all_md), unsafe_allow_html=True)
    while all_md:
        all_md.pop()


def append_md(string, color):
    all_md.append('<span style="color:{}">{}</span>'.format(color, string))

def levenshtein(cor, ans):
    """
    Detecting error in word using Levenshtein distance(Edit distance)
    :param cor: user spoken word
    :param ans: answer word
    :return: Boolean List which is True when the index of cor is an error, False otherwise
    """
    D = [[0 for _ in range(len(ans) + 1)] for _ in range(len(cor) + 1)]
    n = len(cor)
    m = len(ans)
    ret = [False for _ in range(len(cor) + 1)]

    # making levenshtein distance matrix
    for i in range(m):
        D[0][i + 1] = i + 1
    for i in range(n):
        D[i + 1][0] = i + 1

    for i in range(1, n + 1):
        for j in range(1, m + 1):
            cost = 0 if cor[i - 1] == ans[j - 1] else 1
            D[i][j] = min(D[i][j - 1] + 1, D[i - 1][j] + 1, D[i - 1][j - 1] + cost)

    # backtracking to find error index
    x = n
    y = m
    while x and y:
        if cor[x - 1] == ans[y - 1]:
            ret[x - 1] = True
            x -= 1
            y -= 1
        else:
            if D[x - 1][y] < D[x][y - 1]:
                x -= 1
            else:
                y -= 1

    return ret


def diff(ground_truth, users):
    ground_truth_phoneme = ground_truth
    hypothesis_phoneme = users

    ground_truth_char = jamotools.join_jamos(ground_truth_phoneme)
    hypothesis_char = jamotools.join_jamos(hypothesis_phoneme)

    ret = levenshtein(hypothesis_char, ground_truth_char)

    return ground_truth_char, hypothesis_char, ret
