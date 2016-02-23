#!/bin/bash

SESSION=$USER

tmux -2 new-session -d -s $SESSION
# Setup a window for tailing log files
tmux new-window -t $SESSION:0 -n 'roscore'
tmux new-window -t $SESSION:1 -n 'core'
tmux new-window -t $SESSION:2 -n 'robot'
tmux new-window -t $SESSION:3 -n 'cameras'
tmux new-window -t $SESSION:4 -n 'ui'
tmux new-window -t $SESSION:5 -n 'navigation'
tmux new-window -t $SESSION:6 -n 'gmapping'
tmux new-window -t $SESSION:7 -n 'Rviz'


tmux select-window -t $SESSION:0
tmux split-window -v
tmux select-pane -t 0
tmux send-keys "roscore" C-m
tmux resize-pane -U 30
tmux select-pane -t 1
tmux send-keys "htop" C-m

tmux select-window -t $SESSION:1
tmux send-keys "DISPLAY=:0 roslaunch mongodb_store mongodb_store.launch db_path:=/opt/strands/aaf_datacentre"

tmux select-window -t $SESSION:2
tmux send-keys "DISPLAY=:0 roslaunch strands_bringup strands_robot.launch with_mux:=false"

tmux select-window -t $SESSION:3
tmux send-keys "DISPLAY=:0 roslaunch strands_bringup strands_cameras.launch head_camera:=true head_ip:=left-cortex head_user:=strands chest_camera:=true chest_ip:=right-cortex chest_user:=strands"

tmux select-window -t $SESSION:4
tmux send-keys "rosparam set /deployment_language english && HOST_IP=192.168.0.100 DISPLAY=:0 roslaunch strands_ui strands_ui.launch mary_machine:=right-cortex mary_machine_user:=strands"

tmux select-window -t $SESSION:5
tmux send-keys "DISPLAY=:0 roslaunch DISPLAY=:0 roslaunch icra_start icra_nav.launch map:=/opt/strands/maps/WW_GF_2015_09_08-cropped.yaml topological_map:=WW_GF_2015_09_11"

tmux select-window -t $SESSION:6
tmux send-keys "DISPLAY=:0 roslaunch icra_start iros_gmapping.launch"

tmux select-window -t $SESSION:7
tmux send-keys "DISPLAY=:0 rviz"

# Set default window
tmux select-window -t $SESSION:0

# Attach to session
tmux -2 attach-session -t $SESSION

tmux setw -g mode-mouse off