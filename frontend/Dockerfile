FROM python:3.10

LABEL maintainer="diracdiego@gmail.com"

COPY . /opt/app
WORKDIR /opt/app

RUN pip -no-cache-dir install streamlit google-cloud-translate==2.0.1 google.auth

ENV GOOGLE_APPLICATION_CREDENTIALS ./secrets/key.json

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py", "--server.port", "8080"]
