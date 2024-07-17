FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    software-properties-common \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /home

ENV PYTHONPATH=.

COPY requirements.txt /home/requirements.txt
COPY youtube_downloader /home/youtube_downloader
RUN pip3 install -r /home/requirements.txt

EXPOSE 7860
ENV GRADIO_SERVER_NAME="0.0.0.0"

CMD ["gradio", "/home/youtube_downloader/app.py"]