#!/usr/bin/env python

# Copyright(c) 2015, Shihira Fung <fengzhiping@hotmail.com>

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../core"))

from context import context
from policy import policy

sample1 = """
load!: policy_test
assert!: is_authenticated

await: modify_email -> address
apply: send_verf_email(address)

await: verf_email_recv
apply: save_current_user_info(address)
"""

sample2 = """
load!: policy_test

await: first_string -> s1
apply: concat_with_time(s1) -> s1

await: second_string -> s2
apply: concat_with_time(s2) -> s2

await: return_result
apply: join_with_linefeed(s1, s2) -> result
yield: result
"""

############################################################
# DELEGATES FOR sample1:

def is_authenticated():
    print "Confirmed user identity"
    return True

def send_verf_email(address):
    print "Sent email to %s, and wait for the reception of user..." % address

def save_current_user_info(address):
    print "Updated the current user info: email = %s" % address

############################################################
# DELEGATES FOR sample1:

def concat_with_time(s):
    import time

    return str(s) + time.ctime()

def join_with_linefeed(s1, s2):
    return "%s\n%s\n" % (str(s1), str(s2))

############################################################
# TEST PROCEDURE

def tests():

    # sample1 ##############################################
    c = context.start_new()

    if True:
        p = policy.load(sample1)
        p.load_context(c)
        p.provide("modify_email", "john@example.com")

        p.resume()

    if True:
        p = policy.load(sample1)
        p.load_context(c)
        p.provide("verf_email_recv")
        p.resume()

        assert(p.is_end())

    # sample2 ##############################################
    c = context.start_new()

    if True:
        p = policy.load(sample2)
        p.load_context(c)
        p.provide("first_string", "First Record: ")
        p.resume()

    if True:
        p = policy.load(sample2)
        p.load_context(c)
        p.provide("second_string", "Second Record: ")
        p.resume()

    if True:
        p = policy.load(sample2)
        p.load_context(c)
        p.provide("return_result")
        print p.resume()[0]

        assert(p.is_end())


if __name__ == "__main__":
    tests()

