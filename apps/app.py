import math
import random
import tkinter as tk
from tkinter import messagebox, filedialog
import abc
import configparser
from calculator import SimpleCalculator, AdvancedCalculator, SingleDigitOperations, TwoDigitOperations

# Icon location
ICON_FILE: str = "images/calculator.ico"
# Configuration file where app start location is stored
CONFIG_FILE: str = "configuration.txt"
# Maximal number of digits that can be displayed
MAX_NO_DIGITS = 15

# Various constants used across the code
ZERO = '0'
POINT = '.'
MINUS_SIGN = '-'
ERROR_DISPLAY = 'Error'


class App(tk.Tk):
    """
    Class representing main tk instance. The point of this class is to easily change frames when necessary
    """

    def __init__(self):
        super().__init__()
        self.frame = None
        # self.switch_frame(SimpleCalculatorApp)
        self.switch_frame(SimpleCalculatorApp)

    # Swap frames by creating a new frame and destroying the old frame
    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self.frame is not None:
            if self.frame.number_line is not None:
                self.frame.number_line.destroy()
            self.frame.destroy()
        self.frame = new_frame
        self.frame.pack()


class CalculatorApp(tk.Frame):
    """
    Class designed to hold all the functionalities of both calculator frames
    This class also holds all the abstract methods of inheriting apps
    """

    def __init__(self, parent: App):
        super().__init__(parent)
        self.parent = parent
        self.parent.iconbitmap(ICON_FILE)
        self.parent.protocol("WM_DELETE_WINDOW", self.quit)

        # Configure location of the screen
        self.config = configparser.ConfigParser()
        self.config.read(CONFIG_FILE, 'utf-8')
        x_location = int(self.config['DEFAULT'].get("x_location", '531'))
        y_location = int(self.config['DEFAULT'].get("y_location", '227'))
        self.parent.geometry('+%d+%d' % (x_location, y_location))
        self.parent.resizable(False, False)

        # Define calculator functionalities
        self.number_line = None
        self.create_menu()
        self.create_number_line()
        self.create_workspace()

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
        self.parent.title("Simple calculator")
        self.calculator = SimpleCalculator()
        # If the user performs any operation that requires two numbers (like +, - etc.)
        # Than the new digit will always replace the current number
        self.is_input_new_number = False

    def create_menu(self):
        """
        The goal of the menu is to allow to easily quit the calculator and to quickly swap calculators
        """

        calculator_options = (
            ("Simple calculator", lambda: self.parent.switch_frame(SimpleCalculatorApp)),
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

        self.number_line = tk.Label(text='0', relief=tk.RIDGE, height=2, anchor='e', padx=10,
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

        buttons_lane_1 = tk.Frame(workspace)
        tk.Button(buttons_lane_1, text='C', width=13, height=1, command=lambda:
        self.reset_calculator()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='MC', width=12, height=1, command=lambda:
        self.calculator.clear_memory()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='MR', width=12, height=1, command=lambda:
        self.retrieve_memory()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='M+', width=12, height=1, command=lambda:
        self.add_memory()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='M-', width=12, height=1, command=lambda:
        self.subtract_memory()).pack(side=tk.LEFT)
        buttons_lane_1.pack()

        # For better visibility all key aspects of the calculator will be bold
        buttons_lane2 = tk.Frame(workspace)
        tk.Button(buttons_lane2, text='1/x', width=10, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.RECIPROCAL)).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='x\u00b2', width=10, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.POWER, 2)).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='\u221Ax', width=10, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.ROOT, 2)).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='\u00F7', width=10, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.DIVISION)).pack(side=tk.LEFT)
        buttons_lane2.pack()

        buttons_lane3 = tk.Frame(workspace)
        # Number related buttons have white background for better visibility
        tk.Button(buttons_lane3, text='7', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('7')).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='8', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('8')).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='9', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('9')).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='x', width=10, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.MULTIPLICATION)).pack(side=tk.LEFT)
        buttons_lane3.pack()

        buttons_lane4 = tk.Frame(workspace)
        tk.Button(buttons_lane4, text='4', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('4')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='5', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('5')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='6', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('6')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='-', width=10, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.SUBTRACTION)).pack(side=tk.LEFT)
        buttons_lane4.pack()

        buttons_lane5 = tk.Frame(workspace)
        tk.Button(buttons_lane5, text='1', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('1')).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='2', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('2')).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='3', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('3')).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='+', width=10, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.ADDITION)).pack(side=tk.LEFT)
        buttons_lane5.pack()

        buttons_lane6 = tk.Frame(workspace)
        tk.Button(buttons_lane6, text='+/-', width=10, height=2, background='white', font='bold', command=lambda:
        self.prepend_sign()).pack(side=tk.LEFT)
        tk.Button(buttons_lane6, text='0', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_number('0')).pack(side=tk.LEFT)
        tk.Button(buttons_lane6, text=',', width=10, height=2, background='white', font='bold', command=lambda:
        self.append_decimal()).pack(side=tk.LEFT)
        #  = button will have different background to be more recognizable
        tk.Button(buttons_lane6, text='=', width=10, height=2, background='light blue', font='bold', command=lambda:
        self.finish_two_digit_operation()).pack(side=tk.LEFT)
        buttons_lane6.pack()

        workspace.pack()

    def reset_calculator(self):
        self.calculator.restart()
        self.number_line['text'] = ZERO

    def retrieve_memory(self):
        if self.calculator.is_working:
            self.set_number(self.calculator.memory)

    def add_memory(self):
        if self.calculator.is_working:
            self.calculator.add_memory(float(self.number_line['text']))

    def subtract_memory(self):
        if self.calculator.is_working:
            self.calculator.subtract_memory(float(self.number_line['text']))

    # The number cannot have more than 12 digits due to inability to display more digits than that
    def is_max_length(self):
        if len(self.number_line['text'].replace(MINUS_SIGN, '').replace(POINT, '')) == MAX_NO_DIGITS:
            messagebox.showwarning("Too many digits",
                                   f'The maximum number of digits that the calculator can display is:  {MAX_NO_DIGITS}')
            return True
        return False

    def append_number(self, digit):
        """
        Append the digit to the current number
        """

        if self.calculator.is_working:
            # Special case for 0 (replace digit) and with a new number after operation
            if self.number_line['text'] == ZERO or self.is_input_new_number:
                self.number_line['text'] = digit
                self.is_input_new_number = False
            elif not self.is_max_length():
                self.number_line['text'] += digit

    def append_decimal(self):
        """
        Append decimal point to the current number
        """

        if self.calculator.is_working and POINT not in self.number_line['text'] and not self.is_input_new_number:
            self.number_line['text'] += POINT

    def prepend_sign(self):
        """
        Prepend proper sign to the value (by default no visible sign is a + sign)
        Sign is not prepended to the 0 value
        """

        if self.calculator.is_working and not self.is_input_new_number:
            if MINUS_SIGN in self.number_line['text']:
                self.number_line['text'] = self.number_line['text'][1:]
            elif self.number_line['text'] != ZERO:
                self.number_line['text'] = MINUS_SIGN + self.number_line['text']

    def set_number(self, number):
        """
        Swap currently displayed number with a new number or error messsage
        """

        if number is None:
            self.number_line['text'] = ERROR_DISPLAY
        else:
            self.number_line['text'] = self.format_number(number)

    def format_number(self, number):
        """
        Format the number so that it fits into the display of the calculator
        """

        integer_part, _, decimal_part = number.replace(MINUS_SIGN, '').partition('.')
        # Number cannot be displayed because it's too large
        if len(integer_part) > MAX_NO_DIGITS:
            self.calculator.disable()
            return ERROR_DISPLAY
        # There are no decimal numbers. We can display the number immediately
        elif len(decimal_part) == 0:
            return number
        # Display float values up to 12 digits. Remove trailing zeros
        else:
            no_signs_display = MAX_NO_DIGITS
            if MINUS_SIGN in number:
                no_signs_display += 1
            if POINT in number:
                no_signs_display += 1
            display_number = number[:no_signs_display].rstrip(ZERO)
            if display_number[-1] == POINT:
                display_number = display_number[:-1]
            # Don't display -0
            if len(display_number) == 2 and display_number[0] == MINUS_SIGN and display_number[1] == ZERO:
                display_number = ZERO

            return display_number

    # One digit operations are operation that only require one number like x^2
    def perform_one_digit_operation(self, operation: SingleDigitOperations, condition_number=None):
        if self.calculator.is_working:
            self.calculator.calculate_one_digit_operation(float(self.number_line['text']), operation, condition_number)
            self.calculator.operation = None
            self.set_number(self.calculator.number)

    # Start operation (like +, - etc.) that requires two numbers
    def start_two_digit_operation(self, operation: TwoDigitOperations):
        if self.calculator.is_working:
            self.calculator.number = float(self.number_line['text'])
            self.calculator.operation = operation
            self.is_input_new_number = True

    def finish_two_digit_operation(self):
        if self.calculator.is_working and self.calculator.operation is not None:
            self.calculator.calculate_two_digit_operation(float(self.number_line['text']))
            self.set_number(self.calculator.number)


