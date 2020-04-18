class Describer(object):

    def __init__(self, *args, **kwargs):
        self.base = args[0]

    def __get__(self, instance, owner):
        return self.base

    def __set__(self, instance, value):
        pass


class NotDataDescriber(object):

    def __init__(self, *args, **kwargs):
        self.base = args[0]

    def __get__(self, instance, owner):
        return self.base


class Master(object):
    data_describer = Describer(1)
    not_data_describer = NotDataDescriber(2)

    def __init__(self, *args, **kwargs):
        self.data_describer = 100
        self.not_data_describer = 10000

if __name__ == '__main__':
    master = Master()
    print master.__dict__
    print master.not_data_describer
    print master.data_describer