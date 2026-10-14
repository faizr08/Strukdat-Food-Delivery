"""
backend/M2.py - Milestone 2: Stack, Postfix Evaluator, Naive Queue, Circular Queue
"""

class StackCart:
    def __init__(self):
        self.items = []

    def push(self, item):
        self.items.append(item)

    def pop(self):
        if not self.is_empty():
            return self.items.pop()
        return None

    def peek(self):
        if not self.is_empty():
            return self.items[-1]
        return None

    def is_empty(self):
        return len(self.items) == 0

    def size(self):
        return len(self.items)


class PostfixEvaluator:
    @staticmethod
    def evaluate(expression):
        stack = []
        tokens = expression.split()
        for token in tokens:
            if token.replace('.', '', 1).isdigit():
                if '.' in token:
                    stack.append(float(token))
                else:
                    stack.append(int(token))
            elif token in ['+', '-', '*', '/']:
                if len(stack) < 2:
                    raise ValueError("Ekspresi RPN tidak valid: operand kurang")
                b = stack.pop()
                a = stack.pop()
                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        raise ValueError("Pembagian dengan nol")
                    stack.append(a / b)
            else:
                raise ValueError(f"Token tidak dikenal: {token}")
        if len(stack) != 1:
            raise ValueError("Ekspresi RPN tidak valid")
        return stack[0]


class NaiveQueue:
    def __init__(self):
        self.items = []

    enqueue = lambda self, item: self.items.append(item)
    dequeue = lambda self: self.items.pop(0) if not self.is_empty() else None
    is_empty = lambda self: len(self.items) == 0
    size = lambda self: len(self.items)


class CircularQueue:
    def __init__(self, max_size=5):
        self.max_size = max_size
        self.queue = [None] * max_size
        self.head = 0
        self.tail = 0
        self.count = 0

    def enqueue(self, item):
        self.queue[self.tail] = item
        self.tail = (self.tail + 1) % self.max_size
        if self.count < self.max_size:
            self.count += 1
        else:
            self.head = (self.head + 1) % self.max_size

    def get_all(self):
        res = []
        for i in range(self.count):
            idx = (self.head + i) % self.max_size
            res.append(self.queue[idx])
        return res
