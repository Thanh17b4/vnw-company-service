from cerberus import Validator


def is_blank(my_string):
    if my_string and my_string.strip():
        return False
    return True


def is_integer(id: any):
    v = Validator({'id': {'type': 'integer'}})
    result = v.validate({'id': id})
    return result

