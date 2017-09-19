# coding: utf-8

"""
Command line front end.
This module just call the functions available in the different modules.
"""

import sys
import commandset


from scribesclasses.commands.commons import ManageCommandSet
from scribesclasses.commands.assignements import AssignmentsCommand
from scribesclasses.commands.changespec import ChangeSpecCommand
from scribesclasses.commands.commands import CommandsCommand
from scribesclasses.commands.doc import DocCommand
from scribesclasses.commands.github import GHCommand
from scribesclasses.commands.query import QueryCommand

class EvalCommand(commandset.Command):
    # commandSet=Manage
    name=           'eval'
    help=           'evaluate one or more case study'
    description=    'The eval command evaluate a given set of case study' \


    def addArguments(self):
        self.subParser.add_argument(
            'case',
            nargs='*',
            help='--csprint name(s) of the case study to be evaluated.'
                 ' For instance CyberXXX CyberYYY to eval only these case studies.'
                 ' If no case study is supplied all cases study will be evaluated.')

    def do(self, parameters):
        print(parameters)
        print('eval with : ('+' '.join(parameters.case)+')')




def execute(arguments):
    COMMAND_SET = ManageCommandSet()
    COMMAND_SET.addCommand(DocCommand())
    COMMAND_SET.addCommand(CommandsCommand())
    COMMAND_SET.addCommand(GHCommand())
    COMMAND_SET.addCommand(AssignmentsCommand())
    COMMAND_SET.addCommand(EvalCommand())
    COMMAND_SET.addCommand(ChangeSpecCommand())
    COMMAND_SET.addCommand(QueryCommand())
    COMMAND_SET.do(arguments)


def main():
    execute(sys.argv[1:])

if __name__ == "__main__":
    HOST = sys.argv[1]          # CENTRAL | USER | BOT | UNDEFINED
    REPO_NAME = sys.argv[2]     # e.g. l3miage-bdsi-hq | l3miage-bdsi-G00
    DIRECTORY = sys.argv[3]     #

    # print "HOST=%s" % HOST
    # print "REPO_NAME=%s" % REPO_NAME
    # print "DIRECTORY=%s" % DIRECTORY

    execute(sys.argv[4:])

    # echo "VIRTUAL_ENV"=$VIRTUAL_ENV
    # echo "PY_PATH"=$PY_PATH
        #, 'l3miage-bdsi-hq', '/home/jmfavre/DEV/l3miage/l3miage-bdsi-hq'

    # print "called: ",sys.argv
    # exit(0)
    # for cmd in [
    #         #'eval --help',  # help will exit as its normal behavior
    #         'eval stoto',
    #         'eval toto titi',
    #         'eval case1',
    #         'eval --classroom manage.py  ',
    #         'eval --classroom manage.py  toto titi ',
    #         'eval --classroom /a/b/classroom.json -g 1 2 3 -vvv',
    #         'eval --classroom /a/b/classroom.json --group 1 2 3',
    #         'eval case1 case2 -u escribis -tg --classroom /a/b/classroom.json --group 1 2 3',
    #         'eval case1 case2 -u escribis -tg 01',
    #         # 'changespec mydir',
    #         # '--help',
    #         '--help'
    #     ]:
    #     # print '='*80+'\n'+cmd+'\n'
    #     # print '-'*30+'\'n'+str(COMMAND_SET.mainParser)
    #     # params=COMMAND_SET.getParameters(cmd.split())
    #     #print str(params)+'\n----\n'
    #     # r = COMMAND_SET.do(cmd.split())
    #     # print "result="+str(r)
    #     # args.func(args)
    #     execute(cmd.split())
    #     print()
    #     print()


