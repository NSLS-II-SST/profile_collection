from ..HW.detectors import waxs_det

def giveme_inputs(*args, **kwargs):
    return args, kwargs


def string_to_inputs(string):
    return eval("giveme_inputs(" + string + ")")


def args_to_string(*args, **kwargs):
    outstr = ""
    for arg in args:
        if isinstance(arg, str):
            outstr += f'"{arg}",'
        else:
            outstr += f"{arg},"
    for key in kwargs.keys():
        if isinstance(kwargs[key], str):
            outstr += f'{key} = "{kwargs[key]}", '
        else:
            outstr += f"{key} = {kwargs[key]}, "
    return outstr.rstrip(", ")
