# g16_prii3_ws

Los nodos dibujan el número 16 con el robot (simulación en Gazebo y robot real Jetbot) y tienen servicios para parar, reanudar y reiniciar el dibujo. También hay un nodo de evitación de colisiones que detiene el robot si hay un obstáculo delante.

## Requisitos

- Ubuntu 22.04
- ROS2 Humble
- Gazebo y Turtlebot3. Se instalan con este comando:

```
sudo apt install ros-humble-gazebo-ros-pkgs ros-humble-turtlebot3-gazebo
```

## Instalación

En una terminal, copia estos comandos:

```
git clone https://github.com/eminmujahid4-maker/g16_sprint2.git g16_prii3_ws
cd g16_prii3_ws
colcon build --symlink-install
source install/setup.bash
```

## Simulación: dibujar el número

Se necesitan dos terminales.

Terminal 1 (abre Gazebo con el robot Waffle en un mundo vacío):

```
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

Terminal 2 (dibuja el número):

```
cd g16_prii3_ws
source install/setup.bash
ros2 launch g16_prii3_move_turtlebot draw_number.launch.py
```

## Simulación: servicios

En otra terminal, desde la carpeta g16_prii3_ws, ejecuta primero:

```
source install/setup.bash
```

Después, para detener, reanudar o reiniciar el dibujo:

```
ros2 service call /stop_drawing std_srvs/srv/Empty
ros2 service call /resume_drawing std_srvs/srv/Empty
ros2 service call /restart_drawing std_srvs/srv/Empty
```



## Simulación: evitación de colisiones

Terminal 1 (igual que antes):

```
export TURTLEBOT3_MODEL=waffle
ros2 launch turtlebot3_gazebo empty_world.launch.py
```

Terminal 2 (dibuja el número y se detiene si hay un obstáculo delante):

```
cd g16_prii3_ws
source install/setup.bash
ros2 launch g16_prii3_move_turtlebot collision_avoidance.launch.py
```

Terminal 3 (cuando el robot esté avanzando, crea un cubo delante de él):

```
cd g16_prii3_ws
source install/setup.bash
ros2 service call /spawn_entity gazebo_msgs/srv/SpawnEntity "{name: 'cubo', xml: '$(cat ~/cubo.sdf)', initial_pose: {position: {x: 1.5, y: 0.0, z: 0.0}}}"
```

El robot se detiene. Para quitar el cubo y que el robot continúe:

```
ros2 service call /delete_entity gazebo_msgs/srv/DeleteEntity "{name: 'cubo'}"
```

Si Gazebo se queda colgado, ciérralo con:

```
pkill gzclient
pkill gzserver
```

## Robot real (Jetbot)

Se conecta al robot por SSH y se necesitan dos terminales dentro del robot.

La primera vez, en el robot:

```
git clone https://github.com/eminmujahid4-maker/g16_sprint2.git
cd g16_prii3_ws
colcon build --symlink-install --packages-select g16_prii3_move_jetbot
source install/setup.bash
```

Terminal 1 (nodo de control del robot):

```
ros2 launch jetbot_pro_ros2 jetbot.py
```

Terminal 2 (dibuja el número):

```
cd g16_prii3_ws
source install/setup.bash
ros2 launch g16_prii3_move_jetbot draw_number.launch.py
```

Para la evitación de colisiones, en la terminal 2 se usa este comando en lugar del anterior:

```
cd g16_prii3_ws
source install/setup.bash
ros2 launch g16_prii3_move_jetbot collision_avoidance.launch.py
```

Los servicios son los mismos que en simulación. En el robot real el reinicio no puede volver a la posición inicial: reinicia el dibujo desde donde esté el robot, así que hay que colocarlo a mano en el punto de salida antes de llamarlo.

## Apagado del Jetbot

Para apagar el robot de forma segura al terminar la práctica, ejecuta por SSH:

```
sudo shutdown now
```
