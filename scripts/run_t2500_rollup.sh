#!/usr/bin/env bash
set -e

input_dir=$1
metrics=$2
trend=$3

python scripts/python/eval/rollup.py --input "$input_dir" --metrics "$metrics" --trend "$trend"
