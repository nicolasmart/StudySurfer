from classes.audio_analysis import audioAnalyzer
from classes.helper import genSRT
from moviepy.editor import VideoFileClip, AudioFileClip, TextClip, CompositeVideoClip, concatenate
from moviepy.video.tools.subtitles import SubtitlesClip

def getVideo(path:str):
    a = audioAnalyzer()
    genSRT(a.analyzeAudio())
    gameplay = VideoFileClip(path)
    TTSAudio = AudioFileClip('./resources/audio.wav')

    audioDuration = TTSAudio.duration
    gpDuration = gameplay.duration # gameplayDuration = 267.8 for subway surfer
    clipDuration = gpDuration

    ClipList = []
    if audioDuration > gpDuration:
        while audioDuration>gpDuration: #Adds another clip if audio duration is longer than gameplay duration
            if (audioDuration > gpDuration + clipDuration):
                clip = gameplay
                ClipList.append(clip)
                gpDuration += clipDuration
            else: #If adding another full clips is too long, add a subclip of the remaining time left
                clip = gameplay.subclip(0,audioDuration-gpDuration)
                ClipList.append(clip)
                gpDuration += (audioDuration-gpDuration)
        final_clip = concatenate(ClipList)
    else: 
        final_clip = gameplay.subclip(0,TTSAudio.duration)
    final_clip.audio = TTSAudio #Adds audio to video
    
    #Add subtitles
    generator = lambda txt: TextClip(txt, font='Arial-Bold', color = 'white', stroke_color = 'black', stroke_width=1.5, method='caption',fontsize=40,size=[1280,900])
    with open("./resources/subtitles.srt", "r", encoding='utf-8') as f:
        subtitles_data = []
        for line in f:
            if line.strip().isdigit():
                continue
            if '-->' in line:
                start, end = line.strip().split(' --> ')
                start = start.replace(',', '.')
                end = end.replace(',', '.')

                def time_to_seconds(time_str):
                    h, m, s = time_str.split(':')
                    return float(h) * 3600 + float(m) * 60 + float(s)

                subtitles_data.append(((time_to_seconds(start), time_to_seconds(end)), next(f).strip()))
        subtitles = SubtitlesClip(subtitles_data, generator)
    final_clip = CompositeVideoClip([final_clip, subtitles])
    final_clip.write_videofile("./final.mp4")
