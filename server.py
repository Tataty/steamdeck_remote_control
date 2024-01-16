import socket
import json
import tkinter as tk
import threading
import random
import math
import time

# Задайте адрес и порт сервера
server_address = ('0.0.0.0', 12345)

# Создайте сокет для обмена данными по UDP
server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(server_address)

# Создание основного окна
root = tk.Tk()
root.title("Falling Squares")

# Инициализация Canvas для отрисовки
canvas = tk.Canvas(root, width=600, height=600, bg="white")
canvas.pack()

# Создание квадрата игрока
player_square = canvas.create_rectangle(320, 320, 335, 335, fill="red")
            
# Список для хранения квадратов, которые будут падать
falling_squares = []

def clear_all_squares():
    global falling_squares

    for square in falling_squares:
        canvas.delete(square)

    falling_squares = []
    
def check_collision():
    global falling_squares, player_square

    player_coords = canvas.coords(player_square)

    for square in falling_squares:
        square_coords = canvas.coords(square)

        # Проверка столкновения по bounding boxes
        if (player_coords[0] < square_coords[2] and
                player_coords[2] > square_coords[0] and
                player_coords[1] < square_coords[3] and
                player_coords[3] > square_coords[1]):
                
            return True
    return False

mx, my = 0, 0

def receive_data():
    global mx, my
    while True:
        # Получение данных
        data, client_address = server_socket.recvfrom(1024)
        received_data = json.loads(data.decode('utf-8'))

        # Отрисовка квадрата на указанных координатах
        mx = received_data['x']
        my = received_data['y']
        
        if math.sqrt(mx*mx + my*my) < 0.8:
            mx, my = 0, 0


def add_falling_square():
    global falling_squares, canvas
    x = random.uniform(0, 1) * 570
    square = canvas.create_rectangle(x, 0, x + 30, 30, fill="blue")
    falling_squares.append(square)

delta_time = 0

def move_falling_squares():
    global falling_squares
    for square in falling_squares:
        canvas.move(square, 0, 100 * delta_time)
        x1, y1, x2, y2 = canvas.coords(square)
        if y2 > 600:
            canvas.delete(square)
            falling_squares.remove(square)


# Создаем Entry для ввода текста
entry = tk.Entry(root)
entry.pack()

def display_text(score):
    # Очищаем холст от предыдущего текста
    canvas.delete("text_tag")
    
    # Получаем текст из Entry
    text = entry.get()
    
    # Выводим текст на холсте
    canvas.create_text(15, 15, text=str(score), font=("Helvetica", 12), tags="text_tag")

# Создание отдельного потока для приема данных
receive_thread = threading.Thread(target=receive_data)
receive_thread.start()

add_falling_square()

# Переменные для измерения времени
last_time = time.time()
# Основной цикл программы
last_time_summon = 0
time_game = 1

while True:
    current_time = time.time()
    delta_time = current_time - last_time
    last_time = current_time
    
    time_game += delta_time
    display_text(int(time_game))
    
    last_time_summon += delta_time
    if last_time_summon > 0.4 / math.sqrt(time_game):
        last_time_summon = 0
        if random.uniform(0, 1) > 0.5:
            add_falling_square()
    
    move_falling_squares()
    if check_collision():
        time_game = 1
    
        clear_all_squares()
        
    
        canvas.coords(player_square, 320, 320, 335, 335)

    player_coords = canvas.coords(player_square)
        
    if player_coords[0] + mx * delta_time * 100 < 0 or player_coords[2] + mx * delta_time * 100 > 600:
        mx = 0
        
    if player_coords[1] + my * delta_time * 100 < 0 or player_coords[3] + my * delta_time * 100 > 600:
        my = 0
        
    canvas.move(player_square, mx * delta_time * 100, my * delta_time * 100)
    
    root.update()
