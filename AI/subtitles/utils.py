
import time
import math
import os
from faster_whisper import WhisperModel
from moviepy.editor import VideoFileClip


def extract_audio(input_video:str):
    video_clip = VideoFileClip(input_video)

    # Extract the audio from the video clip
    audio_clip = video_clip.audio

    # Write the audio to a separate file
    audio_clip.write_audiofile(f"audio_{str(input_video.split(".")[0])}.wav")

    # Close the video and audio clips
    audio_clip.close()
    video_clip.close()
