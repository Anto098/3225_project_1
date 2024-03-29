#!/bin/bash
#$1 = dir with all files
#$2 = output dir
if [ -d $2 ]
then
	echo "dir already exists"
else
	mkdir $2
fi
for full_path in "$1"/*
do
  file_name=$(echo "$full_path" | cut -d "/" -f2)
  python3 ./transf.py $full_path ./$2/$file_name
done


