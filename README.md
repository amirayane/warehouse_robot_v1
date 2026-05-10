# ROS2 Warehouse Robot Project
This project simulates a mobile warehouse robot in Gazebo and RViz2 using ROS2.  
The robot is designed for warehouse navigation, manipulation, and future autonomous navigation (Nav2).
## Project Status

This project is still under development.

- Robot spawns correctly in Gazebo and RViz2
- Custom warehouse world is loaded
- Differential drive base is working
- Robot can be manually controlled using ROS2 topics

##Robot Movement

The robot is controlled using:

```bash
ros2 topic pub --once /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
"{header: {frame_id: 'base_link'}, twist: {linear: {x: 0.3}, angular: {z: 0.3}}}"

Movement explanation:
linear.x → forward / backward movement
angular.z → turning left / right


## How to Build the Project

Open a terminal and run:

```bash
cd ~/ros2_ws
colcon build
source install/setup.bash

##how to launch the project
#launch gazebo

ros2 launch warehouse_robot gazebo.launch.py


#launch rviz

ros2 launch warehouse_robot display.launch.py

#how to make the robot move 
in a different terminal:
ros2 topic pub --once /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
"{header: {frame_id: 'base_link'}, twist: {linear: {x: 0.3}, angular: {z: 0.0}}}"

#how to make it turn
ros2 topic pub --once /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
"{header: {frame_id: 'base_link'}, twist: {linear: {x: 0.0}, angular: {z: 0.8}}}"

#how to make it stop
ros2 topic pub --once /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
"{header: {frame_id: 'base_link'}, twist: {linear: {x: 0.0}, angular: {z: 0.0}}}"

##note 
#what isnt working yet:

hand_control 
teleop.py

#what will be added:
lidar
nav2