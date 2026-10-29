from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='g16_prii3_move_turtlebot',
            executable='collision_avoidance',
            name='draw_node'
        )
    ])