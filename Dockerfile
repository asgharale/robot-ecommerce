FROM python:3.11-alpine

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

COPY ./requirements /tmp/requirements/

ARG DEV=false

RUN python -m venv /py && \
    /py/bin/pip3 install --upgrade pip && \
    apk add --update --no-cache postgresql-client jpeg-dev && \
    apk add --update --no-cache --virtual .tmp-build-deps \
        build-base postgresql-dev musl-dev zlib zlib-dev

RUN /py/bin/pip install -r /tmp/requirements/base.txt && \
    if [ "$DEV" = "true" ]; then \
        /py/bin/pip install -r /tmp/requirements/development.txt; \
    fi && \
    rm -rf /tmp/* && \
    apk del .tmp-build-deps

COPY . /app
WORKDIR /app

ENV PATH="/py/bin:$PATH"

EXPOSE 8000