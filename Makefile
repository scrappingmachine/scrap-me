.PHONY: venv install run test style build all_tests push
TAG=latest

venv:
	python3 -m venv .venv

install:
	pip install -r requirements.txt

build:
	docker build -t scrappingmachine/scrap-me:${TAG} .

push:
	docker push scrappingmachine/scrap-me:${TAG}

test:
	pytest -v tests/

style:
	flake8 --max-line-length=100 src tests main.py

all_tests: style test
