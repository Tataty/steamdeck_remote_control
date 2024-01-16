import tkinter as tk
from PIL import Image, ImageTk
import cv2

class VideoApp:
    def __init__(self, master, video_source):
        self.master = master
        self.master.title("IP Camera Viewer")

        self.video_source = video_source
        self.vid = cv2.VideoCapture(self.video_source)

        self.canvas = tk.Canvas(master, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        self.btn_snapshot = tk.Button(master, text="Snapshot", command=self.snapshot)
        self.btn_snapshot.pack(padx=10, pady=10)

        self.update()

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)

    def snapshot(self):
        ret, frame = self.vid.read()
        if ret:
            cv2.imwrite("snapshot.png", cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            print("Snapshot taken!")

    def update(self):
        ret, frame = self.vid.read()
        if ret:
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)

        self.master.after(10, self.update)

    def on_closing(self):
        if self.vid.isOpened():
            self.vid.release()
        self.master.destroy()

def main():
    video_source = "http://192.168.0.102:5000/video_feed"  # Замените это URL-ом вашей IP-камеры

    root = tk.Tk()
    app = VideoApp(root, video_source)
    root.mainloop()

if __name__ == "__main__":
    main()
