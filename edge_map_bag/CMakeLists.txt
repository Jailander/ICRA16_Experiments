cmake_minimum_required(VERSION 2.8.3)
project(edge_map_bag)

## Find catkin macros and libraries
## if COMPONENTS list like find_package(catkin REQUIRED COMPONENTS xyz)
## is used, also find other catkin packages
find_package(catkin REQUIRED COMPONENTS
  rosbag
  roscpp
  sensor_msgs
  tf
)


catkin_package(
#  INCLUDE_DIRS include
#  LIBRARIES edge_map_bag
#  CATKIN_DEPENDS rosbag roscpp
#  DEPENDS system_lib
)


###########
## Build ##
###########

## Specify additional locations of header files
## Your package locations should be listed before other locations
# include_directories(include)
include_directories(
  ${catkin_INCLUDE_DIRS}
)


add_executable(edge_bag src/main.cpp)
target_link_libraries(edge_bag ${catkin_LIBRARIES})
#add_dependencies(talker beginner_tutorials_generate_messages_cpp)

#add_executable(listener src/listener.cpp)
#target_link_libraries(listener ${catkin_LIBRARIES})
#add_dependencies(listener beginner_tutorials_generate_messages_cpp)
