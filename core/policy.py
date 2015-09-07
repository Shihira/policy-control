from context import context
import commands

class SleepPolicy(Exception):
    pass

class parameter(object):

    def __init__(self):
        self._type = ""
        self.value = ""

    def assign(self, parser):
        self._type = parser.param_type
        self.value = parser.value

        return self

    def evaluate(self, context = None):
        if self._type == "string":
            return eval(self.value)
        elif self._type == "symbol":
            return context.vars[self.value]


class argument(object):

    def __init__(self):
        self.name = ""
        self.parameters = []

    def assign(self, parser):
        self.name = parser.name
        self.parameters = [ parameter().assign(p)
                for p in parser.parameter_list ]

        return self

class cmdline(object):

    def __init__(self):
        self.command = ""
        self.essential = False
        self.arguments = []
        self.assignments = []

    def assign(self, parser):
        self.command = parser.command
        self.essential = parser.essential
        self.arguments = [ argument().assign(a)
                for a in parser.argument_list ]
        self.assignments = [ argument().assign(a)
                for a in parser.assignment_list ]

        return self

    def run(self, context):
        commands.command_dict[self.command](self, context)

class policy(object):

    def __init__(self):
        self.cmdlines = []
        self.context = context()

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

    def load_context(c):
        self.context = c

    def provide(await_tag, value):
        self.context._await_tags += [(await_tag, value)]

    def resume(self):
        """
        Resume a policy from interruption:

        1. Run all essential(!) commands prior to breakpoint
        2. Keep on running from breakpoint until policy finished
        3. return yielded values
        """

        if not self.context:
            self.context = context.start_new()

        try:
            for ln, cmdline in enumerate(self.cmdlines):
                if cmdline.essential:
                    cmdline.run(self.context)
                elif ln == context.ip:
                    cmdline.run(self.context)

                context.ip += 1
        except SleepPolicy, e:
            return self.context._yield


