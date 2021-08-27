import streamlit as st
from gillajabi_asr import init_model
import os, io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types
from pororo import Pororo
from korean_romanizer.romanizer import Romanizer
import urllib.request
import time
from record_func import record, save_record
from display_wave import display_wav
import json

def mainpage():
    st.header("Your personal Korean pronunciation teacher")
    speech2text = init_model()
    idol = st.selectbox("which idol would you like to see?",
                        ("Select Idol!", "Blackpink", "Solar", "Solar2", "IU", "Taeyeon"))

    if idol == "Select Idol!":
        st.warning("select an idol!")
    else:
        video_file = open(f'./videos/{idol}.mp4', 'rb')
        video_bytes = video_file.read()
        st.video(video_bytes)
        video_audio = f"./videos/{idol}_audio.wav"

        os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = 'client_secret.json'
        client = speech.SpeechClient()

        with io.open(video_audio, 'rb') as audio_file:
            content = audio_file.read()

        audio = types.RecognitionAudio(content=content)
        config = types.RecognitionConfig(
            encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
            language_code='ko-KR')

        response = client.recognize(config, audio)

        for result in response.results:
            global idolvoice
            idolvoice = result.alternatives[0].transcript
            st.markdown("""
                                    <style>
                                    .big-font {
                                        font-size:24px !important;
                                    }
                                    </style>
                                    """, unsafe_allow_html=True)

            st.markdown(f'<p class="big-font">Korean: {idolvoice}</p>', unsafe_allow_html=True)
            g2p = Pororo(task="g2p", lang="ko")
            r = Romanizer(g2p(idolvoice))

            st.markdown(f'<p class="big-font">Romaji: {r.romanize()}</p>', unsafe_allow_html=True)

            encText = urllib.parse.quote(idolvoice)
            data = "source=ko&target=en&text=" + encText
            url = "https://openapi.naver.com/v1/papago/n2mt"
            request = urllib.request.Request(url)
            request.add_header("X-Naver-Client-Id", st.secrets["naver_client_id"])
            request.add_header("X-Naver-Client-Secret", st.secrets["naver_client_secret"])
            response = urllib.request.urlopen(request, data=data.encode("utf-8"))
            rescode = response.getcode()

            if rescode == 200:
                response_body = json.load(response)
                eng_translation = response_body['message']['result']['translatedText']
                st.markdown(f'<p class="big-font">Translation: {eng_translation}</p>',
                            unsafe_allow_html=True)

                st.markdown(
                    '**Pronounce the Korean through reading the Romaji. After clicking the Start Button, you will have 3 seconds to practice!** :kr:')

            else:
                return "Error Code: {}".format(rescode)

        if st.button("Start Gillajab-i!"):

            # bar = st.progress(0)
            # for percent_complete in range(100):
            #     time.sleep(0.03)
            #     bar.progress(percent_complete + 1)
            time.sleep(1)
            st.markdown('**A 5 second recording will Start soon! Get ready** :sunglasses:')
            time.sleep(1)

            for countdown in reversed(range(1, 4)):
                st.markdown(f'**Recording will start in {countdown}**')

                time.sleep(1)

            record_state = st.text('Recording..')
            duration = 5
            fs = 16000
            myrecording = record(duration, fs)

            path_myrecording = f"./output/recording/{idol}.wav"

            save_record(path_myrecording, myrecording, fs)
            record_state.text(f"Done! Gillajob-i is processing your Korean..")

            display_wav(save_path=f"./output/recording/{idol}.wav", speech2text=speech2text, idolvoice=idolvoice)
