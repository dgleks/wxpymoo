# Tts functions, used for cross platform compatibility.
import platform
if platform.system()=="Windows":
    import Tolk
elif platform.system()=="Linux":
    import speechd
elif platform.system()=="Darwin":
    from AppKit import *

def initialize():
    if platform.system()=="Windows":
        Tolk.load()
    elif platform.system()=="Linux":
        vars.client = speechd.SSIPClient("")
    elif platform.system()=="Darwin":
        vars.client=NSSpeechSynthesizer.alloc().initWithVoice_(None)

def say(text, interrupt):
    if platform.system()=="Windows":
        if interrupt==1:
            Tolk.output(text, True)
        else:
            Tolk.output(text)
    elif platform.system()=="Linux":
        if interrupt==1:
            vars.client.cancel()
        vars.client.speak(text)
    elif platform.system()=="Darwin":
        if interrupt:
            vars.client.stopSpeaking()
        vars.client.startSpeakingString_(text)
def deinitialize():
    if platform.system()=="Windows":
        Tolk.unload()
    elif platform.system()=="Linux":
        vars.client.close()
    elif platform.system()=="Darwin":
        vars.client.release()
