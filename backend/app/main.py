from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
def create_generated_images(text:str) -> dict:
    """
    TODO: Replace this endpoint with Text2Img.
    """
    return {"Hello": text}
