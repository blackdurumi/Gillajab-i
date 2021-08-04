# !pip install --upgrade google-cloud-speech==1.3.2
import os
import io
from google.cloud import speech
from google.cloud.speech import enums
from google.cloud.speech import types

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "./voltaic-day-321901-f0ba9adaf731.json"

# STT에 사용할 파일 지정
speech_file = "./example.wav"

if __name__ == "__main__":
    """Transcribe the given audio file."""
    client = speech.SpeechClient()

    with io.open(speech_file, 'rb') as audio_file:
        content = audio_file.read()

    audio = types.RecognitionAudio(content=content)
    # 여기에서는 오디오 인코딩 방식과 샘플레이트를 지정해야함
    config = types.RecognitionConfig(
        encoding=enums.RecognitionConfig.AudioEncoding.LINEAR16,
        # encoding=enums.RecognitionConfig.AudioEncoding.FLAC,
        sample_rate_hertz=16000,
        # enableWordTimeOffsets=True,
        language_code='ko-KR')

    response = client.recognize(config, audio)

    for result in response.results:
        print(u'Transcript: {}'.format(result.alternatives[0].transcript))
        print(u'Confidence: {}'.format(result.alternatives[0].confidence))