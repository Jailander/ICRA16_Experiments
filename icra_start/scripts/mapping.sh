#!/bin/bash

i=0

mkdir Maps
mkdir Done
mkdir Fails
FILES=./*.bag

export ROS_MASTER_URI=http://alfred:11312
#roscore -p 11312 &

for f in $FILES
do
  echo "Processing $f file..."
  #echo "Starting roscore..."
  #roscore &
  #echo "done"
  #sleep 2
  
  rosparam set use_sim_time true
  echo "Starting gmapping"
  rosrun gmapping slam_gmapping _maxUrange:=15.0 _xmin:=-20 _ymin:=-25 _xmax:=5 _ymax:=18 _delta:=0.05 _odom_frame:=map _map_frame:=gmap &
  #rosrun gmapping slam_gmapping _delta:=0.05 &
  echo "done"
  sleep 1

  rosbag play -r 10 "$f"
  T=$?
  timeout 100 rosrun map_server map_saver
 
  S=$?
  if [ "${S}" != "0" ]; then
    echo "Map Saver FAILED: ${S}" >> ./fails.txt
    mv "$f" ./Fails/
  else
    mv map.yaml ./Maps/"$f".yaml
    #cp map.pgm ./Maps/"$f"-o.pgm

    #timeout 40 ./mapstitch -o $f.pgm base.pgm map.pgm
    #R=$?
    #if [ "${R}" != "0" ]; then
    #  echo "Mapstitch FAILED: ${R}" >> ./fails.txt
    #fi
    cp map.pgm ./Maps/$f.pgm
    mv "$f" ./Done/
    rm map.pgm
    #cp newbase.pgm base.pgm
  fi
  (( i+=1 ))

  echo "done"
  sleep 1
  echo "Killing gmapping"
  killall slam_gmapping
  echo "done"

  sleep 1
  # take action on each file. $f store current file name
done
