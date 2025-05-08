from fastapi import FastAPI, Query
from fastapi.responses import JSONResponse
import subprocess
import os
from pathlib import Path

app = FastAPI()

@app.get("/download_playlist")
def download_playlist(url: str = Query(...)):
    output_dir = "downloads"
    os.makedirs(output_dir, exist_ok=True)

    command = [
        "yt-dlp",
        "--yes-playlist",
        "--extract-audio",
        "--audio-format", "m4a",
        "--embed-metadata",
        "--embed-thumbnail",
        "--add-metadata",
        "-o", f"{output_dir}/%(artist)s - %(title)s.%(ext)s",
        url
    ]

    try:
        subprocess.run(command, check=True)
        files = os.listdir(output_dir)
        return JSONResponse({"message": "Playlist baixada com sucesso!", "arquivos": files})
    except subprocess.CalledProcessError as e:
        return JSONResponse({"error": "Falha ao baixar playlist", "detalhes": str(e)}, status_code=500)
