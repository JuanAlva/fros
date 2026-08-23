# primer_paquete_2026

Paquete único de ROS 2 (`ament_cmake`) con la resolución de los ejercicios de la materia. Se optó por la opción de "un solo paquete" (en vez de un paquete por ejercicio) porque `ejercicio2` depende de la interfaz custom `MyAction`, que requiere `rosidl`/`ament_cmake` y no puede generarse desde un paquete `ament_python` puro. Cada ejercicio tiene su propia carpeta con su código (`scripts/`) y su `README.md`.

## Estructura

```
primer_paquete_2026/
├── ejercicio1/
│   ├── scripts/            # ejercicio1_publisher.py, ejercicio1_subscriber.py
│   └── README.md
├── ejercicio2/
│   ├── scripts/            # ejercicio2_action_server.py, ejercicio2_action_client.py
│   └── README.md
├── ejercicio3/              # Sin código: análisis de TF2 sobre clase3
│   └── README.md
├── ejercicio4/               # Sin código Python: modelo URDF/XACRO extendido
│   ├── robot_description/
│   └── config/
├── action/                    # Interfaz custom (MyAction.action), usada por ejercicio2
└── launch/                     # Un launch file por ejercicio
    ├── ejercicio1.launch.py
    ├── ejercicio2.launch.py
    └── ejercicio4.launch.py
```

## Ejercicios

- [Ejercicio 1](ejercicio1/README.md) — Publisher/Subscriber con reset por servicio.
- [Ejercicio 2](ejercicio2/README.md) — Action server/client con feedback palabra por palabra.
- [Ejercicio 3](ejercicio3/README.md) — Análisis de TF2 sobre `clase3` (sin código propio).
- [Ejercicio 4](ejercicio4/README.md) — Extensión XACRO del doble péndulo.

## TP Final — Manipulación con MyCobot320

Escenario de manipulación con el MyCobot320 y la pinza `adaptive_gripper` (`clase4`), usando `ros2_control` y MoveIt2: mundo de Gazebo con 3 objetos sobre un escritorio, esos mismos objetos como obstáculos en la Planning Scene, y un script que lleva el efector final a una pose de pre-grasp planificando y ejecutando una trayectoria que los esquiva.

### Estructura




```
primer_paquete_2026/
├── launch/
│   └── tp_final.launch.py           # Gazebo + ros2_control + MoveIt + RViz + PlotJuggler
└── tp_final/
    ├── robot_description/
    │   ├── mycobot_320_m5_2022/
    │   │   ├── mycobot_320_m5_2022.xacro       # brazo + garra fusionados + ros2_control
    │   │   ├── mycobot_320_m5_2022_bak.xacro   # backup sin garra (checkpoint previo)
    │   │   └── *.dae                            # mallas del brazo
    │   └── adaptive_gripper/
    │       ├── mycobot_adaptive_gripper.urdf    # referencia original de clase4 (sin usar)
    │       └── *.dae                            # mallas de la garra
    ├── config/
    │   ├── display.rviz
    │   ├── gazebo.config
    │   ├── plotjuggler_layout.xml
    │   └── mycobot_320_m5_2022/
    │       ├── ros2_controllers.yaml            # joint_trajectory_controller + gripper_action_controller
    │       └── moveit/
    │           ├── mycobot_320_m5_2022.srdf     # grupos + end_effector
    │           ├── kinematics.yaml
    │           ├── joint_limits.yaml
    │           ├── moveit_controllers.yaml
    │           ├── ompl_planning.yaml
    │           ├── pilz_cartesian_limits.yaml
    │           ├── pilz_industrial_motion_planner_planning.yaml
    │           └── stomp_planning.yaml
    ├── worlds/
    │   ├── mundo_escritorio.world               # el que usa el TP: escritorio + 3 objetos
    │   ├── mundo_obstaculos.world                # heredado de clase6/7, no usado acá
    │   ├── mundo_suelo.world                     # heredado, no usado
    │   └── mundo_vacio.world                     # heredado, no usado
    ├── models/Desk/                              # modelo del escritorio (mesh)
    └── scripts/
        ├── pregrasp_goal.py                      # pre-grasp: planifica y ejecuta
        ├── hello_moveit.py                       # referencia/debug (clase7)
        ├── hello_moveit_obstacles.py              # referencia/debug (clase7)
        ├── move_to_joints.py                      # referencia/debug (clase7)
        └── move_to_pose.py                        # referencia/debug (clase7)
```

### Archivos modificados vs. nuevos

**Modificados** (ya existían en el paquete):
- `CMakeLists.txt` — reglas de instalación de `tp_final/` y de los scripts nuevos.
- `package.xml` — dependencias de MoveIt/`ros2_control`.

**Nuevos** (creados/adaptados para este TP, no existían antes):
- `launch/tp_final.launch.py`
- `tp_final/robot_description/mycobot_320_m5_2022/mycobot_320_m5_2022.xacro` (fusión brazo + garra)
- `tp_final/config/mycobot_320_m5_2022/ros2_controllers.yaml`
- `tp_final/config/mycobot_320_m5_2022/moveit/mycobot_320_m5_2022.srdf`
- `tp_final/worlds/mundo_escritorio.world` (variante propia, con los 3 objetos de agarre)
- `tp_final/scripts/pregrasp_goal.py`

El resto de `tp_final/` (mallas del brazo y la garra, `models/Desk/`, configs de MoveIt sin tocar, los mundos no usados, y los scripts de referencia `hello_moveit*.py`/`move_to_*.py`) son copias de `clase4`/`clase7`, reutilizadas tal cual salvo el ajuste de `package://` en las mallas.

### Ejecución

```bash
# 1. Compilar
colcon build --packages-select primer_paquete_2026 --symlink-install
source install/setup.bash

# 2. Lanzar la simulación completa (Gazebo + ros2_control + MoveIt + RViz)
ros2 launch primer_paquete_2026 tp_final.launch.py
```

Al arrancar, a veces `joint_state_broadcaster` no llega a activarse solo por una carrera de timing contra Gazebo. Si en RViz ves el robot sin transformadas (TF) o `ros2 control list_controllers` lo muestra `inactive`, activalo a mano:

```bash
ros2 control set_controller_state joint_state_broadcaster active
```

Con la simulación corriendo, en otra terminal:

```bash
# 3. Enviar el goal de pre-grasp (planifica y ejecuta esquivando los 3 objetos)
ros2 run primer_paquete_2026 pregrasp_goal.py
```

### Estado conocido / pendiente

- La garra (`adaptive_gripper`) está modelada e integrada en el URDF, pero sus joints quedaron **fijos** (no revolute): el motor de físicas de esta instalación no soporta la restricción `<mimic>`, y sin ella los dedos quedaban libres auto-colisionando hasta abortar la simulación. Actuar la garra de verdad (abrir/cerrar) queda como trabajo futuro, con otra estrategia de sincronización de los joints seguidores.
- Los gains de PID (`ros2_controllers.yaml`) están tuneados para sostener el brazo en home de forma estable; si se agrega carga extra al efector final, pueden necesitar reajuste (ver clase6).

## Build

```bash
colcon build --packages-select primer_paquete_2026 --symlink-install
```
