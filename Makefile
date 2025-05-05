# Makefile for MinerU Lambda Extraction

.PHONY: help setup test docker-build docker-run clean

help:
	@echo "Available targets:"
	@echo "  setup         Install Python deps, download models, patch config"
	@echo "  test          Run local test of lambda handler"
	@echo "  docker-build  Build Docker image for Lambda"
	@echo "  docker-run    Run Docker image locally"
	@echo "  clean         Remove __pycache__ and temp files"

setup:
	sudo apt-get update && sudo apt-get install -y libgl1
	pip install -r app/requirements.txt
	python app/setup_magic_pdf.py

test:
	python app/test_lambda_local.py

docker-build:
	docker build -t mineru-lambda .

docker-run:
	docker run --rm -it mineru-lambda

clean:
	rm -rf __pycache__ app/__pycache__ app/*.pyc app/*.pyo app/*.log
