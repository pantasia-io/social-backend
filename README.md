# Python Boilerplate
Python Boilerplate to kick start your project with settings aligned to Data Team standards.

## What it is
* A starting point for any generic project

## What it is not
* To limit you on your project structure design.

## Features
### Package Management
We use [Poetry](https://python-poetry.org/) instead of the typical `pip` and `requirements.txt`.
To get started, run `pip install poetry` in your virtual environment, then run `poetry install`.

### CODEOWNERS
Users specified in this file will be notified for review for any Pull Request.

### Pull Request Template
Templates of pull request

### src
Place where all the source code lives.

### tests
Place where all the unit test lives. Follow the [first structure](https://docs.pytest.org/en/reorganize-docs/new-docs/user/directory_structure.html) to organize your test files.

### .editorconfig
Config file for your IDE formatter.

### .flake8
Config file for Flake8. `line-length=88` is to prevent conflict with black.

### .gitignore
Prevent files/directory from being committed into VCS.

### .pre-commit-config.yaml
List of pre commit hooks for code quality check. For `sb-git-hooks` to work, you need to install the hooks locally [following this guide](https://shopadmin.atlassian.net/wiki/spaces/DATA/pages/1283260417/Prevent+Secrets+from+Being+Committed+into+Git).

### Makefile
It has few preconfigured target for basic code checking:
* `make format` - Runs formatting according to `black` and `isort`
* `make lint` - Lints code using `flake8`
* `make pytest` - Runs `pytest` for files in `tests` directory
* `make pytest-coverage` - Runs `pytest-cov` and generate coverage report.

### requirements.txt
Contains basic library for the above functionalities.

### Dockerfile
Simple boilerplate for python app

### .dockerignore
Prevent files/direcories from being pushed into docker image builds.
