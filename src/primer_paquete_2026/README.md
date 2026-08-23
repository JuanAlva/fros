# primer_paquete_2026

Paquete único de ROS 2 (`ament_cmake`) con la resolución de los ejercicios de la materia. Se optó por la opción de "un solo paquete" (en vez de un paquete por ejercicio) porque `ejercicio2` depende de la interfaz custom `MyAction`, que requiere `rosidl`/`ament_cmake` y no puede generarse desde un paquete `ament_python` puro. Cada ejercicio tiene su propia carpeta con su código (`scripts/`) y su `README.md`.

## Build

```bash
colcon build --packages-select primer_paquete_2026 --symlink-install
```

### Ejecución

```bash
# 1. Compilar
colcon build --packages-select primer_paquete_2026 --symlink-install
source install/setup.bash

# 2. Lanzar la simulación completa (Gazebo + ros2_control + MoveIt + RViz)
ros2 launch primer_paquete_2026 tp_final.launch.py
```

Al arrancar, a veces `joint_state_broadcaster` no llega a activarse solo por una carrera de timing contra Gazebo.

```bash
ros2 control set_controller_state joint_state_broadcaster active
```

Con la simulación corriendo, en otra terminal:

```bash
# 3. Enviar el goal de pre-grasp (planifica y ejecuta esquivando los 3 objetos)
ros2 run primer_paquete_2026 pregrasp_goal.py
```
