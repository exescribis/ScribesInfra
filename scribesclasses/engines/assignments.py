# coding: utf-8

"""

Ensure that assignements are up to date and create them if necessary.
"Assignements" are collections of "Works" in a given "CaseStudy".

Assignements are represented as following:

*   .assignments directories in headquarters subdirectories contain
    the different work for each assignements.
    There is one subdirectory for each work:

    *   ``work.info.json`` describes the labels and milestones.
    *   ``work.text.md`` contains the text of work definition and then
        the text of work items (separated by ________)
    *   ``work.issues.gen.txt`` is created and updated by this module and
        contains issue numbers created on github.

*   the file ``assignment-status.json`` at the root of the headquarters
    directory list the assignements and their status. Use ``CREATE``
    in order to create new work.

*   Issues on GitHub represents work definitions and work items.

"""

import os

import githubbot
from scribesclasses.models.assignments import Assignment


class ClassroomAssignmentEngine(object):
    def __init__(self, classroom):
        self.classroom = classroom
        self.assignments = {}

    def _assignment(self, assignmentName):
        """
        Create an assignment object.
        Use "publish" method to publish it.
        :param assignmentName: the assignment name such as CaseStudy/doThat
        :return: the assignmment created
        """
        assignment = Assignment(self.classroom, assignmentName)
        self.assignments[assignmentName] = assignment
        return assignment

    def showAssignment(self, assignmentName):
        a = self._assignment(assignmentName)
        a.showWork()

    def publishAssignment(self, assignmentName):
        a = self._assignment(assignmentName)
        a.publishWork()

    def build(self, arguments=()):
        assignment_status_file = os.path.join(
            self.classroom.hq.dir,
            'assignments.json')
        if not os.path.isfile(assignment_status_file):
            print( 'WARNING: no status file found. %s' % assignment_status_file)
            print('         Assuming that no assignements are to be processed')
        else:
            assignments = githubbot.load_json(assignment_status_file)
            assignments_by_status = {}
            for a_name, a_status in assignments.iteritems():
                if a_status not in assignments_by_status:
                    assignments_by_status[a_status] = []
                assignments_by_status[a_status].append(a_name)
                print("=======  Assignment",a_name,a_status)
                if a_status == "CREATE":
                    a = self._assignment(a_name)
                    a.publishWork()
            print(', '.join(
                    '%d "%s"' % (len(assignments),status)
                    for (status,assignments) in assignments_by_status.iteritems()))
