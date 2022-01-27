class ClassForTesting:
    def use_this_func(self, a):
        return a


class ClassForTesting2(ClassForTesting):
    def use_this_func(self, a):
        b = a * 10
        return b


class ClassForTesting3(ClassForTesting):
    pass


class ClassForTesting4(ClassForTesting2):
    def use_this_func(self, a):
        b = a * 10
        c = b + 10
        return c
