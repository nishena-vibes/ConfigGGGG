#!/bin/bash

find "$1" -type f -printf "%f\t%p\n" | awk -F'\t' '
  { files[$1] = files[$1] ? files[$1] "\n" $2 : $2; count[$1]++ }
  END {
    for (name in count) {
      if (count[name] > 1) {
        print "=== " name " ==="
        print files[name]
      }
    }
  }'
