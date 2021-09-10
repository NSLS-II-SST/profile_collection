run_report(__file__)

from .RSoXSBase.configurations import *

@register_line_magic
def nmode(line):
    RE(all_out())
del nmode


@register_line_magic
def wmode(line):
    RE(WAXSmode())
del wmode


@register_line_magic
def smode(line):
    RE(SAXSmode())
del smode

