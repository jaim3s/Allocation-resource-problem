class A:
    def __init__(self, **kwargs):
        print(kwargs)


a = A(**{"width":2, "asd":3})
