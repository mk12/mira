#!/bin/bash

set -xeufo pipefail

export FLASK_ENV=development
export FLASK_APP=app.py

python3 -m flask run
