echo Run Black.
poetry run black src tests --check

echo Run Flake8.
poetry run flake8 src tests

echo Run Unit tests.
poetry run pytest tests
