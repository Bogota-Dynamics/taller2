import rclpy
import pygame
from rclpy.node import Node
from geometry_msgs.msg import Twist
from my_msgs.srv import SaveMotions
from os.path import abspath


class robot_bot_teleop(Node):

    def __init__(self):
        super().__init__('robot_bot_teleop')
        self.publisher_ = self.create_publisher(Twist, 'robot_cmdVel', 10)
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.timer = self.create_timer(0.1, self.timer_callback)

        #Encontrar el control para input
        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("No se detectaron dispositivos de joystick.")
            pygame.quit()
            exit()
        else:
            print("Hay" + str(joystick_count))

        #Inicializar variablese para publicar controles
        self.linear = float(input("Ingrese la velocidad lineal: "))
        self.angular = float(input("Ingrese la velocidad angular: "))
        self.msg_viejo = 0

        # crear un servicio que guarde la lista de movimientos en un archivo txt
        self.motion = f'{self.linear},{self.angular}\n' # lista de movimientos
        self.service = self.create_service(SaveMotions, 'save_motion', self.save_motion_callback)

    def save_motion_callback(self, request, response):
        filename = 'src/taller1/motion/' + request.filename + '.txt'
        response.path = abspath(filename)
        self.get_logger().info('Writing to file: ' + response.path)

        with open(response.path, 'w') as f:
            f.write(self.motion)
        return response

    def timer_callback(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
        
        x_axis_left = self.joystick.get_axis(0)
        triggerR = self.joystick.get_axis(4)
        triggerL = self.joystick.get_axis(5)

        minVal = 0.1 # si el valor leído es menor a 0.1, no lo lee

        mov = 'QUIETO'
        if (abs(x_axis_left) > minVal):
            mov = ("Izquierda" if x_axis_left < 0 else "Derecha")
        if (triggerL > -1):
            mov = ("TriggerL")
        if (triggerR > -1):
            mov = ("TriggerR")

        msg = Twist()
        if 'TriggerR' == mov:
            msg.linear.x = self.linear
        elif 'TriggerL' == mov:
            msg.linear.x = -self.linear
        elif 'Izquierda' == mov:
            msg.angular.z = self.angular
        elif 'Derecha' == mov:  
            msg.angular.z = -self.angular
        else:
            msg.linear.x = 0.0

        self.motion += mov + '\n' # w = adelante, s = atras, a = izquierda, d = derecha


        print(msg)
        if (self.msg_viejo!=msg): 
            self.publisher_.publish(msg)

        self.msg_viejo = msg

def main(args=None):
    rclpy.init(args=args)
    pygame.init()
    teleop = robot_bot_teleop()
    rclpy.spin(teleop)
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    teleop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
