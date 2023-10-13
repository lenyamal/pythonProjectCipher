#!/bin/bash

python3 -m venv src/venv
source src/venv/bin/activate

pip install -r requirements.txt

python3 src/main.py
