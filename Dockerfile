FROM python:3.7-slim
ENV PYTHONUNBUFFERED=1
RUN python -m pip install --upgrade pip
WORKDIR /django
ADD . /django
COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .