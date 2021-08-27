import librosa
import librosa.display
import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from recognize import recognize


def display_wav(save_path, speech2text, idolvoice):
    audio_file = open(save_path, "rb")
    audio_bytes = audio_file.read()

    y, sr = librosa.load(save_path)
    S = librosa.feature.melspectrogram(y=y, sr=sr, n_fft=2048)
    S_dB = librosa.power_to_db(S, ref=np.max)

    with st.spinner("Processing your audio..."):
        result, elapsed_time, dur = recognize(save_path, speech2text, idolvoice)
        result_len = len(result)
        empty_len = 5 - result_len

        for _ in range(empty_len):
            result.append("( - )")

        df = pd.DataFrame({f"{elapsed_time:.2f} / {dur:.2f} (sec.)": result})
        df = df.style.set_properties(**{"font-size": "25px"})

        wave_data = pd.DataFrame({"": y})
        st.subheader("This is your Voice Wave!")
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
        st.subheader("This is your Voice Spectrogram!")
        st.pyplot(fig)

        st.subheader("Listen to your pronunciation again!")
        st.audio(audio_bytes, format="audio/wav")

        st.subheader("Top 5 Korean Phoneme Sequence recognized by Gillajob-i!")
        st.table(df)
