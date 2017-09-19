import os

from scribesclasses.models import works


class Assignment(object):

    def __init__(self, classroom, assignmentPath):
        self.classroom = classroom
        self.assignmentPath = assignmentPath
        self.assignmentName = os.path.basename(assignmentPath)
        self.assignmentDirectory = os.path.join(
                classroom.hq.path(os.path.dirname(assignmentPath)),
                '.assignments', self.assignmentName)
        print(self.assignmentDirectory)
        assert(os.path.isdir(self.assignmentDirectory))
        self.workName = self.assignmentName
        self.workDirectory = self.assignmentDirectory
        assert(os.path.isdir(self.workDirectory))
        self.work = works.Work(
                self.workDirectory,
                self.classroom.org(),
                self.classroom.root.name,
                self.classroom.groupList.keys(),
                self.classroom.groupList.factory.repoName())

    def showWork(self):
        self.work.show()

    def publishWork(self, definitionOnly=False):
        self.work.save(definitionOnly=definitionOnly)