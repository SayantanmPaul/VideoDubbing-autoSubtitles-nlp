import streamlit as st
import moviepy.editor as mp
from moviepy.video.io.VideoFileClip import VideoFileClip
from moviepy.video.VideoClip import TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.tools.subtitles import SubtitlesClip

import tempfile
import os
import sys
import subprocess
import whisper
from whisper.utils import WriteSRT
from pydub import AudioSegment
from pydub.playback import play
import srt
import datetime
from gtts import gTTS


uploaded_file = st.file_uploader("Choose a video...", type=["mp4", "mov"])

if uploaded_file is not None:
    tfile = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4") 
    tfile.write(uploaded_file.read())
    
    my_clip = mp.VideoFileClip(tfile.name)

    temp_video_file = tempfile.NamedTemporaryFile(delete=False, suffix=".mp4")
    my_clip.write_videofile(temp_video_file.name)
    
    st.video(temp_video_file.name)
    
    orginal_audio="orginal_audio.wav"
    my_clip.audio.write_audiofile(orginal_audio)

    model =whisper.load_model("tiny")
    model.device

    result=model.transcribe(orginal_audio)
    print(result)

    output_directory='./'

    srt_writer=WriteSRT(output_directory)
    options = {
        "highlight_words": True,
        "max_line_count": 2,
        "max_line_width": 50
    }
    srt_writer(result, orginal_audio,options=options)

    srt_generated=os.path.join(output_directory,os.path.splitext(os.path.basename(orginal_audio))[0]+'.srt')

    clip=VideoFileClip(temp_video_file.name)

    generator = lambda txt: TextClip(txt, font='Arial', fontsize=24, color='white')
    subtitles = SubtitlesClip(srt_generated, generator)


    final = CompositeVideoClip([clip, subtitles.set_pos(('center', 'bottom'))])

    final.write_videofile("Trim_subtitled.mp4")
    st.video("Trim_subtitled.mp4")