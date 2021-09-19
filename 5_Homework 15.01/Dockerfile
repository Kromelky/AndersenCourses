# syntax=docker/dockerfile:1
FROM python:3.9-alpine

RUN apk update --no-cache && \
    apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir lxml>=3.5.0 && \
    apk del .build-deps && \
    pip install --no-cache-dir Flask beautifulsoup4 requests && \
    mkdir /app && \
    wget -O /app/main.zip --no-check-certificate https://github.com/Kromelky/FlaskApplication/archive/main.zip && \
    unzip /app/main.zip -d /app -o && \
    cp -a /app/FlaskApplication-main/. /app/. && \
    rm -fr /app/FlaskApplication-main && \
    rm /app/main.zip && \
    rm -fr /app/curls
EXPOSE 8080
WORKDIR /app
CMD python main.py -p 8080
