#!/bin/bash
#$1 = dir with all files
#$2 = output dir
mkdir $2
for file in $1:
do
	python3 ./transf.py $file > ./$2
done

