import os

class ClassroomEvalEngine(object):
    """
    Execute the eval.sh of each case.
    The current implementation is based on res/bin/eval.sh but this should be changed.
    """

    def __init__(self, classroom):
        self.classroom = classroom

    def build(self, arguments):
        self.hqDirectory = self.classroom.hq.dir
        this_dir=os.path.dirname(os.path.realpath(__file__))
        script=os.path.join(this_dir,'res','bin','eval.sh')
        command=script+' '+self.hqDirectory+' '+' '.join(arguments)
        print(command)
        os.system(command)