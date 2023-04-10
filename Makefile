black:
	python -m black .

lint:
	python -m flake8 . --count --statistics

test:
	python -m pytest

types:
	python -m mypy .

coverage:
	python -m pytest --cov=. tests/

style: black lint

all: style types coverage
