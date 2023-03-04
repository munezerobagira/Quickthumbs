from typing import Union

from fastapi import FastAPI, File, UploadFile
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from thumbnail import generate_thumbnail
import numpy as np
import cv2


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
@app.get("/")
def read_root():
    return FileResponse("QT.html")

@app.post("/thumbs/")
async def create_upload_file( file: UploadFile):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    await generate_thumbnail(img, "testing", "testing")
    return { "filename": file.filename}
