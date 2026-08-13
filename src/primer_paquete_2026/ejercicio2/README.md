# Ejercicio 2

## Consigna

Crear un nodo que recibe un texto como action server y envía cada palabra del texto como feedback a 1Hz.
Crear otro nodo como action client que reciba un texto como argumento y lo envíe al primer nodo como action. Se subscribe al feedback del primero y lo muestra en la terminal. Cuando el primer nodo indica que terminó, el segundo nodo publica el mensaje “Texto republicado!”
Cree el mensaje custom para hacerlo.
Crear un roslaunch que permita pasar el texto como argumento y ejecute ambos nodos.

## Contenido

- `scripts/ejercicio2_action_server.py`: nodo `ejercicio2_action_server`. Action server (`repeat_text`, interfaz custom `MyAction` en [`../action/MyAction.action`](../action/MyAction.action)). Recibe un texto como goal y devuelve cada palabra como feedback a 1 Hz.
- `scripts/ejercicio2_action_client.py`: nodo `ejercicio2_action_client`. Envía un texto como goal, muestra cada feedback recibido y, cuando el server termina, publica `"Texto republicado!"` en `/texto_republicado` (`std_msgs/String`).

## Interfaz `MyAction`

```
string mytext
---
bool result
---
string words
```

Goal: `mytext` (texto a repetir) · Result: `result` (éxito) · Feedback: `words` (palabra actual).

## Parámetros

| Nodo | Parámetro | Default |
|---|---|---|
| `ejercicio2_action_client` | `text` | `"Hola mundo desde ROS 2"` |

## Ejecución

```bash
ros2 launch primer_paquete_2026 ejercicio2.launch.py text:="tu texto acá"
```

Por separado:
```bash
ros2 run primer_paquete_2026 ejercicio2_action_server.py
ros2 run primer_paquete_2026 ejercicio2_action_client.py --ros-args -p text:="tu texto acá"
```
