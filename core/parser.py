# Copyright(c) 2015, Shihira Fung <fengzhiping@hotmail.com>

import re

class PolicyParsingError(Exception):
    def __init__(self, message, row = 0, col = 0):
        super(PolicyParsingError, self).__init__(message)

        self.row = row
        self.col = col

    def __str__(self):
        return "[row %d, col %d] %s" \
                % (self.row, self.col, self.message)

def _parse_sign(source, sign):
    source[0] = re.match(r"\s*(.*)", source[0]).group(1)
    # cut the same length from the source and compare
    if source[0][:len(sign)] != sign:
        return False
    source[0] = source[0][len(sign):]
    return True

_len = lambda x : len(x[0])

def _parse_symbol(source):
    """
    letter ::= 'A' | ... | 'Z' | 'a' | ... | 'z'
    underscore ::= '_'
    digit ::= '0' | ... | '9'
    symbol ::=
        letter | underscore
        { letter | underscore | digit }
    """
    symbol = re.match(r"\s*([A-Za-z_][A-Za-z0-9_]*)(.*)", source[0])
    if not symbol:
        return ""
    source[0] = symbol.group(2)
    return symbol.group(1)

def _parse_string(source):
    r"""
    string ::=
        '"' {
        [ OTHER THAN '\' '"' | '\n' | '\r' | '\"' | '\\' ]
        } '"'
    """
    string = re.match(
        r'\s*("([^\\"]|\\[nr\\"])*")(.*)', source[0])

    if not string:
        return ""
    source[0] = string.group(3)
    return string.group(1)

class _parse_parameter:
    """
    variable ::= symbol
    value ::= string | variable
    parameter ::= value
    """
    def __init__(self, param):
        full_len = _len(param)

        self.param_type = None
        self.value = _parse_string(param)

        if not self.value:
            self.value = _parse_symbol(param)
            if self.value:
                self.param_type = "symbol"
            else:
                raise PolicyParsingError(
                        "Invalid symbol", col = full_len - _len(param))
        else:
            self.param_type = "string"

    def __str__(self):
        return "{%s:%s}" % (self.param_type, self.value)


class _parse_argument:
    """
    parameter-list ::=
        '('
        [ parameter-list ',' parameter | parameter ]
        ')'
    argument ::= symbol [ parameter-list ]
    """
    def __init__(self, arg):
        full_len = _len(arg)
        self.parameter_list = []

        self.name = _parse_symbol(arg)

        if not self.name: raise PolicyParsingError(
                "Missing argument name", col = full_len - _len(arg))
        has_lprnth = _parse_sign(arg, "(")
        # left parenthesis not found is not an error
        if not has_lprnth: pass
        else:
            has_comma = False
            try:
                while True:
                    self.parameter_list += [_parse_parameter(arg)]
                    has_comma = _parse_sign(arg, ",")
                    if not has_comma: break
            except PolicyParsingError, e:
                e.col += full_len - _len(arg)
                if has_comma: raise e

            has_rprnth = _parse_sign(arg, ")")
            if not has_rprnth: raise PolicyParsingError(
                    "Missing right parenthesis", col = full_len - _len(arg))

    def __str__(self):
        return "<%s %s>" % (self.name,
                "(%s)" % ", ".join([str(p) for p in self.parameter_list]))

class _parse_cmdline:
    """
    argument-list ::= argument-list [ "," ] argument | argument
    full-argument ::= argument-list [ "->" argument-list ]
    command-line ::=
        command [ '!' ] ':'
        full-argument
    """
    def __init__(self, cl):
        # IMPORTANT: we locate the failure use subtraction from full_len
        full_len = _len(cl)
        self.essential = False
        self.argument_list = []
        self.assignment_list = []
        self.command = ""

        # leave the command of empty lines empty
        if not cl[0].strip(): return

        self.command = _parse_symbol(cl)
        if not self.command: raise PolicyParsingError(
                "Missing command name", col = full_len - _len(cl))

        self.essential = _parse_sign(cl, "!")
        has_colon = _parse_sign(cl, ":")
        if not has_colon: raise PolicyParsingError(
                "Missing colon ':'", col = full_len - _len(cl))

        try:
            while True:
                self.argument_list += [_parse_argument(cl)]
        except PolicyParsingError, e:
            # argument failuare is not an error
            e.col += full_len - _len(cl)

        has_arrow = _parse_sign(cl, "->")
        if not has_arrow and cl[0].strip():
            # end of line is reached
            raise PolicyParsingError(
                "Missing arrow '->'", col = full_len - _len(cl))
        else:

            has_comma = False
            try:
                while True:
                    self.assignment_list += [_parse_argument(cl)]
                    has_comma = _parse_sign(cl, ",")
            except PolicyParsingError, e:
                e.col += full_len - _len(cl)
                # if the end of line is reached, reading finised and no error
                if cl[0][e.col:].strip() or has_comma: raise e

    def __str__(self):
        return "%s%s: %s -> %s" % (self.command,
                "!" if self.essential else "",
                "[ %s ]" % ", ".join([str(a) for a in self.argument_list]),
                "[ %s ]" % ", ".join([str(a) for a in self.assignment_list]),
            )

class parse_policy:
    r"""
    policy ::=
        policy \n command-line | command-line
    """
    def __init__(self, pf):
        self.command_line_list = []

        pf = pf.split("\n")
        try:
            for ln_num, ln in enumerate(pf):
                self.command_line_list += [_parse_cmdline([ln])]
        except PolicyParsingError, e:
            e.row = ln_num
            raise e


