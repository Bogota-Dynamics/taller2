import rclpy
import pynput

from pynput import keyboard
import time
from rclpy.node import Node
from my_msgs.srv import SaveMotions
from os.path import abspath

from geometry_msgs.msg import Twist


class TurtleBotPlayer(Node):

    def __init__(self):
        super().__init__('turtle_bot_player')

        self.publisher_ = self.create_publisher(Twist, 'robot_cmdVel', 10)
        # crear un servicio que recree los movimientos guardados en un archivo txt
        self.service = self.create_service(SaveMotions, 'recreate_motion', self.recreate_motion_callback)

    def recreate_motion_callback(self, request, response):

        # leer el archivo y publicar los movimientos
        filename = 'src/taller2/motion/' + request.filename + '.txt'
        response.path = abspath(filename)
        self.get_logger().info('Reading from file: ' + response.path)
        msg = Twist()
        msg.linear.x=0.0
        msg.angular.z=0.0
        self.publisher_.publish(msg)   

        msg_viejo = 0   

        with open(response.path, 'r') as f:
            # 1. La primera linea es la velocidad lineal y angular
            vels = f.readline().split(',')
            linear = float(vels[0])
            angular = float(vels[1])
            # 2. Las siguientes lineas son los movimientos
            #    TriggerR: adelante
            #    TriggerL: atras
            #    Izquierda: izquierda
            #    Derecha: derecha
            #    QUIETO: pausa, separada por '=' del tiempo de pausa
            for line in f:
                start = time.time()
                line = line.strip()
                print(line)
                msg = Twist()
                if line == 'TriggerR':
                    msg.linear.x = linear
                    self.get_logger().info('Publishing: Adelante')
                elif line == 'TriggerL':
                    msg.linear.x = -linear
                    self.get_logger().info('Publishing: Atras')
                elif line == 'Izquierda':
                    msg.angular.z = angular
                    self.get_logger().info('Publishing: Izquierda')
                elif line == 'Derecha':
                    msg.angular.y = -angular
                    self.get_logger().info('Publishing: Derecha')
                elif line == 'QUIETO':
                    msg.linear.x=0.0
                    msg.angular.z=0.0

                # Los mensajes se publican cada 0.04 segundos aproximadamente
                while (time.time() - start) < 0.04: pass
                if (msg_viejo != msg):
                    print("AAAAAAAAAAAAAAA")
                    self.publisher_.publish(msg)
                    msg_viejo = msg

        msg = Twist()
        msg.linear.x=0.0
        msg.angular.z=0.0
        self.publisher_.publish(msg)        
        self.get_logger().info('Done')
        # retornar el path global del archivo
        return response


def main(args=None):
    rclpy.init(args=args)
    
    player = TurtleBotPlayer()

    rclpy.spin(player)

    player.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()