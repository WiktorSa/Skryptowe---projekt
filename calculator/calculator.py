class SimpleCalculator:
    """
    Class to mantain simple operations (+, -, *, /, MC, C, MR M+, M-)
    Used for simple calculator app
    """

    def __init__(self):
        self.number: float = 0
        self.memory: float = 0

    def add(self, number: float):
        self.number += number

    def substract(self, number: float):
        self.number -= number

    def multiply(self, number: float):
        self.number *= number

    def divide(self, number: float):
        self.number /= number

    # M+ operation
    def add_memory(self, number: float):
        self.memory += number

    # M- operation
    def substract_memory(self, number: float):
        self.memory -= number

    # MR operation
    def erase_from_memory(self):
        self.number = self.memory
        self.memory = 0

    # MC operation
    def clear_memory(self):
        self.memory = 0

    # C operation
    def clear_number(self):
        self.number = 0


class AdvancedCalculator(SimpleCalculator):
    pass
