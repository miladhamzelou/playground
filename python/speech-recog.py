import speech_recognition as sr
print(sr.__version__)

# wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/harvard.wav
# wget https://github.com/realpython/python-speech-recognition/raw/master/audio_files/jackhammer.wav
r = sr.Recognizer()

# print('--------------------------------------------------------------------------------')
# with sr.AudioFile('harvard.wav') as source:
#     audio = r.record(source, duration=10)
#     print(r.recognize_google(audio))


# print('--------------------------------------------------------------------------------')
# with sr.AudioFile('jackhammer.wav') as source:
#     r.adjust_for_ambient_noise(source, duration=0.5)
#     audio = r.record(source)
#     print(r.recognize_google(audio))

# print('--------------------------------------------------------------------------------')
# with sr.AudioFile('jackhammer.wav') as source:
#     r.adjust_for_ambient_noise(source, duration=0.5)
#     audio = r.record(source)
#     print(r.recognize_google(audio, show_all=True))

print('--------------------------------------------------------------------------------')
print(sr.Microphone.list_microphone_names())
with sr.Microphone() as source:
    r.adjust_for_ambient_noise(source)
    audio = r.listen(source)
    try:
        print(r.recognize_google(audio))
    except:
        print("error: ")
