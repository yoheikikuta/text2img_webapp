FROM python:3.10

LABEL maintainer="diracdiego@gmail.com"

COPY . /opt/app
WORKDIR /opt/app

RUN pip install streamlit

EXPOSE 8501

ENTRYPOINT ["streamlit", "run"]
CMD ["app.py"]
