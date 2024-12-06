from moviepy.video.VideoClip import ColorClip, TextClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.compositing.concatenate import concatenate_videoclips
from moviepy.video.io.VideoFileClip import VideoFileClip


def create_video_slide(phrase, video_path, stat_title, stat_value, duration=5):
    # Load the background video
    clip = VideoFileClip(video_path)

    # Check if the video is shorter than the slide duration
    if clip.duration < duration:
        # Calculate the number of loops needed
        loops = int(duration // clip.duration) + 1
        # Extend the clip by concatenating itself
        clip = concatenate_videoclips([clip] * loops).subclip(0, duration)
    else:
        # Trim the video to the desired duration
        clip = clip.subclip(0, duration)

    # Resize the video to fit Instagram Story dimensions
    clip = clip.resize((1080, 1920)).loop(duration=duration)

    # Create a semi-transparent background for the text
    text_background_1 = ColorClip(size=(1080, 400), color=(0, 0, 0))  # Black rectangle
    text_background_1 = text_background_1.set_opacity(0.6).set_duration(duration)
    text_background_1 = text_background_1.set_position(("center", 1920 // 5))

    # Create a semi-transparent background for the text
    text_background = ColorClip(size=(1080, 400), color=(0, 0, 0))  # Black rectangle
    text_background = text_background.set_opacity(0.6).set_duration(duration)
    text_background = text_background.set_position(("center", 1920 // 2 - 100))  # Centered horizontally, slightly above center

    phrase_text = TextClip(
        phrase,
        fontsize=80,
        color="white",
        font="fonts/ZenLoop-Regular.ttf",  # Replace with your font path or name
        size=(1080, None),  # Auto-wrap text to fit width
        method="caption",
    ).set_position(("center", 1920 // 2 - 100)).set_duration(duration)

    # Create text clips for the title and value
    title_text = TextClip(
        stat_title,
        fontsize=80,
        color="white",
        font="fonts/Boogaloo-Regular.ttf",  # Replace with your font path or name
        size=(1080, None),  # Auto-wrap text to fit width
        method="caption",
    ).set_position(("center", 1920 // 2 - 100)).set_duration(duration)

    value_text = TextClip(
        stat_value,
        fontsize=100,
        color="white",
        font="fonts/Boogaloo-Regular.ttf",  # Replace with your font path or name
        size=(1080, None),
        method="caption",
    ).set_position(("center", 1920 // 2 + 100)).set_duration(duration)

    # Overlay the text and background onto the video
    final_clip = CompositeVideoClip([clip, text_background_1, phrase_text, text_background, title_text, value_text])

    # Set the duration of the final clip
    final_clip = final_clip.set_duration(duration)

    return final_clip


def generate_wrapped_slides_with_video(percentages, cool_phrase, video_paths):
    slides = []
    for idx, (activity, percentage) in enumerate(percentages.items()):
        stat_title = f"{activity} Time"
        stat_value = f"{percentage:.2f}%"
        video_path = video_paths[idx]  # Use the unique video for this slide
        slides.append(create_video_slide(video_path, stat_title, stat_value))
    slides.append(create_video_slide(video_paths[-1], "Final Thought", cool_phrase))  # Use last video for the final thought
    return slides


def create_music_video_slide(stat_title, stat_value):
    video_path = "background_videos/music.mp4"

    phrases = [
        "Le subes al volumen, pero no le subes a tu vida, ¿qué pasó?",
        "Spotify Premium lo tienes, pero ánimo para chambear, no.",
        "La playlist de llorar en el trabajo no puede faltar.",
        "¿Y si le pones la misma energía a tu vida que a tus playlists?",
        "¿Más tiempo buscando música que buscando trabajo?",
    ]


