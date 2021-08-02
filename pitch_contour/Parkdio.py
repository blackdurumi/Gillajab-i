# ! pip install praat-parselmouth
# ! pip install webrtcvad
# ! pip install librosa
# ! pip install souncfile

import parselmouth
import webrtcvad
import librosa
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

import soundfile as sf
from numpy import dot
from numpy.linalg import norm

import os
import warnings
warnings.filterwarnings('ignore')

from scipy.io import wavfile
import struct

#import librosa.display
#import IPython.display as ipd

#path = 'C://Users/park1/PycharmProjects/DataCampus/'
#file1 = path+'hello1.wav'
#file2 = path+'hello2.wav'

def sound2array(file1, file2):
    """
    y1 : file1's audio array
    y2 : file2's audio array
    sr1 : file1's audio sample rate
    sr2 : file's audio sample rate

    if your wav file has 2 channel(stereo) you have to change 1 channel(mono) for webrtcvad

    :param file1: file1's path
    :param file2: file2's path
    :return: y1,y2,sr1,sr2
    """
    sr1, y1 = wavfile.read(file1)
    sr2, y2 = wavfile.read(file2)

    if len(y1.shape) == 2:
        y1 = y1[:, 0] ## from stereo to mono type(2channel ==> 1channel)

    if len(y2.shape) == 2:
        y2 = y2[:,  0]

    return y1, y2, sr1, sr2

def vad(samples, sample_rate=16000):

    """
    speech_samples: is_speech audio array(have audio amplitude)


    window_duration 10, 20, or 30 ms only(audio frame)

    :param samples: audio array(WebRTCVAD only accepts 16-bit mono PCM audio) - only 1 channel
    :param sample_rate: audio sample rate(WebRTCVAD only accepts 8000, 16000, 32000 or 48000 Hz sampled audio)
    :return: speech_samples
    """
    vad = webrtcvad.Vad()
    vad.set_mode(3)

    raw_samples = struct.pack("%dh" % len(samples), *samples)

    window_duration = 0.01  # duration in seconds
    samples_per_window = int(window_duration * sample_rate + 0.5)
    bytes_per_sample = 2

    segments = []

    for i, start in enumerate(np.arange(0, len(samples), samples_per_window)):
        stop = min(start + samples_per_window, len(samples))

        if stop == len(samples):
            break

        is_speech = vad.is_speech(raw_samples[start * bytes_per_sample: stop * bytes_per_sample],
                                  sample_rate=sample_rate)
        segments.append({'start': start, 'stop': stop, 'is_speech': is_speech})

    speech_samples = np.concatenate(
        [samples[segment['start']:segment['stop']] for segment in segments if segment['is_speech']])

    start = []
    end = []
    for segment in segments:
        if segment['is_speech']:
            if samples[segment['start']] > 3000:
                start.append(segment['start'])
                end.append(segment['stop'])

    # print(f"start:{np.round(np.min(start)/22050, 2)} sec, stop:{np.round(np.max(end)/22050, 2)} sec")

    return speech_samples


def vad_plot(samples, sample_rate=16000):
    """
    show entire amplitude plot of audio & line of is_speech part

    :param samples: audio array(WebRTCVAD only accepts 16-bit mono PCM audio)
    :param sample_rate: audio sample rate(WebRTCVAD only accepts 8000, 16000, 32000 or 48000 Hz sampled audio)
    :return: plot
    """
    vad = webrtcvad.Vad()
    vad.set_mode(3)

    raw_samples = struct.pack("%dh" % len(samples), *samples)

    window_duration = 0.01  # duration in seconds
    samples_per_window = int(window_duration * sample_rate + 0.5)
    bytes_per_sample = 2

    segments = []

    for i, start in enumerate(np.arange(0, len(samples), samples_per_window)):
        stop = min(start + samples_per_window, len(samples))

        if stop == len(samples):
            break

        is_speech = vad.is_speech(raw_samples[start * bytes_per_sample: stop * bytes_per_sample],
                                  sample_rate=sample_rate)
        segments.append({'start': start, 'stop': stop, 'is_speech': is_speech})

    plt.figure(figsize=(14, 5))
    plt.plot(samples, color='lightcoral')

    ymax = max(samples)

    # plot segment identifed as speech
    for segment in segments:
        if segment['is_speech']:
            plt.plot([segment['start'], segment['stop'] - 1], [ymax * 1.1, ymax * 1.1], color='cornflowerblue')

    plt.xlabel('sample')
    plt.grid()
    plt.show()

