class OurClass:
    value = 10

    def my_method(self):
        print(id(self))

    @classmethod
    def my_class_method(cls):
        print(id(cls))

    @staticmethod
    def my_static_method():
        print("Static")


value = 10

def my_method(self):
    print(id(self))

@classmethod
def my_class_method(cls):
    print(id(cls))

@staticmethod
def my_static_method():
    print("Static")


OurClass2 = type(
    "OurClass2",
    (object,),
    {
        "value": value,
        "my_method": my_method,
        "my_class_method": my_class_method,
        "my_static_method": my_static_method
    }
)


class Lifecycle:
    def __new__(cls, *args, **kwargs):
        print("Called __new__")

        return super().__new__(cls, *args, **kwargs)

    def __init__(self):
        print("__init__")

    def __del__(self):
        print("__del__")
