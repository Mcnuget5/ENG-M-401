black:
	python -m black .

lint:
	python -m flake8 . --count --statistics

test:
	python -m pytest

types:
	python -m mypy ./eng_m/ ./tests/

coverage:
	python -m pytest --cov-report html --cov=. tests/

style: black lint

all: style types coverage
