from abc import ABC, abstractmethod

# Command interface (unchanged)
class Command(ABC):
    @abstractmethod
    def execute(self, operands):
        pass

# Concrete Commands (unchanged)
class AddCommand(Command):
    def execute(self, operands):
        return operands.pop() + operands.pop()

class SubtractCommand(Command):
    def execute(self, operands):
        b = operands.pop()
        a = operands.pop()
        return a - b

# Command Factory (unchanged)
class CommandFactory:
    @staticmethod
    def get_command(operator):
        if operator == '+':
            return AddCommand()
        elif operator == '-':
            return SubtractCommand()
        else:
            raise ValueError(f"Unknown operator: {operator}")

# Strategy interface
class CalculationStrategy(ABC):
    @abstractmethod
    def calculate(self, expression):
        pass

# Concrete Strategy for Postfix notation
class PostfixStrategy(CalculationStrategy):
    def calculate(self, expression):
        stack = []
        for token in expression:
            if token.isdigit():
                stack.append(int(token))
            else:
                command = CommandFactory.get_command(token)
                result = command.execute(stack)
                stack.append(result)
        return stack[-1] if stack else None

# Concrete Strategy for Infix notation (simplified, assumes single-digit numbers)
class InfixStrategy(CalculationStrategy):
    def calculate(self, expression):
        operators = []
        operands = []
        for token in expression:
            if token.isdigit():
                operands.append(int(token))
            elif token in ['+', '-']:
                while operators and operators[-1] in ['+', '-']:
                    command = CommandFactory.get_command(operators.pop())
                    result = command.execute(operands)
                    operands.append(result)
                operators.append(token)
        while operators:
            command = CommandFactory.get_command(operators.pop())
            result = command.execute(operands)
            operands.append(result)
        return operands[-1] if operands else None

# Calculator class (modified to use Strategy)
class Calculator:
    def __init__(self, strategy):
        self.strategy = strategy

    def set_strategy(self, strategy):
        self.strategy = strategy

    def calculate(self, expression):
        return self.strategy.calculate(expression)

# Controller (modified to use Strategy)
class CalculatorController:
    def __init__(self):
        self.calculator = Calculator(PostfixStrategy())  # Default to Postfix

    def set_strategy(self, strategy):
        self.calculator.set_strategy(strategy)

    def process_expression(self, expression):
        return self.calculator.calculate(expression)

# Usage
controller = CalculatorController()

# Using Postfix notation
postfix_result = controller.process_expression(["16", "5", "+"])
print(f"Postfix Result: {postfix_result}")  # Output: Postfix Result: 21

# Switch to Infix notation
controller.set_strategy(InfixStrategy())
infix_result = controller.process_expression(["5", "+", "3"])
print(f"Infix Result: {infix_result}")  # Output: Infix Result: 8
