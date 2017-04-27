# coding: utf-8

import collections
import re

WORK_SUBTASKS_PATTERN       = """ *[-*] *\[(?P<status>[Xx ])\] *\((?P<id>[0-9]*)\) (?P<title>.*)"""


class WorkItemSubstaskProgress(object):
    """
    Represented by a line in each work item for each.
    Each group can check if the subtask has been performed or not.
    A `Subtask` represented in work items by à line items.
    line matching WORK_SUBTASKS_PATTERN. It could looks like
        - [ ] (2) Specification of the problem module
    """

    def __init__(self, groupKey, id, title, status):
        #: string groupKey
        self.groupKey = groupKey

        #: string id
        self.id = id

        #: string  title
        self.title = title.strip()  # striping is necessary because github add some \r

        #: a boolean indicating if the subtask is completed or not
        self.status = status

    @staticmethod
    def matchLine(line):
        return re.match(WORK_SUBTASKS_PATTERN, line)

    def __str__(self):
        return "%s:%s:%s" % (self.groupKey, self.id, "X" if self.status else ".")


class WorkItemSubtasksProgress(object):
    """
    A set of subtasks for a given workitem.
    Could looks like this in the work item github issue

        - [x] (1) Specification of the problem module
        - [x] (2) Implementation useless elements emoval
        - [ ] (3) Write down documentation for the problem module

    """
    def __init__(self, groupKey, text, workItemClosed=None):
        # ..... init .................................

        #: str
        self.groupKey = groupKey
        #: str  text defining the subtasks (in work item)
        self.text = text

        #: dict[string,WorkItemSubtask]
        #: filled by _extractSubtasks()
        self.__subtasks = self.__extractSubtasks(groupKey, self.text)

        #: bool|None  is the work item issue closed ?
        #:    True=done, False=todo, None=Unkown (yet)
        self.workItemClosed = workItemClosed

    def subtask(self, id):
        return self.__subtasks[id]

    @property
    def subtaskIds(self):
        return self.__subtasks.keys()

    @property
    def subtasksCount(self):
        return len(self.subtaskIds)

    @property
    def subtaskTitles(self):
        return [st.title for st in self.__subtasks.values()]

    @property
    def couldBeClosed(self):
        return all((st.status for st in self.__subtasks.values()))

    @property
    def shouldBeClosedWarning(self):
        if self.workItemClosed is None:
            return None
        else:
            return (
                self.subtasksCount != 0
                and not self.workItemClosed
                and self.couldBeClosed )

    @property
    def shouldNotBeClosedWarning(self):
        if self.workItemClosed is None:
            return None
        else:
            return (
                self.subtasksCount != 0
                and self.workItemClosed
                and not self.couldBeClosed)

    def __extractSubtasks(self, groupKey, text):
        """
        Used by __init__
        :param text: the text to be analyzed
        :return: OrderedDict(id,WorkItemSubstaskProgress)
        """
        lines = text.split('\n')
        subtasks = collections.OrderedDict()
        for line in lines:
            m = WorkItemSubstaskProgress.matchLine(line)
            if m:
                subtasks[m.group('id')] = WorkItemSubstaskProgress(
                    groupKey=groupKey,
                    id=m.group('id'),
                    title=m.group('title'),
                    status=m.group('status') != ' '
                )
        return subtasks

    def __str__(self):
        return ' '.join(
            str(st) for st in self.__subtasks.values())

    def __repr__(self):
        return self.__str__()




class WorkSubtasksProgress(object):
    """
    We assume here that all workitems have the same subtasks.
    """

    def __init__(self):
        #: OrderedDict(str,WorkItemSubtasksProgress) For each group the workitems subtrask
        #: Will be filled with the add method
        self.__groupKeyToWorkItemSubtasks = collections.OrderedDict()
        #: The set of task ids. Filled with the add method
        #: We assume here that all workitems have the same subtasks.
        self.__subtaskIds = []
        #: We also assume that the titles does not change either
        self.__subtaskTitles = []

    @property
    def groupKeys(self):
        """ List of group keys """
        return self.__groupKeyToWorkItemSubtasks.keys()

    @property
    def subtaskIds(self):
        return self.__subtaskIds

    # @property
    # def subtaskTitles(self):
    #     return self.__subtaskTitles

    def _anyWorkItemSubtasks(self):
        wis = self.__groupKeyToWorkItemSubtasks.values()
        if len(wis) == 0:
            raise Exception('WorkSubtasksProgress: no group')
        else:
            return wis[0]


    def subtaskTitle(self, id):
        """
        Return the title of the given task. Because titles are assumed
        to be homogeneous between all workitems, they are all the same
        for a given subtask id. Raise an exception if this id does not
        exist.
        :param id: the subtask id (common to all workitems)
        :return: the title
        :raise: an exception if there is no group or if the id is not existing
        """
        st = self._anyWorkItemSubtasks()
        return st.subtask(id).title

    def workItemSubtask(self, groupKey, id):
        return self.__groupKeyToWorkItemSubtasks[groupKey].subtask(id)

    def add(self, workItemSubtasks):
        if len(self.groupKeys) == 0:
            # First call to add. We store the subtask ids.
            self.__subtaskIds = workItemSubtasks.subtaskIds
            self.__subtaskTitles = workItemSubtasks.subtaskTitles

        else:
            # Checking that the subtask ids are the same as before,
            # All work items must have the same tasks
            if workItemSubtasks.subtaskIds != self.__subtaskIds:
                print 'ERROR: the tasks ids for group %s do not match' % workItemSubtasks.groupKey
                print '   found  : %s' % str(workItemSubtasks.subtaskIds)
                print '   before : %s' % str( self.__subtaskIds)
                assert (workItemSubtasks.subtaskIds == self.__subtaskIds)
            # Checking that the title are the same as before
            if  workItemSubtasks.subtaskTitles != self.__subtaskTitles:
                print 'ERROR: the subtasksTitles for group %s no not match' \
                      % workItemSubtasks.subtaskTitles
                print '   found  : %s' % str(workItemSubtasks.subtaskTitles)
                print '   before : %s' % str( self.__subtaskTitles)
                assert(workItemSubtasks.subtaskTitles == self.__subtaskTitles)
        self.__groupKeyToWorkItemSubtasks[workItemSubtasks.groupKey] \
            = workItemSubtasks

    def linesForGroups(self):
        """
        Return a list of lines (list(str)) with one group on each line
        :return:
        """
        lines = []
        for g in self.groupKeys:
            line = 'Group %s:' %g
            for i in self.subtaskIds:
                line += 'X' if self.workItemSubtask(g,i).status else '.'
            lines += [line]
        return lines

    def linesForSubtasks(self):
        lines = []
        for i in self.subtaskIds:
            line = '(%s)' % i
            for g in self.groupKeys:
                line +=   'X' if self.workItemSubtask(g,i).status else '.'
            line += self.subtaskTitle(i)
            lines += [line]
        return lines