#! /usr/bin/env sh

rm -Rf venv
python3 -m venv venv
source venv/bin/activate
pip install --upgrade pip wheel
pip install -r requirements.txt
