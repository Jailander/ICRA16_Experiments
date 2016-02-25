#! /usr/bin/env python

import os
#import sys
import yaml
import glob
from datetime import datetime
import rospy
# Brings in the SimpleActionClient
#import std_msgs #.msg import String

#import cv2
#import numpy as np

def load_yaml(filename):
    rospy.loginfo("loading %s"%filename)
    with open(filename, 'r') as f:
        return yaml.load(f)

class stitcher(object):
    
    def __init__(self) :
        self.endexec= False
        rospy.on_shutdown(self._on_node_shutdown)
        filenames=[]

        yaml_info = load_yaml('iros_base.yaml')
        print yaml_info
        
        files = glob.glob('./*.pgm')
        print files
        for i in files:
            namestr = (i[2:])[:-4]
            #print namestr
            if namestr != 'iros_base':
                filenames.append(namestr)
        
        for i in filenames:
            yaml_cpy = yaml_info
            epoch = (datetime.strptime(i,"%Y-%m-%d_%H-%M")).strftime('%s')
            print i, epoch
            epochname = epoch+'.pgm'
            yaml_cpy['image']=epochname
            yamlfilename = epoch+'.yaml'
            #yml = yaml.safe_dump(yaml_cpy, default_flow_style=False)
            yml = yaml.safe_dump(yaml_cpy)
            fh = open(yamlfilename, "w")
            s_output = str(yml)
            print s_output
            fh.write(s_output)
            fh.close
            stitchcmdstr = 'rosrun mapstitch mapstitch -o '+epochname+' iros_base.pgm '+i+'.pgm'
            mvcmdstr = 'mv '+epoch+'.* ./stitched_maps/'
            mvcmdstr2 = 'mv '+i+'.* ./processed/'
            print stitchcmdstr
            os.system(stitchcmdstr)
            print mvcmdstr
            os.system(mvcmdstr)
            print mvcmdstr2
            os.system(mvcmdstr2)

#        while not self.endexec :
#        sdate = datetime.now()
#        print sdate.strftime("%Y-%m-%d %H:%M:%S")
#        filename = sdate.strftime("%Y-%m-%d_%H-%M")
#        a,b=rosnode.kill_nodes['/slam_gmapping']
#        print a,b
#        copycmdstr = 'rosrun map_server map_saver -f '+filename+' map:=gmap'
#        print copycmdstr
#        os.system(copycmdstr)
#        os.system('rosnode kill /slam_gmapping')
        
    def _on_node_shutdown(self):
        self.endexec= True
        #sleep(2)


if __name__ == '__main__':
#    print 'Argument List:',str(sys.argv)
#    if len(sys.argv) < 2 :
#	sys.exit(2)
    rospy.init_node('stitcher')
    ps = stitcher()