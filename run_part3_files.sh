#!/bin/bash
for i in {1..8}
do
  python3 simdoc.py output_0"$i".txt
  #echo tuvi_y_tuvi_0"$i"veces!
done
