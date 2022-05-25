import math
from calculator.utils import Operations


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

    def calculate(self, number: float):
        if self._operation == Operations.ADDITION:
            self.add(number)
        elif self._operation == Operations.SUBTRACTION:
            self.substract(number)
        elif self._operation == Operations.MULTIPLICATION:
            self.multiply(number)
        elif self._operation == Operations.DIVISION:
            self.divide(number)

    def add(self, number: float):
        self._number += number

    def substract(self, number: float):
        self._number -= number

    def multiply(self, number: float):
        self._number *= number

    def divide(self, number: float):
        self._number /= number

    def reciprocal(self, number: float):
        if number == 0:
            self._number = None
        else:
            self._number = 1 / number

    def power2(self, number):
        self._number = math.pow(number, 2)

    def square_root(self, number):
        if number < 0:
            self._number = None
        else:
            self._number = math.sqrt(number)

    # M+ operation
    def add_memory(self, number: float):
        self._memory += number

    # M- operation
    def substract_memory(self, number: float):
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
    pass
