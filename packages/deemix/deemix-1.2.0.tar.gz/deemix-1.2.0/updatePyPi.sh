#!/usr/bin/env bash
rm -rd build
rm -rd dist

python3 setup.py sdist bdist_wheel
python3 -m twine upload dist/*
