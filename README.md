# ROS2 Warehouse Robot Project

## Project Status

This project is still under development.

The robot model can currently be displayed in:
- Gazebo
- RViz2

The robot movement and controller system are not fully working yet due to simulation and gripper integration errors.

---

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



