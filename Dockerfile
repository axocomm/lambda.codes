FROM ubuntu:latest
MAINTAINER axocomm <axocomm@gmail.com>

RUN apt-get update && apt-get install -y \
    python-pip \
    python-dev \
    build-essential \
    software-properties-common

RUN add-apt-repository -y ppa:chris-lea/node.js
RUN apt-get update && apt-get install -y nodejs

RUN npm install -g gulp

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

RUN npm install
RUN npm uninstall gulp-sass
RUN npm install gulp-sass

RUN gulp build

ENV PAGE_DIR /pages
ENTRYPOINT ["python"]
CMD ["app.py"]
