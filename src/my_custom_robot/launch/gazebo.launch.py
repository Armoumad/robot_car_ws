#!/usr/bin/env python3
import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory
import xacro

def generate_launch_description():
    pkg_share = get_package_share_directory('my_custom_robot')
    urdf_file = os.path.join(pkg_share, 'urdf', 'my_robot.urdf.xacro')
    world_file = os.path.join(pkg_share, 'worlds', 'empty.world')
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')

    declare_use_sim_time_cmd = DeclareLaunchArgument(
        'use_sim_time', default_value='true', description='Use simulation time'
    )

    robot_description_config = xacro.process_file(urdf_file)
    robot_description = {'robot_description': robot_description_config.toxml()}

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[robot_description, {'use_sim_time': use_sim_time}],
        output='screen'
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'),
                         'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file}.items()
    )

    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'mobile_base'],
        output='screen'
    )

    sp_jsb = Node(package='controller_manager', executable='spawner',
                  arguments=['joint_state_broadcaster'],
                  parameters=[{'use_sim_time': use_sim_time}], output='screen')

    sp_diff = Node(package='controller_manager', executable='spawner',
                   arguments=['diff_drive_controller'],
                   parameters=[{'use_sim_time': use_sim_time}], output='screen')

    return LaunchDescription([
        declare_use_sim_time_cmd,
        robot_state_publisher_node,
        gazebo_launch,
        spawn_robot,
        sp_jsb,
        sp_diff
    ])