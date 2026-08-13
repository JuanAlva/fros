import launch
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    counter_max_arg = launch.actions.DeclareLaunchArgument(
        'counter_max',
        default_value='100',
        description='Maximum count value before publisher shuts down'
    )

    timer_period_arg = launch.actions.DeclareLaunchArgument(
        'timer_period',
        default_value='0.2',
        description='Timer period in seconds for publishing counter values (0.2 = 5 Hz)'
    )

    reset_arg = launch.actions.DeclareLaunchArgument(
        'reset_value',
        default_value='50',
        description='Counter value at which the subscriber resets the publisher'
    )

    publisher_node = Node(
        package='primer_paquete_2026',
        executable='ejercicio1_publisher.py',
        name='counter_publisher',
        output='screen',
        parameters=[
            {'counter_max': LaunchConfiguration('counter_max')},
            {'timer_period': LaunchConfiguration('timer_period')}
        ],
        on_exit=launch.actions.Shutdown()
    )

    subscriber_node = Node(
        package='primer_paquete_2026',
        executable='ejercicio1_subscriber.py',
        name='counter_subscriber',
        output='screen',
        parameters=[
            {'reset_value': LaunchConfiguration('reset_value')}
        ]
    )

    ld = launch.LaunchDescription()
    ld.add_action(counter_max_arg)
    ld.add_action(timer_period_arg)
    ld.add_action(reset_arg)
    ld.add_action(publisher_node)
    ld.add_action(subscriber_node)

    return ld
