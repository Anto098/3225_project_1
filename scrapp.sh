#!/bin/bash
#$1 = dir name
mkdir $1
curl https://www.w3.org/Style/CSS/Test/CSS3/Selectors/current/html/full/flat/ | grep -o 'css3-modsel-[^"]*' | while read -r line; do curl https://www.w3.org/Style/CSS/Test/CSS3/Selectors/current/html/full/flat/$line > ./$1/$line ; done
