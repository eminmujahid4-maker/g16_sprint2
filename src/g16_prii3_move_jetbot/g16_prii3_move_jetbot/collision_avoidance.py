import rclpy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist

from g16_prii3_move_jetbot.draw_number import DrawNumber


class CollisionAvoidanceWithDrawing(DrawNumber):
    def __init__(self):
        super().__init__()
        self.get_logger().info('Nodo Collision Avoidance con dibujo iniciado.')
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

    def dibujar(self):
        if self.obstacle:
            self.pub.publish(Twist())
            return
        super().dibujar()


def main(args=None):
    rclpy.init(args=args)
    node = CollisionAvoidanceWithDrawing()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()