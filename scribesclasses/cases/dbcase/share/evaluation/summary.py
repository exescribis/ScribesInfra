import os
import glob
import scribesclasses.models.classrooms
import sys

POINTS={
        'O' : 5,
        '^' : 4,
        'x' : 1,
        '|' : 1,
        '-' : 1,
        '#' : 1,
        '$' : 0,
        '.' : 0
        }

MAX_POINTS = max(POINTS.values())

def points(status):
    return POINTS[status]

def caseBuildDir(classroom, case):
    return classroom.localHQRepoPath(
        os.path.join(case, '.build'))

def queryNames(classroom, case):
    expectedStatesDir = classroom.localHQRepoPath(os.path.join(case,'ExpectedStates'))
    pattern=os.path.join(expectedStatesDir,'*_*.csv')
    return [
        os.path.splitext(os.path.basename(csvfile))[0]
        for csvfile in glob.glob(pattern)]

def caseGroupBuildDir(classroom, case, key):
    return os.path.join(caseBuildDir(classroom,case), key)

def caseGroupBuildDirs(classroom, case):
    return [
        caseGroupBuildDir(classroom, case, key)
        for key in classroom.groupList.keys() ]

def caseGroupBuildFile(classroom, case, queryName, key, suffix):
    dir = caseGroupBuildDir(classroom, case, key)
    return os.path.join(dir, queryName+suffix)

def caseGroupQuerySummary(classroom, case, queryName, key):
    file = caseGroupBuildFile(classroom, case, queryName, key, '.summary.txt')
    try:
        with open(file, 'r') as f:
            content = f.read().strip()
    except:
        content='?'
    return content


class SummaryMatrix(object):

    def __init__(self, classroom, case):
        self.classroom = classroom
        self.case = case
        self._matrix = {}

        #: [(queryName,key)] -> result
        self.queryNames = queryNames(classroom, case)
        self.groupKeys = classroom.groupList.keys()
        for queryName in self.queryNames:
            for key in self.groupKeys:
                summary = caseGroupQuerySummary(classroom, case, queryName, key)
                self._matrix[(queryName,key)] = summary
            #     print summary + ' ',
            # print queryName

    def groupPoints(self, groupKey):
        _ = 0
        for queryName in self.queryNames:
            _ += points(self._matrix[(queryName,groupKey)])
        return _

    def lines4Queries(self):
        _ = ''
        for queryName in self.queryNames:
            for key in self.groupKeys:
                _ = _ + ("%s " % self._matrix[(queryName,key)])
            _ = _ + queryName + '\n'
        return _

    def display(self):
        print(self.lines4Queries())
        # for queryName in self.queryNames:
        #     for key in self.groupKeys:
        #         print self._matrix[(queryName,key)],
        #     print queryName
        print()
        for groupKey in self.groupKeys:
            print( '%s: %s points / %s' % (
                    groupKey,
                    self.groupPoints(groupKey),
                    len(self.queryNames)*MAX_POINTS ) )


#
#
# CLASSROOM = scribesclasses.models.classrooms.Classroom()
#
# for case in sys.argv[1:]:
#     m = SummaryMatrix(CLASSROOM, case)
#     m.display()