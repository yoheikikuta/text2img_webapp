FROM python:3.10

RUN pip install --no-cache-dir fastapi uvicorn numpy git+https://github.com/openai/glide-text2im

EXPOSE 8080

COPY ./app /app
COPY ./model /model

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
