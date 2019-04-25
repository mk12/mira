#!/bin/bash

set -eufo pipefail

prog=$(basename "$0")

pg_dir=database
pg_log=postgres.log
db_name=mira
config_path=instance/application.cfg

py_init_db=init_db.py

cmd=
verbose=0

say() {
    echo " * $*"
}

die() {
    echo "$prog: $*" >&2
    exit 1
}

usage()  {
    cat <<EOS
usage: $prog [-v] COMMAND

commands:
    create  (re)create the database
    drop    delete the database
    start   start postgres
    stop    stop postgres
    psql    start psql session

options:
    -v      verbose output
EOS
}

run() {
    if [[ "$verbose" == 1 ]]; then
        "$@"
    else
        "$@" &> /dev/null
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
    mkdir -p "$(dirname "$config_path")"
    if [[ -f "$config_path" ]]; then
        say "Note: config file $config_path already exists"
    else
        say "Creating config file $config_path"
        secret=$(python3 -c "import os; print(os.urandom(16).hex())")
        cat <<EOS > "$config_path"
DB_USER = '$(whoami)'
DB_PASSWORD = ''
SECRET_KEY = '$secret'
EOS
    fi
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
        say "Note: postgres is already running (stop it with '$0 stop')"
        return
    fi
    if ! [[ -d "$pg_dir" ]]; then
        die "Database has not been created (create it with '$0 create')"
    fi
    say "Starting postgres (logs in $pg_log)"
    if ! run pg_ctl -D "$pg_dir" -w -l "$pg_log" start; then
        die "Failed to start postgres (have you run '$0 create'?)"
    fi
}

stop_db() {
    if ! pg_running; then
        say "Note: postgres is not running (start it with '$0 start')"
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
    cd "$(dirname "$0")"

    case "$cmd" in
        create) create_db ;;
        drop) drop_db ;;
        start) start_db ;;
        stop) stop_db ;;
        psql) psql_db ;;
        *) usage 1 ;;
    esac
}

while (( $# )); do
    case "$1" in
        -h|--help) usage; exit 0 ;;
        -v|--verbose) verbose=1 ;;
        create|drop|start|stop|psql)
            if [[ -n "$cmd" ]]; then
                usage 1
            fi
            cmd=$1
            ;;
        *) usage; exit 1 ;;
    esac
    shift
done

main
