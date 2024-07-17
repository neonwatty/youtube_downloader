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
                        visible=False,
                    )

                @download_button.click(inputs=[url_input, resolution_dropdown], outputs=[og_video])
                def download_this(url_input, resolution_dropdown):
                    # temporary_video_location = tmpdirname + "/original_" + str(uuid.uuid4()) + ".mp4"
                    # temporary_audio_location = temporary_video_location.replace("mp4", "mp3")

                    temporary_video_location = download_video(url_input, tmpdirname)
                    temporary_audio_location = temporary_video_location.replace("mp4", "mp3")

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



if __name__ == "__main__":
    print("Launching Gradio interface...")
    demo.launch()  # allow_flagging="never"
