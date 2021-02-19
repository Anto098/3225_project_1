#!/bin/bash
#$1 = dir with all files
#$2 = output dir
if [ -d $2 ]
then
	echo "dir already exists"
else
	mkdir $2
fi
echo "$1"
for file in "$1"/*
do
  echo "$file"
#   newfile=$(${file#htmls})
  fn=$(echo "$file" | cut -d "/" -f2)
  echo "$fn"
  python3 ./transf.py $file > ./$2/$fn
done


