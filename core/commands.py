import policy

def _assign_vars(value, containers, context):
    # try to unpack tuples
    if len(containers) > 1:
        if isinstance(value, tuple) and len(containers) == len(value):
            for elem_i, elem in enumerate(value):
                context.vars[containers[elem_i]] = elem
        else: raise ValueError("Unable to unpack %s" % str(value))
    # general value assignment
    elif len(containers) == 1:
        context.vars[containers[0]] = value

def _call_func(funcname, param, context):
    ret = None
    found = False
    for module in context._preload:
        if hasattr(module, funcname):
            found = True
            ret = getattr(module, funcname)(*param)
            break

    if not found:
        raise NameError("Symbol %s not found" % str(func.name))

    return ret


def _load(cmdline, context):
    context._preload += \
        [__import__(cmdline.arguments[0].name)]

def _apply(cmdline, context):
    func = cmdline.arguments[0]
    param = [ p.evaluate(context) for p in func.parameters ]
    assign = [a.name for a in cmdline.assignments]

    ret = _call_func(func.name, param, context)
    _assign_vars(ret, assign, context)

def _yield(cmdline, context):
    vars_to_yield = [context.vars[a.name] for a in cmdline.arguments]
    context._yield += vars_to_yield

def _await(cmdline, context):
    tag_request = cmdline.arguments[0].name
    assign = [a.name for a in cmdline.assignments]

    value = None
    found = False

    for at_i, at in enumerate(context._await_tags):
        at, at_value = at

        if at == tag_request:
            del context._await_tags[at_i]
            value = at_value
            found = True
            break

    if not found:
        raise policy.SleepPolicy()

    _assign_vars(value, assign, context)


def _assert(cmdline, context):
    assertion = cmdline.arguments[0]
    param = [ p.evaluate(context) for p in assertion.parameters ]
    assign = [a.name for a in cmdline.assignments]

    ret = None

    try: ret = _call_func(assertion.name, param, context)
    except NameError:
        ret = context.vars[assertion.name]

    assert(ret)

command_dict = {
        "load":   _load,
        "apply":  _apply,
        "await":  _await,
        "yield":  _yield,
        "assert": _assert,
    }
