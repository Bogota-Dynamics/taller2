import rclpy
import serial
import serial.tools.list_ports
from rclpy.node import Node
from math import pi, cos, sin, atan2

from geometry_msgs.msg import Twist



class PositionPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(Twist, 'robot_cmPos', 10)
        timer_period = 0.2  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)

        self.x = 0
        self.y = 0
        self.theta = pi/2
        self.r1_radio=0.05
        self.r2_radio=0.05
        self.distancia_ruedas=0.15
        self.update_freq = timer_period
        self.vel1 = 0
        self.vel2 = 0

        ports = list(serial.tools.list_ports.comports())
        arduino_port = ports[0].device
        self.arduino = serial.Serial(port=arduino_port, baudrate=250000,timeout=.1)

    def timer_callback(self):      
        if self.arduino.in_waiting>0:
            line = self.arduino.readline().decode('utf-8')
            self.get_logger().info(line)  
            line = line.split(",")
            self.vel1 = float(line[0])
            self.vel2 = float(line[1])

        self.odometria(self.vel1,self.vel2)

        #Publlicar las posiciones
        msg = Twist()
        msg.linear.x = float(self.x)
        msg.linear.y = float(self.y)
        print(msg)
        self.publisher_.publish(msg)

    def odometria(self, w2, w1):

        # ODOMETRIA
        v1 = w1 * self.r1_radio
        v2 = w2 * self.r2_radio

        v = (v1 + v2)/2 # Velocidad lineal (m/s)
        w = (v2 - v1)/self.distancia_ruedas # Velocidad angular (rad/s)

        dt = self.update_freq # Tiempo de actualizacion (s)
        self.y += v * cos(self.theta) * dt # Distancia recorrida en x (en m)
        self.x += v * sin(self.theta) * dt # Distancia recorrida en y (en m)
        self.theta += w * dt # Angulo recorrido (en rad)
        self.theta = atan2(sin(self.theta), cos(self.theta)) # Normalización del angulo
        """
        if w1 != 0 and w2 != 0:
            dt = self.update_freq
            theta1 = w1 * dt
            theta2 = w2 * dt
            d1 = self.r1_radio * theta1
            d2 = self.r2_radio * theta2
            d = (d1 + d2) / 2
            delta_theta = (theta2 - theta1) / d
            self.x = self.x + d * cos(self.theta + delta_theta / 2)
            self.y = self.y + d * sin(self.theta + delta_theta / 2)
            self.theta = self.theta + delta_theta
        """


def main(args=None):
    rclpy.init(args=args)
    minimal_publisher = PositionPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()