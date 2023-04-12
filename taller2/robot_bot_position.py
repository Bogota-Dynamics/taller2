import RPi.GPIO as GPIO
import rclpy
import time
from rclpy.node import Node

from std_msgs.msg import String


class PositionPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'robot_cmPos', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        #ENCODER
        self.pin_enc1_a = 18
        self.pin_enc1_b = 23
        GPIO.setup(self.pin_enc1_a, GPIO.IN)
        GPIO.setup(self.pin_enc1_b, GPIO.IN)

        self.count_enc1 = 0
        self.current_time = 0
        self.previous_time = 0
        self.resolucion = 640
        self.direccion = True

        GPIO.add_event_detect(self.pin_enc1_a, GPIO.RISING, callback=self.encoder1_callback)


    def timer_callback(self):        

        vel = self.getVelocidad()

        msg = "Encoder 1 count: {}".format(self.vel)

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1


    def getVelocidad(self):

        self.current_time = time.time()

        if (self.current_time - self.previous_time > 1000):
            self.previous_time = self.current_time
            rpm = self.count_enc1*60/self.resolucion
            self.count_enc1 = 0
        return rpm


    def encoder1_callback(self, pin):
    
        val = GPIO.input(self.pin_enc1_b)

        if (val == GPIO.LOW):
            self.direccion = False
            self.count_enc1 += 1
        else:
            self.direccion = True
            self.count_enc1 -= 1

        

def main(args=None):
    rclpy.init(args=args)
    GPIO.setmode(GPIO.BCM)
    minimal_publisher = PositionPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()


