#!/bin/bash
#$1 = dir with all files
#$2 = output dir
if[ -d $1]; then
	echo "dir already exists"
else
	mkdir $2
fi
for file in $1:
do
	echo $file
	python3 ./transf.py $file > ./$2/$file
done

