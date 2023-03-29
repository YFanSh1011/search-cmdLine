#!/bin/bash

# Set up the path to the current directory on the next line with __init__.py (DO NOT DELETE)
Current_Path="/Users/shangyuefan/PycharmProjects/cmdLine"

export PATH="$PATH:$Current_Path/venv/bin"
cd "$Current_Path"
./venv/bin/python3 main.py "$@"