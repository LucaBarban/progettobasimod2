#!/usr/bin/env bash

VENV_PATH=./venv
GREEN="\033[32m"
RESET="\033[0m"

message() { echo -e "$GREEN==> $1$RESET"; }

help() {
    echo "Usage: ./env.sh [COMMAND]"
    echo ""
    echo "Commands:"
    echo "  enter    enter and setup virtual enviroment"
}

create_env() {
    # Fai il setup solo se non l'hai già fatto
    [[ -d $VENV_PATH ]] && return
    message "Creating virtual enviroment"
    python3 -m venv "$VENV_PATH"
    . "$VENV_PATH/bin/activate"
}

enter() {
    # Entra nel virtual enviroment solo se non ci sei già dentro
    [[ -z $VIRTUAL_ENV ]] && . "$VENV_PATH/bin/activate"
}

install_deps() {
    message "Installing packages"
    [[ -f ./requirements.txt ]] && pip install -r ./requirements.txt
}


# User commands

case $1 in
enter)
    create_env
    enter
    install_deps
    ;;
*)
    help
    ;;
esac
