import sys

from fastapi import FastAPI, Response

sys.path.append('../')
from model.model import Text2ImgML

app = FastAPI()
ml_model = Text2ImgML()

ml_model.load_model()

@app.get("/")
def create_generated_images(text:str) -> bytes:
    samples = ml_model.generate_64x64_tensor(text)
    up_samples = ml_model.upscale_to_256x256_tensor(text, samples)
    img_arr = ml_model._convert_result_tensor_to_ndarray(up_samples)

    return Response(content=img_arr.tobytes(), media_type="image/png")
