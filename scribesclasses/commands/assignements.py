import commandset
import githubbot.accounts
import scribesclasses.engines.assignments

class AssignmentsCommand(commandset.Command):
    name =          'assignments'
    help =          'generate assignments on GitHub'
    description =   'create assignements on github if they have the CREATED status in assignement-status.json'

    def addArguments(self):
        self.subParser.add_argument(
            'subcommand',
            choices=['publish', 'show'])
        self.subParser.add_argument(
            'assignmentName')

    def do(self, parameters):
        githubbot.accounts.gitHubSession(parameters.user)
        engine = scribesclasses.engines.assignments.ClassroomAssignmentEngine(parameters.classroom)
        if parameters.subcommand == 'show':
            engine.showAssignment(parameters.assignmentName)
        elif parameters.subcommand == 'publish':
            engine.publishAssignment(parameters.assignmentName)
        else:
            print("unkown command '%s'" % parameters.subcommand)

        # githubbot.accounts.gitHubSession(parameters.user)
        # engine = scribesclasses.engines.assignments.ClassroomAssignmentEngine(parameters.classroom)
        # engine.build()
        # TODO: implement the 'assignements' command
        #     engine.build() is not working direclty
        #     the test_assignments is working but not using .build()

