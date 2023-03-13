import rclpy
import pynput
import pygame
from pynput import keyboard
import time
from rclpy.node import Node
from os.path import abspath

from geometry_msgs.msg import Twist


class TurtleBotTeleop(Node):

    def __init__(self):
        super().__init__('turtle_bot_teleop')
        self.publisher_ = self.create_publisher(Twist, 'turtlebot_cmdVel', 20)
        joystick = pygame.joystick.get_count()
        joystick.init()
        #listener = keyboard.Listener(on_press=self.on_presss, on_release=self.on_release)
        #listener.start()
        self.linear = float(input("Ingrese la velocidad lineal: "))
        self.angular = float(input("Ingrese la velocidad angular: "))
        self.prevchar = ''

    def on_presss(self, key):

        if not(hasattr(key, 'char')): 
            self.get_logger().info('Invalid input')
            return # evitar que muera la terminal
        
        msg = Twist()
        if key.char == 'w':
            msg.linear.x=self.linear
            self.get_logger().info('Publishing: Adelante')
        elif key.char == 's':
            msg.linear.x=-self.linear
            self.get_logger().info('Publishing: Atras')
        elif key.char == 'a':
            msg.angular.z=self.angular
            self.get_logger().info('Publishing: Izquierda')
        elif key.char == 'd':
            msg.angular.z=-self.angular
            self.get_logger().info('Publishing: Derecha')
        else:
            self.get_logger().info(f'Invalid input')
            return

        self.publisher_.publish(msg)

    def on_release(self, key):
        if not(hasattr(key, 'char')) or key.char not in ['w', 's', 'a', 'd']:
            self.get_logger().info(f'Invalid input')
            return
        msg = Twist()
        msg.linear.x=0.0
        msg.angular.z=0.0
        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: Stop')
        self.prevchar = ''


def main(args=None):
    rclpy.init(args=args)
    
    teleop = TurtleBotTeleop()

    rclpy.spin(teleop)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    teleop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()