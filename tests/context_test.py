#!/usr/bin/env python

# Copyright(c) 2015, Shihira Fung <fengzhiping@hotmail.com>

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../core"))

from context import context

def tests():
    c = context()

    print bool(c)
    print c.__getstate__()
    c.array = [ 1, 2, 3 ]
    c.attr = "Hel"
    print c.attr
    c.attr += "lo"
    print c.__getstate__()

    c = context.start_new()
    print c.__getstate__()
    c._dontstore = "never_store"
    print c.__getstate__()
    c.ensure("array", [1]).array += [2]
    c.ensure("array", [1]).array += [3]
    print c.__getstate__()
    del c.array
    print c.__getstate__()
    c.__setstate__({ "attr": ["a", 1]})
    print c.__getstate__()
    c.__setstate__({ "ensure": "Don't do this!"})
    try: print c.ensure("apple", "pear")
    except TypeError: print "Don't do this!"

    c.clear()
    print c.__getstate__()

if __name__ == "__main__":
    tests()
