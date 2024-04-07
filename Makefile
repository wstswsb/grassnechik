lint:
	ruff check --fix .
	ruff format .
	mypy --strict .
