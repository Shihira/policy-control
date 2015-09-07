class context(object):
    """
    Context stores and manages runtime infomation like local-variables, the
    pointer pointing to currently running command, etc. The concrete content of
    context depends on command implementations.

    context is picklale, you can store it in persistent interface with pickle.
    attributes start with '_' are not going to be dumpped.
    each context has a unique id `context.id` after started

    A context is currently containing these fields(attributes):

    * id: id is for you to identify transactions
    * vars: variables to store in this transaction
    * ip: instructor pointer register :-)
    * _yield: yield record (not stored)
    * _preload: modules loaded with `load` command (not stored)

    """

    def __getattr__(self, attr):
        "Available expression: value = context[attr]"
        return self.__dict__[attr]

    def __setattr__(self, attr, value):
        "Available expression: context[attr] = value"
        self.__dict__[attr] = value
        return value

    def __getstate__(self):
        """
        Available expression: s = pickle.dumps(context)
        NOTE AGAIN: variables start with '_' are not going to be dumpped
        """
        dump = self.__dict__.copy()
        return dict(filter(lambda p: p[0][0] != "_", dump.items()))

    def __setstate__(self, d):
        "Available expression: context = pickle.loads(s)"
        self.__dict__.update(d)

    def __init__(self, **kwargs):
        "Available expression: context(attr1 = value1, attr2 = value2)"
        self.__dict__.update(kwargs)

    def __len__(self):
        "Available expression: bool(context)"
        return len(self.__dict__)

    def __delattr__(self, attr):
        del self.__dict__[attr]

    def ensure(self, attr, init = None):
        """
        If an attribute exists return it directly, otherwise
        initialize it with `init`
        """
        if not hasattr(self, attr):
            self.__setattr__(attr, init)
        return self

    def clear(self):
        self.__dict__.clear()

    @staticmethod
    def start_new():
        "start a new context/session, with default context value initialized"
        import os

        return context(
                id = os.urandom(32),
                vars = { },
                ip = 0,
                _yield = [ ],
                _preload = [ ],
                _await_tags = [ ],
            )

