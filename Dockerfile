FROM python:3.9-slim-buster

WORKDIR /src

COPY requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN apt update && \
    apt install \
    ffmpeg \
    mp4v2-utils \
    fdkaac \
    php-cli \
    php-intl \
    php-json \
    php-mbstring \
    php-xml


RUN wget https://github.com/sandreas/m4b-tool/releases/download/v.0.4.2/m4b-tool.phar -O /usr/local/bin/m4b-tool && \
    chmod +x /usr/local/bin/m4b-tool

CMD m4b-tool --version