from tkinter import *
import time


global pause


class TwoBodyView(Frame):
    def __init__(self, root_tk, **kw):
        super().__init__(**kw)
        self.root = root_tk
        self.root.title("Two-Body Animation")
        self.H = 500
        self.W = 500
        self.body_one_positions = list()
        self.body_two_positions = list()
        self.canvas = None

    def create_canvas(self):
        self.canvas = Canvas(self.root, width=self.W, height=self.H)

    def read_vector(self):
        f = open("vectors.txt")
        positions = f.readlines()
        for position in positions:
            position = list(map(float, position.split(",")))
            self.body_one_positions.append((position[0], position[1]))
            self.body_two_positions.append((position[2], position[3]))
        f.close()

    def restart_animation(self):
        self.canvas.delete("all")
        self.draw()

    def pause_animation(self):
        global pause
        pause = True

    def quit(self):
        root.destroy()

    def draw(self):
        global pause
        pause = False
        restart_button = Button(self.canvas, text="restart", font='Helvetica 10 bold', width=10, height=1,
                                        command=self.restart_animation)
        exit_button = Button(self.canvas, text="exit", font='Helvetica 10 bold', width=10, height=1,
                                        command=self.quit)
        self.canvas.create_window(50, 20, window=restart_button)
        self.canvas.create_window(150, 20, window=exit_button)

        self.canvas.pack()

        body_one = self.canvas.create_oval(185, 185, 200, 200, fill="red")
        body_two = self.canvas.create_oval(285, 285, 300, 300, fill="blue")

        for i in range(1, len(self.body_one_positions)):

            while pause:
                continue

            self.canvas.move(body_one, (self.body_one_positions[i][0] - self.body_one_positions[i - 1][0]) * 50,
                             (self.body_one_positions[i][1] - self.body_one_positions[i - 1][1]) * 50)

            self.canvas.move(body_two, (self.body_two_positions[i][0] - self.body_two_positions[i - 1][0]) * 50,
                             (self.body_two_positions[i][1] - self.body_two_positions[i - 1][1]) * 50)
            self.canvas.create_line(self.canvas.coords(body_one), fill="red")
            self.canvas.create_line(self.canvas.coords(body_two), fill="blue")
            self.root.update()
            time.sleep(0.000001)


if __name__ == '__main__':
    root = Tk()
    view = TwoBodyView(root)
    view.create_canvas()
    view.read_vector()
    view.draw()






