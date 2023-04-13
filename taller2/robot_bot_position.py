import rclpy
import serial
from rclpy.node import Node

from std_msgs.msg import String


class PositionPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'robot_cmPos', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.arduino = serial.Serial(port='/dev/ttyACM1', baudrate=250000,timeout=.1)

    def timer_callback(self):      
        if self.arduino.in_waiting>0:
            line = self.serial_port.readline().decode().rstrip()
            msg = String()
            msg.data = line
            self.publisher_.publish(msg)
            self.get_logger().info('Publishing: "%s"' % msg.data)  
        
def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = PositionPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()


