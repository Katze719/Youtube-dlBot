FROM python:3.10.13-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

RUN set -eux; \
    mkdir /app;

RUN set -eux; \
    apt-get install -y youtube-dl; \
    whereis youtube-dl;

COPY . /app

CMD ["python3", "./bot.py"]
