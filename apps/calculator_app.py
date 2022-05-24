import tkinter as tk
from tkinter import messagebox, filedialog
import abc
import configparser
from apps.app import App
from calculator import SimpleCalculator, AdvancedCalculator

# Configuration file where app start location is stored
CONFIG_FILE: str = "configuration.txt"
# Default width and size of the app
APP_WIDTH: int = 400
APP_HEIGHT: int = 415
# Maximal number of digits that can be displayed at the same time
MAX_NO_DIGITS = 12


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
        x_location = int(self.config['DEFAULT'].get("x_location", '531'))
        y_location = int(self.config['DEFAULT'].get("y_location", '227'))
        self.parent.geometry('%dx%d+%d+%d' % (APP_WIDTH, APP_HEIGHT, x_location, y_location))
        self.parent.resizable(False, False)

    # In contrast to typical calculator we will save user preferences about location
    # We will also ask him for confirmation about ending the program
    def quit(self, event=None):
        reply = messagebox.askyesno("End of work", "Finish?")
        if reply:
            self.config["DEFAULT"]["X_LOCATION"] = str(self.parent.winfo_x())
            self.config["DEFAULT"]["Y_LOCATION"] = str(self.parent.winfo_y())
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

        self.number_line_input = None
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

        # Display quit option
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

        self.number_line_input = tk.StringVar(self.parent, value='0')
        self.number_line = tk.Label(text=self.number_line_input.get(), relief=tk.RIDGE, height=2, anchor='e', padx=10,
                                    font='Helvetica 36 bold')
        self.number_line.pack(fill='x')

    def create_workspace(self):
        """
        Create workspace - the place for all the buttons
        To create the design we will pack frames with 4 buttons in one row
        Note - in some cases we are using unicode to display calculator options
        """

        # Each calculator frame will be assigned to the main workspace frame
        workspace = tk.Frame(self)

        # We need 5 buttons here thus they will have different size from the rest of the buttons
        # These are memory buttons thus they should be smaller than the rest of the buttons
        memory_butttons = tk.Frame(workspace)
        tk.Button(memory_butttons, text='MC', width=10, height=1, command=lambda:
            self.calculator.clear_memory()).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='C', width=10, height=1, command=lambda:
            self.set_number('0')).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='MR', width=10, height=1).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='M+', width=10, height=1, command=lambda:
            self.calculator.add_memory(float(self.number_line_input.get()))).pack(side=tk.LEFT)
        tk.Button(memory_butttons, text='M-', width=10, height=1, command=lambda:
            self.calculator.substract_memory(float(self.number_line_input.get()))).pack(side=tk.LEFT)
        memory_butttons.pack()

        # For better visibility all key aspects of the calculator will be bold
        buttons_lane1 = tk.Frame(workspace)
        tk.Button(buttons_lane1, text='1/x', width=10, height=2, font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane1, text='x\u00b2', width=10, height=2, font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane1, text='\u221Ax', width=10, height=2, font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane1, text='\u00F7', width=10, height=2, font='bold').pack(side=tk.LEFT)
        buttons_lane1.pack()

        buttons_lane2 = tk.Frame(workspace)
        # Number related buttons have white background for better visibility
        tk.Button(buttons_lane2, text='7', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('7')).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='8', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('8')).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='9', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('9')).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='x', width=10, height=2, font='bold').pack(side=tk.LEFT)
        buttons_lane2.pack()

        buttons_lane3 = tk.Frame(workspace)
        tk.Button(buttons_lane3, text='4', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('4')).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='5', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('5')).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='6', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('6')).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='-', width=10, height=2, font='bold').pack(side=tk.LEFT)
        buttons_lane3.pack()

        buttons_lane4 = tk.Frame(workspace)
        tk.Button(buttons_lane4, text='1', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('1')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='2', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('2')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='3', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('3')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='+', width=10, height=2, font='bold').pack(side=tk.LEFT)
        buttons_lane4.pack()

        buttons_lane4 = tk.Frame(workspace)
        tk.Button(buttons_lane4, text='+/-', width=10, height=2, background='white', font='bold').pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='0', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_number('0')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text=',', width=10, height=2, background='white', font='bold', command=lambda:
            self.append_decimal()).pack(side=tk.LEFT)
        #  = button will have different background to be more recognizable
        tk.Button(buttons_lane4, text='=', width=10, height=2, background='light blue', font='bold').pack(side=tk.LEFT)
        buttons_lane4.pack()

        workspace.pack()

    def append_number(self, digit: str):
        """
        Append the inputted digit to the current number
        """

        current_number = self.number_line_input.get()
        if current_number == '0':
            new_number = digit
        else:
            new_number = current_number + digit
        self.number_line_input.set(new_number)
        self.number_line.config(text=new_number)

    def append_decimal(self, point: str = '.'):
        """
        Append decimal point to the current number
        """
        current_number = self.number_line_input.get()
        if point not in current_number:
            new_number = current_number + point
            self.number_line_input.set(new_number)
            self.number_line.config(text=new_number)

    def set_number(self, number: str):
        """
        Set the currently displayed number to the given number
        """

        self.number_line_input.set(number)
        self.number_line.config(text=number)
        print(self.number_line.cget('text'))


class AdvancedCalculatorApp(SimpleCalculatorApp):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.parent.title("Advanced calculator")
        self.calculator = AdvancedCalculator()
