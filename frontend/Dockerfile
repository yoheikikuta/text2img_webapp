FROM python:3.10

LABEL maintainer="diracdiego@gmail.com"

WORKDIR /opt/app
COPY frontend/app.py frontend/util.py ./

RUN pip3 install --no-cache-dir streamlit google-cloud-translate==2.0.1 google.auth

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port", "8501"]
