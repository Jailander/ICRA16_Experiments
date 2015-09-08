#! /usr/bin/env python

import rospy
import sys
import yaml
from datetime import datetime
# Brings in the SimpleActionClient
import actionlib
import topological_navigation.msg


class edge_patroller(object):
    
    def __init__(self, list_of_nodes) :
        
        rospy.on_shutdown(self._on_node_shutdown)
                   
        self.client = actionlib.SimpleActionClient('topological_navigation', topological_navigation.msg.GotoNodeAction)
        
        self.client.wait_for_server()
        rospy.loginfo(" ... Init done")
        
        print "loading %s"%list_of_nodes
        yaml_data=open(list_of_nodes, "r")
    
        data = yaml.load(yaml_data)        
        print data        
        
        sdate = datetime.now()
        print sdate.strftime("%Y-%m-%d %H:%M:%S")
        
        for i in data:
            self.navigate_to(i)

        edate = datetime.now()
        print edate.strftime("%Y-%m-%d %H:%M:%S")
        
        print (edate-sdate).total_seconds()
    
    
    def navigate_to(self, goal):
    
        navgoal = topological_navigation.msg.GotoNodeGoal()
    
        print "Requesting Navigation to %s" %goal
    
        navgoal.target = goal
    
        # Sends the goal to the action server.
        self.client.send_goal(navgoal)#,self.done_cb, self.active_cb, self.feedback_cb)
    
        # Waits for the server to finish performing the action.
        self.client.wait_for_result()
    
        # Prints out the result of executing the action
        ps = self.client.get_result()  # A FibonacciResult
        print ps

    def _on_node_shutdown(self):
        self.client.cancel_all_goals()
        #sleep(2)


if __name__ == '__main__':
    print 'Argument List:',str(sys.argv)
    if len(sys.argv) < 2 :
	sys.exit(2)
    rospy.init_node('edge_patroller')
    ps = edge_patroller(sys.argv[1])