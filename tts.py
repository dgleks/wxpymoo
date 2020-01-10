# Tts functions, used for cross platform compatibility.
import platform
if platform.system()=="Windows":
    import Tolk
elif platform.system()=="Linux":
    import speechd
elif platform.system()=="Darwin":
    from AppKit import *
client = None
def initialize():
    global client
    if platform.system()=="Windows":
        Tolk.load()
    elif platform.system()=="Linux":
        client = speechd.SSIPClient("")
    elif platform.system()=="Darwin":
        client=NSSpeechSynthesizer.alloc().initWithVoice_(None)

def say(text, interrupt):
    if platform.system()=="Windows":
        if interrupt==1:
            Tolk.output(text, True)
        else:
            Tolk.output(text)
    elif platform.system()=="Linux":
        if interrupt==1:
            client.cancel()
        client.speak(text)
    elif platform.system()=="Darwin":
        if interrupt:
            client.stopSpeaking()
        client.startSpeakingString_(text)
def deinitialize():
    if platform.system()=="Windows":
        Tolk.unload()
    elif platform.system()=="Linux":
        client.close()
    elif platform.system()=="Darwin":
        client.release()
