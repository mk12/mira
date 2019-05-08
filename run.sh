#!/bin/bash

set -eufo pipefail

prog=$(basename "$0")

flask_app="mira:app"
flask_config_path=".env"
vue_config_path="web/.env.development.local"

default_dev_port=5000
default_web_port=8080
default_test_port=5050
normal_postgres_port=5432
test_postgres_port=5431

database_name="mira"
db_dir="database"
default_db_env=dev
db_env_path="$db_dir/current"

cmd=dev
port=
verbose=false
db_env=
db_env_dir=
postgres_dir=
postgres_log_path=
migration_dir=
postgres_port=$normal_postgres_port
pytest_filter=

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
usage: $prog [-hv] [-p PORT]  COMMAND

commands:
    dev         start the flask server (default)
    web         start the vue server
    prod        build and start the prod server
    test        run api tests
    install     install development dependencies
    lint        format and lint code
    db:use      switch active db environment
    db:create   create database
    db:drop     delete database
    db:start    start postgres
    db:stop     stop postgres
    db:psql     start a psql session
    db:migrate  create a db migration
    db:upgrade  upgrade db migration

options:
    -h         show this help message
    -v         verbose output
    -d ENV     specify db environment (default: $default_db_env)
    -p PORT    bind to the given port
    -k EXPR    filter for pytest
EOS
}

database_url() {
    echo "postgres://$(whoami):@localhost:$1/$database_name"
}

set_db_env() {
    db_env=$1
    db_env_dir="${db_dir:?}/$db_env"
    postgres_dir="$db_env_dir/postgres"
    postgres_log_path="$db_env_dir/postgres.log"
    migration_dir="$db_env_dir/migrations"
}

gen_flask_config() {
    if ! [[ -s "$flask_config_path" ]]; then
        say "Note: generating $flask_config_path"
        secret=$(python3 -c "import os; print(os.urandom(16).hex())")
        cat <<EOS > "$flask_config_path"
DATABASE_URL=$(database_url "$normal_postgres_port")
FLASK_SECRET_KEY=$secret
EOS
    fi
}

set_backend_port() {
    var="VUE_APP_BACKEND"
    setting="$var=http://localhost:$port/api/"
    say "Note: setting $setting in $vue_config_path"
    if run grep "^$var=" "$vue_config_path"; then
        sed -e "/^$var=/d" -i '' "$vue_config_path"
    fi
    echo "$setting" >> "$vue_config_path"
}

flask_do() {
    FLASK_APP="$flask_app" python3 -m flask "$@"
}

yarn_do() {
    yarn --cwd web "$@"
}

run_dev() {
    : ${port:=$default_dev_port}
    gen_flask_config
    set_backend_port "$port"
    start_db
    say "Serving the flask app in development mode on port $port"
    FLASK_ENV="development" flask_do run --port "$port"
}

run_web() {
    : ${port:=$default_web_port}
    say "Serving the vue app in development mode on port $port"
    yarn_do run serve --port "$port"
}

run_prod() {
    : ${port:=$default_web_port}
    say "Building the vue app for production"
    yarn_do run build
    say "Serving the flask app in production mode using waitress on port $port"
    FLASK_FORCE_HTTPS=no python3 -m waitress --port "$port" "$flask_app"
}

run_test() {
    : "${port:=$default_test_port}"
    # Run postgres on a different port, and make sure Flask knows about it.
    postgres_port=$test_postgres_port
    db_url=$(database_url "$postgres_port")
    export DATABASE_URL=$db_url
    gen_flask_config
    if ! [[ -d "dist" ]]; then
        die "Run '$0 prod' first to generate dist/index.html"
    fi
    if ! [[ -d "$postgres_dir" ]]; then
        create_db
    fi
    start_db
    say "Clearing test database"
    run psql -p "$postgres_port" -d "$database_name" <<EOS
DELETE FROM users;
DELETE FROM friendships;
DELETE FROM canvases;
EOS
    say "Starting flask test server"
    FLASK_APP="$flask_app" FLASK_ENV="development" FLASK_RATELIMIT_ENABLED=no \
        python3 -m flask run --port "$port" > flask_test.log 2>&1 &
    flask_pid=$!
    say "Running api tests"
    status=0
    MIRA_PORT=$port python3 -m pytest tests $pytest_filter || status=$?
    say "Stopping the flask test server"
    kill "$flask_pid"
    stop_db
    return $status
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
    python3 -m black -l 80 mira
    python3 -m flake8 mira || status=$?

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
    if run pg_ctl -D "$postgres_dir" status; then
        return 0
    fi
    for pid in $(pgrep -x postgres); do
        say "Note: found another postgres process (kill it with 'kill $pid')"
    done
    if nc -z localhost "$postgres_port"; then
        die "Port $postgres_port is already in use"
    fi
    return 1
}

