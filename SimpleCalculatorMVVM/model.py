from operations import *
import math

class OperationFactory:
    @staticmethod
    def create_operation(op_type):
        operations = {
            '+': Addition,
            '-': Subtraction,
            '*': Multiplication,
            '/': Division,
            '%': Modulo,
            '^': Power,
            '√': SquareRoot,
            'sin': Sine,
            'cos': Cosine,
            'tan': Tangent,
            'ln': NaturalLog
        }
        return operations.get(op_type)()

class CalculatorModel:
    def __init__(self):
        self.operation_factory = OperationFactory()

    def evaluate(self, expression):
        expression = (expression.replace('^', '**')
                              .replace('√', 'math.sqrt')
                              .replace('sin', 'math.sin')
                              .replace('cos', 'math.cos')
                              .replace('tan', 'math.tan')
                              .replace('ln', 'math.log'))
        return eval(expression, {"math": math, "__builtins__": {}})