FROM nvidia/cuda:11.0.3-base-ubuntu20.04

RUN apt-get update && apt-get install -y git
RUN apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir fastapi uvicorn numpy git+https://github.com/openai/glide-text2im

EXPOSE 8081

COPY ./app /app
COPY ./model /model

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8081"]
