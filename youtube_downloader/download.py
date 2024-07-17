from pytube import YouTube
from moviepy.editor import VideoFileClip, AudioFileClip
import requests
import tempfile
import re


def download_joint_stream(yt: YouTube, itag: int, save_dir: str, yt_title: str) -> str:
    try:
        final_save_path = save_dir + "/" + yt_title + ".mp4"
        final_save_path = re.sub(r"[^a-zA-Z0-9./]", " ", final_save_path)
        yt.streams.get_by_itag(itag).download(filename=final_save_path)
        return final_save_path
    except Exception as e:
        raise ValueError(f"download_joint_stream failed with exception {e}")


def download_separate_streams_and_join(yt: YouTube, audio_itag: int, video_itag: int, save_dir: str, yt_title: str) -> str:
    with tempfile.TemporaryDirectory() as tmpdirname:
        tmpaudiopath = tmpdirname + "/" + yt_title + "_audio.mp4"
        tmpaudiopath = re.sub(r"[^a-zA-Z0-9./]", " ", tmpaudiopath)

        tmpvideopath = tmpdirname + "/" + yt_title + "_video.mp4"
        tmpvideopath = re.sub(r"[^a-zA-Z0-9./]", " ", tmpvideopath)

        yt.streams.get_by_itag(audio_itag).download(filename=tmpaudiopath)
        yt.streams.get_by_itag(video_itag).download(filename=tmpvideopath)

        # combine the video clip with the audio clip
        video_clip = VideoFileClip(tmpvideopath)
        audio_clip = AudioFileClip(tmpaudiopath)
        video_clip.audio = audio_clip
        final_save_path = save_dir + "/" + yt_title + ".mp4"
        final_save_path = re.sub(r"[^a-zA-Z0-9./]", " ", final_save_path)
        video_clip.write_videofile(
            final_save_path,
            codec="libx264",
            audio_codec="aac",
            temp_audiofile="temp-audio.m4a",
            remove_temp=True,
        )
    return final_save_path
