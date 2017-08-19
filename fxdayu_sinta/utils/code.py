# encoding:utf-8

SH = ".XSHG"
SZ = ".XSHE"


def fold(code):
    if len(code) == 11:
        return code[:6]
    else:
        return code


def unfold(code):
    if len(code) == 6:
        if code.startswith('6'):
            return code + SH
        elif code.startswith('0') or code.startswith('3'):
            return code + SZ
        else:
            return code
    else:
        return code


def tick_code(code):
    code = fold(code)
    if len(code) == 6:
        if code.startswith('6'):
            return "sh"+code
        elif code.startswith('0') or code.startswith('3'):
            return "sz"+code
        else:
            return code
    else:
        return code