class AdvancedCalculatorApp(SimpleCalculatorApp):
    def __init__(self, parent: App):
        super().__init__(parent)
        self.parent.title("Advanced calculator")
        self.calculator = AdvancedCalculator()

    # This workspace will have more buttons packed that simple calculator
    def create_workspace(self):
        workspace = tk.Frame(self)

        buttons_lane_1 = tk.Frame(workspace)
        tk.Button(buttons_lane_1, text='C', width=12, height=1, command=lambda:
        self.reset_calculator()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='MC', width=12, height=1, command=lambda:
        self.calculator.clear_memory()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='MR', width=12, height=1, command=lambda:
        self.retrieve_memory()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='M+', width=12, height=1, command=lambda:
        self.add_memory()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='M-', width=12, height=1, command=lambda:
        self.subtract_memory()).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='\u230AX\u230B', width=12, height=1, command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.FLOOR)).pack(side=tk.LEFT)
        tk.Button(buttons_lane_1, text='\u2308X\u2309', width=12, height=1, command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.CEIL)).pack(side=tk.LEFT)
        buttons_lane_1.pack()

        buttons_lane2 = tk.Frame(workspace)
        tk.Button(buttons_lane2, text='1/x', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.RECIPROCAL)).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='|x|', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.ABSOLUTE_VALUE)).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='n!', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.FACTORIAL)).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='\u03C0', width=9, height=2, font='bold', command=lambda:
        self.set_number(str(math.pi))).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='e', width=9, height=2, font='bold', command=lambda:
        self.set_number(str(math.e))).pack(side=tk.LEFT)
        tk.Button(buttons_lane2, text='rand', width=9, height=2, font='bold', command=lambda:
        self.set_number(str(random.random()))).pack(side=tk.LEFT)
        buttons_lane2.pack()

        buttons_lane3 = tk.Frame(workspace)
        tk.Button(buttons_lane3, text='x\u00b2', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.POWER, 2)).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='x\u00b3', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.POWER, 3)).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='\u221Ax', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.ROOT, 2)).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='\u221Bx', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.ROOT, 3)).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='mod', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.MODULO)).pack(side=tk.LEFT)
        tk.Button(buttons_lane3, text='\u00F7', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.DIVISION)).pack(side=tk.LEFT)
        buttons_lane3.pack()

        buttons_lane4 = tk.Frame(workspace)
        tk.Button(buttons_lane4, text='xʸ', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.EXPONENTATION)).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='ʸ\u221Ax', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.ROOT)).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='7', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('7')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='8', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('8')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='9', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('9')).pack(side=tk.LEFT)
        tk.Button(buttons_lane4, text='x', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.MULTIPLICATION)).pack(side=tk.LEFT)
        buttons_lane4.pack()

        buttons_lane5 = tk.Frame(workspace)
        tk.Button(buttons_lane5, text='10ˣ', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.TOPOWER, 10)).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='2ˣ', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.TOPOWER, 2)).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='4', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('4')).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='5', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('5')).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='6', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('6')).pack(side=tk.LEFT)
        tk.Button(buttons_lane5, text='-', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.SUBTRACTION)).pack(side=tk.LEFT)
        buttons_lane5.pack()

        buttons_lane6 = tk.Frame(workspace)
        tk.Button(buttons_lane6, text='log', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.LOG, 10)).pack(side=tk.LEFT)
        tk.Button(buttons_lane6, text='logᵧx', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.LOG)).pack(side=tk.LEFT)
        tk.Button(buttons_lane6, text='1', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('1')).pack(side=tk.LEFT)
        tk.Button(buttons_lane6, text='2', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('2')).pack(side=tk.LEFT)
        tk.Button(buttons_lane6, text='3', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('3')).pack(side=tk.LEFT)
        tk.Button(buttons_lane6, text='+', width=9, height=2, font='bold', command=lambda:
        self.start_two_digit_operation(TwoDigitOperations.ADDITION)).pack(side=tk.LEFT)
        buttons_lane6.pack()

        buttons_lane7 = tk.Frame(workspace)
        tk.Button(buttons_lane7, text='ln', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.LOG, math.e)).pack(side=tk.LEFT)
        tk.Button(buttons_lane7, text='eˣ', width=9, height=2, font='bold', command=lambda:
        self.perform_one_digit_operation(SingleDigitOperations.TOPOWER, math.e)).pack(side=tk.LEFT)
        tk.Button(buttons_lane7, text='+/-', width=9, height=2, font='bold', background='white', command=lambda:
        self.prepend_sign()).pack(side=tk.LEFT)
        tk.Button(buttons_lane7, text='0', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_number('0')).pack(side=tk.LEFT)
        tk.Button(buttons_lane7, text=',', width=9, height=2, font='bold', background='white', command=lambda:
        self.append_decimal()).pack(side=tk.LEFT)
        tk.Button(buttons_lane7, text='=', width=9, height=2, font='bold', background='light blue', command=lambda:
        self.finish_two_digit_operation()).pack(side=tk.LEFT)
        buttons_lane7.pack()

        workspace.pack()
