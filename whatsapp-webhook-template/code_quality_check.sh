flake8
isort .
black .

mypy backend
mypy main.py

pylint backend
pylint main.py

pytest
