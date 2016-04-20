FROM ubuntu:latest
MAINTAINER axocomm <axocomm@gmail.com>

RUN apt-get update && apt-get install -y \
    python-pip \
    python-dev

COPY . /app
WORKDIR /app

RUN pip install -r requirements.txt

ENV PAGE_DIR /pages
ENTRYPOINT ["python"]
CMD ["app.py"]
