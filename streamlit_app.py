import streamlit as st
from PIL import Image, ImageDraw, ImageFont
from moviepy.editor import VideoFileClip, TextClip, CompositeVideoClip
import random
import os
import numpy as np
from moviepy.video.compositing.concatenate import concatenate_videoclips

# Ensure FFmpeg is available
os.environ["IMAGEIO_FFMPEG_EXE"] = '/opt/homebrew/bin/ffmpeg'  # Adjust this if FFmpeg is in a custom location


# Function to calculate yearly percentages
def calculate_percentages(minutes_music, work_hours, sleep_hours, exercise_hours, hobby_hours):
    total_year_minutes = 525600  # Total minutes in a year (365 days)
    activities_minutes = {
        "Music": minutes_music,
        "Work": work_hours * 60 * 365,
        "Sleep": sleep_hours * 60 * 365,
        "Exercise": exercise_hours * 60 * 365,
        "Hobbies": hobby_hours * 60 * 365,
    }
    percentages = {k: (v / total_year_minutes) * 100 for k, v in activities_minutes.items()}
    return percentages


# Function to create a single slide
def create_slide(stat_title, stat_value, color, width=1080, height=1920):
    image = Image.new("RGB", (width, height), color)
    draw = ImageDraw.Draw(image)

    # Use default fonts (replace with custom fonts for better design)
    title_font = ImageFont.truetype("fonts/Boogaloo-Regular.ttf", 80)  # Replace with your font path
    value_font = ImageFont.truetype("fonts/Boogaloo-Regular.ttf", 100)

    # Calculate text size and position for centering
    title_bbox = draw.textbbox((0, 0), stat_title, font=title_font)
    value_bbox = draw.textbbox((0, 0), stat_value, font=value_font)

    title_width, title_height = title_bbox[2] - title_bbox[0], title_bbox[3] - title_bbox[1]
    value_width, value_height = value_bbox[2] - value_bbox[0], value_bbox[3] - value_bbox[1]

    # Centering the text
    title_x = (width - title_width) // 2
    title_y = (height - title_height) // 2 - 50  # Slightly above center for the title
    value_x = (width - value_width) // 2
    value_y = (height - value_height) // 2 + 50  # Slightly below center for the value

    # Draw the text
    draw.text((title_x, title_y), stat_title, font=title_font, fill="white")
    draw.text((value_x, value_y), stat_value, font=value_font, fill="white")

    return image


# Function to create a video slide with text overlay
def create_video_slide(video_path, stat_title, stat_value, duration=5):
    # Load the video
    clip = VideoFileClip(video_path)

    # Resize video to fit Instagram Story dimensions
    clip = clip.resize((1080, 1920))

    # Create text clips for the title and value
    title_text = TextClip(
        stat_title,
        fontsize=80,
        color="white",
        font="Arial-Bold",  # Ensure this font is installed or change to an available one
        size=(1080, None),  # Centered horizontally
        align="center",
        method="caption",
    ).set_position(("center", "center")).set_duration(duration)

    value_text = TextClip(
        stat_value,
        fontsize=100,
        color="white",
        font="Arial-Bold",  # Ensure this font is installed or change to an available one
        size=(1080, None),
        align="center",
        method="caption",
    ).set_position(("center", "center")).set_duration(duration).set_position(
        lambda t: ("center", 1920 // 2 + 100)  # Slightly below the title
    )

    # Overlay the text onto the video
    final_clip = CompositeVideoClip([clip, title_text, value_text])

    # Set the duration of the final clip
    final_clip = final_clip.set_duration(duration)

    return final_clip


# Function to generate vibrant slides for all stats
def generate_wrapped_slides_with_video(percentages, cool_phrase, video_path):
    slides = []
    for activity, percentage in percentages.items():
        stat_title = f"{activity} Time"
        stat_value = f"{percentage:.2f}%"
        slides.append(create_video_slide(video_path, stat_title, stat_value))
    slides.append(create_video_slide(video_path, "Final Thought", cool_phrase))
    return slides


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

    # Path to the background video
    background_video_path = "background_videos/music.mp4"  # Replace with the path to your video

    # Generate video slides
    slides = generate_wrapped_slides_with_video(percentages, cool_phrase, background_video_path)

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

