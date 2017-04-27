"""
Evaluation of database queries.
The build() method is called from manage.py.
The code could be executed from a group directory or from
headquarters. For group directory the group must be '.'.
"""
import os
import summary
import scribesclasses.models.classrooms

__all__ = ['build']

THIS_DIR=os.path.dirname(__file__)



def build(caseParam, groupParam='all', queryParam='all', verbose='-v'):
    """
    Build the queries by running the script bin/build-query.sh
    and then display a matrix
    """


    def _callBuildScript(case, group, query, verbose):

        def _buildQueryScript():
            return os.path.join(
                os.path.dirname(__file__),
                'bin', 'build-query.sh')

        command='%s %s %s %s %s' % (
            _buildQueryScript(),
            case,
            group,
            query,
            verbose
        )
        os.system(command)

    classroom = scribesclasses.models.classrooms.Classroom()

    if groupParam=='all':
        group_keys = classroom.groupList.keys()
    else:
        group_keys = [ groupParam ]

    for group_key in group_keys:
        _callBuildScript(caseParam, group_key, queryParam, verbose)


    if groupParam=='all' and queryParam=='all':
        matrix = summary.SummaryMatrix(classroom, caseParam)
        matrix.display()