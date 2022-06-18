# import numpy as np
from fastapi import FastAPI, Response
import sys
sys.path.append('../')
from model.model import Text2ImgML

app = FastAPI()
ml = Text2ImgML()

ml.load()

@app.get("/")
def create_generated_images(text:str) -> bytes:
    img_arr = ml.predict(text)

    return Response(content=img_arr.tobytes(), media_type="image/png")
