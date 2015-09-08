
//#include <sstream>
#include <string>

#include "ros/ros.h"
#include "std_msgs/String.h"
#include "sensor_msgs/LaserScan.h"
#include "tf2_msgs/TFMessage.h"
#include <rosbag/bag.h>

rosbag::Bag bag;
bool save=false;


/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */
void laserCallback(const sensor_msgs::LaserScan::ConstPtr& msg)
{
 // ROS_INFO("I heard: [%s]", msg->data.c_str());
    if(save) bag.write("/scan", ros::Time::now(), msg);
    //ROS_INFO("Laser[%d]", save);
}


/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */
void tfCallback(const tf2_msgs::TFMessage::ConstPtr& msg)
{
 // ROS_INFO("I heard: [%s]", msg->data.c_str());
    if(save) bag.write("/tf", ros::Time::now(), msg);
    //ROS_INFO("tf [%d]", save);
}


/**
 * This tutorial demonstrates simple receipt of messages over the ROS system.
 */
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
        std::string bagname = msg->data + "_" + std::string(stime) +".bag"; //.c_str() + ".bag";
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
   * any ROS arguments and name remapping that were provided at the command line.
   * For programmatic remappings you can use a different version of init() which takes
   * remappings directly, but for most command-line programs, passing argc and argv is
   * the easiest way to do it.  The third argument to init() is the name of the node.
   *
   * You must call one of the versions of ros::init() before using any other
   * part of the ROS system.
   */
  ros::init(argc, argv, "edge_bag");

  /**
   * NodeHandle is the main access point to communications with the ROS system.
   * The first NodeHandle constructed will fully initialize this node, and the last
   * NodeHandle destructed will close down the node.
   */
  ros::NodeHandle n;

  /**
   * The subscribe() call is how you tell ROS that you want to receive messages
   * on a given topic.  This invokes a call to the ROS
   * master node, which keeps a registry of who is publishing and who
   * is subscribing.  Messages are passed to a callback function, here
   * called chatterCallback.  subscribe() returns a Subscriber object that you
   * must hold on to until you want to unsubscribe.  When all copies of the Subscriber
   * object go out of scope, this callback will automatically be unsubscribed from
   * this topic.
   *
   * The second parameter to the subscribe() function is the size of the message
   * queue.  If messages are arriving faster than they are being processed, this
   * is the number of messages that will be buffered up before beginning to throw
   * away the oldest ones.
   */
  ros::Subscriber sub = n.subscribe("/scan", 10, laserCallback);
  ros::Subscriber subtf = n.subscribe("/tf", 1000, tfCallback);
  ros::Subscriber subce = n.subscribe("/current_edge", 1, edgeCallback);

  //bag.open("test.bag", rosbag::bagmode::Write);

  /**
   * ros::spin() will enter a loop, pumping callbacks.  With this version, all
   * callbacks will be called from within this thread (the main one).  ros::spin()
   * will exit when Ctrl-C is pressed, or the node is shutdown by the master.
   */
  ros::spin();

  //bag.close();

  return 0;
}
