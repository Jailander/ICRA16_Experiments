#! /usr/bin/env python


import sys
import os
import rospy
import yaml
from datetime import datetime
# Brings in the SimpleActionClient
import actionlib
import topological_navigation.msg
import std_msgs #.msg import String
import scitos_msgs #/ResetOdometry


class patroller(object):
    
    def __init__(self, list_of_nodes) :
        self.endexec= False
        rospy.on_shutdown(self._on_node_shutdown)
                   
        self.client = actionlib.SimpleActionClient('topological_navigation', topological_navigation.msg.GotoNodeAction)
        
        self.client.wait_for_server()
        rospy.loginfo(" ... Init done")
        
        print "loading %s"%list_of_nodes
        yaml_data=open(list_of_nodes, "r")
    
        data = yaml.load(yaml_data)        
        print data['freq']
        print data['nodes']
        
       
        while not self.endexec :
            sdate = datetime.now()
            print sdate.strftime("%Y-%m-%d %H:%M:%S")
            if sdate.minute%data['freq'] == 0 :
                
                try:
                    current_node = rospy.wait_for_message('/current_node', std_msgs.msg.String, timeout=10.0)
                except rospy.ROSException :
                    rospy.logwarn("Failed to get current node")
                
                print current_node
                if current_node.data == 'ChargingPoint':
                    print "Reset Odometry"
                    self.reset_odom()
                    
                try:
                    start_mileage = rospy.wait_for_message('/odom_mileage', std_msgs.msg.Float32, timeout=10.0)
                except rospy.ROSException :
                    rospy.logwarn("Failed to get mileage")
   
                for i in data['nodes']:
                    self.navigate_to(i)

                edate = datetime.now()
                print edate.strftime("%Y-%m-%d %H:%M:%S")
                
                try:
                    end_mileage = rospy.wait_for_message('/odom_mileage', std_msgs.msg.Float32, timeout=10.0)
                except rospy.ROSException :
                    rospy.logwarn("Failed to get mileage")

                self.save_data(sdate, edate, start_mileage, end_mileage)
                
                

            else:
                rospy.sleep(30.)
                

    def save_data(self, sdate, edate, start_mileage, end_mileage):
        stats={}

        print sdate.strftime("%Y-%m-%d %H:%M:%S")
        filename = sdate.strftime("%Y-%m-%d_%H-%M")
        copycmdstr = 'rosrun map_server map_saver -f '+filename+' map:=gmap'
        print copycmdstr
        os.system(copycmdstr)
        os.system('rosnode kill /slam_gmapping')
        
        stats['start']=sdate.strftime('%s')
        stats['end']=edate.strftime('%s')
        dur = (edate-sdate).total_seconds()
        stats['total_time']=dur
        stats['distance']=end_mileage.data-start_mileage.data
        
               
        yml = yaml.safe_dump(stats, default_flow_style=False)
        filename2 = 'stats_'+filename+'.yaml'
        fh = open(filename2, "w")
        s_output = str(yml)
        fh.write(s_output)
        fh.close          


    def reset_odom(self):
        try:
            rospy.wait_for_service('/reset_odometry', timeout=3)
            try:
                reset = rospy.ServiceProxy('/reset_odometry', scitos_msgs.srv.ResetOdometry)
                resp1 = reset()
                print resp1
                #return True
            except rospy.ServiceException, e:
                print "Service call failed: %s"%e
        except Exception, e:
            rospy.logwarn('reset odometry service not available')

    
    
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
        self.endexec= True
        #sleep(2)


if __name__ == '__main__':
    print 'Argument List:',str(sys.argv)
    if len(sys.argv) < 2 :
	sys.exit(2)
    rospy.init_node('edge_patroller')
    ps = patroller(sys.argv[1])
