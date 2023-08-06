MSG = 3


def hello(count=0):
    return "Hello world {}! {}".format(MSG, count)


def goodbye(name="Joe"):
    return "Goodbye {} {}".format(MSG, name)
