from django.template.defaultfilters import yesno

MSG = 3


def hello(count=0):
    return "Hello world {}! {}".format(MSG, count)


def goodbye(name="Joe"):
    return "Goodbye {} {}".format(MSG, name)


def my_yesno(*args, **kwargs):
    return yesno(*args, **kwargs)
