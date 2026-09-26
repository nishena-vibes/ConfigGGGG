#!/usr/bin/env bash

grep -oE '[a-zA-Z_][a-zA-Z0-9_]*' "$1" | tr '[:upper:]' '[:lower:]' | sort -u | tr '\n' ' ' 
