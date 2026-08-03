import launch
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    text_arg = launch.actions.DeclareLaunchArgument(
        'text',
        default_value='Hola mundo desde ROS 2',
        description='Texto a enviar al action server, palabra por palabra'
    )

    server_node = Node(
        package='primer_paquete_2026',
        executable='clase2_action_server.py',
        name='clase2_action_server',
        output='screen',
    )

    client_node = Node(
        package='primer_paquete_2026',
        executable='clase2_action_client.py',
        name='clase2_action_client',
        output='screen',
        parameters=[
            {'text': LaunchConfiguration('text')}
        ],
    )

    ld = launch.LaunchDescription()
    ld.add_action(text_arg)
    ld.add_action(server_node)
    ld.add_action(client_node)

    return ld
