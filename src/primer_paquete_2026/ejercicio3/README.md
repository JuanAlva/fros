# Ejercicio 3 — Análisis del doble péndulo (`clase3`)

Resolución de los puntos 1 a 4 de `ejercicio3.md`, verificada corriendo `ros2 launch clase3 dp_launch.py`.

## 1. Nodos del sistema

- `robot_state_publisher`: lee el URDF y publica el árbol de TF.
- `joint_state_publisher_gui`: sliders para `joint1` y `joint2`, publica sus valores.
- `rviz2`: visualización del robot y del TF.

## 2. Tópicos activos

- `/joint_states` — publica `joint_state_publisher_gui`.
- `/tf` — publica `robot_state_publisher` (joints móviles: `base_link→link1`, `link1→link2`).
- `/tf_static` — publica `robot_state_publisher` (joints fijos: `world→base_link`, `link2→tool0`).
- `/robot_description` — publica `robot_state_publisher` (URDF).

## 3. Árbol de TF2

```
world → base_link → link1 → link2 → tool0
        (fixed)    (joint1)  (joint2)  (fixed)
```

`world→base_link` y `link2→tool0` son fijos (van por `/tf_static`). `base_link→link1` y `link1→link2` dependen del ángulo de cada joint (van por `/tf`).

## 4. Transformación base_link → tool0 (pose actual)

Con los sliders centrados (`joint1=0`, `joint2=0`), medido con `ros2 run tf2_ros tf2_echo base_link tool0`:

- Traslación: `(0.4, 0, 0.07)` m
- Rotación: identidad

Sale de sumar los offsets de la cadena: `0.05 + 0.02 = 0.07` en Z, `0.2 + 0.2 = 0.4` en X. Como los dos joints son revoluciones en Z y están en 0°, no hay rotación neta. En general (para cualquier ángulo) es la composición `Trans(0,0,0.05)·Rz(θ1)·Trans(0.2,0,0.02)·Rz(θ2)·Trans(0.2,0,0)`.
