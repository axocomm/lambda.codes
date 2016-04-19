.PHONY: build run build-js build-docker run-docker

PAGE_DIR = $(shell pwd)/resources/pages

all: run

run: build-js
	PAGE_DIR=$(PAGE_DIR) python -m app

build-js:
	gulp build

build-docker:
	docker build -t xyzy-min .

run-docker:
	docker run -it -p 5000:5000 -v $(PAGE_DIR):/pages -d xyzy-min
