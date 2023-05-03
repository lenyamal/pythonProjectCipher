#!/bin/bash

python3 -m venv test/venv
source venv/bin/activate

pip install -r requirements.txt

./main.py
