#! /usr/bin/env sh

rm -Rf venv
python3 -m venv venv
./venv/bin/pip install --upgrade pip wheel
./venv/bin/pip install -r requirements.txt
