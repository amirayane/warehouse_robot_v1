# ROS2 Warehouse Robot — ARIA

A simulated mobile manipulator robot built with ROS2 and Gazebo.  
ARIA combines a 4-wheeled differential drive base with a UR5e arm and a Robotiq 2F-85 gripper,  
designed for warehouse navigation and manipulation tasks.

---

## Project Status

> This project is actively under development. Some features are incomplete or broken.

| Component | Status |
|-----------|--------|
| Robot model (URDF/Xacro) |  Working |
| Gazebo simulation | Working |
| RViz2 visualization | Working |
| Differential drive (topic commands) | Working |
| Teleop keyboard node | Broken |
| Hand gesture gripper control | Broken |
| UR5e arm control | Incomplete |
| LiDAR sensor | Defined in URDF, not yet active in ROS2 |
| Pick & place demo | incomplete |
| Nav2 autonomous navigation | Planned |

---

## Robot Architecture
ARIA
├── Mobile Base
│   ├── 4 wheels (differential drive)
│   ├── LiDAR dome (gpu_lidar, /scan)
│   └── diff_drive_controller → /diff_drive_controller/cmd_vel
├── UR5e Arm
│   └── joint_trajectory_controller → /joint_trajectory_controller/joint_trajectory
└── Robotiq 2F-85 Gripper
└── Controlled via /joint_states

**ROS2 Control interfaces:**

| Controller | Type | Topic |
|------------|------|-------|
| `diff_drive_controller` | DiffDriveController | `/diff_drive_controller/cmd_vel` |
| `joint_trajectory_controller` | JointTrajectoryController | `/joint_trajectory_controller/joint_trajectory` |
| `joint_state_broadcaster` | JointStateBroadcaster | `/joint_states` |

---

## How to Build

```bash
cd ~/ros2_ws
colcon build --symlink-install
source install/setup.bash
```

---

## How to Launch

### Gazebo simulation

```bash
ros2 launch warehouse_robot gazebo.launch.py
```

>  Controller spawning is delayed (15s for joint_state_broadcaster, 18s for diff_drive). Wait for the terminal to confirm they are active before sending commands.

### RViz2 only 

```bash
ros2 launch warehouse_robot display.launch.py
```

---

## How to Move the Robot

Open a new terminal and source first:

```bash
source ~/ros2_ws/install/setup.bash
```

**Move forward:**
```bash
ros2 topic pub --once /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
"{header: {frame_id: 'base_link'}, twist: {linear: {x: 0.3}, angular: {z: 0.0}}}"
```

**Turn:**
```bash
ros2 topic pub --once /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
"{header: {frame_id: 'base_link'}, twist: {linear: {x: 0.0}, angular: {z: 0.8}}}"
```

**Stop:**
```bash
ros2 topic pub --once /diff_drive_controller/cmd_vel geometry_msgs/msg/TwistStamped \
"{header: {frame_id: 'base_link'}, twist: {linear: {x: 0.0}, angular: {z: 0.0}}}"
```

**Parameters:**
- `linear.x` → forward (`+`) / backward (`-`)
- `angular.z` → turn left (`+`) / turn right (`-`)

---

## Scripts (Partially Working)

### `teleop.py` — Keyboard control
> Currently broken. Intended to let you drive the robot with W/A/S/D keys.  
> The node starts but commands are not received by the controller.

```bash
ros2 run warehouse_robot teleop
```

### `hand_control.py` — MediaPipe gesture control
>  Currently broken. Intended to open/close the gripper using hand gestures via webcam.  
> The node starts and camera opens, but gripper joints do not respond correctly.

```bash
ros2 run warehouse_robot hand_control
```

### `pick_demo.py` — Arm pick & place
>  Abandoned. Intended to move the UR5e arm through a pick sequence.  
> The `joint_trajectory_controller` was commented out in the launch file due to conflicts.

---

## Known Issues

- **Teleop not working** — `TwistStamped` is published but the controller doesn't respond
- **Gripper not responding** — Publishing to `/joint_states` is read-only; gripper needs its own controller
- **Arm controller disabled** — `joint_trajectory_controller` is commented out in `gazebo.launch.py` to avoid conflicts with the diff drive spawner
- **LiDAR defined but inactive** — Sensor exists in the URDF but `/scan` topic is not verified to publish

---

## Planned Work

- [ ] Fix teleop keyboard node
- [ ] Add proper gripper controller (mimic joint or action server)
- [ ] Re-enable and test UR5e arm trajectory controller
- [ ] Verify LiDAR `/scan` output in Gazebo
- [ ] Integrate Nav2 for autonomous navigation
- [ ] Rewrite hand gesture control with correct controller interface

---

## Package Structure
ros2_ws/src/warehouse_robot/
├── config/
│   └── controllers.yaml
├── launch/
│   ├── display.launch.py       
│   └── gazebo.launch.py        
├── urdf/
│   └── aria_robot.urdf.xacro
├── worlds/
│   └── warehouse.world
└── warehouse_robot/
├── teleop.py               
├── hand_control.py         
└── pick_demo.py            
