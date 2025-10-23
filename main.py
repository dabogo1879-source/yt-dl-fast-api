import os
import yt_dlp
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import random
import string

app = FastAPI()

# Configure download path
download_path = os.getenv('DOWNLOAD_PATH', '/tmp/downloads')
os.makedirs(download_path, exist_ok=True)

class YtVideoDownloadRequestBody(BaseModel):
    url: str

def generate_random_file_name():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=16))

@app.post("/api/download")
def download_video(body: YtVideoDownloadRequestBody):
    file_name = f'{generate_random_file_name()}.m4a'
    urls = [body.url]
    ydl_opts = {
        'outtmpl': {
            'default': "/".join([download_path, file_name]),
        },
        'format': 'm4a/bestaudio/best',
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)
    if error_code == 0:
        return {"status": "success", "file_name": file_name}
    else:
        raise HTTPException(506, detail="download failed for internal server error")

@app.get("/download_audio")
@app.post("/download_audio")
def download_audio(url: str = None, body: YtVideoDownloadRequestBody = None):
    """Download audio endpoint - supports both GET and POST methods"""
    
    # Get URL from query parameter (GET) or request body (POST)
    video_url = url if url else (body.url if body else None)
    
    if not video_url:
        raise HTTPException(400, detail="URL parameter is required")
    
    file_name = f'{generate_random_file_name()}.m4a'
    urls = [video_url]
    ydl_opts = {
        'outtmpl': {
            'default': "/".join([download_path, file_name]),
        },
        'format': 'm4a/bestaudio/best',
        'cookiefile': 'cookies.txt',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'm4a',
        }]
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        error_code = ydl.download(urls)
    if error_code == 0:
        return {"status": "success", "file_name": file_name}
    else:
        raise HTTPException(506, detail="download failed for internal server error")
