from enum import Enum


class SingleDigitOperations(Enum):
    """
    Enum represeting all single digit operations
    """
    RECIPROCAL = "1/x"
    POWER = "x^a"
    ROOT = "root(x)"
    FLOOR = "floor(x)"
    CEIL = "ceil(x)"
    ABSOLUTE_VALUE = "|x|"
    FACTORIAL = "n!"
    TOPOWER = "a^x"
    LOG = "logarithm"


class TwoDigitOperations(Enum):
    """
    Enum representing all possible two digit operations
    """
    ADDITION = "+"
    SUBTRACTION = "-"
    MULTIPLICATION = "*"
    DIVISION = "/"
    MODULO = "mod"
    EXPONENTATION = "x^y"
    ROOT = "root(x) of y"
    LOG = "logarithm"
