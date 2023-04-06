lint:
	python -m flake8 . --count --statistics

black:
	python -m black .

test:
	python -m mypy .
	python -m pytest

coverage:
	python -m pytest --cov=. tests/
