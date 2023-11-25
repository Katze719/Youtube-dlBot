FROM python:3.10.13-bookworm
ENV TZ=Europe/Berlin
ENV DEBIAN_FRONTEND noninteractive

RUN set -eux; \
    mkdir /app;

COPY . /app

RUN cp /app/youtube-dl/youtube-dl /usr/local/bin/youtube-dl
RUN chmod +x /usr/local/bin/youtube-dl

WORKDIR /app

RUN set -eux; \
    pip install -r ./requirements.txt;

CMD ["python3", "./bot.py"]
