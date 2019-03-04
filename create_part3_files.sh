#!/bin/bash
# this short script will create the files for part 3
# relative path to the folder
FOLDER=../ass2_data 
B=200

# 1- one file containing a term-document matrix with no vocabulary restriction and no other transformations.
python3 gendoc.py $FOLDER output_01.txt

# 2- one file containing a term-document matrix with a vocabulary restriction of your choice, but allowing significantly fewer terms than the total number and no other transformations.
python3 gendoc.py -B $B $FOLDER output_02.txt
 
# 3- one file containing a term-document matrix with no vocabulary restriction, but with tf-idf applied.
python3 gendoc.py -T $FOLDER output_03.txt

# 4- one file containing the same vocabulary restriction as in (2), but with tf-idf applied.
python3 gendoc.py -T -B $B $FOLDER output_04.txt

# 5- one file with no vocabulary restriction, with truncated SVD applied to 100 dimensions.
python3 gendoc.py -S 100 $FOLDER output_05.txt

# 6- one file with no vocabulary restriction, with truncated SVD applied to 1000 dimensions.
python3 gendoc.py -S 1000 $FOLDER output_06.txt

# 7- one file as in (3), but with truncated SVD applied to 100 dimensions.
python3 gendoc.py -T -S 100 $FOLDER output_07.txt

# 8- one file as in (3), but with truncated SVD applied to 1000 dimensions.
python3 gendoc.py -T -S 1000 $FOLDER output_08.txt

