
from IPython.utils.coloransi import TermColors as color
import textwrap
import sys, time, msvcrt, ansiwrap

def colored(text, tint='white', attrs=[]):
    '''
    A simple wrapper around IPython's interface to TermColors
    '''
    tint = tint.lower()
    if 'dark' in tint:
        tint = 'Dark' + tint[4:].capitalize()
    elif 'light' in tint:
        tint = 'Light' + tint[5:].capitalize()
    elif 'blink' in tint:
        tint = 'Blink' + tint[5:].capitalize()
    elif 'no' in tint:
        tint = 'Normal'
    else:
        tint = tint.capitalize()
    return '{0}{1}{2}'.format(getattr(color, tint), text, color.Normal)

def run_report(thisfile):
    '''
    Noisily proclaim to be importing a file of python code.
    '''
    print(colored('Importing %s ...' % thisfile.split('/')[-1], 'lightcyan'))

run_report(__file__)


def boxed_text(title, text, tint, width=75):
    '''
    Put text in a lovely unicode block element box.  The top
    of the box will contain a title.  The box elements will
    be coloreded.
    '''
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
        if msvcrt.kbhit():
            byte_arr = msvcrt.getche()
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