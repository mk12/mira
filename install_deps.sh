#!/bin/bash

set -eufo pipefail

prog=$(basename "$0")

say() {
    echo " * $*"
}

die() {
    echo "$prog: $*" >&2
    exit 1
}

if [[ "$(uname -s)" != "Darwin" ]]; then
    die "only works on macOS"
fi
if ! command -v brew > /dev/null; then
    die "must install homebrew"
fi

say "installing homebrew dependencies"
for p in python3 postgresql; do
    if brew list --versions "$p" > /dev/null; then
        say "$p already installed"
    elif ! brew install "$p"; then
        die "failed to install $p"
    fi
done

say "installing pip3 dependencies"
pip3 install -r requirements.txt
