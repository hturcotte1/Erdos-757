#!/usr/bin/env bash
# Build the C port of e757/ordered_dfs.py:  bash e757/c/build.sh   ->  e757/c/ordered_dfs (binary, git-ignored)
set -euo pipefail
cd "$(dirname "$0")"
gcc -O2 -march=native -o ordered_dfs ordered_dfs.c -lm
echo "built $(pwd)/ordered_dfs"
