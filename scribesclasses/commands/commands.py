import commandset

import scribesclasses.engines.commands

class CommandsCommand(commandset.Command):
    name =          'commands'
    help =          'generate commands that apply on all groups'
    description =   'TODO'

    def do(self, parameters):
        engine = scribesclasses.engines.commands.ClassroomCommandsEngine(parameters.classroom)
        engine.build()