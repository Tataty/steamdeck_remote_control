import cv2

# Замените 'your_camera_ip' и 'your_camera_port' на фактический IP-адрес и порт вашей камеры
camera_ip = '192.168.1.108'
camera_port = '554'
username = "admin"
password = "ksu2023ksu"

# Формируем URL-адрес для получения видеопотока с камеры
url = f'rtsp://{camera_ip}:{camera_port}/H264'

# Создаем объект VideoCapture с URL-адресом камеры
cap = cv2.VideoCapture(url)

# Проверяем, успешно ли открылся видеопоток
if not cap.isOpened():
    print("Ошибка открытия видеопотока")
    exit()

# Чтение и отображение видеопотока
while True:
    ret, frame = cap.read()

    if not ret:
        print("Ошибка чтения кадра")
        break

    # Ваш код обработки кадра, если это необходимо
    # Добавляем текст "LaschenkovRO" в центр изображения
    font = cv2.FONT_HERSHEY_SIMPLEX
    text = "LaschenkovRO"
    text_size = cv2.getTextSize(text, font, 1, 2)[0]
    text_x = (frame.shape[1] - text_size[0]) // 2 - 200
    text_y = (frame.shape[0] + text_size[1]) // 2 - 100
    cv2.putText(frame, text, (text_x, text_y), font, 1, (255, 255, 255), 2, cv2.LINE_AA)

    # Отображение кадра
    cv2.imshow('IP Camera', frame)

    # Выход из цикла при нажатии клавиши 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Освобождаем ресурсы
cap.release()
cv2.destroyAllWindows()
