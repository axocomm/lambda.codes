FROM alpine:latest
MAINTAINER axocomm <axocomm@gmail.com>

RUN apk add --no-cache py-pip python-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PAGE_DIR /pages
ENTRYPOINT ["python"]
CMD ["app.py"]
