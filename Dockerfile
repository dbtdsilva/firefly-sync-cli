# Use an official Python runtime as the base image
FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/
COPY src /app/src

RUN pip install -r requirements.txt

CMD ["sh", "-c", "python app.py --file-watcher-path ${FILE_WATCHER_PATH}"]
