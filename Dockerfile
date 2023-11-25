FROM python:3.10.13-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

RUN set -eux; \
    mkdir /app;

COPY . /app

RUN cp /app/youtube-dl/youtube-dl /usr/local/bin/youtube-dl

WORKDIR /app

CMD ["python3", "./bot.py"]
