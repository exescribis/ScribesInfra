import commandset

import githubbot.accounts
import scribesclasses.engines.github

class GitHubCommand(commandset.Command):
    name =          'github'
    help =          'update the github representation of a classroom'
    description =   '"github ensure" will make sure that github repositories exist.\n' \
                    '"github delete" will delete github representation. Use with CAUTION!'


    def addArguments(self):
        self.subParser.add_argument(
            'subcommand',
            choices=['ensure','delete'],
            help='ensure or delete'
                 ' For instance CyberXXX CyberYYY to eval only these case studies.'
                 ' If no case study is supplied all cases study will be evaluated.')

        # TODO: add a parameter to ensure labelsSpec/milestones

    def do(self, parameters):
        course = parameters.classroom.course
        githubbot.accounts.gitHubSession(parameters.user)
        engine = scribesclasses.engines.github.ClassroomOnGitHubEngine(parameters.classroom)
        if parameters.subcommand == 'ensure':
            print("Ensuring that all github items are available for course %s" % course)
            # TODO: add the ensureLabels / ensureMilestone   from parameers
            engine.ensureAtGitHub(
                ensureLabels=True,
                ensureMilestones=True)
            print("done")
        elif parameters.subcommand == 'delete':
            print('You are about to DELETE ALL stuff on github for the course %s' % course)
            answer = raw_input('IS THIS REALLY WANT YOU WANT ? ARE YOU EVIL ?')
            if answer != '666':
                print("Deletion cancelled")
            else:
                # FIXME: this currently raise an exception
                #       github.py, line 53, in deleteGroupAtGitHub
                #       group.ghRepo.delete()
                #       AttributeError: 'NoneType' object has no attribute 'delete'
                #
                # This is due to the fact that group.ghRepo is initialized only in the ensure case
                # This works with the test, but not here because ensure is not executed before
                # This should be fixed.
                print("Deleting all github items for course %s " % course)
                engine.deleteAtGitHub(666)
                print("done")
