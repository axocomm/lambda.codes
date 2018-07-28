FROM alpine:latest
MAINTAINER axocomm <axocomm@gmail.com>

RUN apk add --no-cache py-pip python-dev npm make g++

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt
RUN npm i -g gulp && npm i
RUN gulp build

ENV PAGE_DIR /pages
ENTRYPOINT ["python"]
CMD ["app.py"]
