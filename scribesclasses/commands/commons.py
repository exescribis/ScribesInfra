import commandset
import os
import sys

import scribesclasses.models.classrooms

class ManageCommandSet(commandset.CommandSet):
    # prog='python manage.py'  # could redefined the parent class
    description=    'manage.py allows to manage classrooms thanks' \
                    ' to different sub commands'

    def __init__(self):
        super(ManageCommandSet, self).__init__()

    def addCommonArguments(self):
        self.commonArgumentParser.add_argument(
            '-tg', '--testgroup',
            nargs='?',
            default=None,
            const='00',
            help='Key of the testing group. Default to "00".')
        self.commonArgumentParser.add_argument(
            '-u', '--user',
            default='scribesbot',
            help='User used to connect to github. Default to "scribesbot".')
        # self.commonArgumentParser.add_argument(
        #     '-l', '--localroot',
        #     default='~/DEV',
        #     help='Path to root local root directory directory containing organizations (e.g. m2r).'
        #          ' Default to "~/DEV".')
        self.commonArgumentParser.add_argument(
            '-c', '--classroomfile',
            default='./classroom.json',
            help='Path to the file "classroom.json". Default to "./classroom.json". ') #, type=argparse.FileType('r'))
        self.commonArgumentParser.add_argument(
            '-g', '--group',
            nargs='*',
            help='Group or list of group keys (e.g. "-g 12" or "-g 01 02 07").'
                 ' If this parameter is not specified all groups in the classroom will be selected')
        self.commonArgumentParser.add_argument(
            '-v', '--verbose',
            action='count',
            default=0,
            help='verbosity level of output. Repeat -v options'
                 ' to increase verbosity (e.g. -vvv)')

    def addDerivedParameters(self, parameters):
        # introducing a new variables with vars is necessary to change/add parameters
        paramvars=vars(parameters)

        def getClassroomValue():
            if not os.path.isfile(parameters.classroomfile):
                sys.stderr.write(
                    ('ERROR: classroom file "%s" not found. '
                    + ' You should move to a hq directory.\n') % parameters.classroomfile)
                sys.exit(2)
            else:
                return scribesclasses.models.classrooms.Classroom(
                    classRoomFile=parameters.classroomfile,
                    testingKey=parameters.testgroup,
                    defaultAccountInfo=parameters.user
                )

        paramvars['classroom'] = getClassroomValue()
