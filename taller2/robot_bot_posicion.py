import rclpy
import serial
from rclpy.node import Node
from math import pi, cos, sin, atan2

from std_msgs.msg import Twist


class PositionPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, 'robot_cmPos', 10)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.x = 0
        self.y = 0
        self.theta = 0

        self.arduino = serial.Serial(port='/dev/ttyACM1', baudrate=250000,timeout=.1)

    def timer_callback(self):      
        if self.arduino.in_waiting>0:
            line = self.arduino.readline().decode('utf-8')
            self.get_logger().info(line)  
            line = line.split(",")

            self.odometria(line[0], line[1])

            #Publlicar las posiciones
            msg = Twist()
            msg.linear.x = float(self.x)
            msg.linear.y = float(self.y)
            self.publisher_.publish(msg)

    def odometria(self, w1, w2):
        # ODOMETRIA
        v1 = w1 * self.r1_radio
        v2 = w2 * self.r2_radio

        v = (v1 + v2)/2 # Velocidad lineal (m/s)
        w = (v2 - v1)/self.distancia_ruedas # Velocidad angular (rad/s)

        dt = self.update_freq # Tiempo de actualizacion (s)
        self.x += v * cos(self.theta) * dt # Distancia recorrida en x (en m)
        self.y += v * sin(self.theta) * dt # Distancia recorrida en y (en m)
        self.theta += w * dt # Angulo recorrido (en rad)
        self.theta = atan2(sin(self.theta), cos(self.theta)) # Normalización del angulo


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = PositionPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()