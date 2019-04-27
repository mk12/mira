#!/bin/bash

set -eufo pipefail

prog=$(basename "$0")

app="mira:app"
config_path="instance/application.cfg"
py_init_db="mira/init_db.py"
db_name="mira"
pg_dir="database"
pg_log="postgres.log"
line_length=80

cmd=dev
port_opt=
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
        "$@" > /dev/null 2>&1
    fi
}

usage() {
    cat <<EOS
usage: $prog [-hv] [-p PORT] COMMAND

commands:
    dev        start the flask server (default)
    prod       build and start the prod server
    web        start the vue server
    install    install development dependencies
    lint       format and lint code
    db:create  create the database
    db:drop    delete the database
    db:start   start postgres
    db:stop    stop postgres
    db:psql    start a psql session

options:
    -h         show this help message
    -v         verbose output
    -p PORT    bind to the given port
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

yarn_do() {
    yarn --cwd web "$@"
}

run_dev() {
    ensure_config
    start_db
    say "Serving the flask app in development mode"
    FLASK_APP="$app" FLASK_ENV="development" python3 -m flask run $port_opt
}

run_prod() {
    say "Building the vue app for production"
    yarn_do run build
    say "Serving the flask app in production mode using waitress"
    python3 -m waitress $port_opt "$app"
}

run_web() {
    say "Serving the vue app in development mode"
    yarn_do run serve $port_opt
}

install_deps() {
    to_install=()
    for p in python3 postgres yarn; do
        if ! run command -v "$p"; then
            to_install+=("${p/postgres/postgresql}")
        fi
    done
    if [[ "${#to_install[@]-0}" -gt 0 ]]; then
        if [[ "$(uname -s)" != "Darwin" ]]; then
            say "Please install these dependencies manually: ${to_install[*]}"
            die "Could not automatically install dependencies"
        fi
        if ! run command -v brew; then
            say "Please install Homebrew (https://brew.sh) and run this again"
            die "Homebrew not installed"
        fi
        for p in "${to_install[@]}"; do
            if ! brew install "$p"; then
                die "Failed to install $p"
            fi
        done
    fi

    say "Installing python dependencies"
    pip3 install -r requirements-dev.txt \
        | grep -v "Requirement already satisfied" || :

    if ! run command -v vue; then
        say "Installing the Vue cli"
        yarn_do global add @vue/cli
    fi

    say "Installing javascript dependencies"
    yarn_do install
}

lint_code() {
    status=0

    say "Linting python"
    python3 -m black -l "$line_length" mira
    python3 -m flake8 --max-line-length "$line_length" mira || status=$?

    say "Linting javascript"
    yarn_do run lint || status=$?

    if run command -v shellcheck; then
        say "Linting bash"
        shellcheck "$0" || status=$?
    else
        say "Note: install shellcheck to lint bash scripts"
    fi

    return $status
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
    if ! python3 "$py_init_db"; then
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
        dev) run_dev ;;
        prod) run_prod ;;
        web) run_web ;;
        install) install_deps ;;
        lint) lint_code ;;
        db:create) create_db ;;
        db:drop) drop_db ;;
        db:start) start_db ;;
        db:stop) stop_db ;;
        db:psql) psql_db ;;
        *) die "$cmd: Invalid command" ;;
    esac
}

if [[ $# -ge 1 && "$1" != "-"* ]]; then
    cmd=$1
    shift
fi

while getopts "hvp:" opt; do
    case $opt in
        h) usage ; exit 0 ;;
        v) verbose=true ;;
        p) port_opt="--port $OPTARG" ;;
        *) exit 1 ;;
    esac
done

shift $((OPTIND - 1))
if [[ $# -eq 1 ]]; then
    cmd=$1
elif [[ $# -gt 1 ]]; then
    usage
    exit 1
fi

main
