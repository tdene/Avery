from bus import Slave, Payload
import settings as setti

import speech_recognition as sr
import snowboydecoder

from threading import Thread

import signal

def getCallback():
    return None

def transcribe(audio):
    r = sr.Recognizer()
    text=None
    try:
        text=r.recognize_google(audio).lower().strip()
    except Exception as e:
        print(e)
        print("Speech Recognition could not understand audio")
    print(text)
    bus.emit(Payload("handleUtterance",{"utterances":[text]},context={"callback":getCallback()}))
    detectWake()

def getUtterance():
# obtain audio from the microphone
    r = sr.Recognizer()
    r.energy_threshold=500
    with sr.Microphone(sample_rate=48000,device_index=2) as source:
        audio = r.listen(source)
#    with open("test2.wav","wb") as f:
#        f.write(audio.get_wav_data())
    transcribe(audio)

interrupted=False

def detectWake():
    def signal_handler(signal, frame):
        global interrupted
        interrupted = True

    def interrupt_callback():
        global interrupted
        return interrupted

    def callback():
        snowboydecoder.play_audio_file(snowboydecoder.DETECT_DING)
        detector.terminate()
        getUtterance()

    models = setti.models

    # capture SIGINT signal, e.g., Ctrl+C
    signal.signal(signal.SIGINT, signal_handler)

    sensitivity = [0.5]*len(models)
    detector = snowboydecoder.HotwordDetector(models, sensitivity=sensitivity)
    callbacks = [callback]*len(models)

    detector.start(detected_callback=callbacks,
                   interrupt_check=interrupt_callback,
                   sleep_time=0.03)

bus=None

def main():
    global bus
    bus=Slave()
    bus.listen(True)
    detectWake()
#    handleUtterance("testing")

if __name__ == "__main__":
    main()
