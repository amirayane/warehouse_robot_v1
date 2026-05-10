from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node
from launch.actions import TimerAction
from ament_index_python.packages import get_package_share_directory
import os
import subprocess


def generate_launch_description():

    pkg_path = get_package_share_directory('warehouse_robot')
    world_path = os.path.join(
        pkg_path,
        'worlds',
        'warehouse.world'
    )
    xacro_file = os.path.join(pkg_path, 'urdf', 'aria_robot.urdf.xacro')

    robot_description = subprocess.check_output(
        ['xacro', xacro_file]
    ).decode('utf-8')

    gazebo = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(
            get_package_share_directory('ros_gz_sim'),
            'launch',
            'gz_sim.launch.py'
        )
    ),
    launch_arguments={
        'gz_args': '-r ' + world_path
    }.items()
)

    robot_state_pub = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': robot_description}]
    )
    
    spawn_robot = Node(
        package='ros_gz_sim',
        executable='create',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'aria_robot',
            '-allow_renaming', 'true'
        ],
        output='screen'
    )

   
    joint_state_broadcaster_spawner = TimerAction(
        period=15.0,
        actions=[Node(
        package='controller_manager',
        executable='spawner',
        arguments=['joint_state_broadcaster'],
        output='screen'
    )]
    )

    # joint_trajectory_spawner = TimerAction(
    #     period=6.0,
    #     actions=[Node(
    #     package='controller_manager',
    #     executable='spawner',
    #     arguments=['joint_trajectory_controller'],
    #     output='screen'
    # )]
    # )

    diff_drive_spawner = TimerAction(
        period=18.0,
        actions=[Node(
        package='controller_manager',
        executable='spawner',
        arguments=['diff_drive_controller'],
        output='screen'
    )]
    )
    

    return LaunchDescription([
        gazebo,
        robot_state_pub,
        spawn_robot,
    
      
        joint_state_broadcaster_spawner,
        # joint_trajectory_spawner,
        diff_drive_spawner 
    ])