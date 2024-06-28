import random

class A:
    def __init__(self, seed):
        random.seed(seed)

    def func(self, a, b):
        return random.randint(a, b)

a = A(10)

print(a.func(2, 4))
