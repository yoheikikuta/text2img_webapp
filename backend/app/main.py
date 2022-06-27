import logging
import sys

from fastapi import FastAPI, Response

sys.path.append('../')
from model.model import Text2ImgML

app = FastAPI()

ml_model = Text2ImgML()
ml_model.load_model()

stdout_handler = logging.StreamHandler(stream=sys.stdout)
stdout_handler.setLevel(logging.DEBUG)
stdout_handler.addFilter(lambda record: record.levelno <= logging.INFO)
logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
logger.addHandler(stdout_handler)

logger.info('Backend API is ready.')
logger.info(f"The device of this machine is: {ml_model.device}.")

@app.get("/")
def create_generated_images(text:str) -> bytes:
    logger.info('API is called.')
    samples = ml_model.generate_64x64_tensor(text)
    logger.info('Successfully generated 64x64 tensor.')
    up_samples = ml_model.upscale_to_256x256_tensor(text, samples)
    logger.info('Successfully upscaled 64x64 tensor to 256x256 tensor.')
    img_arr = ml_model._convert_result_tensor_to_ndarray(up_samples)
    logger.info(f'Successfully converted result tensor to ndarray. Its shape is {img_arr.shape}')

    return Response(content=img_arr.tobytes(), media_type="image/png")
