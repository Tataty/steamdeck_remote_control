import socket
import time
import random

def generate_data():
    # Генерируем случайные значения от -1 до 1
    data1 = random.uniform(-1, 1)
    data2 = random.uniform(-1, 1)
    return data1, data2

def send_data():
    host = '127.0.0.1'  # IP-адрес сервера (в данном случае, localhost)
    port = 12345         # Произвольный порт

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((host, port))
        while True:
            data = generate_data()
            message = f"{data[0]} {data[1]}"
            s.sendall(message.encode())
            time.sleep(1)

if __name__ == "__main__":
    send_data()