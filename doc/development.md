# test-runner: Developer Documentation

This document contains information
that is only relevant for developers and maintainers
of `test-runner`.

Be aware that `test-runner` needs at least Python 3.6
and was tested on Linux and macOS with Python 3.6 and 3.7.

## Installation for Development

After cloning the [GitHub repository](https://github.com/pytesting/test-runner),
it is recommended to set up a virtual environment.
This can be done by
```commandline
virtualenv -p /usr/bin/python3 path/to/venv
source path/to/venv/bin/activate
pip install -r dev-requirements.txt
```
This will automatically install all dependencies necessary for `test-runner` 
development.

## Coding Guidelines

We want `test-runner` to be as clean as it possibly can.
Thus we require the usage of `flake8`,
the writing of unit tests,
and a particular code style.

[`flake8`](http://flake8.pycqa.org/en/latest) is a tool for style guide 
enforcement.
This means, it checks for certain patterns in the code that are considered 
bad practice.
We want to have a clean output of `flake8` for `test-runner`.
Thus it is recommended to run `flake8 .` on the project's root
before committing.
Furthermore, `flake8` will also be run by the continuous integration
and causes it to fail if there are any problems present.

Unit tests are also required for each class and module.
At the time of writing this guidelines,
the test suite achieved 100% line coverage and 100% branch coverage on the code.

Third, we require the usage of the [`black`](https://github.com/ambv/black)
code formatter.
It can be invoked by
```commandline
black -l 80 --py36 .
```
in the project's root folder.
You can also use a pre-commit hook,
see `black`'s documentation for details.
