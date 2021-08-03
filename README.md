![header](https://capsule-render.vercel.app/api?type=waving&color=auto&height=250&section=header&text=📕2021%20데이터청년캠퍼스%20고려대학교%20과정%204조&fontSize=40)

# 2021 데이터청년캠퍼스 고려대학교 과정 4조

## 팀 소개(Team Members)
- 박근형 (https://github.com/park-geun-hyeong)
- 손소영 (https://github.com/soyeongsohn)
- 이정훈 (https://github.com/hoonww)
- 이종현 (https://github.com/tomtom1103)
- 정세연 (https://github.com/Seyeon-Jeong)

## 프로젝트 소개(About Project)
- Project Name : 외국 청소년을 대상으로 한 한류 아이돌 컨텐츠를 이용한 한국어 발음 능력 향상 서비스
- Description
+추후 pdf

## 레포지토리 구성(About Repository)
### data : 데이터 수집
- pytube: pytube library를 사용하여 유튜브 영상에서 음원추출
- pytube_GUI: pytube와 tkinter를 사용하여 url입력후 버튼을 누르면 자동으로 음원을 추출해주는 GUI환경 구성
- crawling: pytube와 selenium, bs4를 사용하여 유튜브 검색 후 영상에서 음원, 자막 추출
### document : 프리젠테이션 파일, 아이디어 기획 문서 등등

### full_protype : prototype
- full_prototype_ver_1.py : 서비스 프로토타입(to be updated)
- KORtoENG.py : 네이버 파파고 api 이용한 한글->영어 번역 모듈
- romanizer.py : korean_romanizer와 pororo 라이브러리를 사용, 한글->로마자 표기 번역 모듈

### pitch_contour: 음성데이터들의 pitch_contour 비교
- <b>pitch_contour_1</b> : 기존의 음성데이터와 새롭게 녹음한 음성데이터 amplitude 시각화 & spectorgram, intensity, pitch 비교해보기
- <b>pitch_contour_2</b> : pitch_contour_1에서 진행해보았던 내용들을 함수로 일반화시켜 보았고, 추가로 차이가 큰 부분들을 error part를 가정하여 해당하는 time들과 slicing되어진 sample값들을 구하기(ipd.Audio함수를 통해 error part를 직접 들어보았다.)
- <b>Parkdio.py</b> : pitch_contour.ipynb를 바탕으로 비교하고자 하는 두개의 audiofile(path)를 parameter로 넣을경우 plot(vad_plot, cut_plot)들과 array들의 dataframe(show_df), 최종적으로는 acc와 cos_sim을 비교해주는(show_acc) py module이다. <b>(단 두개의 오디오 파일은 22050 sampling을 가지는 wav format file 이여야 한다)</b>
- <b>sample_data</b> : audio.wav ==> 비교적 바르게 읽은 audio file , user.wav ==> 외국인의 입장에서 읽은 audio file (wav format, 22050 sampling)
