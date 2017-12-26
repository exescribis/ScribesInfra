from __future__ import print_function
import commandset

import githubbot.accounts
import scribesclasses.engines.github.classrooms

D="""
This command reads a classroom.json file and create/edit/delete
the corresponding github artefacts.
"github ensure" will make sure that github entities exist.
"github delete" will delete github entities. Use with CAUTION!
"""
class GHCommand(commandset.Command):
    name =          'github'
    help =          'update the github representation of a classroom'
    description =   D

    repoIds=('root','hq', 'info', 'web', 'groups')

    def addArguments(self):
        self.subParser.add_argument(
            'subcommand',
            choices=['ensure','delete'],
            help='ensure or delete'
                 ' For instance CyberXXX CyberYYY to eval only these case studies.'
                 ' If no case study is supplied all cases study will be evaluated.')
        self.subParser.add_argument(
            'spec',
            default=GHCommand.repoIds,
            help='Some of root hq info web groups labels milestones teams members',
            nargs='*'
        )

        # TODO: add a parameter to ensure labelsSpec/milestones

    def do(self, parameters, prefix=''):

        course = parameters.classroom.course
        if prefix is not None:
            print(
                (prefix+'Login to github as %s\n'
                'Make sure that %s "owner" of the organization')
                % (parameters.user, parameters.user) )
        githubbot.accounts.gitHubSession(parameters.user)
        engine = scribesclasses.engines.github.classrooms.ClassroomOnGHEngine(
            parameters.classroom)
        if parameters.subcommand == 'ensure':
            if prefix is not None:
                print(
                    prefix+"Ensuring %s" % ' '.join(parameters.spec))
            engine.ensureAtGH(
                repoIds=[id for id in parameters.spec
                         if id in GHCommand.repoIds],
                ensureLabels='labels' in parameters.spec,
                ensureMilestones='milestones' in parameters.spec,
                ensureTeams='teams' in parameters.spec,
                readMembers='members' in parameters.spec)
            if prefix is not None:
                print("\n===> All github items are there.")
                print('\n\nWHAT REMAIN TO BE DONE:')
                print('- Populating the teams')
                print('- Associating the teams with the group')
        elif parameters.subcommand == 'delete':
            print('You are about to DELETE ALL stuff on github for the course %s' % course)
            answer = raw_input('IS THIS REALLY WANT YOU WANT ? ARE YOU EVIL ?')
            if answer != '666':
                print("Deletion cancelled")
            else:
                # FIXME: this currently raise an exception
                #       github.py, line 53, in deleteGroupAtGH
                #       group.ghRepo.delete()
                #       AttributeError: 'NoneType' object has no attribute 'delete'
                #
                # This is due to the fact that group.ghRepo is initialized only in the ensure case
                # This works with the test, but not here because ensure is not executed before
                # This should be fixed.
                print("Deleting all github items for course %s " % course)
                engine.deleteAtGH(666)
                print("done")
