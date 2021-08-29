![header](https://capsule-render.vercel.app/api?type=waving&color=auto&height=250&section=header&text=📕2021%20데이터청년캠퍼스%20고려대학교%20과정%204조&fontSize=40)

# 길라잡이 : 외국인을 위한 한류 콘텐츠 기반 발음 평가 서비스

## 팀 소개(Team Members)
- 박근형 (https://github.com/park-geun-hyeong)
- 손소영 (https://github.com/soyeongsohn)
- 이정훈 (https://github.com/hoonww)
- 이종현 (https://github.com/tomtom1103)
- 정세연 (https://github.com/Seyeon-Jeong)

## What is Gillajab-i, and why did we make it?

Gillajab-i is a program that helps a non-native Korean in perfecting his/her Korean Pronunciation. Due to the steep popularity rise in K-Pop and all things Korean, the number of non-native Korean learners are at record high. So in order to help these Korean learners, kids from none other than Korea University made this app to help learners prefect their Korean through CAPT (Computer Aided Pronunciation Training).


![](https://github.com/hoonww/DataYouthCampus-Team4/blob/main/gillajabi/images/topik2.png)

## What does it do?

Gillajab-i first lets the user (thats you! 😊) choose from a number of videos featuring their favorite K-content. Then Gillajab-i Automatically recognizes the Audio of the video, then

Automatically recognizes the video audio

Converts the video audio into Korean text

Converts the Korean text into Romaji (for the user to read)

Converts the Korean text into English (for the user to understand)

So that the user can really understand their favorite idol is sayting. After reading the Korean out loud (via Romaji) and practicing his/her pronunciation, the user can click the Start Gillajab-i! button to record her Korean.

After the recording, Gillajab-i automatically detects the users Korean, then

Splits it into Phonemes.

Then, Calculates the pronunciation rate of the user compared to the original pronunciation(of the video) using CER

And highlights where the user's pronunciation was off using Levenshtein distance. Neat huh? 😎

## How does it do it?


First of all, we trained a brand new ASR model that specifies in recognizing the phonemes of the spoken Korean Language.

We used ESPNet, an end-to-end speech recognition toolkit to train our model.


![](https://github.com/hoonww/DataYouthCampus-Team4/blob/main/gillajabi/images/gillajabi_border.png)

First, we collected 1000 hours of raw Korean speaking data, and used Short-time Fourier transforming to convert the audio data into Mel-Spectrograms. The Mel-Spectrograms were then fed into a CNN, thus allowing the model to actually "read the audio!"

![](https://github.com/hoonww/DataYouthCampus-Team4/blob/main/gillajabi/images/stft_mel.png)

Then, the output vectors of the CNN model is fed through 12 layers of Encoding, and 6 Layers of Decoding, and results in a model that is able to detect the phoneme sequence of the Korean Spoken Language!

![](https://github.com/hoonww/DataYouthCampus-Team4/blob/main/gillajabi/images/levenshtein.png)



