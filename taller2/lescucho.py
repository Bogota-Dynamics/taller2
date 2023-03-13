import rclpy
import serial
import time
from rclpy.node import Node
from geometry_msgs.msg import Twist

class TurtleBotInterface(Node):

    def __init__(self):

        #Inicializar el subscriber
        super().__init__('controlar')
        self.subscription = self.create_subscription(
            Twist,
            'turtlebot_cmdVel',
            self.listener_callback,
            20)
    

        self.arduino = serial.Serial(port='/dev/ttyACM0', baudrate=250000,timeout=.1)
    

    def listener_callback(self, msg):

        x = msg.linear.x
        y = msg.linear.y

        mensaje = f'{x},{y}'

        self.write_read(mensaje)

        
    def write_read(self, x):

        self.arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = self.arduino.readline()
        self.get_logger().info(data)


def main(args=None):
    rclpy.init(args=args)

    interface = TurtleBotInterface()

    rclpy.spin(interface)

    interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()