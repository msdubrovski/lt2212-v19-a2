#!/bin/bash
# this short script will create the files for part 3
# relative path to the folder
FOLDER=../ass2_data 
B=p

# 1- one file containing a term-document matrix with no vocabulary restriction and no other transformations.
python3 gendoc.py -D v $FOLDER output_01_.txt

# 2- one file containing a term-document matrix with a vocabulary restriction of your choice, but allowing significantly fewer terms than the total number and no other transformations.
python3 gendoc.py -D v -B $B $FOLDER output_02_B"$B".txt
 
# 3- one file containing a term-document matrix with no vocabulary restriction, but with tf-idf applied.
python3 gendoc.py -D v -T $FOLDER output_03_T.txt

# 4- one file containing the same vocabulary restriction as in (2), but with tf-idf applied.
python3 gendoc.py -D v -T -B $B $FOLDER output_04_B"$B"T.txt

# 5- one file with no vocabulary restriction, with truncated SVD applied to 100 dimensions.
python3 gendoc.py -D v -S 100 $FOLDER output_05_S100.txt

# 6- one file with no vocabulary restriction, with truncated SVD applied to 1000 dimensions.
python3 gendoc.py -D v -S 1000 $FOLDER output_06_S1000.txt

# 7- one file as in (3), but with truncated SVD applied to 100 dimensions.
python3 gendoc.py -D v -T -S 100 $FOLDER output_07_TS100.txt

# 8- one file as in (3), but with truncated SVD applied to 1000 dimensions.
python3 gendoc.py -D v -T -S 1000 $FOLDER output_08_TS1000.txt

