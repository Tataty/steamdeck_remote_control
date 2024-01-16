import socket
import json
import turtle
import threading
import random
import math
# Задайте адрес и порт сервера
server_address = ('192.168.0.102', 12345)

# Создайте сокет для обмена данными по UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

# Инициализация черепахи для отрисовки
screen = turtle.Screen()
screen.setup(width=600, height=600)
player_square = turtle.Turtle()
player_square.shape("square")
player_square.color("red")

# Установка максимальной скорости для черепахи игрока
player_square.speed("fastest")

# Список для хранения квадратов, которые будут падать
falling_squares = []

x, y = 0, 0
mx, my = 0, 0

def receive_data():
    global falling_squares, mx, my
        
    try:
        while True:
            # Получение данных
            data, client_address = server_socket.recvfrom(1024)
            received_data = json.loads(data.decode('utf-8'))
            mx, my = received_data['x'], -received_data['y']
            if math.sqrt(mx*mx + my*my) < 0.8:
                mx, my = 0, 0
            # Отрисовка квадрата на указанных координатах
    except KeyboardInterrupt:
        pass


def add_falling_square():
    global falling_squares
    square = turtle.Turtle()
    square.shape("square")
    square.color("blue")
    square.penup()
    square.speed(0)
    square.goto(random.uniform(-1, 1) * 300, 290)
    falling_squares.append(square)


def move_falling_squares():
    global falling_squares
    for square in falling_squares:
        y = square.ycor()
        y -= 10
        square.sety(y)
        if y < -300:
            square.hideturtle()
            falling_squares.remove(square)


# Создание отдельных потоков
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

# Добавление падающих квадратов в основном потоке
screen.listen()
screen.onkey(add_falling_square, "a")

try:
    # Основной цикл программы
    while True:
        x += mx * 5
        y += my * 5
        #if random.uniform(-1, 0.2) > 0:
        #    add_falling_square()
        player_square.goto(x, y)
        move_falling_squares()
        screen.update()
except KeyboardInterrupt:
    pass