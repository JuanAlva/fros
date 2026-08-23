import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    SetEnvironmentVariable,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    Command,
    FindExecutable,
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    # ==========================================================================
    # VARIABLES DE ENTORNO
    # Se setean con os.environ (no con SetEnvironmentVariable) porque deben estar
    # disponibles ANTES de que cualquier proceso hijo arranque. SetEnvironmentVariable
    # es una acción del grafo de launch y se ejecuta demasiado tarde para esto.
    # ==========================================================================

    os.environ['GZ_SIM_SYSTEM_PLUGIN_PATH'] = (
        '/opt/ros/jazzy/opt/gz_sim_vendor/lib/gz-sim-8/plugins:'
        + os.environ.get('GZ_SIM_SYSTEM_PLUGIN_PATH', '')
    )

    # ==========================================================================
    # PATHS DEL PAQUETE
    # ==========================================================================

    pkg_share = FindPackageShare('primer_paquete_2026').find('primer_paquete_2026')

    # ==========================================================================
    # ACCIONES DE ENTORNO
    # ==========================================================================

    set_resource_path = SetEnvironmentVariable(
        'GZ_SIM_RESOURCE_PATH',
        os.path.join(pkg_share, '..') + ':' +  # share/ → Gazebo encuentra primer_paquete_2026/ejercicio5/robot_description/...
        os.path.join(pkg_share, 'ejercicio5', 'models') + ':' +
        os.environ.get('GZ_SIM_RESOURCE_PATH', '')
    )

    # ==========================================================================
    # ARGUMENTOS DE LAUNCH
    # ==========================================================================

    arg_use_sim_time = DeclareLaunchArgument(
        'use_sim_time',
        default_value='true',
        description='True para usar un clock simulado'
    )

    arg_xacro_file = DeclareLaunchArgument(
        'xacro_file',
        default_value='dp/dp.xacro',
        description='Archivo de definición del robot'
    )

    arg_world_name = DeclareLaunchArgument(
        'world_name',
        default_value='mundo_vacio.world',
        description='Nombre del archivo del mundo para Gazebo'
    )

    # ==========================================================================
    # DESCRIPCIÓN DEL ROBOT
    # ==========================================================================

    robot_description = {
        'robot_description': Command([
            FindExecutable(name='xacro'), ' ',
            PathJoinSubstitution([
                FindPackageShare('primer_paquete_2026'),
                'ejercicio5', 'robot_description',
                LaunchConfiguration('xacro_file')
            ]),
        ])
    }

    # ==========================================================================
    # NODOS DE INFRAESTRUCTURA
    # ==========================================================================

    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[robot_description]
    )

    node_gz_spawn_entity = Node(
        package='ros_gz_sim',
        executable='create',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-name', 'mi_robot',
            '-allow_renaming', 'true',
            '-x', '0.0',
            '-y', '0.0',
            '-z', '0.553',
        ],
    )

    node_bridge = Node(
        package='ros_gz_bridge',
        executable='parameter_bridge',
        arguments=[
            '/clock@rosgraph_msgs/msg/Clock[gz.msgs.Clock',
            '/world/mundo_simulacion/model/mi_robot/joint_state@sensor_msgs/msg/JointState[gz.msgs.Model',
            '/imu@sensor_msgs/msg/Imu[gz.msgs.IMU',
            '/model/mi_robot/joint/joint1/cmd_force@std_msgs/msg/Float64]gz.msgs.Double',
            '/model/mi_robot/joint/joint2/cmd_force@std_msgs/msg/Float64]gz.msgs.Double',
        ],
        remappings=[
            ('/world/mundo_simulacion/model/mi_robot/joint_state', '/joint_states'),
        ],
        output='screen'
    )

    # ==========================================================================
    # LAUNCH DE GAZEBO
    # ==========================================================================

    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare('ros_gz_sim'),
                'launch',
                'gz_sim.launch.py'
            ])
        ]),
        launch_arguments=[(
            'gz_args', [
                '-v 1 ',
                PathJoinSubstitution([
                    FindPackageShare('primer_paquete_2026'),
                    'ejercicio5', 'worlds',
                    LaunchConfiguration('world_name')
                ]),
                ' --gui-config ',
                PathJoinSubstitution([
                    FindPackageShare('primer_paquete_2026'),
                    'ejercicio5', 'config', 'gazebo.config'
                ])
            ]
        )]
    )

    # ==========================================================================
    # NODOS DE USUARIO
    # ==========================================================================

    node_rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='log',
        arguments=['-d', os.path.join(pkg_share, 'ejercicio5', 'config', 'display.rviz')]
    )

    node_gui_torque = Node(
        package='primer_paquete_2026',
        executable='gui_apply_torque.py',
        name='gui_apply_torque',
        parameters=[{'robot_name': 'mi_robot'}],
        output='screen',
    )

    # ==========================================================================
    # LAUNCH DESCRIPTION
    # ==========================================================================

    return LaunchDescription([
        arg_use_sim_time,
        arg_xacro_file,
        arg_world_name,

        set_resource_path,

        launch_gazebo,

        node_robot_state_publisher,
        node_gz_spawn_entity,
        node_bridge,

        node_rviz,
        node_gui_torque,
    ])
