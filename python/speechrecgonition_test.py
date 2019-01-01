import unittest
import speech_recognition as sr
# sudo apt install libportaudio19-dev
# wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav
class SpeechRecognitionTestase(unittest.TestCase):
    def test_case1(self):
        r = sr.Recognizer()
        with sr.AudioFile('harvard.wav') as source:
            audio = r.record(source, duration=10)
            print(r.recognize_google(audio))
        with sr.Microphone() as source:
            r.adjust_for_ambient_noise(source)
            print("listen")
            audio = r.listen(source)
            try:
                print(r.recognize_google(audio))
            except:
                print("error: ")
