#!/bin/bash
set -e

DIR_PATH="/opt/101025-ptm/VAndreev/DIR/Test"
EXT=("sh" "txt" "jpg")

mkdir -p "$DIR_PATH"

for FILE in {1..10}
   do
     index=$((RANDOM % 3))
#     date '+%T' > "$DIR_PATH/$RANDOM-$FILE"."${EXT[$index]}"
     echo "$DIR_PATH/$RANDOM-$FILE"."${EXT[$index]}"
     sleep 1
   done
