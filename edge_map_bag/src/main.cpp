
//#include <sstream>
#include <string>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/LaserScan.h"
#include "tf2_msgs/TFMessage.h"
#include "strands_navigation_msgs/NavStatistics.h"
#include "geometry_msgs/PoseWithCovarianceStamped.h"

#include <rosbag/bag.h>

rosbag::Bag bag;
bool save=false;


void laserCallback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
 // ROS_INFO("I heard: [%s]", msg->data.c_str());
    if(save) bag.write("/scan", ros::Time::now(), msg);
    //ROS_INFO("Laser[%d]", save);
}


void tfCallback(const tf2_msgs::TFMessage::ConstPtr& msg)
{
    if(save) bag.write("/tf", ros::Time::now(), msg);
}


void navstatsCallback(const strands_navigation_msgs::NavStatistics::ConstPtr& msg)
{
    if(save) bag.write("/topological_navigation/Statistics", ros::Time::now(), msg);
    ROS_INFO("navStats [%d]", save);
}


void amclCallback(const geometry_msgs::PoseWithCovarianceStamped::ConstPtr& msg)
{
    if(save) bag.write("/amcl_pose", ros::Time::now(), msg);
    ROS_INFO("amcl [%d]", save);
}


void edgeCallback(const std_msgs::String::ConstPtr& msg)
{
    ROS_INFO("Current Edge: [%s, %d]", msg->data.c_str(), (int)save);
    if(!strcmp(msg->data.c_str(), "none"))
    {
        ROS_INFO("No edge being traversed stop recording");
        save = false;
        bag.close();
    }
    else
    {
        if(save)
        {
            save = false;
            bag.close();
        }
        ros::Time begin = ros::Time::now();
        char stime[20];
        sprintf(stime,"%d",begin.sec);
        std::string bagname = std::string(stime) + "_" + msg->data + ".bag"; //.c_str() + ".bag";
        ROS_INFO("Recording info for [%s]", bagname.c_str());
        bag.open(bagname.c_str(), rosbag::bagmode::Write);
        //bag.open(bagname, rosbag::bagmode::Write);
        save = true;
    }
}




int main(int argc, char **argv)
{
  /**
   * The ros::init() function needs to see argc and argv so that it can perform
   */
  ros::init(argc, argv, "edge_bag");

  /**
   * NodeHandle is the main access point to communications with the ROS system.
   */
  ros::NodeHandle n;

  /**
   * The subscribe() call is how you tell ROS that you want to receive messages
   */
  ros::Subscriber sub = n.subscribe("/scan", 10, laserCallback);
  ros::Subscriber subtf = n.subscribe("/tf", 1000, tfCallback);
  ros::Subscriber subce = n.subscribe("/current_edge", 1, edgeCallback);
  ros::Subscriber subns = n.subscribe("/topological_navigation/Statistics", 1, navstatsCallback);
  ros::Subscriber subamcl = n.subscribe("/amcl_pose", 1, amclCallback);



  /**
   * ros::spin() will enter a loop, pumping callbacks.  With this version, all
   */
  ros::spin();

  //bag.close();

  return 0;
}
