FROM python:3.12.1

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /dictionary

COPY . /dictionary

RUN pip install --upgrade pip
RUN pip install -r requirements.txt

EXPOSE 8000
