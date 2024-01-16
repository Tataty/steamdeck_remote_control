import socket
import time
import random
import signal
from xbox360controller import Xbox360Controller

class ClientController:

    server_address = ('192.168.0.102', 12345)
    
    def on_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))

    def on_button_released(self, button):
        print('Button {0} was released'.format(button.name))

    def on_axis_moved(self, axis):
        print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
        
        # Отправка данных
        data = {'x': axis.x, 'y': axis.y}  # Пример координат
        message = json.dumps(data).encode('utf-8')
        self.client_socket.sendto(message, self.server_address)
    
    def __init__(self):
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            print("Begin")
            with Xbox360Controller(0, axis_threshold=0.2) as controller:
                # Button A events
                controller.button_a.when_pressed = self.on_button_pressed
                controller.button_a.when_released = self.on_button_released

                # Left and right axis move event
                controller.axis_l.when_moved = self.on_axis_moved
                controller.axis_r.when_moved = self.on_axis_moved

                print("signal Begin")
                signal.pause()
        except KeyboardInterrupt:
            pass
            
cc = ClientController()