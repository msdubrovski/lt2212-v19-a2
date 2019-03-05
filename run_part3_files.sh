#!/bin/bash
for i in {1..8}
do
  python3 simdoc.py -M output_0"$i"*.txt
done
