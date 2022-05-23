import tkinter as tk
from apps import App, SimpleCalculatorApp

if __name__ == '__main__':
    root = App()
    root.switch_frame(SimpleCalculatorApp)
    root.mainloop()
