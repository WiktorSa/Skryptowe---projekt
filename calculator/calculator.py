class SimpleCalculator:
    """
    Class to mantain simple operations (+, -, *, /, 1/x, x^2, sqrt(x)  MC, C, MR M+, M-)
    Used for simple calculator app
    """

    def __init__(self):
        self._number: float = 0
        self._memory: float = 0

    @property
    def number(self):
        return self._number

    @property
    def memory(self):
        return self._memory

    def add(self, number: float):
        self._number += number

    def substract(self, number: float):
        self._number -= number

    def multiply(self, number: float):
        self._number *= number

    def divide(self, number: float):
        self._number /= number

    # M+ operation
    def add_memory(self, number: float):
        self._memory += number

    # M- operation
    def substract_memory(self, number: float):
        self._memory -= number

    # MR operation
    def erase_from_memory(self):
        self._number = self._memory
        self._memory = 0

    # MC operation
    def clear_memory(self):
        self._memory = 0

    # C operation
    def clear_number(self):
        self._memory = 0


class AdvancedCalculator(SimpleCalculator):
    pass
