#!/bin/bash

FILES=./*.zip


for h in $FILES
do
  unzip "$h"
done

DIRS=./*/
subdircount=`find ./ -mindepth 1 -type d | wc -l`


if [ "$subdircount" -lt 1 ]; then
    echo "no tours here"
    DIR_NAME=${PWD##*/}
    echo "No tours on $DIR_NAME" >> ../day_tours.txt
else
  for d in $DIRS
  do
    echo "cd $d"
    cd $d
    rosrun predicted_maps_utils mapping.sh
    killall roscore
    DIR_NAME=${PWD##*/}
   
    cp ./*.pgm ../
    cd ..
    #zip -r "$DIR_NAME.zip" $DIR_NAME
    rm -fr "$DIR_NAME"
  done
fi

sleep 1

rosrun predicted_maps_utils stitch_maps.py 
