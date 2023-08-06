class Base(object):
    __data = "Base"

    @classmethod
    def func(cls):
        return "Class name is {}, data is {}".format(cls.__name__, cls.__data)


class A(Base):
    __data = "A"


class B(A):
    pass


b = B()
print(b.__data)
