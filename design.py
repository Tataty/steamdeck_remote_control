import sys
import cv2
import requests
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QPushButton, QSlider, QVBoxLayout, QWidget


class CameraApp(QWidget):
    def __init__(self, camera_url):
        super(CameraApp, self).__init__()

        self.camera_url = camera_url
        self.image_label = QLabel(self)
        self.start_button = QPushButton('Start', self)
        self.start_button.clicked.connect(self.start_camera)

        self.scale_slider = QSlider(Qt.Horizontal)
        self.scale_slider.setMinimum(1)
        self.scale_slider.setMaximum(3)
        self.scale_slider.setValue(1)
        self.scale_slider.valueChanged.connect(self.update_scale)

        layout = QVBoxLayout(self)
        layout.addWidget(self.image_label)
        layout.addWidget(self.start_button)
        layout.addWidget(self.scale_slider)

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.update_frame)

        self.cap = None
        self.is_camera_running = False
        self.scale_factor = 1

    def start_camera(self):
        if not self.is_camera_running:
            self.cap = cv2.VideoCapture(self.camera_url)
            self.timer.start(30)  # 30 мс между кадрами
            self.start_button.setText('Stop')
            self.is_camera_running = True
        else:
            self.timer.stop()
            self.cap.release()
            self.image_label.clear()
            self.start_button.setText('Start')
            self.is_camera_running = False

    def update_frame(self):
        ret, frame = self.cap.read()
        if ret:
            # Уменьшаем размер изображения
            frame = self.resize_image(frame, self.scale_factor)

            rgb_image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_image.shape
            bytes_per_line = ch * w
            qt_image = QImage(rgb_image.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(qt_image)
            self.image_label.setPixmap(pixmap)

    def update_scale(self):
        self.scale_factor = self.scale_slider.value()

    def resize_image(self, image, scale_factor):
        # Ограничиваем размер изображения по ширине и высоте
        max_width, max_height = 1280, 480
        height, width, _ = image.shape

        # Вычисляем новые размеры с сохранением пропорций
        new_width = min(width, max_width)
        new_height = min(height, max_height)
        if width > max_width:
            new_height = int(max_width / width * height)
        if height > max_height:
            new_width = int(max_height / height * width)

        # Масштабируем изображение
        resized_image = cv2.resize(image, (new_width, new_height))
        return resized_image

camera_ip = '127.0.0.1'
camera_port = '5000'
def main():
    app = QApplication(sys.argv)

    # Замените "http://your_ip_camera_url" на фактический URL вашей IP-камеры
    camera_url = f'http://{camera_ip}:{camera_port}/video_feed'
    window = CameraApp(camera_url)
    window.setGeometry(100, 100, 800, 600)
    window.setWindowTitle('IP Camera Viewer')
    window.show()

    sys.exit(app.exec_())


if __name__ == '__main__':
    main()
