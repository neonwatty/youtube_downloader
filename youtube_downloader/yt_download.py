import yt_dlp
from yt_dlp import YoutubeDL
import re


def is_valid_youtube_url(url: str) -> bool:
    if not isinstance(url, str):
        return False
    pattern = r"^https://www\.youtube\.com/watch\?v=[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    if "shorts" in url:
        pattern = r"^https://www\.youtube\.com/shorts/[A-Za-z0-9_-]{11}$"  # youtube vido ids are always 11 chars long
    return re.match(pattern, url) is not None


def download_video(url: str, savedir: str, resolution_dropdown: str, my_proxies: dict = {}) -> str:
    try:
        print("Downloading video from youtube...")
        if is_valid_youtube_url(url):
            with YoutubeDL() as ydl:
                info_dict = ydl.extract_info(url, download=False)
                video_url = info_dict.get("url", None)
                video_id = info_dict.get("id", None)
                video_title = info_dict.get("title", None)
                if video_title is None:
                    savepath = savedir + "/" + video_id + ".mp4"
                else:
                    savepath = savedir + "/" + video_title + ".mp4"

            ydl_opts = {
                "format": "bestvideo+bestaudio/best",
                "merge_output_format": "mp4",
                "outtmpl": savepath,
            }
            if resolution_dropdown == "1080":
                ydl_opts = {
                    "format": "bestvideo[height<=1080]+bestaudio/best",
                    "merge_output_format": "mp4",
                    "outtmpl": savepath,
                }

            if resolution_dropdown == "720":
                ydl_opts = {
                    "format": "bestvideo[height<=720]+bestaudio/best",
                    "merge_output_format": "mp4",
                    "outtmpl": savepath,
                }

            if resolution_dropdown == "360":
                ydl_opts = {
                    "format": "bestvideo[height<=360]+bestaudio/best",
                    "merge_output_format": "mp4",
                    "outtmpl": savepath,
                }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print("...done!")
            return savepath
        else:
            raise ValueError(f"invalid input url: {url}")
    except Exception as e:
        raise ValueError(f"yt_download failed with exception {e}")
