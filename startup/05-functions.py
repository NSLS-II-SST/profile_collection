run_report(__file__)

import sys, time, ansiwrap
import time, sys
import sys

if sys.platform[:3] == 'win':
    import msvcrt

    def getkey():
        key = msvcrt.getche()
        return key

    def kbhit():
        return msvcrt.kbhit()

elif sys.platform[:3] == 'lin':
    import getch
    from select import select
    def getkey():
        key = getch.getche()
        return key
    def kbhit():
        dr, dw, de = select([sys.stdin], [], [], 0)
        return dr != []


def boxed_text(title, text, tint, width=75, shrink=False):
    '''
    Put text in a lovely unicode block element box.  The top
    of the box will contain a title.  The box elements will
    be coloreded.
    '''

    if shrink:
        width = min(width,max((ansiwrap.ansilen(line) for line in text.split('\n'))))


    remainder = width - 5 - len(title)
    ul        = u'\u250C' # u'\u2554'
    ur        = u'\u2510' # u'\u2557'
    ll        = u'\u2514' # u'\u255A'
    lr        = u'\u2518' # u'\u255D'
    bar       = u'\u2500' # u'\u2550'
    strut     = u'\u2502' # u'\u2551'
    print('')
    print(colored(''.join([ul, bar*3, ' ', title, ' ', bar*remainder, ur]), tint))
    for line1 in text.splitlines():
        lines = ansiwrap.fill(line1,width,subsequent_indent=" "*26)
        for line in lines.splitlines():
            line = line.rstrip()
            add = ''
            add = ' '*(width-ansiwrap.ansilen(line))
            print(''.join([colored(strut, tint), line, add, colored(strut, tint)]))
    print(colored(''.join([ll, bar*width, lr]), tint))


def read_input( caption, default, timeoutval, timeout = 5):

    start_time = time.time()
    sys.stdout.write('%s(%s):'%(caption, default))
    sys.stdout.flush()
    input = ''
    timedout=False
    while True:
        if kbhit():
            byte_arr = getkey()
            if ord(byte_arr) == 13: # enter_key
                break
            elif ord(byte_arr) >= 32: #space_char
                input += "".join(map(chr,byte_arr))
        if len(input) == 0 and (time.time() - start_time) > timeout:
            print("timed out, continuing.")
            input = timeoutval
            timedout=True
            break

    print('')  # needed to move to next line
    if timedout:
        return timeoutval
    elif len(input) > 0:
        return input
    else:
        return default




def error_msg(text):
    return colored(text, 'lightred')
def warning_msg(text):
    return colored(text, 'yellow')
def url_msg(text):
    return text
def bold_msg(text):
    return colored(text, 'white')
def verbosebold_msg(text):
    return colored(text, 'lightcyan')
def list_msg(text):
    return colored(text, 'cyan')
def disconnected_msg(text):
    return colored(text, 'purple')
def info_msg(text):
    return colored(text, 'brown')
def whisper(text):
    return colored(text, 'darkgray')
