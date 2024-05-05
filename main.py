import subprocess
video_path=""
cmd = [
        'ffmpeg',
        '-i',"downloads/Downloaded_video.mp4",  # Input video file
        '-i', "downloads/Downloaded_video.mp3",  # Input audio file
        '-c:v', 'copy',    # Copy the video stream
        '-c:a', 'aac',     # Encode audio to AAC
        '-strict', 'experimental',
        '-map', '0:v:0',   # Map video stream from the first input
        '-map', '1:a:0',
        "downloads/"       # Map audio stream from the second input
                           # Output file path
    ]

subprocess.run(cmd)