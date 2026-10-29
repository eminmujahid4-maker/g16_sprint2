#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from std_srvs.srv import Empty

def mov(lin, ang, seg):
    return {"lin": lin, "ang": ang, "seg": seg}


MOVS = [
    mov(0.2, 0.0, 10.0),      # palo del 1: 2 m
    mov(0.0, -1.0, 1.57),    # girar 90° a la derecha
    mov(0.2, 0.0, 10.0),      # ir al inicio del 6: 2m
    mov(0.0, 1.0, 3.14),     # girar 180° para mirar hacia atrás
    mov(0.2, 0.0, 5.0),      # 6: barra de arriba (1m)
    mov(0.0, 1.0, 1.57),     # girar 90° a la izquierda
    mov(0.2, 0.0, 10.0),      # 6: lado izquierdo entero (2 m)
    mov(0.0, 1.0, 1.57),     # girar 90° a la izquierda
    mov(0.2, 0.0, 5.0),      # 6: barra de abajo (0.9 m)
    mov(0.0, 1.0, 1.57),     # girar 90° a la izquierda
    mov(0.2, 0.0, 5.0),      # 6: lado derecho de abajo (1m)
    mov(0.0, 1.0, 1.57),     # girar 90° a la izquierda
    mov(0.2, 0.0, 5.0),      # 6: barra del medio (1m)
]

class DrawNumberTurtlebot(Node):
    def __init__(self):
        super().__init__('draw_number_turtlebot')
        self.pub = self.create_publisher(Twist, '/cmd_vel', 10)

        self.reset_cli = self.create_client(Empty, '/reset_simulation')

        self.create_service(Empty, 'stop_drawing', self.stop)
        self.create_service(Empty, 'resume_drawing', self.resume)
        self.create_service(Empty, 'restart_drawing', self.restart)

        self.paso = 0
        self.tiempo = 0.0
        self.pausa = False
        self.timer = self.create_timer(0.05, self.dibujar)
        self.get_logger().info('Nodo draw_number_turtlebot iniciado.')

    def stop(self, request, response):
        self.pausa = True
        self.pub.publish(Twist())
        self.get_logger().info('Dibujo pausado.')
        return response

    def resume(self, request, response):
        self.pausa = False
        self.get_logger().info('Dibujo reanudado.')
        return response

    def restart(self, request, response):
        self.pub.publish(Twist())
        self.reset_cli.call_async(Empty.Request())
        self.paso = 0
        self.tiempo = 0.0
        self.pausa = False
        self.get_logger().info('Dibujo reiniciado.')
        return response

    def dibujar(self):
        if self.pausa or self.paso >= len(MOVS):
            return

        actual = MOVS[self.paso]
        msg = Twist()
        msg.linear.x = actual["lin"]
        msg.angular.z = actual["ang"]
        self.pub.publish(msg)

        self.tiempo += 0.05
        if self.tiempo >= actual["seg"]:
            self.pub.publish(Twist())
            self.paso += 1
            self.tiempo = 0.0

def main(args=None):
    rclpy.init(args=args)
    node = DrawNumberTurtlebot()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()