import rclpy
import pygame
import tkinter as tk
from threading import Thread

from tkinter import filedialog
from rclpy.node import Node
from geometry_msgs.msg import Twist
from my_msgs.srv import SaveMotions

class TurtleBotInterface(Node):

    def __init__(self):

        #Inicializar el subscriber
        super().__init__('turtle_bot_interface')
        self.subscription = self.create_subscription(
            Twist,
            'robot_cmPos',
            self.listener_callback,
            10)
        
        self.client = self.create_client(SaveMotions, 'save_motion')
        self.client2 = self.create_client(SaveMotions, 'recreate_motion')

        #Definicion de variables
        self.pos_actual = [275,300]
        self.coords = []
        self.background_color = (255,255,255)

        #Initialize pygame window
        self.screen = pygame.display.set_mode((550,600))
        self.screen.fill(self.background_color)
        
       
        #Display button save draw
        self.button1 = Button('Guardar Imagen', 150,35,(10,560),self.screen)
        self.button1.draw()

        #Display button save motion
        self.button2 = Button('Guardar Recorrido', 180,35,(170,560),self.screen)
        self.button2.draw()

        #Display button recreate motion
        self.button3 = Button('Recrear Recorrido', 180,35,(360,560),self.screen)
        self.button3.draw()

        #Input text
        self.user_text = 'Robot'
        self.input_rect = pygame.Rect((25,10), (500, 30))
        self.input_state = False

        #Rectangulo Area de juego
        self.area_rect = pygame.Rect((25,50), (500, 500))

        

    def listener_callback(self, msg):

        #Para que no se muera pygame 
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                pygame.quit() #Cerrar la ventana

            if event.type == pygame.MOUSEBUTTONDOWN:
                if self.input_rect.collidepoint(event.pos):
                    self.input_state = True   
                else:
                    self.input_state = False

            if event.type == pygame.KEYDOWN and self.input_state:
                if event.key == pygame.K_BACKSPACE:
                    self.user_text = self.user_text[:-1]
                else:
                    if self.text_surface.get_width()<350:
                        self.user_text += event.unicode

        #Area de juego
        pygame.draw.rect(self.screen, '#9b9b9b', self.area_rect, 5) 
        
        #Nombre de la grafica
        if self.input_state:
            pygame.draw.rect(self.screen, '#9b9b9b', self.input_rect) 
        else:
            pygame.draw.rect(self.screen, (255,255,255), self.input_rect) 

        self.text_surface = pygame.font.Font(None, 35).render(self.user_text, True, '#475F77')
        self.screen.blit(self.text_surface, (self.input_rect.x + ((500-self.text_surface.get_width())/2), self.input_rect.y + 2.5))


        #Guardar Imagen del camino
        if not self.button1.check_click():
            self.get_logger().info("Guardar Imagen")
            tkthread = Thread(target=tk_open_dialog_thread, args=(self,))
            tkthread.start()
        
        #Guardar Recorrido
        if not self.button2.check_click():
            self.get_logger().info("Guardar Recorrido")
            mtThread = Thread(target=save_motion_thread, args=(self,))
            mtThread.start()

        #Guardar Recorrido
        if not self.button3.check_click():
            self.get_logger().info("Recrear Recorrido")
            mkmtThread = Thread(target=recreate_motion_thread, args=(self,))
            mkmtThread.start()

        #Dibujar el camino robot
        if self.pos_actual != (msg.linear.x, msg.linear.y):
            nuevas = self.cordenates(msg.linear.x, msg.linear.y)
            pygame.draw.line(self.screen, (60,179,113), self.pos_actual,nuevas,5)
            pygame.display.update()
            self.pos_actual = nuevas
            #self.get_logger().info(f"Coordenadas: [{nuevas[0]}]")
            self.coords.append(nuevas) # guardar las coordenadas en el archivo


    def cordenates(self,linearx,lineary):
        if linearx>0:
            x = 275+linearx*100
        else:
            x = 275+linearx*100
        if lineary>0:
            y = 300-lineary*100
        else:
            y = 300-lineary*100
        return (x,y)

def tk_open_dialog_thread(interface:TurtleBotInterface):
    file_path = filedialog.asksaveasfilename(
        defaultextension=".png",
        filetypes=[
            ("PNG Image", "*.png"), 
            ("All Files", "*.*")
        ])
    pygame.image.save(interface.screen, file_path)

def save_motion_thread(interface:TurtleBotInterface):
    while not interface.client.wait_for_service(timeout_sec=1.0):
        interface.get_logger().info('service not available, waiting again...')

    request = SaveMotions.Request()
    request.filename = interface.user_text
    interface.get_logger().info('Calling service...')
    future = interface.client.call_async(request)
    #rclpy.spin_until_future_complete(interface, future)

    #if future.result() is not None:
    #    interface.get_logger().info(f"Result saved at: {future.result().path}")
    #else:
    #    interface.get_logger().info("Service call failed %r" % (future.exception(),))


def recreate_motion_thread(interface:TurtleBotInterface):
    while not interface.client2.wait_for_service(timeout_sec=1.0):
        interface.get_logger().info('service not available, waiting again...')

    request = SaveMotions.Request()
    request.filename = interface.user_text
    interface.get_logger().info('Calling service...')
    future = interface.client2.call_async(request)
    #rclpy.spin_until_future_complete(interface, future)

    #if future.result() is not None:
    #    interface.get_logger().info(f"Result recreated from: {future.result().path}")
    #else:
    #    interface.get_logger().info("Service call failed %r" % (future.exception(),))

class Button:
    def __init__(self,text,width,height,pos,screen,fontsize=25):
        self.screen = screen
        self.pressed = False
        #Top rectangle
        self.top_rect = pygame.Rect((pos),(width, height))
        self.top_color = '#475F77'

        #Texto Boton
        self.text_surface = pygame.font.Font(None, fontsize).render(text, True, '#FFFFFF')
        self.text_rect = self.text_surface.get_rect(center = self.top_rect.center)

    def draw(self):
        pygame.draw.rect(self.screen, self.top_color, self.top_rect, border_radius=5)
        self.screen.blit(self.text_surface, self.text_rect)

    def check_click(self):
        mouse_pos = pygame.mouse.get_pos()
        if self.top_rect.collidepoint(mouse_pos):
            if pygame.mouse.get_pressed()[0]:
                self.pressed = True
                return True
            else:
                if self.pressed == True:
                    self.pressed = False
                    return False
        return True


def main(args=None):
    rclpy.init(args=args)
    pygame.init()
    interface = TurtleBotInterface()

    rclpy.spin(interface)

    interface.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()