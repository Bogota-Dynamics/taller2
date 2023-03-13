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
            10)
    
    

    def listener_callback(self, msg):

        global arduino

        x = msg.linear.x
        y = msg.linear.y

        mensaje = 'x,y'

        self.write(mensaje)

    
    def write_read(self, x):
        arduino.write(bytes(x, 'utf-8'))
        time.sleep(0.05)
        data = arduino.readline()
        self.get_logger().info(data)





def main(args=None):
    rclpy.init(args=args)

    arduino = serial.Serial(port='COM', baudrate=9600,timeout=.1)
    interface = TurtleBotInterface()

    rclpy.spin(interface)

    interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()