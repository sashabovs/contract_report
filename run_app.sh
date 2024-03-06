#!/usr/bin/env bash

python3.10 -m venv venv
. venv/Scripts/activate
pip install -r requirements.txt

flask --app app run

