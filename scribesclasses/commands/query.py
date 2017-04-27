import commandset
import scribesclasses.cases.dbcase.share.evaluation.build


class QueryCommand(commandset.Command):
    name =          'query'
    help =          'build database queries'
    description =   'TODO'


    def addArguments(self):
        self.subParser.add_argument(
            'case')
        self.subParser.add_argument(
            'group')
        self.subParser.add_argument(
            'query')

    def do(self, parameters):
        # TODO: this should be rewritten to take into account manage.py std parameters
        scribesclasses.cases.dbcase.share.evaluation.build.build(
            caseParam=parameters.case,
            groupParam=parameters.group,
            queryParam=parameters.query,
            verbose='-v' if parameters.verbose>=1 else ''
        )