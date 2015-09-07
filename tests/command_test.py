#!/usr/bin/env python

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../core"))

from context import context
from parser import _parse_cmdline

import policy

def gen_cl(cl):
    pcl = _parse_cmdline([cl])
    cl = policy.cmdline()
    cl.assign(pcl)
    return cl

def print_string(s):
    print s

def get_a_tuple():
    return (12, 34, 56)

def tests():
    c = context.start_new()

    gen_cl("load: command_test").run(c)
    print c.__dict__

    gen_cl("apply: get_a_tuple -> a, b, c").run(c)
    gen_cl('apply: print_string(c)').run(c)
    gen_cl("apply: get_a_tuple() -> a").run(c)
    gen_cl('apply: print_string(a)').run(c)
    try: gen_cl("apply: get_a_tuple -> a, b").run(c)
    except Exception, e: print e
    try: gen_cl("apply: no_such_func -> a, b").run(c)
    except Exception, e: print e
    print c.__getstate__()

    gen_cl("yield: a b").run(c)
    print c._yield
    gen_cl("yield: c").run(c)
    print c._yield

    c._await_tags += [('get_email', "a@a.com")]
    c._await_tags += [('get_empty', None)]
    gen_cl("await: get_email -> d").run(c)
    gen_cl("apply: print_string(d)").run(c)
    print c.__dict__
    try: gen_cl("await: not_yet_exists -> x").run(c)
    except policy.SleepPolicy, e: print "Sleeping..."
    gen_cl("await: get_empty -> x").run(c)

    gen_cl("assert: d").run(c)
    try: gen_cl("assert: x").run(c)
    except AssertionError: print "Assertion not passed"

if __name__ == "__main__":
    tests()
