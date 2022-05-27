import math
from calculator.utils import SingleDigitOperations, TwoDigitOperations


class SimpleCalculator:
    """
    Class to mantain simple operations (+, -, *, /, 1/x, x^2, sqrt(x)  MC, C, MR M+, M-)
    Used for simple calculator app
    """

    def __init__(self):
        self._number: float = 0
        self._memory: float = 0
        self._operation = None

    @property
    def number(self):
        if self._number is None:
            return self._number
        elif int(self._number) == self._number:
            return str(int(self._number))
        else:
            return f'{self._number:.30f}'

    @number.setter
    def number(self, number):
        self._number = number

    @property
    def memory(self):
        if int(self._memory) == self._memory:
            return str(int(self._memory))
        else:
            return f'{self._memory:.30f}'

    @memory.setter
    def memory(self, memory):
        self._memory = memory

    @property
    def operation(self):
        return self._operation

    @operation.setter
    def operation(self, operation):
        self._operation = operation

    # Calculate operations where no second digit is required (or it can be deduced)
    def calculate_one_digit_operation(self, number, operation: SingleDigitOperations, condition_number):
        if operation == SingleDigitOperations.RECIPROCAL:
            self.reciprocal(number)
        elif operation == SingleDigitOperations.POWER:
            self.power_given_value(number, condition_number)
        elif operation == SingleDigitOperations.ROOT:
            self.root_given_value(number, condition_number)

    # Calculate operations where two digits are required (the number and operation is already stored in calculator)
    def calculate_two_digit_operation(self, number):
        if self._operation == TwoDigitOperations.ADDITION:
            self.add(number)
        elif self._operation == TwoDigitOperations.SUBTRACTION:
            self.subtract(number)
        elif self._operation == TwoDigitOperations.MULTIPLICATION:
            self.multiply(number)
        elif self._operation == TwoDigitOperations.DIVISION:
            self.divide(number)

    def add(self, number):
        self._number += number

    def subtract(self, number):
        self._number -= number

    def multiply(self, number):
        self._number *= number

    def divide(self, number):
        if number == 0:
            self._number = None
        else:
            self._number /= number

    def reciprocal(self, number):
        if number == 0:
            self._number = None
        else:
            self._number = 1 / number

    def power_given_value(self, number, power):
        try:
            self._number = math.pow(number, power)
        except ValueError:
            self._number = None

    def root_given_value(self, number, root):
        # Special condition for negative numbers and integer roots to allow for more diversity in computing
        if number < 0 and root % 2 == 1:
            try:
                self._number = -math.pow(abs(number), 1 / root)
            except ValueError:
                self._number = None
        # For other occassions we can calculate the power of the inverse
        else:
            self.power_given_value(number, 1 / root)

    # M+ operation
    def add_memory(self, number: float):
        self._memory += number

    # M- operation
    def subtract_memory(self, number: float):
        self._memory -= number

    # MC operation
    def clear_memory(self):
        self._memory = 0

    # If the operation results in an error than the calculator is turned off
    # and no operations can be made (excluding clearing memory) until restart
    @property
    def is_working(self):
        return self._number is not None

    def disable(self):
        self._number = None

    def restart(self):
        self._number = 0
        self._operation = None


class AdvancedCalculator(SimpleCalculator):
    def __init__(self):
        super().__init__()

    def calculate_one_digit_operation(self, number, operation: SingleDigitOperations, condition_number):
        if operation == SingleDigitOperations.FLOOR:
            self.floor(number)
        elif operation == SingleDigitOperations.CEIL:
            self.ceil(number)
        elif operation == SingleDigitOperations.ABSOLUTE_VALUE:
            self.absolute_value(number)
        elif operation == SingleDigitOperations.FACTORIAL:
            self.factorial(number)
        elif operation == SingleDigitOperations.TOPOWER:
            self.power_given_value(condition_number, number)
        elif operation == SingleDigitOperations.LOG:
            self.log_given_value(number, condition_number)
        else:
            super().calculate_one_digit_operation(number, operation, condition_number)

    def calculate_two_digit_operation(self, number: float):
        if self._operation == TwoDigitOperations.MODULO:
            self.modulo(number)
        elif self._operation == TwoDigitOperations.EXPONENTATION:
            self.power(number)
        elif self._operation == TwoDigitOperations.ROOT:
            self.root(number)
        elif self._operation == TwoDigitOperations.LOG:
            self.log(number)
        else:
            super().calculate_two_digit_operation(number)

    def floor(self, number):
        self._number = math.floor(number)

    def ceil(self, number):
        self._number = math.ceil(number)

    def absolute_value(self, number):
        self._number = abs(number)

    def factorial(self, number):
        try:
            self._number = math.factorial(number)
        except ValueError:
            self._number = None

    def modulo(self, number):
        self._number %= number

    def power(self, power):
        self.power_given_value(self._number, power)

    def root(self, root):
        self.root_given_value(self._number, root)

    def log_given_value(self, number, log):
        try:
            self._number = math.log(number, log)
        except ValueError:
            self._number = None

    def log(self, log):
        self.log_given_value(self._number, log)
