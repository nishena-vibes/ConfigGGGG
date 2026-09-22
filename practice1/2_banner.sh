#!/bin/bash

TOP_STR="+-"
MSG="$1"
for i in $(seq 2 "$(echo $MSG | wc -m)"); do
	TOP_STR="$TOP_STR-"
done

TOP_STR="$TOP_STR-+"

echo "$TOP_STR"
echo "| $MSG |"
echo "$TOP_STR"
