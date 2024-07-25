flake8
isort .
black .

mypy migrate.py
mypy migrations

pylint migrations
pylint migrate.py
