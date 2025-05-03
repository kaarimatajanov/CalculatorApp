from model import CalculatorModel

class CalculatorViewModel:
    def __init__(self):
        self.model = CalculatorModel()
        self.expression = ""
        self.history = []
        self.error = None

    def append_input(self, char):
        self.expression += char
        self.error = None
        return self.expression

    def evaluate(self):
        try:
            result = self.model.evaluate(self.expression)
            self.history.append(f"{self.expression} = {result}")
            self.expression = str(round(result, 6))
            self.error = None
            return self.expression
        except Exception as e:
            self.error = str(e)
            self.expression = ""
            return None

    def clear(self):
        self.expression = ""
        self.error = None
        return self.expression

    def backspace(self):
        self.expression = self.expression[:-1]
        self.error = None
        return self.expression

    def clear_history(self):
        self.history = []
        return self.history

    def get_history(self):
        return "\n".join(self.history)

    def get_error(self):
        return self.error