use_db() {
    say "Switching active database environment to $db_env"
    mkdir -p "$db_env_dir"
    echo "$db_env" > "$db_env_path"
}

create_db() {
    drop_db
    say "Creating a postgres database cluster in $postgres_dir"
    mkdir -p "$postgres_dir"
    if ! run initdb "$postgres_dir"; then
        die "initdb failed"
    fi
    start_db
    if ! run createdb -p "$postgres_port" "$database_name"; then
        die "createdb failed"
    fi
    gen_flask_config
    say "Generating initial database migration in $migration_dir"
    if ! run flask_do db init --directory "$migration_dir"; then
        die "Failed to initialize the migration repository"
    fi
    if ! run flask_do db migrate --directory "$migration_dir"; then
        die "Failed to generate the initial database migration"
    fi
    say "Applying initial database migration"
    if ! run flask_do db upgrade --directory "$migration_dir"; then
        die "Failed to apply the initial database migration"
    fi
    stop_db
}

drop_db() {
    if pg_running; then
        stop_db
    fi
    say "Deleting database environment directory $db_env_dir"
    rm -rf "$db_env_dir"
    if [[ -s "$db_env_path" && "$(< "$db_env_path")" == "$db_env" ]]; then
        say "Resetting active database environment to the default"
        echo "$default_db_env" > "$db_env_path"
    fi
}

start_db() {
    if pg_running; then
        say "Note: postgres is already running (stop it with '$0 db:stop')"
        return
    fi
    if ! [[ -d "$postgres_dir" ]]; then
        die "Database has not been created (create it with '$0 db:create')"
    fi
    say "Starting postgres (logs in $postgres_log_path)"
    if ! run pg_ctl -D "$postgres_dir" -w -l "$postgres_log_path" \
            -o "-p $postgres_port" start; then
        die "Failed to start postgres (have you run '$0 create'?)"
    fi
}

stop_db() {
    if ! pg_running; then
        say "Note: postgres is not running (start it with '$0 db:start')"
        return
    fi
    say "Stopping postgres"
    if ! run pg_ctl -D "$postgres_dir" stop; then
        die "Failed to stop postgres"
    fi
}

psql_db() {
    if ! pg_running; then
        start_db
    fi
    say "Connecting to database $database_name"
    if ! psql -p "$postgres_port" -d "$database_name"; then
        die "Failed to start psql"
    fi
}

migrate_db() {
    say "Running db migrate"
    flask_do db migrate --directory "$migration_dir"
}

upgrade_db() {
    say "Running db upgrade"
    run flask_do db upgrade --directory "$migration_dir"
}

main() {
    cd "$(dirname "$0")"
    case $cmd in
        dev) run_dev ;;
        web) run_web ;;
        prod) run_prod ;;
        test) run_test ;;
        install) install_deps ;;
        lint) lint_code ;;
        db:use) use_db ;;
        db:create) create_db ;;
        db:drop) drop_db ;;
        db:start) start_db ;;
        db:stop) stop_db ;;
        db:psql) psql_db ;;
        db:migrate) migrate_db ;;
        db:upgrade) upgrade_db ;;
        *) die "$cmd: Invalid command" ;;
    esac
}

if [[ $# -ge 1 && "$1" != "-"* ]]; then
    cmd=$1
    shift
fi

while getopts "hvk:d:p:" opt; do
    case $opt in
        h) usage ; exit 0 ;;
        v) verbose=true ;;
        k) pytest_filter="-k $OPTARG" ;;
        d) set_db_env "$OPTARG" ;;
        p) port=$OPTARG ;;
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

if [[ -z "$db_env" ]]; then
    if [[ "$cmd" == "test" ]]; then
        set_db_env "test"
    elif [[ -s "$db_env_path" ]]; then
        set_db_env "$(< "$db_env_path")"
    else
        set_db_env "$default_db_env"
    fi
fi

main
