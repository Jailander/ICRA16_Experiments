#!/bin/bash

i=0

mkdir ST
mkdir Done

FILES=./*.pgm

export ROS_MASTER_URI=http://alfred:11312
#roscore -p 11312 &

for f in $FILES
do
  echo "Processing $f file..."
  rosrun mapstitch mapstitch -o out.pgm base.pgm "$f"
  R=$?
  if [ "${R}" != "0" ]; then
     echo "Mapstitch FAILED: ${R}" >> ./fails.txt
  else
     cp out.pgm ./ST/"$f"
     mv $f ./Done
  fi
  
  #sleep 1
  # take action on each file. $f store current file name
done
