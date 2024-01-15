import pygame
import socket

def draw_rectangle(screen, x, y):
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(x, y, 50, 50))

def receive_data():
    host = '0.0.0.0'  # IP-адрес сервера (в данном случае, localhost)
    port = 12345         # Произвольный порт

    pygame.init()
    screen = pygame.display.set_mode((800, 600))
    pygame.display.set_caption('Moving Rectangle')

    x, y = 375, 275  # Начальные координаты прямоугольника

    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((host, port))
        s.listen()
        conn, addr = s.accept()

        with conn:
            print('Connected by', addr)
            while True:
                data = conn.recv(1024).decode()
                if not data:
                    break

                # Разбираем данные
                data_split = data.split()
                if len(data_split) == 2:
                    x_offset, y_offset = float(data_split[0]), float(data_split[1])
                    x += int(x_offset * 50)  # Масштабируем изменение
                    y += int(y_offset * 50)

                screen.fill((255, 255, 255))  # Очищаем экран
                draw_rectangle(screen, x, y)
                pygame.display.flip()

if __name__ == "__main__":
    receive_data()
