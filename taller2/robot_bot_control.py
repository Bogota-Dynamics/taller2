import rclpy
import serial
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist

class robot_bot_control(Node):

    def __init__(self):
        super().__init__('robot_bot_control')
        self.subscription = self.create_subscription(
            Twist,
            'robot_cmdVel',
            self.listener_callback,
            10)
    

        self.arduino = serial.Serial(port='/dev/ttyACM1', baudrate=250000,timeout=.1)
    

    def listener_callback(self, msg):

        x = msg.linear.x
        y = msg.angular.y

        mensaje = f'{x},{y}'

        self.write_read(mensaje)

        
    def write_read(self, x):
        print(f'writing {x}')
        self.arduino.write(bytes(x, 'utf-8'))


def main(args=None):
    rclpy.init(args=args)
    interface = robot_bot_control()
    rclpy.spin(interface)
    interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
