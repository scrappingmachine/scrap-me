.PHONY: venv install run test style build all_tests
TAG=latest

venv:
	python3 -m venv .venv

install:
	pip install -r requirements.txt

build:
	docker build -t scrappingmachine/scrap-me:${TAG} .

test:
	pytest -v tests/

style:
	flake8 --max-line-length=100 client server tests utils

all_tests: style test
