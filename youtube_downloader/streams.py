from typing import Tuple
from pytube import YouTube
from pytube.query import StreamQuery
import re


def is_valid_youtube_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    pattern = r"^https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    if "shorts" in url:
        pattern = r"^https://www\.youtube\.com/shorts/[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    return re.match(pattern, url) is not None


def get_yt_streams(url: str, my_proxies: dict = {}) -> Tuple[YouTube, str, str, StreamQuery, StreamQuery, StreamQuery]:
    try:
        # validate url
        if is_valid_youtube_url(url):
            # load in video
            yt = YouTube(url, proxies=my_proxies)

            # audio only streams
            audio_only_streams = yt.streams.filter(file_extension="mp4", only_audio=True, type="audio").order_by("abr").asc()

            # video only streams
            video_only_streams = yt.streams.filter(file_extension="mp4", only_video=True, type="video").order_by("resolution").asc()

            # audio and video joint streams
            audio_video_streams = (
                yt.streams.filter(
                    file_extension="mp4",
                    only_audio=False,
                    only_video=False,
                    progressive=True,
                    type="video",
                )
                .order_by("resolution")
                .asc()
            )

            # get title and thumbnail
            yt_title = yt.title.replace("/", " ")
            yt_thumbnail_url = yt.thumbnail_url

            return (
                yt,
                yt_title,
                yt_thumbnail_url,
                audio_only_streams,
                video_only_streams,
                audio_video_streams,
            )
        else:
            raise ValueError(f"invalid input url: {url}")
    except Exception as e:
        raise ValueError(f"get_yt_streams failed with exception {e}")
