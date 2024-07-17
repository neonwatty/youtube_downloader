import io
import tempfile
from youtube_downloader.yt_download import download_video
import gradio as gr

video_choices = ["best", "1080", "720", "360"]


print("Setting up Gradio interface...")
with gr.Blocks(theme=gr.themes.Soft(), title=" youtube downloader") as demo:
    with gr.Tabs():
        with gr.TabItem("youtube downloader"):
            with tempfile.TemporaryDirectory() as tmpdirname:
                with gr.Row():
                    with gr.Column(scale=4):
                        url_input = gr.Textbox(
                            value="https://www.youtube.com/shorts/43BhDHYBG0o",
                            label="🔗 Paste YouTube / Shorts URL here",
                            placeholder="e.g., https://www.youtube.com/watch?v=.",
                            max_lines=1,
                        )
                    with gr.Column(scale=3):
                        resolution_dropdown = gr.Dropdown(
                            choices=video_choices, value="best", label="video resolution", info="choose video resolution", interactive=True
                        )

                    with gr.Column(scale=2):
                        download_button = gr.Button("download", variant="primary")

                with gr.Row():
                    og_video = gr.Video(
                        visible=True,
                        show_download_button=True,
                        show_label=True,
                        label="your video",
                        format="mp4",
                        width="50vw",
                        height="50vw",
                    )

                @download_button.click(inputs=[url_input, resolution_dropdown], outputs=[og_video])
                def download_this(url_input, resolution_dropdown):
                    temporary_video_location = download_video(url_input, tmpdirname, resolution_dropdown)

                    filename = open(temporary_video_location, "rb")
                    byte_file = io.BytesIO(filename.read())
                    with open(temporary_video_location, "wb") as out:
                        out.write(byte_file.read())

                    new_og_video = gr.Video(
                        value=temporary_video_location,
                        visible=True,
                        show_download_button=True,
                        show_label=True,
                        label="your video",
                        format="mp4",
                        width="50vw",
                        height="50vw",
                    )

                    return new_og_video

        with gr.TabItem("💡 About"):
            with gr.Blocks() as about:
                gr.Markdown(
                    (
                        "### About \n"
                        "Some notes on how this works: \n\n"
                        "1.  **youtube / google login**: you do **not** need to be logged into a google account to use the app, with one exception: age restricted videos"
                        "2.  **age restricted videos**: this app cannot fetch age restricted videos yet, which requires a user login to google / youtube - this feature is not yet available"
                        "3.  **video resolution**: not all videos have all possible resolutions, so you may not be able to fetch the resolution you want for some videos (as they don't exist) \n"
                        "4.  **recommended hardware**: this is a very light weight app, so minimum specs should work fine"
                        "5.  **proxies**: there is an option in the yt_download module to enter proxy server ips"
                    )
                )


if __name__ == "__main__":
    print("Launching Gradio interface...")
    demo.launch()  # allow_flagging="never"
