#!/usr/bin/env python

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../core"))

from parser import _parse_sign, _parse_string, _parse_symbol
from parser import _parse_cmdline, _parse_argument, _parse_parameter
from parser import PolicyParsingError

def tests():
    # sign test
    print _parse_sign(["(abcd"], "(")
    print _parse_sign([" -> abcd"], "->")
    print _parse_sign([" - > abcd"], "->")

    # string test
    print _parse_string([' "hello"'])
    print _parse_string(['"" Not "hello"'])
    print _parse_string(['"he\\""llo"'])
    print _parse_string([r'"he\\llo\"'])

    # symbol test
    print _parse_symbol(['1abcd'])
    print _parse_symbol(['__sd#'])
    print _parse_symbol(['_^e_sd#'])

    # parameter test
    print _parse_parameter(['"hell\\"o"'])
    print _parse_parameter(['_hel"lo"'])
    try: print parameter([' 1hello'])
    except Exception, e: print e

    # argument test
    print _parse_argument(["argum"])
    print _parse_argument(["argum()"])
    print _parse_argument(["argum(sym1, sym2)"])
    try: print _parse_argument(["argum(sym1, sym2, )"])
    except Exception, e: print e
    try: print _parse_argument(["argum(sym1, 2sym)"])
    except Exception, e: print e
    print _parse_argument(['argum(sym1, "hello\\n", sym2)'])
    print _parse_argument(['argum(",",",%",",\\",")'])

    # command line test
    print _parse_cmdline(["command: argument"])
    print _parse_cmdline(["command: argument()"])
    print _parse_cmdline(["cmd: argument() -> a"])
    print _parse_cmdline(['cmd: argument(a, "6") argg -> a, b(c)'])
    print _parse_cmdline(['cmd_cmd!: arg(a, "6") -> a, b(c)'])

if __name__ == "__main__":
    tests()
