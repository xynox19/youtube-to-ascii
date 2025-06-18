import cv2
import os
import time
import numpy as np
from rich.console import Console
from pytube import YouTube

VIDEO_FILE = "bad_apple.mp4" #change file name as needed for video chosen
USE_YOUTUBE = False  # Set to True to download from YouTube
YOUTUBE_URL = "https://www.youtube.com/watch?v=FtutLA63Cp8" #change url as needed
ASCII_CHARS = "@%#*+=-:. "  # Dark to light for multicolour videos
WIDTH = 120  # Terminal width (adjust as needed)
FPS_LIMIT = 30  # Cap playback FPS

def download_video():
    print("Downloading video from YouTube...")
    yt = YouTube(YOUTUBE_URL)
    stream = yt.streams.filter(res="360p", file_extension="mp4").first()
    stream.download(filename=VIDEO_FILE)
    print("Download complete.")

def frame_to_ascii(image, width=100):
    height = int((image.shape[0] / image.shape[1]) * width * 0.55)
    image = cv2.resize(image, (width, height))
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    ascii_str = ""
    for row in gray:
        for pixel in row:
            ascii_str += ASCII_CHARS[pixel * len(ASCII_CHARS) // 256]
        ascii_str += "\n"
    return ascii_str

def play_ascii_video(video_path):
    console = Console()
    cap = cv2.VideoCapture(video_path)
    fps = cap.get(cv2.CAP_PROP_FPS)
    frame_duration = 1 / min(fps, FPS_LIMIT)

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        ascii_frame = frame_to_ascii(frame, WIDTH)
        console.clear()
        console.print(f"[white on black]{ascii_frame}[/]")
        time.sleep(frame_duration)

    cap.release()

if __name__ == "__main__":
    if USE_YOUTUBE and not os.path.exists(VIDEO_FILE):
        download_video()
    elif not os.path.exists(VIDEO_FILE):
        print(f"ERROR: {VIDEO_FILE} not found. Please download it or enable USE_YOUTUBE.")
        exit(1)

    try:
        play_ascii_video(VIDEO_FILE)
    except KeyboardInterrupt:
        print("\nExiting...")
