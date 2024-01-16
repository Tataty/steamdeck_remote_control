import socket
import json
import turtle

# Задайте адрес и порт сервера
server_address = ('192.168.0.102', 12345)

# Создайте сокет для обмена данными по UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

# Инициализация черепахи для отрисовки
screen = turtle.Screen()
screen.setup(width=600, height=600)
square = turtle.Turtle()
square.shape("square")
square.color("red")

try:
    while True:
        # Получение данных
        data, client_address = server_socket.recvfrom(1024)
        received_data = json.loads(data.decode('utf-8'))

        # Отрисовка квадрата на указанных координатах
        x = received_data['x']
        y = received_data['y']
        square.goto(x * 300, y * 300)
        screen.update()
        print(received_data)
finally:
    # Закрытие сокета
    server_socket.close()
    turtle.done()