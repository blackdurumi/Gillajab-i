import streamlit as st
import pandas as pd
from PIL import Image

topik = Image.open('./images/topik2.png')
model = Image.open('./images/gillajabi_border.png')
stft = Image.open('./images/stft.png')
cnn = Image.open('./images/cnn.png')

def info():

    st.markdown(
        """## What is Gillajab-i, and why did we make it?
        
Gillajab-i is a program that helps a non-native Korean in perfecting his/her Korean Pronunciation.
Due to the steep popularity rise in K-Pop and all things Korean, the number of
non-native Korean learners are at record high. So in order to help these Korean learners,
kids from none other than Korea University made this app to help learners prefect their Korean
through CAPT (Computer Aided Pronunciation Training).
        """, unsafe_allow_html=True,
    )

    st.image(topik, caption="Rise in TOPIK (Test of Proficiency in Korean) participants, 1997-2009")

    st.markdown(
        """## What does it do?

Gillajab-i first lets the user (thats you! :blush:) choose from a number of videos featuring their favorite
K-content. Then Gillajab-i Automatically recognizes the Audio of the video, then
        
        
        
        """, unsafe_allow_html=True)
    st.markdown(
        """
1. Automatically recognizes the video audio

2. Converts the video audio into Korean text

3. Converts the Korean text into Romaji (for the user to read)

4. Converts the Korean text into English (for the user to understand)
        """
    )

    st.markdown(
        """
So that the user can **really** understand their favorite idol is sayting.
After reading the Korean out loud (via Romaji) and practicing his/her pronunciation,
the user can click the **Start Gillajab-i!** button to record her Korean.

After the recording, Gillajab-i automatically detects the users Korean, then

1. Splits it into Phonemes.

2. Then, Calculates the pronunciation rate of the user compared to the original pronunciation(of the video)
using CER

3. And highlights where the user's pronunciation was off using Levenshtein distance. Neat huh? :sunglasses:
        """

    )

    st.markdown(
        """## How does it do it?
First of all, we trained a brand new ASR model that specifies in recognizing the **phonemes** of the
spoken Korean Language.

We used ESPNet, an end-to-end speech recognition toolkit to train our model.
        """
    )
    st.image(model)

    st.markdown(
        """
First, we collected 1000 hours of raw Korean speaking data, and used Short-time Fourier transforming to
convert the audio data into Mel-Spectrograms.
        """

    )
    st.image(stft)

    st.markdown(
        """
Then, the Mel-Spectrogram image was fed into a CNN model.
        """
    )

    st.image(cnn)

    st.markdown(
        """
Then, the output vectors of the CNN model is fed through 12 layers of Encoding, and 6 Layers of Decoding,
and results in a model that is able to detect the phoneme sequence of the Korean Spoken Language!
        """
    )
