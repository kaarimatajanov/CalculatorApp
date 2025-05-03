from operations import *
import math

class CalculatorModel:
    def __init__(self):
        self.operations = {
            '+': Addition(),
            '-': Subtraction(),
            '*': Multiplication(),
            '/': Division(),
            '%': Modulo(),
            '^': Power(),
            '√': SquareRoot(),
            'sin': Sine(),
            'cos': Cosine(),
            'tan': Tangent(),
            'ln': NaturalLog()
        }

    def evaluate(self, expression):
        # Заменяем символы для совместимости с Python
        expression = (expression.replace('^', '**')
                              .replace('√', 'math.sqrt')
                              .replace('sin', 'math.sin')
                              .replace('cos', 'math.cos')
                              .replace('tan', 'math.tan')
                              .replace('ln', 'math.log'))
        # Безопасный eval
        return eval(expression, {"math": math, "__builtins__": {}})