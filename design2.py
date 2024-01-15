import PySimpleGUI as sg
import cv2
import numpy as np

def main():
    layout = [[sg.Image(filename="", key="-IMAGE-")],
              [sg.Exit()]]

    window = sg.Window("IP Video Player", layout, resizable=True)

    cap = cv2.VideoCapture("http://192.168.1.108:5000/video_feed")  # Замените на ваш IP и порт

    while True:
        event, values = window.read(timeout=20)

        if event == sg.WINDOW_CLOSED or event == "Exit":
            break

        ret, frame = cap.read()
        if not ret:
            sg.popup_error("Failed to receive video stream. Make sure the URL is correct.")
            break

        frame = cv2.resize(frame, (1280, 720))  # Измените размер кадра по вашему усмотрению
        imgbytes = cv2.imencode(".png", frame)[1].tobytes()

        window["-IMAGE-"].update(data=imgbytes)

    cap.release()
    window.close()

if __name__ == "__main__":
    main()
