import io
import numpy as np
from fastapi import FastAPI, Response

app = FastAPI()


@app.get("/")
def create_generated_images(text:str) -> bytes:
    """
    TODO: Replace this endpoint with Text2Img.
    """
    img_arr = np.random.rand(256,256*5,3) * 255
    
    return Response(content=img_arr.tobytes(), media_type="image/png")
