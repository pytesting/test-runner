#!/bin/bash

rm -rf build dist test_runner.egg-info

python setup.py sdist bdist_wheel

twine upload --repository-url https://test.pypi.org/legacy/ dist/*

twine upload dist/*
