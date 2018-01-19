"""
The module :py:module:`commandset` provides an abstraction layer on
top of the standard standard python module :py:module:`argparse` to create
CLI like::

    python manage.py <command> <common-parameter> ... <specific-parameter> ...

Various "commands" are supported with the same program called "command set".
Some "arguments" are common to all commands, some are specific to each command.

The whole set of commands are instances of :py:class`CommandSet` which are basically
a set of "command", each command being an instance of :py:class`Command`.

Additionaly to ``CommandSet`` and ``Command``, concepts includes "arguments"
and "parameters". Arguments and commands are not represented explicitly however:

* "arguments" are specfications of textual representations on the command line,
  that is are unparsed, "concrete syntax", formal elements.
* "parameters" are the results of concrete parsing. Parameters are given to the
  command to be executed via the ``do`` method. Collections of parameters
  are represented as :py:class:`-.Namespace`.

"Common arguments" (or common parameters) are defined at the :py:class`CommandSet`
level (via the method :py:meth:`~.addCommonArguments`). These are available to
all commands.

By contrast "specific arguments" (or specific parameters) are defined at
:py:class`Command` level (via the method :py:meth:`~.addArguments`).

This very simple framework is intented to be used via subclassing.
See the scribesclasses.manage.py for example of use.
"""
import argparse

# import termcolor if available. Useful for colored output.
try:
    import termcolor
    cprint = termcolor.cprint
except:
    def cprint(text,color):
        print text



class CommandSet(object):
    """
    A set of "Command" represented CLI like ``python manage.py <command> ...``.
    Once created this set should be populated with :py:classCommand objects.

    All common parameters are to be defined at once using the method addCommonArguments.
    The following parameters are added in all cases:

    * ``-h``, ``--help`` show an help message
    * ``--csdebug`` enable command set debugging

    Some class attributes can be redefined.
    See https://docs.python.org/2/library/argparse.html#argumentparser-objects
    """
    prog='python manage.py'
    """The way to launch the program. Default is 'python manage.py', but this could be redefined"""

    usage=None
    """ optional usage text of the CommandSet to change the help output """

    description=None
    """ optional description of the CommandSet to change the help output """

    def __init__(self):
        """
        Build an empty CommandSet. This command set should then
        be populated with the :py:meth:`~.CommandSet.addCommand` method.

        The constructor of the super-class must be called explicitely like this::

            super(MyCommandSet, self).__init__()

        Returns:
             CommandSet: An empty command set. Commands are to be added.
        """

        self.commands = []
        self.mainParser =  argparse.ArgumentParser(
            prog=self.prog,
            usage=self.usage,
            description=self.description)
        self.subParsers = self.mainParser.add_subparsers(
            title='commands',
            dest='command')
        self.commonArgumentParser = argparse.ArgumentParser(add_help=False)
        self.commonArgumentParser.add_argument(
            '--csdebug',
            action='store_true',
            help='command set debugging')
        self.addCommonArguments()

    def addCommand(self, command):
        """
        Add a command to the "command set".

        A standard practice is for the client code to call this method,
        once after each command creation. This could look like ::

            COMMAND_SET = MyCommandSet()
            COMMAND_SET.addCommand(MyCommand1())
            COMMAND_SET.addCommand(MyCommand2())
            # ...

        Args:
            command (Command): the command to be added

        Returns:
            None
        """
        assert isinstance(command, Command)
        command.commandSet = self
        command.subParser = self.subParsers.add_parser(
            parents=[self.commonArgumentParser],
            name=command.name,
            help=command.help,
            description=command.description)
        command.addArguments()
        command.subParser.set_defaults(func=command.do)

    def addCommonArguments(self):
        """
        Add common arguments to all commands.

        This method does nothing by default. It could be redefined by subclasses.
        A common practice is to redefined it like this::

            class MyCommandSet(commandset.CommandSet):

                def addCommonArguments(self):
                    self.commonArgumentParser.add_argument( ... )
                    self.commonArgumentParser.add_argument( ... )
                    ...

        Returns:
            None
        """
        pass

    def addDerivedParameters(self, parameters):
        """
        Add "derived" parameters to the map of ``parameters`` given ... as parameter.
        The ``parameters`` variable is modified in place.
        This allows to make some check on common parameters and add
        derived parameters from them.
        This method does nothing by default.
        It could be redefined by sublcasses.

        Args:
            parameters (argparse.Namespace): A collection of parameters.

        Returns:
            None: The ``parameters`` collection is modified in place.
        """
        pass

    def computeParameters(self, stringArgs):
        """
        This method transforms a command line arguments (concrete syntax)
        into a map of "parameters". This method will call the
        py:meth:`~.CommandSet.addDerivedParameters` method.

        This method is not intended to be subclassed.
        it is not necessary to called it either.
        This method is called bythe :py:meth:`~.CommandSet.do` command.

        Args:
            stringArgs (list[string]): the list of actual arguments (e.g. from the command line)

        Returns:
            args.Namespace: A namespace containing all parameters that can be extracted
            from the command line plus some derived parameters (see the method
            :py:meth:`~.CommandSet.addDerivedParameters`)
        """
        parameters = self.mainParser.parse_args(stringArgs)
        self.addDerivedParameters(parameters)
        return parameters


    def do(self, stringArgs):
        """
        Execute the 'do' method of the selected command after
        argument parsing.
        The step are basically the following:

        *   the actual "arguments" are parsed. The selected command is set.
            The "parameters" are set according to argument values.

        *   the :py:meth:`~.Command.do` method of the selected
            command is executed, taking the computed
            "parameters" as parameter.

        :param stringArgs:
        :return: Any
        """

        def _p(text):
            cprint(text, 'green')

        def __print_parameters(args, params):
            _p('#'*80)
            _p( 'DEBUG: execution of command' )
            _ = ' '.join(args)
            _p( '-'*len(_) )
            _p( _ )
            _p( '-'*len(_) )
            map = vars(params)
            for key in map:
                _p( key.ljust(10)+' = '+str(map[key]) )
            _p( '='*80 )

        def __print_exec_prolog():
            _p( 'executing ...' )
            _p( '>'*80 )
            # _p( ' ' )

        def __print_exec_epilog():
            _p( ' ' )
            _p( '<'*80 )
            _p( 'execution done. Result = '+str(result) )
            _p( '#'*80 )


        parameters = self.computeParameters(stringArgs)

        if parameters.csdebug:
            __print_parameters(stringArgs, parameters)
            __print_exec_prolog()

        result = parameters.func(parameters)

        if parameters.csdebug:
            __print_exec_epilog()

        return result



class Command(object):
    """
    Abstract class to be subclassed by each command.
    Some class attributes must/could be redefined.
    """

    # See https://docs.python.org/2/library/argparse.html#argumentparser-objects
    name=''
    """ Must be redefined in subclasses"""

    help=''
    """ Could be redefined in subclasses """

    description= None
    """ """

    def __init__(self):
        """
        Dummy constructor for documentation purpose only.
        It is not necessary to call this constructor.
        The field are filled by the addCommand of CommandSet
        """
        self.commandSet = None   # This will be updated by addCommand
        self.subParser  = None   # This will be updated by addCommand

    def addArguments(self):
        """
        This method must be defined for each subclass.
        It should takes the following form::

            self.supParser.add_argument( 'param1', ... )
            self.supParser.add_argument( 'param2', ... )

        See the ``ArgumentParser.add_argument`` method in the standard library
        for more details :
        https://docs.python.org/2/library/argparse.html#the-add-argument-method

        :return: None
        """
        pass

    def do(self, args):
        pass


