FROM python:3.10.13-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

RUN set -eux; \
    mkdir /app;

COPY . /app

WORKDIR /app

RUN set -eux; \
    pip install -r ./requirements.txt;

RUN cp /app/youtube-dl/youtube-dl /usr/local/bin/youtube-dl
RUN chmod +x /usr/local/bin/youtube-dl

CMD ["python3", "./bot.py"]
