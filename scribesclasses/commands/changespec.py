import commandset

import scribesclasses.engines.changespec

class ChangeSpecCommand(commandset.Command):
    name =          'changespec'
    help =          'compare directory changes against a .changespec specification'
    description =   ''



    def addArguments(self):
        self.subParser.add_argument(
            'subcommand',
            choices=['init', 'compare'])
        self.subParser.add_argument(
            'directory')
        self.subParser.add_argument(
            'group',
            nargs='?')
        self.subParser.add_argument(
            '-f', '--filter',
            default='*',
            help='output filter')
    def do(self, parameters):
        engine = scribesclasses.engines.changespec.ClassroomChangeSpecEngine(
            classroom=parameters.classroom,
            directory=parameters.directory)
        if parameters.subcommand=='init':
            engine.init()
        elif parameters.subcommand=='compare':
            engine.compare(
                group=parameters.group,
                filter=parameters.filter
            )
        else:
            print('ERROR: subcommand %s not allowed' % parameters.subcommand)
