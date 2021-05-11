# Development

## Install dev requirements
`pip install -r requirements-dev.txt`

## Formatting
- `black .`

## Linting
- `flake8`

## Run test
- `pytest --cov=app` run test
- `pytest --cov=app --cov-report html` run test with html report

## Install pre-commit
- `pip install pre-commit`
- add hooks
  `pre-commit install`
  `pre-commit install --hook-type commit-msg`
- update to the latest versions `pre-commit autoupdate`
