#!/usr/bin/env bash
input_csv=$1
output_csv=$2

python run_composite_scoring.py ${input_csv} ${output_csv}
