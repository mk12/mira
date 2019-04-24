#!/bin/bash

set -xeufo pipefail

prog=$(basename "$0")

app="mira"
env="development"
start_db=true

usage() {
    cat <<EOS
usage: $prog [-hnp]

options:
    -h  show this help message
    -n  do not start the database
    -p  use production mode
EOS
}

main() {
    if [[ "$start_db" == true ]]; then
        ./db.sh start
    fi
    if [[ "$env" == "production" ]]; then
        gunicorn mira:app
    else
        FLASK_ENV="$env" FLASK_APP="$app" python3 -m flask run
    fi
}

while getopts "hnp" opt; do
    case $opt in
        h) usage ; exit 0 ;;
        n) start_db=false ;;
        p) env="production" ;;
        *) exit 1 ;;
    esac
done

main
