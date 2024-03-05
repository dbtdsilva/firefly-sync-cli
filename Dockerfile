# Use an official Python runtime as the base image
FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/
COPY src /app/src

RUN pip install -r requirements.txt

CMD ["sh", "-c", "if [ \"$DAEMON_CRON_ENABLED\" = true ] || [ \"$DAEMON_CRON_ENABLED\" = 1]; then python app.py daemon; else python app.py daemon --no-cron-job; fi"]