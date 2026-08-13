import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, ExecuteProcess
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():
    bag_path_arg = DeclareLaunchArgument(
        'bag_path',
        default_value='/root/ros2_ws/src/r2b_robotarm/r2b_robotarm_0.mcap',
        description='Ruta al archivo .mcap del rosbag r2b_robotarm'
    )

    bag_play = ExecuteProcess(
        cmd=['ros2', 'bag', 'play', LaunchConfiguration('bag_path'), '--clock'],
        output='screen',
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=[
            '-d',
            os.path.join(
                get_package_share_directory('primer_paquete_2026'),
                'crear_pkg', 'rviz', 'tp1.rviz'
            )
        ],
    )

    rqt_node = Node(
        package='rqt_gui',
        executable='rqt_gui',
        name='rqt_gui',
        output='screen',
        arguments=[
            '--perspective-file',
            os.path.join(
                get_package_share_directory('primer_paquete_2026'),
                'crear_pkg', 'rqt', 'tp1.perspective'
            )
        ],
    )

    return LaunchDescription([
        bag_path_arg,
        bag_play,
        rviz_node,
        rqt_node,
    ])
