#!/usr/bin/env bash
# Prints the GOAL-STATUS block read by the /goal evaluator. Protected: do not edit.
cd "$(dirname "$0")/.." && exec python3 scripts/status.py
