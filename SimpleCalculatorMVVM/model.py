from operations import *
import math
import logging

# Настройка логирования
logging.basicConfig(filename='calculator.log', level=logging.INFO,
                    format='%(asctime)s - %(message)s')

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

    def logging_decorator(func):
        def wrapper(self, expression):
            try:
                result = func(self, expression)
                logging.info(f"Вычисление: {expression} = {result}")
                return result
            except Exception as e:
                logging.error(f"Ошибка при вычислении {expression}: {str(e)}")
                raise
        return wrapper

    @logging_decorator
    def evaluate(self, expression):
        expression = (expression.replace('^', '**')
                              .replace('√', 'math.sqrt')
                              .replace('sin', 'math.sin')
                              .replace('cos', 'math.cos')
                              .replace('tan', 'math.tan')
                              .replace('ln', 'math.log'))
        return eval(expression, {"math": math, "__builtins__": {}})