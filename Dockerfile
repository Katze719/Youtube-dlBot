FROM python:3.10.13-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

RUN set -eux; \
    mkdir /app;

RUN set -eux; \
    apt-get install -y youtube-dl;

COPY . /app

RUN cp /app/youtube-dl/youtube-dl /usr/local/bin/youtube-dl

CMD ["python3", "./bot.py"]
