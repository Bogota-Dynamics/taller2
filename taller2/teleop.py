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
        self.joystick = pygame.joystick.Joystick(0)
        self.joystick.init()
        self.timer = self.create_timer(0.1, self.timer_callback)

        joystick_count = pygame.joystick.get_count()
        if joystick_count == 0:
            print("No se detectaron dispositivos de joystick.")
            pygame.quit()
            exit()
        else:
            print("Hay" + str(joystick_count))

        #listener = keyboard.Listener(on_press=self.on_presss, on_release=self.on_release)
        #listener.start()

        self.linear = float(input("Ingrese la velocidad lineal: "))
        self.angular = float(input("Ingrese la velocidad angular: "))
        self.prevchar = ''

    def timer_callback(self):
        for event in pygame.event.get(): 
            if event.type == pygame.QUIT: 
                pygame.quit()
                quit()
        
        x_axis_left = self.joystick.get_axis(0)
        y_axis_right = self.joystick.get_axis(3)
        triggerR = self.joystick.get_axis(4)
        triggerL = self.joystick.get_axis(5)

        minVal = 0.1 # si el valor leído es menor a 0.1, no lo lee

        mov = []
        if (abs(x_axis_left) > minVal):
            mov.append("Izquierda" if x_axis_left < 0 else "Derecha")
        if (abs(y_axis_right) > minVal):
            mov.append("Abajo" if y_axis_right > 0 else "Arriba")
        if (triggerL > -1):
            mov.append("TriggerL")
        if (triggerR > -1):
            mov.append("TriggerR")

        msg = Twist()
        if 'TriggerR' in mov:
            msg.linear.x = self.linear
        if 'TriggerL' in mov:
            msg.linear.x = -self.linear
        else:
            msg.linear.x = 0

        print(msg)
        self.publisher_.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    
    pygame.init()
    teleop = TurtleBotTeleop()

    rclpy.spin(teleop)

    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    teleop.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()