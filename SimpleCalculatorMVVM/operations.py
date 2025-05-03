from abc import ABC, abstractmethod
import math

# Абстрактный класс операции
class Operation(ABC):
    @abstractmethod
    def execute(self, a, b=None):
        pass

# Конкретные операции
class Addition(Operation):
    def execute(self, a, b):
        return a + b

class Subtraction(Operation):
    def execute(self, a, b):
        return a - b

class Multiplication(Operation):
    def execute(self, a, b):
        return a * b

class Division(Operation):
    def execute(self, a, b):
        if b == 0:
            raise ValueError("Деление на ноль!")
        return a / b

class Modulo(Operation):
    def execute(self, a, b):
        return a % b

class Power(Operation):
    def execute(self, a, b):
        return a ** b

class SquareRoot(Operation):
    def execute(self, a, b=None):
        if a < 0:
            raise ValueError("Квадратный корень из отрицательного числа!")
        return math.sqrt(a)

class Sine(Operation):
    def execute(self, a, b=None):
        return math.sin(a)

class Cosine(Operation):
    def execute(self, a, b=None):
        return math.cos(a)

class Tangent(Operation):
    def execute(self, a, b=None):
        return math.tan(a)

class NaturalLog(Operation):
    def execute(self, a, b=None):
        if a <= 0:
            raise ValueError("Логарифм не определен для неположительных чисел!")
        return math.log(a)