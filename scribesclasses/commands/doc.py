import commandset
import scribesclasses.engines.onweb


class DocCommand(commandset.Command):
    name =          'doc'
    help =          'generate documentation for the classroom'
    description =   'TODO'

    def addArguments(self):
        self.subParser.add_argument(
            'subcommand',
            choices=['groups','hq','publish', 'all'],
            help='ensure or delete'
                 ' For instance CyberXXX CyberYYY to eval only these case studies.'
                 ' If no case study is supplied all cases study will be evaluated.')

    def do(self, parameters):
        engine = scribesclasses.engines.onweb.ClassroomOnWebEngine(
            parameters.classroom
        )
        if parameters.subcommand == 'groups':
            engine.generateAllGroupDocs()
        elif parameters.subcommand == 'hq':
            engine.generatedHQDocs()
        elif parameters.subcommand == 'publish':
            engine.publishAllDocs()
        elif parameters.subcommand == 'all':
            engine.build()
        else:
            raise SyntaxError('command not implemented: %s' % parameters.subcommand)