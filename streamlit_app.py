import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip, ColorClip
import random
import os
import numpy as np
from moviepy.video.compositing.concatenate import concatenate_videoclips
from stats import calculate_percentages
from visual import generate_wrapped_slides_with_video

# Ensure FFmpeg is available
os.environ["IMAGEIO_FFMPEG_EXE"] = '/opt/homebrew/bin/ffmpeg'  # Adjust this if FFmpeg is in a custom location

# Streamlit App
st.title("Spotify Wrapped-Style Life Stats")
st.markdown("Answer a few questions about your life, and we'll create a vibrant video summarizing your stats!")

# User Inputs
minutes_music = st.number_input("Minutes listening to music per year", min_value=0, value=0)
work_hours = st.slider("Work hours per day", 0, 24, 8)
sleep_hours = st.slider("Sleep hours per day", 0, 24, 8)
exercise_hours = st.slider("Exercise hours per day", 0, 24, 1)
hobby_hours = st.slider("Hobby hours per day", 0, 24, 2)

# Cool phrase input
cool_phrase = st.text_input("Add a cool phrase for your video", "Work hard, play hard!")

# Button to generate the video
if st.button("Generate Spotify Wrapped-Style Video with Background"):
    # Calculate percentages
    percentages = calculate_percentages(minutes_music, work_hours, sleep_hours, exercise_hours, hobby_hours)

    video_paths = [
        "background_videos/music.mp4",
        "background_videos/work.mp4",
        "background_videos/sleep.mp4",
        "background_videos/exercise.mp4",
        "background_videos/hobby.mp4",
        "background_videos/joker.mp4",
    ]

    # Generate video slides
    slides = generate_wrapped_slides_with_video(percentages, cool_phrase, video_paths)

    # Concatenate all video slides into one video
    final_video = concatenate_videoclips(slides)
    temp_video_path = "life_wrapped_with_bg.mp4"
    final_video.write_videofile(temp_video_path, codec="libx264", fps=24)

    # Display the video in Streamlit
    with open(temp_video_path, "rb") as video_file:
        st.video(video_file.read())

    # Allow user to download the video
    with open(temp_video_path, "rb") as video_file:
        st.download_button(
            label="Download Wrapped Video with Background",
            data=video_file,
            file_name="life_wrapped_with_bg.mp4",
            mime="video/mp4",
        )

