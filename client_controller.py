import socket
import time
import random
import signal
from xbox360controller import Xbox360Controller

def on_button_pressed(button):
    print('Button {0} was pressed'.format(button.name))

def on_button_released(button):
    print('Button {0} was released'.format(button.name))

def on_axis_moved(axis):
    print('Axis {0} moved to {1} {2}'.format(axis.name, axis.x, axis.y))
    
    message = f"{axis.x} {axis.y}"
    s.sendall(message.encode())
    
class ClientController:

    host = '192.168.1.108'  # IP-адрес сервера (в данном случае, localhost)
    port = 12345         # Произвольный порт
    
    def __init__(self):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.connect((host, port))
                with Xbox360Controller(0, axis_threshold=0.2) as controller:
                    # Button A events
                    controller.button_a.when_pressed = on_button_pressed
                    controller.button_a.when_released = on_button_released

                    # Left and right axis move event
                    controller.axis_l.when_moved = on_axis_moved
                    controller.axis_r.when_moved = on_axis_moved

                    signal.pause()
        except KeyboardInterrupt:
            pass
            
cc = ClientController()