import socket
import time
import random
import signal
from xbox360controller import Xbox360Controller
import json
import threading

class ClientController:

    server_address = ('192.168.0.102', 12345)
    
    def on_button_pressed(self, button):
        print('Button {0} was pressed'.format(button.name))

    def on_button_released(self, button):
        print('Button {0} was released'.format(button.name))

    def SendToServer(self):
        while True:
            message = json.dumps(self.last_axis_data).encode('utf-8')
            print('send moved: {} {}'.format(last_axis_data.x, last_axis_data.y))
            self.client_socket.sendto(message, self.server_address)
            time.sleep(0.1)
    
    def on_axis_moved(self, axis):
        
        self.last_axis_data = {'x': axis.x, 'y': axis.y}
    
    def __init__(self):
        self.last_axis_data = {'x': 0, 'y': 0}
        
        self.send_thread = threading.Thread(target=self.SendToServer)
        self.send_thread.start()
    
        try:
            self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
            with Xbox360Controller(0, axis_threshold=0.2) as controller:
                # Button A events
                controller.button_a.when_pressed = self.on_button_pressed
                controller.button_a.when_released = self.on_button_released

                # Left and right axis move event
                controller.axis_l.when_moved = self.on_axis_moved
                controller.axis_r.when_moved = self.on_axis_moved

                signal.pause()
                
        except KeyboardInterrupt:
            pass
            
cc = ClientController()