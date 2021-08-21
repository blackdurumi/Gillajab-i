import sys, os, re, time
from streamlit import cli as stcli
import streamlit as st
from pydub import AudioSegment
from uuid import uuid4
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import librosa
import librosa.display

from espnet2.bin.asr_inference import Speech2Text
import soundfile


@st.cache(allow_output_mutation=True, suppress_st_warning=True)
def init_model():
    asr_config = "./exp/asr_train_asr_transformer5.aihub_raw_bpe/config.yaml"

    asr_path = "./exp/asr_train_asr_transformer5.aihub_raw_bpe/valid.acc.ave.pth"

    # speech2text = Speech2Text(asr_config, asr_path, lm_config, lm_path, ctc_weight=0.0, lm_weight=0.0, nbest=1)
    # speech2text = Speech2Text(asr_config, asr_path, lm_config, lm_path, ctc_weight=0.0, lm_weight=0.4, beam_size=2, nbest=10, device='cpu')
    speech2text = Speech2Text(
        asr_config,
        asr_path,
        None,
        None,
        ctc_weight=0.3,
        lm_weight=0.0,
        beam_size=3,
        nbest=5,  # 1,
        device="cpu", # "cuda",
    )

    return speech2text


def recognize(audio_path, speech2text):

    # y, sr = librosa.load(audio_path, mono=True, sr=16000)
    # yt, index = librosa.effects.trim(y, top_db=25)

    audio, rate = soundfile.read(audio_path)
    dur = len(audio) / rate
    print("audio : {:d} {:.2f}".format(len(audio), dur))

    # start_trim, end_trim = index
    # audio_trim = audio[start_trim:end_trim]
    # dur_trim = len(audio_trim) / rate

    # print("audio : {:.2f} --> {:.2f}".format(dur, dur_trim))

    start = time.time()
    ret = speech2text(audio)  # Return n-best list of recognized results
    # print(ret)
    end = time.time()

    hyp_sents = []

    for idx_hyp in range(len(ret)):
        hyp_sent, _, _, hyp = ret[idx_hyp]
        hyp_sents.append(hyp_sent)
        # print(hyp)
        print("[{}] ({}), {:.4f}".format(idx_hyp + 1, hyp_sent, hyp.score.item()))

    elapsed_time = end - start
    print("time : {:.8f} (sec.)".format(elapsed_time))

    rtf = elapsed_time / dur
    print("RTF: {:.2f}".format(rtf))

    return hyp_sents, elapsed_time, dur


def display_wav(save_path, speech2text):
    audio_file = open(save_path, "rb")
    audio_bytes = audio_file.read()

    y, sr = librosa.load(save_path)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048)
    S_dB = librosa.power_to_db(S, ref=np.max)

    with st.spinner("음성인식 처리 중 ..."):
        result, elapsed_time, dur = recognize(save_path, speech2text)
        result_len = len(result)
        empty_len = 5 - result_len

        for _ in range(empty_len):
            result.append("( - )")

        df = pd.DataFrame({f"{elapsed_time:.2f} / {dur:.2f} (sec.)": result})
        df = df.style.set_properties(**{"font-size": "25px"})

        wave_data = pd.DataFrame({"": y})
        st.subheader("Wave")
        st.line_chart(wave_data, use_container_width=True)

        fig, ax = plt.subplots(figsize=(25, 5))
        img = librosa.display.specshow(
            S_dB, x_axis="time", y_axis="mel", sr=sr, fmax=8000, ax=ax
        )
        fig.colorbar(
            img,
            ax=ax,
            format="%+2.0f dB",
        )
        st.subheader("Spectrogram")
        st.pyplot(fig)

        st.subheader("Listen audio file")
        st.audio(audio_bytes, format="audio/wav")

        st.subheader("5-Best 음성인식 결과 문장")
        st.table(df)


def save_to_wav(audio_file, file_name, speech2text):
    TIME = "_".join([str(element) for element in time.localtime(time.time())[:6]])
    UUID = str(uuid4())
    ID = TIME + "_" + UUID + "_"

    file_name = re.sub("wav|mp3|flac", "wav", file_name)

    save_dir = "./wavs"
    save_path = os.path.join(save_dir, ID + file_name)

    audio_file.export(save_path, format="wav")
    print(f"Saved File: {save_path}")

    display_wav(save_path, speech2text)


def upload_file(speech2text):
    uploaded_file = st.file_uploader("")

    if uploaded_file:
        file_name = uploaded_file.__dict__["name"]
        file_type = uploaded_file.__dict__["type"]
        audio_file = None

        print(f"Uploaded File Type: {file_type}")

        if re.search("wav|mpeg|flac", file_type):
            audio_file = AudioSegment.from_file(uploaded_file)
        else:
            print("File Type Error")
            st.error("Please upload an Audio File (.wav/.mp3/.flac)")

        if audio_file:
            save_to_wav(audio_file, file_name, speech2text)


def main():
    st.set_page_config(layout="wide")
    st.title("DOWNCAP")
    st.header("Speech To Text")
    st.sidebar.title("DOWNCAP")
    app_mode = st.sidebar.selectbox(
        "", ("Main", "Example 1", "Example 2", "Example 3", "Example 4")
    )

    samples_path = "./samples/sample_exnum.wav"

    speech2text = init_model()

    if app_mode == "Main":
        upload_file(speech2text)
    elif app_mode == "Example 1":
        display_wav(re.sub("exnum", "1", samples_path), speech2text)
    elif app_mode == "Example 2":
        display_wav(re.sub("exnum", "2", samples_path), speech2text)
    elif app_mode == "Example 3":
        display_wav(re.sub("exnum", "3", samples_path), speech2text)
    elif app_mode == "Example 4":
        display_wav(re.sub("exnum", "4", samples_path), speech2text)


if __name__ == "__main__":
    if st._is_running_with_streamlit:
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0], "--server.port", "7001"]
        sys.exit(stcli.main())
