#!/usr/bin/env bash
(
    cd "$(dirname "$0")" || {
        echo "Error: Failed to change directory to the script's location." >&2
        exit 1
    }

    ./.venv/bin/python -OO ./robobottom.py
)

