#!/usr/bin/env python3
import rclpy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

# Importas tu clase o lógica desde draw_number (si están en el mismo paquete o archivo)
# O simplemente integras el chequeo del láser dentro de tu bucle de dibujo:
from g16_prii3_move_turtlebot.draw_number import DrawNumberTurtlebot # (Ejemplo de importación)

class CollisionAvoidanceWithDrawing(DrawNumberTurtlebot):
    def __init__(self):
        super().__init__()
        # Cambiamos el nombre del nodo si es necesario
        self.get_logger().info('Nodo Collision Avoidance con dibujo iniciado.')
        
        # Añadimos el suscriptor del láser
        self.sub = self.create_subscription(LaserScan, '/scan', self.scan_callback, 10)
        self.safe_distance = 0.5
        self.obstacle = False

    def scan_callback(self, msg: LaserScan):
        if len(msg.ranges) > 0:
            front_distance = msg.ranges[0]
            if front_distance > msg.range_min and front_distance < self.safe_distance:
                if not self.obstacle:
                    self.get_logger().info('¡Obstáculo detectado! Frenando...')
                self.obstacle = True
            else:
                self.obstacle = False



    # Sobrescribimos o adaptamos el método 'dibujar' para que compruebe el obstáculo antes de avanzar
    def dibujar(self):
        if self.obstacle:
            # Si hay obstáculo, detenemos el movimiento pero NO avanzamos el contador de pasos del dibujo
            msg = Twist()
            self.pub.publish(msg)
            return
        
        # Si no hay obstáculo, llamamos al método original de dibujo
        super().dibujar()

def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceWithDrawing()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()