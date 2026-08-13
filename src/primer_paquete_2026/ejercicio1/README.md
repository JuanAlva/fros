# Ejercicio 1

## Consigna

Proveer un paquete de ROS con un launch file con dos nodos:
- Un nodo publica cinco veces por segundo un contador. Este nodo tiene un servicio que resetea su contador.
- Un segundo nodo está suscrito al primero y cuando el mensaje con el contador llega a 50 (cada 10 segundos), resetea el contador del nodo.
- Ambos nodos pueden configurar por parámetros:
    - Nodo publicando:
        - Frecuencia que publica.
        - Cantidad máxima que publica.
    - Nodo suscrito:
        - A qué número reinicia el contador del nodo.
- Launchfile que lance todo y permita configurar la frecuencia y el número en el que se reinicia como argumentos.

## Contenido

- `scripts/ejercicio1_publisher.py`: nodo `counter_publisher`. Publica un contador incremental en `counter_topic` (`std_msgs/Int32`) y expone el servicio `reset_counter` (`std_srvs/Trigger`) para resetearlo a 0.
- `scripts/ejercicio1_subscriber.py`: nodo `counter_subscriber`. Se suscribe a `counter_topic`; cuando el valor recibido llega a `reset_value`, llama al servicio `reset_counter`.

## Parámetros

| Nodo | Parámetro | Default | Descripción |
|---|---|---|---|
| `counter_publisher` | `timer_period` | `0.2` s (5 Hz) | Frecuencia de publicación |
| `counter_publisher` | `counter_max` | `100` | Valor tope antes de que el publisher se apague |
| `counter_subscriber` | `reset_value` | `50` | Valor del contador en el que se dispara el reset |

## Ejecución

Con el launch (ambos nodos, parámetros configurables como argumentos):
```bash
ros2 launch primer_paquete_2026 ejercicio1.launch.py
ros2 launch primer_paquete_2026 ejercicio1.launch.py timer_period:=0.1 reset_value:=20
```

Por separado:
```bash
ros2 run primer_paquete_2026 ejercicio1_publisher.py
ros2 run primer_paquete_2026 ejercicio1_subscriber.py
```
