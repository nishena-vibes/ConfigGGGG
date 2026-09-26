#!/bin/bash

find $1 -type f -printf "%f\t%p\n" | sort | uniq -D -w $(find BRUHRR/ -type f -printf "%f\n" | wc -L)
