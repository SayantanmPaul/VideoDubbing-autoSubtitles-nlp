import os
import sys
import subprocess
import moviepy.editor as mp

clip_path = "demo.mp4"
my_clip = mp.VideoFileClip(clip_path)
my_clip.audio.write_audiofile(r"my_result.wav")

import speech_recognition as sr
r = sr.Recognizer()

with sr.AudioFile('my_result.wav') as source:
    audio = r.record(source)
    try:
        audio_text = r.recognize_google(audio)
        print(audio_text)
    except sr.UnknownValueError:
        print("404 error no input",UnknownValueError)
    except sr.RequestError:
        print("402 error from api",UnknownValueError)

import speech_recognition as spr
from googletrans import Translator
from gtts import gTTS

recog1 = spr.Recognizer()

with spr.AudioFile('my_result.wav') as source:
  recog1.adjust_for_ambient_noise(source, duration=0.02)
  audio = recog1.record(source)
  try:
    audio_text = recog1.recognize_google(audio)
    audio_text = audio_text.lower()
  except recog1.UnknownValueError:
    print("404 error no input")
  except recog1.RequestError:
    print("402 error from api")

translator=Translator()

from_lang = 'en'
to_lang = 'hi'

tts = gTTS(text=translator.translate(audio_text, src=from_lang, dest=to_lang).text, lang=to_lang,  tld='co.in' , slow=False)
tts.save("insider.mp3")

translated_clip = mp.VideoFileClip(r"demo.mp4")
translated_audio = mp.AudioFileClip(r"insider.mp3")
final_clip = translated_clip.set_audio(translated_audio)
final_clip.write_videofile(r"insider.mp4", codec="libx264", audio_codec="aac")

import whisper
from whisper.utils import get_writer
model =whisper.load_model("tiny")

model.device

def audioconversion(my_clip, output_ext="mp3"):
  filename, ext=os.path.splitext(my_clip)
  subprocess.call(["ffmpeg", "-y", "-i", my_clip, f"{filename}.{output_ext}"], stdout=subprocess.DEVNULL,stderr=subprocess.STDOUT)
  return f"{filename}.{output_ext}"

clip="./demo.mp4"
audio_file = audioconversion(clip)

result=model.transcribe(audio_file)
print(result)
output_directory = "./"

vtt_writer=whisper.utils.WriteVTT(output_directory)
options = {
    "highlight_words": True,
    "max_line_count": 2,
    "max_line_width": 50
}
vtt_writer(result, clip,options=options)

from base64 import b64encode
from IPython.display import HTML

target_vd="insider.mp4"
subbtitled_path="demo.vtt"

with open(target_vd, 'rb') as f:
      video_data = f.read()
      video_base64 = b64encode(video_data).decode()

with open(subbtitled_path, 'r') as f:
      captions_data = f.read()
      captions_base64 = b64encode(captions_data.encode('utf-8')).decode()

video_html = f"""
  <video width="640" height="360" controls>
      <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
      <track src="data:text/vtt;base64,{captions_base64}" kind="captions" srclang="en" label="English" default>
  </video>
  """

HTML(video_html)