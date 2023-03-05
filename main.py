from typing import Union
from uuid import uuid4
from os.path import join as joinpath
from fastapi import FastAPI, File,Form, Response, UploadFile

from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from thumbnail import generate_thumbnail
from starlette.responses import StreamingResponse
import numpy as np
import cv2


app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
app.mount("/images_output", StaticFiles(directory="images_output"), name="static")
@app.get("/")
def read_root():
    return FileResponse("static/QT.html")

@app.post(
        "/process-image/", 
)
async def create_upload_file( file: UploadFile, title: str=Form(),subtitle:str=Form()):
    contents = await file.read()
    nparr = np.fromstring(contents, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    image=await generate_thumbnail(img, title, subtitle)
    filepath=joinpath("images_output", str(uuid4())+".png")
    image.save(filepath)
   
    return {"thumnail":"/"+filepath}