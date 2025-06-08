import wave
import numpy as np
import pyttsx3
from classes.helper import splitParagraph
class audioAnalyzer:
    data = ""
    def __init__(self):
        script = open("./resources/script.txt", "r", encoding="utf8")
        self.data = script.read().replace("\""," ").replace(":",". \n\n\n").replace("–", ". \n\n\n").replace("—", ". \n\n\n").replace(', ','. \n\n\n').replace('\n','. \n\n\n')
        self.getAudio()
        

    def getAudio(self):
        engine = pyttsx3.init() #Generates TTS audio from script.txt
        engine.save_to_file(self.data,"./resources/audio.wav")
        engine.runAndWait()
        engine.stop()
        

    def analyzeAudio(self):
        timing = []
        silence = []
        sentences = splitParagraph(self.data.replace(". \n\n\n",". "))
        raw = wave.open('./resources/audio.wav','r')
        frameData = raw.readframes(-1) #Gets all audio frame data, then converts values into int.
        frameData = np.frombuffer(frameData, dtype ="int16")
        length = len(frameData)
        fps = raw.getframerate()
        raw.close()
        i = 0
        tolerance = 200
        min_silence_frames = 5000
        
        while frameData[i] >= -tolerance and frameData[i] <= tolerance: #Beginning pause
            i+=1
        silence.append([0,i])

        while i in range(i,length): #Period pauses
            if frameData[i] >= -tolerance and frameData[i] <= tolerance:
                start = i
                j = i
                while j in range (i, length):
                    if frameData[j] >= -tolerance and frameData[j] <= tolerance:
                        j+=1
                        i+=1
                    else:
                        if j - start >= min_silence_frames:
                            silence.append([start,j])
                        break
            i+=1
        sLength = len(silence)
        for i in range(0, min(sLength - 1, len(sentences))):
            timing.append([round(silence[i][1] / fps, 3), round(silence[i + 1][0], 3) / fps, sentences[i]])
        if sLength > 0 and len(sentences) > 0:
            timing.append([round(silence[sLength - 1][0] / fps, 3), round(length / fps, 3), sentences[len(sentences) - 1]])  # end of last silence, end of audio clip
        return timing #Returns sentences along with the timing [start, end, sentence] 




