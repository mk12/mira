#!/bin/bash

set -eufo pipefail

prog=$(basename "$0")

app="mira:app"
config_path="instance/application.cfg"
py_init_db="init_db.py"
db_name="mira"
pg_dir="database"
pg_log="postgres.log"

cmd="run"
port=5000
env="development"
verbose=false

say() {
    echo " * $*"
}

die() {
    echo "$prog: $*" >&2
    exit 1
}

run() {
    if [[ "$verbose" == 1 ]]; then
        "$@"
    else
        "$@" &> /dev/null
    fi
}

usage() {
    cat <<EOS
usage: $prog [-hpv] [-b PORT] [COMMAND]

commands:
    run        start the server (default)
    db:create  create the database
    db:drop    delete the database
    db:start   start postgres
    db:stop    stop postgres
    db:psql    start psql session

options:
    -h          show this help message
    -p          run in production mode
    -v          verbose output
    -b PORT     bind to the given port
EOS
}

ensure_config() {
    if ! [[ -s "$config_path" ]]; then
        mkdir -p "$(dirname "$config_path")"
        say "Note: generating $config_path"
        secret=$(python3 -c "import os; print(os.urandom(16).hex())")
        cat <<EOS > "$config_path"
DB_USER = "$(whoami)"
DB_PASSWORD = ""
SECRET_KEY = "$secret"
EOS
    fi
}

run_server() {
    ensure_config
    start_db
    if [[ "$env" == "production" ]]; then
        gunicorn -b "localhost:$port" "$app"
    else
        FLASK_APP="$app" FLASK_ENV="$env" python3 -m flask run -p "$port"
    fi
}

pg_running() {
    if run pg_ctl -D "$pg_dir" status; then
        return 0
    fi
    pid=$(pgrep -x postgres)
    if [[ -n "$pid" ]]; then
        die "There is a rogue postgres process (kill it with 'kill $pid')"
    fi
    return 1
}

create_db() {
    drop_db
    say "Creating a postgres database cluster in $pg_dir/"
    if ! run initdb "$pg_dir"; then
        die "initdb failed"
    fi
    start_db
    if ! run createdb "$db_name"; then
        die "createdb failed"
    fi
    ensure_config
    say "Running $py_init_db"
    if ! run python3 "$py_init_db"; then
        die "Failed to initialize database"
    fi
    stop_db
}

drop_db() {
    if pg_running; then
        stop_db
    fi
    say "Deleting database directory $pg_dir/"
    rm -rf "$pg_dir"
}

start_db() {
    if pg_running; then
        say "Note: postgres is already running (stop it with '$0 db:stop')"
        return
    fi
    if ! [[ -d "$pg_dir" ]]; then
        die "Database has not been created (create it with '$0 db:create')"
    fi
    say "Starting postgres (logs in $pg_log)"
    if ! run pg_ctl -D "$pg_dir" -w -l "$pg_log" start; then
        die "Failed to start postgres (have you run '$0 create'?)"
    fi
}

stop_db() {
    if ! pg_running; then
        say "Note: postgres is not running (start it with '$0 db:start')"
        return
    fi
    say "Stopping postgres"
    if ! run pg_ctl -D "$pg_dir" stop; then
        die "Failed to stop postgres"
    fi
}

psql_db() {
    if ! pg_running; then
        start_db
    fi
    say "Connecting to database $db_name"
    if ! psql -d "$db_name"; then
        die "Failed to start psql"
    fi
}

main() {
    case $cmd in
        run) run_server ;;
        db:create) create_db ;;
        db:drop) drop_db ;;
        db:start) start_db ;;
        db:stop) stop_db ;;
        db:psql) psql_db ;;
        *) die "$cmd: Invalid command" ;;
    esac
}

while getopts "hvpb:" opt; do
    case $opt in
        h) usage ; exit 0 ;;
        p) env="production" ;;
        v) verbose=true ;;
        b) port=$OPTARG ;;
        *) exit 1 ;;
    esac
done

shift $((OPTIND - 1))
if [[ $# -eq 1 ]]; then
    cmd=$1
elif [[ $# -gt 1 ]]; then
    die "Too many arguments"
fi

main