def cut_time(samples, sample_rate=16000):
    """
    s: start time(sec) of is_speech part
    e: end time(sec) of is_speech part

    :param samples: audio array(WebRTCVAD only accepts 16-bit mono PCM audio)
    :param sample_rate: audio sample rate(WebRTCVAD only accepts 8000, 16000, 32000 or 48000 Hz sampled audio)
    :return: s, e
    """
    vad = webrtcvad.Vad()
    vad.set_mode(3)

    raw_samples = struct.pack("%dh" % len(samples), *samples)

    window_duration = 0.01  # duration in seconds
    samples_per_window = int(window_duration * sample_rate + 0.5)
    bytes_per_sample = 2

    segments = []

    for i, start in enumerate(np.arange(0, len(samples), samples_per_window)):
        stop = min(start + samples_per_window, len(samples))

        if stop == len(samples):
            break

        is_speech = vad.is_speech(raw_samples[start * bytes_per_sample: stop * bytes_per_sample],
                                  sample_rate=sample_rate)
        segments.append({'start': start, 'stop': stop, 'is_speech': is_speech})

    speech_samples = np.concatenate(
        [samples[segment['start']:segment['stop']] for segment in segments if segment['is_speech']])

    start = []
    end = []
    for segment in segments:
        if segment['is_speech']:
            if samples[segment['start']] > 3000:
                start.append(segment['start'])
                end.append(segment['stop'])

    # print(f"start:{np.round(np.min(start)/22050, 2)} sec, stop:{np.round(np.max(end)/22050, 2)} sec")

    s = np.float(np.round(np.min(start) / 22050, 2))
    e = np.float(np.round(np.max(end) / 22050, 2))

    return s, e


def draw_spectrogram(spectrogram, dynamic_range=70):
    """
    show spectrogram plot of audio array

    :param spectrogram:  spectrogram of audio_array(parselmouth.Sound().to_spectrogram())
    :param dynamic_range:
    :return: plot
    """
    X, Y = spectrogram.x_grid(), spectrogram.y_grid()
    sg_db = 10 * np.log10(spectrogram.values)
    plt.pcolormesh(X, Y, sg_db, vmin=sg_db.max() - dynamic_range, cmap='afmhot')
    plt.ylim([spectrogram.ymin, spectrogram.ymax])
    plt.xlabel("time [s]")
    plt.ylabel("frequency [Hz]")


def draw_intensity(intensity):
    """
    show intensity plot of audio array

    :param intensity: intensity of audio_array(parselmouth.Sound().to_intensity())
    :return: plot
    """
    plt.plot(intensity.xs(), intensity.values.T, linewidth=3, color='w')
    plt.plot(intensity.xs(), intensity.values.T, linewidth=1)
    plt.grid(False)
    plt.ylim(0)
    plt.ylabel("intensity [dB]")


def draw_pitch(pitch):

    """

    show pitch plot of audio array

    :param pitch: pitch of audio_array(parselmouth.Sound().to_intensity())
    :return: plot
    """
    # Extract selected pitch contour, and
    # replace unvoiced samples by NaN to not plot
    pitch_values = pitch.selected_array['frequency']
    pitch_values[pitch_values == 0] = np.nan
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=5, color='w')
    plt.plot(pitch.xs(), pitch_values, 'o', markersize=2)
    plt.grid(False)
    plt.ylim(0, pitch.ceiling)
    plt.ylabel("fundamental frequency [Hz]")


