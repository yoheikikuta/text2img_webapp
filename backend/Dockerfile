FROM nvidia/cuda:11.0.3-base-ubuntu20.04

LABEL maintainer="diracdiego@gmail.com"

RUN apt-get update && apt-get install -y git
RUN apt-get install -y python3 python3-pip
RUN pip3 install --no-cache-dir google-cloud-storage fastapi uvicorn numpy git+https://github.com/openai/glide-text2im

EXPOSE 80

COPY backend/app /app
COPY backend/model /model

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "80"]
