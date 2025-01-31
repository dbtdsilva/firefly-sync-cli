# Use an official Python runtime as the base image
FROM python:3.9-slim

WORKDIR /app

COPY app.py /app/
COPY requirements.txt /app/
COPY src /app/src

RUN pip install -r requirements.txt

CMD ["sh", "-c", "args=daemon; \
  if [ \"$DAEMON_FIREFLY_CRON_ENABLED\" != true ] && [ \"$DAEMON_FIREFLY_CRON_ENABLED\" != 1 ]; then \
    args=\"$args --no-firefly-cron-job\"; \
  fi; \
  if [ \"$DAEMON_STOCK_CRON_ENABLED\" != true ] && [ \"$DAEMON_STOCK_CRON_ENABLED\" != 1 ]; then \
    args=\"$args --no-stock-cron-job\"; \
  fi; \
  python app.py $args"]