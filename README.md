# hypermodern-python
Hypermodern Python


# Chapter 1: Setup

## Run console script
```bash
poetry run hypermodern-python
```

# Chapter 2: Testing

## Run tests
```bash
poetry run pytest
```

## Run coverage
```bash
poetry run pytest --cov
```

## Automate tests with NOX
```bash
# install nox
pip install --user --upgrade nox
# run tests
nox
# run tests reusing the same env
nox -r
```

## Run e2e tests
```bash
nox -rs tests-3.9 -- -m e2e
```
