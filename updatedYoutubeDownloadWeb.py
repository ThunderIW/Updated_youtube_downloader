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
    audio = yt.streams.filter(only_audio=True).first()
    video.download(output_path='downloads', filename="Downloaded_video.mp4")
    audio.download(output_path='downloads', filename="Downloaded_video.mp3")
    cmd = [
        'ffmpeg',
        '-i', "downloads/Downloaded_video.mp4",  # Input video file
        '-i', "downloads/Downloaded_video.mp3",  # Input audio file
        '-c:v', 'copy',  # Copy the video stream
        '-c:a', 'aac',  # Encode audio to AAC
        '-strict', 'experimental',
        '-map', '0:v:0',  # Map video stream from the first input
        '-map', '1:a:0',
        "downloads/video.mp4"  # Map audio stream from the second input
        # Output file path
    ]

    process = subprocess.run(cmd, capture_output=True, text=True)
    if process.returncode == 0:
        st.success("Video and audio have been merged successfully!")
        with open("downloads/video.mp4", "rb") as file:
            btn = st.download_button(label="Download", data=file, file_name=f"{title}.mp4", mime="video/mp4")
    else:
        st.error("Failed to merge video and audio: " + process.stderr)

    os.remove("downloads/video.mp4")
