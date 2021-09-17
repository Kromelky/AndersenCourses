# syntax=docker/dockerfile:1
FROM python:3.9-alpine

RUN apk add --no-cache --virtual .build-deps gcc libc-dev libxslt-dev && \
    apk add --no-cache libxslt && \
    pip install --no-cache-dir lxml>=3.5.0 && \
    apk del .build-deps \
    pip install Flask beautifulsoup4 requests lxml
COPY /app /app
WORKDIR /app
EXPOSE 8080
ENTRYPOINT ["/app/run.sh"]
