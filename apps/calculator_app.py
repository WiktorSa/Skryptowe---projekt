import tkinter as tk
from tkinter import messagebox, filedialog
import abc
import configparser
from apps.app import App
from calculator import SimpleCalculator, AdvancedCalculator

CONFIG_FILE: str = "configuration.txt"


class CalculatorApp(tk.Frame):
    """
    Class designed to hold all the functionalities of both calculator frames
    This class also holds all the abstract methods of inheriting apps
    """

    def __init__(self, parent: App):
        super().__init__(parent)
        self.parent = parent
        self.parent.protocol("WM_DELETE_WINDOW", self.quit)

        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE, 'utf-8')
        self.parent.geometry(self.config["DEFAULT"].get("BASE_GEOMETRY", "628x271+443+233"))
        # self.parent.resizable(False, False)

    # In contrast to typical calculator we will save user preferences about location
    # We will also ask him for confirmation about ending the program
    def quit(self, event=None):
        reply = messagebox.askyesno("End of work", "Finish?")
        if reply:
            self.config["DEFAULT"]["BASE_GEOMETRY"] = self.parent.winfo_geometry()
            with open(CONFIG_FILE, 'w') as f:
                self.config.write(f)
            self.parent.destroy()

    @abc.abstractmethod
    def create_menu(self):
        pass

    @abc.abstractmethod
    def create_number_line(self):
        pass

    @abc.abstractmethod
    def create_workspace(self):
        pass


class SimpleCalculatorApp(CalculatorApp):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.parent.iconbitmap('images/calculator.ico')
        self.parent.title("Simple calculator")
        self.calculator = SimpleCalculator()
        self.create_menu()

        self.number_input = None
        self.number_line = None
        self.create_number_line()
        self.create_workspace()

    def create_menu(self):
        """
        The goal of the menu is to allow to easily quit the calculator and to quickly swap calculators
        """

        # Display currently used calculator
        if isinstance(self.calculator, AdvancedCalculator):
            calculator_options = (
                ("Simple calculator", lambda: self.parent.switch_frame(SimpleCalculatorApp)),
                ("Advanced calculator (present)", lambda: self.parent.switch_frame(AdvancedCalculatorApp)),
            )
        else:
            calculator_options = (
                ("Simple calculator (present)", lambda: self.parent.switch_frame(SimpleCalculatorApp)),
                ("Advanced calculator", lambda: self.parent.switch_frame(AdvancedCalculatorApp)),
            )

        options_quit = (
            ("Quit", self.quit, "Ctrl+Q", "<Control-q>"),
        )

        menubar = tk.Menu(self.parent)
        file_menu = tk.Menu(menubar, tearoff=0)
        for label, command in calculator_options:
            file_menu.add_command(label=label, underline=0, command=command)

        quit_menu = tk.Menu(menubar, tearoff=0)
        for label, command, shortcut_text, shortcut in options_quit:
            quit_menu.add_command(label=label, underline=0, command=command, accelerator=shortcut_text)
            self.parent.bind(shortcut, command)

        menubar.add_cascade(label="Calculator", menu=file_menu)
        menubar.add_cascade(label="Quit", menu=quit_menu)
        self.parent.config(menu=menubar)

    def create_number_line(self):
        """
        Number line shows the user the number that he has inputed
        """

        self.number_input = tk.StringVar(self.parent, value='0')
        self.number_line = tk.Label(text=self.number_input.get(), relief=tk.RIDGE, height=4, anchor='e', padx=10)
        self.number_line.pack(fill='x')

    def create_workspace(self):
        memory_butttons = tk.Frame(self, width=100, height=50)
        tk.Button(memory_butttons, text='MC', width=9, height=1).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='C', width=10, height=1).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='MR', width=10, height=1).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='M+', width=10, height=1).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='M-', width=9, height=1).pack(side=tk.LEFT)
        memory_butttons.pack()

        buttons_lane1 = tk.Frame(self)
        tk.Button(buttons_lane1, text='1/x', width=12, height=3).pack(side=tk.LEFT)
        tk.Button(buttons_lane1, text='x^2', width=12, height=3).pack(side=tk.LEFT)
        tk.Button(buttons_lane1, text='sqrt(x)', width=12, height=3).pack(side=tk.LEFT)
        tk.Button(buttons_lane1, text=':', width=12, height=3).pack(side=tk.LEFT)
        buttons_lane1.pack()

        buttons_lane2 = tk.Frame(self)
        tk.Button(buttons_lane2, text='7', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='8', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='9', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='x', width=12, height=3).pack(side=tk.LEFT)
        buttons_lane2.pack()

        buttons_lane3 = tk.Frame(self)
        tk.Button(buttons_lane3, text='4', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='5', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='6', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='-', width=12, height=3).pack(side=tk.LEFT)
        buttons_lane3.pack()

        buttons_lane4 = tk.Frame(self)
        tk.Button(buttons_lane4, text='1', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='2', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='3', width=12, height=3, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='+', width=12, height=3).pack(side=tk.LEFT)
        buttons_lane4.pack()


class AdvancedCalculatorApp(SimpleCalculatorApp):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.parent.title("Advanced calculator")
        self.calculator = AdvancedCalculator()
