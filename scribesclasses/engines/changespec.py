

"""
Define change specifications (changespec) that allows to check if changes
to a directory conform to a change specification.
"""
import os

from changecontrol.changespec import ChangeSpecification
from changecontrol.changespec import directory2ChangeSpecificationFile
from changecontrol.comparison import DirectoryComparison


# # use less now because of
# def readDefaultFileSetFromDirectory(directory):
#
#     # the variable below is used to remove the directory from the path returned
#     directory_len = len(directory.split(os.path.sep))
#     paths = []
#     for root, dirs, files in os.walk(directory):
#         sub_dir = os.path.sep.join(root.split(os.path.sep)[directory_len:])
#         # print '*%s*=*%s*'%(root,sub_dir)
#         for name in dirs:
#             if sub_dir != '':
#                 path = os.path.join(sub_dir, name)+os.path.sep
#             else:
#                 path = name+os.path.sep
#             paths.append(path)
#         for name in files:
#             paths.append(os.path.join(sub_dir, name))
#     return paths


IGNORE_NAMES = ['.git','.work']


class ClassroomChangeSpecEngine(object):
    """
    """

    def __init__(self, classroom, directory):
        self.classroom = classroom
        self.hq_changespec_file = \
            self.classroom.localHQRepoPath(
                os.path.join(directory,'.changespec'))
        self.directory = directory
        self.root_directory = \
            self.classroom.localRootRepoPath(directory)

    def _groupDirectory(self, key=None):
        return self.classroom.localGroupRepoPath(
            key=key,
            path=self.directory)

    def _compareDirectory(self, key, directory, filter='*'):
        change_spec = ChangeSpecification.fromFile(self.hq_changespec_file)
        dc = DirectoryComparison(
            self.root_directory,
            self._groupDirectory(key),
            IGNORE_NAMES)
#       dc.showTree(acceptFun=change_spec.accept)
        print('-'*80)
        dc.showFlatList(acceptFun=change_spec.accept,filter=filter)
#        for item in dc.itemStatusByRelativePath.values():
#            print item.relativePath, CHANGESPEC.accept(item)

    def compare(self, group='all', filter='*'):
        print("O"*200)
        print(group)
        if group == 'all':
            groups = self.classroom.groupList.keys()
        else:
            groups = [ group ]

        for key in groups:
            print('='*80)
            print('%s: Comparing group %s directory  %s'
                  % (key, key, self.directory))
            self._compareDirectory(
                directory=self.directory,
                key=key,
                filter=filter
            )

    def init(self):
        directory2ChangeSpecificationFile(
            root=self.root_directory,
            outputFile=self.hq_changespec_file,
        )
        print('%s saved' % self.hq_changespec_file)