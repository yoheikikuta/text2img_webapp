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
    samples = ml.generate_64x64_tensor(text)
    up_samples = ml.upscale_to_256x256_tensor(text, samples)
    img_arr = ml._convert_result_tensor_to_ndarray(up_samples)

    return Response(content=img_arr.tobytes(), media_type="image/png")