def cut_plot(file1, file2):

    """

    show plot of amplitude, intensity, pitch, spectrogram of is_speech part


    :param file1: file1' path
    :param file2: file2's path
    :return: plot(amplitude, intensity, pitch, spectrogram)
    """

    y1,y2,sr1,sr2 = sound2array(file1, file2)

    s1, e1 = cut_time(y1)
    s2, e2 = cut_time(y2)

    snd1 = parselmouth.Sound(file1)
    snd2 = parselmouth.Sound(file2)

    snd_part1 = snd1.extract_part(from_time=s1, to_time=e1)  ## VAD
    snd_part2 = snd2.extract_part(from_time=s2, to_time=e2)

    intensity1 = snd_part1.to_intensity()
    intensity2 = snd_part2.to_intensity()

    spectrogram1 = snd_part1.to_spectrogram()
    spectrogram2 = snd_part2.to_spectrogram()

    pitch1 = snd_part1.to_pitch()
    pitch2 = snd_part2.to_pitch()

    plt.figure(figsize=(14, 5))
    plt.plot(snd_part1.xs(), snd_part1.values.T, linewidth=0.5, color='violet')
    plt.xlim([snd_part1.xmin, snd_part1.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    plt.show()

    plt.figure(figsize=(14, 5))
    plt.plot(snd_part2.xs(), snd_part2.values.T, linewidth=0.5, color='limegreen')
    plt.xlim([snd_part2.xmin, snd_part2.xmax])
    plt.xlabel("time [s]")
    plt.ylabel("amplitude")
    plt.show()

    plt.figure(figsize=(14, 5))
    draw_spectrogram(spectrogram1)
    plt.twinx()
    draw_intensity(intensity1)
    plt.xlim([snd_part1.xmin, snd_part1.xmax])
    plt.title('hello1 spectrogram&intensity')
    plt.show()

    plt.figure(figsize=(14, 5))
    draw_spectrogram(spectrogram2)
    plt.twinx()
    draw_intensity(intensity2)
    plt.xlim([snd_part2.xmin, snd_part2.xmax])
    plt.title('hello2 spectrogram&intensity')
    plt.show()

    plt.figure(figsize=(14, 5))
    draw_spectrogram(spectrogram1)
    plt.twinx()
    draw_pitch(pitch1)
    plt.title("hello1 spectrogram & pitch")

    plt.figure(figsize=(14, 5))
    draw_spectrogram(spectrogram2)
    plt.twinx()
    draw_pitch(pitch2)
    plt.title("hello2 spectrogram & pitch")


def show_df(file1, file2):
    """
    df1 : DataFrame of sec, audio1's intensity(is_speech), audio2's intensity(is_speech)
    df2 : DataFrame of sec, audio1's pitch(is_speech), audio2's pitch(is_speech)
    
    
        
    :param file1: file1's path
    :param file2: file2's path
    :return: df1, df2
    """
    y1,y2,sr1,sr2= sound2array(file1,file2)

    s1, e1 = cut_time(y1)
    s2, e2 = cut_time(y2)

    snd1 = parselmouth.Sound(file1)
    snd2 = parselmouth.Sound(file2)

    snd_part1 = snd1.extract_part(from_time=s1, to_time=e1)  ## VAD
    snd_part2 = snd2.extract_part(from_time=s2, to_time=e2)

    intensity1 = snd_part1.to_intensity()
    intensity2 = snd_part2.to_intensity()

    spectrogram1 = snd_part1.to_spectrogram()
    spectrogram2 = snd_part2.to_spectrogram()

    pitch1 = snd_part1.to_pitch()
    pitch2 = snd_part2.to_pitch()

    z1 = e1 - s1
    z2 = e2 - s2

    ##  is_speech 구간이 작은쪽을 기준으로 dataframe 구성

    if z1 < z2:
        intensity_sep = np.float(round((e1 - s1) / intensity1.values.shape[1], 5))
        pitch_sep = np.float(round((e1 - s1) / pitch1.selected_array['frequency'].shape[0], 5))

        intensity_sec = np.arange(s1, e1, intensity_sep)[:-1]
        pitch_sec = np.arange(s1, e1, pitch_sep)[:-1]

        dict1 = {'sec': intensity_sec,
                 'intensity1': intensity1.values.reshape(-1, ),
                 'intensity2': intensity2.values.reshape(-1)[:intensity1.values.reshape(-1).shape[0]]
                 }

        dict2 = {
            'sec': pitch_sec,
            'pitch1': pitch1.selected_array['frequency'],
            'pitch2': pitch2.selected_array['frequency'][:pitch1.selected_array['frequency'].shape[0]]
        }

        df1 = pd.DataFrame.from_dict(dict1, orient='index').transpose()
        df2 = pd.DataFrame.from_dict(dict2, orient='index').transpose()


    else:

        intensity_sep = np.float(round((e2 - s2) / intensity1.values.shape[1], 5))
        pitch_sep = np.float(round((e2 - s2) / pitch1.selected_array['frequency'].shape[0], 5))

        intensity_sec = np.arange(s2, e2, intensity_sep)[:-1]
        pitch_sec = np.arange(s2, e2, pitch_sep)[:-1]

        dict1 = {'sec': intensity_sec,
                 'intensity1': intensity1.values.reshape(-1, )[:intensity2.values.reshape(-1).shape[0]],
                 'intensity2': intensity2.values.reshape(-1)
                 }

        dict2 = {
            'sec': pitch_sec,
            'pitch1': pitch1.selected_array['frequency'][:pitch2.selected_array['frequency'].shape[0]],
            'pitch2': pitch2.selected_array['frequency']
        }

        df1 = pd.DataFrame.from_dict(dict1, orient='index').transpose()
        df2 = pd.DataFrame.from_dict(dict2, orient='index').transpose()
    
    ## 혹시 모를 null값을 위한 padding 처리
    df1.fillna(method='pad', inplace=True)
    df2.fillna(method='pad', inplace=True)

    return df1, df2


def show_error_part(file1, file2):
    """
    i assume error part if intensity_sub & pitch_sub over 90% of sub_list

    intensity_error_part : audio array that has intensity error
    pitch_error_part : audio array that has pitch error


    :param file1: file1's path
    :param file2: file2's path
    :return: intensity_error_part, pitch_error_part
    """
    y1,y2,sr1,sr2 = sound2array(file1, file2)

    df1, df2 = show_df(file1, file2)

    intensity_sub = []
    pitch_sub = []

    for a, b in df1.iloc[:, 1:].values:
        intensity_sub.append(np.abs(a - b))

    for a, b in df2.iloc[:, 1:].values:
        pitch_sub.append(np.abs(a - b))


    intensity_error_standard = np.percentile(intensity_sub, 90)
    pitch_error_standard = np.percentile(pitch_sub, 90)

    intensity_error_idx = [i for i, k in enumerate(intensity_sub) if k > intensity_error_standard]
    pitch_error_idx = [i for i, k in enumerate(pitch_sub) if k > pitch_error_standard]

    intensity_error_sec = df1.sec.loc[intensity_error_idx].values
    pitch_error_sec = df2.sec.loc[pitch_error_idx].values

    intensity_error_part = y2[round(np.min(intensity_error_sec) * sr1):round(np.max(intensity_error_sec) * sr1)]
    pitch_error_part = y2[round(np.min(pitch_error_sec) * sr1):round(np.max(pitch_error_sec) * sr1)]

    return intensity_error_part, pitch_error_part


def show_acc(file1, file2):
    """
    print accuracy & cosine similarity of audio files
    accuracy: 1 - len(error_part)/len(is_speech_part)

    :param file1: file1's path
    :param file2: file2's path
    :return: None
    """
    y1,y2,sr1,sr2 = sound2array(file1, file2)

    intensity_error_part, pitch_error_part = show_error_part(file1, file2)
    df1, df2 = show_df(file1, file2)

    intensity1 = df1.iloc[:, 1].values
    intensity2 = df1.iloc[:, 2].values

    pitch1 = df2.iloc[:, 1].values
    pitch2 = df2.iloc[:, 2].values

    intensity_cos_sim = (dot(intensity1, intensity2) / (norm(intensity1) * norm(intensity2))) * 100
    pitch_cos_sim = (dot(pitch1, pitch2) / (norm(pitch1) * norm(pitch2))) * 100

    intensity_acc = 100 - ((len(intensity_error_part) / len(vad(y2))) * 100)
    pitch_acc = 100 - ((len(pitch_error_part) / len(vad(y2))) * 100)

    print(f'intensity_acc : {intensity_acc :.4f} %')
    print(f'pitch_acc : {pitch_acc :.4f} %')
    print('=' * 50)
    print(f"intensity_cos_sim:{intensity_cos_sim:.4f} %")
    print(f"pitch_cos_sim: {pitch_cos_sim:.4f} %")

