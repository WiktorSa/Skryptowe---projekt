import tkinter as tk


class App(tk.Tk):
    """
    Class representing main tk instance. The point of this class is to easily change frames when necessary
    """

    def __init__(self):
        super().__init__()
        self.frame = None

    # Swap frames by creating a new frame and destroying the old frame
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()
