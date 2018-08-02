FROM alpine:latest
MAINTAINER axocomm <axocomm@gmail.com>

# python2.7 is required for node-gyp, naturally
RUN apk add --no-cache python python3 npm make g++

COPY . /app
WORKDIR /app

RUN pip3 install -r requirements.txt
RUN npm i -g gulp && npm i
RUN gulp build

ENV PAGE_DIR /pages
ENTRYPOINT ["python3"]
CMD ["app.py"]
