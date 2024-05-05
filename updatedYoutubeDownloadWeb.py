import shutil
import os
import subprocess

import streamlit as st
import tempfile
import urllib.request
from moviepy.editor import *

available_res = set()
from pytube import YouTube

st.title("Youtube Downloader")

with st.form("my form"):
    video_url = st.text_input("Enter youtube video link")
    submitted = st.form_submit_button("Submit")

if submitted:
    yt = YouTube(video_url)
    title = yt.title
    author = yt.author

    thumbnail_url = yt.thumbnail_url

    urllib.request.urlretrieve(thumbnail_url, filename="TEST.png")
    shutil.move("TEST.png", "thumbnail")
    st.image("thumbnail/TEST.png")
    st.text(f"Video Title: {title}")
    st.text(f"Video Author: {author}")
    os.remove("thumbnail/TEST.png")

    video = yt.streams.filter(res="1080p").first()
    audio=yt.streams.filter(only_audio=True).first()
    video.download(output_path='downloads',filename="Downloaded_video.mp4")
    audio.download(output_path='downloads',filename="Downloaded_video.mp3")
    video_clip=VideoFileClip("downloads/Downloaded_video.mp4")
    audio_clip=AudioFileClip("downloads/Downloaded_video.mp3")
    final_clip = video_clip.set_audio(audio_clip)
    final_clip.write_videofile("downloads/test.mp4", codec="libx264", audio_codec="aac")

    video_path=r"downloads\test.mp4"
    with open(video_path,"rb") as file:
        btn=st.download_button(label="Download",
                               data=file,file_name=f"{title}.mp4",
                               mime="video/mp4")

    os.remove("downloads/test.mp4")



