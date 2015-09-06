class parameters(object):

    def __init__(self):
        self._type = ""
        self.value = ""

    def assign(self, parser):
        self._type = parser.param_type
        self.value = parser.value

        return self

class argument(object):

    def __init__(self):
        self.name = ""
        self.paramenters = []

    def assign(self, parser):
        self.name = parser.name
        self.paramenters = [ parameter().assign(p)
                for p in parser.parameter_list ]

        return self

class cmdline(object):

    def __init__(self):
        self.command = ""
        self.arguments = []
        self.assignments = []

    def assign(self, parser):
        self.command = parser.command
        self.arguments = [ argument().assign(a)
                for a in parser.argument_list ]
        self.assignments = [ argument().assign(a)
                for a in parser.assignment_list ]

        return self

class policy(object):

    def __init__(self):
        self.cmdlines = []

    def assign(self, parser):
        self.cmdlines = [ cmdline().assign(c)
                for c in parser.command_line_list ]

        return self

    @staticmethod
    def load(policy_file):
        """
        It can load either a file object or a string contains policy content,
        and return the policy object, acting as a factory method.
        """

        if isinstance(policy_file, file):
            policy_file = policy_file.read()
        elif not isinstance(policy_file, str):
            raise TypeError("%s is neither a file nor a string" % policy_file)

        from parser import _parse_policy
        return policy().assign(_parse_policy(policy_file))

