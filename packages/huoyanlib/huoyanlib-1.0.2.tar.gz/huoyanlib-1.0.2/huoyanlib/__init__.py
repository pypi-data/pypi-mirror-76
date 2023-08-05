class HuoYanError(Exception):
    """"nothing"""


def _raise_huoyanerror_object():
    raise HuoYanError('Please use the right object')


def _raise_huoyanerror_tcl():
    raise HuoYanError('this object can‘t be used in tkinter')