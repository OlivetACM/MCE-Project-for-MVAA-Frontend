FROM python:3-stretch
ENV PYTHONUNBUFFERED 1

COPY . /code/
WORKDIR /code/www

RUN apt update
RUN apt install -y imagemagick tesseract-ocr libtesseract-dev ghostscript poppler-utils

RUN pip install -r ../requirements.txt
