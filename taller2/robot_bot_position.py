import RPi.GPIO as GPIO
import rclpy
import time
from rclpy.node import Node
from math import pi, cos, sin, atan2
from std_msgs.msg import String


class PositionPublisher(Node):

    def __init__(self):
        super().__init__('minimal_publisher')
        self.publisher_ = self.create_publisher(String, 'robot_cmPos', 10)
        timer_period = 0.5  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.i = 0

        self.update_freq = timer_period # s

        #RUEDAS # TODO: Cambiar a los valores reales
        self.r1_radio = 0.05 # m
        self.r1_resolucion = 640 # ticks/rev

        self.r2_radio = 0.05 # m
        self.r2_resolucion = 640 # ticks/rev

        self.distancia_ruedas = 10 # m


        #ENCODER
        self.pin_enc1_a = 18
        self.pin_enc1_b = 23

        self.pin_enc2_a = ... # TODO
        self.pin_enc2_b = ... # TODO

        GPIO.setup(self.pin_enc1_a, GPIO.IN)
        GPIO.setup(self.pin_enc1_b, GPIO.IN)
        
        #GPIO.setup(self.pin_enc1_a, GPIO.IN)
        #GPIO.setup(self.pin_enc1_b, GPIO.IN)

        self.count_enc1 = 0
        self.count_enc2 = 0
        self.current_time = 0
        self.previous_time = 0
        self.direccion1 = True
        #self.direccion2 = True

        GPIO.add_event_detect(self.pin_enc1_a, GPIO.RISING, callback=self.encoder1_callback)
        #GPIO.add_event_detect(self.pin_enc2_a, GPIO.RISING, callback=self.encoder2_callback)

        self.x = 0
        self.y = 0
        self.theta = 0

    def timer_callback(self):        
        w1, w2 = self.getVelocidad() # Velocidad rueda izq (w1) y rueda derecha (w2)
        
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

        msg = "Encoder 1 count: {}".format(self.vel)

        self.publisher_.publish(msg)
        self.get_logger().info('Publishing: "%s"' % msg.data)
        self.i += 1

    def getVelocidad(self):
        self.current_time = time.time()

        self.previous_time = self.current_time
        rpm1 = self.count_enc1*60/self.r1_resolucion
        rpm2 = self.count_enc2*60/self.r2_resolucion
        self.count_enc1 = 0
        self.count_enc2 = 0
        
        return (rpm1, rpm2)


    def encoder1_callback(self, pin):
        val = GPIO.input(self.pin_enc1_b)

        if (val == GPIO.LOW):
            self.direccion1 = False
            self.count_enc1 += 1
        else:
            self.direccion1 = True
            self.count_enc1 -= 1

    def encoder2_callback(self, pin):
        val = GPIO.input(self.pin_enc2_b)

        if (val == GPIO.LOW):
            self.direccion2 = False
            self.count_enc2 += 1
        else:
            self.direccion2 = True
            self.count_enc2 -= 1
        

def main(args=None):
    rclpy.init(args=args)
    GPIO.setmode(GPIO.BCM)
    minimal_publisher = PositionPublisher()
    rclpy.spin(minimal_publisher)
    minimal_publisher.destroy_node()
    rclpy.shutdown()
    


if __name__ == '__main__':
    main()


