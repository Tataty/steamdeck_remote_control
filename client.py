import socket
import json

# Задайте адрес и порт сервера
server_address = ('192.168.0.102', 12345)

# Создайте сокет для обмена данными по UDP
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

try:
    # Отправка данных
    data = {'x': -0.5, 'y': -0.5}  # Пример координат
    message = json.dumps(data).encode('utf-8')
    client_socket.sendto(message, server_address)
finally:
    # Закрытие сокета
    client_socket.close()
