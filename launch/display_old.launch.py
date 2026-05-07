from launch import LaunchDescription
from launch_ros.actions import Node
import subprocess
import os

def generate_launch_description():

    xacro_file = os.path.expanduser(
        '~/ros2_ws/src/warehouse_robot/urdf/aria_robot.urdf.xacro'
    )

    robot_description = subprocess.check_output(
        ['xacro', xacro_file]
    ).decode('utf-8')

    return LaunchDescription([

        # Robot state publisher (keeps TF tree working)
        Node(
            package='robot_state_publisher',
            executable='robot_state_publisher',
            parameters=[{'robot_description': robot_description}]
        ),

        # Joint state GUI (manual testing of movement)
        Node(
            package='joint_state_publisher_gui',
            executable='joint_state_publisher_gui'
        ),

        # ROS2 Control Manager (ADDED for movement control)
        Node(
            package='controller_manager',
            executable='ros2_control_node',
            parameters=[
                {'robot_description': robot_description},
                os.path.expanduser('~/ros2_ws/src/warehouse_robot/config/controllers.yaml')
            ],
            output='screen'
        ),

        # RViz visualization
        Node(
            package='rviz2',
            executable='rviz2'
        )
    ])