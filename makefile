run:
	python -m app.app

test:
	pytest

lint:
	ruff check .

docker:
	docker build -t semka-informatics .