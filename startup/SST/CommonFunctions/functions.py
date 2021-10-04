from IPython.utils.coloransi import TermColors as color
import sys
import ansiwrap
from select import select


def colored(text, tint="white", attrs=[]):
    """
    A simple wrapper around IPython's interface to TermColors
    """
    tint = tint.lower()
    if "dark" in tint:
        tint = "Dark" + tint[4:].capitalize()
    elif "light" in tint:
        tint = "Light" + tint[5:].capitalize()
    elif "blink" in tint:
        tint = "Blink" + tint[5:].capitalize()
    elif "no" in tint:
        tint = "Normal"
    else:
        tint = tint.capitalize()
    return "{0}{1}{2}".format(getattr(color, tint), str(text), color.Normal)


def run_report(thisfile):
    """
    Noisily proclaim to be importing a file of python code.
    """
    print(colored("Importing %s ..." % thisfile.split("/")[-1], "lightcyan"))


def boxed_text(title, text, tint, width=75, shrink=False):
    """
    Put text in a lovely unicode block element box.  The top
    of the box will contain a title.  The box elements will
    be coloreded.
    """

    if shrink:
        width = min(width, max((ansiwrap.ansilen(line) for line in text.split("\n"))))

    remainder = width - 5 - len(title)
    ul = u"\u250C"  # u'\u2554'
    ur = u"\u2510"  # u'\u2557'
    ll = u"\u2514"  # u'\u255A'
    lr = u"\u2518"  # u'\u255D'
    bar = u"\u2500"  # u'\u2550'
    strut = u"\u2502"  # u'\u2551'
    print("")
    print(colored("".join([ul, bar * 3, " ", title, " ", bar * remainder, ur]), tint))
    for line1 in text.splitlines():
        lines = ansiwrap.fill(line1, width, subsequent_indent=" " * 26)
        for line in lines.splitlines():
            line = line.rstrip()
            add = ""
            add = " " * (width - ansiwrap.ansilen(line))
            print("".join([colored(strut, tint), line, add, colored(strut, tint)]))
    print(colored("".join([ll, bar * width, lr]), tint))


def read_input(message, default, timeout, secs):
    print(message)
    rlist, _, _ = select([sys.stdin], [], [], secs)
    if rlist:
        s = sys.stdin.readline()
        if ord(s[0]) == 13 or ord(s[0]) == 10:
            return default
        else:
            return s.rstrip(chr(10) + chr(13))
    else:
        return timeout


def error_msg(text):
    return colored(text, "lightred")


def warning_msg(text):
    return colored(text, "yellow")


def url_msg(text):
    return text


def bold_msg(text):
    return colored(text, "white")


def verbosebold_msg(text):
    return colored(text, "lightcyan")


def list_msg(text):
    return colored(text, "cyan")


def disconnected_msg(text):
    return colored(text, "purple")


def info_msg(text):
    return colored(text, "brown")


def whisper(text):
    return colored(text, "darkgray")
